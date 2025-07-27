#!/bin/bash

echo "Searching for potential problem files..."
echo "========================================"

cd /Users/shawnsmith/dev/bfc/boilerplate

# Check for any malformed JSON files that might be read by Claude Code
echo -e "\nChecking all JSON files for syntax errors:"
find . -name "*.json" -not -path "./node_modules/*" -not -path "./.git/*" -type f | while read -r file; do
    if ! python3 -m json.tool "$file" > /dev/null 2>&1; then
        echo "❌ Invalid JSON: $file"
        # Show the specific error
        python3 -c "import json; json.load(open('$file'))" 2>&1 | grep -v Traceback | head -2
    fi
done

# Check for files with potential string/array confusion
echo -e "\nChecking for string/array type mismatches:"
find . -name "*.json" -not -path "./node_modules/*" -not -path "./.git/*" -type f | while read -r file; do
    # Look for patterns where a string is used where an array might be expected
    if grep -E '"(matchers?|hooks?|commands?)":\s*"[^"]*"' "$file" > /dev/null 2>&1; then
        echo "⚠️  Potential issue in: $file"
        grep -n -E '"(matchers?|hooks?|commands?)":\s*"[^"]*"' "$file" | head -3
    fi
done

# Check specifically in .claude directory
echo -e "\nJSON files in .claude directory:"
ls -la .claude/*.json 2>/dev/null || echo "No JSON files found"
