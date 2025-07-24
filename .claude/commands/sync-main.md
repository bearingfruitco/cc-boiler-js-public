# Sync Main

Safely sync the main branch with remote repository.

## Arguments:
- $1: --force (optional) - Force sync even with uncommitted changes

## Steps:

```bash
FORCE_MODE="$1"

echo "## 🔄 Syncing Main Branch"
echo ""

# 1. Check current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"

# 2. Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
  if [ "$FORCE_MODE" != "--force" ]; then
    echo "❌ You have uncommitted changes!"
    echo ""
    echo "Options:"
    echo "1. Commit changes: git add . && git commit -m 'WIP'"
    echo "2. Stash changes: git stash"
    echo "3. Force sync: /sync-main --force"
    exit 1
  else
    echo "⚠️  Stashing uncommitted changes..."
    git stash push -m "Auto-stash before main sync $(date +%Y%m%d_%H%M%S)"
  fi
fi

# 3. Switch to main
if [ "$CURRENT_BRANCH" != "main" ]; then
  echo "Switching to main branch..."
  git checkout main || {
    echo "❌ Failed to switch to main"
    exit 1
  }
fi

# 4. Pull latest changes
echo -e "\n📥 Pulling latest changes..."
git pull origin main --rebase || {
  echo "❌ Failed to pull from origin"
  echo "You may need to resolve conflicts"
  exit 1
}

# 5. Update branch registry
echo -e "\n📝 Updating branch registry..."

REGISTRY_FILE=".claude/branch-state/branch-registry.json"
if [ -f "$REGISTRY_FILE" ]; then
  # Update last_pulled timestamp
  CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  CURRENT_COMMIT=$(git rev-parse HEAD)
  
  # Use jq to update the JSON
  jq ".main_branch.last_pulled = \"$CURRENT_TIME\" | .main_branch.stable_commit = \"$CURRENT_COMMIT\"" "$REGISTRY_FILE" > "$REGISTRY_FILE.tmp" && mv "$REGISTRY_FILE.tmp" "$REGISTRY_FILE"
  
  echo "✅ Registry updated"
fi

# 6. Show what changed
echo -e "\n## 📊 Sync Summary"
echo "• Branch: main"
echo "• Latest commit: $(git log -1 --pretty=format:'%h - %s')"
echo "• Updated at: $(date)"

# 7. Return to original branch if different
if [ "$CURRENT_BRANCH" != "main" ] && [ "$CURRENT_BRANCH" != "" ]; then
  echo -e "\n🔄 Returning to $CURRENT_BRANCH..."
  git checkout "$CURRENT_BRANCH"
  
  # Restore stash if we created one
  if [ "$FORCE_MODE" = "--force" ]; then
    echo "📦 Restoring stashed changes..."
    git stash pop
  fi
fi

# 8. Show next steps
echo -e "\n## 💡 Next Steps"
echo "• Create new feature branch: /fw start [issue]"
echo "• Check branch status: /branch-status"
echo "• View features: /feature-status"

# 9. Check if current branch needs rebase
if [ "$CURRENT_BRANCH" != "main" ] && [ "$CURRENT_BRANCH" != "" ]; then
  # Check if current branch is behind main
  BEHIND=$(git rev-list --count HEAD..main)
  if [ "$BEHIND" -gt 0 ]; then
    echo -e "\n⚠️  Current branch is $BEHIND commits behind main"
    echo "Consider rebasing: git rebase main"
  fi
fi
```

## Example Output:

```
## 🔄 Syncing Main Branch

Current branch: feature/auth-mfa

📥 Pulling latest changes...
From github.com:company/repo
   abc123..def456  main -> origin/main
Successfully rebased and updated refs/heads/main.

📝 Updating branch registry...
✅ Registry updated

## 📊 Sync Summary
• Branch: main
• Latest commit: def456 - Add user profile endpoints
• Updated at: Mon Jan 21 10:30:00 PST 2025

🔄 Returning to feature/auth-mfa...
Switched to branch 'feature/auth-mfa'

## 💡 Next Steps
• Create new feature branch: /fw start [issue]
• Check branch status: /branch-status
• View features: /feature-status

⚠️  Current branch is 3 commits behind main
Consider rebasing: git rebase main
```

## Error Handling:

```
## 🔄 Syncing Main Branch

Current branch: feature/auth-mfa
❌ You have uncommitted changes!

Options:
1. Commit changes: git add . && git commit -m 'WIP'
2. Stash changes: git stash
3. Force sync: /sync-main --force
```

## Integration:
- Called before `/fw start`
- Part of branch management
- Updates registries automatically
