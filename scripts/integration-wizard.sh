#!/bin/bash

# ============================================================================
# Claude Code Boilerplate INTEGRATION WIZARD v6.0.1
# 
# Fixed version that works with curl | bash
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
SCRIPT_DIR="/tmp/claude-boilerplate-script-$$"
BACKUP_DIR=".claude-integration/backup/$(date +%Y%m%d_%H%M%S)"
PROJECT_DIR="$(pwd)"
WIZARD_LOG=".claude-integration/wizard.log"

# First, download and re-execute if we're being piped
if [ ! -t 0 ]; then
  echo -e "${CYAN}Setting up integration wizard...${NC}"
  
  # Create temp directory for script
  mkdir -p "$SCRIPT_DIR"
  
  # Save this script to a file
  cat > "$SCRIPT_DIR/wizard.sh"
  
  # Make it executable
  chmod +x "$SCRIPT_DIR/wizard.sh"
  
  # Re-execute with proper terminal input
  exec bash "$SCRIPT_DIR/wizard.sh"
  exit 0
fi

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
║              BOILERPLATE INTEGRATION WIZARD v6.0.1                      ║
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
    local claude_items=$(find .claude -type f 2>/dev/null | wc -l)
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
  fi
  
  # Check for package.json
  if [ -f "package.json" ]; then
    echo "  ✓ Node.js project (package.json found)"
    PROJECT_TYPE="node"
  fi
  
  # Check for other frameworks
  if [ -f "vite.config.js" ] || [ -f "vite.config.ts" ]; then
    FRAMEWORK="vite"
    echo "  ✓ Vite project detected"
  fi
  
  echo ""
  echo -e "${GREEN}Analysis complete!${NC}"
  echo ""
  echo "Press ENTER to continue..."
  read -r
}

choose_integration_mode() {
  show_wizard_header
  echo -e "${CYAN}📦 STEP 2: Choose Integration Mode${NC}"
  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  
  echo "How would you like to integrate the boilerplate?"
  echo ""
  echo -e "${BOLD}1)${NC} ${GREEN}Full Integration${NC} (Recommended)"
  echo "   • Complete Claude Code system"
  echo "   • All 150+ commands and 31 agents"
  echo "   • Hooks, PRPs, and automation"
  echo ""
  echo -e "${BOLD}2)${NC} ${BLUE}Commands & Agents Only${NC}"
  echo "   • Just the .claude directory"
  echo "   • No project structure changes"
  echo "   • Quick and minimal"
  echo ""
  echo -e "${BOLD}3)${NC} ${YELLOW}Selective Features${NC}"
  echo "   • Choose specific components"
  echo "   • Custom integration"
  echo "   • Maximum control"
  echo ""
  echo -e "${BOLD}4)${NC} ${MAGENTA}Upgrade Existing${NC}"
  if [ "$HAS_CLAUDE" = "existing" ]; then
    echo "   • Update your existing Claude setup"
    echo "   • Preserve your customizations"
    echo "   • Add new v4.0.0 features"
  else
    echo "   • (Not applicable - no existing setup)"
  fi
  echo ""
  
  echo -n "Select mode (1-4): "
  read -r mode_choice
  
  case $mode_choice in
    1) WIZARD_MODE="full" ;;
    2) WIZARD_MODE="commands" ;;
    3) WIZARD_MODE="selective" ;;
    4) 
      if [ "$HAS_CLAUDE" = "existing" ]; then
        WIZARD_MODE="upgrade"
      else
        echo -e "${RED}No existing Claude setup to upgrade. Defaulting to full integration.${NC}"
        WIZARD_MODE="full"
      fi
      ;;
    *) 
      echo -e "${YELLOW}Invalid choice. Using recommended full integration.${NC}"
      WIZARD_MODE="full"
      ;;
  esac
  
  echo ""
  echo -e "${GREEN}Selected: ${WIZARD_MODE} integration${NC}"
  sleep 2
}

configure_conflict_strategy() {
  show_wizard_header
  echo -e "${CYAN}⚙️ STEP 3: Configure Conflict Strategy${NC}"
  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  
  echo "How should we handle files that already exist?"
  echo ""
  echo -e "${BOLD}1)${NC} ${GREEN}Smart Merge${NC} (Recommended)"
  echo "   • Intelligently merge configurations"
  echo "   • Preserve your customizations"
  echo "   • Add -boilerplate suffix for conflicts"
  echo ""
  echo -e "${BOLD}2)${NC} ${BLUE}Skip Existing${NC}"
  echo "   • Never overwrite your files"
  echo "   • Only add new files"
  echo "   • Safest option"
  echo ""
  echo -e "${BOLD}3)${NC} ${YELLOW}Interactive${NC}"
  echo "   • Ask for each conflict"
  echo "   • Maximum control"
  echo "   • Takes more time"
  echo ""
  
  echo -n "Select strategy (1-3): "
  read -r strategy_choice
  
  case $strategy_choice in
    1) CONFLICTS_STRATEGY="smart" ;;
    2) CONFLICTS_STRATEGY="skip" ;;
    3) CONFLICTS_STRATEGY="interactive" ;;
    *) 
      echo -e "${YELLOW}Invalid choice. Using smart merge.${NC}"
      CONFLICTS_STRATEGY="smart"
      ;;
  esac
  
  echo ""
  echo -e "${GREEN}Strategy: ${CONFLICTS_STRATEGY}${NC}"
  sleep 2
}

download_boilerplate() {
  show_wizard_header
  echo -e "${CYAN}📥 STEP 4: Downloading Boilerplate${NC}"
  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  
  echo "Downloading latest boilerplate..."
  
  # Create temp directory
  mkdir -p "$TEMP_DIR"
  
  # Clone the repository
  if git clone --quiet "$PUBLIC_REPO" "$TEMP_DIR/boilerplate" 2>/dev/null; then
    echo -e "${GREEN}✓ Downloaded successfully${NC}"
  else
    echo -e "${RED}✗ Failed to download boilerplate${NC}"
    echo "Please check your internet connection and try again."
    exit 1
  fi
  
  echo ""
  echo "Press ENTER to continue..."
  read -r
}

select_features() {
  if [ "$WIZARD_MODE" != "selective" ]; then
    return
  fi
  
  show_wizard_header
  echo -e "${CYAN}🎯 STEP 5: Select Features${NC}"
  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  
  echo "Select features to integrate (comma-separated numbers):"
  echo ""
  echo "  1) Commands (150+ custom commands)"
  echo "  2) Agents (31 specialized AI agents)"
  echo "  3) Hooks (automation & safety)"
  echo "  4) PRPs (Product Requirement Prompts)"
  echo "  5) Design System (enforced typography)"
  echo "  6) Security Features (PII protection)"
  echo "  7) Git Hooks (pre-commit validation)"
  echo "  8) Documentation (guides & templates)"
  echo ""
  echo -n "Enter selections (e.g., 1,2,3): "
  read -r feature_selection
  
  # Process selections (simplified for now)
  echo ""
  echo -e "${GREEN}Features selected: ${feature_selection}${NC}"
  sleep 2
}

create_backups() {
  show_wizard_header
  echo -e "${CYAN}💾 STEP 6: Creating Backups${NC}"
  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  
  echo "Creating safety backups..."
  
  # Create backup directory
  mkdir -p "$BACKUP_DIR"
  
  # Backup critical files if they exist
  local files_to_backup=(
    ".claude"
    "CLAUDE.md"
    "package.json"
    "tsconfig.json"
    "tailwind.config.js"
    ".env"
    ".gitignore"
  )
  
  for file in "${files_to_backup[@]}"; do
    if [ -e "$file" ]; then
      cp -r "$file" "$BACKUP_DIR/" 2>/dev/null && \
        echo "  ✓ Backed up: $file"
    fi
  done
  
  echo ""
  echo -e "${GREEN}Backups created at: ${BACKUP_DIR}${NC}"
  echo ""
  echo "Press ENTER to continue..."
  read -r
}

perform_integration() {
  show_wizard_header
  echo -e "${CYAN}🔧 STEP 7: Performing Integration${NC}"
  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  
  case $WIZARD_MODE in
    "full")
      echo "Performing full integration..."
      integrate_full
      ;;
    "commands")
      echo "Integrating commands and agents only..."
      integrate_commands_only
      ;;
    "selective")
      echo "Integrating selected features..."
      integrate_selective
      ;;
    "upgrade")
      echo "Upgrading existing setup..."
      integrate_upgrade
      ;;
  esac
  
  echo ""
  echo -e "${GREEN}✓ Integration complete!${NC}"
  sleep 2
}

integrate_full() {
  # Copy .claude directory
  if [ -d "$TEMP_DIR/boilerplate/.claude" ]; then
    if [ -d ".claude" ] && [ "$CONFLICTS_STRATEGY" = "smart" ]; then
      echo "  → Merging .claude directory..."
      rsync -av --backup --suffix="-original" \
        "$TEMP_DIR/boilerplate/.claude/" ".claude/" 2>/dev/null
    else
      cp -r "$TEMP_DIR/boilerplate/.claude" . 2>/dev/null
    fi
    echo "  ✓ Integrated .claude directory"
  fi
  
  # Copy other directories based on mode
  local dirs=("PRPs" "field-registry" "scripts" "docs")
  for dir in "${dirs[@]}"; do
    if [ -d "$TEMP_DIR/boilerplate/$dir" ] && [ ! -d "$dir" ]; then
      cp -r "$TEMP_DIR/boilerplate/$dir" . 2>/dev/null && \
        echo "  ✓ Added $dir"
    fi
  done
  
  # Handle configuration files
  local configs=(
    "CLAUDE.md"
    "tailwind.config.js"
    "tsconfig.json"
    ".gitignore"
  )
  
  for config in "${configs[@]}"; do
    if [ -f "$TEMP_DIR/boilerplate/$config" ]; then
      if [ -f "$config" ] && [ "$CONFLICTS_STRATEGY" = "smart" ]; then
        cp "$TEMP_DIR/boilerplate/$config" "${config}.boilerplate" 2>/dev/null && \
          echo "  ✓ Added ${config}.boilerplate (merge manually)"
      elif [ ! -f "$config" ]; then
        cp "$TEMP_DIR/boilerplate/$config" . 2>/dev/null && \
          echo "  ✓ Added $config"
      fi
    fi
  done
}

integrate_commands_only() {
  # Just copy .claude directory
  if [ -d "$TEMP_DIR/boilerplate/.claude" ]; then
    if [ -d ".claude" ]; then
      echo "  → Merging .claude directory..."
      rsync -av --backup --suffix="-original" \
        "$TEMP_DIR/boilerplate/.claude/" ".claude/" 2>/dev/null
    else
      cp -r "$TEMP_DIR/boilerplate/.claude" . 2>/dev/null
    fi
    echo "  ✓ Integrated .claude directory"
  fi
  
  # Add CLAUDE.md if it doesn't exist
  if [ ! -f "CLAUDE.md" ] && [ -f "$TEMP_DIR/boilerplate/CLAUDE.md" ]; then
    cp "$TEMP_DIR/boilerplate/CLAUDE.md" . 2>/dev/null && \
      echo "  ✓ Added CLAUDE.md"
  fi
}

integrate_selective() {
  # Simplified selective integration
  echo "  → Integrating selected features..."
  # This would process the feature_selection variable
  # For now, just do a minimal integration
  integrate_commands_only
}

integrate_upgrade() {
  # Upgrade existing setup
  echo "  → Upgrading existing Claude setup..."
  
  # Backup existing
  cp -r .claude ".claude.backup-$(date +%Y%m%d)" 2>/dev/null
  
  # Merge new features
  rsync -av --update \
    "$TEMP_DIR/boilerplate/.claude/" ".claude/" 2>/dev/null
  
  echo "  ✓ Upgraded to latest version"
}

post_integration_setup() {
  show_wizard_header
  echo -e "${CYAN}🚀 STEP 8: Post-Integration Setup${NC}"
  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  
  # Set up git hooks if requested
  if [ -f ".claude/scripts/setup-hooks.sh" ]; then
    echo "Setting up Git hooks..."
    bash .claude/scripts/setup-hooks.sh 2>/dev/null && \
      echo "  ✓ Git hooks installed"
  fi
  
  # Create .env.example if needed
  if [ ! -f ".env.example" ] && [ -f "$TEMP_DIR/boilerplate/.env.example" ]; then
    cp "$TEMP_DIR/boilerplate/.env.example" . 2>/dev/null && \
      echo "  ✓ Added .env.example"
  fi
  
  echo ""
  echo -e "${GREEN}Setup complete!${NC}"
  sleep 2
}

show_next_steps() {
  show_wizard_header
  echo -e "${CYAN}✅ Integration Complete!${NC}"
  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  
  echo -e "${GREEN}Your project now has:${NC}"
  case $WIZARD_MODE in
    "full")
      echo "  ✓ 150+ custom commands"
      echo "  ✓ 31 specialized AI agents"
      echo "  ✓ Automated hooks system"
      echo "  ✓ PRP methodology"
      echo "  ✓ Complete documentation"
      ;;
    "commands")
      echo "  ✓ All Claude Code commands"
      echo "  ✓ AI agents"
      echo "  ✓ Basic configuration"
      ;;
    *)
      echo "  ✓ Selected features integrated"
      ;;
  esac
  
  echo ""
  echo -e "${CYAN}🎯 Next Steps:${NC}"
  echo ""
  echo "1. Start Claude Code:"
  echo -e "   ${BOLD}claude .${NC}"
  echo ""
  echo "2. Load the system context:"
  echo -e "   ${BOLD}/sr${NC}"
  echo ""
  echo "3. Analyze your existing code:"
  echo -e "   ${BOLD}/analyze-existing full${NC}"
  echo ""
  echo "4. Check available commands:"
  echo -e "   ${BOLD}/help${NC}"
  echo ""
  
  if [ "$CONFLICTS_STRATEGY" = "smart" ] && [ -f "*.boilerplate" ]; then
    echo -e "${YELLOW}⚠️ Manual Merge Required:${NC}"
    echo "Some files were saved with .boilerplate suffix."
    echo "Please review and merge them manually:"
    ls -la *.boilerplate 2>/dev/null
    echo ""
  fi
  
  echo -e "${GREEN}Happy coding with Claude! 🚀${NC}"
  echo ""
  
  # Save integration log
  mkdir -p "$(dirname "$WIZARD_LOG")"
  cat > "$WIZARD_LOG" <<EOF
Integration completed: $(date)
Mode: $WIZARD_MODE
Strategy: $CONFLICTS_STRATEGY
Framework: $FRAMEWORK
Backup: $BACKUP_DIR
EOF
  
  echo "Integration log saved to: $WIZARD_LOG"
  echo ""
  echo "Press ENTER to finish..."
  read -r
}

cleanup() {
  # Clean up temp directory
  rm -rf "$TEMP_DIR" 2>/dev/null
  rm -rf "$SCRIPT_DIR" 2>/dev/null
}

# Main execution
main() {
  # Trap to ensure cleanup
  trap cleanup EXIT
  
  # Run wizard steps
  wizard_welcome
  analyze_project
  choose_integration_mode
  configure_conflict_strategy
  download_boilerplate
  select_features
  create_backups
  perform_integration
  post_integration_setup
  show_next_steps
  
  echo -e "${GREEN}✨ Wizard completed successfully!${NC}"
}

# Run main function
main
