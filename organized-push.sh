#!/bin/bash
# Organized commit strategy for claude-code-boilerplate updates

cd /Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate

echo "🚀 Organized GitHub Update Process"
echo "=================================="
echo ""

# Function to create a commit
make_commit() {
    local message="$1"
    if [[ $(git status --porcelain | grep -E "^(M|A)" | wc -l) -gt 0 ]]; then
        git commit -m "$message"
        echo "✅ Committed: $message"
    else
        echo "⏭️  Nothing to commit for: $message"
    fi
}

# 1. First commit: Core documentation updates
echo "📚 Commit 1: Core Documentation"
git add MASTER_WORKFLOW_GUIDE.md
git add TDD_QUICK_REFERENCE.md
git add README.md
git add docs/claude/NEW_CHAT_CONTEXT.md
git add docs/setup/DAY_1_COMPLETE_GUIDE.md
git add docs/workflow/DAILY_WORKFLOW.md
git add .claude/QUICK_REFERENCE.md
make_commit "docs: Add Master Workflow Guide and update core documentation

- Added comprehensive MASTER_WORKFLOW_GUIDE.md
- Added TDD_QUICK_REFERENCE.md  
- Updated README to reference master guide
- Updated all key docs to point to master guide
- Enhanced daily workflow documentation"

# 2. Second commit: PRP and command updates
echo ""
echo "📝 Commit 2: PRP System and Commands"
git add .claude/commands/prd-to-prp.md
git add .claude/commands/prp-*.md
git add .claude/commands/tdd-*.md
git add .claude/commands/create-prp.md
git add PRPs/
git add .claude/aliases.json
make_commit "feat: Add PRP commands and TDD workflow enhancements

- Added PRP command suite (create-prp, prp-execute, etc.)
- Enhanced TDD workflow commands
- Added prd-to-prp conversion command
- Updated command aliases for better discovery"

# 3. Third commit: Hook updates
echo ""
echo "🪝 Commit 3: Hook System Updates"
git add .claude/hooks/pre-tool-use/*.py
git add .claude/hooks/post-tool-use/*.py
git add .claude/hooks/notification/*.py
git add .claude/hooks/*.json
git add .claude/hooks/config.json
make_commit "feat: Update hooks for TDD enforcement and PRP validation

- Enhanced TDD enforcer hook
- Added test auto-runner
- Updated PRP validator
- Improved dependency tracking
- Enhanced response capture for issues"

# 4. Fourth commit: Project files and scripts
echo ""
echo "🔧 Commit 4: Project Updates"
git add .claude/dependencies/manifest.json
git add *.sh
git add package.json
git add biome.json
git add drizzle.config.ts
make_commit "chore: Update project configuration and scripts

- Updated dependencies manifest
- Added git helper scripts
- Updated build configuration
- Enhanced project scripts"

# 5. Fifth commit: Everything else
echo ""
echo "🎯 Commit 5: Remaining Updates"
git add -A
make_commit "chore: Add remaining updates and improvements

- Updated component examples
- Enhanced test configurations
- Improved error handling
- General code quality improvements"

# Push all commits
echo ""
echo "🔄 Pushing all commits to GitHub..."
git push origin main

echo ""
echo "✅ All updates pushed successfully!"
echo ""
echo "📊 Final Summary:"
git log --oneline -5
echo ""
echo "🌐 View on GitHub: https://github.com/bearingfruitco/claude-code-boilerplate"
