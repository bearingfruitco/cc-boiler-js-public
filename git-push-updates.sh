#!/bin/bash

# Git commit and push script for Claude Code Boilerplate updates

cd "$(dirname "$0")/.."

echo "🔍 Checking Git status..."
echo ""

# Show current status
git status --short

echo ""
echo "📝 Creating commit..."

# Add all changes
git add .

# Create commit message
COMMIT_MSG="fix: resolve TypeScript errors for Next.js 15 compatibility

- Fix Drizzle ORM uuid generation (defaultRandom → sql gen_random_uuid)
- Create TypeScript module for field registry JSON imports
- Add missing Analytics component
- Add global type definitions for window and env
- Create system verification tests and scripts
- Update for Next.js 15 async headers/cookies

All v2.3.6 features intact:
- Event-driven architecture
- Design system enforcement (4-2-4 rule)
- PRD-driven development
- Multi-agent support
- Zero context loss"

# Commit
git commit -m "$COMMIT_MSG"

echo ""
echo "🚀 Pushing to GitHub..."

# Push to origin
git push origin main

echo ""
echo "✅ Done! Changes pushed to GitHub."
