---
name: integration-rollback
description: Rollback boilerplate integration to pre-integration state
aliases: ["rollback-integration", "undo-integration"]
---

# Rollback Boilerplate Integration

## 🔄 Finding Latest Backup

```bash
if [ ! -d ".claude-integration/backup" ]; then
  echo "❌ No integration backup found!"
  echo "Cannot rollback without backup directory."
  exit 1
fi

# Find most recent backup
LATEST_BACKUP=$(ls -t .claude-integration/backup/ | head -1)

if [ -z "$LATEST_BACKUP" ]; then
  echo "❌ No backup folders found!"
  exit 1
fi

echo "Found backup: $LATEST_BACKUP"
echo ""
echo "This will restore:"
ls -la ".claude-integration/backup/$LATEST_BACKUP/"
echo ""
echo "⚠️  This will REMOVE all boilerplate additions!"
echo "Continue? (y/n)"
```

## 🗑️ Removing Boilerplate Additions

```bash
# Assuming user confirmed...

echo "Removing boilerplate files..."

# Remove our added files
rm -f CLAUDE_BOILERPLATE.md
rm -rf .agent-os
rm -rf PRPs
rm -rf field-registry

# Remove .claude directory (will restore from backup)
rm -rf .claude
```

## 📦 Restoring Your Original Setup

```bash
echo "Restoring your original files..."

# Restore .claude directory
if [ -d ".claude-integration/backup/$LATEST_BACKUP/.claude" ]; then
  cp -r ".claude-integration/backup/$LATEST_BACKUP/.claude" .
  echo "✓ Restored .claude directory"
fi

# Restore CLAUDE.md if it was modified
if [ -f ".claude-integration/backup/$LATEST_BACKUP/CLAUDE.md" ]; then
  cp ".claude-integration/backup/$LATEST_BACKUP/CLAUDE.md" .
  echo "✓ Restored CLAUDE.md"
fi

# Restore .husky if it existed
if [ -d ".claude-integration/backup/$LATEST_BACKUP/.husky" ]; then
  rm -rf .husky
  cp -r ".claude-integration/backup/$LATEST_BACKUP/.husky" .
  echo "✓ Restored Git hooks"
fi
```

## ✅ Verification

```bash
echo ""
echo "## Rollback Complete!"
echo ""
echo "Restored to pre-integration state from: $LATEST_BACKUP"
echo ""
echo "Your original setup:"

# Show what's restored
if [ -d ".claude/commands" ]; then
  COMMAND_COUNT=$(ls -1 .claude/commands/*.md 2>/dev/null | wc -l)
  echo "- Commands: $COMMAND_COUNT"
fi

if [ -f "CLAUDE.md" ]; then
  echo "- CLAUDE.md: ✓"
fi

if [ -d ".husky" ]; then
  echo "- Git hooks: ✓"
fi

echo ""
echo "The boilerplate has been completely removed."
echo "Your project is back to its original Claude Code setup."
```

## 💡 Next Steps

If you want to try integration again with different options:

```bash
# Try selective mode (choose specific features)
/integrate-boilerplate --mode=selective

# Try sidecar mode (no conflicts)
/integrate-boilerplate --mode=sidecar

# Do a dry run first
/integrate-boilerplate --dry-run
```

The backup is preserved at `.claude-integration/backup/$LATEST_BACKUP/` for safety.
