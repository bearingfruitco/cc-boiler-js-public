#!/bin/bash
# Test if hooks are actually executing

echo "🧪 Claude Code Hooks Live Test"
echo "=============================="
echo ""
echo "This will test if your hooks are actually running."
echo ""
echo "📝 Instructions:"
echo "1. Start Claude Code in this directory"
echo "2. Press Ctrl+R to enter transcript mode (to see hook execution)"
echo "3. Ask Claude to: 'read the README.md file'"
echo ""
echo "🔍 What to look for in transcript mode:"
echo "- You should see 'Running pre-tool-use hooks...' messages"
echo "- Hook names like '00-auto-approve-safe-ops.py' should appear"
echo "- The read operation might be auto-approved by your hooks"
echo ""
echo "📊 Expected hook execution for a Read operation:"
echo "- PreToolUse hooks will run (all ~35 of them)"
echo "- PostToolUse hooks will run after (all ~22 of them)"
echo ""
echo "Press Enter to see your hook configuration summary..."
read

# Show hook counts
echo ""
echo "📈 Your Active Hooks:"
grep -E '"PreToolUse"|"PostToolUse"|"Stop"|"SubagentStop"' .claude/settings.json | sort | uniq -c
