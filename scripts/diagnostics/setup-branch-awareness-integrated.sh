#!/bin/bash
# Setup script for Integrated Branch Awareness System
# Non-disruptive, enhances existing Claude Code Boilerplate

echo "🚀 Setting up Integrated Branch Awareness..."
echo "This enhances your existing system without disrupting it."
echo ""

# 1. Create directories if needed
echo "📁 Ensuring directories exist..."
mkdir -p .claude/branch-state
mkdir -p .claude/state
mkdir -p .claude/metrics

# 2. Make hooks executable
echo "🔧 Setting up hooks..."
if [ -f .claude/hooks/pre-tool-use/20-feature-awareness.py ]; then
  chmod +x .claude/hooks/pre-tool-use/20-feature-awareness.py
  echo "✅ Feature awareness hook ready (non-blocking)"
else
  echo "⏭️  Feature awareness hook not found (optional)"
fi

if [ -f .claude/hooks/notification/branch-health.py ]; then
  chmod +x .claude/hooks/notification/branch-health.py
  echo "✅ Branch health notifications ready"
else
  echo "⏭️  Branch health notifications not found (optional)"
fi

# 3. Initialize feature state if desired
echo ""
read -p "Initialize feature tracking? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  if [ ! -f .claude/branch-state/feature-state.json ]; then
    cat > .claude/branch-state/feature-state.json << 'EOF'
{
  "last_updated": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "features": {},
  "mode": "info"
}
EOF
    echo "✅ Feature state initialized (info mode)"
  fi
fi

# 4. Show integration points
echo ""
echo "📋 Integration Summary:"
echo "========================"
echo ""
echo "✅ Enhanced Commands:"
echo "  • /sr - Now shows branch context when relevant"
echo "  • /branch-info - Lightweight branch status"
echo "  • /feature-status - Check feature state"
echo ""
echo "✅ Automatic Features:"
echo "  • Feature awareness when editing (info only)"
echo "  • Branch health tips (every 2 hours)"
echo "  • PRP enhancement (if using PRPs)"
echo ""
echo "✅ Event Integration:"
echo "  • Branch events fire to your event queue"
echo "  • Non-blocking, async tracking"
echo ""

# 5. Test the integration
echo "🧪 Testing integration..."
echo ""

# Test branch-info command
if [ -f .claude/commands/branch-info.md ]; then
  echo "✅ branch-info command available"
  
  # Show current branch info
  CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "none")
  echo "   Current branch: $CURRENT_BRANCH"
fi

# Check for modified files
MODIFIED=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
if [ "$MODIFIED" -gt "0" ]; then
  echo "   Modified files: $MODIFIED"
fi

echo ""
echo "✅ Setup Complete!"
echo ""
echo "🎯 Next Steps:"
echo "============="
echo "1. Continue using Claude Code normally"
echo "2. Notice helpful branch/feature info in /sr"
echo "3. Optional: Add features to track with /feature-status"
echo "4. Optional: Use branch-info in chains"
echo ""
echo "💡 Key Point: Everything is additive and non-blocking!"
echo "   - Your workflow remains unchanged"
echo "   - Information appears only when helpful"
echo "   - All features can be disabled if needed"
echo ""
echo "📖 Full docs: docs/branch-awareness-integration-guide.md"
