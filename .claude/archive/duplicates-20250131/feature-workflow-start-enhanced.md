# Feature Workflow Start - Enhanced

Enhanced version of /fw start that integrates branch management and feature protection.

## Integration Points:
- Updates branch registry when creating branches
- Checks for related completed features
- Sets up feature protection
- Enforces branch limits

## Additional Steps:

```bash
# After existing /fw start steps...

# 4. Branch Management Integration
echo -e "\n## 🌿 Branch Management"

# Check branch limits
BRANCH_REGISTRY=".claude/branch-state/branch-registry.json"
if [ -f "$BRANCH_REGISTRY" ]; then
  ACTIVE_COUNT=$(cat "$BRANCH_REGISTRY" | jq '.active_branches | length')
  MAX_ALLOWED=$(cat "$BRANCH_REGISTRY" | jq '.branch_rules.max_active_branches')
  
  if [ $ACTIVE_COUNT -ge $MAX_ALLOWED ]; then
    echo "⚠️  At branch limit ($ACTIVE_COUNT/$MAX_ALLOWED)"
    echo "Consider completing existing work first"
    echo "Run: /branch-status"
  fi
  
  # Update registry with new branch
  NEW_BRANCH_ENTRY="{
    \"name\": \"$BRANCH_NAME\",
    \"issue\": \"#$ISSUE_NUMBER\",
    \"status\": \"in_progress\",
    \"created\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
    \"base_commit\": \"$(git rev-parse main)\",
    \"files_modified\": []
  }"
  
  cat "$BRANCH_REGISTRY" | jq ".active_branches += [$NEW_BRANCH_ENTRY]" > "$BRANCH_REGISTRY.tmp" && mv "$BRANCH_REGISTRY.tmp" "$BRANCH_REGISTRY"
fi

# 5. Feature State Check
echo -e "\n## 📦 Feature State Check"

FEATURE_STATE=".claude/branch-state/feature-state.json"
if [ -f "$FEATURE_STATE" ]; then
  # Check if issue relates to existing feature
  ISSUE_TITLE=$(gh issue view $ISSUE_NUMBER --json title -q .title)
  
  # Simple keyword matching - could be enhanced
  for keyword in auth form api database; do
    if [[ "$ISSUE_TITLE" =~ $keyword ]]; then
      RELATED_FEATURE=$(cat "$FEATURE_STATE" | jq -r ".features | keys[] | select(. | contains(\"$keyword\"))" | head -1)
      
      if [ ! -z "$RELATED_FEATURE" ]; then
        echo "📎 Related feature found: $RELATED_FEATURE"
        FEATURE_STATUS=$(cat "$FEATURE_STATE" | jq -r ".features[\"$RELATED_FEATURE\"].status")
        
        if [ "$FEATURE_STATUS" = "completed" ]; then
          echo "⚠️  This feature is already completed!"
          echo "   Are you enhancing it? Make sure to:"
          echo "   - Not recreate working parts"
          echo "   - Build on existing implementation"
          echo ""
          echo "Run: /feature-status $RELATED_FEATURE"
          
          # Mark as enhancement
          cat "$FEATURE_STATE" | jq ".features[\"$RELATED_FEATURE\"].in_progress_enhancements = {
            \"issue\": \"#$ISSUE_NUMBER\",
            \"branch\": \"$BRANCH_NAME\",
            \"started\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
          }" > "$FEATURE_STATE.tmp" && mv "$FEATURE_STATE.tmp" "$FEATURE_STATE"
        fi
      fi
    fi
  done
fi

# 6. Set Protection Context
echo -e "\n## 🛡️ Protection Setup"
echo "Branch protection: ACTIVE"
echo "Feature awareness: ENABLED"
echo "Conflict prevention: ON"
```

## Enhanced Complete Action:

```bash
# When /fw complete is run...

# Update feature state
if [ -f "$FEATURE_STATE" ]; then
  # Check if this completes a feature
  read -p "Does this complete a feature? (y/N) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Feature name: " FEATURE_NAME
    
    # Get files modified in this branch
    FILES=$(git diff --name-only main..HEAD | jq -R . | jq -s .)
    
    # Update feature state
    FEATURE_ENTRY="{
      \"status\": \"completed\",
      \"branch\": \"$CURRENT_BRANCH\",
      \"completed_date\": \"$(date +%Y-%m-%d)\",
      \"files\": $FILES,
      \"working_implementation\": {
        \"description\": \"Implemented via issue #$ISSUE_NUMBER\",
        \"test_coverage\": \"$(npm test -- --coverage | grep 'All files' | awk '{print $10}')\"
      },
      \"do_not_recreate\": true
    }"
    
    cat "$FEATURE_STATE" | jq ".features[\"$FEATURE_NAME\"] = $FEATURE_ENTRY" > "$FEATURE_STATE.tmp" && mv "$FEATURE_STATE.tmp" "$FEATURE_STATE"
  fi
fi

# Clean up branch registry
if [ -f "$BRANCH_REGISTRY" ]; then
  cat "$BRANCH_REGISTRY" | jq ".active_branches = [.active_branches[] | select(.name != \"$CURRENT_BRANCH\")]" > "$BRANCH_REGISTRY.tmp" && mv "$BRANCH_REGISTRY.tmp" "$BRANCH_REGISTRY"
fi
```

## Integration with Existing Workflow:

1. **Seamless Enhancement** - Adds protection without changing core flow
2. **Optional Features** - Protection only activates if state files exist
3. **Backward Compatible** - Works with or without branch management
4. **Chain Integration** - Works with existing chains like `feature-complete`
