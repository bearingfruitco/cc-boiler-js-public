---
name: prp-status
aliases: [prp-progress, check-prp-status, prp-info]
description: Check execution status and progress of PRPs
category: PRPs
---

# PRP Status: $ARGUMENTS

Display comprehensive status of PRP execution including progress, validation history, and blockers.

## Status Overview:

### 1. Basic Information
```yaml
PRP: user-authentication
Location: PRPs/active/user-authentication.md
Created: 2024-01-15
Last Activity: 2024-01-16 14:30
Confidence Score: 8/10
Current Stage: Implementation
```

### 2. Progress Tracking
```
Task Progress:
━━━━━━━━━━━━━━━━━━━━ 65% (13/20 tasks)

Completed:
✅ Create user model
✅ Setup database migrations  
✅ Implement JWT utilities
✅ Create auth endpoints
⏳ Add middleware (in progress)
⏹️ Write tests (pending)
⏹️ Documentation (pending)
```

### 3. File Modifications
```
Files Modified: 15
├── src/models/user.py ✓
├── src/api/auth.py ✓
├── src/utils/jwt.py ✓
├── tests/test_auth.py (partial)
└── ... 11 more files
```

### 4. Validation History
```
Level 1 (Syntax):    ✅ Last run: 10 min ago
Level 2 (Unit):      ✅ Last run: 1 hour ago  
Level 3 (Integration): ❌ Last run: 2 hours ago
  └─ Error: Database connection timeout
Level 4 (Production): ⏹️ Not run yet
```

### 5. Blockers & Issues
```
Active Blockers:
🚫 Bug #127: JWT refresh token not working
⚠️ Missing dependency: python-jose==3.3.0
⏰ Waiting on: Database schema approval
```

### 6. Time Tracking
```
Time Spent: 4h 32m
├── Implementation: 3h 15m
├── Testing: 45m
├── Debugging: 32m
└── Validation: 0m (automated)

Estimated Remaining: 2h 30m
```

## Command Options:

```bash
# Basic status
/prp-status auth

# Detailed status with history
/prp-status auth --detailed

# All active PRPs
/prp-status --all

# Export status report
/prp-status auth --export
```

## Status Indicators:

- ✅ Complete
- ⏳ In Progress  
- ⏹️ Pending
- ❌ Failed
- 🚫 Blocked
- ⚠️ Warning

## Integration with Other Commands:

```bash
# Check status before continuing
/prp-status auth
/pt auth  # Continue processing

# Resolve blockers
/prp-status auth
/bt resolve 127  # Fix blocker
/prp-execute auth --retry

# Export for team update
/prp-status --all --export > team-update.md
```

## Data Sources:

Pulls information from:
- `.claude/metrics/prp_progress/`
- `.claude/metrics/prp_validation/`
- `.claude/bugs/bugs.json`
- Git status for file changes
- Task tracking from PRPs/active/

## Auto-Refresh:

Status automatically updates when:
- Files are modified
- Validation runs complete
- Tasks are marked complete
- Bugs are added/resolved