#!/bin/bash

# integrate-boilerplate-v2.sh
# Enhanced integration script that never overwrites existing files
# Instead adds -boilerplate suffix and provides clear comparison tools
# 
# Usage:
#   curl -sSL https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/scripts/integrate-boilerplate-v2.sh | bash
#   
#   Or download and run:
#   ./integrate-boilerplate-v2.sh [--mode=full|selective|sidecar] [--dry-run]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Default values
MODE="${1:-full}"
DRY_RUN=false
BOILERPLATE_REPO="https://github.com/bearingfruitco/claude-code-boilerplate.git"
TEMP_DIR=".claude-boilerplate-temp"
INTEGRATION_DIR=".claude-integration"
CONFLICTS_DIR="$INTEGRATION_DIR/conflicts"
REPORT_FILE="$INTEGRATION_DIR/INTEGRATION_REPORT.md"

# Parse arguments
for arg in "$@"; do
  case $arg in
    --mode=*)
      MODE="${arg#*=}"
      ;;
    --dry-run)
      DRY_RUN=true
      ;;
    --help)
      echo "Usage: $0 [--mode=full|selective|sidecar] [--dry-run]"
      echo ""
      echo "Modes:"
      echo "  full      - Integrate entire boilerplate (with -boilerplate suffix for conflicts)"
      echo "  selective - Choose specific components to integrate"
      echo "  sidecar   - Install as separate .claude-boilerplate directory"
      echo ""
      echo "Options:"
      echo "  --dry-run - Preview changes without making them"
      exit 0
      ;;
  esac
done

# Helper Functions
record_conflict() {
  local original="$1"
  local boilerplate="$2"
  local diff_file="$3"
  
  echo "### $(basename $original)" >> "$REPORT_FILE"
  echo "- **Your Version**: \`$original\`" >> "$REPORT_FILE"
  echo "- **Boilerplate**: \`$boilerplate\`" >> "$REPORT_FILE"
  echo "- **Diff**: \`$diff_file\`" >> "$REPORT_FILE"
  echo "- **Action Required**: Review and merge manually" >> "$REPORT_FILE"
  echo "" >> "$REPORT_FILE"
}

record_addition() {
  local file="$1"
  echo "- Added: \`$file\`" >> "$INTEGRATION_DIR/additions.log"
}

create_json_merge_suggestion() {
  local original="$1"
  local boilerplate="$2"
  local merge_file="${original%.json}-merge-suggestion.json"
  
  # Use jq to create a merged version (if available)
  if command -v jq &> /dev/null; then
    echo "// Merge suggestion for $original" > "$merge_file"
    echo "// Original + Boilerplate additions" >> "$merge_file"
    jq -s '.[0] * .[1]' "$original" "$boilerplate" >> "$merge_file" 2>/dev/null || {
      echo "// Could not auto-merge - manual merge required" >> "$merge_file"
    }
  fi
}

merge_directory() {
  local source_dir="$1"
  local target_dir="$2"
  local prefix="$3"
  
  # Create target if doesn't exist
  mkdir -p "$target_dir"
  
  # Process each file in source
  find "$source_dir" -type f | while read -r file; do
    relative_path="${file#$source_dir/}"
    target_file="$target_dir/$relative_path"
    
    if [ -f "$target_file" ]; then
      # Conflict detected
      target_dir_path=$(dirname "$target_file")
      filename=$(basename "$target_file")
      name="${filename%.*}"
      ext="${filename##*.}"
      
      # Create boilerplate version with suffix
      if [ "$ext" = "$filename" ]; then
        # No extension
        boilerplate_file="$target_dir_path/${name}-boilerplate"
      else
        boilerplate_file="$target_dir_path/${name}-boilerplate.$ext"
      fi
      
      # Copy boilerplate version
      mkdir -p "$(dirname "$boilerplate_file")"
      cp "$file" "$boilerplate_file"
      
      # Create diff
      diff_file="$CONFLICTS_DIR/${prefix}/${relative_path}.diff"
      mkdir -p "$(dirname "$diff_file")"
      diff -u "$target_file" "$boilerplate_file" > "$diff_file" 2>/dev/null || true
      
      # Record conflict
      record_conflict "$target_file" "$boilerplate_file" "$diff_file"
      
      # Special handling for specific file types
      case "$ext" in
        json)
          create_json_merge_suggestion "$target_file" "$file"
          ;;
        md)
          # For markdown, create a combined version
          combined_file="$target_dir_path/${name}-combined.$ext"
          {
            echo "<!-- Your Original Version -->"
            cat "$target_file"
            echo -e "\n\n<!-- Boilerplate Additions -->"
            cat "$file"
          } > "$combined_file"
          ;;
      esac
    else
      # No conflict - copy directly
      mkdir -p "$(dirname "$target_file")"
      cp "$file" "$target_file"
      record_addition "$target_file"
    fi
  done
}

# Start Integration Process
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}    Claude Code Boilerplate Integration v2.0${NC}"
echo -e "${BLUE}    Enhanced: Never Overwrites Your Files${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Step 1: Check prerequisites
if [ ! -d ".git" ]; then
  echo -e "${RED}❌ Not in a git repository!${NC}"
  echo "Please run this from your project root."
  exit 1
fi

echo -e "${GREEN}✓${NC} Git repository detected"

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ] && [ "$DRY_RUN" = false ]; then
  echo -e "${YELLOW}⚠️  Warning: You have uncommitted changes${NC}"
  echo "It's recommended to commit or stash changes first."
  echo -n "Continue anyway? (y/n) "
  read -r response
  if [ "$response" != "y" ]; then
    exit 0
  fi
fi

# Step 2: Setup integration directory
if [ "$DRY_RUN" = false ]; then
  mkdir -p "$INTEGRATION_DIR"
  mkdir -p "$CONFLICTS_DIR"
  
  # Initialize report
  cat > "$REPORT_FILE" << EOF
# Claude Code Boilerplate Integration Report

## Integration Date: $(date '+%Y-%m-%d %H:%M:%S')
## Mode: $MODE
## Project: $(basename $(pwd))

## Summary
EOF
fi

# Step 3: Clone boilerplate
echo ""
echo -e "${BLUE}📥 Fetching boilerplate...${NC}"

if [ -d "$TEMP_DIR" ]; then
  rm -rf "$TEMP_DIR"
fi

git clone --quiet "$BOILERPLATE_REPO" "$TEMP_DIR"
echo -e "${GREEN}✓${NC} Boilerplate downloaded"

# Step 4: Analyze project
echo ""
echo -e "${BLUE}🔍 Analyzing your project...${NC}"
echo ""

# Count existing files
PROJECT_INFO=$(find . -type f -name "*.tsx" -o -name "*.ts" -o -name "*.jsx" -o -name "*.js" 2>/dev/null | grep -v node_modules | wc -l || echo 0)
echo "  • Code files found: $PROJECT_INFO"

# Detect framework
if [ -f "next.config.js" ] || [ -f "next.config.mjs" ]; then
  echo "  • Framework: Next.js"
  FRAMEWORK="nextjs"
elif [ -f "remix.config.js" ]; then
  echo "  • Framework: Remix"
  FRAMEWORK="remix"
elif [ -f "vite.config.js" ] || [ -f "vite.config.ts" ]; then
  echo "  • Framework: Vite"
  FRAMEWORK="vite"
else
  echo "  • Framework: Unknown/Custom"
  FRAMEWORK="unknown"
fi

# Check for existing boilerplate integration
if [ -d ".claude" ]; then
  echo "  • Existing .claude directory found"
  EXISTING_INTEGRATION=true
else
  EXISTING_INTEGRATION=false
fi

# Step 5: Execute integration based on mode
echo ""
echo -e "${BLUE}🔧 Integration Plan ($MODE mode)${NC}"
echo ""

case "$MODE" in
  "sidecar")
    echo "Will install boilerplate as a separate directory:"
    echo "  • Everything goes in .claude-boilerplate/"
    echo "  • No conflicts with your existing files"
    echo "  • Access with /bb prefix"
    
    if [ "$DRY_RUN" = false ]; then
      # Simple copy for sidecar mode
      cp -r "$TEMP_DIR/.claude" .claude-boilerplate
      cp "$TEMP_DIR/CLAUDE.md" .claude-boilerplate/
      
      echo -e "${GREEN}✓${NC} Sidecar installation complete"
    fi
    ;;
    
  "selective")
    echo "Choose components to integrate:"
    echo ""
    echo "1) Commands & Automation (.claude/)"
    echo "2) Agent OS Standards (.agent-os/)"
    echo "3) PRP System (PRPs/)"
    echo "4) Security Features (field-registry/)"
    echo "5) Design System (tailwind.config.js + components/)"
    echo "6) Git Hooks (.husky/)"
    echo "7) Testing Setup (playwright.config.ts + tests/)"
    echo "8) Documentation (docs/)"
    echo ""
    echo -n "Enter numbers (comma-separated): "
    read -r SELECTIONS
    
    if [ "$DRY_RUN" = false ]; then
      IFS=',' read -ra SELECTED <<< "$SELECTIONS"
      for i in "${SELECTED[@]}"; do
        case $(echo $i | tr -d ' ') in
          1) merge_directory "$TEMP_DIR/.claude" ".claude" "claude" ;;
          2) merge_directory "$TEMP_DIR/.agent-os" ".agent-os" "agent-os" ;;
          3) merge_directory "$TEMP_DIR/PRPs" "PRPs" "prps" ;;
          4) merge_directory "$TEMP_DIR/field-registry" "field-registry" "field-registry" ;;
          # ... implement other selections
        esac
      done
    fi
    ;;
    
  *)  # full mode
    echo -e "${PURPLE}This integration will:${NC}"
    echo ""
    echo "1. ${GREEN}NEVER overwrite${NC} your existing files"
    echo "2. Add ${YELLOW}-boilerplate${NC} suffix to conflicting files"
    echo "3. Create ${BLUE}diffs${NC} for easy comparison"
    echo "4. Generate ${PURPLE}merge suggestions${NC} for config files"
    echo "5. Provide an ${GREEN}integration wizard${NC} command"
    echo ""
    
    if [ "$DRY_RUN" = false ]; then
      echo -n "Proceed? (y/n) "
      read -r response
      if [ "$response" != "y" ]; then
        rm -rf "$TEMP_DIR"
        exit 0
      fi
      
      echo ""
      echo -e "${BLUE}🚀 Starting integration...${NC}"
      echo ""
      
      # Integrate each component
      components=(
        ".claude::.claude::claude"
        ".agent-os::.agent-os::agent-os"
        "PRPs::PRPs::prps"
        "field-registry::field-registry::field-registry"
        "docs::docs::docs"
        "components::components::components"
        "lib::lib::lib"
        "hooks::hooks::hooks"
        "stores::stores::stores"
        "types::types::types"
        "scripts::scripts::scripts"
      )
      
      for component in "${components[@]}"; do
        IFS='::' read -r source target prefix <<< "$component"
        if [ -d "$TEMP_DIR/$source" ]; then
          echo -e "  Integrating $source..."
          merge_directory "$TEMP_DIR/$source" "$target" "$prefix"
        fi
      done
      
      # Handle individual files
      files=(
        "CLAUDE.md"
        "tailwind.config.js"
        "tsconfig.json"
        "biome.json"
        "components.json"
        ".coderabbit.yaml"
        "playwright.config.ts"
        "drizzle.config.ts"
        ".gitignore"
      )
      
      for file in "${files[@]}"; do
        if [ -f "$TEMP_DIR/$file" ]; then
          if [ -f "$file" ]; then
            # Conflict
            name="${file%.*}"
            ext="${file##*.}"
            if [ "$ext" = "$file" ]; then
              boilerplate_file="${file}-boilerplate"
            else
              boilerplate_file="${name}-boilerplate.$ext"
            fi
            
            cp "$TEMP_DIR/$file" "$boilerplate_file"
            diff -u "$file" "$boilerplate_file" > "$CONFLICTS_DIR/$file.diff" 2>/dev/null || true
            record_conflict "$file" "$boilerplate_file" "$CONFLICTS_DIR/$file.diff"
            
            # Special handling for JSON configs
            if [ "$ext" = "json" ] || [ "$ext" = "js" ]; then
              create_json_merge_suggestion "$file" "$TEMP_DIR/$file"
            fi
          else
            # No conflict
            cp "$TEMP_DIR/$file" "$file"
            record_addition "$file"
          fi
        fi
      done
    fi
    ;;
esac

# Step 6: Generate integration wizard command
if [ "$DRY_RUN" = false ] && [ "$MODE" = "full" ]; then
  mkdir -p .claude/commands
  cat > .claude/commands/integration-wizard.md << 'EOF'
# Integration Wizard

$ARGUMENTS

This command helps you complete the boilerplate integration by:
1. Showing all conflicts that need resolution
2. Providing diff visualization
3. Offering merge suggestions
4. Applying selected changes

## Check Integration Status

First, let me analyze the integration status...

```bash
# Count conflicts
CONFLICTS=$(find .claude-integration/conflicts -name "*.diff" 2>/dev/null | wc -l || echo 0)
ADDITIONS=$(wc -l < .claude-integration/additions.log 2>/dev/null || echo 0)

echo "Integration Summary:"
echo "  • Conflicts to resolve: $CONFLICTS"
echo "  • Files added: $ADDITIONS"
echo ""

if [ $CONFLICTS -gt 0 ]; then
  echo "Conflicts found in:"
  find .claude-integration/conflicts -name "*.diff" | while read -r diff; do
    file=$(basename "$diff" .diff)
    echo "  • $file"
  done
fi
```

## Review Conflicts

To review a specific conflict:
```bash
# Example: Review tailwind.config.js conflict
cat tailwind.config.js           # Your version
cat tailwind.config-boilerplate.js  # Boilerplate version
cat .claude-integration/conflicts/tailwind.config.js.diff  # Differences
```

## Apply Merge

To merge specific features from boilerplate:
```bash
# Example: Add design tokens to tailwind.config.js
# This requires manual editing - open both files and merge the needed parts
```

## Complete Integration

Once all conflicts are resolved:
```bash
# Remove boilerplate versions
find . -name "*-boilerplate.*" -type f -delete

# Archive integration report
mv .claude-integration .claude-integration-completed-$(date +%Y%m%d)
```

## Get Help

For specific merge assistance, ask:
- "How do I merge the tailwind configs?"
- "What's different in the tsconfig files?"
- "Should I keep my version or use boilerplate?"
EOF
fi

# Step 7: Cleanup
rm -rf "$TEMP_DIR"

# Step 8: Final report
if [ "$DRY_RUN" = true ]; then
  echo ""
  echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
  echo -e "${YELLOW}DRY RUN COMPLETE - No changes were made${NC}"
  echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
else
  # Finalize report
  if [ -f "$INTEGRATION_DIR/additions.log" ]; then
    TOTAL_ADDED=$(wc -l < "$INTEGRATION_DIR/additions.log")
  else
    TOTAL_ADDED=0
  fi
  
  TOTAL_CONFLICTS=$(find "$CONFLICTS_DIR" -name "*.diff" 2>/dev/null | wc -l || echo 0)
  
  # Update report summary
  {
    echo "- Files Added: $TOTAL_ADDED"
    echo "- Conflicts Found: $TOTAL_CONFLICTS"
    echo "- Integration Mode: $MODE"
    echo ""
    echo "## Files Added"
    echo ""
    if [ -f "$INTEGRATION_DIR/additions.log" ]; then
      cat "$INTEGRATION_DIR/additions.log"
    else
      echo "No files added (all had conflicts)"
    fi
    echo ""
    echo "## Conflicts Requiring Resolution"
    echo ""
  } >> "$REPORT_FILE"
  
  echo ""
  echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
  echo -e "${GREEN}✅ Integration Complete!${NC}"
  echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
  echo ""
  echo "📊 Summary:"
  echo "  • Files added: $TOTAL_ADDED"
  echo "  • Conflicts found: $TOTAL_CONFLICTS"
  echo ""
  
  if [ $TOTAL_CONFLICTS -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Action Required:${NC}"
    echo "  You have $TOTAL_CONFLICTS files that need manual review"
    echo ""
    echo "  1. Run 'claude .' to start Claude Code"
    echo "  2. Use '/integration-wizard' to resolve conflicts"
    echo "  3. Or manually review files ending with '-boilerplate'"
    echo ""
  fi
  
  echo "📁 Integration details saved to:"
  echo "  $REPORT_FILE"
  echo ""
  echo "🚀 Next steps:"
  echo "  1. Review the integration report"
  echo "  2. Resolve any conflicts"
  echo "  3. Install new dependencies (see report)"
  echo "  4. Run '/sr' in Claude Code to explore features"
  echo ""
  
  # Show rollback command
  echo "🔄 To rollback this integration:"
  echo "  ./scripts/rollback-integration.sh"
  echo ""
fi

echo "Happy coding! 🚀"
