"""
Architecture Changelog Generator
Generates and updates markdown changelog for architecture changes
"""

import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class ArchitectureChangelogGenerator:
    """Generates markdown changelog from architecture changes"""
    
    def __init__(self, base_path: str = "/Users/shawnsmith/dev/bfc/boilerplate"):
        self.base_path = Path(base_path)
        self.changelog_path = self.base_path / "docs" / "architecture" / "CHANGELOG.md"
        
    def initialize_changelog(self):
        """Create initial changelog file if it doesn't exist"""
        if not self.changelog_path.exists():
            initial_content = """# Architecture Changelog

All notable changes to the system architecture are documented in this file.

The format is based on architectural decision records and tracks:
- Component additions/removals
- API changes
- Database schema modifications
- Security policy updates
- System design changes

## Change Categories

- **🏗️ System**: Core architecture and design changes
- **🔌 API**: API endpoint modifications
- **💾 Database**: Schema and data model changes
- **🔒 Security**: Security policies and authentication changes
- **📋 Planning**: Roadmap and future architecture updates

---

"""
            self.changelog_path.parent.mkdir(parents=True, exist_ok=True)
            self.changelog_path.write_text(initial_content)
    
    def update_changelog(self, change_record: Dict):
        """Add new entry to markdown changelog"""
        self.initialize_changelog()
        
        # Format the new entry
        entry = self.format_changelog_entry(change_record)
        
        # Read existing changelog
        existing = self.read_changelog()
        
        # Insert new entry after the header (before first entry)
        updated = self.insert_entry(existing, entry)
        
        # Write back
        self.write_changelog(updated)
    
    def read_changelog(self) -> str:
        """Read the current changelog content"""
        if self.changelog_path.exists():
            return self.changelog_path.read_text()
        return ""
    
    def write_changelog(self, content: str):
        """Write updated changelog content"""
        self.changelog_path.write_text(content)
    
    def insert_entry(self, existing: str, new_entry: str) -> str:
        """Insert new entry at the appropriate position"""
        # Find the position after the separator line
        separator_pattern = r'^---\s*$'
        lines = existing.split('\n')
        
        insert_position = None
        for i, line in enumerate(lines):
            if re.match(separator_pattern, line):
                insert_position = i + 1
                break
        
        if insert_position is None:
            # No separator found, append at end
            return existing + '\n' + new_entry
        
        # Insert the new entry
        lines.insert(insert_position, new_entry)
        return '\n'.join(lines)
    
    def format_changelog_entry(self, record: Dict) -> str:
        """Format change record as markdown entry"""
        # Extract date and format
        timestamp = datetime.fromisoformat(record["timestamp"])
        date_str = timestamp.strftime("%Y-%m-%d")
        
        # Determine emoji based on category
        category_emojis = {
            "system": "🏗️",
            "api": "🔌",
            "database": "💾",
            "security": "🔒",
            "planning": "📋",
            "general": "📝"
        }
        emoji = category_emojis.get(record["category"], "📝")
        
        # Build the entry
        entry_parts = [
            f"\n## [{date_str}] {emoji} {record['description']}\n",
            f"- **Type**: {self.format_change_type(record['type'])}",
            f"- **Category**: {record['category'].title()}",
            f"- **Impact**: {self.format_impact(record['impact'])}",
        ]
        
        # Add optional fields
        if record.get("author") and record["author"] != "system":
            entry_parts.append(f"- **Author**: {record['author']}")
            
        if record.get("related_prp"):
            prp_link = f"[{record['related_prp']}](../../PRPs/active/{record['related_prp']}.md)"
            entry_parts.append(f"- **Related PRP**: {prp_link}")
            
        if record.get("related_issue"):
            entry_parts.append(f"- **Related Issue**: #{record['related_issue']}")
            
        if record.get("commit"):
            entry_parts.append(f"- **Commit**: {record['commit'][:8]}")
        
        # Add changes section
        entry_parts.append("\n### Changes")
        entry_parts.extend(self.format_changes(record["changes"]))
        
        # Add rationale if provided
        if record.get("rationale"):
            entry_parts.append("\n### Rationale")
            entry_parts.append(record["rationale"])
        
        # Add impact details
        if record["impact"].get("components_affected"):
            entry_parts.append("\n### Components Affected")
            for component in record["impact"]["components_affected"]:
                entry_parts.append(f"- {component}")
        
        # Add migration notes if needed
        if record["impact"].get("requires_migration"):
            entry_parts.append("\n### ⚠️ Migration Required")
            entry_parts.append("This change requires database migrations.")
        
        # Add breaking change warning
        if record["impact"].get("breaking_change"):
            entry_parts.append("\n### 🚨 Breaking Change")
            entry_parts.append("This is a breaking change that may require code updates.")
        
        entry_parts.append("\n---")
        
        return "\n".join(entry_parts)
    
    def format_change_type(self, change_type: str) -> str:
        """Format change type for display"""
        type_mappings = {
            "component_added": "Component Addition",
            "component_removed": "Component Removal",
            "api_modified": "API Modification",
            "schema_changed": "Schema Change",
            "security_updated": "Security Update",
            "relationships_modified": "Relationship Change",
            "content_updated": "Content Update"
        }
        return type_mappings.get(change_type, change_type.replace("_", " ").title())
    
    def format_impact(self, impact: Dict) -> str:
        """Format impact information"""
        severity = impact.get("severity", "low")
        
        # Add emoji for severity
        severity_emojis = {
            "low": "🟢",
            "medium": "🟡",
            "high": "🔴",
            "critical": "🚨"
        }
        emoji = severity_emojis.get(severity, "")
        
        parts = [f"{emoji} {severity.title()}"]
        
        # Add impact flags
        flags = []
        if impact.get("breaking_change"):
            flags.append("Breaking")
        if impact.get("requires_code_changes"):
            flags.append("Code Changes")
        if impact.get("requires_migration"):
            flags.append("Migration")
            
        if flags:
            parts.append(f"({', '.join(flags)})")
        
        return " ".join(parts)
    
    def format_changes(self, changes: Dict) -> List[str]:
        """Format detailed changes section"""
        formatted = []
        
        # Components
        if changes["components"]["added"]:
            formatted.append("\n#### Components Added")
            for comp in changes["components"]["added"]:
                formatted.append(f"- `{comp['name']}` ({comp.get('type', 'component')})")
                
        if changes["components"]["removed"]:
            formatted.append("\n#### Components Removed")
            for comp in changes["components"]["removed"]:
                formatted.append(f"- ~~`{comp['name']}`~~ ({comp.get('type', 'component')})")
        
        # APIs
        if changes["apis"]["added"]:
            formatted.append("\n#### APIs Added")
            for api in changes["apis"]["added"]:
                method = api.get('method', 'GET')
                path = api.get('path', 'unknown')
                formatted.append(f"- `{method} {path}`")
                
        if changes["apis"]["removed"]:
            formatted.append("\n#### APIs Removed")
            for api in changes["apis"]["removed"]:
                method = api.get('method', 'GET')
                path = api.get('path', 'unknown')
                formatted.append(f"- ~~`{method} {path}`~~")
        
        # Database tables
        if changes["database_tables"]["added"]:
            formatted.append("\n#### Database Tables Added")
            for table in changes["database_tables"]["added"]:
                formatted.append(f"- `{table['name']}`")
                
        if changes["database_tables"]["removed"]:
            formatted.append("\n#### Database Tables Removed")
            for table in changes["database_tables"]["removed"]:
                formatted.append(f"- ~~`{table['name']}`~~")
        
        # Relationships
        if changes["relationships"]["added"]:
            formatted.append("\n#### Relationships Added")
            for rel in changes["relationships"]["added"]:
                formatted.append(f"- `{rel['from']}` → `{rel['to']}`")
                
        if changes["relationships"]["removed"]:
            formatted.append("\n#### Relationships Removed")
            for rel in changes["relationships"]["removed"]:
                formatted.append(f"- ~~`{rel['from']}` → `{rel['to']}`~~")
        
        # Security policies
        if changes["security_policies"]["added"]:
            formatted.append("\n#### Security Policies Added")
            for policy in changes["security_policies"]["added"]:
                formatted.append(f"- {policy['policy']}")
        
        return formatted
    
    def generate_summary_section(self, changes: List[Dict], 
                                period_days: int = 30) -> str:
        """Generate a summary section for recent changes"""
        summary = []
        summary.append(f"\n## Summary (Last {period_days} Days)\n")
        
        # Count changes by type
        by_type = {}
        by_category = {}
        breaking_count = 0
        
        for change in changes:
            # Type counts
            change_type = change["type"]
            by_type[change_type] = by_type.get(change_type, 0) + 1
            
            # Category counts
            category = change["category"]
            by_category[category] = by_category.get(category, 0) + 1
            
            # Breaking changes
            if change["impact"].get("breaking_change"):
                breaking_count += 1
        
        # Format summary
        summary.append(f"- **Total Changes**: {len(changes)}")
        summary.append(f"- **Breaking Changes**: {breaking_count}")
        
        if by_type:
            summary.append("\n### By Type")
            for change_type, count in sorted(by_type.items(), 
                                           key=lambda x: x[1], reverse=True):
                summary.append(f"- {self.format_change_type(change_type)}: {count}")
        
        if by_category:
            summary.append("\n### By Category")
            for category, count in sorted(by_category.items(), 
                                        key=lambda x: x[1], reverse=True):
                summary.append(f"- {category.title()}: {count}")
        
        summary.append("\n---\n")
        
        return "\n".join(summary)
