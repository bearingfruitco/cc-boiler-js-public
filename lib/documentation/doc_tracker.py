"""
Documentation Tracker
Tracks documentation updates and maintains update history
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class DocumentationTracker:
    """Tracks and logs documentation updates"""
    
    def __init__(self, tracking_file: str = ".claude/doc-updates.json",
                 project_root: str = "/Users/shawnsmith/dev/bfc/boilerplate"):
        self.project_root = Path(project_root)
        self.tracking_file = self.project_root / tracking_file
        self.updates = self.load_updates()
        
    def load_updates(self) -> Dict:
        """Load existing update history"""
        if self.tracking_file.exists():
            try:
                with open(self.tracking_file, 'r') as f:
                    return json.load(f)
            except:
                return {"updates": [], "statistics": {}}
        return {"updates": [], "statistics": {}}
    
    def save_updates(self):
        """Save update history"""
        self.tracking_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.tracking_file, 'w') as f:
            json.dump(self.updates, f, indent=2)
    
    def log_update(self, source_file: str, doc_file: str, result: Dict):
        """Log a documentation update"""
        update_record = {
            "id": self.generate_update_id(),
            "timestamp": datetime.now().isoformat(),
            "source_file": source_file,
            "doc_file": doc_file,
            "update_type": result.get('update_type', 'unknown'),
            "success": result.get('success', False),
            "sections_updated": result.get('sections_updated', []),
            "error": result.get('error')
        }
        
        self.updates["updates"].append(update_record)
        self.update_statistics(update_record)
        self.save_updates()
        
        return update_record
    
    def generate_update_id(self) -> str:
        """Generate unique update ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        count = len(self.updates["updates"])
        return f"doc-update-{timestamp}-{count:04d}"
    
    def update_statistics(self, update_record: Dict):
        """Update running statistics"""
        stats = self.updates.get("statistics", {})
        
        # Initialize stats if needed
        if not stats:
            stats = {
                "total_updates": 0,
                "successful_updates": 0,
                "failed_updates": 0,
                "by_type": {},
                "by_file": {},
                "last_update": None
            }
        
        # Update counts
        stats["total_updates"] += 1
        if update_record["success"]:
            stats["successful_updates"] += 1
        else:
            stats["failed_updates"] += 1
        
        # Update by type
        update_type = update_record["update_type"]
        stats["by_type"][update_type] = stats["by_type"].get(update_type, 0) + 1
        
        # Update by file
        doc_file = update_record["doc_file"]
        stats["by_file"][doc_file] = stats["by_file"].get(doc_file, 0) + 1
        
        # Update last update time
        stats["last_update"] = update_record["timestamp"]
        
        self.updates["statistics"] = stats
    
    def get_recent_updates(self, limit: int = 10) -> List[Dict]:
        """Get recent documentation updates"""
        updates = self.updates.get("updates", [])
        return updates[-limit:] if updates else []
    
    def get_updates_for_file(self, doc_file: str) -> List[Dict]:
        """Get all updates for a specific documentation file"""
        return [u for u in self.updates.get("updates", [])
                if u["doc_file"] == doc_file]
    
    def get_failed_updates(self) -> List[Dict]:
        """Get all failed documentation updates"""
        return [u for u in self.updates.get("updates", [])
                if not u["success"]]
    
    def get_update_summary(self) -> Dict:
        """Get summary of documentation updates"""
        stats = self.updates.get("statistics", {})
        recent = self.get_recent_updates(5)
        
        summary = {
            "total_updates": stats.get("total_updates", 0),
            "success_rate": self._calculate_success_rate(),
            "most_updated_files": self._get_most_updated_files(5),
            "recent_updates": [
                {
                    "file": u["doc_file"],
                    "type": u["update_type"],
                    "time": u["timestamp"]
                } for u in recent
            ],
            "update_types": stats.get("by_type", {})
        }
        
        return summary
    
    def _calculate_success_rate(self) -> float:
        """Calculate documentation update success rate"""
        stats = self.updates.get("statistics", {})
        total = stats.get("total_updates", 0)
        successful = stats.get("successful_updates", 0)
        
        if total == 0:
            return 0.0
            
        return round((successful / total) * 100, 1)
    
    def _get_most_updated_files(self, limit: int) -> List[Dict]:
        """Get most frequently updated documentation files"""
        stats = self.updates.get("statistics", {})
        by_file = stats.get("by_file", {})
        
        # Sort by update count
        sorted_files = sorted(
            by_file.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]
        
        return [
            {"file": file, "count": count}
            for file, count in sorted_files
        ]
    
    def should_update_doc(self, doc_file: str, 
                         source_modified_time: datetime) -> bool:
        """Check if documentation should be updated based on history"""
        # Get last update for this doc
        updates = self.get_updates_for_file(doc_file)
        
        if not updates:
            # Never updated, should update
            return True
        
        # Get most recent successful update
        successful_updates = [u for u in updates if u["success"]]
        if not successful_updates:
            # No successful updates, should try again
            return True
        
        last_update = successful_updates[-1]
        last_update_time = datetime.fromisoformat(last_update["timestamp"])
        
        # Update if source was modified after last doc update
        return source_modified_time > last_update_time
