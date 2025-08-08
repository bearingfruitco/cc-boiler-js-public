#!/bin/bash

# Pre-push checks before code goes to GitHub

echo "🔍 Running pre-push checks..."

# Run tests
echo "Running tests..."
if command -v npm &> /dev/null; then
  npm test 2>/dev/null || echo "⚠️  Some tests failed"
fi

# Check for console.log statements
CONSOLE_COUNT=$(grep -r "console\." --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" . 2>/dev/null | wc -l)
if [ "$CONSOLE_COUNT" -gt 0 ]; then
  echo "⚠️  Found $CONSOLE_COUNT console statements"
fi

# Check for TODO comments
TODO_COUNT=$(grep -r "TODO\|FIXME\|XXX" --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" . 2>/dev/null | wc -l)
if [ "$TODO_COUNT" -gt 0 ]; then
  echo "📝 Found $TODO_COUNT TODO/FIXME comments"
fi

# Check for sensitive files
if [ -f ".env" ] && ! grep -q "^.env$" .gitignore 2>/dev/null; then
  echo "⚠️  WARNING: .env file not in .gitignore!"
fi

echo "✅ Pre-push checks complete"

exit 0
