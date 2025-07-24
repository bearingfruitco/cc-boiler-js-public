# Branch Clean

Clean up merged branches and update registries.

## Arguments:
- $1: --dry-run (optional) - Show what would be cleaned without doing it

## Steps:

```bash
DRY_RUN="$1"

echo "## 🧹 Branch Cleanup"
echo ""

if [ "$DRY_RUN" = "--dry-run" ]; then
  echo "🔍 DRY RUN MODE - No changes will be made"
  echo ""
fi

# 1. Get list of merged branches
echo "### Checking for merged branches..."
MERGED_BRANCHES=$(git branch --merged main | grep -v "main" | grep -v "master" | grep -v "*")

if [ -z "$MERGED_BRANCHES" ]; then
  echo "✅ No merged branches to clean up"
else
  echo "Found merged branches:"
  echo "$MERGED_BRANCHES" | sed 's/^/  • /'
  echo ""
  
  if [ "$DRY_RUN" != "--dry-run" ]; then
    echo "🗑️  Deleting merged branches..."
    echo "$MERGED_BRANCHES" | xargs -n 1 git branch -d
  fi
fi

# 2. Check for stale branches
echo ""
echo "### Checking for stale branches..."
STALE_DAYS=14
CURRENT_DATE=$(date +%s)

git for-each-ref --format='%(refname:short) %(committerdate:unix)' refs/heads/ | while read branch last_commit; do
  if [ "$branch" != "main" ] && [ "$branch" != "master" ]; then
    AGE_DAYS=$(( ($CURRENT_DATE - $last_commit) / 86400 ))
    if [ $AGE_DAYS -gt $STALE_DAYS ]; then
      echo "⚠️  Stale branch: $branch (${AGE_DAYS} days old)"
      
      if [ "$DRY_RUN" != "--dry-run" ]; then
        read -p "Delete $branch? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
          git branch -D "$branch"
          echo "  ✅ Deleted $branch"
        fi
      fi
    fi
  fi
done

# 3. Clean up branch registry
echo ""
echo "### Cleaning branch registry..."

BRANCH_REGISTRY=".claude/branch-state/branch-registry.json"
if [ -f "$BRANCH_REGISTRY" ]; then
  # Get current branches
  CURRENT_BRANCHES=$(git branch --format='%(refname:short)' | jq -R . | jq -s .)
  
  if [ "$DRY_RUN" = "--dry-run" ]; then
    # Show what would be removed
    REGISTRY_BRANCHES=$(cat "$BRANCH_REGISTRY" | jq -r '.active_branches[].name')
    for branch in $REGISTRY_BRANCHES; do
      if ! echo "$CURRENT_BRANCHES" | jq -e ". | index(\"$branch\")" > /dev/null; then
        echo "Would remove from registry: $branch"
      fi
    done
  else
    # Actually clean the registry
    TEMP_FILE="$BRANCH_REGISTRY.tmp"
    cat "$BRANCH_REGISTRY" | jq "
      .active_branches = [.active_branches[] | select(.name as \$name | $CURRENT_BRANCHES | index(\$name))] |
      .last_updated = \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
    " > "$TEMP_FILE" && mv "$TEMP_FILE" "$BRANCH_REGISTRY"
    
    echo "✅ Registry cleaned"
  fi
fi

# 4. Clean up blocked files for deleted branches
if [ "$DRY_RUN" != "--dry-run" ] && [ -f "$BRANCH_REGISTRY" ]; then
  echo ""
  echo "### Cleaning blocked files..."
  
  TEMP_FILE="$BRANCH_REGISTRY.tmp"
  cat "$BRANCH_REGISTRY" | jq "
    .blocked_files = (.blocked_files | with_entries(
      select(.value.blocked_by as \$branch | $CURRENT_BRANCHES | index(\$branch))
    ))
  " > "$TEMP_FILE" && mv "$TEMP_FILE" "$BRANCH_REGISTRY"
  
  echo "✅ Blocked files cleaned"
fi

# 5. Summary
echo ""
echo "### 📊 Cleanup Summary"

if [ "$DRY_RUN" = "--dry-run" ]; then
  echo "• Mode: Dry run (no changes made)"
else
  echo "• Mode: Changes applied"
fi

# Count active branches
if [ -f "$BRANCH_REGISTRY" ]; then
  ACTIVE_COUNT=$(cat "$BRANCH_REGISTRY" | jq -r '.active_branches | length')
  MAX_ALLOWED=$(cat "$BRANCH_REGISTRY" | jq -r '.branch_rules.max_active_branches')
  echo "• Active branches: $ACTIVE_COUNT / $MAX_ALLOWED"
fi

# Show current branch
CURRENT=$(git branch --show-current)
echo "• Current branch: $CURRENT"

echo ""
echo "💡 Next: /branch-status to see current state"
```

## Example Output:

```
## 🧹 Branch Cleanup

### Checking for merged branches...
Found merged branches:
  • feature/old-auth
  • feature/deprecated-api

🗑️  Deleting merged branches...
Deleted branch feature/old-auth (was abc123).
Deleted branch feature/deprecated-api (was def456).

### Checking for stale branches...
⚠️  Stale branch: feature/abandoned-work (21 days old)
Delete feature/abandoned-work? (y/N) y
  ✅ Deleted feature/abandoned-work

### Cleaning branch registry...
✅ Registry cleaned

### Cleaning blocked files...
✅ Blocked files cleaned

### 📊 Cleanup Summary
• Mode: Changes applied
• Active branches: 1 / 2
• Current branch: main

💡 Next: /branch-status to see current state
```

## Integration:
- Run periodically to maintain hygiene
- Safe with --dry-run option
- Updates all registries
- Part of maintenance workflow
