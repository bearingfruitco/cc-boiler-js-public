#!/bin/bash

# ============================================================================
# Claude Code Boilerplate Integration Script v4.0.0
# 
# This script safely integrates the Claude Code Boilerplate into your
# existing project without overwriting your files.
#
# Usage:
#   curl -sSL [url] | bash
#   or
#   ./integrate-existing.sh [options]
#
# Options:
#   --dry-run         Show what would happen without making changes
#   --mode=MODE       Integration mode: full|selective|sidecar (default: full)
#   --no-backup       Skip backup creation (not recommended)
#   --force           Overwrite conflicts (not recommended)
# ============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BOILERPLATE_REPO="https://github.com/bearingfruitco/claude-code-boilerplate.git"
TEMP_DIR="/tmp/claude-boilerplate-$$"
BACKUP_DIR=".claude-integration/backup/$(date +%Y%m%d_%H%M%S)"
MODE="${1:-full}"
DRY_RUN=false
NO_BACKUP=false
FORCE=false

# Parse arguments
for arg in "$@"; do
  case $arg in
    --dry-run)
      DRY_RUN=true
      ;;
    --mode=*)
      MODE="${arg#*=}"
      ;;
    --no-backup)
      NO_BACKUP=true
      ;;
    --force)
      FORCE=true
      ;;
    --help)
      echo "Usage: $0 [options]"
      echo "Options:"
      echo "  --dry-run         Show what would happen without making changes"
      echo "  --mode=MODE       Integration mode: full|selective|sidecar"
      echo "  --no-backup       Skip backup creation"
      echo "  --force           Overwrite conflicts"
      exit 0
      ;;
  esac
done

# Functions
print_header() {
  echo ""
  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${BLUE}  Claude Code Boilerplate Integration v4.0.0${NC}"
  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
}

check_prerequisites() {
  echo -e "${YELLOW}Checking prerequisites...${NC}"
  
  # Check for git
  if ! command -v git &> /dev/null; then
    echo -e "${RED}✗ git is required but not installed${NC}"
    exit 1
  fi
  
  # Check for curl or wget
  if ! command -v curl &> /dev/null && ! command -v wget &> /dev/null; then
    echo -e "${RED}✗ curl or wget is required${NC}"
    exit 1
  fi
  
  # Check if in a git repository
  if [ ! -d ".git" ]; then
    echo -e "${YELLOW}⚠ Warning: Not in a git repository${NC}"
    echo "It's recommended to run this in a git repository for easy rollback"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
      exit 1
    fi
  fi
  
  echo -e "${GREEN}✓ Prerequisites met${NC}"
}

detect_existing_version() {
  echo -e "${YELLOW}Detecting existing boilerplate...${NC}"
  
  if [ ! -d ".claude" ]; then
    echo "  No existing boilerplate detected"
    return
  fi
  
  # Check for version file
  if [ -f ".claude/VERSION" ]; then
    VERSION=$(cat .claude/VERSION)
    echo -e "${YELLOW}  Found version: v$VERSION${NC}"
    EXISTING_VERSION=$VERSION
    return
  fi
  
  # Detect by features
  if [ -d ".claude/agents" ] && [ -f ".claude/commands/orch.md" ]; then
    echo "  Detected v4.0 features"
    EXISTING_VERSION="4.0"
  elif [ -d ".claude/hooks" ]; then
    echo "  Detected v3.5 features"
    EXISTING_VERSION="3.5"
  elif [ -f ".claude/commands/create-prp.md" ]; then
    echo "  Detected v3.0 features"
    EXISTING_VERSION="3.0"
  elif [ -f ".claude/commands/create-prd.md" ]; then
    echo "  Detected v2.0 features"
    EXISTING_VERSION="2.0"
  elif [ -d ".claude/commands" ]; then
    echo "  Detected v1.0 features"
    EXISTING_VERSION="1.0"
  fi
}

download_boilerplate() {
  echo -e "${YELLOW}Downloading boilerplate...${NC}"
  
  if [ "$DRY_RUN" = true ]; then
    echo "  [DRY RUN] Would clone boilerplate to $TEMP_DIR"
    return
  fi
  
  # Clone the boilerplate
  git clone --quiet --depth 1 "$BOILERPLATE_REPO" "$TEMP_DIR" 2>/dev/null
  
  if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Boilerplate downloaded${NC}"
  else
    echo -e "${RED}✗ Failed to download boilerplate${NC}"
    exit 1
  fi
}

create_backup() {
  if [ "$NO_BACKUP" = true ] || [ "$DRY_RUN" = true ]; then
    return
  fi
  
  echo -e "${YELLOW}Creating backup...${NC}"
  
  mkdir -p "$BACKUP_DIR"
  
  # Backup existing directories/files if they exist
  BACKUP_ITEMS=(
    ".claude"
    ".agent-os"
    "field-registry"
    "PRPs"
    "templates"
    "CLAUDE.md"
    "CLAUDE_BOILERPLATE.md"
    "biome.json"
    "playwright.config.ts"
    ".husky"
  )
  
  for item in "${BACKUP_ITEMS[@]}"; do
    if [ -e "$item" ]; then
      cp -r "$item" "$BACKUP_DIR/" 2>/dev/null
      echo "  ✓ Backed up $item"
    fi
  done
  
  # Save metadata
  cat > "$BACKUP_DIR/metadata.json" << EOF
{
  "date": "$(date)",
  "mode": "$MODE",
  "existing_version": "${EXISTING_VERSION:-none}",
  "project": "$(basename $(pwd))"
}
EOF
  
  echo -e "${GREEN}✓ Backup created at $BACKUP_DIR${NC}"
}

integrate_claude_directory() {
  echo -e "${YELLOW}Integrating .claude directory...${NC}"
  
  if [ "$DRY_RUN" = true ]; then
    if [ -d ".claude" ]; then
      echo "  [DRY RUN] Would merge with existing .claude/"
      echo "  [DRY RUN] Conflicts would be renamed with -project suffix"
    else
      echo "  [DRY RUN] Would create .claude/ directory"
    fi
    return
  fi
  
  # Create .claude if it doesn't exist
  mkdir -p .claude/{commands,hooks,agents,config,state,context}
  
  # Handle commands
  if [ -d "$TEMP_DIR/.claude/commands" ]; then
    for cmd in "$TEMP_DIR"/.claude/commands/*.md; do
      basename=$(basename "$cmd")
      
      if [ -f ".claude/commands/$basename" ] && [ "$FORCE" != true ]; then
        # Conflict - rename existing
        mv ".claude/commands/$basename" ".claude/commands/${basename%.md}-project.md"
        echo "  Renamed existing: $basename → ${basename%.md}-project.md"
      fi
      
      cp "$cmd" ".claude/commands/"
    done
    echo -e "${GREEN}  ✓ Commands integrated${NC}"
  fi
  
  # Handle hooks
  if [ -d "$TEMP_DIR/.claude/hooks" ]; then
    for hook_type in pre-tool-use post-tool-use stop; do
      mkdir -p ".claude/hooks/$hook_type"
      
      # Renumber existing hooks to 00-09 if they exist
      if [ -d ".claude/hooks/$hook_type" ]; then
        i=0
        for hook in .claude/hooks/$hook_type/*.py; do
          if [ -f "$hook" ]; then
            base=$(basename "$hook" | sed 's/^[0-9]*//')
            mv "$hook" ".claude/hooks/$hook_type/0${i}-project-${base}" 2>/dev/null
            ((i++)) || true
          fi
        done
      fi
      
      # Copy new hooks
      cp "$TEMP_DIR"/.claude/hooks/$hook_type/*.py ".claude/hooks/$hook_type/" 2>/dev/null || true
    done
    echo -e "${GREEN}  ✓ Hooks integrated${NC}"
  fi
  
  # Copy agents
  cp -r "$TEMP_DIR"/.claude/agents/* .claude/agents/ 2>/dev/null || true
  echo -e "${GREEN}  ✓ Agents installed${NC}"
  
  # Copy config files
  [ ! -f ".claude/settings.json" ] && cp "$TEMP_DIR/.claude/settings.json" .claude/ 2>/dev/null || true
  
  # Create VERSION file
  echo "4.0.0" > .claude/VERSION
}

integrate_other_directories() {
  echo -e "${YELLOW}Integrating other directories...${NC}"
  
  if [ "$DRY_RUN" = true ]; then
    echo "  [DRY RUN] Would install: .agent-os, field-registry, PRPs, templates"
    return
  fi
  
  # Copy directories that likely don't exist
  [ ! -d ".agent-os" ] && cp -r "$TEMP_DIR/.agent-os" . && echo -e "${GREEN}  ✓ Agent OS installed${NC}"
  [ ! -d "field-registry" ] && cp -r "$TEMP_DIR/field-registry" . && echo -e "${GREEN}  ✓ Field registry installed${NC}"
  [ ! -d "PRPs" ] && cp -r "$TEMP_DIR/PRPs" . && echo -e "${GREEN}  ✓ PRPs installed${NC}"
  [ ! -d "templates" ] && cp -r "$TEMP_DIR/templates" . && echo -e "${GREEN}  ✓ Templates installed${NC}"
}

integrate_documentation() {
  echo -e "${YELLOW}Integrating documentation...${NC}"
  
  if [ "$DRY_RUN" = true ]; then
    if [ -f "CLAUDE.md" ]; then
      echo "  [DRY RUN] Would create CLAUDE_BOILERPLATE.md"
      echo "  [DRY RUN] Would append integration notice to CLAUDE.md"
    else
      echo "  [DRY RUN] Would create CLAUDE.md"
    fi
    return
  fi
  
  if [ -f "CLAUDE.md" ]; then
    # User has CLAUDE.md, add ours as supplementary
    cp "$TEMP_DIR/CLAUDE.md" CLAUDE_BOILERPLATE.md
    
    # Add integration notice if not already present
    if ! grep -q "Boilerplate Integration" CLAUDE.md; then
      cat >> CLAUDE.md << 'EOF'

---

## 🚀 Boilerplate Integration

This project has been enhanced with Claude Code Boilerplate v4.0.0.
See `CLAUDE_BOILERPLATE.md` for boilerplate commands and features.

Key commands: `/sr`, `/vd`, `/create-prp`, `/orch`, `/chain`
EOF
    fi
    echo -e "${GREEN}  ✓ Created CLAUDE_BOILERPLATE.md${NC}"
  else
    # No existing CLAUDE.md, use ours
    cp "$TEMP_DIR/CLAUDE.md" CLAUDE.md
    echo -e "${GREEN}  ✓ Installed CLAUDE.md${NC}"
  fi
}

integrate_config_files() {
  echo -e "${YELLOW}Integrating configuration files...${NC}"
  
  if [ "$DRY_RUN" = true ]; then
    echo "  [DRY RUN] Would handle: biome.json, playwright.config.ts, etc."
    return
  fi
  
  # Biome
  if [ -f "biome.json" ]; then
    cp "$TEMP_DIR/biome.json" biome.boilerplate.json
    echo "  Created biome.boilerplate.json (existing preserved)"
  else
    cp "$TEMP_DIR/biome.json" biome.json
    echo -e "${GREEN}  ✓ Installed biome.json${NC}"
  fi
  
  # Playwright
  if [ -f "playwright.config.ts" ]; then
    cp "$TEMP_DIR/playwright.config.ts" playwright.boilerplate.config.ts
    echo "  Created playwright.boilerplate.config.ts (existing preserved)"
  else
    cp "$TEMP_DIR/playwright.config.ts" playwright.config.ts 2>/dev/null || true
    echo -e "${GREEN}  ✓ Installed playwright.config.ts${NC}"
  fi
  
  # .env.example
  if [ ! -f ".env.example" ]; then
    cp "$TEMP_DIR/.env.example" .env.example 2>/dev/null || true
    echo -e "${GREEN}  ✓ Installed .env.example${NC}"
  fi
  
  # Git hooks
  if [ ! -d ".husky" ]; then
    cp -r "$TEMP_DIR/.husky" . 2>/dev/null || true
    echo -e "${GREEN}  ✓ Installed git hooks${NC}"
  fi
}

generate_report() {
  echo -e "${YELLOW}Generating integration report...${NC}"
  
  if [ "$DRY_RUN" = true ]; then
    return
  fi
  
  cat > BOILERPLATE_INTEGRATION.md << 'EOF'
# Boilerplate Integration Complete! 🎉

## Installation Summary

**Date**: $(date)
**Mode**: $(echo $MODE)
**Version**: 4.0.0

### ✅ What Was Added

- **Commands**: 150+ commands in `.claude/commands/`
- **Agents**: 31 AI agents in `.claude/agents/`
- **Hooks**: Automation in `.claude/hooks/`
- **Standards**: Agent OS in `.agent-os/`
- **Security**: Field registry
- **Templates**: Component templates

### 🚀 Next Steps

1. Open in Claude Code:
   ```bash
   claude .
   ```

2. Load the system:
   ```bash
   /sr
   ```

3. Analyze your project:
   ```bash
   /analyze-existing full
   ```

4. Start building:
   ```bash
   /fw start
   ```

### 📚 Key Commands

- `/sr` - Smart resume
- `/vd` - Validate design
- `/create-prp` - Create implementation guide
- `/orch` - Orchestrate agents
- `/chain list` - View workflows
- `/help` - All commands

### 🔄 Rollback

If needed, restore from backup:
```bash
cp -r $(echo $BACKUP_DIR)/* .
```

---

For full documentation, see `/docs` in Claude Code.
EOF
  
  echo -e "${GREEN}✓ Report saved to BOILERPLATE_INTEGRATION.md${NC}"
}

cleanup() {
  if [ "$DRY_RUN" = false ] && [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
  fi
}

main() {
  print_header
  check_prerequisites
  detect_existing_version
  
  # Check if already v4.0
  if [ "$EXISTING_VERSION" = "4.0" ]; then
    echo -e "${GREEN}✓ You already have v4.0.0 installed!${NC}"
    echo "Use /upgrade-boilerplate in Claude Code if you want to refresh."
    exit 0
  fi
  
  download_boilerplate
  create_backup
  
  case "$MODE" in
    full)
      echo -e "${BLUE}Running full integration...${NC}"
      integrate_claude_directory
      integrate_other_directories
      integrate_documentation
      integrate_config_files
      ;;
    selective)
      echo -e "${BLUE}Selective mode${NC}"
      echo "Choose what to integrate:"
      echo "1) Commands & Automation"
      echo "2) Agent OS & Standards"
      echo "3) PRP System"
      echo "4) Security (field-registry)"
      echo "5) Config files"
      read -p "Enter numbers (comma-separated): " choices
      # Implementation would go here
      ;;
    sidecar)
      echo -e "${BLUE}Sidecar mode${NC}"
      if [ "$DRY_RUN" = false ]; then
        cp -r "$TEMP_DIR/.claude" .claude-boilerplate
        echo -e "${GREEN}✓ Installed as .claude-boilerplate/${NC}"
        echo "Access commands with /bb prefix in Claude Code"
      fi
      ;;
  esac
  
  generate_report
  cleanup
  
  echo ""
  echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${GREEN}  ✅ Integration Complete!${NC}"
  echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  echo "Next steps:"
  echo "1. Open in Claude Code: claude ."
  echo "2. Run: /sr"
  echo "3. Run: /analyze-existing full"
  echo ""
  
  if [ -n "$EXISTING_VERSION" ] && [ "$EXISTING_VERSION" != "4.0" ]; then
    echo -e "${YELLOW}Note: Detected version $EXISTING_VERSION${NC}"
    echo "After opening Claude Code, run: /upgrade-boilerplate"
    echo ""
  fi
}

# Trap to ensure cleanup on exit
trap cleanup EXIT

# Run main function
main
