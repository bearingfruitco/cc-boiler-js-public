#!/bin/bash
# setup-enhanced-boilerplate.sh - Quick setup for enhanced Claude Code features

echo "🚀 Setting up enhanced Claude Code boilerplate..."

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Change to project root
cd "$PROJECT_ROOT"

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p .claude/commands
mkdir -p .claude/scripts
mkdir -p .claude/checkpoints/tasks
mkdir -p .claude/orchestration
mkdir -p .claude/team
mkdir -p docs/project/features
mkdir -p tests/browser

# Make scripts executable
echo "🔧 Making scripts executable..."

# Make all Python scripts in hooks executable
if [ -d ".claude/hooks" ]; then
    find .claude/hooks -name "*.py" -type f -exec chmod +x {} \;
    echo "✅ Hook scripts made executable"
fi

# Make scripts in scripts directory executable
if [ -d "scripts" ]; then
    chmod +x scripts/*.sh 2>/dev/null || true
    chmod +x scripts/*.py 2>/dev/null || true
    echo "✅ Scripts made executable"
fi

# Check for required dependencies
echo "🔍 Checking dependencies..."

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js v22+"
    exit 1
else
    NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 22 ]; then
        echo "⚠️  Node.js v$NODE_VERSION found, but v22+ recommended"
    else
        echo "✅ Node.js v$NODE_VERSION installed"
    fi
fi

# Check Bun
if ! command -v bun &> /dev/null; then
    echo "❌ Bun not found. Installing..."
    curl -fsSL https://bun.sh/install | bash
    source ~/.bashrc 2>/dev/null || source ~/.zshrc 2>/dev/null
else
    echo "✅ Bun installed ($(bun --version))"
fi

# Check pnpm
if ! command -v pnpm &> /dev/null; then
    echo "❌ pnpm not found. Installing..."
    npm install -g pnpm@9
else
    echo "✅ pnpm installed ($(pnpm --version))"
fi

# Check Claude Code - try multiple methods
CLAUDE_CODE_FOUND=false
if command -v claude-code &> /dev/null; then
    CLAUDE_CODE_FOUND=true
elif npm list -g @anthropic-ai/claude-code &> /dev/null; then
    CLAUDE_CODE_FOUND=true
elif [ -f "$HOME/.npm-global/bin/claude-code" ]; then
    CLAUDE_CODE_FOUND=true
fi

if [ "$CLAUDE_CODE_FOUND" = false ]; then
    echo "⚠️  Claude Code not found in PATH. It may still be installed."
    echo "   Try: npm install -g @anthropic-ai/claude-code"
    echo "   Then: source ~/.zshrc (or ~/.bashrc)"
else
    echo "✅ Claude Code installed"
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install it first."
    exit 1
else
    echo "✅ Python 3 installed ($(python3 --version))"
fi

# Check Git
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install it first."
    exit 1
else
    echo "✅ Git installed"
fi

# Check GitHub CLI
if ! command -v gh &> /dev/null; then
    echo "⚠️  GitHub CLI not found. Install with: brew install gh"
    echo "   Then run: gh auth login"
else
    echo "✅ GitHub CLI installed"
    # Check if authenticated
    if gh auth status &> /dev/null; then
        echo "✅ GitHub CLI authenticated"
    else
        echo "⚠️  GitHub CLI not authenticated. Run: gh auth login"
    fi
fi

# Install Python dependencies if needed
echo "📦 Checking Python dependencies..."
if ! python3 -c "import git" &> /dev/null; then
    echo "Installing gitpython..."
    pip3 install gitpython --quiet
fi

# Check if package.json exists and install dependencies
if [ -f "package.json" ]; then
    echo "📦 Installing project dependencies with pnpm..."
    pnpm install
    
    # Check if Biome is installed
    if pnpm list @biomejs/biome &> /dev/null; then
        echo "✅ Biome installed for linting/formatting"
    fi
else
    echo "⚠️  No package.json found. Run 'pnpm init' if starting fresh."
fi

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "📝 Creating .env.local file..."
    if [ -f ".env.example" ]; then
        cp .env.example .env.local
        echo "✅ Created .env.local from .env.example"
    else
        touch .env.local
        echo "✅ Created empty .env.local"
    fi
fi

# Summary
echo ""
echo "✅ Enhanced boilerplate setup complete!"
echo ""
echo "📋 Features available:"
echo "  • PRD-driven development (/prd, /gt, /pt)"
echo "  • Task management system (/ts, /tb)"
echo "  • Auto-updating documentation (/auc)"
echo "  • Browser testing with Playwright (/btf)"
echo "  • Multi-agent orchestration (/orch)"
echo "  • Security & field registry system"
echo "  • PII protection hooks"
echo "  • Secure form generation (/ctf)"
echo "  • Biome linting integration (/lc)"
echo "  • Bun test runner (/test)"
echo ""
echo "🚀 Next steps:"
echo "1. Start Claude Code: claude-code ."
echo "2. Run: /init (if first time in this project)"
echo "3. Run: /init-project (to define your project)"
echo "4. Run: /gi PROJECT (to generate GitHub issues)"
echo "5. Start building with: /fw start 1"
echo ""
echo "📚 Documentation:"
echo "  • Quick start: docs/setup/QUICK_START_NEW_PROJECT.md"
echo "  • Full guide: docs/setup/DAY_1_COMPLETE_GUIDE.md"
echo "  • Commands: QUICK_REFERENCE.md"
echo ""

# Run verification
echo "🔍 Running system verification..."
if [ -f "scripts/verify-system.sh" ]; then
    bash scripts/verify-system.sh
fi