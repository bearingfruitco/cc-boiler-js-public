# Issue #12: PRP Regeneration on Architecture Change

## Overview
Create a system that automatically detects architecture changes and regenerates affected PRPs to maintain synchronization between architecture and implementation plans.

## Problem Statement
When architecture evolves, existing PRPs can become outdated. We need:
- Automatic detection of architecture changes that affect PRPs
- Smart regeneration of only affected PRPs
- Preservation of implementation progress
- Clear communication about what changed

## Requirements

### Functional Requirements
1. **Change Detection**
   - Monitor architecture document changes
   - Identify which components are affected
   - Determine which PRPs need updates
   - Detect new components requiring PRPs

2. **Smart Regeneration**
   - Only regenerate affected PRPs
   - Preserve custom additions to PRPs
   - Merge architecture changes intelligently
   - Mark sections that changed

3. **Progress Preservation**
   - Keep completion checkboxes
   - Maintain implementation notes
   - Preserve validation results
   - Track what's already built

### Technical Requirements
1. **Diff Analysis**
   - Compare architecture versions
   - Identify structural changes
   - Map changes to components
   - Calculate impact radius

2. **PRP Update Strategy**
   - Sectional updates vs full regeneration
   - Version control for PRPs
   - Rollback capabilities
   - Conflict resolution

## Implementation Details

### Architecture Change Detection
```python
class ArchitectureChangeDetector:
    def detect_changes(self, old_arch, new_arch):
        """Detect what changed between architecture versions"""
        changes = {
            "components": {
                "added": [],
                "modified": [],
                "removed": []
            },
            "relationships": {
                "added": [],
                "modified": []
            },
            "schemas": {
                "tables_added": [],
                "columns_modified": []
            }
        }
        return changes
    
    def map_to_prps(self, changes):
        """Map architecture changes to affected PRPs"""
        affected_prps = []
        for component in changes["components"]["modified"]:
            prp_file = f"{component}-prp.md"
            if prp_exists(prp_file):
                affected_prps.append({
                    "file": prp_file,
                    "component": component,
                    "change_type": "update_required"
                })
        return affected_prps
```

### PRP Update Process
```python
class PRPRegenerator:
    def regenerate_prp(self, prp_file, arch_changes, preserve_sections):
        """Regenerate PRP while preserving progress"""
        existing_prp = self.parse_prp(prp_file)
        
        # Preserve these sections
        preserved = {
            "completion_status": existing_prp.get_checkboxes(),
            "implementation_notes": existing_prp.get_notes(),
            "custom_sections": existing_prp.get_custom()
        }
        
        # Generate new PRP with architecture updates
        new_prp = self.generate_from_architecture(
            component=existing_prp.component,
            architecture=self.load_current_architecture(),
            preserved=preserved
        )
        
        # Add change markers
        new_prp.mark_changes(arch_changes)
        
        return new_prp
```

### Change Notification
```markdown
# PRP: Authentication Service

> ⚠️ **Architecture Updated**: 2024-01-15
> - Added OAuth2 integration requirement
> - Modified session management approach
> - See [architecture changelog](../docs/architecture/CHANGELOG.md#2024-01-15)

## Overview
[Updated content with changes highlighted]

## Technical Context
### 🔄 Architecture Changes
- **NEW**: OAuth2 provider integration required
- **MODIFIED**: Session storage moved to Redis
- **DEPRECATED**: Local session management

[Rest of PRP content...]
```

### Workflow Integration
```bash
# After architecture update
/validate-architecture
Architecture validation passed with changes detected

# Suggested next command
/prp-sync                     # Sync PRPs with architecture
> Found 3 PRPs requiring updates:
> - authentication-service-prp.md
> - user-management-prp.md  
> - session-handler-prp.md
>
> Update PRPs? (y/n): y

# Or automatic in chain
/chain update-architecture && /validate-architecture && /prp-sync
```

## Success Criteria
- [ ] Architecture changes trigger PRP analysis
- [ ] Only affected PRPs are regenerated
- [ ] Progress and customizations are preserved
- [ ] Clear change notifications in PRPs
- [ ] Rollback capability if needed

## Edge Cases
1. **Major Architecture Overhaul**
   - Option for full PRP regeneration
   - Backup existing PRPs
   - Migration guide generation

2. **Completed PRPs**
   - Don't regenerate if implementation complete
   - Add notes about architecture drift
   - Suggest refactoring PRPs if needed

3. **Conflicting Changes**
   - Manual review required
   - Diff view for decision making
   - Preserve both versions

## Integration Points
- `/validate-architecture` - Detect changes
- `/generate-component-prps` - Reuse generation logic
- `/prp-status` - Show sync status
- Architecture change tracker (Issue #11)

## Priority: High
Critical for maintaining architecture-PRP alignment as projects evolve.
