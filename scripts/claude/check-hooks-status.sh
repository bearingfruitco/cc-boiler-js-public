#!/bin/bash
# Quick status check for Claude Code hooks

echo "🔍 Claude Code Hooks Status Check"
echo "================================="
echo ""

# Check if settings.json exists and is valid
if [ -f ".claude/settings.json" ]; then
    echo "✅ Settings file exists"
    
    # Count hooks
    echo ""
    echo "📊 Hook counts:"
    echo -n "  PreToolUse: "
    grep -o '"command":' .claude/settings.json | grep -B1 -A1 "PreToolUse" | wc -l | xargs
    
    # Check for error patterns
    if grep -q '"matcher": {}' .claude/settings.json; then
        echo "❌ Found problematic empty object matchers"
    else
        echo "✅ No empty object matchers found"
    fi
    
    if grep -q '"matcher": ""' .claude/settings.json; then
        echo "✅ Found correct empty string matchers"
    fi
else
    echo "❌ Settings file not found"
fi

echo ""
echo "🏥 Running claude doctor..."
echo "----------------------------"
claude doctor 2>&1 | head -20
