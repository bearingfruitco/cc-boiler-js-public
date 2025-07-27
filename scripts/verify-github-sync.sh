#!/bin/bash
# verify-github-sync.sh - Verify the GitHub sync was successful

echo "🔍 Verifying GitHub Sync..."
echo "=========================="

cd /Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate

# Check current branch
echo "📍 Current branch:"
git branch --show-current

# Check sync status with remote
echo -e "\n📊 Sync status with remote:"
git fetch origin
git status -sb

# Check for uncommitted changes
UNCOMMITTED=$(git status --porcelain | wc -l | tr -d ' ')
echo -e "\n📁 Uncommitted files: $UNCOMMITTED"

if [ "$UNCOMMITTED" -gt 0 ]; then
    echo "⚠️  There are still uncommitted changes:"
    git status --short
else
    echo "✅ All changes committed!"
fi

# Show recent commits
echo -e "\n📝 Recent commits:"
git log --oneline -5

# Check what's on remote
echo -e "\n🌐 Remote repository info:"
git remote -v

# Verify sensitive files are not tracked
echo -e "\n🔒 Security check - Ensuring sensitive files are not tracked:"
SENSITIVE_FILES=".env .mcp.json .env.local .env.production"
for file in $SENSITIVE_FILES; do
    if git ls-files --error-unmatch "$file" 2>/dev/null; then
        echo "❌ WARNING: $file is tracked in git!"
    else
        echo "✅ $file is not tracked (good)"
    fi
done

# Check .claude directory structure
echo -e "\n📂 Verifying .claude directory structure:"
if [ -d ".claude" ]; then
    echo "✅ .claude directory exists"
    echo "   Commands: $(find .claude/commands -name "*.md" 2>/dev/null | wc -l | tr -d ' ')"
    echo "   Hooks: $(find .claude/hooks -name "*.py" 2>/dev/null | wc -l | tr -d ' ')"
    echo "   Docs: $(find .claude/docs -name "*.md" 2>/dev/null | wc -l | tr -d ' ')"
else
    echo "❌ .claude directory not found!"
fi

# Final summary
echo -e "\n📊 Summary:"
echo "=========================="

# Check if we're up to date with remote
AHEAD=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo "0")
BEHIND=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "0")

if [ "$AHEAD" -eq 0 ] && [ "$BEHIND" -eq 0 ]; then
    echo "✅ Local main is in sync with origin/main"
elif [ "$AHEAD" -gt 0 ]; then
    echo "⚠️  Local main is $AHEAD commits ahead of origin/main"
    echo "   Run: git push origin main"
elif [ "$BEHIND" -gt 0 ]; then
    echo "⚠️  Local main is $BEHIND commits behind origin/main"
    echo "   Run: git pull origin main"
fi

echo -e "\n✨ Verification complete!"
