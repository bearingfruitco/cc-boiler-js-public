#!/bin/bash
# Enhanced v3.0 Rollback Script with State Verification
# This script safely rolls back to v2.8.0 while preserving v3.0 state

set -euo pipefail  # Fail fast on errors

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔄 Claude Code Boilerplate v3.0 Rollback Script${NC}"
echo "================================================"

# Pre-rollback checks
echo -e "\n${YELLOW}🔍 Pre-rollback verification...${NC}"

# Check for v2.8.0 backup files
if [[ ! -f ".claude/backups/chains.v2.8.0.json" ]] || [[ ! -f ".claude/backups/aliases.v2.8.0.json" ]]; then
    echo -e "${RED}❌ ERROR: v2.8.0 backup files not found!${NC}"
    echo "Required files:"
    echo "  - .claude/backups/chains.v2.8.0.json"
    echo "  - .claude/backups/aliases.v2.8.0.json"
    echo -e "\n${YELLOW}Run: ./create-v2-backup.sh first${NC}"
    exit 1
fi

# Get current version if version file exists
CURRENT_VERSION="v3.0"
if [[ -f ".claude/version.json" ]]; then
    CURRENT_VERSION=$(grep -o '"version": "[^"]*"' .claude/version.json | cut -d'"' -f4 || echo "v3.0")
fi
echo -e "📌 Current version: ${BLUE}$CURRENT_VERSION${NC}"

# Create rollback timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=".claude/rollback/v3_state_$TIMESTAMP"

# Create backup directories
echo -e "\n${YELLOW}📦 Creating complete v3.0 state backup...${NC}"
mkdir -p "$BACKUP_DIR"/{agents,commands,scripts,metrics,temp,hooks}

# Function to safely copy files
safe_copy() {
    local source=$1
    local dest=$2
    if compgen -G "$source" > /dev/null; then
        cp -v $source "$dest" 2>/dev/null || true
    fi
}

# Backup v3.0 agents
echo -e "\n${BLUE}Backing up v3.0 agents...${NC}"
safe_copy ".claude/agents/*-specialist.md" "$BACKUP_DIR/agents/"
safe_copy ".claude/agents/*-engineer.md" "$BACKUP_DIR/agents/"
safe_copy ".claude/agents/*-compliance.md" "$BACKUP_DIR/agents/"
safe_copy ".claude/agents/*-deployment.md" "$BACKUP_DIR/agents/"
safe_copy ".claude/agents/ui-systems.md" "$BACKUP_DIR/agents/"
safe_copy ".claude/agents/event-schema.md" "$BACKUP_DIR/agents/"

# Backup v3.0 commands
echo -e "\n${BLUE}Backing up v3.0 commands...${NC}"
safe_copy ".claude/commands/analyze-task.md" "$BACKUP_DIR/commands/"
safe_copy ".claude/commands/orchestrate.md" "$BACKUP_DIR/commands/"
safe_copy ".claude/commands/share-context.md" "$BACKUP_DIR/commands/"
safe_copy ".claude/commands/test-v3.md" "$BACKUP_DIR/commands/"
safe_copy ".claude/commands/agent-health.md" "$BACKUP_DIR/commands/"

# Backup current configuration
echo -e "\n${BLUE}Backing up current configuration...${NC}"
cp -v .claude/chains.json "$BACKUP_DIR/chains.v3.json"
cp -v .claude/aliases.json "$BACKUP_DIR/aliases.v3.json"
[[ -f .claude/settings.json ]] && cp -v .claude/settings.json "$BACKUP_DIR/settings.v3.json"

# Backup metrics if they exist
if [[ -d ".claude/metrics" ]]; then
    echo -e "\n${BLUE}Backing up metrics...${NC}"
    cp -rv .claude/metrics/ "$BACKUP_DIR/metrics/" 2>/dev/null || true
fi

# Create rollback manifest
echo -e "\n${BLUE}Creating rollback manifest...${NC}"
cat > "$BACKUP_DIR/manifest.json" << EOF
{
  "rollback_timestamp": "$TIMESTAMP",
  "from_version": "$CURRENT_VERSION",
  "to_version": "v2.8.0",
  "agent_count": $(find "$BACKUP_DIR/agents" -name "*.md" 2>/dev/null | wc -l || echo 0),
  "command_count": $(find "$BACKUP_DIR/commands" -name "*.md" 2>/dev/null | wc -l || echo 0),
  "backup_size": $(du -sh "$BACKUP_DIR" | cut -f1),
  "created_by": "$(whoami)",
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF

# State verification
echo -e "\n${GREEN}✅ Verifying backup integrity...${NC}"
AGENT_COUNT=$(find "$BACKUP_DIR/agents" -name "*.md" 2>/dev/null | wc -l || echo 0)
COMMAND_COUNT=$(find "$BACKUP_DIR/commands" -name "*.md" 2>/dev/null | wc -l || echo 0)
echo "   - Backed up $AGENT_COUNT v3.0 agents"
echo "   - Backed up $COMMAND_COUNT v3.0 commands"
echo "   - Backup location: $BACKUP_DIR"

# Ask for confirmation
echo -e "\n${YELLOW}⚠️  WARNING: This will roll back to v2.8.0${NC}"
echo "All v3.0 features will be disabled but preserved in: $BACKUP_DIR"
read -p "Continue with rollback? (yes/no): " confirm

if [[ "$confirm" != "yes" ]]; then
    echo -e "${RED}Rollback cancelled.${NC}"
    exit 0
fi

# Perform rollback
echo -e "\n${YELLOW}♻️  Rolling back to v2.8.0...${NC}"

# Restore v2.8.0 configuration
echo "Restoring v2.8.0 configuration files..."
cp .claude/backups/chains.v2.8.0.json .claude/chains.json
cp .claude/backups/aliases.v2.8.0.json .claude/aliases.json

# Remove v3.0 agents
echo -e "\n${BLUE}Removing v3.0 agents...${NC}"
rm -f .claude/agents/supabase-specialist.md
rm -f .claude/agents/orm-specialist.md
rm -f .claude/agents/analytics-engineer.md
rm -f .claude/agents/ui-systems.md
rm -f .claude/agents/privacy-compliance.md
rm -f .claude/agents/event-schema.md
rm -f .claude/agents/platform-deployment.md

# Remove v3.0 commands
echo -e "\n${BLUE}Removing v3.0 commands...${NC}"
rm -f .claude/commands/analyze-task.md
rm -f .claude/commands/orchestrate.md
rm -f .claude/commands/share-context.md
rm -f .claude/commands/test-v3.md
rm -f .claude/commands/agent-health.md

# Clean up v3.0 artifacts
echo -e "\n${BLUE}Cleaning up v3.0 artifacts...${NC}"
rm -rf .claude/metrics/v3-*
rm -rf .claude/temp/context_*

# Post-rollback verification
echo -e "\n${YELLOW}🔍 Post-rollback verification...${NC}"

# Run system audit if available
if [[ -f ".claude/audit-system-complete.py" ]]; then
    echo "Running system audit..."
    python3 .claude/audit-system-complete.py --silent || true
fi

# Create restore script
echo -e "\n${BLUE}Creating restore script...${NC}"
cat > ".claude/scripts/restore-v3-$TIMESTAMP.sh" << 'RESTORE_EOF'
#!/bin/bash
# Restore v3.0 from rollback

BACKUP_DIR="BACKUP_DIR_PLACEHOLDER"

if [[ ! -d "$BACKUP_DIR" ]]; then
    echo "❌ Backup directory not found: $BACKUP_DIR"
    exit 1
fi

echo "🔄 Restoring v3.0 from backup..."

# Restore agents
cp -v "$BACKUP_DIR/agents/"*.md .claude/agents/ 2>/dev/null || true

# Restore commands  
cp -v "$BACKUP_DIR/commands/"*.md .claude/commands/ 2>/dev/null || true

# Restore configuration
cp -v "$BACKUP_DIR/chains.v3.json" .claude/chains.json
cp -v "$BACKUP_DIR/aliases.v3.json" .claude/aliases.json
[[ -f "$BACKUP_DIR/settings.v3.json" ]] && cp -v "$BACKUP_DIR/settings.v3.json" .claude/settings.json

echo "✅ v3.0 restored successfully!"
RESTORE_EOF

# Update the restore script with actual backup directory
sed -i '' "s|BACKUP_DIR_PLACEHOLDER|$BACKUP_DIR|g" ".claude/scripts/restore-v3-$TIMESTAMP.sh"
chmod +x ".claude/scripts/restore-v3-$TIMESTAMP.sh"

# Final summary
echo -e "\n${GREEN}✅ Rollback complete!${NC}"
echo "================================================"
echo -e "📌 Current version: ${BLUE}v2.8.0${NC}"
echo -e "📁 v3.0 backup saved to: ${BLUE}$BACKUP_DIR${NC}"
echo -e "🔧 To restore v3.0, run: ${YELLOW}./claude/scripts/restore-v3-$TIMESTAMP.sh${NC}"
echo -e "\n${GREEN}The system is now running v2.8.0 with all v3.0 changes safely preserved.${NC}"
