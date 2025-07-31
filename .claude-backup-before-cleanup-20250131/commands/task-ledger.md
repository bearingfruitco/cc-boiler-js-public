# Task Ledger - Persistent Task Tracking

View and manage the centralized task ledger that tracks all features and tasks across your project.

## Usage
```bash
/task-ledger              # View current ledger
/tl                      # Short alias
/tl summary              # Quick summary stats
/tl sync                 # Sync with all task files
/tl feature [name]       # Focus on specific feature
```

## Description

The Task Ledger (`.task-ledger.md`) provides a persistent, single-file view of all tasks across all features. It automatically updates as you work and persists across sessions.

### Key Benefits
- **Never lose task state** - Survives session restarts
- **GitHub issue linking** - Direct connection to issues
- **Progress tracking** - See completion at a glance
- **Quick navigation** - Jump to any feature's tasks
- **Auto-updated** - Hook system keeps it current

## Subcommands

### View Ledger
```bash
/task-ledger
/tl
```
Shows the complete task ledger with all features, their progress, and quick actions.

### Summary View
```bash
/tl summary
```
Shows just the summary stats:
- Total features and tasks
- Completion percentage
- Features in each state
- Top priorities

### Sync Ledger
```bash
/tl sync
```
Scans all task files and updates the ledger. Useful if the ledger gets out of sync or when starting to use the ledger on an existing project.

### Feature Focus
```bash
/tl feature user-auth
```
Shows detailed view of a specific feature including:
- Current progress with task list
- Related files (PRD, tasks, tests)
- Git history for the feature
- Time tracking (if enabled)

## Integration with Existing Commands

The Task Ledger enhances these existing commands:

### Task Status (`/ts`)
- Now reads from persistent ledger
- Shows cross-session progress
- Links to GitHub issues

### Task Board (`/tb`)  
- Uses ledger for state persistence
- Accurate progress tracking
- Better feature organization

### Smart Resume (`/sr`)
- Shows task ledger summary
- Highlights in-progress features
- Suggests next actions based on ledger

### Work Status (`/ws`)
- Enhanced with ledger data
- Better progress visibility
- Historical tracking

### Process Tasks (`/pt`)
- Updates ledger in real-time
- Shows progress bar from ledger
- Maintains state across sessions

## Example Output

```markdown
# Task Ledger - my-awesome-app

**Last Updated**: 2024-01-20 14:30:45

## Summary
- **Total Features**: 4
- **Active Tasks**: 87
- **Completed**: 52 (59.8%)
- **In Progress**: 2

---

## Features

### user-authentication

**Created**: 2024-01-15 09:00:00
**Issue**: #23
**Branch**: `feature/23-user-auth`
**Status**: 🔄 In Progress
**Progress**: 18/23 tasks

**Files**:
- Tasks: `docs/project/features/user-authentication-tasks.md`
- PRD: `docs/project/features/user-authentication-PRD.md`
- Tests: `tests/user-authentication/`

**Quick Actions**:
- Process tasks: `/pt user-authentication`
- View board: `/tb`
- Check tests: `/tr tests/user-authentication`

---

### payment-integration

**Created**: 2024-01-18 11:00:00
**Issue**: #24
**Branch**: `feature/24-payments`
**Status**: ✅ Completed
**Progress**: 34/34 tasks

**Files**:
- Tasks: `docs/project/features/payment-integration-tasks.md`
- PRD: `docs/project/features/payment-integration-PRD.md`
- Tests: `tests/payment-integration/`

---
```

## Automatic Updates

The ledger is automatically updated by the `15b-task-ledger-updater.py` hook when:
- New task files are created (`/gt`)
- Tasks are marked complete (`/pt`)
- PRDs are created (`/prd`)
- Features are completed (`/fw complete`)

## Configuration

Configure in `.claude/hooks/config.json`:
```json
{
  "task_ledger": {
    "enabled": true,
    "auto_sync": true,
    "track_time": false,
    "include_in_gist": true,
    "show_in_commands": ["sr", "ws", "ts", "tb"]
  }
}
```

## Best Practices

1. **Let it work automatically** - The hook system maintains it
2. **Use `/tl sync` after major changes** - Ensures accuracy
3. **Check summary in `/sr`** - Quick daily overview
4. **Reference in standup** - Perfect for daily updates
5. **Include in PR description** - Shows what was done

## Chains Integration

The task ledger is included in these chains:
- `daily-startup` - Shows ledger summary
- `task-sprint` - Updates ledger progress
- `feature-planning` - Creates ledger entries
- `feature-complete` - Marks features complete

## Tips

- The ledger is included in GitHub gist saves
- Use `/tl feature [name]` for deep dives
- The ledger helps with sprint planning
- Perfect for handoffs between team members
- Integrates with existing task commands

This command enhances rather than replaces the existing task system!
