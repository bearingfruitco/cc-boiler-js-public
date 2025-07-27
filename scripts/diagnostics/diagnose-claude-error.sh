#!/bin/bash

echo "🔍 Claude Code Error Diagnostic"
echo "=============================="
echo ""

# Function to test Claude Code
test_claude() {
    local desc="$1"
    echo -n "Testing $desc... "
    
    # Capture both stdout and stderr
    output=$(cd /Users/shawnsmith/dev/bfc/boilerplate && claude-code --version 2>&1)
    
    if echo "$output" | grep -q "Cannot assign to read only property"; then
        echo "❌ ERROR FOUND"
        return 1
    else
        echo "✅ OK"
        return 0
    fi
}

# 1. Test with current setup
test_claude "current setup"

# 2. Test without settings.json
if [[ -f "/Users/shawnsmith/dev/bfc/boilerplate/.claude/settings.json" ]]; then
    mv "/Users/shawnsmith/dev/bfc/boilerplate/.claude/settings.json" "/Users/shawnsmith/dev/bfc/boilerplate/.claude/settings.json.diag_backup"
    test_claude "without settings.json"
    mv "/Users/shawnsmith/dev/bfc/boilerplate/.claude/settings.json.diag_backup" "/Users/shawnsmith/dev/bfc/boilerplate/.claude/settings.json"
fi

# 3. Test without entire .claude directory
if [[ -d "/Users/shawnsmith/dev/bfc/boilerplate/.claude" ]]; then
    mv "/Users/shawnsmith/dev/bfc/boilerplate/.claude" "/Users/shawnsmith/dev/bfc/boilerplate/.claude.diag_backup"
    test_claude "without .claude directory"
    mv "/Users/shawnsmith/dev/bfc/boilerplate/.claude.diag_backup" "/Users/shawnsmith/dev/bfc/boilerplate/.claude"
fi

# 4. Check Node.js and npm versions
echo ""
echo "Environment:"
echo "  Node.js: $(node --version 2>/dev/null || echo 'Not found')"
echo "  npm: $(npm --version 2>/dev/null || echo 'Not found')"
echo "  Claude Code location: $(which claude-code)"

# 5. Try to get more detailed error
echo ""
echo "Attempting to get detailed error..."
cd /Users/shawnsmith/dev/bfc/boilerplate
NODE_ENV=development claude-code --verbose 2>&1 | grep -C 5 "Cannot assign" || echo "Could not capture detailed error"
