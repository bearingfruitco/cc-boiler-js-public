#!/bin/bash
# add-to-existing.sh - Safely add Claude Code boilerplate to existing project
# Usage: ./add-to-existing.sh [minimal|standard|full]

set -euo pipefail

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
REPO_URL="https://github.com/bearingfruitco/claude-code-boilerplate"
INSTALL_MODE=${1:-standard}

print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check if already has Claude setup
if [ -d ".claude" ]; then
    print_warning "Found existing .claude directory"
    echo "Choose an option:"
    echo "1) Backup and proceed"
    echo "2) Merge with existing"
    echo "3) Cancel"
    read -p "Your choice (1-3): " choice
    
    case $choice in
        1)
            mv .claude .claude.backup.$(date +%Y%m%d-%H%M%S)
            print_status "Backed up existing .claude directory"
            ;;
        2)
            print_status "Will merge with existing setup"
            ;;
        3)
            print_error "Installation cancelled"
            exit 0
            ;;
    esac
fi

# Create directories
print_status "Creating directory structure..."
mkdir -p .claude/{commands,hooks/{pre-tool-use,post-tool-use,stop},scripts,team,checkpoints,personas}
mkdir -p docs/{project,team,setup}

# Download based on mode
case $INSTALL_MODE in
    minimal)
        print_status "Installing minimal setup (commit control + basics)..."
        
        # Essential commands only
        cd .claude/commands
        for cmd in commit-review git-status checkpoint smart-resume help; do
            curl -sLO "$REPO_URL/raw/main/boilerplate/.claude/commands/$cmd.md" || print_warning "Failed to download $cmd"
        done
        
        # Aliases
        cd ..
        curl -sLO "$REPO_URL/raw/main/boilerplate/.claude/aliases.json"
        
        print_status "Minimal installation complete!"
        ;;
        
    standard)
        print_status "Installing standard setup (recommended features)..."
        
        # Download all commands
        cd .claude
        curl -sL "$REPO_URL/archive/main.tar.gz" | \
            tar -xz --strip=2 --wildcards "*/boilerplate/.claude/commands/*" || print_error "Failed to download commands"
        
        # Core configurations
        curl -sLO "$REPO_URL/raw/main/boilerplate/.claude/aliases.json"
        curl -sLO "$REPO_URL/raw/main/boilerplate/.claude/chains.json"
        
        # Essential hooks
        cd hooks
        curl -sLO "$REPO_URL/raw/main/boilerplate/.claude/hooks/config.json"
        
        # State save hook
        cd post-tool-use
        curl -sLO "$REPO_URL/raw/main/boilerplate/.claude/hooks/post-tool-use/01-state-save.py"
        chmod +x 01-state-save.py
        
        # PII protection hook  
        cd ../pre-tool-use
        curl -sLO "$REPO_URL/raw/main/boilerplate/.claude/hooks/pre-tool-use/07-pii-protection.py"
        chmod +x 07-pii-protection.py
        
        cd ../../..
        print_status "Standard installation complete!"
        ;;
        
    full)
        print_status "Installing full system..."
        
        # Clone and copy everything
        temp_dir=$(mktemp -d)
        git clone --depth 1 "$REPO_URL" "$temp_dir"
        
        # Copy all Claude files
        cp -r "$temp_dir/boilerplate/.claude/"* .claude/
        
        # Copy additional systems
        [ ! -d "field-registry" ] && cp -r "$temp_dir/boilerplate/field-registry" .
        [ ! -d "lib/security" ] && mkdir -p lib && cp -r "$temp_dir/boilerplate/lib/security" lib/
        [ ! -d "lib/forms" ] && mkdir -p lib && cp -r "$temp_dir/boilerplate/lib/forms" lib/
        
        # Documentation
        cp -r "$temp_dir/boilerplate/docs/"* docs/
        
        # Key markdown files
        for file in CLAUDE.md QUICK_REFERENCE.md; do
            [ ! -f "$file" ] && cp "$temp_dir/boilerplate/$file" .
        done
        
        # Cleanup
        rm -rf "$temp_dir"
        
        # Run hooks installer
        cd .claude/scripts
        chmod +x install-hooks.sh
        print_status "Running hooks installer..."
        ./install-hooks.sh
        cd ../..
        
        print_status "Full installation complete!"
        ;;
esac

# Create initial configuration if needed
if [ ! -f ".claude/hooks/config.json" ]; then
    cat > .claude/hooks/config.json << 'EOF'
{
  "github": {
    "auto_commit": false,
    "gist_visibility": "secret"
  },
  "hooks": {
    "pre-tool-use": [],
    "post-tool-use": [
      {
        "script": "01-state-save.py",
        "enabled": false,
        "throttle": 300
      }
    ]
  }
}
EOF
    print_status "Created default configuration (auto-commit disabled)"
fi

# Handle existing PRD
if [ -f "PRD.md" ] || [ -f "prd.md" ] || [ -f "README.md" ]; then
    print_warning "Found existing project documentation"
    mkdir -p docs/project/original
    
    for file in PRD.md prd.md README.md; do
        if [ -f "$file" ]; then
            cp "$file" "docs/project/original/"
            print_status "Preserved $file in docs/project/original/"
        fi
    done
fi

# Create commit control guide reference
cat > docs/team/QUICK_START.md << 'EOF'
# Quick Start - Claude Code Boilerplate Added!

## 🎮 Essential Commands Now Available

### Git Safety (No Auto-commits!)
- `/gs` or `/git-status` - Check changes safely
- `/cr` or `/commit-review` - Review before committing  
- `/checkpoint` - Save work state without committing

### Daily Workflow
- `/sr` or `/smart-resume` - Start each session here
- `/help` - See all available commands

## ⚙️ Current Settings
- ✅ Auto-commit: DISABLED
- ✅ Work state saves: Every 5 minutes (to gists)
- ✅ Your existing work: Preserved

## 📚 More Info
- Full guide: `docs/setup/ADD_TO_EXISTING_PROJECT.md`
- Commit control: `docs/team/COMMIT_CONTROL_GUIDE.md`
EOF

# Final summary
echo ""
echo "========================================="
echo "✅ Claude Code Boilerplate Added!"
echo "========================================="
echo ""
echo "Installation mode: $INSTALL_MODE"
echo ""
echo "🎮 Try these commands in Claude Code:"
echo "   /help        - See all commands"
echo "   /gs          - Check git status"  
echo "   /checkpoint  - Save your work"
echo "   /cr          - Commit with review"
echo ""

if [ "$INSTALL_MODE" = "minimal" ]; then
    echo "💡 To add more features later:"
    echo "   ./add-to-existing.sh standard"
    echo "   ./add-to-existing.sh full"
fi

echo ""
echo "📖 Documentation created in:"
echo "   docs/team/QUICK_START.md"
echo ""
echo "Happy coding! 🚀"
