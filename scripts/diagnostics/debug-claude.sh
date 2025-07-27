#!/bin/bash

# Enable debug mode for Node.js
export NODE_OPTIONS="--trace-warnings"
export DEBUG="*"

echo "Running Claude Code in debug mode..."
echo "=================================="
echo ""

cd /Users/shawnsmith/dev/bfc/boilerplate

# Try to run Claude Code with maximum debugging
claude-code --verbose 2>&1 | tee claude-debug.log

echo ""
echo "Debug output saved to claude-debug.log"
echo "Look for lines containing 'Cannot assign to read only property' and the preceding lines"
