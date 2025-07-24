#!/bin/bash
# Initialize Task Ledger for existing projects

echo "🚀 Initializing Task Ledger System..."

# Check if task ledger already exists
if [ -f ".task-ledger.md" ]; then
    echo "⚠️  Task ledger already exists. Use '/tl sync' to update it."
    exit 0
fi

# Create initial task ledger
cat > .task-ledger.md << EOF
# Task Ledger - $(basename "$PWD")

> Single source of truth for all project tasks. Auto-updated by Claude Code hooks.

**Last Updated**: $(date "+%Y-%m-%d %H:%M:%S")

## Summary
- **Total Features**: 0
- **Active Tasks**: 0
- **Completed**: 0
- **In Progress**: 0

---

## Features

EOF

echo "✅ Task ledger created: .task-ledger.md"

# Check for existing task files and offer to sync
TASK_FILES=$(find docs/project/features -name "*-tasks.md" 2>/dev/null | wc -l)
if [ $TASK_FILES -gt 0 ]; then
    echo ""
    echo "📁 Found $TASK_FILES existing task files."
    echo "Run '/tl sync' to import them into the ledger."
fi

echo ""
echo "🎯 Next steps:"
echo "  1. The task ledger will auto-update as you work"
echo "  2. View it anytime with '/tl'"
echo "  3. See summary in '/sr' (smart resume)"
echo ""
echo "Happy task tracking! 🎉"
