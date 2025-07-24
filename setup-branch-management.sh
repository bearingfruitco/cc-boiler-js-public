#!/bin/bash
# Setup script for Branch Management & Feature Protection System

echo "🚀 Setting up Branch Management & Feature Protection..."
echo ""

# 1. Create directories
echo "📁 Creating directories..."
mkdir -p .claude/branch-state

# 2. Make hooks executable
echo "🔧 Making hooks executable..."
chmod +x .claude/hooks/pre-tool-use/20-feature-state-guardian.py
chmod +x .claude/hooks/pre-tool-use/21-branch-controller.py

# 3. Initialize state files if they don't exist
echo "📝 Initializing state files..."

if [ ! -f .claude/branch-state/feature-state.json ]; then
  cat > .claude/branch-state/feature-state.json << 'EOF'
{
  "last_updated": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "features": {},
  "branches": {
    "main": {
      "last_merge": "$(date -u +%Y-%m-%d)",
      "stable_features": []
    }
  }
}
EOF
  echo "✅ Created feature-state.json"
else
  echo "⏭️  feature-state.json already exists"
fi

if [ ! -f .claude/branch-state/branch-registry.json ]; then
  # Get current branch
  CURRENT_BRANCH=$(git branch --show-current)
  CURRENT_COMMIT=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
  
  cat > .claude/branch-state/branch-registry.json << EOF
{
  "last_updated": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "main_branch": {
    "name": "main",
    "last_pulled": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "stable_commit": "$CURRENT_COMMIT",
    "protected": true
  },
  "active_branches": [],
  "branch_rules": {
    "max_active_branches": 2,
    "require_main_sync": true,
    "require_tests_before_new": false,
    "auto_cleanup_merged": true,
    "prevent_conflicting_branches": true,
    "sync_timeout_hours": 24
  },
  "blocked_files": {}
}
EOF
  echo "✅ Created branch-registry.json"
else
  echo "⏭️  branch-registry.json already exists"
fi

# 4. Test commands
echo ""
echo "🧪 Testing commands..."
echo ""

# Test branch-status
echo "Running /branch-status..."
if [ -f .claude/commands/branch-status.md ]; then
  echo "✅ branch-status command available"
else
  echo "❌ branch-status command not found"
fi

# Test feature-status
if [ -f .claude/commands/feature-status.md ]; then
  echo "✅ feature-status command available"
else
  echo "❌ feature-status command not found"
fi

# Test sync-main
if [ -f .claude/commands/sync-main.md ]; then
  echo "✅ sync-main command available"
else
  echo "❌ sync-main command not found"
fi

# 5. Show current state
echo ""
echo "📊 Current Branch State:"
echo "========================"
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"

# Count modified files
MODIFIED_COUNT=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
echo "Modified files: $MODIFIED_COUNT"

# Check if main needs sync
if [ "$CURRENT_BRANCH" != "main" ]; then
  BEHIND=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "0")
  if [ "$BEHIND" -gt "0" ]; then
    echo "⚠️  Main is $BEHIND commits behind origin"
  fi
fi

echo ""
echo "✅ Setup Complete!"
echo ""
echo "📚 Quick Start Guide:"
echo "===================="
echo "1. Check branch status:     /branch-status (or /bs)"
echo "2. Check feature status:    /feature-status [name] (or /fs)"
echo "3. Sync main branch:        /sync-main (or /sync)"
echo "4. Resume with awareness:   /sr"
echo ""
echo "🎯 Next Steps:"
echo "============="
echo "1. Add your completed features to .claude/branch-state/feature-state.json"
echo "2. Run /branch-status to see current state"
echo "3. Use /fw start [issue] to create protected branches"
echo ""
echo "📖 Documentation: docs/branch-management-integration.md"
