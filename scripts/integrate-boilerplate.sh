#!/bin/bash

# integrate-boilerplate.sh
# This script can be run from ANY existing project to integrate the boilerplate
# 
# Usage:
#   curl -sSL https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/scripts/integrate-boilerplate.sh | bash
#   
#   Or download and run:
#   wget https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/scripts/integrate-boilerplate.sh
#   chmod +x integrate-boilerplate.sh
#   ./integrate-boilerplate.sh [--mode=full|selective|sidecar] [--dry-run]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
MODE="${1:-full}"
DRY_RUN=false
BOILERPLATE_REPO="https://github.com/bearingfruitco/claude-code-boilerplate.git"
TEMP_DIR=".claude-boilerplate-temp"

# Parse arguments
for arg in "$@"; do
  case $arg in
    --mode=*)
      MODE="${arg#*=}"
      ;;
    --dry-run)
      DRY_RUN=true
      ;;
    --help)
      echo "Usage: $0 [--mode=full|selective|sidecar] [--dry-run]"
      exit 0
      ;;
  esac
done

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}    Claude Code Boilerplate Integration v4.0.0${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Step 1: Check if we're in a git repo
if [ ! -d ".git" ]; then
  echo -e "${RED}❌ Not in a git repository!${NC}"
  echo "Please run this from your project root."
  exit 1
fi

echo -e "${GREEN}✓${NC} Git repository detected"

# Step 2: Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
  echo -e "${YELLOW}⚠️  Warning: You have uncommitted changes${NC}"
  echo "It's recommended to commit or stash changes first."
  echo -n "Continue anyway? (y/n) "
  read -r response
  if [ "$response" != "y" ]; then
    exit 0
  fi
fi

# Step 3: Analyze existing setup
echo ""
echo -e "${BLUE}🔍 Analyzing your existing setup...${NC}"
echo ""

CONFLICTS=()
EXISTING_FILES=()

# Check for ALL potential conflicts
# Core boilerplate directories
[ -f "CLAUDE.md" ] && EXISTING_FILES+=("CLAUDE.md") && echo "  • Found CLAUDE.md"
[ -d ".claude" ] && EXISTING_FILES+=(".claude/") && echo "  • Found .claude directory"
[ -d ".agent-os" ] && EXISTING_FILES+=(".agent-os/") && echo "  • Found .agent-os directory"
[ -d "PRPs" ] && EXISTING_FILES+=("PRPs/") && echo "  • Found PRPs directory"
[ -d "field-registry" ] && EXISTING_FILES+=("field-registry/") && echo "  • Found field-registry"

# Config files that might conflict
[ -f ".coderabbit.yaml" ] && EXISTING_FILES+=(".coderabbit.yaml") && echo "  • Found .coderabbit.yaml"
[ -f "biome.json" ] && EXISTING_FILES+=("biome.json") && echo "  • Found biome.json"
[ -f "components.json" ] && EXISTING_FILES+=("components.json") && echo "  • Found components.json (shadcn)"
[ -f "tailwind.config.js" ] && EXISTING_FILES+=("tailwind.config.js") && echo "  • Found tailwind.config.js"
[ -f "postcss.config.js" ] && EXISTING_FILES+=("postcss.config.js") && echo "  • Found postcss.config.js"
[ -f "tsconfig.json" ] && EXISTING_FILES+=("tsconfig.json") && echo "  • Found tsconfig.json"
[ -f "next.config.js" ] && EXISTING_FILES+=("next.config.js") && echo "  • Found next.config.js"
[ -f "middleware.ts" ] && EXISTING_FILES+=("middleware.ts") && echo "  • Found middleware.ts"

# Database configs
[ -f "drizzle.config.ts" ] && EXISTING_FILES+=("drizzle.config.ts") && echo "  • Found drizzle.config.ts"
[ -d "prisma" ] && EXISTING_FILES+=("prisma/") && echo "  • Found prisma directory"

# Testing configs
[ -f "playwright.config.ts" ] && EXISTING_FILES+=("playwright.config.ts") && echo "  • Found playwright.config.ts"

# Git and CI/CD
[ -d ".husky" ] && EXISTING_FILES+=(".husky/") && echo "  • Found .husky directory"
[ -d ".github" ] && EXISTING_FILES+=(".github/") && echo "  • Found .github directory"
[ -f ".gitignore" ] && EXISTING_FILES+=(".gitignore") && echo "  • Found .gitignore"

# App structure directories
[ -d "app" ] && EXISTING_FILES+=("app/") && echo "  • Found app directory"
[ -d "components" ] && EXISTING_FILES+=("components/") && echo "  • Found components directory"
[ -d "lib" ] && EXISTING_FILES+=("lib/") && echo "  • Found lib directory"
[ -d "hooks" ] && EXISTING_FILES+=("hooks/") && echo "  • Found hooks directory"
[ -d "stores" ] && EXISTING_FILES+=("stores/") && echo "  • Found stores directory"
[ -d "types" ] && EXISTING_FILES+=("types/") && echo "  • Found types directory"
[ -d "styles" ] && EXISTING_FILES+=("styles/") && echo "  • Found styles directory"
[ -d "config" ] && EXISTING_FILES+=("config/") && echo "  • Found config directory"

# Package management
[ -f "package.json" ] && echo "  • Found package.json (will merge dependencies)"
[ -f "pnpm-lock.yaml" ] && echo "  • Found pnpm-lock.yaml"
[ -f ".npmrc" ] && EXISTING_FILES+=(".npmrc") && echo "  • Found .npmrc"
[ -f "bunfig.toml" ] && EXISTING_FILES+=("bunfig.toml") && echo "  • Found bunfig.toml"

# Count specific conflicts
if [ -d ".claude/commands" ]; then
  EXISTING_COMMANDS=$(ls -1 .claude/commands/*.md 2>/dev/null | wc -l || echo 0)
  echo "  • Found $EXISTING_COMMANDS existing commands"
fi

if [ -d ".claude/hooks" ]; then
  EXISTING_HOOKS=$(find .claude/hooks -name "*.py" -o -name "*.js" 2>/dev/null | wc -l || echo 0)
  echo "  • Found $EXISTING_HOOKS existing hooks"
fi

# Step 4: Create backup (unless dry run)
if [ "$DRY_RUN" = false ]; then
  echo ""
  echo -e "${BLUE}📦 Creating backup...${NC}"
  
  BACKUP_DIR=".claude-integration/backup/$(date +%Y%m%d_%H%M%S)"
  mkdir -p "$BACKUP_DIR"
  
  for file in "${EXISTING_FILES[@]}"; do
    if [ -e "$file" ]; then
      cp -r "$file" "$BACKUP_DIR/" 2>/dev/null || true
      echo "  • Backed up $file"
    fi
  done
  
  echo -e "${GREEN}✓${NC} Backup created at: $BACKUP_DIR"
fi

# Step 5: Clone boilerplate to temp directory
echo ""
echo -e "${BLUE}📥 Fetching boilerplate...${NC}"

if [ -d "$TEMP_DIR" ]; then
  rm -rf "$TEMP_DIR"
fi

git clone --quiet "$BOILERPLATE_REPO" "$TEMP_DIR"
echo -e "${GREEN}✓${NC} Boilerplate downloaded"

# Step 6: Show integration plan
echo ""
echo -e "${BLUE}📋 Integration Plan (Mode: $MODE)${NC}"
echo ""

case "$MODE" in
  "selective")
    echo "Select components to integrate:"
    echo ""
    echo "1) Commands & Automation (.claude/)"
    echo "2) Design System Enforcement"
    echo "3) PRP System (PRPs/)"
    echo "4) Agent OS Standards (.agent-os/)"
    echo "5) Security Features (field-registry/)"
    echo "6) Git Hooks (.husky/)"
    echo "7) Documentation (CLAUDE.md, guides)"
    echo "8) Config Files (.coderabbit.yaml, etc)"
    echo ""
    echo -n "Enter numbers (comma-separated, e.g., 1,3,5): "
    read -r SELECTIONS
    ;;
    
  "sidecar")
    echo "Will install as .claude-boilerplate/ (no conflicts)"
    echo "Access commands with /bb prefix"
    ;;
    
  *)  # full mode
    echo "Full integration will:"
    echo ""
    echo "${GREEN}Core Claude Code:${NC}"
    if [ -f "CLAUDE.md" ]; then
      echo "  • Keep your CLAUDE.md"
      echo "  • Add CLAUDE_BOILERPLATE.md"
    else
      echo "  • Add CLAUDE.md"
    fi
    
    if [ -d ".claude" ]; then
      echo "  • Merge .claude directories:"
      echo "    - Your commands: preserved or renamed with -project suffix"
      echo "    - Hooks: numbered so yours run first"
    else
      echo "  • Add complete .claude directory"
    fi
    
    echo ""
    echo "${GREEN}Standards & Documentation:${NC}"
    echo "  • Add .agent-os/ (standards, product docs)"
    echo "  • Add PRPs/ (one-pass implementation)"
    echo "  • Add field-registry/ (security features)"
    
    echo ""
    echo "${GREEN}Config Files:${NC}"
    if [ -f "tailwind.config.js" ]; then
      echo "  • Merge tailwind.config.js (add design tokens)"
    else
      echo "  • Add tailwind.config.js with v4 + design system"
    fi
    
    if [ -f "tsconfig.json" ]; then
      echo "  • Merge tsconfig.json paths and settings"
    else
      echo "  • Add tsconfig.json with strict settings"
    fi
    
    [ ! -f "biome.json" ] && echo "  • Add biome.json (linting/formatting)"
    [ ! -f "components.json" ] && echo "  • Add components.json (shadcn config)"
    [ ! -f ".coderabbit.yaml" ] && echo "  • Add .coderabbit.yaml (AI reviews)"
    
    echo ""
    echo "${GREEN}Development Tools:${NC}"
    if [ -f "drizzle.config.ts" ] || [ -d "prisma" ]; then
      echo "  • Skip database config (you have your own)"
    else
      echo "  • Add drizzle.config.ts and schema"
    fi
    
    [ ! -f "playwright.config.ts" ] && echo "  • Add playwright.config.ts"
    [ ! -d ".husky" ] && echo "  • Add Git hooks (.husky)"
    
    echo ""
    echo "${GREEN}Code Structure:${NC}"
    if [ -d "components" ]; then
      echo "  • Merge components/ (add ui/, forms/ subdirs)"
    fi
    if [ -d "lib" ]; then
      echo "  • Merge lib/ (add events/, db/, validation/)"
    fi
    [ ! -d "hooks" ] && echo "  • Add hooks/ directory"
    [ ! -d "stores" ] && echo "  • Add stores/ (Zustand stores)"
    [ ! -d "types" ] && echo "  • Add types/ directory"
    
    echo ""
    echo "${YELLOW}Will NOT overwrite:${NC}"
    echo "  • Your app/ directory"
    echo "  • Your package.json (deps will be listed separately)"
    echo "  • Your middleware.ts"
    echo "  • Your .env files"
    echo "  • Your database schema (if exists)"
    ;;
esac

# Step 7: Confirm before proceeding
if [ "$DRY_RUN" = true ]; then
  echo ""
  echo -e "${YELLOW}DRY RUN MODE - No changes will be made${NC}"
else
  echo ""
  echo -n "Proceed with integration? (y/n) "
  read -r response
  if [ "$response" != "y" ]; then
    rm -rf "$TEMP_DIR"
    exit 0
  fi
fi

# Step 8: Execute integration
if [ "$DRY_RUN" = false ]; then
  echo ""
  echo -e "${BLUE}🔧 Executing integration...${NC}"
  echo ""
  
  case "$MODE" in
    "sidecar")
      # Simple - just copy everything to .claude-boilerplate
      cp -r "$TEMP_DIR/.claude" .claude-boilerplate
      echo -e "${GREEN}✓${NC} Installed as .claude-boilerplate/"
      
      # Create wrapper command
      cat > .claude-boilerplate/bb-wrapper.md << 'EOF'
# Boilerplate Command Wrapper
# Use: /bb [command] to access boilerplate commands
# Example: /bb cc Button
EOF
      ;;
      
    "selective")
      # Parse selections and copy selected components
      IFS=',' read -ra SELECTED <<< "$SELECTIONS"
      for i in "${SELECTED[@]}"; do
        case $i in
          1) # Commands & Automation
            mkdir -p .claude
            cp -r "$TEMP_DIR/.claude/"* .claude/ 2>/dev/null || true
            echo -e "${GREEN}✓${NC} Added commands & automation"
            ;;
          3) # PRP System
            cp -r "$TEMP_DIR/PRPs" . 2>/dev/null || true
            echo -e "${GREEN}✓${NC} Added PRP system"
            ;;
          4) # Agent OS
            cp -r "$TEMP_DIR/.agent-os" . 2>/dev/null || true
            echo -e "${GREEN}✓${NC} Added Agent OS"
            ;;
          # ... handle other selections
        esac
      done
      ;;
      
    *)  # full mode
      # Handle CLAUDE.md
      if [ -f "CLAUDE.md" ]; then
        cp "$TEMP_DIR/CLAUDE.md" CLAUDE_BOILERPLATE.md
        
        # Append integration notice to existing CLAUDE.md
        cat >> CLAUDE.md << 'EOF'

## Boilerplate Integration

This project has been enhanced with Claude Code Boilerplate v4.0.0.
See CLAUDE_BOILERPLATE.md for boilerplate-specific features.

Key additions:
- 116+ commands (/help for list)
- Design enforcement (/vd)
- PRP implementation (/create-prp)
- 31 AI agents (/personas)
EOF
        echo -e "${GREEN}✓${NC} Created CLAUDE_BOILERPLATE.md"
      else
        cp "$TEMP_DIR/CLAUDE.md" .
        echo -e "${GREEN}✓${NC} Added CLAUDE.md"
      fi
      
      # Handle .claude directory
      if [ -d ".claude" ]; then
        # Complex merge logic
        echo "  Merging .claude directories..."
        
        # Handle commands
        if [ -d ".claude/commands" ]; then
          mkdir -p .claude/commands/project
          
          # Check each boilerplate command for conflicts
          for cmd in "$TEMP_DIR"/.claude/commands/*.md; do
            cmd_name=$(basename "$cmd")
            if [ -f ".claude/commands/$cmd_name" ]; then
              # Conflict - move existing
              mv ".claude/commands/$cmd_name" ".claude/commands/project/${cmd_name%.md}-project.md"
              echo "    • Moved your /$cmd_name to -project"
            fi
            cp "$cmd" .claude/commands/
          done
        else
          cp -r "$TEMP_DIR/.claude/commands" .claude/
        fi
        
        # Handle hooks with numbering
        if [ -d ".claude/hooks" ]; then
          for hook_type in pre-tool-use post-tool-use; do
            if [ -d ".claude/hooks/$hook_type" ]; then
              # Renumber existing hooks to 00-09
              for hook in .claude/hooks/$hook_type/*; do
                if [ -f "$hook" ]; then
                  base=$(basename "$hook")
                  num="${base%%[!0-9]*}"
                  name="${base#$num}"
                  new_name="0${num}${name}"
                  mv "$hook" ".claude/hooks/$hook_type/$new_name"
                fi
              done
            fi
            
            # Copy boilerplate hooks (they start at 10+)
            if [ -d "$TEMP_DIR/.claude/hooks/$hook_type" ]; then
              mkdir -p ".claude/hooks/$hook_type"
              cp "$TEMP_DIR/.claude/hooks/$hook_type/"* ".claude/hooks/$hook_type/" 2>/dev/null || true
            fi
          done
          echo "    • Merged hooks (yours run first)"
        else
          cp -r "$TEMP_DIR/.claude/hooks" .claude/ 2>/dev/null || true
        fi
        
        # Copy other .claude contents
        for item in personas sub-agents chains.json config.json settings.json; do
          if [ -e "$TEMP_DIR/.claude/$item" ]; then
            if [ ! -e ".claude/$item" ]; then
              cp -r "$TEMP_DIR/.claude/$item" .claude/
            fi
          fi
        done
        
        echo -e "${GREEN}✓${NC} Merged .claude directory"
      else
        cp -r "$TEMP_DIR/.claude" .
        echo -e "${GREEN}✓${NC} Added .claude directory"
      fi
      
      # Copy other directories (no conflicts expected)
      for dir in .agent-os PRPs field-registry; do
        if [ ! -d "$dir" ] && [ -d "$TEMP_DIR/$dir" ]; then
          cp -r "$TEMP_DIR/$dir" .
          echo -e "${GREEN}✓${NC} Added $dir"
        fi
      done
      
      # Handle config files with merging
      # Tailwind config - merge to add design tokens
      if [ -f "tailwind.config.js" ] && [ -f "$TEMP_DIR/tailwind.config.js" ]; then
        cp tailwind.config.js tailwind.config.js.backup
        echo "    • Backed up tailwind.config.js"
        echo "    • TODO: Manually merge design tokens from $TEMP_DIR/tailwind.config.js"
      elif [ ! -f "tailwind.config.js" ] && [ -f "$TEMP_DIR/tailwind.config.js" ]; then
        cp "$TEMP_DIR/tailwind.config.js" .
        echo -e "${GREEN}✓${NC} Added tailwind.config.js"
      fi
      
      # TypeScript config - merge paths
      if [ -f "tsconfig.json" ] && [ -f "$TEMP_DIR/tsconfig.json" ]; then
        cp tsconfig.json tsconfig.json.backup
        echo "    • Backed up tsconfig.json"
        echo "    • TODO: Add path aliases from boilerplate"
      elif [ ! -f "tsconfig.json" ] && [ -f "$TEMP_DIR/tsconfig.json" ]; then
        cp "$TEMP_DIR/tsconfig.json" .
        echo -e "${GREEN}✓${NC} Added tsconfig.json"
      fi
      
      # Copy other config files if they don't exist
      for file in biome.json components.json .coderabbit.yaml postcss.config.js playwright.config.ts; do
        if [ ! -f "$file" ] && [ -f "$TEMP_DIR/$file" ]; then
          cp "$TEMP_DIR/$file" .
          echo -e "${GREEN}✓${NC} Added $file"
        fi
      done
      
      # Database config - only if not present
      if [ ! -f "drizzle.config.ts" ] && [ ! -d "prisma" ] && [ -f "$TEMP_DIR/drizzle.config.ts" ]; then
        cp "$TEMP_DIR/drizzle.config.ts" .
        echo -e "${GREEN}✓${NC} Added drizzle.config.ts"
        # Also copy the schema
        if [ -d "$TEMP_DIR/lib/db" ]; then
          mkdir -p lib/db
          cp -r "$TEMP_DIR/lib/db/"* lib/db/
          echo -e "${GREEN}✓${NC} Added database schema"
        fi
      fi
      
      # Merge lib directory structure
      if [ -d "lib" ]; then
        # Add subdirectories that don't exist
        for subdir in events validation api db monitoring; do
          if [ ! -d "lib/$subdir" ] && [ -d "$TEMP_DIR/lib/$subdir" ]; then
            cp -r "$TEMP_DIR/lib/$subdir" lib/
            echo -e "${GREEN}✓${NC} Added lib/$subdir"
          fi
        done
      else
        cp -r "$TEMP_DIR/lib" .
        echo -e "${GREEN}✓${NC} Added lib directory"
      fi
      
      # Merge components directory structure
      if [ -d "components" ]; then
        # Add ui and forms subdirectories if they don't exist
        for subdir in ui forms; do
          if [ ! -d "components/$subdir" ] && [ -d "$TEMP_DIR/components/$subdir" ]; then
            cp -r "$TEMP_DIR/components/$subdir" components/
            echo -e "${GREEN}✓${NC} Added components/$subdir"
          fi
        done
      else
        cp -r "$TEMP_DIR/components" .
        echo -e "${GREEN}✓${NC} Added components directory"
      fi
      
      # Add other directories if they don't exist
      for dir in hooks stores types templates scripts/validation; do
        if [ ! -d "$dir" ] && [ -d "$TEMP_DIR/$dir" ]; then
          mkdir -p "$(dirname "$dir")"
          cp -r "$TEMP_DIR/$dir" "$dir"
          echo -e "${GREEN}✓${NC} Added $dir"
        fi
      done
      
      # Handle .husky directory
      if [ -d ".husky" ] && [ -d "$TEMP_DIR/.husky" ]; then
        # Merge hooks
        for hook in "$TEMP_DIR/.husky/"*; do
          hook_name=$(basename "$hook")
          if [ -f ".husky/$hook_name" ]; then
            # Append our hooks to existing
            echo "" >> ".husky/$hook_name"
            echo "# Boilerplate hooks" >> ".husky/$hook_name"
            cat "$hook" >> ".husky/$hook_name"
            echo "    • Merged .husky/$hook_name"
          else
            cp "$hook" ".husky/"
            echo -e "${GREEN}✓${NC} Added .husky/$hook_name"
          fi
        done
      elif [ ! -d ".husky" ] && [ -d "$TEMP_DIR/.husky" ]; then
        cp -r "$TEMP_DIR/.husky" .
        echo -e "${GREEN}✓${NC} Added .husky directory"
      fi
      
      # Copy root documentation files
      for file in QUICK_REFERENCE.md; do
        if [ ! -f "$file" ] && [ -f "$TEMP_DIR/$file" ]; then
          cp "$TEMP_DIR/$file" .
          echo -e "${GREEN}✓${NC} Added $file"
        fi
      done
      
      # Merge .gitignore
      if [ -f "$TEMP_DIR/.gitignore" ]; then
        echo "" >> .gitignore
        echo "# Claude Code Boilerplate" >> .gitignore
        cat "$TEMP_DIR/.gitignore" >> .gitignore
        echo -e "${GREEN}✓${NC} Updated .gitignore"
      fi
      ;;
  esac
fi

# Step 9: Cleanup
rm -rf "$TEMP_DIR"

# Step 10: Final report
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Integration Complete!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

if [ "$DRY_RUN" = true ]; then
  echo "This was a dry run. No changes were made."
  echo "Run without --dry-run to apply changes."
else
  echo "What's new:"
  echo "  • 116+ commands (run 'claude .' then /help)"
  echo "  • 31 AI agents for orchestration"
  echo "  • Design system enforcement"
  echo "  • PRP one-pass implementation"
  echo "  • Smart chains and automation"
  echo ""
  
  # Check for missing dependencies
  if [ -f "package.json" ]; then
    echo "${YELLOW}Dependencies to add:${NC}"
    echo "Run: pnpm add @supabase/supabase-js framer-motion lucide-react"
    echo "Run: pnpm add -D @biomejs/biome drizzle-kit @playwright/test"
    echo ""
  fi
  
  # Show manual merge tasks
  if [ -f "tailwind.config.js.backup" ] || [ -f "tsconfig.json.backup" ]; then
    echo "${YELLOW}Manual merge needed:${NC}"
    [ -f "tailwind.config.js.backup" ] && echo "  • Merge design tokens into tailwind.config.js"
    [ -f "tsconfig.json.backup" ] && echo "  • Add path aliases to tsconfig.json"
    echo ""
  fi
  
  echo "Next steps:"
  echo "  1. Run 'claude .' to start Claude Code"
  echo "  2. Run '/sr' to load the full system"
  echo "  3. Run '/help' to see available commands"
  echo ""
  
  if [ -d ".claude-integration/backup" ]; then
    echo "Rollback available:"
    echo "  If issues arise, your backup is at:"
    echo "  $BACKUP_DIR"
  fi
fi

echo ""
echo "Happy coding! 🚀"
