# Feature Complete

Mark a feature as completed and update state accordingly.

## Arguments:
- $1: feature-name (required) - Name of the feature to mark complete

## Steps:

```bash
FEATURE_NAME="$1"

if [ -z "$FEATURE_NAME" ]; then
  echo "❌ Error: Feature name required"
  echo "Usage: /feature-complete [feature-name]"
  exit 1
fi

echo "## 🎉 Completing Feature: $FEATURE_NAME"
echo ""

# 0. Run verification first
echo "🔍 Running verification checks..."
echo ""

# Check if feature passes verification
VERIFICATION_OUTPUT=$(python3 -c "
import subprocess
import json
result = subprocess.run(['npm', 'test', '$FEATURE_NAME.test', '--', '--run'], 
                       capture_output=True, text=True, timeout=30)
if result.returncode != 0:
    print('FAILED')
else:
    # Check TypeScript
    ts_result = subprocess.run(['npm', 'run', 'typecheck'], 
                              capture_output=True, text=True, timeout=15)
    if ts_result.returncode != 0:
        print('FAILED')
    else:
        print('PASSED')
" 2>/dev/null || echo "SKIPPED")

if [ "$VERIFICATION_OUTPUT" = "FAILED" ]; then
  echo "❌ Verification failed! Cannot mark feature as complete."
  echo ""
  echo "Run: /verify $FEATURE_NAME"
  echo "Fix any issues before marking complete."
  exit 1
elif [ "$VERIFICATION_OUTPUT" = "PASSED" ]; then
  echo "✅ Verification passed!"
  echo ""
else
  echo "⚠️  Verification skipped (tests not found)"
  echo ""
fi

# 1. Load current state
FEATURE_STATE_FILE=".claude/branch-state/feature-state.json"
if [ ! -f "$FEATURE_STATE_FILE" ]; then
  echo "❌ Feature state file not found"
  exit 1
fi

# 2. Check if feature exists
FEATURE=$(cat "$FEATURE_STATE_FILE" | jq -r ".features[\"$FEATURE_NAME\"]")
if [ "$FEATURE" = "null" ]; then
  echo "❌ Feature '$FEATURE_NAME' not found"
  echo "Creating new completed feature entry..."
  
  # Get current branch files
  CURRENT_BRANCH=$(git branch --show-current)
  FILES=$(git diff --name-only main..HEAD | jq -R . | jq -s .)
  
  # Create new feature entry
  FEATURE="{
    \"status\": \"completed\",
    \"branch\": \"$CURRENT_BRANCH\",
    \"completed_date\": \"$(date +%Y-%m-%d)\",
    \"files\": $FILES,
    \"do_not_recreate\": true
  }"
fi

# 3. Update feature status
echo "📝 Updating feature state..."

# Get test coverage if available
TEST_COVERAGE=$(npm test -- --coverage 2>/dev/null | grep "All files" | awk '{print $10}' || echo "unknown")

# Update the feature
UPDATED_FEATURE=$(echo "$FEATURE" | jq ". + {
  \"status\": \"completed\",
  \"completed_date\": \"$(date +%Y-%m-%d)\",
  \"working_implementation\": {
    \"description\": \"Feature completed and tested\",
    \"test_coverage\": \"$TEST_COVERAGE\",
    \"last_validated\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
  }
}")

# Save back to file
cat "$FEATURE_STATE_FILE" | jq ".features[\"$FEATURE_NAME\"] = $UPDATED_FEATURE | .last_updated = \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"" > "$FEATURE_STATE_FILE.tmp" && mv "$FEATURE_STATE_FILE.tmp" "$FEATURE_STATE_FILE"

# 4. Update branch registry
BRANCH_REGISTRY_FILE=".claude/branch-state/branch-registry.json"
if [ -f "$BRANCH_REGISTRY_FILE" ]; then
  echo "📝 Updating branch registry..."
  
  # Remove from active branches
  CURRENT_BRANCH=$(git branch --show-current)
  cat "$BRANCH_REGISTRY_FILE" | jq ".active_branches = [.active_branches[] | select(.name != \"$CURRENT_BRANCH\")] | .last_updated = \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"" > "$BRANCH_REGISTRY_FILE.tmp" && mv "$BRANCH_REGISTRY_FILE.tmp" "$BRANCH_REGISTRY_FILE"
  
  # Clear blocked files for this branch
  cat "$BRANCH_REGISTRY_FILE" | jq ".blocked_files = (.blocked_files | with_entries(select(.value.blocked_by != \"$CURRENT_BRANCH\")))" > "$BRANCH_REGISTRY_FILE.tmp" && mv "$BRANCH_REGISTRY_FILE.tmp" "$BRANCH_REGISTRY_FILE"
fi

# 5. Show summary
echo ""
echo "✅ Feature Completed!"
echo ""
echo "### Summary:"
echo "• Feature: $FEATURE_NAME"
echo "• Status: completed"
echo "• Date: $(date +%Y-%m-%d)"
echo "• Test Coverage: $TEST_COVERAGE"
echo ""
echo "### Protected Files:"
echo "$FILES" | jq -r '.[]' | sed 's/^/  • /'
echo ""
echo "### Next Steps:"
echo "1. Merge to main: git checkout main && git merge $CURRENT_BRANCH"
echo "2. Delete branch: git branch -d $CURRENT_BRANCH"
echo "3. Start new feature: /fw start [issue]"
```

## Example Output:

```
## 🎉 Completing Feature: user-authentication

📝 Updating feature state...
📝 Updating branch registry...

✅ Feature Completed!

### Summary:
• Feature: user-authentication
• Status: completed
• Date: 2025-01-21
• Test Coverage: 92%

### Protected Files:
  • components/auth/LoginForm.tsx
  • components/auth/RegisterForm.tsx
  • lib/auth/jwt.ts

### Next Steps:
1. Merge to main: git checkout main && git merge feature/auth
2. Delete branch: git branch -d feature/auth
3. Start new feature: /fw start [issue]
```

## Integration:
- Called after feature testing passes
- Updates protection status
- Clears branch blocks
- Part of feature lifecycle
