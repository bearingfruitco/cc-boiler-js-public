#!/bin/bash

echo "🔍 Claude Code Configuration Diagnostic"
echo "======================================"
echo ""

# Check if .claude directory exists
if [ ! -d ".claude" ]; then
    echo "❌ No .claude directory found in current directory"
    exit 1
fi

echo "✅ Found .claude directory"
echo ""

# Check for aliases.json syntax
echo "📝 Checking aliases.json..."
if [ -f ".claude/aliases.json" ]; then
    if grep -q '"?: "help"' .claude/aliases.json; then
        echo "   ❌ Found syntax error in aliases.json (missing quote)"
    else
        echo "   ✅ aliases.json syntax is correct"
    fi
else
    echo "   ⚠️  No aliases.json found"
fi
echo ""

# Check for duplicate hook numbers
echo "🔍 Checking for duplicate hook numbers..."
for dir in pre-tool-use post-tool-use stop sub-agent-stop; do
    if [ -d ".claude/hooks/$dir" ]; then
        duplicates=$(ls .claude/hooks/$dir/ 2>/dev/null | grep -E '^[0-9]+' | cut -d'-' -f1 | sort | uniq -d)
        if [ -n "$duplicates" ]; then
            echo "   ❌ Found duplicate numbers in $dir: $duplicates"
        else
            echo "   ✅ No duplicates in $dir"
        fi
    fi
done
echo ""

# Check settings.json format
echo "⚙️  Checking settings.json format..."
if [ -f ".claude/settings.json" ]; then
    # Check for old format (kebab-case)
    if grep -q '"pre-tool-use":\|"post-tool-use":\|"sub-agent-stop":' .claude/settings.json; then
        echo "   ⚠️  Using old hook format (kebab-case)"
        echo "   📌 New format requires: PreToolUse, PostToolUse, Stop, SubagentStop"
    else
        echo "   ✅ Settings.json appears to use correct format"
    fi
    
    # Check for minimal config
    if ! grep -q '"hooks":' .claude/settings.json; then
        echo "   ✅ Using minimal configuration (no hooks)"
    fi
else
    echo "   ❌ No settings.json found"
fi
echo ""

# List all settings files
echo "📁 Settings files found:"
ls -la .claude/settings* 2>/dev/null || echo "   No settings files found"
echo ""

# Summary
echo "📊 Summary"
echo "=========="
echo ""
echo "Next steps:"
echo "1. Start Claude Code with: claude"
echo "2. Test basic commands: /help, /doctor, /status"
echo "3. If stable, you can swap settings.json with settings-with-hooks.json"
echo ""
echo "To enable hooks (after testing):"
echo "  mv .claude/settings.json .claude/settings-minimal.json"
echo "  mv .claude/settings-with-hooks.json .claude/settings.json"
echo ""
