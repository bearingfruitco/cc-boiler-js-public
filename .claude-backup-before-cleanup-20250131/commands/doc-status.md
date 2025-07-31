---
name: doc-status
aliases: ["docs-status", "documentation-status", "doc-sync-status"]
description: Check documentation synchronization status
---

# Documentation Status

Check the synchronization status between code and documentation.

## Usage

```bash
/doc-status                    # Overall documentation status
/doc-status components         # Status of component docs
/doc-status api               # Status of API docs
/doc-status --outdated        # Show only outdated docs
/doc-status --missing         # Show missing documentation
```

## Options

- `--outdated`: Show only documentation that needs updating
- `--missing`: Show code files without documentation
- `--summary`: Show summary statistics only
- `--component="name"`: Check specific component
- `--recent`: Show recent documentation updates

## Status Indicators

- ✅ **Synced**: Documentation up to date with code
- ⚠️ **Outdated**: Code changed after last doc update
- ❌ **Missing**: No documentation exists
- 🔄 **Updating**: Documentation update in progress
- ❗ **Error**: Last update failed

## Examples

### Check overall status
```bash
/doc-status
```

### Find outdated documentation
```bash
/doc-status --outdated
```

### Check component documentation
```bash
/doc-status components
```

### Check specific component
```bash
/doc-status --component="Button"
```

### View recent updates
```bash
/doc-status --recent
```

## Output Example

```
📊 Documentation Status Report

Components:
✅ Button.tsx → docs/components/Button.md (synced)
⚠️ Card.tsx → docs/components/Card.md (outdated - 2 days)
❌ Modal.tsx → docs/components/Modal.md (missing)

API Routes:
✅ /api/users → docs/api/users.md (synced)
⚠️ /api/auth → docs/api/auth.md (outdated - 1 day)

Summary:
- Total: 15 files
- Synced: 10 (67%)
- Outdated: 3 (20%)
- Missing: 2 (13%)
- Success Rate: 95%

Recent Updates:
- Button.md - updated 1 hour ago
- users.md - updated 3 hours ago
```

## Related Commands

- `/update-docs` - Force documentation update
- `/doc-preview` - Preview documentation changes
- `/doc-validate` - Validate documentation quality
