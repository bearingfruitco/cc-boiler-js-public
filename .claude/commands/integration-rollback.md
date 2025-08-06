---
name: integration-rollback
description: Rollback the boilerplate integration to previous state
aliases: ["rollback", "undo-integration"]
---

# Rollback Boilerplate Integration

## 🔄 Rolling Back Integration

```bash
echo "🔄 Starting rollback process..."

# Check for backup directory
if [ ! -d ".claude-integration/backup" ]; then
  echo "❌ No backup found! Cannot rollback."
  echo ""
  echo "The backup directory .claude-integration/backup/ doesn't exist."
  echo "This means either:"
  echo "  1. Integration was never run"
  echo "  2. Backup was manually deleted"
  echo "  3. Integration was run with --no-backup flag"
  exit 1
fi

# Find the most recent backup
LATEST_BACKUP=$(ls -t .claude-integration/backup/ | head -1)

if [ -z "$LATEST_BACKUP" ]; then
  echo "❌ No backup folders found in .claude-integration/backup/"
  exit 1
fi

echo "Found backup: $LATEST_BACKUP"
echo ""
echo "This will restore your project to the state before integration."
echo "Current boilerplate additions will be removed."
echo ""
echo "Press Enter to continue or Ctrl+C to cancel..."
read
```

## 📦 Phase 1: Remove Boilerplate Files

```bash
echo "Removing boilerplate files..."

# Remove boilerplate-specific files
[ -f "CLAUDE_BOILERPLATE.md" ] && rm -f CLAUDE_BOILERPLATE.md && echo "  ✓ Removed CLAUDE_BOILERPLATE.md"
[ -f "playwright.boilerplate.config.ts" ] && rm -f playwright.boilerplate.config.ts && echo "  ✓ Removed playwright.boilerplate.config.ts"
[ -d "docs/boilerplate" ] && rm -rf docs/boilerplate && echo "  ✓ Removed docs/boilerplate/"

# Remove directories that were added
if [ -f ".claude-integration/backup/$LATEST_BACKUP/.claude" ]; then
  # User had .claude before, restore it
  rm -rf .claude
  echo "  ✓ Removed current .claude directory"
else
  # User didn't have .claude before, but we need to be careful
  # Only remove if it looks like ours
  if [ -f ".claude/commands/sr.md" ]; then
    rm -rf .claude
    echo "  ✓ Removed boilerplate .claude directory"
  fi
fi

# Remove other boilerplate directories if they didn't exist before
if [ ! -d ".claude-integration/backup/$LATEST_BACKUP/.agent-os" ]; then
  [ -d ".agent-os" ] && rm -rf .agent-os && echo "  ✓ Removed .agent-os directory"
fi

if [ ! -d ".claude-integration/backup/$LATEST_BACKUP/field-registry" ]; then
  [ -d "field-registry" ] && rm -rf field-registry && echo "  ✓ Removed field-registry"
fi

if [ ! -d ".claude-integration/backup/$LATEST_BACKUP/templates" ]; then
  [ -d "templates" ] && rm -rf templates && echo "  ✓ Removed templates directory"
fi
```

## 🔄 Phase 2: Restore Original Files

```bash
echo ""
echo "Restoring original files from backup..."

BACKUP_PATH=".claude-integration/backup/$LATEST_BACKUP"

# Restore directories
if [ -d "$BACKUP_PATH/.claude" ]; then
  cp -r "$BACKUP_PATH/.claude" .
  echo "  ✓ Restored original .claude directory"
fi

if [ -d "$BACKUP_PATH/.agent-os" ]; then
  cp -r "$BACKUP_PATH/.agent-os" .
  echo "  ✓ Restored original .agent-os directory"
fi

if [ -d "$BACKUP_PATH/.husky" ]; then
  cp -r "$BACKUP_PATH/.husky" .
  echo "  ✓ Restored original .husky directory"
fi

if [ -d "$BACKUP_PATH/field-registry" ]; then
  cp -r "$BACKUP_PATH/field-registry" .
  echo "  ✓ Restored original field-registry"
fi

# Restore individual files
if [ -f "$BACKUP_PATH/CLAUDE.md" ]; then
  cp "$BACKUP_PATH/CLAUDE.md" CLAUDE.md
  echo "  ✓ Restored original CLAUDE.md"
fi

if [ -f "$BACKUP_PATH/biome.json" ]; then
  cp "$BACKUP_PATH/biome.json" biome.json
  echo "  ✓ Restored original biome.json"
fi

if [ -f "$BACKUP_PATH/playwright.config.ts" ]; then
  cp "$BACKUP_PATH/playwright.config.ts" playwright.config.ts
  echo "  ✓ Restored original playwright.config.ts"
fi

if [ -f "$BACKUP_PATH/.env.example" ]; then
  cp "$BACKUP_PATH/.env.example" .env.example
  echo "  ✓ Restored original .env.example"
fi

# Clean up any backup files created during integration
[ -f "biome.project.json" ] && rm -f biome.project.json
[ -f ".env.example.backup" ] && rm -f .env.example.backup
```

## ✅ Phase 3: Verification

```bash
echo ""
echo "Verifying rollback..."

# Check that boilerplate files are gone
BOILERPLATE_REMOVED=true

[ -f "CLAUDE_BOILERPLATE.md" ] && BOILERPLATE_REMOVED=false && echo "  ⚠️ CLAUDE_BOILERPLATE.md still exists"
[ -f ".claude/commands/sr.md" ] && [ ! -f "$BACKUP_PATH/.claude/commands/sr.md" ] && BOILERPLATE_REMOVED=false && echo "  ⚠️ Boilerplate commands may still exist"
[ -d "docs/boilerplate" ] && BOILERPLATE_REMOVED=false && echo "  ⚠️ docs/boilerplate/ still exists"

if [ "$BOILERPLATE_REMOVED" = true ]; then
  echo "  ✓ All boilerplate files removed"
fi

# Check that original files are restored
ORIGINALS_RESTORED=true

if [ -d "$BACKUP_PATH/.claude" ] && [ ! -d ".claude" ]; then
  ORIGINALS_RESTORED=false
  echo "  ⚠️ Original .claude directory not restored"
fi

if [ -f "$BACKUP_PATH/CLAUDE.md" ] && [ ! -f "CLAUDE.md" ]; then
  ORIGINALS_RESTORED=false
  echo "  ⚠️ Original CLAUDE.md not restored"
fi

if [ "$ORIGINALS_RESTORED" = true ]; then
  echo "  ✓ All original files restored"
fi
```

## 📋 Phase 4: Rollback Report

```bash
# Create rollback report
cat > .claude-integration/ROLLBACK_COMPLETE.md << EOF
# Rollback Complete

**Date**: $(date)
**Restored from**: $LATEST_BACKUP

## What Was Removed
- Boilerplate .claude commands and hooks
- CLAUDE_BOILERPLATE.md
- Agent OS standards (if added by integration)
- Field registry (if added by integration)
- Boilerplate documentation in docs/boilerplate/

## What Was Restored
- Your original .claude directory (if it existed)
- Your original CLAUDE.md (if it existed)
- Your original configuration files
- Your original Git hooks

## Current State
Your project is now in the same state as before the boilerplate integration.

## Next Steps

If you want to try integration again with different options:
\`\`\`bash
/integrate-boilerplate --mode=selective
\`\`\`

Or try sidecar mode for zero conflicts:
\`\`\`bash
/integrate-boilerplate --mode=sidecar
\`\`\`

## Backup Preserved
Your backup is still available at:
$BACKUP_PATH

EOF

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Rollback Complete!"
echo ""
echo "Your project has been restored to its pre-integration state."
echo "The backup is preserved at: $BACKUP_PATH"
echo ""
echo "Report saved to: .claude-integration/ROLLBACK_COMPLETE.md"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

## 🗑️ Optional: Clean Up Backups

```bash
echo ""
echo "Would you like to remove the backup directory to save space? (y/N)"
read -r REMOVE_BACKUP

if [ "$REMOVE_BACKUP" = "y" ] || [ "$REMOVE_BACKUP" = "Y" ]; then
  rm -rf .claude-integration/backup
  echo "✓ Backup directory removed"
else
  echo "✓ Backup preserved for future reference"
fi
```
