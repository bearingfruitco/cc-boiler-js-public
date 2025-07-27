#!/bin/bash
set -e
# Test if Claude Code accepts the hook configuration

echo "Testing Claude Code hook configuration..."
echo "Current settings.json:"
cat .claude/settings.json
echo ""
echo "Running /doctor command to check for errors..."

# Navigate to the project directory and run doctor command
cd /Users/shawnsmith/dev/bfc/boilerplate
claude doctor 2>&1 | tee claude-doctor-output.txt

echo ""
echo "Check claude-doctor-output.txt for results"
