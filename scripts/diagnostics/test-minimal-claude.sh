#!/bin/bash

# Create a test directory with minimal Claude config
TEST_DIR="/tmp/claude-test-$$"
mkdir -p "$TEST_DIR/.claude"

# Create minimal settings.json
cat > "$TEST_DIR/.claude/settings.json" << 'EOF'
{
  "permissions": {
    "defaultMode": "default"
  }
}
EOF

echo "Created test directory: $TEST_DIR"
echo "Testing Claude Code with minimal config..."

cd "$TEST_DIR"
claude-code 2>&1 | head -20

echo ""
echo "If this works without the error, the issue is in your .claude directory"
echo "If this also fails, the issue is with Claude Code installation"
