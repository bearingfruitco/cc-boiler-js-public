#!/bin/bash

# quick-add-boilerplate.sh
# Simplified script for adding boilerplate to existing projects
# 
# Usage: 
#   From your existing project:
#   curl -sSL https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/scripts/quick-add-boilerplate.sh | bash

set -e

echo "🚀 Claude Code Boilerplate - Quick Add"
echo ""

# Check if in git repo
if [ ! -d ".git" ]; then
  echo "❌ Not in a git repository!"
  echo "Please run from your project root."
  exit 1
fi

# Quick backup of potential conflicts
if [ -d ".claude" ] || [ -f "CLAUDE.md" ]; then
  echo "📦 Backing up existing files..."
  mkdir -p .claude-backup-$(date +%Y%m%d_%H%M%S)
  [ -d ".claude" ] && cp -r .claude .claude-backup-*/
  [ -f "CLAUDE.md" ] && cp CLAUDE.md .claude-backup-*/
fi

echo "📥 Downloading boilerplate..."

# Create temp directory
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

# Download as zip (faster than git clone)
curl -sL https://github.com/bearingfruitco/claude-code-boilerplate/archive/main.zip -o boilerplate.zip
unzip -q boilerplate.zip
cd -

echo "🔧 Integrating..."

# Smart copy function
smart_copy() {
  local src="$1"
  local dst="$2"
  local type="$3"
  
  if [ -e "$dst" ]; then
    case "$type" in
      "rename-ours")
        # Their file exists, rename ours
        local base=$(basename "$dst")
        local new_name="${base%.*}_BOILERPLATE.${base##*.}"
        cp "$src" "$(dirname "$dst")/$new_name"
        echo "  • Added $new_name (kept your $base)"
        ;;
      "merge-dir")
        # Merge directories
        cp -rn "$src"/* "$dst"/ 2>/dev/null || true
        echo "  • Merged into $dst"
        ;;
      "skip")
        echo "  • Skipped $dst (already exists)"
        ;;
    esac
  else
    cp -r "$src" "$dst"
    echo "  • Added $dst"
  fi
}

BP_DIR="$TEMP_DIR/claude-code-boilerplate-main"

# Copy with conflict handling
smart_copy "$BP_DIR/CLAUDE.md" "./CLAUDE.md" "rename-ours"
smart_copy "$BP_DIR/.claude" "./.claude" "merge-dir"
smart_copy "$BP_DIR/.agent-os" "./.agent-os" "skip"
smart_copy "$BP_DIR/PRPs" "./PRPs" "skip"
smart_copy "$BP_DIR/field-registry" "./field-registry" "skip"
smart_copy "$BP_DIR/QUICK_REFERENCE.md" "./QUICK_REFERENCE.md" "skip"
smart_copy "$BP_DIR/.coderabbit.yaml" "./.coderabbit.yaml" "skip"

# Update .gitignore
if [ -f "$BP_DIR/.gitignore" ]; then
  echo "" >> .gitignore
  echo "# Claude Code Boilerplate" >> .gitignore
  grep -E "(\.claude/state|PRPs/active|\.agent-os/research)" "$BP_DIR/.gitignore" >> .gitignore 2>/dev/null || true
fi

# Cleanup
rm -rf "$TEMP_DIR"

echo ""
echo "✅ Integration complete!"
echo ""
echo "Next steps:"
echo "1. Run: claude ."
echo "2. Run: /sr"
echo "3. Run: /help"
echo ""
echo "If conflicts occurred, check for _BOILERPLATE files."
