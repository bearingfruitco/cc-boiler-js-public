---
name: architecture-changes
aliases: ["arch-changes", "arch-log", "architecture-log"]
description: View and manage architecture change history
---

# Architecture Changes

View, search, and analyze architecture change history.

## Usage

```bash
/architecture-changes              # View recent changes
/architecture-changes --since="2024-01-01"  # Changes since date
/architecture-changes --impact="high"       # Filter by impact
/architecture-changes --breaking           # Show breaking changes only
/architecture-changes --summary            # Show summary statistics
```

## Options

- `--since="YYYY-MM-DD"`: Show changes since specified date
- `--until="YYYY-MM-DD"`: Show changes until specified date
- `--impact="level"`: Filter by impact level (low, medium, high, critical)
- `--breaking`: Show only breaking changes
- `--file="path"`: Show changes for specific architecture file
- `--type="type"`: Filter by change type
- `--summary`: Show summary statistics instead of details
- `--export`: Export changes to markdown report

## Change Types

- `component_added`: New component added to architecture
- `component_removed`: Component removed from architecture
- `api_modified`: API endpoints changed
- `schema_changed`: Database schema modifications
- `security_updated`: Security policy changes
- `relationships_modified`: Component relationships changed

## Impact Levels

- 🟢 **Low**: Minor updates, documentation changes
- 🟡 **Medium**: New features, non-breaking changes
- 🔴 **High**: Breaking changes, major refactoring
- 🚨 **Critical**: Security changes, data model changes

## Examples

### View recent changes
```bash
/architecture-changes
```

### View high-impact changes this month
```bash
/architecture-changes --since="2024-01-01" --impact="high"
```

### Check breaking changes
```bash
/architecture-changes --breaking
```

### Get summary statistics
```bash
/architecture-changes --summary
```

### Export change report
```bash
/architecture-changes --export > architecture-report.md
```

## Related Commands

- `/validate-architecture` - Validate and track changes
- `/architecture-viz` - Visualize architecture
- `/adr-generate` - Generate ADR from changes
- `/prp-sync` - Sync PRPs with changes
