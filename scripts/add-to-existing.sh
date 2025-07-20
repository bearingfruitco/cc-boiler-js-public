#!/bin/bash

# Add Claude Code Boilerplate to Existing Project
# Usage: curl -sSL [url] | bash -s [minimal|full]

set -e

MODE=${1:-full}
BOILERPLATE_REPO="https://github.com/bearingfruitco/claude-code-boilerplate.git"

echo "🚀 Adding Claude Code Boilerplate to Existing Project"
echo "===================================================="
echo "Mode: $MODE"
echo ""

# Create temp directory
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Clone boilerplate
echo "📥 Downloading boilerplate..."
git clone --quiet $BOILERPLATE_REPO $TEMP_DIR

# Function to copy with backup
copy_with_backup() {
    local src=$1
    local dst=$2
    
    if [ -e "$dst" ]; then
        echo "⚠️  Backing up existing $dst to $dst.backup"
        cp -r "$dst" "$dst.backup"
    fi
    
    cp -r "$src" "$dst"
    echo "✓ Copied $dst"
}

# Minimal mode - just commands and docs
if [ "$MODE" = "minimal" ]; then
    echo ""
    echo "📦 Installing minimal Claude Code system..."
    
    # Copy essential files
    copy_with_backup "$TEMP_DIR/.claude" ".claude"
    copy_with_backup "$TEMP_DIR/CLAUDE.md" "CLAUDE.md"
    copy_with_backup "$TEMP_DIR/QUICK_REFERENCE.md" "QUICK_REFERENCE.md"
    
    # Create project config if doesn't exist
    if [ ! -f ".claude/project-config.json" ]; then
        cp "$TEMP_DIR/.claude/project-config.json" ".claude/project-config.json"
        echo "✓ Created project-config.json template"
    fi
    
    # Setup PRP directories even in minimal mode
    echo ""
    echo "📁 Setting up PRP system..."
    mkdir -p PRPs/{templates,ai_docs,active,completed,execution_logs}
    mkdir -p .claude/metrics/{prp_progress,prp_validation}
    mkdir -p .claude/context
    echo "✓ PRP directories created"
    
    echo ""
    echo "✅ Minimal installation complete!"
    echo ""
    echo "Next steps:"
    echo "1. Update .claude/project-config.json with your repo details"
    echo "2. Open in Claude Code: claude ."
    echo "3. Run: /init"
    echo "4. Try PRP: /create-prp test-feature"
    
else
    # Full mode - everything useful
    echo ""
    echo "📦 Installing full Claude Code system..."
    
    # Copy all essential directories and files
    copy_with_backup "$TEMP_DIR/.claude" ".claude"
    copy_with_backup "$TEMP_DIR/CLAUDE.md" "CLAUDE.md"
    copy_with_backup "$TEMP_DIR/QUICK_REFERENCE.md" "QUICK_REFERENCE.md"
    copy_with_backup "$TEMP_DIR/.coderabbit.yaml" ".coderabbit.yaml"
    
    # Copy scripts directory if it doesn't exist
    if [ ! -d "scripts" ]; then
        mkdir -p scripts
    fi
    cp "$TEMP_DIR/scripts/quick-setup.sh" "scripts/quick-setup.sh"
    chmod +x scripts/quick-setup.sh
    echo "✓ Copied setup script"
    
    # Setup PRP System
    echo ""
    echo "📁 Setting up complete PRP system..."
    mkdir -p PRPs/{templates,ai_docs,active,completed,execution_logs,scripts}
    mkdir -p .claude/metrics/{prp_progress,prp_validation}
    mkdir -p .claude/context
    
    # Copy PRP files
    if [ -d "$TEMP_DIR/PRPs" ]; then
        cp -r "$TEMP_DIR/PRPs/templates" "PRPs/" 2>/dev/null || true
        cp -r "$TEMP_DIR/PRPs/scripts" "PRPs/" 2>/dev/null || true
        cp "$TEMP_DIR/PRPs/README.md" "PRPs/" 2>/dev/null || true
        echo "✓ Copied PRP templates and scripts"
    fi
    
    # Create PRP base template if it doesn't exist
    if [ ! -f "PRPs/templates/prp_base.md" ]; then
        cat > PRPs/templates/prp_base.md << 'EOF'
# PRP: [FEATURE NAME]

## Metadata
- **Created**: [DATE]
- **Author**: [AUTHOR]
- **Confidence**: [1-10]
- **Complexity**: [Low/Medium/High]

## Goal
[Clear description of what needs to be built]

## Why
- **Business Value**: [Impact on users/system]
- **Technical Need**: [Problems this solves]

## What
[User-visible behavior and technical requirements]

### Success Criteria
- [ ] [Specific measurable outcome]
- [ ] [Performance requirement]
- [ ] [Security requirement]

## All Needed Context

### Documentation & References
```yaml
- url: [documentation link]
  why: [specific reason needed]
  
- file: [codebase example]
  pattern: [what to follow]
  gotcha: [what to avoid]
```

### Known Gotchas
- CRITICAL: [Important warning]
- GOTCHA: [Common mistake to avoid]
- WARNING: [Performance consideration]

## Implementation Blueprint

### Phase 1: Foundation
- Task 1: [Description]
- Task 2: [Description]

### Phase 2: Core Features
- Task 3: [Description]
- Task 4: [Description]

## Validation Loops

### Level 1: Syntax & Standards
```bash
bun run lint
bun run typecheck
```

### Level 2: Component Testing
```bash
bun test [feature]
```

### Level 3: Integration Testing
```bash
bun run test:e2e [feature]
```

### Level 4: Production Readiness
```bash
bun run lighthouse
bun run analyze
```

## Confidence Score: [X]/10

### Scoring Rationale:
- Documentation: [X]/2
- Patterns: [X]/2
- Gotchas: [X]/2
- Tests: [X]/2
- Automation: [X]/2
EOF
        echo "✓ Created PRP base template"
    fi
    
    # Optional: Copy field registry for form security
    if [ ! -d "field-registry" ]; then
        copy_with_backup "$TEMP_DIR/field-registry" "field-registry"
    fi
    
    # Optional: Copy docs structure
    if [ ! -d "docs/project" ]; then
        mkdir -p docs/project/features
        echo "✓ Created docs structure"
    fi
    
    # Add PRP scripts to package.json if it exists
    if [ -f "package.json" ] && ! grep -q "prp:run" package.json; then
        echo "📦 Adding PRP scripts to package.json..."
        # This is tricky with sed, so we'll just notify the user
        echo ""
        echo "⚠️  Please add these scripts to your package.json:"
        echo '    "prp:run": "bun run PRPs/scripts/prp-runner.ts",'
        echo '    "prp:validate": "bun run PRPs/scripts/prp-runner.ts --prp",'
        echo ""
    fi
    
    echo ""
    echo "✅ Full installation complete!"
    echo ""
    echo "Next steps:"
    echo "1. Run: ./scripts/quick-setup.sh"
    echo "2. Install GitHub Apps when prompted"
    echo "3. Open in Claude Code and run: /init"
    echo "4. Try PRP: /create-prp test-feature"
fi

echo ""
echo "📚 Documentation:"
echo "- Commands: QUICK_REFERENCE.md"
echo "- PRP Guide: PRPs/README.md"
echo "- Full guide: .claude/commands/*.md"
echo "- AI instructions: CLAUDE.md"
echo ""
echo "🎉 Ready to enhance your development workflow with PRP!"