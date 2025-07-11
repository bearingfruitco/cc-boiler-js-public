#!/bin/bash
# setup-enhanced-boilerplate.sh - Quick setup for enhanced Claude Code features

echo "🚀 Setting up enhanced Claude Code boilerplate..."

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p .claude/commands
mkdir -p .claude/scripts
mkdir -p .claude/checkpoints/tasks
mkdir -p docs/project/features
mkdir -p tests/browser

# Make Python scripts executable
echo "🔧 Making scripts executable..."
chmod +x .claude/scripts/*.py
chmod +x .claude/scripts/*.sh
chmod +x .claude/hooks/pre-tool-use/*.py
chmod +x .claude/hooks/post-tool-use/*.py
chmod +x setup-security-features.sh

# Check for required dependencies
echo "🔍 Checking dependencies..."

# Check Claude Code
if ! command -v claude-code &> /dev/null; then
    echo "❌ Claude Code not found. Please install it first."
    exit 1
else
    echo "✅ Claude Code installed"
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install it first."
    exit 1
else
    echo "✅ Python 3 installed"
fi

# Check Git
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install it first."
    exit 1
else
    echo "✅ Git installed"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install gitpython --quiet

# Summary
echo ""
echo "✅ Enhanced boilerplate setup complete!"
echo ""
echo "📋 New features added:"
echo "  • PRD-driven development (/prd, /gt, /pt)"
echo "  • Task management system (/ts, /tb)"
echo "  • Auto-updating documentation (/auc)"
echo "  • Browser testing with Playwright (/btf)"
echo "  • Enhanced command chains"
echo "  • 🆕 Security & field registry system"
echo "  • 🆕 PII protection hooks"
echo "  • 🆕 Secure form generation (/ctf)"
echo ""
echo "🚀 Next steps:"
echo "1. Run: ./setup-security-features.sh (for forms)"
echo "2. Start Claude Code: claude-code ."
echo "3. Run: /init (if first time)"
echo "4. Run: /spm (setup Playwright MCP)"
echo "5. Start building with: /prd [feature-name]"
echo ""
echo "📚 See DAY_1_COMPLETE_GUIDE.md for detailed instructions"
echo "🔒 See field-registry/README.md for security features"