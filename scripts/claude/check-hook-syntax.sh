#!/bin/bash

echo "Checking Python syntax in all hook files..."
echo "========================================="

cd /Users/shawnsmith/dev/bfc/boilerplate/.claude/hooks

# Check each Python file for syntax errors
find . -name "*.py" -type f | while read -r file; do
    if python3 -m py_compile "$file" 2>/dev/null; then
        echo "✅ $file"
    else
        echo "❌ $file - SYNTAX ERROR:"
        python3 -m py_compile "$file" 2>&1 | grep -v "Traceback" | head -3
    fi
done

# Also check for files with incorrect line endings or encoding
echo -e "\nChecking for file encoding issues..."
find . -name "*.py" -type f | while read -r file; do
    if file "$file" | grep -q "CRLF"; then
        echo "⚠️  $file has Windows line endings (CRLF)"
    fi
    if ! file "$file" | grep -q "ASCII\|UTF-8"; then
        echo "⚠️  $file has unusual encoding"
    fi
done
