# Branch Status

Show comprehensive branch overview and health check.

## Arguments:
- $1: --detailed (optional) - Show more details

## Steps:

```bash
# 1. Load registries
FEATURE_STATE=$(cat .claude/branch-state/feature-state.json 2>/dev/null || echo '{}')
BRANCH_REGISTRY=$(cat .claude/branch-state/branch-registry.json 2>/dev/null || echo '{}')

# 2. Get current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "## 🌿 Current Branch: $CURRENT_BRANCH"

# 3. Check if current branch is in registry
BRANCH_INFO=$(echo "$BRANCH_REGISTRY" | jq -r ".active_branches[] | select(.name == \"$CURRENT_BRANCH\")")

if [ ! -z "$BRANCH_INFO" ]; then
  STATUS=$(echo "$BRANCH_INFO" | jq -r '.status')
  ISSUE=$(echo "$BRANCH_INFO" | jq -r '.issue')
  CREATED=$(echo "$BRANCH_INFO" | jq -r '.created')
  FILES_COUNT=$(echo "$BRANCH_INFO" | jq -r '.files_modified | length')
  
  echo "Status: $STATUS"
  echo "Issue: $ISSUE"
  echo "Created: $CREATED"
  echo "Files Modified: $FILES_COUNT"
fi

# 4. Show branch health
echo -e "\n## 🏥 Branch Health"

# Check if main is up to date
LAST_PULLED=$(echo "$BRANCH_REGISTRY" | jq -r '.main_branch.last_pulled')
if [ ! -z "$LAST_PULLED" ]; then
  # Calculate hours since last pull
  LAST_PULL_TIMESTAMP=$(date -d "$LAST_PULLED" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%SZ" "$LAST_PULLED" +%s 2>/dev/null)
  CURRENT_TIMESTAMP=$(date +%s)
  HOURS_DIFF=$(( ($CURRENT_TIMESTAMP - $LAST_PULL_TIMESTAMP) / 3600 ))
  
  if [ $HOURS_DIFF -gt 24 ]; then
    echo "⚠️  Main branch: Last synced $HOURS_DIFF hours ago (needs update)"
  else
    echo "✅ Main branch: Synced $HOURS_DIFF hours ago"
  fi
else
  echo "❓ Main branch: Never synced"
fi

# Check test status
if npm test --silent 2>&1 | grep -q "failed"; then
  echo "❌ Tests: Failing"
else
  echo "✅ Tests: Passing"
fi

# 5. Show active branches
echo -e "\n## 📊 Active Branches"
ACTIVE_COUNT=$(echo "$BRANCH_REGISTRY" | jq -r '.active_branches | length')
MAX_ALLOWED=$(echo "$BRANCH_REGISTRY" | jq -r '.branch_rules.max_active_branches')

echo "Active: $ACTIVE_COUNT / $MAX_ALLOWED allowed"

if [ $ACTIVE_COUNT -gt 0 ]; then
  echo "$BRANCH_REGISTRY" | jq -r '.active_branches[] | "  • \(.name) (Issue: \(.issue // "N/A"), Status: \(.status))"'
fi

# 6. Show blocked files
echo -e "\n## 🔒 Blocked Files"
BLOCKED_COUNT=$(echo "$BRANCH_REGISTRY" | jq -r '.blocked_files | length')

if [ $BLOCKED_COUNT -gt 0 ]; then
  echo "$BRANCH_REGISTRY" | jq -r '.blocked_files | to_entries[] | "  • \(.key) (blocked by: \(.value.blocked_by))"'
else
  echo "None"
fi

# 7. Show branch rules
echo -e "\n## 📋 Branch Rules"
echo "$BRANCH_REGISTRY" | jq -r '.branch_rules | 
  "• Max active branches: \(.max_active_branches)
• Require main sync: \(.require_main_sync)
• Require tests before new: \(.require_tests_before_new)
• Auto cleanup merged: \(.auto_cleanup_merged)
• Prevent conflicts: \(.prevent_conflicting_branches)"'

# 8. Show recommendations
echo -e "\n## 💡 Recommendations"

if [ $HOURS_DIFF -gt 24 ]; then
  echo "1. Sync main branch: /sync-main"
fi

if [ $ACTIVE_COUNT -ge $MAX_ALLOWED ]; then
  echo "2. Complete or close a branch before starting new work"
fi

# Check for stale branches
if [ $ACTIVE_COUNT -gt 0 ]; then
  # Would check age of branches here
  echo "3. Review active branches for staleness"
fi
```

## Example Output:

```
## 🌿 Current Branch: feature/auth-enhancement
Status: in_progress
Issue: #42
Created: 2025-01-20T10:00:00Z
Files Modified: 3

## 🏥 Branch Health
✅ Main branch: Synced 2 hours ago
❌ Tests: Failing

## 📊 Active Branches
Active: 2 / 2 allowed
  • feature/auth-enhancement (Issue: #42, Status: in_progress)
  • feature/import-fix (Issue: #17, Status: in_progress)

## 🔒 Blocked Files
  • components/auth/LoginForm.tsx (blocked by: feature/auth-enhancement)

## 📋 Branch Rules
• Max active branches: 2
• Require main sync: true
• Require tests before new: false
• Auto cleanup merged: true
• Prevent conflicts: true

## 💡 Recommendations
1. Fix failing tests before proceeding
2. You're at the branch limit - complete work before new features
```

## Integration:
- Called by `/sr` for context
- Used by `/fw start` for validation
- Part of daily workflow
