#!/bin/bash

# ============================================================================
# Smart Local Boilerplate Integration
# 
# Integrates Claude Code Boilerplate from local copy into existing project
# Usage: ./integrate-from-local.sh [mode]
# Modes: full, commands, design, security, prps
# ============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Configuration
BOILERPLATE_DIR="/Users/shawnsmith/dev/bfc/boilerplate"
BACKUP_DIR=".integration-backup/$(date +%Y%m%d_%H%M%S)"
PROJECT_DIR="$(pwd)"
MODE="${1:-full}"

# Verify boilerplate exists
if [ ! -d "$BOILERPLATE_DIR" ]; then
  echo -e "${RED}Error: Boilerplate not found at $BOILERPLATE_DIR${NC}"
  echo "Please ensure the boilerplate is cloned to that location."
  exit 1
fi

echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}    Claude Code Boilerplate Integration (Local)${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Mode: ${MODE}${NC}"
echo -e "${YELLOW}Source: ${BOILERPLATE_DIR}${NC}"
echo -e "${YELLOW}Target: ${PROJECT_DIR}${NC}"
echo ""

# Create backup directory
mkdir -p "$BACKUP_DIR"
echo -e "${BLUE}Creating backups in ${BACKUP_DIR}...${NC}"

# Backup existing files
backup_if_exists() {
  if [ -e "$1" ]; then
    cp -r "$1" "$BACKUP_DIR/" 2>/dev/null
    echo "  ✓ Backed up: $1"
  fi
}

# Core files to potentially backup
backup_if_exists ".claude"
backup_if_exists "CLAUDE.md"
backup_if_exists "tailwind.config.js"
backup_if_exists "tsconfig.json"
backup_if_exists "biome.json"
backup_if_exists ".gitignore"
backup_if_exists "package.json"

echo ""
echo -e "${CYAN}Starting integration...${NC}"
echo ""

# Function to copy with smart merging
smart_copy() {
  local src="$1"
  local dest="$2"
  local merge_suffix="${3:-.boilerplate}"
  
  if [ -e "$dest" ]; then
    if [ -d "$src" ] && [ -d "$dest" ]; then
      # Directory exists - merge
      echo "  → Merging: $dest"
      rsync -av --backup --suffix="-original" "$src/" "$dest/" 2>/dev/null
    else
      # File exists - create .boilerplate version
      cp "$src" "${dest}${merge_suffix}" 2>/dev/null
      echo "  ⚠️ Created ${dest}${merge_suffix} (manual merge needed)"
    fi
  else
    # Doesn't exist - just copy
    cp -r "$src" "$dest" 2>/dev/null
    echo "  ✓ Added: $dest"
  fi
}

case $MODE in
  "full")
    echo -e "${GREEN}Full Integration Mode${NC}"
    echo ""
    
    # Core Claude files
    smart_copy "$BOILERPLATE_DIR/.claude" ".claude"
    smart_copy "$BOILERPLATE_DIR/CLAUDE.md" "CLAUDE.md"
    
    # PRPs and field registry
    smart_copy "$BOILERPLATE_DIR/PRPs" "PRPs"
    smart_copy "$BOILERPLATE_DIR/field-registry" "field-registry"
    
    # Configuration files
    smart_copy "$BOILERPLATE_DIR/tailwind.config.js" "tailwind.config.js"
    smart_copy "$BOILERPLATE_DIR/tsconfig.json" "tsconfig.json"
    smart_copy "$BOILERPLATE_DIR/biome.json" "biome.json"
    
    # Components (selective)
    if [ ! -d "components/ui" ]; then
      mkdir -p components
      cp -r "$BOILERPLATE_DIR/components/ui" "components/" 2>/dev/null
      echo "  ✓ Added: components/ui"
    fi
    
    # Lib utilities (selective)
    if [ ! -f "lib/utils.ts" ]; then
      mkdir -p lib
      cp "$BOILERPLATE_DIR/lib/utils.ts" "lib/" 2>/dev/null
      echo "  ✓ Added: lib/utils.ts"
    fi
    
    # Hooks
    if [ ! -d "hooks" ]; then
      cp -r "$BOILERPLATE_DIR/hooks" . 2>/dev/null
      echo "  ✓ Added: hooks"
    fi
    
    # Scripts
    mkdir -p scripts
    cp "$BOILERPLATE_DIR/scripts/setup-hooks.sh" "scripts/" 2>/dev/null
    cp "$BOILERPLATE_DIR/scripts/quick-setup.sh" "scripts/" 2>/dev/null
    chmod +x scripts/*.sh
    echo "  ✓ Added: setup scripts"
    ;;
    
  "commands")
    echo -e "${GREEN}Commands & Agents Only${NC}"
    echo ""
    
    smart_copy "$BOILERPLATE_DIR/.claude" ".claude"
    smart_copy "$BOILERPLATE_DIR/CLAUDE.md" "CLAUDE.md"
    ;;
    
  "design")
    echo -e "${GREEN}Design System Only${NC}"
    echo ""
    
    smart_copy "$BOILERPLATE_DIR/tailwind.config.js" "tailwind.config.js"
    if [ ! -d "components/ui" ]; then
      mkdir -p components
      cp -r "$BOILERPLATE_DIR/components/ui" "components/" 2>/dev/null
      echo "  ✓ Added: components/ui"
    fi
    ;;
    
  "security")
    echo -e "${GREEN}Security Features Only${NC}"
    echo ""
    
    smart_copy "$BOILERPLATE_DIR/field-registry" "field-registry"
    if [ -d "$BOILERPLATE_DIR/lib/security" ]; then
      mkdir -p lib
      cp -r "$BOILERPLATE_DIR/lib/security" "lib/" 2>/dev/null
      echo "  ✓ Added: lib/security"
    fi
    ;;
    
  "prps")
    echo -e "${GREEN}PRPs Only${NC}"
    echo ""
    
    smart_copy "$BOILERPLATE_DIR/PRPs" "PRPs"
    ;;
    
  *)
    echo -e "${RED}Unknown mode: $MODE${NC}"
    echo "Available modes: full, commands, design, security, prps"
    exit 1
    ;;
esac

echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Integration Complete!${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Check for files needing manual merge
if ls *.boilerplate 2>/dev/null 1>&2; then
  echo -e "${YELLOW}⚠️ Manual merge required for:${NC}"
  ls -la *.boilerplate
  echo ""
  echo "Compare these with your existing files and merge as needed."
  echo ""
fi

echo -e "${BOLD}Next steps:${NC}"
echo "1. Start Claude Code: ${CYAN}claude .${NC}"
echo "2. Load context: ${CYAN}/sr${NC}"
echo "3. Check commands: ${CYAN}/help${NC}"
echo "4. Analyze project: ${CYAN}/analyze-existing full${NC}"
echo ""

if [ "$MODE" = "full" ]; then
  echo -e "${YELLOW}Don't forget to:${NC}"
  echo "• Review and merge any .boilerplate files"
  echo "• Run: npm install (if new dependencies)"
  echo "• Set up git hooks: ./scripts/setup-hooks.sh"
fi

echo ""
echo -e "${GREEN}Backup saved to: ${BACKUP_DIR}${NC}"
