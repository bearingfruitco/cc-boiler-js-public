# Branch Switch

Smart branch switching with context preservation and validation.

## Arguments:
- $1: branch-name (required) - Branch to switch to
- $2: --force (optional) - Force switch even with uncommitted changes

## Steps:

```bash
TARGET_BRANCH="$1"
FORCE_MODE="$2"

if [ -z "$TARGET_BRANCH" ]; then
  echo "❌ Error: Branch name required"
  echo "Usage: /branch-switch [branch-name] [--force]"
  echo ""
  echo "Available branches:"
  git branch | sed 's/^/  /'
  exit 1
fi

echo "## 🔄 Smart Branch Switch"
echo ""

# 1. Current state check
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"

if [ "$CURRENT_BRANCH" = "$TARGET_BRANCH" ]; then
  echo "✅ Already on branch $TARGET_BRANCH"
  exit 0
fi

# 2. Check for uncommitted changes
CHANGES=$(git status --porcelain)
if [ ! -z "$CHANGES" ] && [ "$FORCE_MODE" != "--force" ]; then
  echo "❌ You have uncommitted changes!"
  echo ""
  echo "Changed files:"
  git status --porcelain | head -5 | sed 's/^/  /'
  echo ""
  echo "Options:"
  echo "1. Commit: git add . && git commit -m 'WIP: $CURRENT_BRANCH'"
  echo "2. Stash: git stash push -m 'WIP: $CURRENT_BRANCH'"
  echo "3. Force: /branch-switch $TARGET_BRANCH --force"
  exit 1
fi

# 3. Save current context
echo "💾 Saving current context..."

# Create branch context file
CONTEXT_DIR=".claude/branch-context"
mkdir -p "$CONTEXT_DIR"

CONTEXT_FILE="$CONTEXT_DIR/${CURRENT_BRANCH//\//_}.md"
cat > "$CONTEXT_FILE" << EOF
# Branch Context: $CURRENT_BRANCH

## Last Active: $(date)

## Current State:
- Modified files: $(git status --porcelain | wc -l)
- Last commit: $(git log -1 --pretty=format:'%h - %s')

## Current Work:
$(git status --porcelain | head -10)

## TODOs:
$(grep -r "TODO:" --include="*.tsx" --include="*.ts" . 2>/dev/null | grep -v node_modules | head -5)

## Notes:
[Add your notes here]
EOF

# Auto-stash if forced
if [ ! -z "$CHANGES" ] && [ "$FORCE_MODE" = "--force" ]; then
  echo "📦 Auto-stashing changes..."
  STASH_MSG="Auto-stash: $CURRENT_BRANCH $(date +%Y%m%d_%H%M%S)"
  git stash push -m "$STASH_MSG"
  echo "Stashed as: $STASH_MSG"
fi

# 4. Update branch registry
BRANCH_REGISTRY=".claude/branch-state/branch-registry.json"
if [ -f "$BRANCH_REGISTRY" ]; then
  # Update last accessed time for current branch
  TEMP_FILE="$BRANCH_REGISTRY.tmp"
  cat "$BRANCH_REGISTRY" | jq "
    .active_branches = [.active_branches[] | 
      if .name == \"$CURRENT_BRANCH\" then 
        . + {last_accessed: \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"} 
      else . end
    ]
  " > "$TEMP_FILE" && mv "$TEMP_FILE" "$BRANCH_REGISTRY"
fi

# 5. Switch branch
echo ""
echo "🔀 Switching to $TARGET_BRANCH..."
git checkout "$TARGET_BRANCH" || {
  echo "❌ Failed to switch branches"
  exit 1
}

# 6. Load target context
TARGET_CONTEXT_FILE="$CONTEXT_DIR/${TARGET_BRANCH//\//_}.md"
if [ -f "$TARGET_CONTEXT_FILE" ]; then
  echo ""
  echo "📋 Previous context for $TARGET_BRANCH:"
  echo "================================"
  head -20 "$TARGET_CONTEXT_FILE"
  echo "================================"
fi

# 7. Check feature state
FEATURE_STATE=".claude/branch-state/feature-state.json"
if [ -f "$FEATURE_STATE" ]; then
  # Check if this branch is working on a feature
  FEATURE=$(cat "$FEATURE_STATE" | jq -r ".features | to_entries[] | select(.value.in_progress_enhancements.branch == \"$TARGET_BRANCH\") | .key" | head -1)
  
  if [ ! -z "$FEATURE" ]; then
    echo ""
    echo "🔧 Working on feature enhancement: $FEATURE"
    echo "Run: /feature-status $FEATURE"
  fi
fi

# 8. Show branch status
echo ""
echo "### 📊 Branch Status"

# Modified files
MODIFIED=$(git status --porcelain | wc -l)
echo "• Modified files: $MODIFIED"

# Behind/ahead of main
if [ "$TARGET_BRANCH" != "main" ]; then
  BEHIND=$(git rev-list --count HEAD..main 2>/dev/null || echo "0")
  AHEAD=$(git rev-list --count main..HEAD 2>/dev/null || echo "0")
  echo "• Behind main: $BEHIND commits"
  echo "• Ahead of main: $AHEAD commits"
fi

# Test status
if npm test --silent >/dev/null 2>&1; then
  echo "• Tests: ✅ Passing"
else
  echo "• Tests: ❌ Failing"
fi

# 9. Suggest next actions
echo ""
echo "### 💡 Next Actions"

if [ $MODIFIED -gt 0 ]; then
  echo "• Review changes: git status"
fi

if [ "$BEHIND" -gt "0" ] 2>/dev/null; then
  echo "• Update from main: git rebase main"
fi

if [ -f "$TARGET_CONTEXT_FILE" ]; then
  # Extract TODOs from context
  TODOS=$(grep -A5 "## TODOs:" "$TARGET_CONTEXT_FILE" | tail -n +2 | head -3)
  if [ ! -z "$TODOS" ]; then
    echo "• Continue with TODOs from context"
  fi
fi

echo "• Check status: /branch-status"
echo "• Resume work: /sr"

# 10. Check for stashed changes on this branch
echo ""
STASHES=$(git stash list | grep "$TARGET_BRANCH" | head -3)
if [ ! -z "$STASHES" ]; then
  echo "📦 Found stashes for this branch:"
  echo "$STASHES" | sed 's/^/  /'
  echo ""
  echo "To apply: git stash pop"
fi

echo ""
echo "✅ Switched to $TARGET_BRANCH"
```

## Example Output:

```
## 🔄 Smart Branch Switch

Current branch: feature/auth-mfa
💾 Saving current context...
📦 Auto-stashing changes...
Stashed as: Auto-stash: feature/auth-mfa 20250121_143022

🔀 Switching to feature/form-validation...
Switched to branch 'feature/form-validation'

📋 Previous context for feature/form-validation:
================================
# Branch Context: feature/form-validation

## Last Active: 2025-01-20 16:45:00

## Current State:
- Modified files: 2
- Last commit: abc123 - Add email validation

## Current Work:
M components/forms/validators.ts
M tests/validation.test.ts
================================

🔧 Working on feature enhancement: lead-form

### 📊 Branch Status
• Modified files: 2
• Behind main: 3 commits
• Ahead of main: 5 commits
• Tests: ✅ Passing

### 💡 Next Actions
• Review changes: git status
• Update from main: git rebase main
• Continue with TODOs from context
• Check status: /branch-status
• Resume work: /sr

📦 Found stashes for this branch:
  stash@{2}: WIP on feature/form-validation: Work in progress

To apply: git stash pop

✅ Switched to feature/form-validation
```

## Integration:
- Preserves context between switches
- Auto-stashes with --force
- Shows relevant information
- Part of branch workflow
