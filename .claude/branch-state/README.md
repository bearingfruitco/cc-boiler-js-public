# Branch Management & Feature Protection System

## Overview

This system prevents AI agents from accidentally recreating completed features or creating conflicting branches. It maintains awareness of what's already built and enforces branch discipline.

## Quick Start

```bash
# Run setup script
./setup-branch-management.sh

# Check your branch status
/branch-status

# See what features exist
/feature-status

# Sync main branch
/sync-main
```

## Core Concepts

### 1. Feature State Protection
- Tracks completed features and their files
- Prevents recreation of working code
- Ensures enhancements use proper branches

### 2. Branch Management
- Limits active branches (default: 2)
- Requires main branch synchronization
- Prevents file conflicts between branches

## Commands

### `/branch-status` (aliases: `/bs`, `/branch`)
Shows comprehensive branch overview including:
- Current branch and health
- Active branch count vs limit
- Blocked files
- Sync status with main

### `/feature-status [name]` (aliases: `/fs`, `/feature`)
Shows details about a specific feature:
- Completion status
- Working implementation details
- Files associated with feature
- Active enhancements

### `/sync-main` (aliases: `/sync`, `/pull-main`)
Safely syncs main branch:
- Stashes uncommitted changes
- Updates from origin
- Returns to original branch
- Shows what changed

## Protection Examples

### Example 1: Preventing Feature Recreation
```
You: /cc LoginForm

⚠️ FEATURE STATE PROTECTION!

You're about to modify a COMPLETED feature that's already working!

📍 Feature: user-authentication
📄 File: components/auth/LoginForm.tsx
✅ Status: completed (2025-01-15)
🌿 Current Branch: feature/random-work
⚠️ Main Branch Has: JWT-based authentication with Supabase

💡 Recommended Actions:
1. Switch to main: git checkout main && git pull
2. Create enhancement branch: git checkout -b feature/enhance-auth
3. Or continue on: feature/47-auth-mfa
```

### Example 2: Branch Limit Enforcement
```
You: /fw start 99

🚫 BRANCH LIMIT EXCEEDED!

You already have 2 active branch(es) (max: 2):
  • feature/47-lead-form-prefill (Issue: #47)
  • feature/52-api-endpoints (Issue: #52)

💡 To create a new branch, first:
1. Complete current work: /fw complete 47
2. Or stash work: /branch stash
3. Or close branch: /branch close
```

### Example 3: File Conflict Prevention
```
You: Create new branch to modify import script

⚠️ FILE CONFLICT DETECTED!

These files are being modified on another branch:
  • scripts/import_to_leads_comprehensive.py
    Branch: feature/17-import-fix
    Issue: #17

💡 Options:
1. Work on different files
2. Wait for other branch to merge
3. Collaborate on existing branch: git checkout feature/17-import-fix
```

## Configuration

Edit `.claude/hooks/config.json`:

```json
{
  "branch_management": {
    "enabled": true,
    "max_active_branches": 2,        // Increase for larger teams
    "require_main_sync_hours": 24,   // How often to sync main
    "require_tests_before_new": false,// Require passing tests
    "block_conflicting_files": true,  // Prevent file conflicts
    "strict_mode": false             // true = block, false = warn
  },
  "feature_protection": {
    "enabled": true,
    "protect_from_recreation": true,  // Protect completed features
    "require_enhancement_branches": true,
    "warn_on_wrong_branch": true
  }
}
```

## State Files

### `.claude/branch-state/feature-state.json`
Tracks completed features and their implementations:
```json
{
  "features": {
    "user-authentication": {
      "status": "completed",
      "files": ["components/auth/LoginForm.tsx"],
      "working_implementation": {
        "description": "JWT auth with Supabase"
      }
    }
  }
}
```

### `.claude/branch-state/branch-registry.json`
Tracks active branches and rules:
```json
{
  "active_branches": [{
    "name": "feature/47-form",
    "issue": "#47",
    "files_modified": ["components/forms/LeadForm.tsx"]
  }],
  "blocked_files": {
    "components/forms/LeadForm.tsx": {
      "blocked_by": "feature/47-form"
    }
  }
}
```

## Workflow Integration

### Enhanced Smart Resume
```bash
/sr
# Now shows:
# - Branch health status
# - Protected features you're working on
# - Branch conflicts
# - Enhancement tracking
```

### Enhanced Feature Workflow
```bash
/fw start 50
# Now checks:
# - Branch limits
# - Main sync status
# - File conflicts
# - Related features
```

## Best Practices

1. **Regular Maintenance**
   ```bash
   # Daily routine
   /sync-main          # Start with fresh main
   /branch-status      # Check branch health
   /sr                 # Resume with context
   ```

2. **Feature Completion**
   ```bash
   # After merging to main
   /feature-complete user-authentication
   # Updates feature-state.json
   # Removes from active branches
   # Unblocks files
   ```

3. **Team Coordination**
   - Commit state files to git
   - Share branch ownership
   - Review conflicts in standups

## Troubleshooting

### Q: Protection is too aggressive
A: Set `strict_mode: false` in config for warnings only

### Q: How to override protection?
A: Add `--force` flag (use sparingly):
```bash
/cc LoginForm --force
```

### Q: Branch limit too restrictive?
A: Increase `max_active_branches` in config

### Q: How to unblock a file?
A: Edit `.claude/branch-state/branch-registry.json` and remove from `blocked_files`

## Advanced Features

### Feature Families
Group related features:
```json
{
  "feature_families": {
    "authentication": ["user-auth", "social-login", "mfa"],
    "forms": ["lead-form", "contact-form", "survey-form"]
  }
}
```

### Auto-Detection
System automatically detects:
- When you're on wrong branch for a feature
- When files would conflict
- When main is stale
- When branches are abandoned

## Future Enhancements

- [ ] Auto-merge completed branches
- [ ] Feature dependency tracking
- [ ] Branch age warnings
- [ ] Conflict resolution assistance
- [ ] Team member assignment
