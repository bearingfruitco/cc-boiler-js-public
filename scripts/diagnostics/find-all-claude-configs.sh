#!/bin/bash

echo "Searching for all .claude directories that might affect this project..."
echo "================================================"

# Check current directory
echo "Current directory (.claude):"
ls -la /Users/shawnsmith/dev/bfc/boilerplate/.claude/settings* 2>/dev/null || echo "  No settings files found"

# Check parent directories
echo -e "\nParent directories:"
current="/Users/shawnsmith/dev/bfc/boilerplate"
while [[ "$current" != "/" ]]; do
    parent=$(dirname "$current")
    if [[ -d "$parent/.claude" ]]; then
        echo "  Found .claude in: $parent"
        ls -la "$parent/.claude/settings*" 2>/dev/null
    fi
    current="$parent"
done

# Check home directory
echo -e "\nHome directory:"
if [[ -d "$HOME/.claude" ]]; then
    echo "  Found .claude in: $HOME"
    ls -la "$HOME/.claude/settings*" 2>/dev/null
else
    echo "  No .claude directory in home"
fi

# Check for global Claude config
echo -e "\nGlobal Claude config locations:"
for loc in "$HOME/.config/claude" "$HOME/.config/claude-code" "/etc/claude" "/usr/local/etc/claude"; do
    if [[ -d "$loc" ]]; then
        echo "  Found: $loc"
        ls -la "$loc" 2>/dev/null
    fi
done

echo -e "\nClaude Code version:"
claude-code --version 2>/dev/null || echo "  Could not get version"
