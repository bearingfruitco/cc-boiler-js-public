#!/bin/bash
# Quick Fix for Claude Code and Biome Issues

echo "🔧 Quick Fix for Development Issues"
echo "==================================="
echo ""

# 1. Fix Biome
echo "1️⃣ Fixing Biome Configuration..."
if [ -f "biome.json.fixed" ]; then
    cp biome.json biome.json.backup.$(date +%Y%m%d_%H%M%S)
    cp biome.json.fixed biome.json
    echo "   ✅ Applied fixed biome.json"
    
    # Check if biome is installed
    if ! npx biome --version &>/dev/null; then
        echo "   📦 Installing Biome..."
        npm install --save-dev @biomejs/biome
    fi
else
    echo "   ❌ biome.json.fixed not found"
fi

echo ""
echo "2️⃣ Fixing Claude Code Installation..."

# Check current status
CLAUDE_VERSION=$(claude --version 2>&1)
if [ $? -eq 0 ]; then
    echo "   Current version: $CLAUDE_VERSION"
else
    echo "   ❌ Claude command not working"
fi

# Check for multiple installations
if [ -d "$HOME/.claude/local" ]; then
    echo "   ⚠️  Found local installation at ~/.claude/local"
    echo ""
    echo "   To fix Claude Code:"
    echo "   1. npm uninstall -g @claude-ai/cli"
    echo "   2. rm -rf ~/.claude/local"
    echo "   3. npm install -g @claude-ai/cli@latest"
    echo "   4. Restart terminal"
    echo "   5. Run: claude --doctor"
else
    echo "   ✅ No duplicate local installation found"
fi

echo ""
echo "3️⃣ Quick Actions:"
echo ""
echo "For Biome error in IDE:"
echo "  - Restart your IDE after the fix"
echo "  - Or run: npx biome check ."
echo ""
echo "For Claude Code:"
echo "  - If seeing multiple installations, run the commands above"
echo "  - The warning doesn't affect functionality"
echo ""
echo "✅ Quick fix complete!"
