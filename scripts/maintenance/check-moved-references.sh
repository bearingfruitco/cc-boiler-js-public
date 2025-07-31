#!/bin/bash
# Script to find references to moved files in documentation

echo "Searching for references to moved files..."
echo "========================================="

# Files that were moved
MOVED_FILES=(
    "CLEANUP_ANALYSIS_REPORT.md"
    "CLEANUP_COMPLETE.md"
    "COMMAND_CONSOLIDATION.md"
    "BOILERPLATE_CHANGELOG.md"
    "analyze-alias-duplication.py"
    "analyze-commands.py" 
    "clean-aliases.sh"
    "create-all-aliases.sh"
    "complete-playwright-integration.sh"
    "fix-commands.sh"
    "test-integration-docs.sh"
    "ENHANCEMENT_SUMMARY.md"
    "V4_RELEASE_SUMMARY.md"
    "CLAUDE_AGENT_COMPLETE_ONBOARDING.md"
    "CLAUDE_AGENT_HANDOFF.md"
    "CLAUDE_AGENT_QUICK_PROMPT.md"
    "GIT_PUSH_DUAL_REPOS_PROMPT.md"
    "GIT_PUSH_QUICK_PROMPT.md"
    "execute-push.sh"
    "push-to-both-repos.sh"
)

# Search in docs directory
cd /Users/shawnsmith/dev/bfc/boilerplate

for file in "${MOVED_FILES[@]}"; do
    echo -e "\nSearching for references to: $file"
    echo "-----------------------------------"
    
    # Search for the filename in all markdown files
    results=$(grep -r "$file" docs/ --include="*.md" 2>/dev/null | grep -v "Binary file")
    
    if [ ! -z "$results" ]; then
        echo "$results"
    else
        echo "No references found"
    fi
done

echo -e "\n\nSearching for path references..."
echo "================================="

# Check for specific path patterns
echo -e "\nChecking for root path references (e.g., './' or '../'):"
grep -r -E "(\.\/|\.\.\/)(CLEANUP_|COMMAND_|analyze-|clean-|create-all-|complete-playwright|fix-commands|test-integration|ENHANCEMENT_|V4_RELEASE|CLAUDE_AGENT_|GIT_PUSH_|execute-push|push-to-both)" docs/ --include="*.md" 2>/dev/null | grep -v "Binary file"

echo -e "\nDone!"
