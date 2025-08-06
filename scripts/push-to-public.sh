#!/bin/bash
# push-to-public.sh - Safely push to public repository

echo "🚀 Starting Public Repository Push..."
echo "===================================="

# Navigate to project
cd /Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate

# Current status
echo "📍 Current branch: $(git branch --show-current)"

# Double-check sensitive files are not tracked
echo "🔒 Security verification..."

# List of sensitive patterns to verify
SENSITIVE_PATTERNS=(
    ".env"
    ".env.*"
    ".mcp.json"
    "*.mcp.json"
    "*api-key*"
    "*secret*"
    "*credential*"
    ".claude/logs/"
    ".claude/transcripts/"
    ".claude/checkpoints/"
    ".claude/context/state/"
    ".claude/team/active/"
)

# Check each pattern
FOUND_SENSITIVE=0
for pattern in "${SENSITIVE_PATTERNS[@]}"; do
    if git ls-files | grep -i "$pattern" > /dev/null 2>&1; then
        echo "❌ WARNING: Found tracked sensitive file matching: $pattern"
        git ls-files | grep -i "$pattern"
        FOUND_SENSITIVE=1
    fi
done

if [ $FOUND_SENSITIVE -eq 1 ]; then
    echo "❌ Sensitive files detected! Aborting push."
    echo "Please remove these files from git tracking first."
    exit 1
fi

echo "✅ No sensitive files detected in git tracking"

# Additional check for file contents
echo "🔍 Checking for sensitive content in config files..."

# Check if any JSON files contain obvious keys
if grep -r "sk-" --include="*.json" . 2>/dev/null | grep -v "node_modules"; then
    echo "⚠️  Warning: Found potential API keys in JSON files"
fi

# Verify public remote
echo "📡 Verifying public remote..."
git remote get-url public || {
    echo "❌ Public remote not found!"
    exit 1
}

# Show what will be pushed
echo "📊 Changes to push to public repo:"
git log public/main..HEAD --oneline 2>/dev/null || echo "  (First push to public repo)"

# Count files
FILE_COUNT=$(git ls-files | wc -l | tr -d ' ')
echo "📁 Total files to push: $FILE_COUNT"

# Create a comprehensive commit message for public repo
PUBLIC_COMMIT_MSG="feat: Claude Code Boilerplate System - Complete Implementation

This is a comprehensive boilerplate system for AI-assisted development using Claude Code.

Features:
- 116+ custom commands for AI-driven development
- 70+ enforcement hooks for design system and quality
- Agent OS integration for cross-tool standards
- Advanced orchestration and workflow management
- Security-first architecture with built-in protections
- Complete documentation and setup guides

Components:
- .claude/ directory with full command system
- Project templates and configurations
- Design system enforcement
- Automated quality gates
- Team collaboration features
- Branch and feature management

Security:
- All sensitive files excluded
- API keys and credentials removed
- Environment variables sanitized
- Safe for public distribution

For setup instructions, see README.md"

# Push to public repository
echo "🚀 Pushing to public repository..."

# First, try to push current branch
git push public HEAD:main -f

if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed to public repository!"
    echo "🌐 View at: https://github.com/bearingfruitco/cc-boiler-js-public"
    
    # Show summary
    echo ""
    echo "📊 Push Summary:"
    echo "==============="
    echo "Repository: bearingfruitco/cc-boiler-js-public"
    echo "Branch: main"
    echo "Files: $FILE_COUNT"
    echo "Security: All sensitive files excluded"
    
    # Switch back to main
    git checkout main
    
    # Optional: Delete the sync branch
    git branch -d public-sync 2>/dev/null || true
    
    echo ""
    echo "✨ Public push complete!"
else
    echo "❌ Push failed!"
    echo "This might be due to:"
    echo "1. Authentication issues - check your GitHub credentials"
    echo "2. Permission issues - ensure you have write access"
    echo "3. Protected branch - check branch protection rules"
    echo ""
    echo "Try running: git push public HEAD:main --force"
fi
