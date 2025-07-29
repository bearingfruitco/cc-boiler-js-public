"""
Architecture-PRP Mapper
Maps architecture changes to affected PRPs
"""

import re
from pathlib import Path
from typing import Dict, List, Set, Optional


class ArchitecturePRPMapper:
    """Maps architecture files to dependent PRPs"""
    
    def __init__(self, project_root: str = "/Users/shawnsmith/dev/bfc/boilerplate"):
        self.project_root = Path(project_root)
        self.prp_dir = self.project_root / "PRPs" / "active"
        self.arch_dir = self.project_root / "docs" / "architecture"
        self._dependency_cache = None
        
    def build_dependency_map(self) -> Dict[str, List[str]]:
        """Build map of architecture files to dependent PRPs"""
        if self._dependency_cache is not None:
            return self._dependency_cache
            
        dependency_map = {}
        
        # Scan all active PRPs
        if not self.prp_dir.exists():
            return dependency_map
            
        for prp_file in self.prp_dir.glob("*.md"):
            # Skip template files
            if prp_file.stem.startswith('_'):
                continue
                
            arch_deps = self.extract_architecture_dependencies(prp_file)
            
            for arch_file in arch_deps:
                if arch_file not in dependency_map:
                    dependency_map[arch_file] = []
                dependency_map[arch_file].append(str(prp_file))
        
        self._dependency_cache = dependency_map
        return dependency_map
    
    def extract_architecture_dependencies(self, prp_file: Path) -> Set[str]:
        """Extract which architecture files a PRP depends on"""
        if not prp_file.exists():
            return set()
            
        with open(prp_file, 'r') as f:
            content = f.read()
            
        dependencies = set()
        
        # Look for direct architecture file references
        arch_refs = re.findall(r'docs/architecture/(\w+\.md)', content)
        for ref in arch_refs:
            dependencies.add(f"docs/architecture/{ref}")
        
        # Look for architecture links
        link_pattern = r'\[.*?\]\((.*?architecture.*?\.md)\)'
        for match in re.finditer(link_pattern, content):
            path = match.group(1)
            # Normalize path
            if 'architecture' in path:
                if path.startswith('../'):
                    path = path.replace('../', '')
                elif path.startswith('../../'):
                    path = path.replace('../../', '')
                dependencies.add(path)
        
        # Extract component name and find in architecture
        component = self.extract_component_name(prp_file, content)
        if component:
            arch_files = self.find_component_in_architecture(component)
            dependencies.update(arch_files)
            
        return dependencies
    
    def extract_component_name(self, prp_file: Path, content: str = None) -> Optional[str]:
        """Extract component name from PRP"""
        # Try filename first
        filename = prp_file.stem
        if filename.endswith('-prp'):
            return filename[:-4]
        
        # Try content if provided
        if content:
            # Look for "# PRP: Component Name" pattern
            title_match = re.search(r'^#\s+PRP:\s+(.+?)$', content, re.MULTILINE)
            if title_match:
                component = title_match.group(1).strip()
                # Clean up common suffixes
                for suffix in [' Component', ' Service', ' Module']:
                    if component.endswith(suffix):
                        component = component[:-len(suffix)]
                return component.lower().replace(' ', '-')
        
        return None
    
    def find_component_in_architecture(self, component: str) -> Set[str]:
        """Find which architecture files mention a component"""
        found_in = set()
        
        if not self.arch_dir.exists():
            return found_in
            
        # Normalize component name variations
        variations = [
            component,
            component.replace('-', '_'),
            component.replace('-', ' '),
            component.title().replace('-', ''),
            component.upper()
        ]
        
        # Search architecture files
        for arch_file in self.arch_dir.glob("*.md"):
            if arch_file.name == "CHANGELOG.md":
                continue
                
            try:
                content = arch_file.read_text()
                # Check if any variation appears in the file
                for variant in variations:
                    if variant in content:
                        rel_path = arch_file.relative_to(self.project_root)
                        found_in.add(str(rel_path))
                        break
            except:
                continue
                
        return found_in
    
    def analyze_architecture_change(self, arch_file: str, changes: Dict) -> List[Dict]:
        """Analyze how architecture changes affect PRPs"""
        affected_prps = []
        
        # Get PRPs that depend on this architecture file
        dependency_map = self.build_dependency_map()
        dependent_prps = dependency_map.get(arch_file, [])
        
        for prp_file in dependent_prps:
            impact = self.assess_impact(prp_file, changes)
            
            if impact['severity'] != 'none':
                affected_prps.append({
                    'prp_file': prp_file,
                    'impact': impact,
                    'regeneration_needed': impact['severity'] in ['high', 'critical']
                })
                
        return affected_prps
    
    def assess_impact(self, prp_file: str, changes: Dict) -> Dict:
        """Assess impact of architecture changes on a PRP"""
        impact = {
            'severity': 'none',
            'reasons': [],
            'changes_needed': [],
            'affected_sections': []
        }
        
        # Component changes have high impact
        if changes['components']['removed']:
            for comp in changes['components']['removed']:
                if self._prp_uses_component(prp_file, comp['name']):
                    impact['severity'] = 'critical'
                    impact['reasons'].append(f"Component {comp['name']} was removed")
                    impact['changes_needed'].append("Complete redesign needed")
                    
        if changes['components']['added']:
            # New components might need integration
            impact['severity'] = max(impact['severity'], 'medium')
            impact['reasons'].append("New components available for integration")
            impact['affected_sections'].append("Integration Points")
        
        # API changes affect implementation
        if changes['apis']['removed']:
            impact['severity'] = 'high'
            impact['reasons'].append("API endpoints removed")
            impact['changes_needed'].append("Update API integration")
            impact['affected_sections'].append("API Integration")
            
        if changes['apis']['added']:
            impact['severity'] = max(impact['severity'], 'low')
            impact['reasons'].append("New API endpoints available")
            impact['affected_sections'].append("API Reference")
        
        # Database changes might affect data layer
        if changes['database_tables']['added'] or changes['database_tables']['removed']:
            impact['severity'] = max(impact['severity'], 'medium')
            impact['reasons'].append("Database schema changed")
            impact['changes_needed'].append("Update data models")
            impact['affected_sections'].append("Data Layer")
        
        # Security changes are always important
        if changes['security_policies']['added'] or changes['security_policies']['removed']:
            impact['severity'] = 'high'
            impact['reasons'].append("Security policies updated")
            impact['changes_needed'].append("Review security implementation")
            impact['affected_sections'].append("Security Requirements")
        
        return impact
    
    def _prp_uses_component(self, prp_file: str, component_name: str) -> bool:
        """Check if a PRP uses a specific component"""
        try:
            with open(prp_file, 'r') as f:
                content = f.read()
                return component_name.lower() in content.lower()
        except:
            return False
    
    def get_prp_architecture_metadata(self, prp_file: str) -> Dict:
        """Extract architecture metadata from PRP"""
        metadata = {
            'last_sync': None,
            'architecture_version': None,
            'dependencies': []
        }
        
        try:
            with open(prp_file, 'r') as f:
                content = f.read()
                
            # Look for sync metadata
            sync_match = re.search(r'Architecture Updated:\s*(\d{4}-\d{2}-\d{2})', content)
            if sync_match:
                metadata['last_sync'] = sync_match.group(1)
                
            # Extract architecture dependencies
            metadata['dependencies'] = list(self.extract_architecture_dependencies(Path(prp_file)))
            
        except:
            pass
            
        return metadata
    
    def clear_cache(self):
        """Clear the dependency cache"""
        self._dependency_cache = None
