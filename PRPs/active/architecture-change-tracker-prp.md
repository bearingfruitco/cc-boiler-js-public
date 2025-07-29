# PRP: Architecture Change Tracker

## Overview
Implement a comprehensive system to track and log all architecture changes, providing complete visibility into architectural evolution and decision history.

## Goals
1. **Track All Architecture Changes**: Automatically detect and log modifications to architecture documents
2. **Generate Architecture Decision Records**: Create ADRs from tracked changes
3. **Provide Change History**: Searchable, filterable history of all architecture evolution
4. **Enable Impact Analysis**: Understand how changes affect the system

## Background Context

### Current State
- Architecture documents exist in `docs/architecture/`
- Changes happen through `/edit` or manual updates
- No automatic tracking of what changed or why
- No centralized changelog for architecture decisions

### Desired State
- Every architecture change is automatically tracked
- Complete changelog with rationale and impact
- ADR generation from significant changes
- Integration with validation and PRP systems

## Technical Context

### Architecture Documents to Track
```
docs/architecture/
├── SYSTEM_DESIGN.md          # Core system architecture
├── API_DESIGN.md             # API endpoints and contracts
├── DATABASE_SCHEMA.md        # Database structure
├── TECHNICAL_ROADMAP.md      # Future architecture plans
├── SECURITY_ARCHITECTURE.md  # Security policies
└── CHANGELOG.md              # NEW: Architecture changelog
```

### Change Detection Strategy
- Git diff analysis for file changes
- Structured parsing of markdown documents
- Component extraction from architecture files
- Relationship mapping between components

## Implementation Blueprint

### Phase 1: Core Change Tracking (2 hours)

#### 1.1 Create Change Detector
```python
# lib/architecture/change_detector.py
import difflib
import json
from pathlib import Path
from datetime import datetime
import hashlib

class ArchitectureChangeDetector:
    def __init__(self, base_path="/Users/shawnsmith/dev/bfc/boilerplate"):
        self.base_path = Path(base_path)
        self.arch_dir = self.base_path / "docs" / "architecture"
        self.change_log_file = self.arch_dir / ".change_log.json"
        
    def calculate_file_hash(self, file_path):
        """Calculate hash of architecture file for change detection"""
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    
    def detect_changes(self, file_path):
        """Detect what changed in an architecture file"""
        # Load previous state
        previous_state = self.load_previous_state(file_path)
        current_state = self.parse_architecture_file(file_path)
        
        changes = {
            "components": self.diff_components(
                previous_state.get("components", []),
                current_state.get("components", [])
            ),
            "relationships": self.diff_relationships(
                previous_state.get("relationships", []),
                current_state.get("relationships", [])
            ),
            "apis": self.diff_apis(
                previous_state.get("apis", []),
                current_state.get("apis", [])
            )
        }
        
        return changes
```

#### 1.2 Create Change Logger
```python
# lib/architecture/change_logger.py
class ArchitectureChangeLogger:
    def __init__(self, log_file="docs/architecture/.change_log.json"):
        self.log_file = Path(log_file)
        self.changes = self.load_changes()
    
    def log_change(self, change_record):
        """Log an architecture change"""
        change_record["id"] = self.generate_change_id()
        change_record["timestamp"] = datetime.now().isoformat()
        
        self.changes.append(change_record)
        self.save_changes()
        
        # Also update markdown changelog
        self.update_changelog_md(change_record)
    
    def create_change_record(self, file_path, changes, metadata):
        """Create a structured change record"""
        return {
            "file": str(file_path),
            "type": self.determine_change_type(changes),
            "category": self.determine_category(file_path),
            "description": self.generate_description(changes),
            "changes": changes,
            "author": metadata.get("author", "system"),
            "rationale": metadata.get("rationale", ""),
            "impact": self.analyze_impact(changes),
            "related_prp": metadata.get("related_prp", ""),
            "related_issue": metadata.get("related_issue", "")
        }
```

### Phase 2: Changelog Generation (1 hour)

#### 2.1 Markdown Changelog Generator
```python
# lib/architecture/changelog_generator.py
class ArchitectureChangelogGenerator:
    def __init__(self, changelog_path="docs/architecture/CHANGELOG.md"):
        self.changelog_path = Path(changelog_path)
        
    def update_changelog(self, change_record):
        """Add new entry to markdown changelog"""
        entry = self.format_changelog_entry(change_record)
        
        # Read existing changelog
        existing = self.read_changelog()
        
        # Insert new entry at top (after header)
        updated = self.insert_entry(existing, entry)
        
        # Write back
        self.write_changelog(updated)
    
    def format_changelog_entry(self, record):
        """Format change record as markdown"""
        date = record["timestamp"][:10]
        
        entry = f"""
## [{date}] {record["description"]}

- **Type**: {record["type"]}
- **Category**: {record["category"]}
- **Author**: {record["author"]}
- **Impact**: {self.format_impact(record["impact"])}
{f'- **Related PRP**: [{record["related_prp"]}](../../PRPs/active/{record["related_prp"]}.md)' if record["related_prp"] else ''}
{f'- **Related Issue**: #{record["related_issue"]}' if record["related_issue"] else ''}

### Changes
{self.format_changes(record["changes"])}

### Rationale
{record["rationale"] or "No rationale provided"}

---
"""
        return entry
```

### Phase 3: ADR Generation (1.5 hours)

#### 3.1 ADR Generator
```python
# lib/architecture/adr_generator.py
class ADRGenerator:
    def __init__(self, adr_dir="docs/architecture/decisions"):
        self.adr_dir = Path(adr_dir)
        self.adr_dir.mkdir(exist_ok=True)
        
    def should_generate_adr(self, change_record):
        """Determine if change warrants an ADR"""
        # Major changes get ADRs
        major_indicators = [
            "component_added",
            "component_removed", 
            "technology_change",
            "security_policy_change",
            "breaking_change"
        ]
        
        return (
            change_record["type"] in major_indicators or
            change_record["impact"].get("severity") == "high" or
            "architectural_decision" in change_record.get("tags", [])
        )
    
    def generate_adr(self, change_record):
        """Generate Architecture Decision Record"""
        adr_number = self.get_next_adr_number()
        title = self.generate_adr_title(change_record)
        filename = f"{adr_number:04d}-{self.slugify(title)}.md"
        
        content = f"""# {adr_number}. {title}

Date: {change_record["timestamp"][:10]}

## Status

Accepted

## Context

{self.expand_context(change_record)}

## Decision

{self.expand_decision(change_record)}

## Consequences

### Positive
{self.list_positive_consequences(change_record)}

### Negative
{self.list_negative_consequences(change_record)}

### Neutral
{self.list_neutral_consequences(change_record)}

## Related

- Change ID: {change_record["id"]}
- Original File: {change_record["file"]}
{f'- Related PRP: {change_record["related_prp"]}' if change_record["related_prp"] else ''}
{f'- Related Issue: #{change_record["related_issue"]}' if change_record["related_issue"] else ''}
"""
        
        self.write_adr(filename, content)
        return filename
```

### Phase 4: Hook Integration (1 hour)

#### 4.1 Post-Tool-Use Hook
```python
# .claude/hooks/post-tool-use/25-architecture-change-tracker.py
#!/usr/bin/env python3

import sys
import json
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.environ.get('CLAUDE_PROJECT_DIR', '/Users/shawnsmith/dev/bfc/boilerplate'))

from lib.architecture.change_detector import ArchitectureChangeDetector
from lib.architecture.change_logger import ArchitectureChangeLogger
from lib.architecture.adr_generator import ADRGenerator

def main():
    # Get hook input
    input_data = json.loads(sys.stdin.read())
    
    # Check if this is an architecture file edit
    tool_name = input_data.get('tool_name')
    if tool_name not in ['Edit', 'Write', 'MultiEdit']:
        return 0
        
    file_path = input_data.get('tool_input', {}).get('file_path', '')
    
    # Only track architecture files
    if not file_path.startswith('docs/architecture/'):
        return 0
    
    # Skip the changelog itself
    if file_path.endswith('CHANGELOG.md'):
        return 0
    
    try:
        # Detect changes
        detector = ArchitectureChangeDetector()
        changes = detector.detect_changes(file_path)
        
        if not changes:
            return 0
        
        # Create change record
        logger = ArchitectureChangeLogger()
        change_record = logger.create_change_record(
            file_path=file_path,
            changes=changes,
            metadata={
                "author": os.environ.get('USER', 'system'),
                "rationale": "Detected from file modification"
            }
        )
        
        # Log the change
        logger.log_change(change_record)
        
        # Generate ADR if needed
        adr_gen = ADRGenerator()
        if adr_gen.should_generate_adr(change_record):
            adr_file = adr_gen.generate_adr(change_record)
            print(f"Generated ADR: {adr_file}")
        
        # Suggest next