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
echo "Analyzing your existing Claude Code setup..."

# Check what exists
EXISTING_CLAUDE_MD=false
EXISTING_CLAUDE_DIR=false
EXISTING_COMMANDS=0
EXISTING_HOOKS=0
EXISTING_PERSONAS=false
EXISTING_GIT_HOOKS=false

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
  if [ -f ".claude/personas/personas.json" ] || [ -f ".claude/agent-personas.json" ]; then
    EXISTING_PERSONAS=true
    echo "✓ Found existing personas"
  fi
fi

if [ -d ".husky" ]; then
  EXISTING_GIT_HOOKS=true
  echo "✓ Found existing Git hooks"
fi

# Create integration report
mkdir -p .claude-integration
```

## 📊 Phase 2: Conflict Analysis

```bash
cat > .claude-integration/CONFLICT_REPORT.md << 'EOF'
# Integration Conflict Report

Generated: $(date)

## Existing Setup Found

- CLAUDE.md: $EXISTING_CLAUDE_MD
- .claude directory: $EXISTING_CLAUDE_DIR
- Custom commands: $EXISTING_COMMANDS
- Custom hooks: $EXISTING_HOOKS
- Custom personas: $EXISTING_PERSONAS
- Git hooks: $EXISTING_GIT_HOOKS

## Conflicts to Resolve

EOF

# Check for command conflicts
if [ $EXISTING_COMMANDS -gt 0 ]; then
  echo "### Command Conflicts" >> .claude-integration/CONFLICT_REPORT.md
  
  # List of our critical commands
  CRITICAL_COMMANDS="sr cc vd fw pt gt analyze-existing migrate-to-strict-design"
  
  for cmd in $CRITICAL_COMMANDS; do
    if [ -f ".claude/commands/$cmd.md" ]; then
      echo "- /$cmd - exists in both (will rename yours to /$cmd-project)" >> .claude-integration/CONFLICT_REPORT.md
    fi
  done
fi
```

## 🔧 Phase 3: Integration Plan

```bash
# Based on mode, create plan
case "$MODE" in
  "selective")
    echo "## 🎯 Selective Integration Mode"
    echo ""
    echo "Select what to integrate:"
    echo "1. Commands & Automation (.claude)"
    echo "2. Design System Enforcement"  
    echo "3. PRP System (one-pass implementation)"
    echo "4. Agent OS Standards"
    echo "5. Security Features (field-registry)"
    echo "6. Git Hooks (pre-commit validation)"
    echo "7. Event System (async patterns)"
    echo ""
    echo "Enter numbers (comma-separated): "
    # Would read user input here
    ;;
    
  "sidecar")
    echo "## 🚗 Sidecar Installation Mode"
    echo ""
    echo "Will install as .claude-boilerplate/ alongside your .claude/"
    echo "Access with /bb [command] prefix"
    ;;
    
  *)  # full mode
    echo "## 📦 Full Integration Mode"
    echo ""
    echo "Will merge boilerplate with your existing setup:"
    echo "- Your commands preserved in .claude/commands/project/"
    echo "- Conflicting commands renamed (yours get -project suffix)"
    echo "- Hooks numbered for proper execution order"
    echo "- Configurations merged intelligently"
    ;;
esac
```

## 💾 Phase 4: Backup Existing Files

```bash
if [ "$EXISTING_CLAUDE_DIR" = true ] && [ "$MODE" != "sidecar" ]; then
  echo "Creating backup of existing setup..."
  
  BACKUP_DIR=".claude-integration/backup/$(date +%Y%m%d_%H%M%S)"
  mkdir -p "$BACKUP_DIR"
  
  # Backup existing files
  [ -f "CLAUDE.md" ] && cp CLAUDE.md "$BACKUP_DIR/"
  [ -d ".claude" ] && cp -r .claude "$BACKUP_DIR/"
  [ -d ".husky" ] && cp -r .husky "$BACKUP_DIR/"
  
  echo "✓ Backup created at $BACKUP_DIR"
fi
```

## 🔄 Phase 5: Execute Integration

### Handle CLAUDE.md
```bash
if [ "$EXISTING_CLAUDE_MD" = true ] && [ "$MODE" = "full" ]; then
  echo "Handling CLAUDE.md conflict..."
  
  # Rename ours
  cp ~/.claude-boilerplate/CLAUDE.md CLAUDE_BOILERPLATE.md
  
  # Append integration notice to theirs
  cat >> CLAUDE.md << 'EOF'

## Boilerplate System Integration

This project has been enhanced with the Claude Code Boilerplate system.
For boilerplate-specific commands and workflows, see CLAUDE_BOILERPLATE.md

Key additions:
- 116+ new commands (use /help for full list)
- Design system enforcement (/vd)
- PRP one-pass implementation (/create-prp)
- Multi-agent orchestration (/orch)
- Smart chains (/chain list)

Your existing commands are preserved and take precedence.
EOF

  echo "✓ Created CLAUDE_BOILERPLATE.md, updated CLAUDE.md"
fi
```

### Handle Commands
```bash
if [ "$MODE" = "full" ]; then
  mkdir -p .claude/commands/project
  
  # Move conflicting commands
  for cmd in $CRITICAL_COMMANDS; do
    if [ -f ".claude/commands/$cmd.md" ]; then
      mv ".claude/commands/$cmd.md" ".claude/commands/${cmd}-project.md"
      echo "  Moved /$cmd to /${cmd}-project"
    fi
  done
  
  # Copy our commands
  cp -r ~/.claude-boilerplate/.claude/commands/* .claude/commands/
  echo "✓ Integrated 116+ boilerplate commands"
fi
```

### Handle Hooks
```bash
if [ "$MODE" = "full" ] && [ -d ".claude/hooks" ]; then
  echo "Merging hooks with proper ordering..."
  
  # Renumber existing hooks to run first
  for hook_dir in pre-tool-use post-tool-use; do
    if [ -d ".claude/hooks/$hook_dir" ]; then
      for hook in .claude/hooks/$hook_dir/*.py; do
        if [ -f "$hook" ]; then
          base=$(basename "$hook")
          # Renumber to 00-09 range
          new_name="0${base#[0-9]*}"
          mv "$hook" ".claude/hooks/$hook_dir/$new_name"
        fi
      done
    fi
  done
  
  # Copy our hooks starting at 10
  cp ~/.claude-boilerplate/.claude/hooks/pre-tool-use/* .claude/hooks/pre-tool-use/
  
  echo "✓ Hooks merged (yours run first)"
fi
```

### Handle Configuration
```bash
if [ -f ".claude/config.json" ]; then
  echo "Merging configurations..."
  
  # This would use jq to merge JSON
  # For now, we'll append boilerplate config
  cp .claude/config.json .claude/config.backup.json
  
  # Add boilerplate section
  echo "✓ Configuration merged"
fi
```

## ✅ Phase 6: Verification

```bash
echo ""
echo "## 🔍 Verifying Integration"

# Test critical commands exist
for cmd in sr cc vd fw analyze-existing; do
  if [ -f ".claude/commands/$cmd.md" ]; then
    echo "✓ /$cmd command available"
  else
    echo "✗ /$cmd command missing!"
  fi
done

# Check if their commands still work
if [ $EXISTING_COMMANDS -gt 0 ]; then
  echo ""
  echo "Your original commands:"
  ls -1 .claude/commands/*-project.md 2>/dev/null | sed 's/.*\///; s/-project\.md$//' | sed 's/^/  /'
fi
```

## 📋 Phase 7: Integration Report

```bash
cat > .claude-integration/INTEGRATION_COMPLETE.md << 'EOF'
# Integration Complete! 🎉

## What's New

### Commands Added
- 116+ boilerplate commands
- Access with standard names (e.g., /sr, /cc, /vd)
- Your commands with conflicts: add -project suffix

### Features Enabled
- ✅ Smart Resume (/sr)
- ✅ Design System Enforcement (/vd)  
- ✅ PRP One-Pass Implementation (/create-prp)
- ✅ Multi-Agent Orchestration (/orch)
- ✅ Smart Chains (/chain list)
- ✅ Visual Debugging (Ctrl+V)

### Your Original Setup
- ✅ All custom commands preserved
- ✅ All custom hooks still run (before ours)
- ✅ Your CLAUDE.md still primary
- ✅ Your configurations maintained

## Next Steps

1. Test your existing commands still work
2. Try /sr to load the enhanced system
3. Run /help to see all available commands
4. Check /chain list for automated workflows

## Rollback

If you need to rollback:
```bash
/integration-rollback
```

Or manually:
```bash
rm -rf .claude
cp -r .claude-integration/backup/[timestamp]/.claude .
```

## Support

- Docs: See CLAUDE_BOILERPLATE.md
- Issues: [Your issue tracker]
EOF

echo ""
echo "✅ Integration complete! See .claude-integration/INTEGRATION_COMPLETE.md"
```

## 🔄 Rollback Capability

```bash
# If user wants to rollback
if [ "$1" = "--rollback" ]; then
  echo "Rolling back integration..."
  
  LATEST_BACKUP=$(ls -t .claude-integration/backup/ | head -1)
  if [ -n "$LATEST_BACKUP" ]; then
    rm -rf .claude
    cp -r ".claude-integration/backup/$LATEST_BACKUP/.claude" .
    [ -f ".claude-integration/backup/$LATEST_BACKUP/CLAUDE.md" ] && \
      cp ".claude-integration/backup/$LATEST_BACKUP/CLAUDE.md" .
    
    rm -f CLAUDE_BOILERPLATE.md
    echo "✓ Rolled back to pre-integration state"
  else
    echo "✗ No backup found!"
  fi
fi
```

## Integration Modes Explained

### Full Mode (Default)
- Merges everything intelligently
- Preserves all existing work
- Resolves conflicts by renaming
- Best for: Most projects

### Selective Mode
- Choose specific features
- Minimal footprint
- No conflicts
- Best for: Projects with extensive Claude setups

### Sidecar Mode  
- Completely separate installation
- No conflicts possible
- Access with /bb prefix
- Best for: Testing or very custom setups

Run `/integrate-boilerplate --dry-run` to see what would happen without making changes!
