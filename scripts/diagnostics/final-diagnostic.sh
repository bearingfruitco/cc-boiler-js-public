#!/bin/bash

echo "Final diagnostic for Claude Code error"
echo "======================================"
echo ""

cd /Users/shawnsmith/dev/bfc/boilerplate

# 1. Show current .claude contents
echo "Current .claude directory contents:"
ls -la .claude/
echo ""

# 2. Validate each JSON file
echo "Validating JSON files:"
for file in .claude/*.json; do
    if [[ -f "$file" ]]; then
        echo -n "  $(basename "$file"): "
        if python3 -m json.tool "$file" > /dev/null 2>&1; then
            echo "✅ Valid"
        else
            echo "❌ Invalid"
            python3 -m json.tool "$file" 2>&1 | grep -v "Traceback" | head -3
        fi
    fi
done
echo ""

# 3. Check for files that might have wrong format
echo "Checking for potential format issues:"
echo ""

# Check settings.json specifically
if [[ -f ".claude/settings.json" ]]; then
    echo "settings.json content:"
    cat .claude/settings.json
    echo ""
fi

# 4. Try running Claude Code with debug info
echo "Running Claude Code with NODE_DEBUG:"
export NODE_DEBUG=*
claude-code --version 2>&1 | grep -C 5 "Cannot assign" || echo "No error captured in version check"

echo ""
echo "If the error persists, try:"
echo "1. rm -rf .claude && mkdir .claude && echo '{}' > .claude/settings.json"
echo "2. Reinstall Claude Code: npm uninstall -g @anthropic-ai/claude-code && npm install -g @anthropic-ai/claude-code"
