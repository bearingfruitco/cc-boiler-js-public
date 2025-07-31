# Feature Status

Check the status and details of a specific feature.

## Arguments:
- $1: feature-name (required) - Name of the feature to check

## Steps:

```bash
FEATURE_NAME="$1"

if [ -z "$FEATURE_NAME" ]; then
  echo "❌ Error: Feature name required"
  echo "Usage: /feature-status [feature-name]"
  echo ""
  echo "Available features:"
  cat .claude/branch-state/feature-state.json | jq -r '.features | keys[]' 2>/dev/null
  exit 1
fi

# Load feature state
FEATURE_STATE=$(cat .claude/branch-state/feature-state.json 2>/dev/null || echo '{}')

# Get feature info
FEATURE=$(echo "$FEATURE_STATE" | jq -r ".features[\"$FEATURE_NAME\"]")

if [ "$FEATURE" = "null" ]; then
  echo "❌ Feature '$FEATURE_NAME' not found"
  echo ""
  echo "Available features:"
  echo "$FEATURE_STATE" | jq -r '.features | keys[] | "  • " + .'
  exit 1
fi

# Display feature information
echo "## 📦 Feature: $FEATURE_NAME"
echo ""

# Basic info
STATUS=$(echo "$FEATURE" | jq -r '.status')
BRANCH=$(echo "$FEATURE" | jq -r '.branch')
COMPLETED=$(echo "$FEATURE" | jq -r '.completed_date // "N/A"')

echo "### 📊 Status"
echo "• Status: $STATUS"
echo "• Branch: $BRANCH"
if [ "$STATUS" = "completed" ]; then
  echo "• Completed: $COMPLETED"
fi

# Working implementation
echo -e "\n### 🔧 Working Implementation"
IMPL=$(echo "$FEATURE" | jq -r '.working_implementation')
if [ "$IMPL" != "null" ]; then
  echo "• Description: $(echo "$IMPL" | jq -r '.description')"
  echo "• Test Coverage: $(echo "$IMPL" | jq -r '.test_coverage // "Unknown"')"
  echo "• Key Functions:"
  echo "$IMPL" | jq -r '.key_functions[]? | "  - " + .'
fi

# Files
echo -e "\n### 📁 Files"
echo "$FEATURE" | jq -r '.files[]? | "• " + .'

# In-progress enhancements
ENHANCEMENT=$(echo "$FEATURE" | jq -r '.in_progress_enhancements')
if [ "$ENHANCEMENT" != "null" ]; then
  echo -e "\n### 🚧 In-Progress Enhancement"
  echo "• Issue: $(echo "$ENHANCEMENT" | jq -r '.issue')"
  echo "• Branch: $(echo "$ENHANCEMENT" | jq -r '.branch')"
  echo "• Adding: $(echo "$ENHANCEMENT" | jq -r '.adding // "Unknown"')"
fi

# Protection status
DO_NOT_RECREATE=$(echo "$FEATURE" | jq -r '.do_not_recreate // false')
if [ "$DO_NOT_RECREATE" = "true" ]; then
  echo -e "\n### 🛡️ Protection"
  echo "⚠️  This feature is protected from recreation"
  echo "• Modifications must be done through proper enhancement branches"
fi

# Current branch check
CURRENT_BRANCH=$(git branch --show-current)
echo -e "\n### 🌿 Branch Check"
echo "• Current branch: $CURRENT_BRANCH"

if [ "$STATUS" = "completed" ] && [ "$CURRENT_BRANCH" != "$BRANCH" ]; then
  if [ "$ENHANCEMENT" != "null" ]; then
    ENHANCEMENT_BRANCH=$(echo "$ENHANCEMENT" | jq -r '.branch')
    if [ "$CURRENT_BRANCH" = "$ENHANCEMENT_BRANCH" ]; then
      echo "✅ You're on the enhancement branch"
    else
      echo "⚠️  Wrong branch for enhancement!"
      echo "  Switch to: git checkout $ENHANCEMENT_BRANCH"
    fi
  else
    echo "⚠️  Feature is on branch: $BRANCH"
    echo "  You may need to switch branches or pull latest"
  fi
fi

# Recommendations
echo -e "\n### 💡 Recommendations"

if [ "$STATUS" = "completed" ]; then
  echo "• To enhance: Create issue and use /fw start [issue]"
  echo "• To view: git checkout $BRANCH && git pull"
else
  echo "• Continue work on branch: $BRANCH"
fi
```

## Example Output:

```
## 📦 Feature: user-authentication

### 📊 Status
• Status: completed
• Branch: main
• Completed: 2025-01-15

### 🔧 Working Implementation
• Description: JWT-based authentication with Supabase
• Test Coverage: 92%
• Key Functions:
  - login
  - logout
  - validateToken
  - refreshToken

### 📁 Files
• components/auth/LoginForm.tsx
• components/auth/RegisterForm.tsx
• lib/auth/jwt.ts

### 🚧 In-Progress Enhancement
• Issue: #42
• Branch: feature/auth-mfa
• Adding: Multi-factor authentication support

### 🛡️ Protection
⚠️  This feature is protected from recreation
• Modifications must be done through proper enhancement branches

### 🌿 Branch Check
• Current branch: main
✅ Feature is on this branch

### 💡 Recommendations
• To enhance: Create issue and use /fw start [issue]
• Enhancement in progress on: feature/auth-mfa
```

## Integration:
- Referenced by protection warnings
- Used before starting work
- Part of feature workflow
