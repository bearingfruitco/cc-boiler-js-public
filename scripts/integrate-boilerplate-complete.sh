#!/bin/bash

# ============================================================================
# Claude Code Boilerplate COMPLETE Integration Script v4.1.0
# 
# This script properly integrates ALL Claude Code Boilerplate files into your
# existing project, with intelligent conflict resolution.
#
# Key improvements:
# - Downloads EVERYTHING to a temp directory for inspection
# - Copies ALL necessary files (not just configs)
# - Shows you what's being added/skipped
# - Creates proper backups
# ============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
PUBLIC_REPO="https://github.com/bearingfruitco/cc-boiler-js-public.git"
TEMP_DIR="/tmp/claude-boilerplate-complete-$$"
BACKUP_DIR=".claude-integration/backup/$(date +%Y%m%d_%H%M%S)"
PROJECT_DIR="$(pwd)"

# Parse arguments
DRY_RUN=false
VERBOSE=false
SKIP_BACKUP=false

for arg in "$@"; do
  case $arg in
    --dry-run)
      DRY_RUN=true
      echo -e "${YELLOW}DRY RUN MODE - No changes will be made${NC}"
      ;;
    --verbose)
      VERBOSE=true
      ;;
    --skip-backup)
      SKIP_BACKUP=true
      ;;
    --help)
      echo "Usage: $0 [options]"
      echo "Options:"
      echo "  --dry-run       Show what would happen without making changes"
      echo "  --verbose       Show detailed progress"
      echo "  --skip-backup   Skip backup creation (not recommended)"
      exit 0
      ;;
  esac
done

# Functions
print_header() {
  echo ""
  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${BLUE}  Claude Code Boilerplate COMPLETE Integration v4.1.0${NC}"
  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
}

check_prerequisites() {
  echo -e "${YELLOW}📋 Checking prerequisites...${NC}"
  
  if ! command -v git &> /dev/null; then
    echo -e "${RED}✗ git is required but not installed${NC}"
    exit 1
  fi
  
  if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}⚠ python3 not found - hooks won't work${NC}"
  fi
  
  echo -e "${GREEN}✓ Prerequisites satisfied${NC}"
}

download_complete_boilerplate() {
  echo -e "${YELLOW}📥 Downloading complete boilerplate...${NC}"
  
  if [ "$DRY_RUN" = true ]; then
    echo "  [DRY RUN] Would clone to $TEMP_DIR"
    return
  fi
  
  # Clone the entire repository
  git clone --depth 1 "$PUBLIC_REPO" "$TEMP_DIR" 2>/dev/null || {
    echo -e "${RED}✗ Failed to download boilerplate${NC}"
    exit 1
  }
  
  echo -e "${GREEN}✓ Downloaded complete boilerplate${NC}"
  
  # Show what we got
  echo -e "${CYAN}📊 Boilerplate contents:${NC}"
  echo "  - Commands: $(find "$TEMP_DIR/.claude/commands" -name "*.md" 2>/dev/null | wc -l) files"
  echo "  - Agents: $(find "$TEMP_DIR/.claude/agents" -name "*.md" 2>/dev/null | wc -l) files"
  echo "  - Hooks: $(find "$TEMP_DIR/.claude/hooks" -name "*.py" 2>/dev/null | wc -l) files"
  echo "  - Scripts: $(find "$TEMP_DIR/.claude/scripts" -name "*.sh" 2>/dev/null | wc -l) files"
  echo "  - Templates: $(find "$TEMP_DIR/templates" -type f 2>/dev/null | wc -l) files"
}

create_backup() {
  if [ "$SKIP_BACKUP" = true ]; then
    echo -e "${YELLOW}⚠ Skipping backup${NC}"
    return
  fi
  
  echo -e "${YELLOW}💾 Creating backup...${NC}"
  
  if [ "$DRY_RUN" = true ]; then
    echo "  [DRY RUN] Would backup to $BACKUP_DIR"
    return
  fi
  
  mkdir -p "$BACKUP_DIR"
  
  # Backup existing directories that might be modified
  [ -d ".claude" ] && cp -r .claude "$BACKUP_DIR/"
  [ -f "CLAUDE.md" ] && cp CLAUDE.md "$BACKUP_DIR/"
  [ -d ".agent-os" ] && cp -r .agent-os "$BACKUP_DIR/"
  [ -d "PRPs" ] && cp -r PRPs "$BACKUP_DIR/"
  
  echo -e "${GREEN}✓ Backup created at $BACKUP_DIR${NC}"
}

integrate_claude_directory() {
  echo -e "${YELLOW}📦 Integrating .claude directory (complete)...${NC}"
  
  if [ "$DRY_RUN" = true ]; then
    echo "  [DRY RUN] Would integrate complete .claude directory"
    return
  fi
  
  # Create all necessary directories
  mkdir -p .claude/{commands,agents,config,state,context,logs,metrics}
  mkdir -p .claude/hooks/{pre-tool-use,post-tool-use,stop,notification,user-prompt-submit,sub-agent-stop,pre-compact,utils}
  mkdir -p .claude/scripts
  
  # 1. Copy ALL commands
  echo "  📝 Copying commands..."
  if [ -d "$TEMP_DIR/.claude/commands" ]; then
    for cmd in "$TEMP_DIR"/.claude/commands/*.md; do
      [ -f "$cmd" ] || continue
      basename=$(basename "$cmd")
      
      if [ -f ".claude/commands/$basename" ]; then
        # Conflict - rename existing
        mv ".claude/commands/$basename" ".claude/commands/${basename%.md}-original.md"
        [ "$VERBOSE" = true ] && echo "    Renamed existing: $basename"
      fi
      
      cp "$cmd" .claude/commands/
      [ "$VERBOSE" = true ] && echo "    ✓ $basename"
    done
  fi
  
  # 2. Copy ALL agents
  echo "  🤖 Copying agents..."
  if [ -d "$TEMP_DIR/.claude/agents" ]; then
    cp -r "$TEMP_DIR"/.claude/agents/*.md .claude/agents/ 2>/dev/null || true
    [ "$VERBOSE" = true ] && echo "    ✓ $(ls .claude/agents/*.md | wc -l) agents"
  fi
  
  # 3. Copy ALL hooks with subdirectories
  echo "  🪝 Copying hooks (complete)..."
  for hook_dir in pre-tool-use post-tool-use stop notification user-prompt-submit sub-agent-stop pre-compact utils; do
    if [ -d "$TEMP_DIR/.claude/hooks/$hook_dir" ]; then
      # Copy all Python files
      cp "$TEMP_DIR"/.claude/hooks/$hook_dir/*.py .claude/hooks/$hook_dir/ 2>/dev/null || true
      # Copy any shell scripts
      cp "$TEMP_DIR"/.claude/hooks/$hook_dir/*.sh .claude/hooks/$hook_dir/ 2>/dev/null || true
      [ "$VERBOSE" = true ] && echo "    ✓ $hook_dir"
    fi
  done
  
  # Copy root hook files
  cp "$TEMP_DIR"/.claude/hooks/*.py .claude/hooks/ 2>/dev/null || true
  cp "$TEMP_DIR"/.claude/hooks/*.sh .claude/hooks/ 2>/dev/null || true
  cp "$TEMP_DIR"/.claude/hooks/*.md .claude/hooks/ 2>/dev/null || true
  
  # 4. Copy ALL scripts (critical for hooks!)
  echo "  📜 Copying scripts..."
  if [ -d "$TEMP_DIR/.claude/scripts" ]; then
    cp -r "$TEMP_DIR"/.claude/scripts/* .claude/scripts/ 2>/dev/null || true
    [ "$VERBOSE" = true ] && echo "    ✓ $(ls .claude/scripts/*.sh 2>/dev/null | wc -l) scripts"
  fi
  
  # 5. Copy config directory
  echo "  ⚙️ Copying configuration..."
  if [ -d "$TEMP_DIR/.claude/config" ]; then
    cp -r "$TEMP_DIR"/.claude/config/* .claude/config/ 2>/dev/null || true
  fi
  
  # 6. Copy settings files
  if [ ! -f ".claude/settings.json" ] && [ -f "$TEMP_DIR/.claude/settings.json" ]; then
    cp "$TEMP_DIR/.claude/settings.json" .claude/
  elif [ -f "$TEMP_DIR/.claude/settings.json" ]; then
    cp "$TEMP_DIR/.claude/settings.json" .claude/settings.boilerplate.json
    echo "    ⚠ settings.json exists - saved boilerplate as settings.boilerplate.json"
  fi
  
  # 7. Copy other important files
  cp "$TEMP_DIR"/.claude/*.md .claude/ 2>/dev/null || true
  cp "$TEMP_DIR"/.claude/VERSION .claude/ 2>/dev/null || true
  
  echo -e "${GREEN}✓ Complete .claude directory integrated${NC}"
}

integrate_root_directories() {
  echo -e "${YELLOW}📁 Integrating root directories...${NC}"
  
  if [ "$DRY_RUN" = true ]; then
    echo "  [DRY RUN] Would copy: .agent-os, PRPs, field-registry, templates, etc."
    return
  fi
  
  # Copy directories that enhance the project
  directories=(
    ".agent-os"
    "PRPs"
    "field-registry"
    "templates"
    "docs"
  )
  
  for dir in "${directories[@]}"; do
    if [ -d "$TEMP_DIR/$dir" ]; then
      if [ ! -d "$dir" ]; then
        cp -r "$TEMP_DIR/$dir" .
        echo -e "${GREEN}  ✓ Installed $dir${NC}"
      else
        echo "  ⚠ $dir exists - skipping"
      fi
    fi
  done
  
  # Special handling for lib directory (merge, don't overwrite)
  if [ -d "$TEMP_DIR/lib" ]; then
    echo "  📚 Merging lib utilities..."
    for libdir in "$TEMP_DIR"/lib/*; do
      dirname=$(basename "$libdir")
      if [ ! -d "lib/$dirname" ]; then
        mkdir -p lib
        cp -r "$libdir" lib/
        [ "$VERBOSE" = true ] && echo "    ✓ lib/$dirname"
      fi
    done
  fi
  
  # Special handling for scripts directory
  if [ -d "$TEMP_DIR/scripts" ] && [ ! -d "scripts" ]; then
    cp -r "$TEMP_DIR/scripts" .
    echo -e "${GREEN}  ✓ Installed scripts directory${NC}"
  fi
}

integrate_documentation() {
  echo -e "${YELLOW}📚 Integrating documentation...${NC}"
  
  if [ "$DRY_RUN" = true ]; then
    echo "  [DRY RUN] Would handle CLAUDE.md and other docs"
    return
  fi
  
  # Handle CLAUDE.md
  if [ -f "CLAUDE.md" ]; then
    cp "$TEMP_DIR/CLAUDE.md" CLAUDE_BOILERPLATE.md
    echo -e "${GREEN}  ✓ Created CLAUDE_BOILERPLATE.md (original preserved)${NC}"
    
    # Add integration notice
    if ! grep -q "Boilerplate Integration" CLAUDE.md; then
      cat >> CLAUDE.md << 'EOF'

---

## 🚀 Claude Code Boilerplate v4.1.0 Integration

This project has been enhanced with the complete Claude Code Boilerplate.

### Key Features:
- 150+ commands (`/sr`, `/vd`, `/cc`, `/chain`, etc.)
- 31 AI agents for specialized tasks
- Automated workflows and hooks
- Design system enforcement
- Architecture tracking

See `CLAUDE_BOILERPLATE.md` for full boilerplate documentation.

Start with: `/sr` (Smart Resume)
EOF
    fi
  else
    cp "$TEMP_DIR/CLAUDE.md" CLAUDE.md
    echo -e "${GREEN}  ✓ Installed CLAUDE.md${NC}"
  fi
  
  # Copy other documentation files
  for doc in QUICK_REFERENCE.md SYSTEM_OVERVIEW.md; do
    if [ -f "$TEMP_DIR/$doc" ] && [ ! -f "$doc" ]; then
      cp "$TEMP_DIR/$doc" .
      echo -e "${GREEN}  ✓ Installed $doc${NC}"
    fi
  done
}

integrate_config_files() {
  echo -e "${YELLOW}⚙️ Integrating configuration files...${NC}"
  
  if [ "$DRY_RUN" = true ]; then
    echo "  [DRY RUN] Would handle config files"
    return
  fi
  
  configs=(
    "biome.json"
    "playwright.config.ts"
    ".env.example"
    "components.json"
    ".coderabbit.yaml"
  )
  
  for config in "${configs[@]}"; do
    if [ -f "$TEMP_DIR/$config" ]; then
      if [ -f "$config" ]; then
        cp "$TEMP_DIR/$config" "${config}.boilerplate"
        echo "  ⚠ $config exists - saved boilerplate as ${config}.boilerplate"
      else
        cp "$TEMP_DIR/$config" "$config"
        echo -e "${GREEN}  ✓ Installed $config${NC}"
      fi
    fi
  done
  
  # Git hooks
  if [ -d "$TEMP_DIR/.husky" ] && [ ! -d ".husky" ]; then
    cp -r "$TEMP_DIR/.husky" .
    echo -e "${GREEN}  ✓ Installed git hooks${NC}"
  fi
}

verify_integration() {
  echo -e "${YELLOW}🔍 Verifying integration...${NC}"
  
  if [ "$DRY_RUN" = true ]; then
    return
  fi
  
  # Count what we have
  COMMANDS=$(find .claude/commands -name "*.md" 2>/dev/null | wc -l)
  AGENTS=$(find .claude/agents -name "*.md" 2>/dev/null | wc -l)
  HOOKS=$(find .claude/hooks -name "*.py" 2>/dev/null | wc -l)
  SCRIPTS=$(find .claude/scripts -name "*.sh" 2>/dev/null | wc -l)
  
  echo -e "${CYAN}📊 Integration Summary:${NC}"
  echo "  Commands: $COMMANDS"
  echo "  Agents: $AGENTS"
  echo "  Hooks: $HOOKS"
  echo "  Scripts: $SCRIPTS"
  
  # Check for critical files
  critical_files=(
    ".claude/commands/sr.md"
    ".claude/settings.json"
    ".claude/hooks/user-prompt-submit/01-tdd-suggester.py"
    ".claude/scripts/handle-agents-command-v3.sh"
  )
  
  MISSING=""
  for file in "${critical_files[@]}"; do
    if [ ! -f "$file" ] && [ ! -f "${file}.boilerplate" ]; then
      MISSING="$MISSING\n  ❌ Missing: $file"
    fi
  done
  
  if [ -n "$MISSING" ]; then
    echo -e "${YELLOW}⚠ Some critical files are missing:${NC}"
    echo -e "$MISSING"
  else
    echo -e "${GREEN}✓ All critical files present${NC}"
  fi
}

generate_report() {
  echo -e "${YELLOW}📄 Generating report...${NC}"
  
  if [ "$DRY_RUN" = true ]; then
    return
  fi
  
  cat > INTEGRATION_COMPLETE.md << EOF
# Claude Code Boilerplate Integration Complete! 🎉

## Installation Summary

**Date**: $(date)
**Version**: 4.1.0 (Complete)

### ✅ What Was Installed

#### Core System
- **Commands**: $COMMANDS custom commands in \`.claude/commands/\`
- **Agents**: $AGENTS AI agents in \`.claude/agents/\`
- **Hooks**: $HOOKS automation hooks in \`.claude/hooks/\`
- **Scripts**: $SCRIPTS support scripts in \`.claude/scripts/\`

#### Additional Features
- Agent OS standards in \`.agent-os/\`
- PRP templates in \`PRPs/\`
- Field registry security in \`field-registry/\`
- Component templates in \`templates/\`
- Documentation in \`docs/\`

### 🚀 Getting Started

1. **Open Claude Code:**
   \`\`\`bash
   claude .
   \`\`\`

2. **Load the system:**
   \`\`\`bash
   /sr
   \`\`\`

3. **Check available commands:**
   \`\`\`bash
   /help
   \`\`\`

### 📚 Essential Commands

- \`/sr\` - Smart Resume (context restoration)
- \`/cc\` - Create Component
- \`/vd\` - Validate Design
- \`/chain list\` - View workflow chains
- \`/orch\` - Orchestrate agents
- \`/create-prp\` - Create implementation guide
- \`/analyze-existing\` - Analyze your project

### 🔄 Backup Location

Your original files are backed up at:
\`$BACKUP_DIR\`

To rollback if needed:
\`\`\`bash
cp -r $BACKUP_DIR/* .
\`\`\`

### 📖 Documentation

- \`CLAUDE_BOILERPLATE.md\` - Main boilerplate guide
- \`QUICK_REFERENCE.md\` - Command reference
- \`.claude/commands/\` - Individual command docs
- \`docs/\` - Full documentation

---

**Ready to start!** Run \`claude .\` and type \`/sr\` to begin.
EOF
  
  echo -e "${GREEN}✓ Report saved to INTEGRATION_COMPLETE.md${NC}"
}

cleanup() {
  if [ "$DRY_RUN" = false ] && [ -d "$TEMP_DIR" ]; then
    echo -e "${YELLOW}🧹 Cleaning up...${NC}"
    rm -rf "$TEMP_DIR"
  fi
}

main() {
  print_header
  check_prerequisites
  
  echo -e "${CYAN}📍 Project directory: $PROJECT_DIR${NC}"
  echo ""
  
  download_complete_boilerplate
  create_backup
  
  integrate_claude_directory
  integrate_root_directories
  integrate_documentation
  integrate_config_files
  
  verify_integration
  generate_report
  cleanup
  
  echo ""
  echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${GREEN}  ✅ COMPLETE Integration Successful!${NC}"
  echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  echo -e "${CYAN}Next steps:${NC}"
  echo "1. Run: claude ."
  echo "2. Type: /sr"
  echo "3. Explore: /help"
  echo ""
  echo -e "${YELLOW}Tip: If any hooks fail, check that Python dependencies are installed.${NC}"
}

# Trap to ensure cleanup
trap cleanup EXIT

# Run main
main
