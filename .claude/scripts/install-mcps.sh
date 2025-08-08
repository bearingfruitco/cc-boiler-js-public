#!/bin/bash

# Install and configure Octocode and Serena MCPs

echo "🚀 Installing Advanced MCPs..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Claude is installed
if ! command -v claude &> /dev/null; then
    echo -e "${RED}❌ Claude CLI not found. Please install Claude first.${NC}"
    exit 1
fi

echo "📦 Installing Octocode MCP..."
echo "=============================="

# Install Octocode MCP
claude mcp add octocode 2>/dev/null || {
    echo -e "${YELLOW}⚠️  Octocode MCP may already be installed or requires manual setup${NC}"
    echo "Manual installation:"
    echo "1. Visit: https://github.com/bgauryy/octocode-mcp"
    echo "2. Follow installation instructions"
    echo ""
}

echo ""
echo "🔍 Installing Serena MCP..."
echo "=========================="

# Install Serena MCP
claude mcp add serena 2>/dev/null || {
    echo -e "${YELLOW}⚠️  Serena MCP may already be installed or requires manual setup${NC}"
    echo "Manual installation:"
    echo "1. Visit: https://github.com/oraios/serena"
    echo "2. Follow installation instructions"
    echo ""
}

echo ""
echo "🔧 Configuring MCP Permissions..."
echo "================================="

# Update settings.local.json to include MCP permissions
SETTINGS_FILE=".claude/settings.local.json"

if [ -f "$SETTINGS_FILE" ]; then
    echo "Adding MCP permissions to $SETTINGS_FILE..."
    
    # Backup current settings
    cp "$SETTINGS_FILE" "$SETTINGS_FILE.backup"
    
    # Add MCP permissions (you may need to manually edit this)
    echo -e "${YELLOW}📝 Please add these lines to your $SETTINGS_FILE:${NC}"
    echo ""
    echo '  "mcp_octocode": true,'
    echo '  "mcp_serena": true,'
    echo ""
else
    echo -e "${YELLOW}⚠️  Settings file not found. Creating...${NC}"
    cat > "$SETTINGS_FILE" << 'EOF'
{
  "mcp_octocode": true,
  "mcp_serena": true,
  "str_replace_editor": true,
  "create_file": true,
  "edit_file": true,
  "read_file": true,
  "list_files": true,
  "bash": ["npm", "node", "git", "ls", "cd", "mkdir", "rm", "cp", "mv"],
  "python": true
}
EOF
    echo -e "${GREEN}✅ Created $SETTINGS_FILE with MCP permissions${NC}"
fi

echo ""
echo "🧪 Testing MCP Connections..."
echo "============================="

# Test connections
cd .claude/mcp-servers/test
npm test 2>/dev/null || {
    echo -e "${YELLOW}⚠️  Test suite not available. Installing dependencies...${NC}"
    npm install chalk
    node test-connections.js
}
cd -

echo ""
echo "📋 Verification Checklist"
echo "========================"
echo ""
echo "Please verify:"
echo "[ ] Octocode MCP is listed in: claude mcp list"
echo "[ ] Serena MCP is listed in: claude mcp list"
echo "[ ] settings.local.json includes mcp_octocode and mcp_serena"
echo "[ ] Test connections passed"
echo ""

# List current MCPs
echo "Current MCPs:"
echo "-------------"
claude mcp list 2>/dev/null || echo "Run 'claude mcp list' to see installed MCPs"

echo ""
echo -e "${GREEN}✅ MCP installation complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Restart Claude Code: exit and run 'claude' again"
echo "2. Test Octocode: Ask Claude to generate code using Octocode"
echo "3. Test Serena: Ask Claude to search the codebase"
echo ""
echo "Example commands to test:"
echo "  'Use Octocode to refactor this function'"
echo "  'Use Serena to find all API endpoints'"
echo ""
