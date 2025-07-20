#!/bin/bash
cd /Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate

echo "=== Git Status Summary ==="
echo ""
echo "Current branch:"
git branch --show-current
echo ""
echo "Remote URL:"
git remote -v | head -1
echo ""
echo "Number of modified files:"
git status --porcelain | grep "^ M" | wc -l
echo ""
echo "Number of untracked files:"
git status --porcelain | grep "^??" | wc -l
echo ""
echo "Number of new files:"
git status --porcelain | grep "^A" | wc -l
echo ""
echo "First 20 changes:"
git status --porcelain | head -20
