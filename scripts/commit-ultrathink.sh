#!/bin/bash

echo "🚀 Committing UltraThink Integration to GitHub"
echo "============================================"

# Check if we're in the right directory
if [ ! -d ".claude" ]; then
    echo "❌ Error: Not in the boilerplate directory"
    exit 1
fi

# Check git status
echo "📊 Current git status:"
git status --short

# Add all the new files
echo ""
echo "📝 Adding new files..."
git add .claude/commands/ultra-think.md
git add .claude/commands/visual-plan.md
git add .claude/hooks/pre-tool-use/18-auto-parallel-agents.py
git add docs/guides/ultrathink-integration-guide.md
git add .claude/aliases.json
git add .claude/settings-with-hooks.json
git add docs/SYSTEM_OVERVIEW.md
git add CLAUDE.md
git add ../NEW_CHAT_CONTEXT.md

# Show what will be committed
echo ""
echo "📋 Files to be committed:"
git status --short --cached

# Create commit message
echo ""
echo "💬 Creating commit..."
git commit -m "feat: Integrate Ray Fernando's UltraThink workflow

- Add /ultra-think (ut) command for 32k+ token deep thinking
- Add /visual-plan (vp) for screenshot-based planning
- Add auto-parallel agent detection hook
- Intelligent agent spawning based on task complexity
- Update documentation with new workflow
- Add aliases for quick access

This brings Ray Fernando's powerful parallel agent workflow into the boilerplate,
enabling automatic multi-agent analysis for complex tasks without manual orchestration."

# Show the result
echo ""
echo "✅ Commit created! Run 'git push' to send to GitHub"
echo ""
echo "📚 Documentation updated in:"
echo "  - CLAUDE.md (main instructions)"
echo "  - NEW_CHAT_CONTEXT.md (quick reference)"
echo "  - docs/guides/ultrathink-integration-guide.md (detailed guide)"
echo "  - docs/SYSTEM_OVERVIEW.md (system architecture)"
