# Branch Protection System Flow

## Visual Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    BRANCH PROTECTION SYSTEM                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐        ┌──────────────┐       ┌─────────────┐ │
│  │   FEATURE    │        │    BRANCH    │       │    HOOK     │ │
│  │    STATE     │◄──────►│   REGISTRY   │◄─────►│   SYSTEM    │ │
│  │              │        │              │       │             │ │
│  │ • Completed  │        │ • Active     │       │ • Pre-tool  │ │
│  │ • Protected  │        │ • Blocked    │       │ • Enforce   │ │
│  │ • Files      │        │ • Rules      │       │ • Protect   │ │
│  └──────────────┘        └──────────────┘       └─────────────┘ │
│          ▲                       ▲                      ▲        │
│          │                       │                      │        │
│          └───────────────────────┴──────────────────────┘        │
│                              COMMANDS                             │
│  ┌────────────┬────────────┬────────────┬────────────┬────────┐ │
│  │   /bs      │   /fs      │  /sync     │  /switch   │  /fc   │ │
│  │ branch     │ feature    │ sync-main  │ branch     │feature │ │
│  │ status     │ status     │            │ switch     │complete│ │
│  └────────────┴────────────┴────────────┴────────────┴────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Protection Flow

### 1. Starting New Work
```
User: /fw start 50
         │
         ▼
┌─────────────────┐
│ Check Registry  │
├─────────────────┤
│ • Branch limit? │──Yes──→ ❌ BLOCKED: Too many branches
│ • Main synced?  │──No───→ ❌ BLOCKED: Sync main first
│ • Tests pass?   │──No───→ ⚠️ WARNING: Fix tests
└────────┬────────┘
         │ All OK
         ▼
    ✅ Create Branch
```

### 2. Modifying Files
```
User: Edit LoginForm.tsx
         │
         ▼
┌─────────────────┐
│ Feature State   │
├─────────────────┤
│ Is completed?   │──Yes──┐
│ Is protected?   │──Yes──┤
└─────────────────┘       │
                          ▼
                ┌─────────────────┐
                │ Branch Check    │
                ├─────────────────┤
                │ Correct branch? │──No──→ ❌ BLOCKED
                │ Enhancement?    │──No──→ ❌ BLOCKED
                └────────┬────────┘
                         │ Yes
                         ▼
                    ✅ Allow Edit
```

### 3. File Conflict Prevention
```
Branch A: Modifying api.ts ──┐
                             ├──→ Registry ──→ api.ts BLOCKED by A
Branch B: Try edit api.ts ───┘                        │
                                                      ▼
                                               ❌ Cannot modify
```

## State File Structure

### feature-state.json
```json
{
  "features": {
    "auth": {
      "status": "completed",
      "files": ["LoginForm.tsx"],
      "do_not_recreate": true
    }
  }
}
     │
     ├──→ Protects files from recreation
     └──→ Tracks enhancements
```

### branch-registry.json  
```json
{
  "active_branches": [{
    "name": "feature/47",
    "files_modified": ["api.ts"]
  }],
  "blocked_files": {
    "api.ts": {
      "blocked_by": "feature/47"
    }
  }
}
     │
     ├──→ Prevents conflicts
     └──→ Enforces limits
```

## Common Scenarios

### Scenario 1: Protected Feature
```
main
 └── auth (completed) ──→ LoginForm.tsx [PROTECTED]
      │
      └── feature/auth-mfa ──→ Can modify LoginForm.tsx ✅
      │
      └── feature/random ────→ Cannot modify LoginForm.tsx ❌
```

### Scenario 2: Branch Limits
```
Active Branches (Max: 2)
├── feature/47 ✅
├── feature/52 ✅
└── feature/99 ❌ BLOCKED - At limit
```

### Scenario 3: Stale Main
```
main (last sync: 48h ago) ❌
 │
 └── feature/new ❌ Cannot create - sync main first
```

## Benefits

1. **No Lost Work** - Can't overwrite completed features
2. **No Conflicts** - Files locked to branches
3. **Clean History** - Orderly branch progression
4. **Clear State** - Always know what's where
5. **Team Friendly** - Shared understanding

## Quick Checks

```bash
# Am I protected?
/feature-status auth

# Can I create branch?  
/branch-status

# Is main current?
/sync-main --dry-run

# What's blocking me?
Check the hook output - it explains everything!
```
