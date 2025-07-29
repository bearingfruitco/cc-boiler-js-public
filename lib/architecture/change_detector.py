"""
Architecture Change Detector
Detects changes in architecture documents and analyzes their impact
"""

import difflib
import json
import re
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Set


class ArchitectureChangeDetector:
    """Detects and analyzes changes in architecture documents"""
    
    def __init__(self, base_path: str = "/Users/shawnsmith/dev/bfc/boilerplate"):
        self.base_path = Path(base_path)
        self.arch_dir = self.base_path / "docs" / "architecture"
        self.state_file = self.arch_dir / ".architecture_state.json"
        self.current_state = self.load_state()
        
    def load_state(self) -> Dict:
        """Load the previous state of architecture files"""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_state(self):
        """Save the current state of architecture files"""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(self.current_state, f, indent=2)
    
    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate hash of architecture file for change detection"""
        if not file_path.exists():
            return ""
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    
    def parse_architecture_file(self, file_path: Path) -> Dict:
        """Parse architecture file to extract components and relationships"""
        if not file_path.exists():
            return {}
            
        with open(file_path, 'r') as f:
            content = f.read()
            
        parsed = {
            "components": self.extract_components(content),
            "relationships": self.extract_relationships(content),
            "apis": self.extract_apis(content),
            "database_tables": self.extract_database_tables(content),
            "security_policies": self.extract_security_policies(content)
        }
        
        return parsed
    
    def extract_components(self, content: str) -> List[Dict]:
        """Extract component definitions from architecture document"""
        components = []
        
        # Look for component definitions in various formats
        # Format 1: ### Component: Name
        component_pattern = r'###\s+Component:\s+(.+?)(?:\n|$)'
        for match in re.finditer(component_pattern, content):
            components.append({
                "name": match.group(1).strip(),
                "type": "component",
                "line": content[:match.start()].count('\n') + 1
            })
        
        # Format 2: Mermaid diagram components
        if 'graph' in content or 'flowchart' in content:
            mermaid_pattern = r'(\w+)\[["\'](.*?)["\']\]'
            for match in re.finditer(mermaid_pattern, content):
                components.append({
                    "name": match.group(2),
                    "id": match.group(1),
                    "type": "mermaid_component",
                    "line": content[:match.start()].count('\n') + 1
                })
        
        return components
    
    def extract_relationships(self, content: str) -> List[Dict]:
        """Extract component relationships from architecture document"""
        relationships = []
        
        # Mermaid arrow relationships
        arrow_pattern = r'(\w+)\s*--[->]+\s*(\w+)'
        for match in re.finditer(arrow_pattern, content):
            relationships.append({
                "from": match.group(1),
                "to": match.group(2),
                "type": "dependency",
                "line": content[:match.start()].count('\n') + 1
            })
        
        return relationships
    
    def extract_apis(self, content: str) -> List[Dict]:
        """Extract API endpoint definitions"""
        apis = []
        
        # Look for API definitions
        api_patterns = [
            r'(GET|POST|PUT|DELETE|PATCH)\s+(/\S+)',
            r'endpoint:\s*`(.*?)`',
            r'route:\s*["\']?(.*?)["\']?\s*[,\n]'
        ]
        
        for pattern in api_patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                if len(match.groups()) == 2:
                    apis.append({
                        "method": match.group(1),
                        "path": match.group(2),
                        "line": content[:match.start()].count('\n') + 1
                    })
                else:
                    apis.append({
                        "path": match.group(1),
                        "line": content[:match.start()].count('\n') + 1
                    })
        
        return apis
    
    def extract_database_tables(self, content: str) -> List[Dict]:
        """Extract database table definitions"""
        tables = []
        
        # Look for table definitions
        table_patterns = [
            r'table\s+["`]?(\w+)["`]?',
            r'Table:\s*(\w+)',
            r'create\s+table\s+(\w+)',
        ]
        
        for pattern in table_patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                tables.append({
                    "name": match.group(1),
                    "line": content[:match.start()].count('\n') + 1
                })
        
        return tables
    
    def extract_security_policies(self, content: str) -> List[Dict]:
        """Extract security policy definitions"""
        policies = []
        
        # Look for security-related content
        security_patterns = [
            r'policy:\s*(.+?)(?:\n|$)',
            r'RLS:\s*(.+?)(?:\n|$)',
            r'Auth:\s*(.+?)(?:\n|$)',
        ]
        
        for pattern in security_patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                policies.append({
                    "policy": match.group(1).strip(),
                    "line": content[:match.start()].count('\n') + 1
                })
        
        return policies
    
    def detect_changes(self, file_path: Path) -> Optional[Dict]:
        """Detect what changed in an architecture file"""
        if not file_path.exists():
            return None
            
        file_key = str(file_path.relative_to(self.base_path))
        current_hash = self.calculate_file_hash(file_path)
        
        # Check if file has changed
        previous_hash = self.current_state.get(file_key, {}).get("hash", "")
        if current_hash == previous_hash:
            return None
        
        # Parse current and previous states
        current_parsed = self.parse_architecture_file(file_path)
        previous_parsed = self.current_state.get(file_key, {}).get("parsed", {})
        
        # Detect changes
        changes = {
            "file": file_key,
            "timestamp": datetime.now().isoformat(),
            "hash": {
                "previous": previous_hash,
                "current": current_hash
            },
            "components": self.diff_components(
                previous_parsed.get("components", []),
                current_parsed.get("components", [])
            ),
            "relationships": self.diff_relationships(
                previous_parsed.get("relationships", []),
                current_parsed.get("relationships", [])
            ),
            "apis": self.diff_apis(
                previous_parsed.get("apis", []),
                current_parsed.get("apis", [])
            ),
            "database_tables": self.diff_tables(
                previous_parsed.get("database_tables", []),
                current_parsed.get("database_tables", [])
            ),
            "security_policies": self.diff_policies(
                previous_parsed.get("security_policies", []),
                current_parsed.get("security_policies", [])
            )
        }
        
        # Update state
        self.current_state[file_key] = {
            "hash": current_hash,
            "parsed": current_parsed,
            "last_updated": datetime.now().isoformat()
        }
        
        return changes
    
    def diff_components(self, old: List[Dict], new: List[Dict]) -> Dict:
        """Compare component lists and identify changes"""
        old_names = {c["name"] for c in old}
        new_names = {c["name"] for c in new}
        
        return {
            "added": [c for c in new if c["name"] not in old_names],
            "removed": [c for c in old if c["name"] not in new_names],
            "modified": []  # Would need deeper comparison for modifications
        }
    
    def diff_relationships(self, old: List[Dict], new: List[Dict]) -> Dict:
        """Compare relationship lists and identify changes"""
        def rel_key(r):
            return f"{r.get('from', '')}->{r.get('to', '')}"
        
        old_keys = {rel_key(r) for r in old}
        new_keys = {rel_key(r) for r in new}
        
        return {
            "added": [r for r in new if rel_key(r) not in old_keys],
            "removed": [r for r in old if rel_key(r) not in new_keys]
        }
    
    def diff_apis(self, old: List[Dict], new: List[Dict]) -> Dict:
        """Compare API lists and identify changes"""
        def api_key(a):
            return f"{a.get('method', 'GET')} {a.get('path', '')}"
        
        old_keys = {api_key(a) for a in old}
        new_keys = {api_key(a) for a in new}
        
        return {
            "added": [a for a in new if api_key(a) not in old_keys],
            "removed": [a for a in old if api_key(a) not in new_keys]
        }
    
    def diff_tables(self, old: List[Dict], new: List[Dict]) -> Dict:
        """Compare database table lists and identify changes"""
        old_names = {t["name"] for t in old}
        new_names = {t["name"] for t in new}
        
        return {
            "added": [t for t in new if t["name"] not in old_names],
            "removed": [t for t in old if t["name"] not in new_names]
        }
    
    def diff_policies(self, old: List[Dict], new: List[Dict]) -> Dict:
        """Compare security policy lists and identify changes"""
        old_policies = {p["policy"] for p in old}
        new_policies = {p["policy"] for p in new}
        
        return {
            "added": [p for p in new if p["policy"] not in old_policies],
            "removed": [p for p in old if p["policy"] not in old_policies]
        }
    
    def get_recent_changes(self, since: Optional[datetime] = None) -> List[Dict]:
        """Get all changes since a given time"""
        changes = []
        
        # Check all architecture files
        for arch_file in self.arch_dir.glob("*.md"):
            if arch_file.name == "CHANGELOG.md":
                continue
                
            change = self.detect_changes(arch_file)
            if change:
                changes.append(change)
        
        # Save updated state
        self.save_state()
        
        return changes
    
    def determine_change_type(self, changes: Dict) -> str:
        """Determine the primary type of change"""
        if changes["components"]["added"]:
            return "component_added"
        elif changes["components"]["removed"]:
            return "component_removed"
        elif changes["apis"]["added"] or changes["apis"]["removed"]:
            return "api_modified"
        elif changes["database_tables"]["added"] or changes["database_tables"]["removed"]:
            return "schema_changed"
        elif changes["security_policies"]["added"] or changes["security_policies"]["removed"]:
            return "security_updated"
        elif changes["relationships"]["added"] or changes["relationships"]["removed"]:
            return "relationships_modified"
        else:
            return "content_updated"
    
    def analyze_impact(self, changes: Dict) -> Dict:
        """Analyze the impact of changes"""
        impact = {
            "severity": "low",
            "components_affected": [],
            "requires_code_changes": False,
            "requires_migration": False,
            "breaking_change": False
        }
        
        # Component changes have high impact
        if changes["components"]["removed"]:
            impact["severity"] = "high"
            impact["breaking_change"] = True
            impact["components_affected"].extend([c["name"] for c in changes["components"]["removed"]])
        
        # API changes can be breaking
        if changes["apis"]["removed"]:
            impact["severity"] = "high"
            impact["breaking_change"] = True
            impact["requires_code_changes"] = True
        
        # Database changes need migrations
        if changes["database_tables"]["added"] or changes["database_tables"]["removed"]:
            impact["severity"] = "medium"
            impact["requires_migration"] = True
        
        # New components need implementation
        if changes["components"]["added"]:
            impact["requires_code_changes"] = True
            impact["components_affected"].extend([c["name"] for c in changes["components"]["added"]])
        
        return impact
