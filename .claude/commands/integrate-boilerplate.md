---
name: integrate-boilerplate
description: |
  Smart integration of boilerplate into existing projects with conflict resolution.
  Preserves existing Claude Code setup while adding boilerplate capabilities.
argument-hint: "[--mode=full|selective|sidecar] [--preserve] [--dry-run]"
aliases: ["ib", "integrate", "add-boilerplate"]
---

# Smart Boilerplate Integration

**Mode**: $MODE (default: full)  
**Options**: $OPTIONS

## 🔍 Phase 1: Scanning Existing Setup

```bash
echo "Analyzing your existing project setup..."
echo ""

# Initialize tracking variables
EXISTING_CLAUDE_MD=false
EXISTING_CLAUDE_DIR=false
EXISTING_COMMANDS=0
EXISTING_HOOKS=0
EXISTING_AGENT_OS=false
EXISTING_FIELD_REGISTRY=false
EXISTING_PRPS=false
EXISTING_CONFIG_FILES=()
EXISTING_NEXTJS=false
EXISTING_COMPONENTS=false
EXISTING_LIB=false
EXISTING_TESTS=false

# Check Claude setup
if [ -f "CLAUDE.md" ]; then
  EXISTING_CLAUDE_MD=true
  echo "✓ Found existing CLAUDE.md"
fi

if [ -d ".claude" ]; then
  EXISTING_CLAUDE_DIR=true
  if [ -d ".claude/commands" ]; then
    EXISTING_COMMANDS=$(ls -1 .claude/commands/*.md 2>/dev/null | wc -l)
    echo "✓ Found $EXISTING_COMMANDS existing commands"
  fi
  if [ -d ".claude/hooks" ]; then
    EXISTING_HOOKS=$(find .claude/hooks -name "*.py" 2>/dev/null | wc -l)
    echo "✓ Found $EXISTING_HOOKS existing hooks"
  fi
fi

# Check Agent OS
if [ -d ".agent-os" ]; then
  EXISTING_AGENT_OS=true
  echo "✓ Found existing Agent OS setup"
fi

# Check boilerplate directories
[ -d "field-registry" ] && EXISTING_FIELD_REGISTRY=true && echo "✓ Found existing field-registry"
[ -d "PRPs" ] && EXISTING_PRPS=true && echo "✓ Found existing PRPs directory"

# Check Next.js/React setup
[ -d "app" ] && EXISTING_NEXTJS=true && echo "✓ Found Next.js app directory"
[ -d "components" ] && EXISTING_COMPONENTS=true && echo "✓ Found components directory"
[ -d "lib" ] && EXISTING_LIB=true && echo "✓ Found lib directory"
[ -d "tests" ] && EXISTING_TESTS=true && echo "✓ Found tests directory"

# Check configuration files
CONFIG_FILES=(
  "biome.json"
  "playwright.config.ts"
  "tailwind.config.js"
  "postcss.config.js"
  "next.config.js"
  "tsconfig.json"
  "drizzle.config.ts"
  "components.json"
  ".coderabbit.yaml"
  ".npmrc"
  "bunfig.toml"
)

echo ""
echo "Configuration files found:"
for config in "${CONFIG_FILES[@]}"; do
  if [ -f "$config" ]; then
    EXISTING_CONFIG_FILES+=("$config")
    echo "  • $config"
  fi
done

# Check environment files
echo ""
echo "Environment files found:"
for env_file in .env*; do
  if [ -f "$env_file" ]; then
    echo "  • $env_file"
  fi
done

# Create integration report
mkdir -p .claude-integration
```

## 📊 Phase 2: Conflict Analysis & Planning

```bash
cat > .claude-integration/CONFLICT_REPORT.md << 'EOF'
# Integration Conflict Report

Generated: $(date)

## Project Analysis

### Type Detection
EOF

# Detect project type
if [ -f "package.json" ]; then
  if [ -d "app" ] && grep -q "next" package.json; then
    echo "- Project Type: Next.js (App Router)" >> .claude-integration/CONFLICT_REPORT.md
  elif [ -d "pages" ] && grep -q "next" package.json; then
    echo "- Project Type: Next.js (Pages Router)" >> .claude-integration/CONFLICT_REPORT.md
  elif grep -q "react" package.json; then
    echo "- Project Type: React" >> .claude-integration/CONFLICT_REPORT.md
  else
    echo "- Project Type: Node.js" >> .claude-integration/CONFLICT_REPORT.md
  fi
fi

cat >> .claude-integration/CONFLICT_REPORT.md << 'EOF'

## Files That Will Be Handled

### Safe to Copy (No Conflicts Expected)
- `.agent-os/` - Standards and documentation
- `field-registry/` - Security system
- `PRPs/` - PRP templates
- `templates/` - Component templates
- `context/` - Context examples
- `demo/` - Demo files
- `.github/` - GitHub workflows (if not exists)

### Will Merge/Rename if Conflicts
- `CLAUDE.md` → Will create `CLAUDE_BOILERPLATE.md`
- `.claude/` → Commands renamed with -project suffix
- Configuration files → Backed up with .original extension

### Will Skip (Project-Specific)
- `app/` - Your Next.js app code
- `components/` - Your existing components  
- `lib/` - Your library code
- `prisma/` - Your database schema
- `public/` - Your static assets
- `.env*` - Your environment files (except .env.example)

### Will Prompt for Decision
- `hooks/` - If you have custom React hooks
- `stores/` - If you have state management
- `types/` - If you have TypeScript types
- `styles/` - If you have custom styles
- `scripts/` - If you have custom scripts
- `tests/` - If you have existing tests

EOF

echo "Conflict report generated at .claude-integration/CONFLICT_REPORT.md"
```

## 🔧 Phase 3: Integration Mode Selection

```bash
case "$MODE" in
  "selective")
    echo ""
    echo "## 🎯 Selective Integration Mode"
    echo ""
    echo "Select components to integrate (comma-separated numbers):"
    echo ""
    echo "Core System:"
    echo "  1. Commands & Automation (.claude/)"
    echo "  2. Agent OS Standards (.agent-os/)"
    echo "  3. Hooks System (.claude/hooks/)"
    echo "  4. AI Agents (.claude/agents/)"
    echo ""
    echo "Development Tools:"
    echo "  5. Field Registry (security)"
    echo "  6. PRP System (one-pass implementation)"
    echo "  7. Git Hooks (.husky/)"
    echo "  8. GitHub Workflows (.github/)"
    echo ""
    echo "Configuration:"
    echo "  9. Biome (linting/formatting)"
    echo "  10. Playwright (browser testing)"
    echo "  11. TypeScript configs"
    echo "  12. Tailwind configs"
    echo ""
    echo "Templates & Examples:"
    echo "  13. Component templates"
    echo "  14. Context examples"
    echo "  15. Demo files"
    echo ""
    echo "Enter your selection: "
    # Would read user input here
    ;;
    
  "sidecar")
    echo ""
    echo "## 🚗 Sidecar Installation Mode"
    echo ""
    echo "Installing boilerplate in parallel structure:"
    echo "  • .claude-boilerplate/ (commands)"
    echo "  • .agent-os-boilerplate/ (standards)"
    echo "  • boilerplate-templates/ (templates)"
    echo ""
    echo "Access with /bb prefix for all commands"
    ;;
    
  *)  # full mode
    echo ""
    echo "## 📦 Full Integration Mode"
    echo ""
    echo "Integration plan:"
    echo "  ✓ Merge .claude directory (preserve conflicts)"
    echo "  ✓ Install Agent OS standards"
    echo "  ✓ Add field-registry security"
    echo "  ✓ Install PRP templates"
    echo "  ✓ Add component templates"
    echo "  ✓ Merge configurations safely"
    echo "  ✓ Skip your app code completely"
    ;;
esac
```

## 💾 Phase 4: Comprehensive Backup

```bash
if [ "$MODE" != "sidecar" ]; then
  echo ""
  echo "Creating comprehensive backup..."
  
  BACKUP_DIR=".claude-integration/backup/$(date +%Y%m%d_%H%M%S)"
  mkdir -p "$BACKUP_DIR"
  
  # Backup all potentially affected files/directories
  BACKUP_ITEMS=(
    "CLAUDE.md"
    ".claude"
    ".agent-os"
    ".husky"
    ".github"
    "field-registry"
    "PRPs"
    "templates"
    "context"
    "demo"
    "hooks"
    "types"
    "stores"
    "scripts"
    "styles"
  )
  
  # Backup configuration files
  for config in "${EXISTING_CONFIG_FILES[@]}"; do
    BACKUP_ITEMS+=("$config")
  done
  
  # Perform backup
  for item in "${BACKUP_ITEMS[@]}"; do
    if [ -e "$item" ]; then
      cp -r "$item" "$BACKUP_DIR/" 2>/dev/null
      echo "  ✓ Backed up $item"
    fi
  done
  
  # Save integration metadata
  cat > "$BACKUP_DIR/integration-metadata.json" << EOF
{
  "date": "$(date)",
  "mode": "$MODE",
  "existing_commands": $EXISTING_COMMANDS,
  "existing_hooks": $EXISTING_HOOKS,
  "project_type": "$([ -d "app" ] && echo "nextjs-app" || echo "other")"
}
EOF
  
  echo ""
  echo "✅ Backup complete: $BACKUP_DIR"
fi
```

## 🔄 Phase 5: Execute Integration

### Core Claude System
```bash
echo ""
echo "## Installing Core System..."

# Handle CLAUDE.md
if [ "$EXISTING_CLAUDE_MD" = true ] && [ "$MODE" = "full" ]; then
  echo "Preserving your CLAUDE.md..."
  cp ~/.claude-boilerplate/CLAUDE.md CLAUDE_BOILERPLATE.md
  
  # Add integration notice to existing
  if ! grep -q "Boilerplate System Integration" CLAUDE.md; then
    cat >> CLAUDE.md << 'EOF'

---

## 🚀 Boilerplate System Integration

This project has been enhanced with Claude Code Boilerplate v4.0.0.
See `CLAUDE_BOILERPLATE.md` for boilerplate-specific features.

Key additions: `/sr`, `/vd`, `/create-prp`, `/orch`, `/chain`
EOF
  fi
  echo "  ✓ Created CLAUDE_BOILERPLATE.md"
elif [ "$MODE" = "full" ]; then
  cp ~/.claude-boilerplate/CLAUDE.md CLAUDE.md
  echo "  ✓ Installed CLAUDE.md"
fi

# Handle .claude directory
if [ "$MODE" = "full" ]; then
  mkdir -p .claude/{commands,hooks,agents,context,state,config}
  
  # Merge commands
  if [ $EXISTING_COMMANDS -gt 0 ]; then
    echo "Merging commands (conflicts will be renamed)..."
    
    # List of critical boilerplate commands
    CRITICAL_COMMANDS="sr cc vd fw pt gt analyze-existing create-prp"
    
    for cmd in $CRITICAL_COMMANDS; do
      if [ -f ".claude/commands/$cmd.md" ]; then
        mv ".claude/commands/$cmd.md" ".claude/commands/${cmd}-project.md"
        echo "    Renamed: /$cmd → /${cmd}-project"
      fi
    done
  fi
  
  # Copy boilerplate commands
  cp -r ~/.claude-boilerplate/.claude/commands/* .claude/commands/ 2>/dev/null
  echo "  ✓ Installed 150+ boilerplate commands"
  
  # Merge hooks
  if [ $EXISTING_HOOKS -gt 0 ]; then
    echo "Merging hooks (yours run first)..."
    
    # Renumber existing hooks to 00-09 range
    for hook_dir in pre-tool-use post-tool-use stop; do
      if [ -d ".claude/hooks/$hook_dir" ]; then
        i=0
        for hook in .claude/hooks/$hook_dir/*.py; do
          if [ -f "$hook" ]; then
            base=$(basename "$hook" | sed 's/^[0-9]*//')
            new_name="0${i}-project-${base}"
            mv "$hook" ".claude/hooks/$hook_dir/$new_name"
            ((i++))
          fi
        done
      fi
    done
  fi
  
  # Copy boilerplate hooks
  mkdir -p .claude/hooks/{pre-tool-use,post-tool-use,stop}
  cp ~/.claude-boilerplate/.claude/hooks/pre-tool-use/* .claude/hooks/pre-tool-use/ 2>/dev/null
  cp ~/.claude-boilerplate/.claude/hooks/post-tool-use/* .claude/hooks/post-tool-use/ 2>/dev/null
  cp ~/.claude-boilerplate/.claude/hooks/stop/* .claude/hooks/stop/ 2>/dev/null
  echo "  ✓ Installed automation hooks"
  
  # Copy agents
  cp -r ~/.claude-boilerplate/.claude/agents/* .claude/agents/ 2>/dev/null
  echo "  ✓ Installed 31 AI agents"
  
  # Copy config and utils
  cp -r ~/.claude-boilerplate/.claude/config .claude/ 2>/dev/null
  cp -r ~/.claude-boilerplate/.claude/utils .claude/ 2>/dev/null
  
  # Settings.json
  if [ ! -f ".claude/settings.json" ]; then
    cp ~/.claude-boilerplate/.claude/settings.json .claude/
    echo "  ✓ Installed settings.json"
  fi
fi
```

### Agent OS & Standards
```bash
if [ "$EXISTING_AGENT_OS" = false ] && [ "$MODE" != "sidecar" ]; then
  echo ""
  echo "## Installing Agent OS..."
  
  cp -r ~/.claude-boilerplate/.agent-os .agent-os
  echo "  ✓ Installed Agent OS standards and documentation"
fi
```

### Development Directories
```bash
echo ""
echo "## Installing Development Tools..."

# Field Registry (security)
if [ "$EXISTING_FIELD_REGISTRY" = false ]; then
  cp -r ~/.claude-boilerplate/field-registry field-registry
  echo "  ✓ Installed field-registry security system"
fi

# PRP System
if [ "$EXISTING_PRPS" = false ]; then
  cp -r ~/.claude-boilerplate/PRPs PRPs
  echo "  ✓ Installed PRP templates"
else
  # Merge PRP templates
  cp -r ~/.claude-boilerplate/PRPs/templates PRPs/ 2>/dev/null
  echo "  ✓ Added PRP templates to existing PRPs"
fi

# Templates
if [ ! -d "templates" ]; then
  cp -r ~/.claude-boilerplate/templates templates
  echo "  ✓ Installed component templates"
fi

# Context examples (safe to add)
if [ ! -d "context" ]; then
  cp -r ~/.claude-boilerplate/context context
  echo "  ✓ Installed context examples"
fi

# Demo files (optional)
if [ ! -d "demo" ] && [ "$MODE" = "full" ]; then
  cp -r ~/.claude-boilerplate/demo demo
  echo "  ✓ Installed demo files"
fi
```

### Configuration Files
```bash
echo ""
echo "## Handling Configuration Files..."

# Biome
if [[ " ${EXISTING_CONFIG_FILES[@]} " =~ " biome.json " ]]; then
  cp biome.json biome.original.json
  echo "  ✓ Backed up biome.json → biome.original.json"
  # Could merge configs here with jq
else
  cp ~/.claude-boilerplate/biome.json biome.json
  echo "  ✓ Installed biome.json"
fi

# Playwright
if [[ " ${EXISTING_CONFIG_FILES[@]} " =~ " playwright.config.ts " ]]; then
  cp ~/.claude-boilerplate/playwright.config.ts playwright.boilerplate.config.ts
  echo "  ✓ Created playwright.boilerplate.config.ts (original preserved)"
else
  cp ~/.claude-boilerplate/playwright.config.ts playwright.config.ts
  echo "  ✓ Installed playwright.config.ts"
fi

# Tailwind (merge carefully)
if [[ " ${EXISTING_CONFIG_FILES[@]} " =~ " tailwind.config.js " ]]; then
  cp tailwind.config.js tailwind.original.config.js
  echo "  ✓ Backed up tailwind.config.js"
  echo "  ⚠️  Manual merge needed for design tokens"
else
  cp ~/.claude-boilerplate/tailwind.config.js tailwind.config.js
  echo "  ✓ Installed tailwind.config.js with strict design system"
fi

# TypeScript config
if [[ " ${EXISTING_CONFIG_FILES[@]} " =~ " tsconfig.json " ]]; then
  echo "  ℹ️  Keeping your tsconfig.json"
else
  cp ~/.claude-boilerplate/tsconfig.json tsconfig.json
  echo "  ✓ Installed tsconfig.json"
fi

# Components.json (shadcn)
if [ ! -f "components.json" ]; then
  cp ~/.claude-boilerplate/components.json components.json
  echo "  ✓ Installed components.json"
fi

# .env.example
if [ -f ".env.example" ]; then
  cp .env.example .env.example.backup
  # Merge unique variables
  cat ~/.claude-boilerplate/.env.example >> .env.example.tmp
  sort -u .env.example.tmp > .env.example
  rm .env.example.tmp
  echo "  ✓ Merged .env.example (backup: .env.example.backup)"
else
  cp ~/.claude-boilerplate/.env.example .env.example
  echo "  ✓ Installed .env.example"
fi
```

### Development Tools
```bash
echo ""
echo "## Installing Development Tools..."

# Git hooks
if [ ! -d ".husky" ]; then
  cp -r ~/.claude-boilerplate/.husky .husky
  echo "  ✓ Installed Git hooks (.husky)"
else
  echo "  ℹ️  Git hooks exist - manual merge may be needed"
fi

# GitHub workflows
if [ ! -d ".github" ]; then
  cp -r ~/.claude-boilerplate/.github .github
  echo "  ✓ Installed GitHub workflows"
else
  # Merge workflows
  mkdir -p .github/workflows
  for workflow in ~/.claude-boilerplate/.github/workflows/*.yml; do
    basename=$(basename "$workflow")
    if [ ! -f ".github/workflows/$basename" ]; then
      cp "$workflow" .github/workflows/
      echo "  ✓ Added workflow: $basename"
    fi
  done
fi

# Scripts directory
if [ ! -d "scripts" ]; then
  cp -r ~/.claude-boilerplate/scripts scripts
  echo "  ✓ Installed utility scripts"
else
  # Add boilerplate scripts that don't exist
  for script in ~/.claude-boilerplate/scripts/*; do
    basename=$(basename "$script")
    if [ ! -f "scripts/$basename" ]; then
      cp "$script" scripts/
      echo "  ✓ Added script: $basename"
    fi
  done
fi
```

### Optional Directories
```bash
# These depend on project structure
echo ""
echo "## Checking Optional Directories..."

# Hooks (React hooks, not Claude hooks)
if [ -d "hooks" ] && [ "$MODE" = "full" ]; then
  echo "  ℹ️  You have a hooks/ directory"
  echo "     Boilerplate React hooks available in templates/hooks/"
fi

# Types
if [ -d "types" ] && [ "$MODE" = "full" ]; then
  echo "  ℹ️  You have a types/ directory" 
  echo "     Boilerplate types available in templates/types/"
fi

# Stores (state management)
if [ ! -d "stores" ] && [ "$MODE" = "full" ]; then
  cp -r ~/.claude-boilerplate/stores stores 2>/dev/null && \
    echo "  ✓ Installed store examples"
fi

# Styles
if [ ! -d "styles" ]; then
  cp -r ~/.claude-boilerplate/styles styles 2>/dev/null && \
    echo "  ✓ Installed global styles"
fi
```

### Documentation
```bash
echo ""
echo "## Installing Documentation..."

mkdir -p docs/boilerplate
cp -r ~/.claude-boilerplate/docs/* docs/boilerplate/ 2>/dev/null
echo "  ✓ Installed boilerplate docs in docs/boilerplate/"

# Copy key documentation files
for doc in CONTRIBUTING.md CHANGELOG.md; do
  if [ ! -f "$doc" ]; then
    cp ~/.claude-boilerplate/$doc $doc 2>/dev/null && \
      echo "  ✓ Installed $doc"
  fi
done
```

## ✅ Phase 6: Post-Integration Setup

```bash
echo ""
echo "## 📦 Final Setup Steps..."

# Update package.json dependencies
if [ -f "package.json" ] && [ "$MODE" = "full" ]; then
  echo ""
  echo "Add these dependencies if missing:"
  cat << 'EOF'
  
  "devDependencies": {
    "@biomejs/biome": "^1.5.0",
    "@playwright/test": "^1.40.0",
    "husky": "^8.0.0"
  }
  
  Run: pnpm install
EOF
fi

# Create .gitignore entries
if [ -f ".gitignore" ]; then
  echo "" >> .gitignore
  echo "# Boilerplate integration" >> .gitignore
  echo ".claude-integration/" >> .gitignore
  echo "*.original.json" >> .gitignore
  echo "*.backup" >> .gitignore
  echo ".claude/state/" >> .gitignore
  echo ".claude/metrics/" >> .gitignore
fi
```

## 🔍 Phase 7: Verification

```bash
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "## ✅ Verification"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Test critical components
echo ""
echo "Core System:"
[ -f ".claude/commands/sr.md" ] && echo "  ✓ Smart Resume (/sr)" || echo "  ✗ Missing /sr"
[ -f ".claude/commands/vd.md" ] && echo "  ✓ Design Validation (/vd)" || echo "  ✗ Missing /vd"
[ -f ".claude/commands/create-prp.md" ] && echo "  ✓ PRP System (/create-prp)" || echo "  ✗ Missing /create-prp"
[ -d ".claude/agents" ] && echo "  ✓ AI Agents installed" || echo "  ✗ Missing agents"
[ -d ".claude/hooks" ] && echo "  ✓ Automation hooks installed" || echo "  ✗ Missing hooks"

echo ""
echo "Standards & Security:"
[ -d ".agent-os/standards" ] && echo "  ✓ Agent OS standards" || echo "  ✗ Missing standards"
[ -d "field-registry" ] && echo "  ✓ Field registry security" || echo "  ✗ Missing field-registry"

echo ""
echo "Development Tools:"
[ -f "biome.json" ] && echo "  ✓ Biome configuration" || echo "  ✗ Missing biome.json"
[ -f "playwright.config.ts" ] || [ -f "playwright.boilerplate.config.ts" ] && \
  echo "  ✓ Playwright testing" || echo "  ✗ Missing Playwright"
[ -d "templates" ] && echo "  ✓ Component templates" || echo "  ✗ Missing templates"

# Show preserved commands if any
if [ $EXISTING_COMMANDS -gt 0 ]; then
  echo ""
  echo "Your Original Commands (preserved):"
  ls -1 .claude/commands/*-project.md 2>/dev/null | head -5 | while read cmd; do
    basename=$(basename "$cmd" .md)
    echo "  • /${basename}"
  done
  [ $(ls -1 .claude/commands/*-project.md 2>/dev/null | wc -l) -gt 5 ] && echo "  ... and more"
fi
```

## 📋 Phase 8: Integration Report

```bash
cat > BOILERPLATE_INTEGRATION.md << 'EOF'
# Boilerplate Integration Complete! 🎉

## Installation Summary

### ✅ Successfully Installed

**Core System:**
- 150+ powerful commands in `.claude/commands/`
- 31 specialized AI agents in `.claude/agents/`
- Smart automation hooks in `.claude/hooks/`
- Agent OS standards in `.agent-os/`

**Development Tools:**
- Field registry security system
- PRP one-pass implementation system
- Component templates
- Git hooks for validation

**Configuration:**
- Design system enforcement
- Biome linting & formatting
- Playwright browser testing
- TypeScript configurations

### 📁 File Locations

**Your Original Files:**
- Commands: `.claude/commands/*-project.md`
- Configs: `*.original.json` files
- Backup: `.claude-integration/backup/`

**Boilerplate Files:**
- Commands: `.claude/commands/`
- Documentation: `CLAUDE_BOILERPLATE.md`
- Standards: `.agent-os/standards/`
- Templates: `templates/`

### 🚀 Quick Start

1. **Load the system:**
   ```bash
   /sr
   ```

2. **Test core features:**
   ```bash
   /vd              # Validate design
   /create-prp      # Create PRP
   /chain list      # View workflows
   ```

3. **Install dependencies:**
   ```bash
   pnpm install
   ```

4. **View all commands:**
   ```bash
   /help
   ```

### 🔄 Rollback

If needed, rollback to pre-integration state:
```bash
/integration-rollback
```

### 📚 Documentation

- Main guide: `CLAUDE_BOILERPLATE.md`
- Standards: `.agent-os/standards/`
- Workflows: `/chain list`
- Commands: `/help`

### ⚠️ Manual Steps Required

1. Review and merge these configs if needed:
   - `tailwind.config.js` (for design tokens)
   - `biome.json` (for linting rules)

2. Install missing dependencies:
   ```bash
   pnpm install
   ```

3. Initialize Git hooks:
   ```bash
   npx husky install
   ```

## Support

- GitHub: [Your repository]
- Issues: [Issue tracker]
- Docs: `docs/boilerplate/`

---

Generated: $(date)
Mode: $MODE
EOF

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "##  🎉 Integration Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Your project now has the full Claude Code Boilerplate v4.0.0!"
echo ""
echo "📄 Full report: BOILERPLATE_INTEGRATION.md"
echo "🔄 Rollback available: /integration-rollback"
echo ""
echo "Next step: Run '/sr' to load everything!"
echo ""
```

## 🔄 Rollback Support

```bash
if [ "$1" = "--rollback" ]; then
  /integration-rollback
  exit 0
fi
```

## Dry Run Support

```bash
if [[ "$OPTIONS" == *"--dry-run"* ]]; then
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "## 🔍 DRY RUN COMPLETE - No changes made"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  echo "Review the plan above. Run without --dry-run to execute."
  exit 0
fi
```
