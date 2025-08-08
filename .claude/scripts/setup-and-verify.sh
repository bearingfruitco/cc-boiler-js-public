#!/bin/bash

# Complete Setup and Verification Script for Claude Advanced Features
# This ensures everything actually works

set -e  # Exit on error

echo "================================================"
echo "🚀 Claude Advanced Features - Complete Setup"
echo "================================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Track results
PASSED=0
FAILED=0
WARNINGS=0

# Helper functions
check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✅ $1 installed${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}❌ $1 not found${NC}"
        ((FAILED++))
        return 1
    fi
}

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅ $1 exists${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}❌ $1 missing${NC}"
        ((FAILED++))
        return 1
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✅ $1 exists${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${YELLOW}⚠️  $1 missing - creating...${NC}"
        mkdir -p "$1"
        ((WARNINGS++))
        return 1
    fi
}

# Step 1: Check Prerequisites
echo -e "${BLUE}Step 1: Checking Prerequisites${NC}"
echo "================================"

check_command "git"
check_command "node"
check_command "npm"
check_command "claude" || echo "  Install: curl -L https://claude.ai/install | bash"
check_command "gh" || echo "  Install: brew install gh (Mac) or see https://cli.github.com"

echo ""

# Step 2: Check Directory Structure
echo -e "${BLUE}Step 2: Verifying Directory Structure${NC}"
echo "======================================"

check_dir ".claude"
check_dir ".claude/agents"
check_dir ".claude/commands"
check_dir ".claude/config"
check_dir ".claude/hooks"
check_dir ".claude/mcp-servers"
check_dir ".claude/mcp-servers/connectors"
check_dir ".claude/scripts"
check_dir ".claude/docs"
check_dir ".claude/logs"
check_dir "PRPs"
check_dir "PRPs/active"
check_dir "plans"

echo ""

# Step 3: Check Critical Files
echo -e "${BLUE}Step 3: Checking Critical Files${NC}"
echo "================================"

# Core configuration
check_file "claw.md"
check_file ".claude/settings.local.json" || {
    echo "  Creating settings.local.json..."
    cat > .claude/settings.local.json << 'EOF'
{
  "mcp_octocode": true,
  "mcp_serena": true,
  "mcp_github": true,
  "mcp_playwright": true,
  "str_replace_editor": true,
  "create_file": true,
  "edit_file": true,
  "read_file": true,
  "list_files": true,
  "bash": ["npm", "node", "git", "ls", "cd", "mkdir", "cp", "mv", "echo", "cat"],
  "python": true
}
EOF
    echo -e "${GREEN}  ✅ Created settings.local.json${NC}"
}

# Key agents
check_file ".claude/agents/validation-gates.md"
check_file ".claude/agents/tdd-engineer.md"
check_file ".claude/agents/senior-engineer.md"

# Parallel commands
check_file ".claude/commands/prep-parallel.md"
check_file ".claude/commands/execute-parallel.md"
check_file ".claude/commands/merge-best.md"
check_file ".claude/commands/cleanup-parallel.md"

# MCPs
check_file ".claude/mcp-servers/connectors/octocode-mcp.js"
check_file ".claude/mcp-servers/connectors/serena-mcp.js"

# Hooks
check_file ".claude/hooks/log-changes.sh"
check_file ".claude/config/hooks.json"

echo ""

# Step 4: Make Scripts Executable
echo -e "${BLUE}Step 4: Setting Permissions${NC}"
echo "============================"

if [ -d ".claude/hooks" ]; then
    chmod +x .claude/hooks/*.sh 2>/dev/null && echo -e "${GREEN}✅ Hooks executable${NC}" || echo -e "${YELLOW}⚠️  No hooks to set${NC}"
fi

if [ -d ".claude/scripts" ]; then
    chmod +x .claude/scripts/*.sh 2>/dev/null && echo -e "${GREEN}✅ Scripts executable${NC}" || echo -e "${YELLOW}⚠️  No scripts to set${NC}"
fi

echo ""

# Step 5: Test MCP Installation
echo -e "${BLUE}Step 5: Testing MCP Installations${NC}"
echo "=================================="

# Check if MCPs are installed
echo "Checking MCP list..."
if command -v claude &> /dev/null; then
    MCP_LIST=$(claude mcp list 2>/dev/null || echo "")
    
    if echo "$MCP_LIST" | grep -q "octocode"; then
        echo -e "${GREEN}✅ Octocode MCP installed${NC}"
        ((PASSED++))
    else
        echo -e "${YELLOW}⚠️  Octocode MCP not found - install with: claude mcp add octocode${NC}"
        ((WARNINGS++))
    fi
    
    if echo "$MCP_LIST" | grep -q "serena"; then
        echo -e "${GREEN}✅ Serena MCP installed${NC}"
        ((PASSED++))
    else
        echo -e "${YELLOW}⚠️  Serena MCP not found - install with: claude mcp add serena${NC}"
        ((WARNINGS++))
    fi
else
    echo -e "${YELLOW}⚠️  Claude not available - skip MCP check${NC}"
fi

echo ""

# Step 6: Test Node Modules
echo -e "${BLUE}Step 6: Checking Node Dependencies${NC}"
echo "==================================="

if [ -f "package.json" ]; then
    if [ -d "node_modules" ]; then
        echo -e "${GREEN}✅ Node modules installed${NC}"
        ((PASSED++))
    else
        echo -e "${YELLOW}⚠️  Installing node modules...${NC}"
        npm install
        ((WARNINGS++))
    fi
else
    echo -e "${YELLOW}⚠️  No package.json found${NC}"
    ((WARNINGS++))
fi

echo ""

# Step 7: Test Git Configuration
echo -e "${BLUE}Step 7: Checking Git Configuration${NC}"
echo "==================================="

if git config user.name &> /dev/null && git config user.email &> /dev/null; then
    echo -e "${GREEN}✅ Git configured${NC}"
    echo "  User: $(git config user.name)"
    echo "  Email: $(git config user.email)"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠️  Git not configured${NC}"
    echo "  Run: git config --global user.name 'Your Name'"
    echo "  Run: git config --global user.email 'your@email.com'"
    ((WARNINGS++))
fi

# Check GitHub CLI
if command -v gh &> /dev/null; then
    if gh auth status &> /dev/null; then
        echo -e "${GREEN}✅ GitHub CLI authenticated${NC}"
        ((PASSED++))
    else
        echo -e "${YELLOW}⚠️  GitHub CLI not authenticated${NC}"
        echo "  Run: gh auth login"
        ((WARNINGS++))
    fi
fi

echo ""

# Step 8: Create Test Files
echo -e "${BLUE}Step 8: Creating Test Files${NC}"
echo "============================"

# Create a test plan for parallel development
cat > plans/test-feature.md << 'EOF'
# Test Feature Plan
This is a test feature for parallel development
- Simple functionality
- Basic tests
- Quick implementation
EOF
echo -e "${GREEN}✅ Created test plan${NC}"

# Create a test initial.md
cat > PRPs/test-initial.md << 'EOF'
# Test Feature
A simple test feature to verify the system works
- Basic CRUD operations
- Simple validation
- Unit tests
EOF
echo -e "${GREEN}✅ Created test initial${NC}"

echo ""

# Step 9: Functional Tests
echo -e "${BLUE}Step 9: Running Functional Tests${NC}"
echo "================================="

# Test MCP connectors
if [ -f ".claude/mcp-servers/connectors/octocode-mcp.js" ]; then
    echo "Testing Octocode connector..."
    node -e "
    try {
        const O = require('./.claude/mcp-servers/connectors/octocode-mcp.js');
        const o = new O();
        console.log('  ✅ Octocode connector loads');
    } catch(e) {
        console.log('  ⚠️  Octocode error:', e.message);
    }
    " 2>/dev/null || echo -e "${YELLOW}  ⚠️  Octocode needs dependencies${NC}"
fi

if [ -f ".claude/mcp-servers/connectors/serena-mcp.js" ]; then
    echo "Testing Serena connector..."
    node -e "
    try {
        const S = require('./.claude/mcp-servers/connectors/serena-mcp.js');
        const s = new S();
        console.log('  ✅ Serena connector loads');
    } catch(e) {
        console.log('  ⚠️  Serena error:', e.message);
    }
    " 2>/dev/null || echo -e "${YELLOW}  ⚠️  Serena needs dependencies${NC}"
fi

echo ""

# Step 10: Create Quick Reference
echo -e "${BLUE}Step 10: Creating Quick Reference${NC}"
echo "=================================="

cat > QUICK_START.md << 'EOF'
# 🚀 Quick Start Commands

## Start Development
```bash
claude
/primer
```

## Standard Development
```bash
/generate-prp PRPs/test-initial.md
/execute-prp PRPs/test-prp.md
/validation-gates "test-feature"
```

## Parallel Development (3x Speed)
```bash
/prep-parallel "test-feature" 3
/execute-parallel "test-feature" "plans/test-feature.md" 3
/merge-best "test-feature" 2
/cleanup-parallel "test-feature" ""
```

## Fix GitHub Issue
```bash
/fix-github-issue 1
```

## Use MCPs
```
"Use Octocode to refactor this function"
"Use Serena to find all API endpoints"
```

## Run Tests
```bash
/test-all
/validation-gates "feature"
```
EOF

echo -e "${GREEN}✅ Created QUICK_START.md${NC}"
echo ""

# Final Report
echo "================================================"
echo -e "${BLUE}📊 Setup Complete - Final Report${NC}"
echo "================================================"
echo ""
echo -e "Passed:   ${GREEN}$PASSED checks${NC}"
echo -e "Warnings: ${YELLOW}$WARNINGS items${NC}"
echo -e "Failed:   ${RED}$FAILED items${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ System is ready to use!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Run: claude"
    echo "2. Run: /primer"
    echo "3. Try: /prep-parallel \"test\" 3"
    echo ""
    echo "See QUICK_START.md for commands"
else
    echo -e "${YELLOW}⚠️  Some issues need attention${NC}"
    echo ""
    echo "Fix the failed items above, then run this script again."
fi

echo ""
echo "================================================"
echo "Happy coding with 3x speed! 🚀"
echo "================================================"
