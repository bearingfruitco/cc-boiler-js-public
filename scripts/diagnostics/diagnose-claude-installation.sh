#!/bin/bash
# Fix Claude Code Multiple Installations

echo "🔧 Fixing Claude Code Installation Issues"
echo "========================================"
echo ""

# Show current status
echo "📊 Current Status:"
claude --version 2>/dev/null || echo "Claude command not working properly"
echo ""

# Check installations
echo "🔍 Checking installations:"
echo ""

# Check npm global
echo "1. NPM Global installation:"
npm list -g @claude-ai/cli 2>/dev/null || echo "   Not found in global npm"

# Check local installation
echo ""
echo "2. Local installation:"
if [ -d "$HOME/.claude/local" ]; then
    echo "   Found at: $HOME/.claude/local"
    ls -la "$HOME/.claude/local" 2>/dev/null | head -5
else
    echo "   Not found"
fi

# Check PATH
echo ""
echo "3. PATH entries:"
echo "$PATH" | tr ':' '\n' | grep -i claude || echo "   No claude entries in PATH"

echo ""
echo "📋 Recommended Fix:"
echo ""
echo "1. Remove duplicate installations:"
echo "   npm uninstall -g @claude-ai/cli"
echo "   rm -rf ~/.claude/local"
echo ""
echo "2. Install Claude Code properly:"
echo "   npm install -g @claude-ai/cli@latest"
echo ""
echo "3. Verify installation:"
echo "   claude --version"
echo "   claude --doctor"
echo ""
echo "4. If using fnm/nvm, ensure correct Node version:"
echo "   fnm use 20  # or nvm use 20"
echo ""

# Create a fix script
cat > fix-claude-installation.sh << 'EOF'
#!/bin/bash
# Claude Code Installation Fix Script

echo "🚀 Starting Claude Code fix..."

# Backup current config if exists
if [ -d "$HOME/.claude" ]; then
    echo "📦 Backing up .claude directory..."
    cp -r "$HOME/.claude" "$HOME/.claude.backup.$(date +%Y%m%d_%H%M%S)"
fi

# Remove all installations
echo "🗑️  Removing duplicate installations..."
npm uninstall -g @claude-ai/cli 2>/dev/null
npm uninstall -g claude 2>/dev/null
rm -rf "$HOME/.claude/local" 2>/dev/null

# Clear npm cache
echo "🧹 Clearing npm cache..."
npm cache clean --force

# Install fresh
echo "📥 Installing Claude Code..."
npm install -g @claude-ai/cli@latest

# Verify
echo ""
echo "✅ Verification:"
claude --version
which claude

echo ""
echo "🎯 Next steps:"
echo "1. Restart your terminal"
echo "2. Run: claude --doctor"
echo "3. Your projects and settings are preserved in ~/.claude"
EOF

chmod +x fix-claude-installation.sh

echo "✅ Created fix-claude-installation.sh"
echo ""
echo "Run: ./fix-claude-installation.sh"
