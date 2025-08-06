#!/bin/bash

echo "Checking for hooks with incorrect exit codes..."
echo ""

# Check PostToolUse hooks that exit with 1 instead of 0 for success
echo "=== PostToolUse hooks with sys.exit(1) outside except blocks ==="
for file in /Users/shawnsmith/dev/bfc/boilerplate/.claude/hooks/post-tool-use/*.py; do
    if [ -f "$file" ]; then
        # Check if file has sys.exit(1) not in an except block
        if grep -q "sys\.exit(1)" "$file"; then
            # Check if it's not just in except blocks
            content=$(cat "$file")
            if echo "$content" | grep -v "except" | grep -q "sys\.exit(1)"; then
                echo "  $(basename "$file")"
            fi
        fi
    fi
done

echo ""
echo "=== Hooks missing sys.exit(0) for success ==="
for file in /Users/shawnsmith/dev/bfc/boilerplate/.claude/hooks/**/*.py; do
    if [ -f "$file" ]; then
        if ! grep -q "sys\.exit(0)" "$file" 2>/dev/null; then
            # Check if it has a main function
            if grep -q "def main" "$file" 2>/dev/null; then
                echo "  $(basename "$file") - $(dirname "$file" | xargs basename)"
            fi
        fi
    fi
done

echo ""
echo "=== Checking for deprecated patterns ==="
echo "Files with 'tool_use' references:"
grep -l "tool_use" /Users/shawnsmith/dev/bfc/boilerplate/.claude/hooks/**/*.py 2>/dev/null | xargs -I {} basename {}

echo ""
echo "Files with '.get('path')' for file operations:"
grep -l "\.get('path'" /Users/shawnsmith/dev/bfc/boilerplate/.claude/hooks/**/*.py 2>/dev/null | xargs -I {} basename {}

echo ""
echo "Files with 'params' or 'parameters':"
grep -l "params\|parameters" /Users/shawnsmith/dev/bfc/boilerplate/.claude/hooks/**/*.py 2>/dev/null | xargs -I {} basename {}
