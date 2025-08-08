#!/bin/bash

# Security scan for newly created files

FILE_PATH="$1"

# Check for sensitive data patterns
PATTERNS=(
  "password.*=.*['\"]"
  "api[_-]?key.*=.*['\"]"
  "secret.*=.*['\"]"
  "token.*=.*['\"]"
  "private[_-]?key"
)

FOUND_ISSUES=false

for pattern in "${PATTERNS[@]}"; do
  if grep -iE "$pattern" "$FILE_PATH" > /dev/null 2>&1; then
    echo "⚠️  SECURITY WARNING: Potential sensitive data found in $FILE_PATH"
    echo "   Pattern matched: $pattern"
    FOUND_ISSUES=true
  fi
done

# Check for hardcoded credentials
if grep -E "(localhost|127\.0\.0\.1):(3306|5432|6379|27017)" "$FILE_PATH" > /dev/null 2>&1; then
  echo "⚠️  WARNING: Hardcoded database connection found in $FILE_PATH"
  FOUND_ISSUES=true
fi

# Check for console.log in production code
if [[ "$FILE_PATH" != *"test"* ]] && [[ "$FILE_PATH" != *"spec"* ]]; then
  if grep -E "console\.(log|error|warn|debug)" "$FILE_PATH" > /dev/null 2>&1; then
    echo "📝 INFO: Console statements found in $FILE_PATH"
  fi
fi

if [ "$FOUND_ISSUES" = false ]; then
  echo "✅ Security scan passed for $FILE_PATH"
fi

exit 0
