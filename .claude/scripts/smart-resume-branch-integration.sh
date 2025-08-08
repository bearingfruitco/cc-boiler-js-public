#!/bin/bash
# Enhanced smart-resume with integrated branch awareness
# This adds to the existing smart-resume command

# Add this section after the existing context restoration

# Branch Awareness Section (NEW)
echo -e "\n## 🌿 Branch & Feature Context"

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"

# Check if we have feature state
if [ -f ".claude/branch-state/feature-state.json" ] || [ -f ".claude/state/feature-awareness-cache.json" ]; then
  # Check which files we're working on
  MODIFIED_FILES=$(git diff --name-only HEAD 2>/dev/null | head -5)
  
  if [ ! -z "$MODIFIED_FILES" ]; then
    echo "Modified files:"
    echo "$MODIFIED_FILES" | sed 's/^/  • /'
    
    # Check if any are part of completed features
    for file in $MODIFIED_FILES; do
      # This would integrate with the Python hook logic
      if grep -q "$file" .claude/branch-state/feature-state.json 2>/dev/null; then
        echo "  ℹ️  $file is part of a completed feature"
      fi
    done
  fi
fi

# Show branch health inline
MAIN_AGE=$(git log -1 --format=%ar origin/main 2>/dev/null)
if [[ "$MAIN_AGE" == *"day"* ]] || [[ "$MAIN_AGE" == *"week"* ]]; then
  echo "⚠️  Main branch last updated: $MAIN_AGE"
  echo "   Consider: /sync-main"
fi

# Active branches count (if registry exists)
if [ -f ".claude/branch-state/branch-registry.json" ]; then
  ACTIVE_COUNT=$(jq '.active_branches | length' .claude/branch-state/branch-registry.json 2>/dev/null || echo "0")
  if [ "$ACTIVE_COUNT" -gt "1" ]; then
    echo "📊 Active branches: $ACTIVE_COUNT"
  fi
fi

# Integration with existing commands
echo -e "\n## 🔗 Integrated Commands"
echo "• /branch-status - Full branch details (if needed)"
echo "• /feature-status - Check feature state (if working on completed feature)"
echo "• Continue with your existing workflow..."
