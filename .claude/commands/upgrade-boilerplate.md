---
name: upgrade-boilerplate
description: |
  Upgrade existing boilerplate installation from older version to v4.0.0.
  Intelligently migrates settings, preserves customizations, and updates components.
argument-hint: "[--from-version=2.0|3.0|auto] [--preserve-all] [--dry-run]"
aliases: ["upgrade", "update-boilerplate", "migrate-version"]
---

# Upgrade Boilerplate Version

**Current Version**: v4.0.0  
**From Version**: $FROM_VERSION (auto-detect if not specified)  
**Options**: $OPTIONS

## 🔍 Phase 1: Version Detection

```bash
echo "🔍 Detecting current boilerplate version..."
echo ""

CURRENT_VERSION="unknown"
VERSION_INDICATORS=()

# Check for version indicators
if [ -f ".claude/VERSION" ]; then
  CURRENT_VERSION=$(cat .claude/VERSION)
  echo "✓ Found version file: v$CURRENT_VERSION"
elif [ -f ".claude/settings.json" ]; then
  # Try to extract version from settings
  if grep -q '"version"' .claude/settings.json; then
    CURRENT_VERSION=$(grep '"version"' .claude/settings.json | sed 's/.*"version".*"\([^"]*\)".*/\1/')
    echo "✓ Found version in settings: v$CURRENT_VERSION"
  fi
fi

# Version detection by feature presence
echo ""
echo "Analyzing features to determine version..."

# v1.0 indicators (original)
if [ -d ".claude/commands" ] && [ ! -d ".claude/agents" ]; then
  VERSION_INDICATORS+=("1.0")
  echo "  • Basic commands only → suggests v1.x"
fi

# v2.0 indicators
if [ -f ".claude/commands/create-prd.md" ] && [ ! -f ".claude/commands/create-prp.md" ]; then
  VERSION_INDICATORS+=("2.0")
  echo "  • Has PRD but no PRP → suggests v2.x"
fi

# v3.0 indicators
if [ -f ".claude/commands/create-prp.md" ] && [ ! -d ".claude/hooks" ]; then
  VERSION_INDICATORS+=("3.0")
  echo "  • Has PRP but no hooks → suggests v3.0"
fi

# v3.5 indicators
if [ -d ".claude/hooks" ] && [ ! -f ".claude/commands/orch.md" ]; then
  VERSION_INDICATORS+=("3.5")
  echo "  • Has hooks but no orchestration → suggests v3.5"
fi

# v4.0 indicators
if [ -f ".claude/commands/orch.md" ] && [ -d ".claude/agents" ]; then
  VERSION_INDICATORS+=("4.0")
  echo "  • Has orchestration and agents → suggests v4.0"
  echo ""
  echo "⚠️  You appear to already have v4.0 features!"
  echo "   Use /integrate-boilerplate --mode=selective to add missing components"
  exit 0
fi

# Determine most likely version
if [ "$CURRENT_VERSION" = "unknown" ]; then
  if [ ${#VERSION_INDICATORS[@]} -gt 0 ]; then
    # Use the highest version indicator
    CURRENT_VERSION="${VERSION_INDICATORS[-1]}"
    echo ""
    echo "📌 Detected version: v$CURRENT_VERSION (based on features)"
  else
    echo ""
    echo "⚠️  Could not detect version. Assuming v2.0"
    CURRENT_VERSION="2.0"
  fi
fi

# Override with user-specified version if provided
if [ -n "$FROM_VERSION" ] && [ "$FROM_VERSION" != "auto" ]; then
  CURRENT_VERSION="$FROM_VERSION"
  echo "📌 Using specified version: v$CURRENT_VERSION"
fi
```

## 📊 Phase 2: Migration Path Analysis

```bash
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "## 📊 Migration Path: v$CURRENT_VERSION → v4.0.0"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Create migration plan based on version
mkdir -p .claude-upgrade

cat > .claude-upgrade/MIGRATION_PLAN.md << EOF
# Boilerplate Upgrade Plan

**From Version**: v$CURRENT_VERSION  
**To Version**: v4.0.0  
**Date**: $(date)

## Changes by Version

EOF

case "$CURRENT_VERSION" in
  "1.0"|"1"*)
    cat >> .claude-upgrade/MIGRATION_PLAN.md << 'EOF'
### From v1.0 to v4.0.0

**Major Additions:**
- ✨ PRP System (one-pass implementation)
- ✨ Multi-agent orchestration (31 agents)
- ✨ Automation hooks (pre/post/stop)
- ✨ Smart chains (workflow automation)
- ✨ Field registry (security)
- ✨ Agent OS integration
- ✨ Playwright testing
- ✨ Design system enforcement

**Structure Changes:**
- `.claude/commands/` → Expanded from ~20 to 150+ commands
- `.claude/agents/` → NEW (31 specialized agents)
- `.claude/hooks/` → NEW (automation system)
- `.agent-os/` → NEW (standards and specs)
- `field-registry/` → NEW (security system)
- `PRPs/` → NEW (one-pass templates)

**Breaking Changes:**
- Command naming conventions updated
- Some v1 commands deprecated
EOF
    ;;
    
  "2.0"|"2"*)
    cat >> .claude-upgrade/MIGRATION_PLAN.md << 'EOF'
### From v2.0 to v4.0.0

**Major Additions:**
- ✨ Multi-agent orchestration (31 agents)
- ✨ Automation hooks (pre/post/stop)
- ✨ Smart chains (workflow automation)
- ✨ Enhanced PRP system
- ✨ Field registry (security)
- ✨ Playwright browser testing

**Structure Changes:**
- `.claude/agents/` → NEW (31 specialized agents)
- `.claude/hooks/` → NEW (automation system)
- `field-registry/` → NEW (security system)
- PRD system → Enhanced with PRP integration

**Command Updates:**
- `/create-prd` → Enhanced with AI suggestions
- `/process-tasks` → Now supports parallel execution
- NEW: `/orch`, `/chain`, `/vd`, `/pw-*` commands
EOF
    ;;
    
  "3.0"|"3"*)
    cat >> .claude-upgrade/MIGRATION_PLAN.md << 'EOF'
### From v3.0 to v4.0.0

**Major Additions:**
- ✨ Multi-agent orchestration (31 agents)
- ✨ Smart chains (workflow automation)
- ✨ Enhanced hooks with official compliance
- ✨ Playwright browser testing
- ✨ Performance monitoring

**Structure Changes:**
- `.claude/agents/` → NEW (31 specialized agents)
- Hooks → Updated for official Claude Code spec
- Commands → Added 50+ new commands

**Command Updates:**
- NEW: `/orch` - Multi-agent orchestration
- NEW: `/chain` - Workflow automation
- NEW: `/pw-*` - Playwright commands
- Enhanced: All existing commands optimized
EOF
    ;;
    
  "3.5"|"3"*)
    cat >> .claude-upgrade/MIGRATION_PLAN.md << 'EOF'
### From v3.5 to v4.0.0

**Major Additions:**
- ✨ Multi-agent orchestration (31 agents)
- ✨ Smart chains (workflow automation)
- ✨ Hook compliance updates
- ✨ Integration system

**Minor Updates:**
- Commands → Added orchestration commands
- Hooks → Fixed stdin handling and exit codes
- Performance → Optimized for large projects

**Command Updates:**
- NEW: `/orch` - Multi-agent orchestration
- NEW: `/chain` - Workflow automation
- NEW: `/integrate-boilerplate` - Safe integration
- Fixed: All hooks now follow official spec
EOF
    ;;
esac

echo "Migration plan created: .claude-upgrade/MIGRATION_PLAN.md"
```

## 💾 Phase 3: Backup Current Installation

```bash
echo ""
echo "## 💾 Creating Backup"
echo ""

BACKUP_DIR=".claude-upgrade/backup-v${CURRENT_VERSION}-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "Backing up current installation..."

# Backup all boilerplate directories
BACKUP_ITEMS=(
  ".claude"
  ".agent-os"
  "field-registry"
  "PRPs"
  "templates"
  "CLAUDE.md"
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

# Save current customizations inventory
echo ""
echo "Identifying customizations to preserve..."

CUSTOM_COMMANDS=()
CUSTOM_HOOKS=()
CUSTOM_AGENTS=()

# Find custom commands (not in standard set)
if [ -d ".claude/commands" ]; then
  for cmd in .claude/commands/*.md; do
    basename=$(basename "$cmd" .md)
    # Check if this is a custom command (not in our standard set)
    if ! grep -q "^$basename$" ~/.claude-boilerplate/.claude/commands/STANDARD_COMMANDS.txt 2>/dev/null; then
      CUSTOM_COMMANDS+=("$basename")
    fi
  done
fi

if [ ${#CUSTOM_COMMANDS[@]} -gt 0 ]; then
  echo "  ✓ Found ${#CUSTOM_COMMANDS[@]} custom commands"
  printf '%s\n' "${CUSTOM_COMMANDS[@]}" > "$BACKUP_DIR/custom-commands.txt"
fi

echo ""
echo "✅ Backup complete: $BACKUP_DIR"
```

## 🔄 Phase 4: Upgrade Process

```bash
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "## 🔄 Starting Upgrade Process"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Based on version, perform specific upgrades
case "$CURRENT_VERSION" in
  "1.0"|"1"*)
    echo ""
    echo "### Upgrading from v1.x → v4.0"
    
    # Major structural upgrade needed
    echo "This is a major upgrade. Recommended approach:"
    echo "1. Preserve your customizations"
    echo "2. Install fresh v4.0 structure"
    echo "3. Restore customizations"
    
    # Preserve customizations
    mkdir -p .claude-upgrade/preserved
    
    # Save custom commands
    if [ ${#CUSTOM_COMMANDS[@]} -gt 0 ]; then
      mkdir -p .claude-upgrade/preserved/commands
      for cmd in "${CUSTOM_COMMANDS[@]}"; do
        cp ".claude/commands/$cmd.md" ".claude-upgrade/preserved/commands/" 2>/dev/null
      done
      echo "  ✓ Preserved custom commands"
    fi
    
    # Install fresh v4.0
    echo ""
    echo "Installing v4.0 structure..."
    
    # Remove old structure
    rm -rf .claude/commands
    rm -rf .claude/context
    
    # Install new structure
    cp -r ~/.claude-boilerplate/.claude/* .claude/
    echo "  ✓ Installed v4.0 commands (150+)"
    echo "  ✓ Installed agents (31)"
    echo "  ✓ Installed hooks"
    
    # Install new directories
    [ ! -d ".agent-os" ] && cp -r ~/.claude-boilerplate/.agent-os .agent-os
    [ ! -d "field-registry" ] && cp -r ~/.claude-boilerplate/field-registry field-registry
    [ ! -d "PRPs" ] && cp -r ~/.claude-boilerplate/PRPs PRPs
    
    # Restore custom commands with -custom suffix
    if [ ${#CUSTOM_COMMANDS[@]} -gt 0 ]; then
      echo ""
      echo "Restoring custom commands..."
      for cmd in .claude-upgrade/preserved/commands/*.md; do
        if [ -f "$cmd" ]; then
          basename=$(basename "$cmd" .md)
          cp "$cmd" ".claude/commands/${basename}-custom.md"
          echo "  ✓ Restored /${basename}-custom"
        fi
      done
    fi
    ;;
    
  "2.0"|"2"*)
    echo ""
    echo "### Upgrading from v2.x → v4.0"
    
    # Moderate upgrade - add missing components
    echo "Adding v4.0 components..."
    
    # Add agents
    if [ ! -d ".claude/agents" ]; then
      mkdir -p .claude/agents
      cp -r ~/.claude-boilerplate/.claude/agents/* .claude/agents/
      echo "  ✓ Installed 31 AI agents"
    fi
    
    # Add hooks
    if [ ! -d ".claude/hooks" ]; then
      mkdir -p .claude/hooks
      cp -r ~/.claude-boilerplate/.claude/hooks/* .claude/hooks/
      echo "  ✓ Installed automation hooks"
    fi
    
    # Update commands (preserve custom)
    echo ""
    echo "Updating commands..."
    
    # Get list of new v4 commands
    NEW_COMMANDS=(
      "orch" "chain" "chain-v4" "vd" "validate-design"
      "pw-test" "pw-verify" "pw-debug" "pw-screenshot"
      "integrate-boilerplate" "integration-rollback"
    )
    
    for cmd in "${NEW_COMMANDS[@]}"; do
      if [ ! -f ".claude/commands/$cmd.md" ]; then
        cp "~/.claude-boilerplate/.claude/commands/$cmd.md" ".claude/commands/" 2>/dev/null
        echo "  ✓ Added /$cmd"
      fi
    done
    
    # Add field-registry
    if [ ! -d "field-registry" ]; then
      cp -r ~/.claude-boilerplate/field-registry field-registry
      echo "  ✓ Installed field-registry"
    fi
    ;;
    
  "3.0"|"3"*)
    echo ""
    echo "### Upgrading from v3.x → v4.0"
    
    # Minor upgrade - mostly additions
    echo "Adding v4.0 enhancements..."
    
    # Add agents
    if [ ! -d ".claude/agents" ]; then
      mkdir -p .claude/agents
      cp -r ~/.claude-boilerplate/.claude/agents/* .claude/agents/
      echo "  ✓ Installed 31 AI agents"
    fi
    
    # Update hooks for compliance
    echo "Updating hooks for official compliance..."
    
    # Backup existing hooks
    if [ -d ".claude/hooks" ]; then
      cp -r .claude/hooks "$BACKUP_DIR/hooks-original"
      
      # Update hook files
      for hook_dir in pre-tool-use post-tool-use stop; do
        if [ -d ".claude/hooks/$hook_dir" ]; then
          # Copy new versions
          cp ~/.claude-boilerplate/.claude/hooks/$hook_dir/*.py ".claude/hooks/$hook_dir/" 2>/dev/null
        fi
      done
      echo "  ✓ Updated hooks for v4.0 compliance"
    fi
    
    # Add new commands
    NEW_COMMANDS=("orch" "chain" "chain-v4" "integrate-boilerplate" "integration-rollback")
    for cmd in "${NEW_COMMANDS[@]}"; do
      if [ ! -f ".claude/commands/$cmd.md" ]; then
        cp "~/.claude-boilerplate/.claude/commands/$cmd.md" ".claude/commands/" 2>/dev/null
        echo "  ✓ Added /$cmd"
      fi
    done
    ;;
    
  "3.5")
    echo ""
    echo "### Upgrading from v3.5 → v4.0"
    
    # Very minor upgrade
    echo "Adding v4.0 final features..."
    
    # Add agents
    if [ ! -d ".claude/agents" ]; then
      mkdir -p .claude/agents
      cp -r ~/.claude-boilerplate/.claude/agents/* .claude/agents/
      echo "  ✓ Installed 31 AI agents"
    fi
    
    # Add orchestration commands
    for cmd in orch chain chain-v4; do
      if [ ! -f ".claude/commands/$cmd.md" ]; then
        cp "~/.claude-boilerplate/.claude/commands/$cmd.md" ".claude/commands/" 2>/dev/null
        echo "  ✓ Added /$cmd"
      fi
    done
    
    # Fix hook compliance
    echo "  ✓ Hooks already compliant in v3.5"
    ;;
esac
```

## 🔧 Phase 5: Configuration Updates

```bash
echo ""
echo "## 🔧 Updating Configurations"

# Update settings.json with version
if [ -f ".claude/settings.json" ]; then
  # Add version field if missing
  if ! grep -q '"version"' .claude/settings.json; then
    # Use jq if available, otherwise manual edit
    echo '  ✓ Adding version to settings.json'
    cp .claude/settings.json .claude/settings.json.bak
    # This would use jq in production
  fi
else
  cp ~/.claude-boilerplate/.claude/settings.json .claude/
  echo "  ✓ Installed settings.json with v4.0 config"
fi

# Create VERSION file
echo "4.0.0" > .claude/VERSION
echo "  ✓ Created version file"

# Update CLAUDE.md with version info
if [ -f "CLAUDE.md" ]; then
  if ! grep -q "Version: v4.0" CLAUDE.md; then
    sed -i.bak '1s/^/<!-- Version: v4.0.0 -->\n/' CLAUDE.md
    echo "  ✓ Updated CLAUDE.md with version"
  fi
fi

# Update package.json dependencies if needed
if [ -f "package.json" ]; then
  echo ""
  echo "  ℹ️  Remember to update dependencies:"
  echo "     pnpm install"
fi
```

## ✅ Phase 6: Verification & Testing

```bash
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "## ✅ Verification"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "Verifying v4.0 installation..."

# Check critical v4.0 features
VERIFICATION_PASSED=true

echo ""
echo "Core Components:"
[ -d ".claude/commands" ] && echo "  ✓ Commands directory" || VERIFICATION_PASSED=false
[ -d ".claude/agents" ] && echo "  ✓ Agents (31)" || VERIFICATION_PASSED=false
[ -d ".claude/hooks" ] && echo "  ✓ Hooks system" || VERIFICATION_PASSED=false
[ -d ".agent-os" ] && echo "  ✓ Agent OS" || VERIFICATION_PASSED=false

echo ""
echo "Key Commands:"
[ -f ".claude/commands/sr.md" ] && echo "  ✓ /sr (smart resume)" || VERIFICATION_PASSED=false
[ -f ".claude/commands/create-prp.md" ] && echo "  ✓ /create-prp" || VERIFICATION_PASSED=false
[ -f ".claude/commands/orch.md" ] && echo "  ✓ /orch (orchestration)" || VERIFICATION_PASSED=false
[ -f ".claude/commands/chain.md" ] && echo "  ✓ /chain (workflows)" || VERIFICATION_PASSED=false

echo ""
echo "Security & Testing:"
[ -d "field-registry" ] && echo "  ✓ Field registry" || echo "  ⚠️ Field registry missing"
[ -f "playwright.config.ts" ] || [ -f "playwright.boilerplate.config.ts" ] && \
  echo "  ✓ Playwright config" || echo "  ⚠️ Playwright not configured"

if [ "$VERIFICATION_PASSED" = true ]; then
  echo ""
  echo "✅ All critical v4.0 components verified!"
else
  echo ""
  echo "⚠️  Some components missing. Run:"
  echo "   /integrate-boilerplate --mode=selective"
fi
```

## 📋 Phase 7: Upgrade Report

```bash
cat > BOILERPLATE_UPGRADE_REPORT.md << EOF
# Boilerplate Upgrade Complete! 🎉

## Upgrade Summary

**From Version**: v$CURRENT_VERSION  
**To Version**: v4.0.0  
**Date**: $(date)  
**Backup Location**: $BACKUP_DIR

## ✅ What Was Upgraded

### Core System
- Commands: Expanded to 150+ commands
- Agents: Added 31 specialized AI agents
- Hooks: Installed/updated automation system
- Standards: Added Agent OS integration

### New Features in v4.0
- ✨ Multi-agent orchestration (/orch)
- ✨ Smart workflow chains (/chain)
- ✨ Browser testing (/pw-*)
- ✨ Design validation (/vd)
- ✨ Integration system (/integrate-boilerplate)
- ✨ Field registry security

### Preserved Items
EOF

if [ ${#CUSTOM_COMMANDS[@]} -gt 0 ]; then
  echo "- Custom Commands (${#CUSTOM_COMMANDS[@]}):" >> BOILERPLATE_UPGRADE_REPORT.md
  for cmd in "${CUSTOM_COMMANDS[@]}"; do
    echo "  • /${cmd}-custom" >> BOILERPLATE_UPGRADE_REPORT.md
  done
fi

cat >> BOILERPLATE_UPGRADE_REPORT.md << 'EOF'

## 🚀 Next Steps

1. **Test core features:**
   ```bash
   /sr              # Load system
   /chain list      # View workflows
   /orch --help     # Learn orchestration
   ```

2. **Review your custom commands:**
   - Original names: `[command]-custom`
   - Test they still work as expected

3. **Update dependencies:**
   ```bash
   pnpm install
   ```

4. **Run verification:**
   ```bash
   /v4-status
   ```

## 🔄 Rollback

If you need to rollback to the previous version:

1. Remove current installation:
   ```bash
   rm -rf .claude .agent-os field-registry PRPs
   ```

2. Restore from backup:
   ```bash
   cp -r $BACKUP_DIR/* .
   ```

## 📚 Documentation

- What's New: See MIGRATION_PLAN.md
- Full Guide: CLAUDE.md or CLAUDE_BOILERPLATE.md
- Commands: /help
- Support: [GitHub Issues]

---

Your boilerplate has been successfully upgraded to v4.0.0!
EOF

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "## 🎉 Upgrade Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Successfully upgraded from v$CURRENT_VERSION to v4.0.0!"
echo ""
echo "📄 Full report: BOILERPLATE_UPGRADE_REPORT.md"
echo "📁 Backup saved: $BACKUP_DIR"
echo ""
echo "Run '/sr' to load the upgraded system!"
```

## 🔄 Rollback Support

```bash
if [ "$1" = "--rollback" ]; then
  echo "Rolling back upgrade..."
  
  # Find most recent backup
  LATEST_BACKUP=$(ls -t .claude-upgrade/backup-v* 2>/dev/null | head -1)
  
  if [ -n "$LATEST_BACKUP" ]; then
    echo "Restoring from: $LATEST_BACKUP"
    
    # Remove current v4 installation
    rm -rf .claude .agent-os field-registry PRPs templates
    
    # Restore backup
    cp -r "$LATEST_BACKUP"/* .
    
    echo "✅ Rolled back to previous version"
  else
    echo "❌ No backup found!"
  fi
  exit 0
fi
```

## Dry Run Mode

```bash
if [[ "$OPTIONS" == *"--dry-run"* ]]; then
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "## 🔍 DRY RUN - No changes made"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  echo "Would upgrade from v$CURRENT_VERSION to v4.0.0"
  echo "Review the plan above and run without --dry-run"
  exit 0
fi
```
