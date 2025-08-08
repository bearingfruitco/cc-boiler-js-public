---
name: parallel-merge
description: Merge the best parallel implementation back to main branch
args: [feature_name, selected_version]
---

# Merge Best Implementation of {{feature_name}}

Merging version {{selected_version}} back to main branch.

## Merge Process

### 1. Review Selected Implementation
```bash
cd .trees/{{feature_name}}-v{{selected_version}}
git log --oneline -5
git diff --stat
```

### 2. Run Final Tests
```bash
npm test
npm run test:e2e
```

### 3. Switch to Main Branch
```bash
cd ../..
git checkout main
git pull origin main
```

### 4. Merge Selected Implementation
```bash
git merge feature/{{feature_name}}-v{{selected_version}}
```

### 5. Clean Up Work Trees
```bash
# Remove work trees
git worktree remove .trees/{{feature_name}}-v1
git worktree remove .trees/{{feature_name}}-v2
git worktree remove .trees/{{feature_name}}-v3

# Delete feature branches
git branch -d feature/{{feature_name}}-v1
git branch -d feature/{{feature_name}}-v2
git branch -d feature/{{feature_name}}-v3
```

### 6. Push to Remote
```bash
git push origin main
```

## Success Report
```
✅ Implementation v{{selected_version}} merged to main
✅ Work trees cleaned up
✅ Feature branches removed
✅ Changes pushed to remote

Feature {{feature_name}} successfully implemented using parallel development!
```

## Benefits Achieved
- Explored {{num_agents}} different approaches
- Selected best implementation
- Reduced development time by ~{{num_agents}}x
- Increased confidence through comparison
