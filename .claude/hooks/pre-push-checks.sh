#!/bin/bash

# Pre-push validation checks
echo "🔍 Running pre-push checks..."

# Check 1: Tests pass
echo "Running tests..."
if npm test > /dev/null 2>&1; then
    echo "✅ Tests pass"
else
    echo "❌ Tests failing. Fix before pushing."
    exit 1
fi

# Check 2: No console.log statements
if grep -r "console.log" --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" --exclude-dir=node_modules --exclude-dir=.next .; then
    echo "⚠️  Warning: console.log statements found"
fi

# Check 3: No TODO comments
if grep -r "TODO" --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" --exclude-dir=node_modules --exclude-dir=.next .; then
    echo "⚠️  Warning: TODO comments found"
fi

echo "✅ Pre-push checks complete"
