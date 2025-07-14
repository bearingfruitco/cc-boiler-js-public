#!/bin/bash

cd /Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate

echo "=== Running type check to see remaining errors ==="
pnpm typecheck 2>&1 | head -50

echo -e "\n=== Adding all fixes ==="
git add -A

echo -e "\n=== Status ==="
git status --short

echo -e "\n=== Committing fixes ==="
git commit -m "fix: resolve critical TypeScript errors for build

- Fix async/await issues in API routes and form handlers
- Add missing type definitions and window declarations
- Create placeholder store implementations
- Fix SWR import (default export)
- Add missing Analytics component
- Create API client module
- Fix Next.js 15 headers/cookies async requirements
- Add placeholder field registry imports
- Create missing mutation hooks
- Fix missing type exports

This resolves the most critical build errors. Some store implementations
and field registry setup still need proper implementation."

echo -e "\n=== Pushing to GitHub ==="
git push origin main

echo -e "\n=== Done! ==="
