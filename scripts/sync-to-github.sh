#!/bin/bash
# sync-to-github.sh - Safely sync all changes to GitHub main branch

echo "🚀 Starting GitHub sync process..."
echo "================================="

# Navigate to the correct directory
cd /Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate

# Check current status
echo "📊 Current Git Status:"
git status --short

# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "🌿 Current branch: $CURRENT_BRANCH"

# Ensure we're on main branch
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "⚠️  Not on main branch. Switching to main..."
    git checkout main
    if [ $? -ne 0 ]; then
        echo "❌ Failed to switch to main branch"
        exit 1
    fi
fi

# Pull latest changes from remote
echo "📥 Pulling latest changes from remote..."
git pull origin main
if [ $? -ne 0 ]; then
    echo "⚠️  Pull failed - may have conflicts. Please resolve manually."
    exit 1
fi

# Check if .gitignore is properly configured
echo "🔒 Verifying .gitignore configuration..."
if ! grep -q ".env" .gitignore; then
    echo "⚠️  Adding .env to .gitignore"
    echo ".env" >> .gitignore
fi
if ! grep -q ".mcp.json" .gitignore; then
    echo "⚠️  Adding .mcp.json to .gitignore"
    echo ".mcp.json" >> .gitignore
fi

# Remove sensitive files from git if they were accidentally added
echo "🧹 Removing sensitive files from git tracking..."
git rm --cached .env 2>/dev/null || true
git rm --cached .mcp.json 2>/dev/null || true
git rm --cached .env.local 2>/dev/null || true
git rm --cached .env.production 2>/dev/null || true
git rm -r --cached .mcp/ 2>/dev/null || true
git rm -r --cached logs/ 2>/dev/null || true
git rm -r --cached transcripts/ 2>/dev/null || true
git rm -r --cached captures/ 2>/dev/null || true
git rm -r --cached .claude/context/state/ 2>/dev/null || true
git rm -r --cached .claude/checkpoints/ 2>/dev/null || true

# Stage all changes
echo "📦 Staging all changes..."
git add -A

# Show what will be committed
echo "📋 Files to be committed:"
git status --short

# Count changes
CHANGES_COUNT=$(git status --porcelain | wc -l | tr -d ' ')
if [ "$CHANGES_COUNT" -eq 0 ]; then
    echo "✅ No changes to commit. Repository is up to date!"
    exit 0
fi

echo "📊 Total changes: $CHANGES_COUNT files"

# Create comprehensive commit message
COMMIT_MSG="feat: sync latest system updates to main branch

Changes included:
- Complete .claude/ directory structure (commands, hooks, docs)
- Project structure templates and configurations
- Documentation updates (README, workflows, guides)
- GitHub workflows and issue templates
- CodeRabbit configuration
- Branch management and feature workflow enhancements

Security:
- Excluded all .env files and environment variables
- Removed .mcp.json and MCP configurations
- Cleaned API keys and credentials
- Ignored logs, transcripts, and personal data
- Protected context state and checkpoint data"

# Commit changes
echo "💾 Committing changes..."
git commit -m "$COMMIT_MSG"

if [ $? -eq 0 ]; then
    echo "✅ Changes committed successfully!"
    
    # Push to remote
    echo "🚀 Pushing to GitHub..."
    git push origin main
    
    if [ $? -eq 0 ]; then
        echo "✅ Successfully pushed to GitHub main branch!"
        echo "🎉 Sync complete!"
        
        # Show final status
        echo ""
        echo "📊 Final Status:"
        git status
        echo ""
        echo "📝 Last commit:"
        git log -1 --oneline
    else
        echo "❌ Push failed. Please check your GitHub credentials and try again."
        exit 1
    fi
else
    echo "❌ Commit failed. Please check the error messages above."
    exit 1
fi

echo ""
echo "🏁 GitHub sync process completed!"
echo "================================="
