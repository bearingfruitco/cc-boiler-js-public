#!/bin/bash
# rollback-v3.sh - Enhanced rollback with verification for v3.0

set -euo pipefail  # Fail fast on errors

echo "🔄 Claude Code Boilerplate v3.0 Rollback Script"
echo "=============================================="

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$(dirname "$SCRIPT_DIR")"

# Pre-rollback checks
echo "🔍 Pre-rollback verification..."
if [[ ! -f "$CLAUDE_DIR/backups/chains.v2.8.0.json" ]]; then
    echo "❌ ERROR: v2.8.0 backup files not found!"
    echo "Please ensure backup files exist in $CLAUDE_DIR/backups/"
    exit 1
fi

# Version detection
if [[ -f "$CLAUDE_DIR/version.json" ]]; then
    CURRENT_VERSION=$(grep -o '"version": "[^"]*"' "$CLAUDE_DIR/version.json" | cut -d'"' -f4)
    echo "📌 Current version: $CURRENT_VERSION"
else
    echo "⚠️  No version file found, assuming v3.0"
    CURRENT_VERSION="3.0.0"
fi

# Create rollback point
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$CLAUDE_DIR/backups/rollback/v3_state_$TIMESTAMP"

# Full state backup
echo "📦 Creating complete v3.0 state backup..."
mkdir -p "$BACKUP_DIR"/{agents,commands,scripts,metrics,temp,hooks}

# Backup v3.0 agents with verification
echo "  - Backing up v3.0 agents..."
for pattern in "*-specialist.md" "*-engineer.md" "*-compliance.md" "*-deployment.md" "*-schema.md" "*-systems.md"; do
    find "$CLAUDE_DIR/agents" -name "$pattern" -exec cp -v {} "$BACKUP_DIR/agents/" \; 2>/dev/null || true
done

# Backup current configuration
echo "  - Backing up current configuration..."
cp -v "$CLAUDE_DIR/chains.json" "$BACKUP_DIR/chains.v3.json"
cp -v "$CLAUDE_DIR/aliases.json" "$BACKUP_DIR/aliases.v3.json"
cp -v "$CLAUDE_DIR/settings.json" "$BACKUP_DIR/settings.v3.json" 2>/dev/null || true

# Backup v3.0 specific commands
echo "  - Backing up v3.0 commands..."
for cmd in analyze-task orchestrate share-context test-v3 agent-health; do
    if [[ -f "$CLAUDE_DIR/commands/$cmd.md" ]]; then
        cp -v "$CLAUDE_DIR/commands/$cmd.md" "$BACKUP_DIR/commands/" 2>/dev/null || true
    fi
    if [[ -f "$CLAUDE_DIR/commands/$cmd.py" ]]; then
        cp -v "$CLAUDE_DIR/commands/$cmd.py" "$BACKUP_DIR/commands/" 2>/dev/null || true
    fi
done

# Backup metrics and temp files
echo "  - Backing up metrics and temporary files..."
if [[ -d "$CLAUDE_DIR/metrics" ]]; then
    cp -rv "$CLAUDE_DIR/metrics/" "$BACKUP_DIR/metrics/" 2>/dev/null || true
fi

# State verification
echo ""
echo "✅ Verifying backup integrity..."
AGENT_COUNT=$(find "$BACKUP_DIR/agents" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
COMMAND_COUNT=$(find "$BACKUP_DIR/commands" -name "*.*" 2>/dev/null | wc -l | tr -d ' ')
echo "   - Backed up $AGENT_COUNT v3.0 agents"
echo "   - Backed up $COMMAND_COUNT v3.0 commands"
echo "   - Backup location: $BACKUP_DIR"

# Confirm rollback
echo ""
echo "⚠️  This will restore the system to v2.8.0"
read -p "Are you sure you want to continue? (y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Rollback cancelled"
    exit 0
fi

# Perform rollback
echo ""
echo "♻️  Rolling back to v2.8.0..."

# Restore v2.8.0 configuration
echo "  - Restoring v2.8.0 configuration..."
cp -v "$CLAUDE_DIR/backups/chains.v2.8.0.json" "$CLAUDE_DIR/chains.json"
cp -v "$CLAUDE_DIR/backups/aliases.v2.8.0.json" "$CLAUDE_DIR/aliases.json"

# Remove v3.0 agents
echo "  - Removing v3.0 agents..."
rm -f "$CLAUDE_DIR/agents/supabase-specialist.md"
rm -f "$CLAUDE_DIR/agents/orm-specialist.md"
rm -f "$CLAUDE_DIR/agents/analytics-engineer.md"
rm -f "$CLAUDE_DIR/agents/ui-systems.md"
rm -f "$CLAUDE_DIR/agents/privacy-compliance.md"
rm -f "$CLAUDE_DIR/agents/event-schema.md"
rm -f "$CLAUDE_DIR/agents/platform-deployment.md"

# Remove v3.0 commands
echo "  - Removing v3.0 commands..."
rm -f "$CLAUDE_DIR/commands/analyze-task.md"
rm -f "$CLAUDE_DIR/commands/orchestrate.md"
rm -f "$CLAUDE_DIR/commands/share-context.md"
rm -f "$CLAUDE_DIR/commands/test-v3.md"
rm -f "$CLAUDE_DIR/commands/agent-health.md"

# Clean up metrics and temp files
echo "  - Cleaning up v3.0 metrics..."
rm -rf "$CLAUDE_DIR/metrics/v3-"*
rm -rf "$CLAUDE_DIR/temp/context_"*

# Post-rollback verification
echo ""
echo "🔍 Post-rollback verification..."
if [[ -f "$CLAUDE_DIR/audit-system-complete.py" ]]; then
    echo "  - Running system audit..."
    python3 "$CLAUDE_DIR/audit-system-complete.py" --verify-v2 || true
fi

# Create restore script
cat > "$BACKUP_DIR/restore-v3.sh" << 'EOF'
#!/bin/bash
# Restore v3.0 from this backup

BACKUP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$(cd "$BACKUP_DIR/../../.." && pwd)"

echo "🔄 Restoring v3.0 from backup..."
echo "  - From: $BACKUP_DIR"
echo "  - To: $CLAUDE_DIR"

# Restore files
cp -v "$BACKUP_DIR/chains.v3.json" "$CLAUDE_DIR/chains.json"
cp -v "$BACKUP_DIR/aliases.v3.json" "$CLAUDE_DIR/aliases.json"
cp -v "$BACKUP_DIR/agents/"*.md "$CLAUDE_DIR/agents/" 2>/dev/null || true
cp -v "$BACKUP_DIR/commands/"* "$CLAUDE_DIR/commands/" 2>/dev/null || true

echo "✅ v3.0 restored!"
EOF

chmod +x "$BACKUP_DIR/restore-v3.sh"

echo ""
echo "✅ Rollback complete!"
echo "📁 V3.0 state saved to: $BACKUP_DIR"
echo "📝 To restore v3.0, run: $BACKUP_DIR/restore-v3.sh"
echo ""
echo "🎯 System is now at v2.8.0"
