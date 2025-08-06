#!/bin/bash

# ============================================================================
# Claude Code Boilerplate INTELLIGENT Integration Script v5.0.0
# 
# This script properly downloads and integrates the ENTIRE boilerplate with:
# - Complete download of ALL files
# - Diff comparison for conflicts
# - Interactive merge options
# - No overwrites without consent
# - Comprehensive directory coverage
# ============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
PUBLIC_REPO="https://github.com/bearingfruitco/cc-boiler-js-public.git"
TEMP_DIR="/tmp/claude-boilerplate-full-$$"
BACKUP_DIR=".claude-integration/backup/$(date +%Y%m%d_%H%M%S)"
PROJECT_DIR="$(pwd)"
INTEGRATION_LOG="$PROJECT_DIR/.claude-integration/integration.log"

# Parse arguments
DRY_RUN=false
AUTO_MERGE=false
VERBOSE=false
INTERACTIVE=true

for arg in "$@"; do
  case $arg in
    --dry-run)
      DRY_RUN=true
      echo -e "${YELLOW}DRY RUN MODE - No changes will be made${NC}"
      ;;
    --auto)
      AUTO_MERGE=true
      INTERACTIVE=false
      ;;
    --verbose)
      VERBOSE=true
      ;;
    --help)
      cat << EOF
Usage: $0 [options]

Options:
  --dry-run    Show what would happen without making changes
  --auto       Auto-merge non-conflicting files (no prompts)
  --verbose    Show detailed progress
  --help       Show this help message

Integration Modes:
  Default: Interactive - prompts for conflicts
  Auto: Automatically integrates non-conflicting files
  Dry Run: Shows what would be done without changes

EOF
      exit 0
      ;;
  esac
done

# Functions
print_header() {
  echo ""
  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${BLUE}  Claude Code Boilerplate INTELLIGENT Integration v5.0.0${NC}"
  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
}

log_action() {
  mkdir -p "$(dirname "$INTEGRATION_LOG")"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$INTEGRATION_LOG"
}

check_prerequisites() {
  echo -e "${YELLOW}📋 Checking prerequisites...${NC}"
  
  # Required tools
  local missing_tools=()
  
  command -v git &> /dev/null || missing_tools+=("git")
  command -v python3 &> /dev/null || missing_tools+=("python3")
  command -v diff &> /dev/null || missing_tools+=("diff")
  
  if [ ${#missing_tools[@]} -gt 0 ]; then
    echo -e "${RED}✗ Missing required tools: ${missing_tools[*]}${NC}"
    echo "Please install them and try again."
    exit 1
  fi
  
  echo -e "${GREEN}✓ All prerequisites satisfied${NC}"
}

download_entire_boilerplate() {
  echo -e "${YELLOW}📥 Downloading COMPLETE boilerplate...${NC}"
  
  if [ "$DRY_RUN" = true ]; then
    echo "  [DRY RUN] Would clone entire repo to $TEMP_DIR"
    return
  fi
  
  # Clone the entire repository with all files
  echo "  Cloning repository..."
  git clone --depth 1 "$PUBLIC_REPO" "$TEMP_DIR" 2>/dev/null || {
    echo -e "${RED}✗ Failed to download boilerplate${NC}"
    exit 1
  }
  
  # Remove .git directory from temp
  rm -rf "$TEMP_DIR/.git"
  
  echo -e "${GREEN}✓ Downloaded complete boilerplate${NC}"
  
  # Show comprehensive summary
  echo -e "${CYAN}📊 Boilerplate Contents Summary:${NC}"
  echo "  Root directories: $(find "$TEMP_DIR" -maxdepth 1 -type d | wc -l)"
  echo "  .claude structure:"
  echo "    - Commands: $(find "$TEMP_DIR/.claude/commands" -name "*.md" 2>/dev/null | wc -l) files"
  echo "    - Agents: $(find "$TEMP_DIR/.claude/agents" -name "*.md" 2>/dev/null | wc -l) files"
  echo "    - Hooks: $(find "$TEMP_DIR/.claude/hooks" -name "*.py" 2>/dev/null | wc -l) Python files"
  echo "    - Scripts: $(find "$TEMP_DIR/.claude/scripts" -name "*.sh" 2>/dev/null | wc -l) shell scripts"
  echo "    - Config: $(find "$TEMP_DIR/.claude/config" -type f 2>/dev/null | wc -l) files"
  echo "  Other key directories:"
  echo "    - PRPs: $(find "$TEMP_DIR/PRPs" -type f 2>/dev/null | wc -l) files"
  echo "    - Templates: $(find "$TEMP_DIR/templates" -type f 2>/dev/null | wc -l) files"
  echo "    - Lib utilities: $(find "$TEMP_DIR/lib" -maxdepth 1 -type d 2>/dev/null | wc -l) modules"
}

create_comprehensive_backup() {
  echo -e "${YELLOW}💾 Creating comprehensive backup...${NC}"
  
  if [ "$DRY_RUN" = true ]; then
    echo "  [DRY RUN] Would backup existing files to $BACKUP_DIR"
    return
  fi
  
  mkdir -p "$BACKUP_DIR"
  
  # Backup ALL directories that might be modified
  local dirs_to_backup=(
    ".claude"
    ".agent-os"
    ".husky"
    "PRPs"
    "field-registry"
    "templates"
    "lib"
    "hooks"
    "scripts"
    "docs"
    "config"
    "stores"
    "types"
  )
  
  for dir in "${dirs_to_backup[@]}"; do
    if [ -d "$dir" ]; then
      cp -r "$dir" "$BACKUP_DIR/"
      echo "  ✓ Backed up $dir"
    fi
  done
  
  # Backup important files
  local files_to_backup=(
    "CLAUDE.md"
    "biome.json"
    "playwright.config.ts"
    ".env.example"
    ".coderabbit.yaml"
    "components.json"
    "tsconfig.json"
    "tailwind.config.js"
  )
  
  for file in "${files_to_backup[@]}"; do
    if [ -f "$file" ]; then
      cp "$file" "$BACKUP_DIR/"
      echo "  ✓ Backed up $file"
    fi
  done
  
  echo -e "${GREEN}✓ Comprehensive backup created at $BACKUP_DIR${NC}"
  log_action "Backup created at $BACKUP_DIR"
}

show_diff_and_merge() {
  local source_file="$1"
  local dest_file="$2"
  local file_type="$3"
  
  if [ ! -f "$dest_file" ]; then
    # File doesn't exist, safe to copy
    return 0
  fi
  
  # Check if files are identical
  if cmp -s "$source_file" "$dest_file"; then
    [ "$VERBOSE" = true ] && echo "    ℹ Files are identical, skipping"
    return 1
  fi
  
  # Files differ
  if [ "$AUTO_MERGE" = true ]; then
    # In auto mode, create .boilerplate version
    cp "$source_file" "${dest_file}.boilerplate"
    echo "    ⚠ Conflict: saved as ${dest_file}.boilerplate"
    return 1
  fi
  
  if [ "$INTERACTIVE" = true ] && [ "$DRY_RUN" = false ]; then
    echo -e "${YELLOW}  ⚠ Conflict detected: $dest_file${NC}"
    echo "  Differences:"
    diff --color=always -u "$dest_file" "$source_file" | head -20 || true
    echo ""
    echo "  Options:"
    echo "  [k]eep existing | [r]eplace | [b]oth (create .boilerplate) | [s]kip"
    read -p "  Choose: " -n 1 choice
    echo ""
    
    case $choice in
      r|R)
        return 0  # Replace
        ;;
      b|B)
        cp "$source_file" "${dest_file}.boilerplate"
        echo "    Created ${dest_file}.boilerplate"
        return 1
        ;;
      k|K|s|S|*)
        return 1  # Keep/Skip
        ;;
    esac
  fi
  
  return 1
}

integrate_claude_directory_complete() {
  echo -e "${YELLOW}📦 Integrating .claude directory (COMPLETE)...${NC}"
  
  if [ "$DRY_RUN" = true ]; then
    echo "  [DRY RUN] Would integrate complete .claude directory with all subdirectories"
    return
  fi
  
  # Create ALL necessary subdirectories first
  local claude_dirs=(
    "commands"
    "agents"
    "config"
    "scripts"
    "hooks/pre-tool-use"
    "hooks/post-tool-use"
    "hooks/stop"
    "hooks/notification"
    "hooks/user-prompt-submit"
    "hooks/sub-agent-stop"
    "hooks/pre-compact"
    "hooks/utils"
    "state"
    "context"
    "logs"
    "metrics"
    "analytics"
    "specs"
    "profiles"
    "personas"
    "dependencies"
    "deployment"
    "branch-state"
    "bugs"
    "collab"
    "handoff"
    "playwright"
    "release"
    "requirements"
    "research"
    "snapshots"
    "team"
    "templates"
    "transcripts"
    "utils"
    "doc-cache"
    "backups"
  )
  
  for dir in "${claude_dirs[@]}"; do
    mkdir -p ".claude/$dir"
  done
  
  # Copy EVERYTHING from .claude
  echo "  📝 Processing .claude contents..."
  
  # Use rsync for intelligent copying if available
  if command -v rsync &> /dev/null; then
    rsync -av --ignore-existing "$TEMP_DIR/.claude/" ".claude/" 2>/dev/null | grep -v "^$" | while read line; do
      [ "$VERBOSE" = true ] && echo "    $line"
    done
    
    # Handle conflicts
    find "$TEMP_DIR/.claude" -type f | while read source_file; do
      rel_path="${source_file#$TEMP_DIR/.claude/}"
      dest_file=".claude/$rel_path"
      
      if [ -f "$dest_file" ]; then
        if ! cmp -s "$source_file" "$dest_file"; then
          if show_diff_and_merge "$source_file" "$dest_file" "claude"; then
            cp "$source_file" "$dest_file"
            echo "    ✓ Updated: $rel_path"
          fi
        fi
      else
        cp --parents "$source_file" . 2>/dev/null || cp "$source_file" "$dest_file"
        [ "$VERBOSE" = true ] && echo "    ✓ Added: $rel_path"
      fi
    done
  else
    # Fallback to cp -r
    cp -rn "$TEMP_DIR/.claude/"* ".claude/" 2>/dev/null || true
    
    # Handle conflicts manually
    for item in "$TEMP_DIR/.claude/"*; do
      basename=$(basename "$item")
      if [ -e ".claude/$basename" ]; then
        if [ -f "$item" ]; then
          if show_diff_and_merge "$item" ".claude/$basename" "claude"; then
            cp "$item" ".claude/$basename"
          fi
        fi
      else
        cp -r "$item" ".claude/"
      fi
    done
  fi
  
  echo -e "${GREEN}✓ Complete .claude directory integrated${NC}"
}

integrate_root_level_items() {
  echo -e "${YELLOW}📁 Integrating root-level directories and files...${NC}"
  
  if [ "$DRY_RUN" = true ]; then
    echo "  [DRY RUN] Would process all root-level items"
    return
  fi
  
  # Critical directories to integrate
  local critical_dirs=(
    ".agent-os"
    "PRPs"
    "field-registry"
    "templates"
    "docs"
  )
  
  for dir in "${critical_dirs[@]}"; do
    if [ -d "$TEMP_DIR/$dir" ]; then
      if [ ! -d "$dir" ]; then
        cp -r "$TEMP_DIR/$dir" .
        echo -e "${GREEN}  ✓ Installed $dir${NC}"
      else
        echo "  ⚠ $dir exists - creating ${dir}.boilerplate for reference"
        cp -r "$TEMP_DIR/$dir" "${dir}.boilerplate"
      fi
    fi
  done
  
  # Merge lib directory (don't overwrite existing)
  if [ -d "$TEMP_DIR/lib" ]; then
    echo "  📚 Merging lib directory..."
    for libdir in "$TEMP_DIR"/lib/*; do
      if [ -d "$libdir" ]; then
        dirname=$(basename "$libdir")
        if [ ! -d "lib/$dirname" ]; then
          mkdir -p lib
          cp -r "$libdir" lib/
          echo "    ✓ Added lib/$dirname"
        else
          [ "$VERBOSE" = true ] && echo "    ℹ lib/$dirname exists, skipping"
        fi
      fi
    done
  fi
  
  # Handle hooks directory
  if [ -d "$TEMP_DIR/hooks" ] && [ ! -d "hooks" ]; then
    cp -r "$TEMP_DIR/hooks" .
    echo -e "${GREEN}  ✓ Installed hooks directory${NC}"
  fi
  
  # Handle stores directory
  if [ -d "$TEMP_DIR/stores" ] && [ ! -d "stores" ]; then
    cp -r "$TEMP_DIR/stores" .
    echo -e "${GREEN}  ✓ Installed stores directory${NC}"
  fi
  
  # Handle types directory
  if [ -d "$TEMP_DIR/types" ] && [ ! -d "types" ]; then
    cp -r "$TEMP_DIR/types" .
    echo -e "${GREEN}  ✓ Installed types directory${NC}"
  fi
  
  # Handle scripts directory
  if [ -d "$TEMP_DIR/scripts" ]; then
    if [ ! -d "scripts" ]; then
      cp -r "$TEMP_DIR/scripts" .
      echo -e "${GREEN}  ✓ Installed scripts directory${NC}"
    else
      echo "  📜 Merging scripts directory..."
      for script in "$TEMP_DIR"/scripts/*; do
        basename=$(basename "$script")
        if [ ! -f "scripts/$basename" ]; then
          cp "$script" scripts/
          [ "$VERBOSE" = true ] && echo "    ✓ Added $basename"
        fi
      done
    fi
  fi
}

integrate_config_files() {
  echo -e "${YELLOW}⚙️ Integrating configuration files...${NC}"
  
  if [ "$DRY_RUN" = true ]; then
    echo "  [DRY RUN] Would handle all config files"
    return
  fi
  
  # Config files with special handling
  local config_files=(
    "biome.json"
    "playwright.config.ts"
    ".env.example"
    "components.json"
    ".coderabbit.yaml"
    "drizzle.config.ts"
    "tailwind.config.js"
    "tsconfig.json"
    "next.config.js"
    "postcss.config.js"
  )
  
  for config in "${config_files[@]}"; do
    if [ -f "$TEMP_DIR/$config" ]; then
      if [ -f "$config" ]; then
        if show_diff_and_merge "$TEMP_DIR/$config" "$config" "config"; then
          cp "$TEMP_DIR/$config" "$config"
          echo -e "${GREEN}  ✓ Updated $config${NC}"
        else
          cp "$TEMP_DIR/$config" "${config}.boilerplate"
          echo "  ℹ Created ${config}.boilerplate for reference"
        fi
      else
        cp "$TEMP_DIR/$config" "$config"
        echo -e "${GREEN}  ✓ Installed $config${NC}"
      fi
    fi
  done
  
  # Git hooks (.husky)
  if [ -d "$TEMP_DIR/.husky" ]; then
    if [ ! -d ".husky" ]; then
      cp -r "$TEMP_DIR/.husky" .
      echo -e "${GREEN}  ✓ Installed git hooks (.husky)${NC}"
    else
      echo "  ℹ .husky exists, skipping"
    fi
  fi
}

integrate_documentation() {
  echo -e "${YELLOW}📚 Integrating documentation...${NC}"
  
  if [ "$DRY_RUN" = true ]; then
    echo "  [DRY RUN] Would handle documentation files"
    return
  fi
  
  # Handle CLAUDE.md specially
  if [ -f "$TEMP_DIR/CLAUDE.md" ]; then
    if [ -f "CLAUDE.md" ]; then
      # Show diff and let user decide
      if show_diff_and_merge "$TEMP_DIR/CLAUDE.md" "CLAUDE.md" "doc"; then
        cp "$TEMP_DIR/CLAUDE.md" "CLAUDE.md"
        echo -e "${GREEN}  ✓ Updated CLAUDE.md${NC}"
      else
        cp "$TEMP_DIR/CLAUDE.md" "CLAUDE_BOILERPLATE.md"
        echo -e "${GREEN}  ✓ Created CLAUDE_BOILERPLATE.md${NC}"
        
        # Add integration notice to existing CLAUDE.md
        if ! grep -q "Boilerplate Integration" CLAUDE.md; then
          cat >> CLAUDE.md << 'EOF'

---

## 🚀 Claude Code Boilerplate v5.0.0 Integration

This project has been enhanced with the COMPLETE Claude Code Boilerplate.

### ✨ Integrated Features:
- **150+ Commands**: `/sr`, `/vd`, `/cc`, `/chain`, `/orch`, etc.
- **31 AI Agents**: Specialized experts for every task
- **Automated Workflows**: Hooks, chains, and orchestration
- **Design System**: Enforced standards and validation
- **Architecture Tracking**: Complete decision history
- **Security Features**: Field registry, PII protection

See `CLAUDE_BOILERPLATE.md` for complete boilerplate documentation.

### 🚀 Quick Start:
1. Run: `claude .`
2. Type: `/sr` (Smart Resume)
3. Explore: `/help` (All commands)

EOF
        fi
      fi
    else
      cp "$TEMP_DIR/CLAUDE.md" "CLAUDE.md"
      echo -e "${GREEN}  ✓ Installed CLAUDE.md${NC}"
    fi
  fi
  
  # Copy other documentation files
  local doc_files=(
    "README.md"
    "QUICK_REFERENCE.md"
    "CONTRIBUTING.md"
    "CHANGELOG.md"
  )
  
  for doc in "${doc_files[@]}"; do
    if [ -f "$TEMP_DIR/$doc" ] && [ ! -f "$doc" ]; then
      cp "$TEMP_DIR/$doc" .
      echo -e "${GREEN}  ✓ Installed $doc${NC}"
    elif [ -f "$TEMP_DIR/$doc" ] && [ -f "$doc" ]; then
      cp "$TEMP_DIR/$doc" "${doc}.boilerplate"
      [ "$VERBOSE" = true ] && echo "  ℹ Created ${doc}.boilerplate for reference"
    fi
  done
}

verify_integration() {
  echo -e "${YELLOW}🔍 Verifying integration completeness...${NC}"
  
  if [ "$DRY_RUN" = true ]; then
    return
  fi
  
  local issues=()
  
  # Check critical directories
  [ ! -d ".claude/commands" ] && issues+=("Missing: .claude/commands")
  [ ! -d ".claude/agents" ] && issues+=("Missing: .claude/agents")
  [ ! -d ".claude/hooks/user-prompt-submit" ] && issues+=("Missing: .claude/hooks/user-prompt-submit")
  [ ! -d ".claude/scripts" ] && issues+=("Missing: .claude/scripts")
  [ ! -d ".agent-os" ] && [ ! -d ".agent-os.boilerplate" ] && issues+=("Missing: .agent-os")
  
  # Check critical files
  [ ! -f ".claude/settings.json" ] && [ ! -f ".claude/settings.boilerplate.json" ] && issues+=("Missing: .claude/settings.json")
  [ ! -f ".claude/commands/sr.md" ] && issues+=("Missing: Smart Resume command")
  
  # Count what we have
  local cmd_count=$(find .claude/commands -name "*.md" 2>/dev/null | wc -l)
  local agent_count=$(find .claude/agents -name "*.md" 2>/dev/null | wc -l)
  local hook_count=$(find .claude/hooks -name "*.py" 2>/dev/null | wc -l)
  local script_count=$(find .claude/scripts -name "*.sh" 2>/dev/null | wc -l)
  
  echo -e "${CYAN}📊 Integration Summary:${NC}"
  echo "  Commands: $cmd_count (expected: 150+)"
  echo "  Agents: $agent_count (expected: 31)"
  echo "  Hooks: $hook_count (expected: 80+)"
  echo "  Scripts: $script_count (expected: 20+)"
  
  if [ ${#issues[@]} -gt 0 ]; then
    echo -e "${YELLOW}⚠ Some items may need attention:${NC}"
    for issue in "${issues[@]}"; do
      echo "  - $issue"
    done
  else
    echo -e "${GREEN}✓ All critical components present${NC}"
  fi
  
  # Check if hooks will work
  if [ -f ".claude/settings.json" ]; then
    local missing_hooks=$(grep -o '\.claude/hooks/[^"]*\.py' .claude/settings.json | while read hook; do
      [ ! -f "$hook" ] && echo "$hook"
    done)
    
    if [ -n "$missing_hooks" ]; then
      echo -e "${YELLOW}⚠ Some configured hooks are missing:${NC}"
      echo "$missing_hooks" | head -5
    fi
  fi
}

generate_integration_report() {
  echo -e "${YELLOW}📄 Generating integration report...${NC}"
  
  if [ "$DRY_RUN" = true ]; then
    return
  fi
  
  cat > INTEGRATION_REPORT.md << EOF
# Claude Code Boilerplate Integration Report

**Date**: $(date)
**Version**: 5.0.0 (Complete)
**Mode**: $([ "$AUTO_MERGE" = true ] && echo "Automatic" || echo "Interactive")

## 📊 Integration Summary

### Components Installed
- **Commands**: $(find .claude/commands -name "*.md" 2>/dev/null | wc -l) files
- **Agents**: $(find .claude/agents -name "*.md" 2>/dev/null | wc -l) AI specialists
- **Hooks**: $(find .claude/hooks -name "*.py" 2>/dev/null | wc -l) automation scripts
- **Scripts**: $(find .claude/scripts -name "*.sh" 2>/dev/null | wc -l) support scripts

### Directories Created/Updated
$(find . -maxdepth 2 -type d -name "*boilerplate*" | while read dir; do
  echo "- $dir (conflict - saved as .boilerplate)"
done)

### Files with Conflicts
$(find . -maxdepth 2 -name "*.boilerplate" -type f | while read file; do
  echo "- $file"
done)

## 🚀 Getting Started

### 1. Launch Claude Code
\`\`\`bash
claude .
\`\`\`

### 2. Initialize System
\`\`\`bash
/sr
\`\`\`

### 3. Verify Installation
\`\`\`bash
/help
\`\`\`

## 📚 Key Commands Available

- \`/sr\` - Smart Resume (loads context)
- \`/cc\` - Create Component
- \`/vd\` - Validate Design
- \`/chain list\` - View workflow chains
- \`/orch\` - Orchestrate agents
- \`/analyze-existing\` - Analyze your project
- \`/create-prp\` - Create implementation guide

## 🔄 Backup Information

**Backup Location**: \`$BACKUP_DIR\`

To rollback if needed:
\`\`\`bash
rm -rf .claude .agent-os PRPs field-registry templates
cp -r $BACKUP_DIR/* .
\`\`\`

## 📝 Next Steps

1. Review any \`.boilerplate\` files for manual merging
2. Test the integration with \`/sr\` command
3. Run \`/analyze-existing\` to understand your project
4. Start building with \`/fw start\`

## 📖 Documentation

- Main guide: \`CLAUDE_BOILERPLATE.md\`
- Commands: \`.claude/commands/\`
- Agents: \`.claude/agents/\`
- Full docs: \`docs/\`

---

**Integration Log**: \`.claude-integration/integration.log\`
EOF
  
  echo -e "${GREEN}✓ Report saved to INTEGRATION_REPORT.md${NC}"
}

cleanup() {
  if [ "$DRY_RUN" = false ] && [ -d "$TEMP_DIR" ]; then
    echo -e "${YELLOW}🧹 Cleaning up temporary files...${NC}"
    rm -rf "$TEMP_DIR"
  fi
}

main() {
  print_header
  check_prerequisites
  
  echo -e "${CYAN}📍 Integrating into: $PROJECT_DIR${NC}"
  echo -e "${CYAN}📦 Mode: $([ "$DRY_RUN" = true ] && echo "Dry Run" || ([ "$AUTO_MERGE" = true ] && echo "Automatic" || echo "Interactive"))${NC}"
  echo ""
  
  # Main integration flow
  download_entire_boilerplate
  create_comprehensive_backup
  
  # Integrate everything
  integrate_claude_directory_complete
  integrate_root_level_items
  integrate_config_files
  integrate_documentation
  
  # Verify and report
  verify_integration
  generate_integration_report
  cleanup
  
  # Final summary
  echo ""
  echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${GREEN}  ✅ INTELLIGENT Integration Complete!${NC}"
  echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  
  if [ "$DRY_RUN" = false ]; then
    echo -e "${CYAN}Ready to use! Next steps:${NC}"
    echo "1. Run: claude ."
    echo "2. Type: /sr"
    echo "3. Enjoy your enhanced development environment!"
    echo ""
    
    if [ $(find . -name "*.boilerplate" | wc -l) -gt 0 ]; then
      echo -e "${YELLOW}Note: Review .boilerplate files for manual merging${NC}"
    fi
  fi
  
  log_action "Integration completed successfully"
}

# Trap to ensure cleanup
trap cleanup EXIT

# Run main
main "$@"
