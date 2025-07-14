#!/bin/bash

# Git push script for v2.3.6
cd /Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate

# Check current status
echo "=== Current Git Status ==="
git status

# Add all changes
echo -e "\n=== Adding all changes ==="
git add .

# Show what will be committed
echo -e "\n=== Changes to be committed ==="
git status --short

# Commit with our message
echo -e "\n=== Committing changes ==="
git commit -F COMMIT_MESSAGE.txt

# Create tag
echo -e "\n=== Creating release tag ==="
git tag -a v2.3.6 -m "Release v2.3.6 - Async Event-Driven Architecture"

# Push to GitHub
echo -e "\n=== Pushing to GitHub ==="
git push origin main
git push origin v2.3.6

echo -e "\n=== Done! ==="
echo "View at: https://github.com/bearingfruitco/claude-code-boilerplate"
