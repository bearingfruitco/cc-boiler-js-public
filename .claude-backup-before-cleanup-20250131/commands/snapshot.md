# Snapshot Command

Take a snapshot of current state or manage existing snapshots for instant rollback capability.

## Arguments:
- $ACTION: create|list|preview|rollback|diff|auto|clean
- $SNAPSHOT_ID: Snapshot number or name (for preview/rollback/diff)
- $DESCRIPTION: Description for create action (optional)

## Why This Command:
- **Fearless Experimentation**: Try anything knowing you can instantly rollback
- **AI Safety Net**: When Claude makes mistakes, rollback in seconds
- **Time Travel**: Compare states across time to understand changes
- **Zero Git Pollution**: No commits needed for experimentation

## Actions:

### Create Manual Snapshot
```bash
/snapshot create "before auth refactor"
/snapshot create  # Uses "manual" as description
```
Creates a snapshot with your description.

### List Snapshots
```bash
/snapshot list
/snapshot list --all  # Show all including auto snapshots
```
Shows recent snapshots:
```
Recent Snapshots:
1. [2025-01-15-14:30:00] before-auth-refactor (2 hours ago)
   Files: 5 | Branch: feature/auth | Size: 12KB
   
2. [2025-01-15-13:00:00] auto (3 hours ago)
   Files: 12 | Branch: feature/auth | Size: 45KB
   Reason: Multiple file edit operation
   
3. [2025-01-15-10:00:00] before-migration (6 hours ago)
   Files: 3 | Branch: main | Size: 8KB
   ⭐ Important (protected from cleanup)
```

### Preview Snapshot
```bash
/snapshot preview 1
/snapshot preview before-auth-refactor  # By name
```
Shows what would be restored:
```
Snapshot: before-auth-refactor
Created: 2025-01-15 14:30:00 (2 hours ago)
Branch: feature/auth
Files that would be restored:
  ✓ components/auth/LoginForm.tsx (modified)
  ✓ lib/auth.ts (modified)
  + app/api/auth/route.ts (deleted - would be restored)
  - components/temp.tsx (created after - would be removed)

Current uncommitted changes would be backed up to:
.claude/snapshots/rollback-backup-2025-01-15-16-30-00.tar.gz
```

### Rollback to Snapshot
```bash
/snapshot rollback 1
/snapshot rollback 1 --no-backup  # Skip backup of current state
```
Restores files from snapshot:
```
⚠️  Rollback Confirmation
This will restore 5 files from: before-auth-refactor
Current changes will be backed up first.

Files to restore:
- components/auth/LoginForm.tsx
- lib/auth.ts
- app/api/auth/route.ts (deleted file)

Continue? (y/n): y

✅ Rollback complete!
- Backup saved to: rollback-backup-2025-01-15-16-30-00
- 5 files restored
- Run 'git status' to see changes
```

### Compare Snapshots
```bash
/snapshot diff 1 2
/snapshot diff current 1  # Compare current state with snapshot
```
Shows differences:
```
Comparing: before-auth-refactor ↔ auto

Files changed between snapshots:
  M components/Header.tsx
  A components/auth/AuthProvider.tsx
  D lib/old-auth.ts

Summary: 3 files changed, 145 insertions(+), 89 deletions(-)
```

### Toggle Auto-Snapshot
```bash
/snapshot auto
/snapshot auto on
/snapshot auto off
```
Controls automatic snapshot creation:
```
Auto-snapshot: ENABLED ✓
Will create snapshots when:
- Editing 5+ files
- Modifying critical files (package.json, .env, etc.)
- Running risky commands
- Using MultiEdit tool
```

### Clean Old Snapshots
```bash
/snapshot clean
/snapshot clean --keep 10  # Keep only 10 most recent
/snapshot clean --older-than 7d  # Remove older than 7 days
```

### Mark Important
```bash
/snapshot important 3
/snapshot important before-migration
```
Protects snapshot from automatic cleanup.

## Integration Features:

### 1. **Automatic Snapshots**
Created automatically when:
- Multiple files being edited (5+)
- Critical files modified (package.json, .env, tsconfig.json)
- Before database migrations
- Before running risky bash commands
- Using MultiEdit for large refactors

### 2. **Git Integration**
- Tracks branch and commit at snapshot time
- Shows if you've switched branches since snapshot
- Warns about conflicts with current branch state

### 3. **Smart Compression**
- Uses tar.gz compression (~70% space savings)
- Excludes node_modules, .next, dist automatically
- Only stores changed files, not entire project

### 4. **Context Preservation**
- Saves Claude's current context with snapshot
- Can restore both files and conversation context
- Perfect for resuming after breaks

## Example Workflows:

### Experimenting with Refactor
```bash
# Before starting risky refactor
/snapshot create "pre-refactor baseline"

# Do the refactor...
/cc AuthSystem --refactor

# If it goes wrong
/snapshot rollback 1

# If it goes well
/snapshot clean  # Remove safety snapshot
```

### Comparing Approaches
```bash
# Try approach 1
/snapshot create "approach-1-complete"

# Rollback and try approach 2
/snapshot rollback main
/snapshot create "approach-2-complete"

# Compare results
/snapshot diff approach-1-complete approach-2-complete
```

### Daily Workflow Protection
```bash
# Morning
/sr  # Smart resume
# Auto-snapshot enabled by default

# Work normally - snapshots created automatically
# Edit multiple files...

# Something breaks
/snapshot list
/snapshot rollback 1  # Back to working state
```

## Configuration:

Settings stored in `.claude/snapshots/manifest.json`:
```json
{
  "settings": {
    "max_snapshots": 20,
    "auto_snapshot": true,
    "min_files_for_auto": 5,
    "exclude_patterns": [
      "node_modules",
      ".next",
      "dist",
      "build",
      "*.log"
    ]
  }
}
```

## Tips:

1. **Name Important Snapshots**: Use descriptive names for manual snapshots
2. **Review Before Rollback**: Always preview first with `/snapshot preview`
3. **Clean Periodically**: Old snapshots are auto-cleaned, but manual cleanup helps
4. **Branch Awareness**: Snapshots are branch-local, switch carefully
5. **Combine with Git**: Snapshots complement but don't replace git commits

## Safety Features:

- **Backup Before Rollback**: Current state always backed up first
- **Confirmation Required**: Rollback requires explicit confirmation  
- **Non-Blocking**: Snapshot creation never blocks your workflow
- **Error Recovery**: Corrupted snapshots are skipped gracefully
- **Space Efficient**: Automatic cleanup prevents disk bloat

This command enables fearless experimentation - try anything knowing you can instantly return to a working state!
