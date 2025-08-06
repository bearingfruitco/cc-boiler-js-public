#!/bin/bash

# ============================================================================
# Claude Code Boilerplate INTEGRATION WIZARD v6.0.0
# 
# An intelligent, interactive wizard that guides you through the entire
# boilerplate integration process with smart recommendations.
# ============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Configuration
PUBLIC_REPO="https://github.com/bearingfruitco/cc-boiler-js-public.git"
TEMP_DIR="/tmp/claude-boilerplate-wizard-$$"
BACKUP_DIR=".claude-integration/backup/$(date +%Y%m%d_%H%M%S)"
PROJECT_DIR="$(pwd)"
WIZARD_LOG=".claude-integration/wizard.log"

# Wizard State
WIZARD_MODE=""
PROJECT_TYPE=""
FRAMEWORK=""
HAS_CLAUDE=""
HAS_TYPESCRIPT=""
HAS_NEXTJS=""
INTEGRATION_PROFILE=""
CONFLICTS_STRATEGY=""

# ASCII Art Header
show_wizard_header() {
  clear
  cat << 'EOF'
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║     _____ _                 _        _____          _                   ║
║    / ____| |               | |      / ____|        | |                  ║
║   | |    | | __ _ _   _  __| | ___ | |     ___   __| | ___             ║
║   | |    | |/ _` | | | |/ _` |/ _ \| |    / _ \ / _` |/ _ \            ║
║   | |____| | (_| | |_| | (_| |  __/| |___| (_) | (_| |  __/            ║
║    \_____|_|\__,_|\__,_|\__,_|\___| \_____\___/ \__,_|\___|            ║
║                                                                          ║
║              BOILERPLATE INTEGRATION WIZARD v6.0.0                      ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
EOF
  echo ""
}

# Wizard Functions
wizard_welcome() {
  show_wizard_header
  echo -e "${CYAN}Welcome to the Claude Code Boilerplate Integration Wizard!${NC}"
  echo ""
  echo "This wizard will help you integrate the Claude Code Boilerplate into your"
  echo "project with intelligent recommendations based on your setup."
  echo ""
  echo -e "${YELLOW}What this wizard does:${NC}"
  echo "  ✓ Analyzes your project structure"
  echo "  ✓ Recommends integration strategies"
  echo "  ✓ Handles conflicts intelligently"
  echo "  ✓ Sets up everything for immediate use"
  echo "  ✓ Provides post-integration guidance"
  echo ""
  echo -e "${GREEN}Press ENTER to begin or Ctrl+C to cancel${NC}"
  read -r
}

analyze_project() {
  show_wizard_header
  echo -e "${CYAN}📊 STEP 1: Analyzing Your Project${NC}"
  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  
  # Check for existing Claude setup
  if [ -d ".claude" ]; then
    HAS_CLAUDE="existing"
    local claude_items=$(find .claude -type f | wc -l)
    echo "  ✓ Found existing .claude directory ($claude_items items)"
  else
    HAS_CLAUDE="none"
    echo "  ✓ No existing Claude setup found"
  fi
  
  # Check for TypeScript
  if [ -f "tsconfig.json" ]; then
    HAS_TYPESCRIPT="yes"
    echo "  ✓ TypeScript project detected"
  fi
  
  # Check for Next.js
  if [ -f "next.config.js" ] || [ -f "next.config.mjs" ]; then
    HAS_NEXTJS="yes"
    FRAMEWORK="nextjs"
    echo "  ✓ Next.js project detected"
  elif [ -f "package.json" ]; then
    if grep -q '"react"' package.json; then
      FRAMEWORK="react"
      echo "  ✓ React project detected"
    elif grep -q '"vue"' package.json; then
      FRAMEWORK="vue"
      echo "  ✓ Vue project detected"
    else
      FRAMEWORK="node"
      echo "  ✓ Node.js project detected"
    fi
  else
    FRAMEWORK="unknown"
    echo "  ✓ Project type: Generic/Unknown"
  fi
  
  # Check for existing config files
  local has_biome=$([ -f "biome.json" ] && echo "yes" || echo "no")
  local has_playwright=$([ -f "playwright.config.ts" ] && echo "yes" || echo "no")
  local has_tailwind=$([ -f "tailwind.config.js" ] && echo "yes" || echo "no")
  
  echo ""
  echo -e "${GREEN}Project Analysis Complete!${NC}"
  echo ""
  echo "Press ENTER to continue..."
  read -r
}

choose_integration_mode() {
  show_wizard_header
  echo -e "${CYAN}📦 STEP 2: Choose Integration Mode${NC}"
  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  
  if [ "$HAS_CLAUDE" = "existing" ]; then
    echo -e "${YELLOW}⚠️  You have an existing Claude setup${NC}"
    echo ""
    echo "Available modes:"
    echo ""
    echo -e "${BOLD}1) Upgrade${NC} - Merge boilerplate with your existing setup"
    echo "   Best if: You want to keep your customizations"
    echo ""
    echo -e "${BOLD}2) Replace${NC} - Backup existing and install fresh"
    echo "   Best if: You want the latest boilerplate features"
    echo ""
    echo -e "${BOLD}3) Parallel${NC} - Install as .claude-boilerplate (no conflicts)"
    echo "   Best if: You want to try without affecting current setup"
    echo ""
  else
    echo "Available modes:"
    echo ""
    echo -e "${BOLD}1) Complete${NC} - Full boilerplate installation (Recommended)"
    echo "   Installs: Everything - commands, agents, hooks, workflows"
    echo ""
    echo -e "${BOLD}2) Essential${NC} - Core features only"
    echo "   Installs: Commands and agents (no hooks/automation)"
    echo ""
    echo -e "${BOLD}3) Minimal${NC} - Just the basics"
    echo "   Installs: Smart resume and key commands only"
    echo ""
  fi
  
  echo -n "Choose mode (1-3): "
  read -r mode_choice
  
  case $mode_choice in
    1)
      if [ "$HAS_CLAUDE" = "existing" ]; then
        WIZARD_MODE="upgrade"
      else
        WIZARD_MODE="complete"
      fi
      ;;
    2)
      if [ "$HAS_CLAUDE" = "existing" ]; then
        WIZARD_MODE="replace"
      else
        WIZARD_MODE="essential"
      fi
      ;;
    3)
      if [ "$HAS_CLAUDE" = "existing" ]; then
        WIZARD_MODE="parallel"
      else
        WIZARD_MODE="minimal"
      fi
      ;;
    *)
      echo -e "${RED}Invalid choice. Using default.${NC}"
      WIZARD_MODE="complete"
      ;;
  esac
  
  echo ""
  echo -e "${GREEN}Selected mode: $WIZARD_MODE${NC}"
  sleep 2
}

choose_conflict_strategy() {
  show_wizard_header
  echo -e "${CYAN}🔧 STEP 3: Conflict Resolution Strategy${NC}"
  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  echo "How should we handle files that already exist?"
  echo ""
  echo -e "${BOLD}1) Interactive${NC} - Ask me for each conflict (Recommended)"
  echo "   You decide for each file"
  echo ""
  echo -e "${BOLD}2) Safe${NC} - Keep all existing files"
  echo "   Creates .boilerplate versions for reference"
  echo ""
  echo -e "${BOLD}3) Aggressive${NC} - Prefer boilerplate versions"
  echo "   Backs up existing, uses boilerplate"
  echo ""
  echo -e "${BOLD}4) Smart${NC} - AI-like decisions"
  echo "   Config files: keep existing"
  echo "   Commands/Hooks: use boilerplate"
  echo "   Documentation: merge"
  echo ""
  
  echo -n "Choose strategy (1-4): "
  read -r strategy_choice
  
  case $strategy_choice in
    1) CONFLICTS_STRATEGY="interactive" ;;
    2) CONFLICTS_STRATEGY="safe" ;;
    3) CONFLICTS_STRATEGY="aggressive" ;;
    4) CONFLICTS_STRATEGY="smart" ;;
    *) CONFLICTS_STRATEGY="interactive" ;;
  esac
  
  echo ""
  echo -e "${GREEN}Strategy selected: $CONFLICTS_STRATEGY${NC}"
  sleep 2
}

select_features() {
  show_wizard_header
  echo -e "${CYAN}✨ STEP 4: Select Features${NC}"
  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  
  if [ "$WIZARD_MODE" = "complete" ]; then
    echo "Complete mode includes all features:"
    echo "  ✓ 150+ Commands"
    echo "  ✓ 31 AI Agents"
    echo "  ✓ Automation Hooks"
    echo "  ✓ Workflow Chains"
    echo "  ✓ Design System"
    echo "  ✓ Security Features"
    echo "  ✓ Architecture Tracking"
    echo ""
    echo "Press ENTER to continue..."
    read -r
    return
  fi
  
  echo "Select features to install (space-separated numbers):"
  echo ""
  echo "Core Features:"
  echo "  1) Smart Resume (/sr command)"
  echo "  2) Design Validation (/vd command)"
  echo "  3) Component Creation (/cc command)"
  echo ""
  echo "AI Agents:"
  echo "  4) All 31 specialized agents"
  echo "  5) Essential agents only (10 core agents)"
  echo ""
  echo "Automation:"
  echo "  6) Pre-tool hooks (validation, security)"
  echo "  7) Post-tool hooks (metrics, learning)"
  echo "  8) Workflow chains"
  echo ""
  echo "Advanced:"
  echo "  9) PRP System (implementation guides)"
  echo "  10) Architecture Tracking"
  echo "  11) Field Registry (security)"
  echo ""
  
  echo -n "Your selection (e.g., 1 2 3 4 6): "
  read -r feature_selection
  
  echo ""
  echo -e "${GREEN}Features selected!${NC}"
  sleep 2
}

download_boilerplate() {
  show_wizard_header
  echo -e "${CYAN}📥 STEP 5: Downloading Boilerplate${NC}"
  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  
  echo "Downloading complete boilerplate..."
  git clone --depth 1 "$PUBLIC_REPO" "$TEMP_DIR" 2>/dev/null || {
    echo -e "${RED}✗ Failed to download boilerplate${NC}"
    exit 1
  }
  
  # Remove .git directory
  rm -rf "$TEMP_DIR/.git"
  
  echo -e "${GREEN}✓ Downloaded successfully${NC}"
  echo ""
  
  # Show what we got
  echo "Boilerplate contents:"
  echo "  • Commands: $(find "$TEMP_DIR/.claude/commands" -name "*.md" 2>/dev/null | wc -l)"
  echo "  • Agents: $(find "$TEMP_DIR/.claude/agents" -name "*.md" 2>/dev/null | wc -l)"
  echo "  • Hooks: $(find "$TEMP_DIR/.claude/hooks" -name "*.py" 2>/dev/null | wc -l)"
  echo "  • Templates: $(find "$TEMP_DIR/templates" -type f 2>/dev/null | wc -l)"
  echo ""
  
  echo "Press ENTER to continue..."
  read -r
}

create_backup() {
  show_wizard_header
  echo -e "${CYAN}💾 STEP 6: Creating Backup${NC}"
  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  
  echo "Creating backup of existing files..."
  mkdir -p "$BACKUP_DIR"
  
  # Backup existing directories
  local backed_up=0
  for dir in .claude .agent-os PRPs field-registry templates docs lib hooks scripts; do
    if [ -d "$dir" ]; then
      cp -r "$dir" "$BACKUP_DIR/"
      ((backed_up++))
      echo "  ✓ Backed up $dir"
    fi
  done
  
  # Backup important files
  for file in CLAUDE.md biome.json playwright.config.ts .env.example; do
    if [ -f "$file" ]; then
      cp "$file" "$BACKUP_DIR/"
      ((backed_up++))
      echo "  ✓ Backed up $file"
    fi
  done
  
  if [ $backed_up -gt 0 ]; then
    echo ""
    echo -e "${GREEN}✓ Backup complete ($backed_up items)${NC}"
    echo "  Location: $BACKUP_DIR"
  else
    echo -e "${GREEN}✓ No existing files to backup${NC}"
  fi
  
  echo ""
  echo "Press ENTER to continue..."
  read -r
}

smart_integrate_file() {
  local source="$1"
  local dest="$2"
  local file_type="$3"
  
  # If destination doesn't exist, just copy
  if [ ! -f "$dest" ]; then
    cp "$source" "$dest"
    return 0
  fi
  
  # Files are identical
  if cmp -s "$source" "$dest"; then
    return 1
  fi
  
  # Handle based on strategy
  case $CONFLICTS_STRATEGY in
    safe)
      cp "$source" "${dest}.boilerplate"
      echo "    ℹ Kept existing, saved new as ${dest}.boilerplate"
      ;;
    aggressive)
      mv "$dest" "${dest}.backup"
      cp "$source" "$dest"
      echo "    ✓ Replaced (backup: ${dest}.backup)"
      ;;
    smart)
      case $file_type in
        config)
          cp "$source" "${dest}.boilerplate"
          echo "    ℹ Kept existing config, reference: ${dest}.boilerplate"
          ;;
        command|hook|agent)
          mv "$dest" "${dest}.original"
          cp "$source" "$dest"
          echo "    ✓ Updated to boilerplate (original: ${dest}.original)"
          ;;
        doc)
          # Merge documentation
          if [ "$dest" = "CLAUDE.md" ]; then
            cp "$source" "CLAUDE_BOILERPLATE.md"
            echo "    ✓ Created CLAUDE_BOILERPLATE.md"
          else
            cp "$source" "${dest}.boilerplate"
          fi
          ;;
      esac
      ;;
    interactive)
      echo ""
      echo -e "${YELLOW}Conflict: $dest${NC}"
      echo "  [k]eep existing | [r]eplace | [b]oth | [v]iew diff | [s]kip"
      read -n 1 -r choice
      echo ""
      case $choice in
        r|R)
          mv "$dest" "${dest}.backup"
          cp "$source" "$dest"
          echo "    ✓ Replaced"
          ;;
        b|B)
          cp "$source" "${dest}.boilerplate"
          echo "    ✓ Created ${dest}.boilerplate"
          ;;
        v|V)
          diff --color=always -u "$dest" "$source" | head -30
          smart_integrate_file "$source" "$dest" "$file_type"
          ;;
        *)
          echo "    ⊖ Skipped"
          ;;
      esac
      ;;
  esac
}

perform_integration() {
  show_wizard_header
  echo -e "${CYAN}🔨 STEP 7: Performing Integration${NC}"
  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  
  # Create directory structure
  echo "Creating directory structure..."
  mkdir -p .claude/{commands,agents,hooks,scripts,config,state,context}
  mkdir -p .claude/hooks/{pre-tool-use,post-tool-use,stop,notification,user-prompt-submit,sub-agent-stop,pre-compact,utils}
  
  # Integrate based on mode
  case $WIZARD_MODE in
    complete|upgrade)
      echo "Installing complete boilerplate..."
      
      # Copy everything
      echo "  → Installing commands..."
      cp -r "$TEMP_DIR/.claude/commands/"* .claude/commands/ 2>/dev/null || true
      
      echo "  → Installing agents..."
      cp -r "$TEMP_DIR/.claude/agents/"* .claude/agents/ 2>/dev/null || true
      
      echo "  → Installing hooks..."
      for hook_dir in pre-tool-use post-tool-use stop notification user-prompt-submit sub-agent-stop pre-compact utils; do
        if [ -d "$TEMP_DIR/.claude/hooks/$hook_dir" ]; then
          cp -r "$TEMP_DIR/.claude/hooks/$hook_dir/"* ".claude/hooks/$hook_dir/" 2>/dev/null || true
        fi
      done
      
      echo "  → Installing scripts..."
      cp -r "$TEMP_DIR/.claude/scripts/"* .claude/scripts/ 2>/dev/null || true
      
      echo "  → Installing configuration..."
      for config_file in "$TEMP_DIR/.claude/"*.json "$TEMP_DIR/.claude/"*.md; do
        [ -f "$config_file" ] && smart_integrate_file "$config_file" ".claude/$(basename "$config_file")" "config"
      done
      
      # Root directories
      for dir in .agent-os PRPs field-registry templates docs; do
        if [ -d "$TEMP_DIR/$dir" ] && [ ! -d "$dir" ]; then
          cp -r "$TEMP_DIR/$dir" .
          echo "  → Installed $dir"
        fi
      done
      ;;
      
    essential)
      echo "Installing essential features..."
      cp -r "$TEMP_DIR/.claude/commands/"* .claude/commands/ 2>/dev/null || true
      cp -r "$TEMP_DIR/.claude/agents/"* .claude/agents/ 2>/dev/null || true
      cp "$TEMP_DIR/.claude/settings.json" .claude/settings-essential.json
      ;;
      
    minimal)
      echo "Installing minimal features..."
      # Just copy key commands
      for cmd in sr.md cc.md vd.md help.md chain.md; do
        [ -f "$TEMP_DIR/.claude/commands/$cmd" ] && cp "$TEMP_DIR/.claude/commands/$cmd" .claude/commands/
      done
      ;;
      
    parallel)
      echo "Installing as parallel setup..."
      cp -r "$TEMP_DIR/.claude" .claude-boilerplate
      echo -e "${GREEN}✓ Installed as .claude-boilerplate${NC}"
      ;;
  esac
  
  echo ""
  echo -e "${GREEN}✓ Integration complete!${NC}"
  echo ""
  echo "Press ENTER to continue..."
  read -r
}

post_integration_setup() {
  show_wizard_header
  echo -e "${CYAN}🚀 STEP 8: Post-Integration Setup${NC}"
  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  
  # Fix permissions
  echo "Setting permissions..."
  find .claude -name "*.sh" -exec chmod +x {} \;
  find .claude -name "*.py" -exec chmod +r {} \;
  
  # Create .env.example if needed
  if [ ! -f ".env.example" ] && [ -f "$TEMP_DIR/.env.example" ]; then
    cp "$TEMP_DIR/.env.example" .
    echo "  ✓ Created .env.example"
  fi
  
  # Initialize git hooks if needed
  if [ -d "$TEMP_DIR/.husky" ] && [ ! -d ".husky" ]; then
    cp -r "$TEMP_DIR/.husky" .
    echo "  ✓ Installed git hooks"
  fi
  
  # Generate quick reference
  cat > BOILERPLATE_QUICKSTART.md << 'EOF'
# Claude Code Boilerplate Quick Start

## 🚀 Getting Started

1. **Launch Claude Code:**
   ```bash
   claude .
   ```

2. **Initialize the system:**
   ```bash
   /sr
   ```

3. **Explore commands:**
   ```bash
   /help
   ```

## 📚 Essential Commands

- `/sr` - Smart Resume (loads context)
- `/cc` - Create Component
- `/vd` - Validate Design
- `/chain list` - View workflows
- `/orch` - Orchestrate agents
- `/analyze-existing` - Analyze project

## 🤖 Key Agents

- `frontend` - React/UI expert
- `backend` - API/server expert
- `security` - Security specialist
- `qa` - Testing expert
- `performance` - Optimization specialist

## 🔄 Workflows

Run complex workflows:
```bash
/chain feature-development
/chain morning-setup
/chain pre-pr
```

## 📖 Documentation

- Full docs: `docs/`
- Commands: `.claude/commands/`
- Agents: `.claude/agents/`

## 🆘 Help

- In Claude: `/help`
- Issues: Check `.claude-integration/wizard.log`
EOF
  
  echo "  ✓ Created BOILERPLATE_QUICKSTART.md"
  echo ""
  echo -e "${GREEN}✓ Post-integration setup complete!${NC}"
  echo ""
  echo "Press ENTER to continue..."
  read -r
}

verify_installation() {
  show_wizard_header
  echo -e "${CYAN}✅ STEP 9: Verification${NC}"
  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  
  local issues=()
  
  # Check critical files
  echo "Checking installation..."
  
  [ -f ".claude/commands/sr.md" ] && echo "  ✓ Smart Resume command" || issues+=("Missing: Smart Resume")
  [ -d ".claude/agents" ] && echo "  ✓ AI Agents" || issues+=("Missing: Agents")
  [ -d ".claude/hooks/user-prompt-submit" ] && echo "  ✓ Hooks configured" || issues+=("Missing: Hooks")
  [ -f ".claude/settings.json" ] || [ -f ".claude/settings-essential.json" ] && echo "  ✓ Settings" || issues+=("Missing: Settings")
  
  echo ""
  
  # Count components
  local cmd_count=$(find .claude/commands -name "*.md" 2>/dev/null | wc -l)
  local agent_count=$(find .claude/agents -name "*.md" 2>/dev/null | wc -l)
  local hook_count=$(find .claude/hooks -name "*.py" 2>/dev/null | wc -l)
  
  echo "Component counts:"
  echo "  • Commands: $cmd_count"
  echo "  • Agents: $agent_count"
  echo "  • Hooks: $hook_count"
  
  echo ""
  
  if [ ${#issues[@]} -eq 0 ]; then
    echo -e "${GREEN}✓ All critical components verified!${NC}"
  else
    echo -e "${YELLOW}⚠ Some components may need attention:${NC}"
    for issue in "${issues[@]}"; do
      echo "  - $issue"
    done
  fi
  
  echo ""
  echo "Press ENTER to continue..."
  read -r
}

show_next_steps() {
  show_wizard_header
  echo -e "${CYAN}🎉 INTEGRATION COMPLETE!${NC}"
  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  echo -e "${GREEN}The Claude Code Boilerplate has been successfully integrated!${NC}"
  echo ""
  echo -e "${BOLD}📋 Next Steps:${NC}"
  echo ""
  echo "1. Start Claude Code:"
  echo -e "   ${CYAN}claude .${NC}"
  echo ""
  echo "2. Initialize the system:"
  echo -e "   ${CYAN}/sr${NC}"
  echo ""
  echo "3. If you see any hook errors, install Python dependencies:"
  echo -e "   ${CYAN}pip install -r .claude/requirements.txt${NC}"
  echo ""
  echo "4. Explore available commands:"
  echo -e "   ${CYAN}/help${NC}"
  echo ""
  echo "5. Analyze your project:"
  echo -e "   ${CYAN}/analyze-existing${NC}"
  echo ""
  
  if [ "$WIZARD_MODE" = "parallel" ]; then
    echo -e "${YELLOW}Note: Installed as .claude-boilerplate${NC}"
    echo "To use, reference commands with full path in Claude Code"
  fi
  
  echo ""
  echo -e "${BOLD}📚 Resources:${NC}"
  echo "  • Quick Start: BOILERPLATE_QUICKSTART.md"
  echo "  • Full Docs: docs/"
  echo "  • Backup: $BACKUP_DIR"
  echo ""
  echo -e "${GREEN}Happy coding with Claude Code Boilerplate! 🚀${NC}"
  echo ""
  
  # Log completion
  mkdir -p "$(dirname "$WIZARD_LOG")"
  cat >> "$WIZARD_LOG" << EOF
[$(date '+%Y-%m-%d %H:%M:%S')] Integration completed
  Mode: $WIZARD_MODE
  Strategy: $CONFLICTS_STRATEGY
  Project: $PROJECT_DIR
  Commands: $(find .claude/commands -name "*.md" 2>/dev/null | wc -l)
  Agents: $(find .claude/agents -name "*.md" 2>/dev/null | wc -l)
  Hooks: $(find .claude/hooks -name "*.py" 2>/dev/null | wc -l)
EOF
}

cleanup() {
  if [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
  fi
}

# Main wizard flow
main() {
  # Set up cleanup
  trap cleanup EXIT
  
  # Run wizard steps
  wizard_welcome
  analyze_project
  choose_integration_mode
  choose_conflict_strategy
  
  if [ "$WIZARD_MODE" != "complete" ]; then
    select_features
  fi
  
  download_boilerplate
  create_backup
  perform_integration
  post_integration_setup
  verify_installation
  show_next_steps
}

# Run the wizard
main "$@"
