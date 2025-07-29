#!/bin/bash

# Sync Architecture Enhancement from Boilerplate to Target Project
# Usage: ./sync-architecture-enhancement.sh [target-directory]

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get target directory from argument or use default
TARGET_DIR="${1:-/Users/shawnsmith/dev/bfc/debt-tofu-report}"
SOURCE_DIR="/Users/shawnsmith/dev/bfc/boilerplate"

echo -e "${GREEN}🔄 Syncing Architecture Enhancement${NC}"
echo "From: $SOURCE_DIR"
echo "To: $TARGET_DIR"
echo ""

# Verify directories exist
if [ ! -d "$SOURCE_DIR" ]; then
    echo -e "${RED}❌ Source directory not found: $SOURCE_DIR${NC}"
    exit 1
fi

if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${RED}❌ Target directory not found: $TARGET_DIR${NC}"
    exit 1
fi

# Create necessary directories
echo -e "${YELLOW}📁 Creating directories...${NC}"
mkdir -p "$TARGET_DIR/.claude/commands"
mkdir -p "$TARGET_DIR/.claude/agents"
mkdir -p "$TARGET_DIR/.claude/templates/architecture"
mkdir -p "$TARGET_DIR/.claude/hooks/pre-tool-use"
mkdir -p "$TARGET_DIR/.claude/hooks/post-tool-use"

# Copy commands
echo -e "${YELLOW}📝 Copying commands...${NC}"
cp -v "$SOURCE_DIR/.claude/commands/create-architecture.md" "$TARGET_DIR/.claude/commands/"
cp -v "$SOURCE_DIR/.claude/commands/validate-architecture.md" "$TARGET_DIR/.claude/commands/"

# Copy agent
echo -e "${YELLOW}🤖 Copying system architect agent...${NC}"
cp -v "$SOURCE_DIR/.claude/agents/system-architect.md" "$TARGET_DIR/.claude/agents/"

# Copy templates
echo -e "${YELLOW}📋 Copying architecture templates...${NC}"
cp -v "$SOURCE_DIR/.claude/templates/architecture/"*.md "$TARGET_DIR/.claude/templates/architecture/"

# Copy hooks
echo -e "${YELLOW}🔗 Copying hooks...${NC}"
cp -v "$SOURCE_DIR/.claude/hooks/pre-tool-use/17-architecture-enforcer.py" "$TARGET_DIR/.claude/hooks/pre-tool-use/"
cp -v "$SOURCE_DIR/.claude/hooks/post-tool-use/04a-architecture-suggester.py" "$TARGET_DIR/.claude/hooks/post-tool-use/"

# Make hooks executable
chmod +x "$TARGET_DIR/.claude/hooks/pre-tool-use/17-architecture-enforcer.py"
chmod +x "$TARGET_DIR/.claude/hooks/post-tool-use/04a-architecture-suggester.py"

# Merge JSON files (requires jq)
echo -e "${YELLOW}🔧 Merging JSON configurations...${NC}"

# Function to merge JSON files
merge_json() {
    local file=$1
    local source="$SOURCE_DIR/.claude/$file"
    local target="$TARGET_DIR/.claude/$file"
    
    if [ -f "$source" ] && [ -f "$target" ]; then
        echo "Merging $file..."
        # Create backup
        cp "$target" "$target.backup-$(date +%Y%m%d-%H%M%S)"
        
        # For command-registry.json - merge commands array
        if [ "$file" = "command-registry.json" ]; then
            jq -s '.[0] * .[1] | .commands = (.[0].commands + .[1].commands | unique_by(.name))' "$target" "$source" > "$target.tmp" && mv "$target.tmp" "$target"
        # For aliases.json - merge aliases object
        elif [ "$file" = "aliases.json" ]; then
            jq -s '.[0] * .[1] | .aliases = (.[0].aliases * .[1].aliases)' "$target" "$source" > "$target.tmp" && mv "$target.tmp" "$target"
        # For chains.json - merge chains object and shortcuts
        elif [ "$file" = "chains.json" ]; then
            jq -s '.[0] * .[1] | .chains = (.[0].chains * .[1].chains) | .shortcuts = (.[0].shortcuts * .[1].shortcuts)' "$target" "$source" > "$target.tmp" && mv "$target.tmp" "$target"
        fi
        echo "✅ Merged $file"
    elif [ -f "$source" ]; then
        echo "Copying $file..."
        cp "$source" "$target"
        echo "✅ Copied $file"
    fi
}

# Check if jq is installed
if command -v jq &> /dev/null; then
    merge_json "command-registry.json"
    merge_json "aliases.json"
    merge_json "chains.json"
else
    echo -e "${YELLOW}⚠️  jq not installed. Please manually merge JSON files:${NC}"
    echo "  - command-registry.json"
    echo "  - aliases.json"
    echo "  - chains.json"
fi

# Update documentation files
echo -e "${YELLOW}📚 Updating documentation...${NC}"

# Check if updates are needed in these files
files_to_check=(
    ".claude/commands/init-project.md"
    ".claude/commands/generate-issues.md"
    ".claude/commands/help.md"
)

for file in "${files_to_check[@]}"; do
    if [ -f "$SOURCE_DIR/$file" ]; then
        echo "Please review and update: $file"
    fi
done

echo ""
echo -e "${GREEN}✅ Architecture Enhancement Sync Complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Review the merged JSON files for conflicts"
echo "2. Test the architecture commands:"
echo "   cd $TARGET_DIR"
echo "   /arch"
echo "3. Check that hooks are working:"
echo "   /gi PROJECT  # Should be blocked without architecture"
echo ""
echo "Architecture templates are now available in:"
echo "$TARGET_DIR/.claude/templates/architecture/"
