#!/bin/bash

cd /Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate

echo "=== Adding fixes ==="
git add -A

echo "=== Committing ==="
git commit -m "fix: resolve TypeScript and build errors

- Rename .ts files containing JSX to .tsx
- Remove experimental PPR feature (requires canary)
- Remove reactCompiler (not stable yet)
- Move Sentry config out of main config object
- Fix file extensions for all component files"

echo "=== Pushing to GitHub ==="
git push origin main

echo "=== Done! ==="
