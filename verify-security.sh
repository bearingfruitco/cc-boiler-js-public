#!/bin/bash

# Security Verification Script
# Run this before making the repository public

echo "🔒 Security Verification for Public Release"
echo "=========================================="

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env.local is tracked
echo -n "Checking if .env.local is in git... "
if git ls-files .env.local --error-unmatch 2>/dev/null; then
    echo -e "${RED}FAIL${NC} - .env.local is tracked in git!"
    echo "Run: git rm --cached .env.local"
    exit 1
else
    echo -e "${GREEN}PASS${NC}"
fi

# Search for common secret patterns
echo -n "Searching for API keys... "
if grep -r "\bsk_[a-zA-Z0-9]\|\bpk_[a-zA-Z0-9]\|api_key.*=.*['\"][a-zA-Z0-9]" . --exclude-dir=node_modules --exclude-dir=.git --exclude="*.md" --exclude=".env.example" --exclude=".mcp.json" 2>/dev/null | grep -v "YOUR_\|your-\|placeholder"; then
    echo -e "${RED}FAIL${NC} - Found potential secrets!"
    exit 1
else
    echo -e "${GREEN}PASS${NC}"
fi

# Check for actual tokens
echo -n "Checking for tokens... "
if grep -r "ghp_[a-zA-Z0-9]\|ghs_[a-zA-Z0-9]\|github_pat_[a-zA-Z0-9]" . --exclude-dir=node_modules --exclude-dir=.git --exclude="*.md" --exclude="*.sh" 2>/dev/null; then
    echo -e "${RED}FAIL${NC} - Found potential GitHub tokens!"
    exit 1
else
    echo -e "${GREEN}PASS${NC}"
fi

# Check sensitive directories are empty
echo -n "Checking sensitive directories... "
SENSITIVE_DIRS=(".claude/logs" ".claude/transcripts" ".claude/captures" ".claude/team/handoffs")
for dir in "${SENSITIVE_DIRS[@]}"; do
    if [ -d "$dir" ] && [ "$(ls -A $dir 2>/dev/null)" ]; then
        echo -e "${YELLOW}WARNING${NC} - $dir contains files"
    fi
done
echo -e "${GREEN}DONE${NC}"

# Verify .gitignore entries
echo -n "Verifying .gitignore... "
REQUIRED_IGNORES=(".env.local" ".claude/logs/" ".claude/transcripts/" ".claude/backups/")
for ignore in "${REQUIRED_IGNORES[@]}"; do
    if ! grep -q "^$ignore" .gitignore; then
        echo -e "${RED}FAIL${NC} - Missing $ignore in .gitignore"
        exit 1
    fi
done
echo -e "${GREEN}PASS${NC}"

# Check for placeholder values in .mcp.json
echo -n "Checking .mcp.json has placeholders... "
if grep -q "YOUR_.*_KEY\|YOUR_.*_TOKEN" .mcp.json; then
    echo -e "${GREEN}PASS${NC}"
else
    echo -e "${YELLOW}WARNING${NC} - .mcp.json might contain real keys"
fi

# Final summary
echo ""
echo "✅ Security verification complete!"
echo ""
echo "Final checklist:"
echo "- [ ] Review SECURITY_REVIEW.md for any additional items"
echo "- [ ] Test a fresh clone in a new directory"
echo "- [ ] Ensure all team members are aware of security practices"
echo "- [ ] Consider adding branch protection rules on GitHub"
echo ""
echo "🚀 Ready to make repository public!"
