---
name: cleanup-parallel
description: Clean up work trees and branches after parallel development
args: [feature_name, keep_best]
---

# Cleanup Parallel Development

Cleaning up work trees and branches for {{feature_name}}.

## Process

### 1. List Current Work Trees
```bash
echo "Current work trees for {{feature_name}}:"
git worktree list | grep {{feature_name}}
```

### 2. Check for Uncommitted Changes
```bash
for i in 1 2 3; do
  if [ -d ".trees/{{feature_name}}-v$i" ]; then
    echo "Checking .trees/{{feature_name}}-v$i..."
    cd .trees/{{feature_name}}-v$i
    
    if [ -n "$(git status --porcelain)" ]; then
      echo "⚠️  Uncommitted changes in v$i"
      git status --short
    else
      echo "✅ v$i is clean"
    fi
    
    cd -
  fi
done
```

### 3. Archive Results (Optional)
```bash
# Save results before cleanup
ARCHIVE_DIR=".claude/archive/parallel/{{feature_name}}-$(date +%Y%m%d)"
mkdir -p "$ARCHIVE_DIR"

for i in 1 2 3; do
  if [ -d ".trees/{{feature_name}}-v$i" ]; then
    # Copy results file
    if [ -f ".trees/{{feature_name}}-v$i/RESULTS.md" ]; then
      cp ".trees/{{feature_name}}-v$i/RESULTS.md" "$ARCHIVE_DIR/results-v$i.md"
    fi
    
    # Save git diff
    cd .trees/{{feature_name}}-v$i
    git diff main > "$ARCHIVE_DIR/diff-v$i.patch"
    cd -
  fi
done

echo "📁 Results archived to $ARCHIVE_DIR"
```

### 4. Remove Work Trees
```bash
# Keep best version if specified
KEEP_VERSION="{{keep_best}}"

for i in 1 2 3; do
  if [ "$KEEP_VERSION" = "$i" ]; then
    echo "📌 Keeping v$i as requested"
    continue
  fi
  
  if [ -d ".trees/{{feature_name}}-v$i" ]; then
    echo "Removing work tree v$i..."
    git worktree remove .trees/{{feature_name}}-v$i --force
    echo "✅ Removed .trees/{{feature_name}}-v$i"
  fi
done
```

### 5. Delete Feature Branches
```bash
# Delete local branches
for i in 1 2 3; do
  if [ "$KEEP_VERSION" = "$i" ]; then
    continue
  fi
  
  BRANCH="feature/{{feature_name}}-v$i"
  if git show-ref --verify --quiet refs/heads/$BRANCH; then
    echo "Deleting branch $BRANCH..."
    git branch -D $BRANCH
    echo "✅ Deleted $BRANCH"
  fi
done

# Optional: Delete remote branches
echo "Delete remote branches? (y/n)"
read -r response

if [ "$response" = "y" ]; then
  for i in 1 2 3; do
    if [ "$KEEP_VERSION" = "$i" ]; then
      continue
    fi
    
    BRANCH="feature/{{feature_name}}-v$i"
    git push origin --delete $BRANCH 2>/dev/null || echo "Remote branch $BRANCH not found"
  done
fi
```

### 6. Clean Git References
```bash
# Prune worktree references
git worktree prune

# Clean up refs
git gc --prune=now
```

### 7. Final Report
```markdown
## Cleanup Summary

Feature: {{feature_name}}
Date: $(date '+%Y-%m-%d %H:%M:%S')

### Removed
- Work trees: [List removed]
- Branches: [List deleted]

### Preserved
- Best version: v{{keep_best}} (if specified)
- Archives: $ARCHIVE_DIR

### Disk Space Recovered
$(du -sh .trees 2>/dev/null || echo "N/A")

✅ Cleanup complete!
```

## Usage Examples

```bash
# Clean up everything
/cleanup-parallel "user-auth" ""

# Keep version 2
/cleanup-parallel "user-auth" "2"

# Archive and clean
/cleanup-parallel "payment-integration" ""
```

## Important Notes
- Always archive results before cleanup
- Consider keeping the best implementation
- Check for uncommitted changes first
- Can be undone by checking out branches again
