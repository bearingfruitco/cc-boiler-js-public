---
name: prp-sync
aliases: ["sync-prps", "prp-regenerate", "prp-update"]
description: Synchronize PRPs with architecture changes
---

# PRP Synchronization

Analyze architecture changes and regenerate affected PRPs while preserving implementation progress.

## Usage

```bash
/prp-sync                    # Sync all affected PRPs
/prp-sync --preview         # Preview changes without regenerating
/prp-sync [prp-name]        # Sync specific PRP
/prp-sync --force           # Regenerate without preserving progress
```

## Process

1. **Detect Changes**: Find recent architecture modifications
2. **Map Impact**: Identify which PRPs are affected
3. **Preview Changes**: Show what will be updated
4. **Regenerate PRPs**: Update with progress preservation
5. **Report Results**: Show summary of updates

## Arguments

- `$ARGUMENTS`: Optional PRP name or flags
  - `--preview`: Show what would change without updating
  - `--force`: Regenerate from scratch (no progress preservation)
  - `[prp-name]`: Sync only the specified PRP

## Workflow

The command will:

1. Check for architecture changes since last sync
2. Build dependency map (architecture → PRPs)
3. Analyze impact on each PRP
4. For each affected PRP:
   - Save current progress (checkboxes, notes, custom sections)
   - Regenerate from updated architecture
   - Merge with preserved content
   - Add change markers
5. Generate summary report
6. Suggest next actions

## Progress Preservation

By default, the following are preserved:
- ✅ Completed task checkboxes
- 📝 Implementation notes
- 🎯 Custom sections
- 📚 Lessons learned
- ⚠️ Known issues/gotchas

## Impact Levels

- 🚨 **Critical**: Component removed, breaking changes
- 🔴 **High**: API changes, security updates
- 🟡 **Medium**: New components, schema changes
- 🟢 **Low**: Minor updates, new options

## Examples

### Preview changes
```bash
/prp-sync --preview
```

### Sync all affected PRPs
```bash
/prp-sync
```

### Force regeneration (start fresh)
```bash
/prp-sync --force
```

### Sync specific PRP
```bash
/prp-sync authentication-service
```

## Related Commands

- `/validate-architecture` - Triggers sync detection
- `/prp-status` - Check PRP sync status
- `/architecture-changes` - View recent changes
- `/prp-validate` - Validate PRP content
