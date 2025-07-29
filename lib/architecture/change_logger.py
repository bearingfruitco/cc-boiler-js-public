"""
Architecture Change Logger
Logs architecture changes and maintains change history
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import uuid


class ArchitectureChangeLogger:
    """Logs and tracks architecture changes over time"""
    
    def __init__(self, log_file: str = "docs/architecture/.change_log.json",
                 base_path: str = "/Users/shawnsmith/dev/bfc/boilerplate"):
        self.base_path = Path(base_path)
        self.log_file = self.base_path / log_file
        self.changes = self.load_changes()
        
    def load_changes(self) -> List[Dict]:
        """Load existing change log"""
        if self.log_file.exists():
            with open(self.log_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_changes(self):
        """Save changes to log file"""
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.log_file, 'w') as f:
            json.dump(self.changes, f, indent=2)
    
    def generate_change_id(self) -> str:
        """Generate unique change ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"arch-change-{timestamp}-{str(uuid.uuid4())[:8]}"
    
    def log_change(self, change_record: Dict):
        """Log an architecture change"""
        # Add metadata
        change_record["id"] = self.generate_change_id()
        change_record["timestamp"] = datetime.now().isoformat()
        
        # Add to log
        self.changes.append(change_record)
        self.save_changes()
        
        # Also update markdown changelog
        from .changelog_generator import ArchitectureChangelogGenerator
        changelog_gen = ArchitectureChangelogGenerator(self.base_path)
        changelog_gen.update_changelog(change_record)
        
        return change_record
    
    def create_change_record(self, file_path: str, changes: Dict, 
                           metadata: Optional[Dict] = None) -> Dict:
        """Create a structured change record"""
        if metadata is None:
            metadata = {}
            
        # Determine change type and description
        from .change_detector import ArchitectureChangeDetector
        detector = ArchitectureChangeDetector(str(self.base_path))
        change_type = detector.determine_change_type(changes)
        
        description = self.generate_description(changes, change_type)
        impact = detector.analyze_impact(changes)
        
        return {
            "file": file_path,
            "type": change_type,
            "category": self.determine_category(file_path),
            "description": description,
            "changes": changes,
            "author": metadata.get("author", "system"),
            "rationale": metadata.get("rationale", ""),
            "impact": impact,
            "related_prp": metadata.get("related_prp", ""),
            "related_issue": metadata.get("related_issue", ""),
            "commit": metadata.get("commit", ""),
            "tags": metadata.get("tags", [])
        }
    
    def determine_category(self, file_path: str) -> str:
        """Determine the category of architecture change"""
        file_name = Path(file_path).name.lower()
        
        if "system" in file_name or "design" in file_name:
            return "system"
        elif "api" in file_name:
            return "api"
        elif "database" in file_name or "schema" in file_name:
            return "database"
        elif "security" in file_name:
            return "security"
        elif "roadmap" in file_name:
            return "planning"
        else:
            return "general"
    
    def generate_description(self, changes: Dict, change_type: str) -> str:
        """Generate human-readable description of changes"""
        descriptions = []
        
        # Component changes
        if changes["components"]["added"]:
            names = [c["name"] for c in changes["components"]["added"]]
            descriptions.append(f"Added components: {', '.join(names)}")
            
        if changes["components"]["removed"]:
            names = [c["name"] for c in changes["components"]["removed"]]
            descriptions.append(f"Removed components: {', '.join(names)}")
        
        # API changes
        if changes["apis"]["added"]:
            endpoints = [f"{a.get('method', 'GET')} {a.get('path', '')}" 
                        for a in changes["apis"]["added"]]
            descriptions.append(f"Added APIs: {', '.join(endpoints)}")
            
        if changes["apis"]["removed"]:
            endpoints = [f"{a.get('method', 'GET')} {a.get('path', '')}" 
                        for a in changes["apis"]["removed"]]
            descriptions.append(f"Removed APIs: {', '.join(endpoints)}")
        
        # Database changes
        if changes["database_tables"]["added"]:
            tables = [t["name"] for t in changes["database_tables"]["added"]]
            descriptions.append(f"Added tables: {', '.join(tables)}")
            
        if changes["database_tables"]["removed"]:
            tables = [t["name"] for t in changes["database_tables"]["removed"]]
            descriptions.append(f"Removed tables: {', '.join(tables)}")
        
        # Security changes
        if changes["security_policies"]["added"]:
            descriptions.append(f"Added {len(changes['security_policies']['added'])} security policies")
        
        # Relationship changes
        if changes["relationships"]["added"]:
            descriptions.append(f"Added {len(changes['relationships']['added'])} component relationships")
            
        if changes["relationships"]["removed"]:
            descriptions.append(f"Removed {len(changes['relationships']['removed'])} component relationships")
        
        # Default description
        if not descriptions:
            descriptions.append(f"Updated architecture documentation")
        
        return "; ".join(descriptions)
    
    def get_changes_by_file(self, file_path: str) -> List[Dict]:
        """Get all changes for a specific file"""
        return [c for c in self.changes if c["file"] == file_path]
    
    def get_changes_by_date(self, start_date: datetime, 
                           end_date: Optional[datetime] = None) -> List[Dict]:
        """Get changes within a date range"""
        changes = []
        for change in self.changes:
            change_date = datetime.fromisoformat(change["timestamp"])
            if change_date >= start_date:
                if end_date is None or change_date <= end_date:
                    changes.append(change)
        return changes
    
    def get_changes_by_type(self, change_type: str) -> List[Dict]:
        """Get all changes of a specific type"""
        return [c for c in self.changes if c["type"] == change_type]
    
    def get_changes_by_impact(self, min_severity: str = "medium") -> List[Dict]:
        """Get changes with impact above a severity threshold"""
        severity_levels = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        min_level = severity_levels.get(min_severity, 2)
        
        return [c for c in self.changes 
                if severity_levels.get(c["impact"]["severity"], 1) >= min_level]
    
    def get_breaking_changes(self) -> List[Dict]:
        """Get all breaking changes"""
        return [c for c in self.changes if c["impact"].get("breaking_change", False)]
    
    def search_changes(self, query: str) -> List[Dict]:
        """Search changes by description or content"""
        query_lower = query.lower()
        results = []
        
        for change in self.changes:
            if (query_lower in change["description"].lower() or
                query_lower in change.get("rationale", "").lower() or
                query_lower in str(change["changes"]).lower()):
                results.append(change)
                
        return results
    
    def generate_summary(self, days: int = 30) -> Dict:
        """Generate summary statistics for recent changes"""
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_changes = self.get_changes_by_date(cutoff_date)
        
        summary = {
            "period_days": days,
            "total_changes": len(recent_changes),
            "by_type": {},
            "by_category": {},
            "by_severity": {},
            "breaking_changes": 0,
            "components_added": 0,
            "components_removed": 0,
            "most_changed_files": {}
        }
        
        for change in recent_changes:
            # Count by type
            change_type = change["type"]
            summary["by_type"][change_type] = summary["by_type"].get(change_type, 0) + 1
            
            # Count by category
            category = change["category"]
            summary["by_category"][category] = summary["by_category"].get(category, 0) + 1
            
            # Count by severity
            severity = change["impact"]["severity"]
            summary["by_severity"][severity] = summary["by_severity"].get(severity, 0) + 1
            
            # Count breaking changes
            if change["impact"].get("breaking_change", False):
                summary["breaking_changes"] += 1
            
            # Count component changes
            summary["components_added"] += len(change["changes"]["components"]["added"])
            summary["components_removed"] += len(change["changes"]["components"]["removed"])
            
            # Track most changed files
            file_path = change["file"]
            summary["most_changed_files"][file_path] = \
                summary["most_changed_files"].get(file_path, 0) + 1
        
        # Sort most changed files
        summary["most_changed_files"] = dict(
            sorted(summary["most_changed_files"].items(), 
                  key=lambda x: x[1], reverse=True)[:5]
        )
        
        return summary
