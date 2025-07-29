# PRP: PRP Regeneration on Architecture Change

## Overview
Build an intelligent system that detects architecture changes and automatically regenerates affected PRPs while preserving implementation progress and custom content.

## Goals
1. **Automatic Change Detection**: Identify when architecture changes affect PRPs
2. **Smart Regeneration**: Update only what's needed, preserve what's done
3. **Progress Preservation**: Keep completion status and implementation notes
4. **Clear Communication**: Show what changed and why in updated PRPs

## Background Context

### Current State
- PRPs are generated from architecture documents
- Architecture evolves during development
- PRPs can become outdated and misaligned
- Manual checking required to maintain sync

### Desired State
- Architecture changes trigger automatic PRP analysis
- Affected PRPs regenerate with changes highlighted
- Implementation progress is never lost
- Clear tracking of what updated and why

## Technical Context

### PRP Structure to Preserve
```markdown
# PRP: Component Name

## Overview
[REGENERATE: May need updates based on architecture]

## Implementation Blueprint
### Phase 1
- [x] Task 1 (completed) [PRESERVE: Completion status]
- [ ] Task 2 (in progress) [PRESERVE: Progress]
- [ ] Task 3 (new from architecture) [REGENERATE: New tasks]

### Implementation Notes
[PRESERVE: All manual notes and learnings]

### Custom Sections
[PRESERVE: Any sections added by developers]
```

### Architecture → PRP Mapping
```
docs/architecture/SYSTEM_DESIGN.md
  → authentication-service-prp.md
  → user-management-prp.md
  → session-handler-prp.md

docs/architecture/API_DESIGN.md
  → api-gateway-prp.md
  → rest-endpoints-prp.md
```

## Implementation Blueprint

### Phase 1: Change Detection System (2 hours)

#### 1.1 Architecture-PRP Mapper
```python
# lib/prp/architecture_mapper.py
import re
from pathlib import Path
from typing import Dict, List, Set

class ArchitecturePRPMapper:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.prp_dir = self.project_root / "PRPs" / "active"
        self.arch_dir = self.project_root / "docs" / "architecture"
        
    def build_dependency_map(self) -> Dict[str, List[str]]:
        """Build map of architecture files to dependent PRPs"""
        dependency_map = {}
        
        # Scan all PRPs for architecture references
        for prp_file in self.prp_dir.glob("*.md"):
            arch_deps = self.extract_architecture_dependencies(prp_file)
            
            for arch_file in arch_deps:
                if arch_file not in dependency_map:
                    dependency_map[arch_file] = []
                dependency_map[arch_file].append(str(prp_file))
                
        return dependency_map
    
    def extract_architecture_dependencies(self, prp_file: Path) -> Set[str]:
        """Extract which architecture files a PRP depends on"""
        with open(prp_file, 'r') as f:
            content = f.read()
            
        dependencies = set()
        
        # Look for architecture file references
        arch_refs = re.findall(r'docs/architecture/\w+\.md', content)
        dependencies.update(arch_refs)
        
        # Parse component references
        if component := self.extract_component_name(content):
            # Map component to architecture sections
            arch_files = self.find_component_in_architecture(component)
            dependencies.update(arch_files)
            
        return dependencies
    
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
```

#### 1.2 PRP Progress Tracker
```python
# lib/prp/progress_tracker.py
import json
from datetime import datetime
from pathlib import Path

class PRPProgressTracker:
    def __init__(self, tracking_file=".claude/prp-progress.json"):
        self.tracking_file = Path(tracking_file)
        self.progress_data = self.load_progress()
        
    def extract_progress(self, prp_file: Path) -> Dict:
        """Extract completion progress from PRP"""
        with open(prp_file, 'r') as f:
            content = f.read()
            
        progress = {
            'file': str(prp_file),
            'timestamp': datetime.now().isoformat(),
            'completion': {
                'total_tasks': 0,
                'completed_tasks': 0,
                'in_progress_tasks': 0
            },
            'checkboxes': [],
            'implementation_notes': [],
            'custom_sections': []
        }
        
        # Extract checkbox states
        checkbox_pattern = r'- \[([ x])\] (.+?)(?:\n|$)'
        for match in re.finditer(checkbox_pattern, content):
            state = match.group(1)
            task = match.group(2)
            
            progress['checkboxes'].append({
                'state': 'completed' if state == 'x' else 'pending',
                'task': task,
                'line': match.start()
            })
            
            progress['completion']['total_tasks'] += 1
            if state == 'x':
                progress['completion']['completed_tasks'] += 1
                
        # Extract implementation notes
        impl_sections = re.findall(
            r'### Implementation Notes(.*?)(?=###|\Z)',
            content,
            re.DOTALL
        )
        if impl_sections:
            progress['implementation_notes'] = impl_sections[0].strip()
            
        # Extract custom sections
        custom_markers = re.findall(
            r'<!-- CUSTOM:(.*?)-->(.*?)<!-- END CUSTOM -->',
            content,
            re.DOTALL
        )
        for marker, content in custom_markers:
            progress['custom_sections'].append({
                'name': marker.strip(),
                'content': content.strip()
            })
            
        return progress
    
    def save_progress(self, prp_file: Path):
        """Save current progress before regeneration"""
        progress = self.extract_progress(prp_file)
        
        # Store in tracking file
        self.progress_data[str(prp_file)] = progress
        
        with open(self.tracking_file, 'w') as f:
            json.dump(self.progress_data, f, indent=2)
            
        return progress
```

### Phase 2: Smart PRP Regeneration (2.5 hours)

#### 2.1 PRP Regenerator
```python
# lib/prp/prp_regenerator.py
from datetime import datetime

class PRPRegenerator:
    def __init__(self):
        self.prp_writer_agent = "prp-writer"
        self.progress_tracker = PRPProgressTracker()
        
    def regenerate_prp(self, prp_file: Path, arch_changes: Dict, 
                      preserve_progress: bool = True) -> Dict:
        """Regenerate PRP with architecture updates"""
        
        # Save current progress
        if preserve_progress:
            saved_progress = self.progress_tracker.save_progress(prp_file)
        else:
            saved_progress = None
            
        # Extract component info
        component_info = self.extract_component_info(prp_file)
        
        # Load updated architecture
        updated_architecture = self.load_architecture_for_component(
            component_info['component']
        )
        
        # Generate new PRP content
        new_prp_content = self.generate_prp_content(
            component=component_info,
            architecture=updated_architecture,
            changes=arch_changes,
            preserved_content=saved_progress
        )
        
        # Write updated PRP
        self.write_prp_with_markers(prp_file, new_prp_content, arch_changes)
        
        return {
            'success': True,
            'file': str(prp_file),
            'changes_applied': len(arch_changes),
            'progress_preserved': preserve_progress
        }
    
    def generate_prp_content(self, **kwargs) -> str:
        """Generate PRP content using prp-writer agent"""
        
        prompt = f"""
Regenerate the PRP for {kwargs['component']['name']} with these architecture updates:

Architecture Changes:
{json.dumps(kwargs['changes'], indent=2)}

Current Architecture:
{kwargs['architecture']}

IMPORTANT - Preserve these elements:
1. Completed tasks (marked with [x])
2. Implementation notes section
3. Custom sections marked with <!-- CUSTOM: -->
4. Task completion order and grouping

Previous Progress to Preserve:
{json.dumps(kwargs['preserved_content'], indent=2) if kwargs['preserved_content'] else 'None'}

Requirements:
1. Update technical specifications to match new architecture
2. Add any new required tasks
3. Mark deprecated tasks clearly
4. Add change notification at top
5. Preserve all completion checkboxes
6. Keep implementation notes intact
7. Update integration points

Return the complete regenerated PRP.
"""
        
        # Invoke prp-writer agent
        result = self.invoke_prp_writer(prompt)
        return result
    
    def write_prp_with_markers(self, prp_file: Path, content: str, 
                               changes: Dict):
        """Write PRP with change markers"""
        
        # Add change header
        change_header = f"""
> ⚠️ **Architecture Updated**: {datetime.now().strftime('%Y-%m-%d')}
> This PRP was regenerated due to architecture changes.
> 
> **Changes Applied**:
{self.format_change_summary(changes)}
>
> **Progress Preserved**: ✅ All completed tasks and notes retained

---

"""
        
        # Prepend header to content
        final_content = change_header + content
        
        # Write to file
        with open(prp_file, 'w') as f:
            f.write(final_content)
```

#### 2.2 Merge Strategy Handler
```python
# lib/prp/merge_strategy.py

class PRPMergeStrategy:
    def __init__(self):
        self.strategies = {
            'preserve_progress': self.merge_preserve_progress,
            'architecture_priority': self.merge_architecture_priority,
            'interactive': self.merge_interactive
        }
        
    def merge_preserve_progress(self, old_prp: str, new_prp: str, 
                                progress: Dict) -> str:
        """Merge strategy that preserves all progress"""
        merged = new_prp
        
        # Restore checkbox states
        for checkbox in progress['checkboxes']:
            if checkbox['state'] == 'completed':
                # Find the task in new PRP and mark as complete
                task_pattern = re.escape(checkbox['task'])
                merged = re.sub(
                    f'- \[ \] {task_pattern}',
                    f'- [x] {checkbox["task"]}',
                    merged
                )
        
        # Restore implementation notes
        if progress['implementation_notes']:
            impl_pattern = r'### Implementation Notes\n(.*?)(?=###|\Z)'
            merged = re.sub(
                impl_pattern,
                f"### Implementation Notes\n{progress['implementation_notes']}\n",
                merged,
                flags=re.DOTALL
            )
        
        # Restore custom sections
        for custom in progress['custom_sections']:
            marker = f"<!-- CUSTOM: {custom['name']} -->"
            end_marker = "<!-- END CUSTOM -->"
            
            # Add custom section if not in new PRP
            if marker not in merged:
                # Add at end of document
                merged += f"\n\n{marker}\n{custom['content']}\n{end_marker}\n"
                
        return merged
```

### Phase 3: Integration with Architecture Validation (1.5 hours)

#### 3.1 Architecture Validation Hook
```python
# .claude/hooks/post-tool-use/26-prp-regeneration.py
#!/usr/bin/env python3

import sys
import json
import os
from pathlib import Path

sys.path.insert(0, os.environ.get('CLAUDE_PROJECT_DIR'))

from lib.prp.architecture_mapper import ArchitecturePRPMapper
from lib.prp.prp_regenerator import PRPRegenerator
from lib.architecture.change_detector import ArchitectureChangeDetector

def main():
    # Get hook input
    input_data = json.loads(sys.stdin.read())
    
    # Check if this is architecture validation
    tool_name = input_data.get('tool_name')
    if tool_name != 'RunCommand':
        return 0
        
    command = input_data.get('tool_input', {}).get('command', '')
    
    # Trigger on architecture validation
    if '/validate-architecture' not in command:
        return 0
    
    try:
        # Detect architecture changes
        detector = ArchitectureChangeDetector()
        arch_changes = detector.get_recent_changes()
        
        if not arch_changes:
            return 0
        
        # Map changes to affected PRPs
        mapper = ArchitecturePRPMapper(os.environ['CLAUDE_PROJECT_DIR'])
        affected_prps = []
        
        for change in arch_changes:
            affected = mapper.analyze_architecture_change(
                change['file'],
                change['changes']
            )
            affected_prps.extend(affected)
        
        if not affected_prps:
            return 0
        
        # Determine regeneration strategy
        critical_prps = [p for p in affected_prps 
                        if p['impact']['severity'] == 'critical']
        
        if critical_prps:
            # Immediate regeneration needed
            output = handle_critical_regeneration(critical_prps)
        else:
            # Suggest regeneration
            output = suggest_regeneration(affected_prps)
        
        print(json.dumps(output))
        
    except Exception as e:
        print(f"PRP regeneration error: {e}", file=sys.stderr)
        return 1
    
    return 0

def handle_critical_regeneration(critical_prps: List[Dict]) -> Dict:
    """Handle critical PRPs that need immediate regeneration"""
    
    regenerator = PRPRegenerator()
    results = []
    
    for prp_info in critical_prps:
        result = regenerator.regenerate_prp(
            Path(prp_info['prp_file']),
            prp_info['impact']['changes'],
            preserve_progress=True
        )
        results.append(result)
    
    return {
        "continue": True,
        "feedback": format_regeneration_feedback(results),
        "nextSuggestions": [
            {
                "command": "/prp-status",
                "description": "Review regenerated PRPs"
            },
            {
                "command": "/fw continue",
                "description": "Continue implementation with updated PRPs"
            }
        ]
    }

def suggest_regeneration(affected_prps: List[Dict]) -> Dict:
    """Suggest PRP regeneration for non-critical changes"""
    
    prp_list = [p['prp_file'] for p in affected_prps]
    
    return {
        "continue": True,
        "feedback": f"""
🔄 Architecture changes detected affecting {len(prp_list)} PRPs:

{format_prp_list(affected_prps)}

These PRPs may need updates to stay synchronized with the architecture.
""",
        "nextSuggestions": [
            {
                "command": "/prp-sync",
                "description": f"Synchronize {len(prp_list)} affected PRPs"
            },
            {
                "command": "/prp-sync --preview",
                "description": "Preview changes before regenerating"
            }
        ]
    }

if __name__ == "__main__":
    sys.exit(main())
```

### Phase 4: Commands and UI (1 hour)

#### 4.1 PRP Sync Command
```python
# .claude/commands/prp-sync.md
---
name: prp-sync
aliases: ["sync-prps", "prp-regenerate"]
description: Synchronize PRPs with architecture changes
---

# PRP Synchronization

Analyze architecture changes and regenerate affected PRPs while preserving progress.

## Usage

```bash
/prp-sync                    # Sync all affected PRPs
/prp-sync --preview         # Preview changes without regenerating
/prp-sync [prp-name]        # Sync specific PRP
/prp-sync --force           # Regenerate without preserving progress
```

## Process

1. **Detect Changes**: Find architecture modifications
2. **Map Impact**: Identify affected PRPs
3. **Preview**: Show what will change
4. **Regenerate**: Update PRPs with progress preservation
5. **Report**: Show summary of updates

## Arguments

- `$ARGUMENTS`: Optional PRP name or flags

## Implementation

1. Check for recent architecture changes
2. Build dependency map of architecture → PRPs
3. For each affected PRP:
   - Save current progress
   - Regenerate from updated architecture
   - Merge with preserved content
   - Add change markers
4. Generate summary report
5. Suggest next actions
```

#### 4.2 Status Command Enhancement
```python
# Add to existing /prp-status command

def check_prp_sync_status(prp_file: Path) -> Dict:
    """Check if PRP is synchronized with architecture"""
    
    # Get last architecture update
    arch_last_modified = get_architecture_last_modified()
    
    # Get PRP metadata
    prp_metadata = extract_prp_metadata(prp_file)
    prp_last_synced = prp_metadata.get('last_architecture_sync')
    
    if not prp_last_synced:
        return {'status': 'unknown', 'message': 'No sync history'}
    
    if prp_last_synced < arch_last_modified:
        return {
            'status': 'outdated',
            'message': f'Architecture updated {format_time_ago(arch_last_modified)}',
            'action': 'Run /prp-sync to update'
        }
    
    return {'status': 'synced', 'message': 'Up to date with architecture'}
```

## Validation Loops

### 🔴 Level 1: Syntax & Structure (Every Regeneration)
```bash
# Automatic validation
- PRP format compliance
- Checkbox preservation
- Section structure
- Change marker format
```

### 🟡 Level 2: Content Validation (Post-Regeneration)  
```bash
# Run with /prp-validate
- Architecture alignment
- Task completeness
- Integration points
- Progress accuracy
```

### 🟢 Level 3: Integration Testing (Pre-Implementation)
```bash
# Run with /prp-test  
- Generated code compatibility
- API contract matching
- Database schema alignment
- Component integration
```

### 🔵 Level 4: Implementation Verification (Post-Implementation)
```bash
# Run with /verify --prp
- Implementation matches PRP
- All tasks completed
- Tests cover requirements
- Documentation updated
```

## Success Criteria

- [ ] Architecture changes detected within validation workflow
- [ ] Affected PRPs identified with 100% accuracy
- [ ] Progress preservation works for all content types
- [ ] Clear change notifications in regenerated PRPs
- [ ] Minimal disruption to active development
- [ ] Integration with existing PRP commands
- [ ] Rollback capability if regeneration fails
- [ ] Performance: <5 seconds for typical regeneration

## Common Pitfalls & Solutions

### Pitfall 1: Lost Work
**Problem**: Developer changes overwritten by regeneration
**Solution**: Always save progress first, provide rollback option

### Pitfall 2: Merge Conflicts
**Problem**: Manual edits conflict with regenerated content
**Solution**: Clear section markers, intelligent merge strategy

### Pitfall 3: Cascade Updates
**Problem**: One change triggers many PRP updates
**Solution**: Batch processing, impact analysis, selective updates

### Pitfall 4: Stale Detection
**Problem**: Not detecting all architecture dependencies
**Solution**: Deep parsing, explicit dependency declaration

## Testing Strategy

1. **Unit Tests**: Change detection, progress extraction, merge logic
2. **Integration Tests**: Full regeneration flow, agent communication
3. **Scenario Tests**: Various change types and impacts
4. **User Tests**: Developer workflow disruption assessment

## Rollout Plan

1. **Phase 1**: Manual sync command with preview
2. **Phase 2**: Automatic detection in validation workflow  
3. **Phase 3**: Smart regeneration with merge strategies
4. **Phase 4**: Full automation with rollback safety

This PRP ensures that implementation plans stay perfectly synchronized with evolving architecture while never losing developer progress or custom content.
