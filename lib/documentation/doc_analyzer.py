"""
Documentation Analyzer
Analyzes code changes to determine documentation updates needed
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Optional, Set


class DocumentationAnalyzer:
    """Analyzes code changes and determines documentation needs"""
    
    def __init__(self, project_root: str = "/Users/shawnsmith/dev/bfc/boilerplate"):
        self.project_root = Path(project_root)
        self.doc_mappings = self.load_doc_mappings()
        
    def load_doc_mappings(self) -> Dict[str, str]:
        """Load mappings between code files and documentation"""
        # Default mappings
        mappings = {
            # Component mappings
            "components/ui/": "docs/components/",
            "components/forms/": "docs/components/forms/",
            "components/layout/": "docs/components/layout/",
            
            # API mappings
            "app/api/": "docs/api/",
            
            # Library mappings
            "lib/": "docs/technical/",
            "lib/db/": "docs/architecture/DATABASE_SCHEMA.md",
            "lib/security/": "docs/security/",
            
            # Type mappings
            "types/": "docs/api/types.md"
        }
        
        # Check for custom mappings file
        mapping_file = self.project_root / ".claude" / "doc-mappings.json"
        if mapping_file.exists():
            import json
            with open(mapping_file, 'r') as f:
                custom_mappings = json.load(f)
                mappings.update(custom_mappings)
        
        return mappings
    
    def analyze_code_change(self, file_path: str, change_type: str) -> Dict:
        """Analyze what documentation needs updating based on code change"""
        analysis = {
            "file": file_path,
            "type": self.determine_file_type(file_path),
            "docs_to_update": [],
            "update_strategy": "incremental",
            "components_affected": []
        }
        
        # Find related documentation
        if self.is_component(file_path):
            analysis["docs_to_update"].extend(
                self.find_component_docs(file_path)
            )
            analysis["components_affected"].append(
                self.extract_component_name(file_path)
            )
        
        if self.is_api_route(file_path):
            analysis["docs_to_update"].extend(
                self.find_api_docs(file_path)
            )
            
        if self.is_type_definition(file_path):
            analysis["docs_to_update"].extend(
                self.find_type_docs(file_path)
            )
            
        if self.is_hook(file_path):
            analysis["docs_to_update"].extend(
                self.find_hook_docs(file_path)
            )
        
        # Determine update strategy
        if change_type == 'Write':
            analysis["update_strategy"] = "full"
        elif 'test' in file_path:
            analysis["update_strategy"] = "skip"
            
        return analysis
    
    def determine_file_type(self, file_path: str) -> str:
        """Determine the type of file"""
        path = Path(file_path)
        
        if path.suffix in ['.ts', '.tsx']:
            if '/components/' in str(path):
                return 'component'
            elif '/api/' in str(path):
                return 'api'
            elif '/hooks/' in str(path):
                return 'hook'
            elif '/types/' in str(path):
                return 'type'
            else:
                return 'typescript'
        elif path.suffix == '.py':
            return 'python'
        elif path.suffix == '.sql':
            return 'sql'
        else:
            return 'other'
    
    def is_component(self, file_path: str) -> bool:
        """Check if file is a React component"""
        return ('/components/' in file_path and 
                file_path.endswith(('.tsx', '.jsx')) and
                not file_path.endswith('.test.tsx'))
    
    def is_api_route(self, file_path: str) -> bool:
        """Check if file is an API route"""
        return ('/api/' in file_path and 
                'route.' in file_path)
    
    def is_type_definition(self, file_path: str) -> bool:
        """Check if file contains type definitions"""
        return ('/types/' in file_path or
                file_path.endswith('.d.ts') or
                'types.ts' in file_path)
    
    def is_hook(self, file_path: str) -> bool:
        """Check if file is a React hook"""
        return ('/hooks/' in file_path or
                ('use' in Path(file_path).stem and 
                 file_path.endswith(('.ts', '.tsx'))))
    
    def find_component_docs(self, file_path: str) -> List[str]:
        """Find documentation files for a component"""
        docs = []
        component_name = self.extract_component_name(file_path)
        
        if not component_name:
            return docs
        
        # Check for component-specific docs
        component_doc = self.project_root / "docs" / "components" / f"{component_name}.md"
        if component_doc.exists():
            docs.append(str(component_doc))
        else:
            # Create path for new doc
            docs.append(str(component_doc))
        
        # Check for README in component directory
        component_dir = Path(file_path).parent
        readme = component_dir / "README.md"
        if readme.exists():
            docs.append(str(readme))
        
        return docs
    
    def find_api_docs(self, file_path: str) -> List[str]:
        """Find documentation files for an API route"""
        docs = []
        
        # Extract API path
        api_path = self.extract_api_path(file_path)
        if api_path:
            api_doc = self.project_root / "docs" / "api" / f"{api_path}.md"
            docs.append(str(api_doc))
        
        # Check for general API docs
        if (self.project_root / "docs" / "api" / "README.md").exists():
            docs.append(str(self.project_root / "docs" / "api" / "README.md"))
        
        return docs
    
    def find_type_docs(self, file_path: str) -> List[str]:
        """Find documentation files for type definitions"""
        docs = []
        
        # Main types documentation
        types_doc = self.project_root / "docs" / "api" / "types.md"
        docs.append(str(types_doc))
        
        # Component-specific type docs
        if '/components/' in file_path:
            component_name = self.extract_component_name(file_path)
            if component_name:
                component_types = self.project_root / "docs" / "components" / f"{component_name}-types.md"
                docs.append(str(component_types))
        
        return docs
    
    def find_hook_docs(self, file_path: str) -> List[str]:
        """Find documentation files for hooks"""
        docs = []
        
        hook_name = Path(file_path).stem
        hook_doc = self.project_root / "docs" / "hooks" / f"{hook_name}.md"
        docs.append(str(hook_doc))
        
        # General hooks documentation
        hooks_readme = self.project_root / "docs" / "hooks" / "README.md"
        if hooks_readme.exists():
            docs.append(str(hooks_readme))
        
        return docs
    
    def extract_component_name(self, file_path: str) -> Optional[str]:
        """Extract component name from file path"""
        path = Path(file_path)
        
        # Remove file extension and common suffixes
        name = path.stem
        for suffix in ['.component', '.stories', '.test', '.spec']:
            if name.endswith(suffix):
                name = name[:-len(suffix)]
        
        return name if name else None
    
    def extract_api_path(self, file_path: str) -> Optional[str]:
        """Extract API path from file path"""
        # Convert file path to API route
        # e.g., app/api/users/[id]/route.ts -> users/[id]
        match = re.search(r'app/api/(.+?)/route\.(ts|js)', file_path)
        if match:
            return match.group(1)
        return None
    
    def extract_documentation_sections(self, doc_path: str) -> Dict:
        """Extract manual vs generated sections from documentation"""
        if not Path(doc_path).exists():
            return {
                "manual": [],
                "generated": [],
                "metadata": {},
                "exists": False
            }
            
        with open(doc_path, 'r') as f:
            content = f.read()
            
        sections = {
            "manual": [],
            "generated": [],
            "metadata": {},
            "exists": True,
            "full_content": content
        }
        
        # Parse sections
        lines = content.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            if line.startswith('<!-- GENERATED:'):
                # Save previous section
                if current_section and current_content:
                    sections[current_section].append({
                        'content': '\n'.join(current_content),
                        'name': current_section
                    })
                # Start new generated section
                current_section = 'generated'
                section_name = line[15:].replace('-->', '').strip()
                current_content = []
            elif line.startswith('<!-- MANUAL:'):
                # Save previous section
                if current_section and current_content:
                    sections[current_section].append({
                        'content': '\n'.join(current_content),
                        'name': current_section
                    })
                # Start new manual section
                current_section = 'manual'
                section_name = line[12:].replace('-->', '').strip()
                current_content = []
            elif line.startswith('<!-- END'):
                # End current section
                if current_section and current_content:
                    sections[current_section].append({
                        'content': '\n'.join(current_content),
                        'name': section_name if 'section_name' in locals() else current_section
                    })
                current_section = None
                current_content = []
            else:
                if current_section:
                    current_content.append(line)
        
        # Extract metadata
        metadata_match = re.search(r'<!-- GENERATED: metadata -->(.*?)<!-- END GENERATED -->', 
                                  content, re.DOTALL)
        if metadata_match:
            sections['metadata'] = self._parse_metadata(metadata_match.group(1))
        
        return sections
    
    def _parse_metadata(self, metadata_content: str) -> Dict:
        """Parse metadata from documentation"""
        metadata = {}
        
        # Look for common metadata patterns
        patterns = {
            'last_updated': r'Last updated:\s*(.+?)(?:\n|$)',
            'source_file': r'Source:\s*(.+?)(?:\n|$)',
            'auto_generated': r'Auto-generated from:\s*(.+?)(?:\n|$)'
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, metadata_content)
            if match:
                metadata[key] = match.group(1).strip()
        
        return metadata
    
    def analyze_code_for_documentation(self, file_path: str) -> Dict:
        """Analyze code file to extract documentation-relevant information"""
        file_type = self.determine_file_type(file_path)
        
        if file_type == 'component':
            return self._analyze_component(file_path)
        elif file_type == 'api':
            return self._analyze_api_route(file_path)
        elif file_type == 'hook':
            return self._analyze_hook(file_path)
        else:
            return {}
    
    def _analyze_component(self, file_path: str) -> Dict:
        """Analyze React component for documentation"""
        info = {
            'props': [],
            'methods': [],
            'hooks': [],
            'exports': [],
            'dependencies': []
        }
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Extract props interface
            props_match = re.search(r'interface\s+\w*Props\s*{([^}]+)}', content, re.DOTALL)
            if props_match:
                info['props'] = self._parse_typescript_interface(props_match.group(1))
            
            # Extract hooks used
            hooks_pattern = r'use[A-Z]\w+(?:\s*\(|\s*<)'
            info['hooks'] = list(set(re.findall(hooks_pattern, content)))
            
            # Extract exports
            export_pattern = r'export\s+(?:default\s+)?(?:function|const|class)\s+(\w+)'
            info['exports'] = re.findall(export_pattern, content)
            
        except Exception as e:
            print(f"Error analyzing component: {e}")
        
        return info
    
    def _analyze_api_route(self, file_path: str) -> Dict:
        """Analyze API route for documentation"""
        info = {
            'methods': [],
            'request_schema': {},
            'response_schema': {},
            'auth_required': False
        }
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Extract HTTP methods
            method_pattern = r'export\s+async\s+function\s+(GET|POST|PUT|DELETE|PATCH)'
            info['methods'] = re.findall(method_pattern, content)
            
            # Check for auth
            info['auth_required'] = 'getSession' in content or 'requireAuth' in content
            
        except Exception as e:
            print(f"Error analyzing API route: {e}")
        
        return info
    
    def _analyze_hook(self, file_path: str) -> Dict:
        """Analyze React hook for documentation"""
        info = {
            'parameters': [],
            'return_type': None,
            'dependencies': []
        }
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Extract hook signature
            hook_name = Path(file_path).stem
            sig_pattern = rf'export\s+(?:default\s+)?function\s+{hook_name}\s*\(([^)]*)\)'
            sig_match = re.search(sig_pattern, content)
            
            if sig_match:
                params = sig_match.group(1)
                if params:
                    info['parameters'] = [p.strip() for p in params.split(',')]
            
        except Exception as e:
            print(f"Error analyzing hook: {e}")
        
        return info
    
    def _parse_typescript_interface(self, interface_body: str) -> List[Dict]:
        """Parse TypeScript interface body to extract props"""
        props = []
        
        # Simple parsing - could be enhanced with proper AST
        lines = interface_body.strip().split('\n')
        for line in lines:
            line = line.strip()
            if ':' in line and not line.startswith('//'):
                # Extract prop name and type
                match = re.match(r'(\w+)(\?)?:\s*(.+?)(?:;|$)', line)
                if match:
                    props.append({
                        'name': match.group(1),
                        'required': match.group(2) != '?',
                        'type': match.group(3).strip()
                    })
        
        return props
