#!/bin/bash

# rollback-integration.sh
# Safely removes boilerplate integration from your project
# 
# Usage:
#   ./scripts/rollback-integration.sh [--keep=components,list] [--force]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Default values
KEEP_COMPONENTS=""
FORCE=false

# Parse arguments
for arg in "$@"; do
  case $arg in
    --keep=*)
      KEEP_COMPONENTS="${arg#*=}"
      ;;
    --force)
      FORCE=true
      ;;
    --help)
      echo "Usage: $0 [--keep=components,list] [--force]"
      echo ""
      echo "Options:"
      echo "  --keep=LIST    Comma-separated list of components to keep"
      echo "                 Example: --keep=commands,agents"
      echo "  --force        Skip confirmation prompts"
      echo ""
      echo "Components:"
      echo "  commands   - Keep .claude/commands/"
      echo "  agents     - Keep .claude/agents/"
      echo "  hooks      - Keep .claude/hooks/"
      echo "  prps       - Keep PRPs/"
      echo "  agenteos   - Keep .agent-os/"
      echo "  docs       - Keep boilerplate docs"
      exit 0
      ;;
  esac
done

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}    Boilerplate Integration Rollback${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Step 1: Detect integration
echo -e "${BLUE}🔍 Detecting integration...${NC}"
echo ""

INTEGRATION_FOUND=false
BOILERPLATE_FILES=()

# Check for -boilerplate suffixed files
while IFS= read -r file; do
  BOILERPLATE_FILES+=("$file")
  INTEGRATION_FOUND=true
done < <(find . -name "*-boilerplate.*" -o -name "*-boilerplate" 2>/dev/null | grep -v node_modules | grep -v .git)

# Check for integration directory
if [ -d ".claude-integration" ]; then
  INTEGRATION_FOUND=true
  echo "  • Found integration metadata"
fi

# Check for boilerplate-specific directories
if [ -d ".agent-os" ]; then
  echo "  • Found .agent-os directory"
fi

if [ -d "PRPs" ]; then
  echo "  • Found PRPs directory"
fi

if [ -d "field-registry" ]; then
  echo "  • Found field-registry"
fi

if [ ${#BOILERPLATE_FILES[@]} -gt 0 ]; then
  echo "  • Found ${#BOILERPLATE_FILES[@]} -boilerplate files"
fi

if [ "$INTEGRATION_FOUND" = false ]; then
  echo -e "${YELLOW}No boilerplate integration detected${NC}"
  exit 0
fi

# Step 2: Show what will be removed
echo ""
echo -e "${BLUE}📋 Rollback Plan${NC}"
echo ""

echo "Will remove:"
echo "  • All files ending with -boilerplate"
echo "  • Integration metadata (.claude-integration/)"

# Check what to keep
IFS=',' read -ra KEEP_ARRAY <<< "$KEEP_COMPONENTS"

if [[ ! " ${KEEP_ARRAY[@]} " =~ " commands " ]]; then
  echo "  • Boilerplate commands from .claude/commands/"
fi

if [[ ! " ${KEEP_ARRAY[@]} " =~ " agents " ]]; then
  echo "  • Boilerplate agents from .claude/agents/"
fi

if [[ ! " ${KEEP_ARRAY[@]} " =~ " hooks " ]]; then
  echo "  • Boilerplate hooks from .claude/hooks/"
fi

if [[ ! " ${KEEP_ARRAY[@]} " =~ " prps " ]] && [ -d "PRPs" ]; then
  echo "  • PRPs directory"
fi

if [[ ! " ${KEEP_ARRAY[@]} " =~ " agenteos " ]] && [ -d ".agent-os" ]; then
  echo "  • .agent-os directory"
fi

# Always remove these (added by boilerplate)
[ -f "CLAUDE_BOILERPLATE.md" ] && echo "  • CLAUDE_BOILERPLATE.md"
[ -f "QUICK_REFERENCE.md" ] && echo "  • QUICK_REFERENCE.md"

# Step 3: Confirm
if [ "$FORCE" = false ]; then
  echo ""
  echo -e "${YELLOW}⚠️  This will permanently remove boilerplate files${NC}"
  echo -n "Continue? (y/n) "
  read -r response
  if [ "$response" != "y" ]; then
    exit 0
  fi
fi

# Step 4: Execute rollback
echo ""
echo -e "${BLUE}🗑️  Removing boilerplate files...${NC}"

# Remove -boilerplate files
removed_count=0
for file in "${BOILERPLATE_FILES[@]}"; do
  rm -f "$file"
  ((removed_count++))
  echo "  • Removed: $file"
done

# Remove integration metadata
if [ -d ".claude-integration" ]; then
  rm -rf ".claude-integration"
  echo "  • Removed: .claude-integration/"
fi

# Remove boilerplate-specific files
[ -f "CLAUDE_BOILERPLATE.md" ] && rm -f "CLAUDE_BOILERPLATE.md" && echo "  • Removed: CLAUDE_BOILERPLATE.md"
[ -f "QUICK_REFERENCE.md" ] && rm -f "QUICK_REFERENCE.md" && echo "  • Removed: QUICK_REFERENCE.md"

# Remove directories (if not keeping)
if [[ ! " ${KEEP_ARRAY[@]} " =~ " prps " ]] && [ -d "PRPs" ]; then
  rm -rf "PRPs"
  echo "  • Removed: PRPs/"
fi

if [[ ! " ${KEEP_ARRAY[@]} " =~ " agenteos " ]] && [ -d ".agent-os" ]; then
  rm -rf ".agent-os"
  echo "  • Removed: .agent-os/"
fi

if [ -d "field-registry" ]; then
  rm -rf "field-registry"
  echo "  • Removed: field-registry/"
fi

# Clean up .claude directory (selectively)
if [ -d ".claude" ]; then
  # Remove boilerplate commands (if not keeping)
  if [[ ! " ${KEEP_ARRAY[@]} " =~ " commands " ]] && [ -d ".claude/commands" ]; then
    # Only remove commands that came from boilerplate
    # This is tricky - we'd need to know which ones are original
    echo "  • Note: Review .claude/commands/ manually"
  fi
  
  # Remove boilerplate agents (if not keeping)
  if [[ ! " ${KEEP_ARRAY[@]} " =~ " agents " ]] && [ -d ".claude/agents" ]; then
    # Remove known boilerplate agents
    for agent in frontend backend security qa performance analyzer; do
      [ -f ".claude/agents/$agent.md" ] && rm -f ".claude/agents/$agent.md"
    done
    echo "  • Removed: boilerplate agents"
  fi
fi

# Remove merge suggestion files
find . -name "*-merge-suggestion.*" -type f -delete 2>/dev/null || true
find . -name "*-combined.*" -type f -delete 2>/dev/null || true

# Step 5: Clean up empty directories
find . -type d -empty -delete 2>/dev/null || true

# Step 6: Final report
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Rollback Complete!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo "Summary:"
echo "  • Removed $removed_count -boilerplate files"
echo "  • Cleaned up integration metadata"

if [ -n "$KEEP_COMPONENTS" ]; then
  echo "  • Kept: $KEEP_COMPONENTS"
fi

echo ""
echo "Your project has been restored to pre-integration state."
echo ""

# Check if any boilerplate might remain
REMAINING=$(find . -name "*boilerplate*" 2>/dev/null | grep -v node_modules | grep -v .git | wc -l || echo 0)
if [ $REMAINING -gt 0 ]; then
  echo -e "${YELLOW}Note: Some boilerplate-related files may remain.${NC}"
  echo "Run this command to find them:"
  echo "  find . -name '*boilerplate*' | grep -v node_modules"
fi

echo ""
echo "If you want to try integration again with different options:"
echo "  ./scripts/integrate-boilerplate-v2.sh --mode=selective"
echo ""
