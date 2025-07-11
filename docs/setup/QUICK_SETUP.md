# Quick Setup Instructions for Team

## Prerequisites

1. **Claude Pro/Max Subscription** - Claude Code is included
2. **Node.js v22+** - Required for all tools

## One-Command Setup (After Cloning)

```bash
# Clone and setup in one go
git clone https://github.com/bearingfruitco/claude-code-boilerplate.git my-project && \
cd my-project && \
rm -rf .git && \
git init && \
./setup-all-dependencies.sh
```

The setup script will automatically:
- Install Claude Code (if needed)
- Install Bun
- Install all dependencies
- Set up hooks
- Configure permissions

## What This Installs

The `setup-all-dependencies.sh` script will:

1. **Check Prerequisites**
   - Claude Code
   - Git & GitHub CLI
   - Node.js v22+
   - pnpm v9+
   - Python 3
   - Bun v1.0+

2. **Install Project Dependencies**
   - All Node packages (including Biome)
   - Playwright MCP globally
   - Python packages (gitpython)

3. **Set Permissions**
   - Makes all scripts executable
   - Sets up hooks properly

4. **Run Initial Setup**
   - Configures hooks system
   - Prepares environment

## Manual Installation (If Needed)

If the script fails or you prefer manual setup:

```bash
# Bun
curl -fsSL https://bun.sh/install | bash

# Node packages
pnpm install

# Global tools
npm install -g @modelcontextprotocol/server-playwright

# Python deps
pip3 install gitpython

# Permissions
chmod +x .claude/scripts/*.sh
chmod +x .claude/scripts/*.py
chmod +x .claude/hooks/pre-tool-use/*.py
chmod +x .claude/hooks/post-tool-use/*.py
```

## Starting Claude Code

After setup completes:

```bash
claude-code .

# In Claude Code:
/init   # First time only
/sr     # Start working
```

## Troubleshooting

- **"command not found: bun"** - Restart terminal after Bun install
- **"command not found: pnpm"** - Run: `npm install -g pnpm@9`
- **Node version too old** - Run: `brew install node@22`
- **Permission denied** - Run: `chmod +x setup-all-dependencies.sh`
