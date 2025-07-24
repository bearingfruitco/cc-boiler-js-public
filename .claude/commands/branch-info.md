# Branch Info

Lightweight branch information integrated into existing workflow.

## Arguments:
- $1: --json (optional) - Output as JSON for chain integration

## Integration:
- Called by /sr automatically
- Used in chains for conditional logic
- Non-blocking, information only

## Steps:

```bash
FORMAT="${1:-text}"

# Gather basic info
CURRENT_BRANCH=$(git branch --show-current)
MODIFIED_COUNT=$(git status --porcelain 2>/dev/null | wc -l)

# Check main age
MAIN_AGE_HOURS=0
if command -v python3 >/dev/null; then
  MAIN_AGE_HOURS=$(python3 -c "
import subprocess
from datetime import datetime
try:
    result = subprocess.run(['git', 'log', '-1', '--format=%at', 'origin/main'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        timestamp = int(result.stdout.strip())
        age_hours = (datetime.now().timestamp() - timestamp) / 3600
        print(int(age_hours))
except:
    print(0)
")
fi

# Output based on format
if [ "$FORMAT" = "--json" ]; then
  # JSON for chain integration
  cat <<EOF
{
  "current_branch": "$CURRENT_BRANCH",
  "modified_files": $MODIFIED_COUNT,
  "main_age_hours": $MAIN_AGE_HOURS,
  "needs_sync": $([ $MAIN_AGE_HOURS -gt 24 ] && echo "true" || echo "false"),
  "has_changes": $([ $MODIFIED_COUNT -gt 0 ] && echo "true" || echo "false")
}
EOF
else
  # Human readable
  if [ $MAIN_AGE_HOURS -gt 48 ]; then
    echo "⚠️  Branch: $CURRENT_BRANCH (main is $MAIN_AGE_HOURS hours old)"
  else
    echo "✅ Branch: $CURRENT_BRANCH"
  fi
  
  if [ $MODIFIED_COUNT -gt 0 ]; then
    echo "📝 Modified: $MODIFIED_COUNT files"
  fi
fi
```

## Chain Integration Example:

```json
{
  "chains": {
    "morning-setup-enhanced": {
      "description": "Morning setup with branch awareness",
      "commands": [
        "smart-resume",
        "branch-info --json",
        "conditional:main_age_hours>48:sync-main"
      ]
    }
  }
}
```

## Usage Examples:

```bash
# Standalone
/branch-info
✅ Branch: feature/auth
📝 Modified: 3 files

# In chain (JSON)
/branch-info --json
{
  "current_branch": "feature/auth",
  "modified_files": 3,
  "main_age_hours": 72,
  "needs_sync": true,
  "has_changes": true
}
```

## Integration Points:
- Smart Resume shows this automatically
- Chains can use JSON for conditional logic
- Metrics track branch health
- No disruption to existing workflow
