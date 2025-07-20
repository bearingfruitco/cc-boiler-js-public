#!/bin/bash

# Quick Setup Script for Claude Code Boilerplate
# This ensures proper repository configuration and PRP system setup

set -e

echo "🚀 Claude Code Boilerplate - Quick Setup"
echo "========================================"
echo "Version: 2.6.0 with PRP System Integration"
echo ""

# Check if we have the boilerplate files
if [ ! -f "CLAUDE.md" ] || [ ! -d ".claude" ]; then
    echo "❌ ERROR: Claude Code boilerplate files not found!"
    echo "Please run this from the boilerplate directory."
    exit 1
fi

# Setup PRP System directories
echo "📁 Setting up PRP system..."
mkdir -p PRPs/{templates,ai_docs,active,completed,execution_logs}
mkdir -p .claude/metrics/{prp_progress,prp_validation}
mkdir -p .claude/context
echo "✓ PRP directories created"

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

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo "⚠️  No git repository found. Initializing..."
    git init
    echo "✓ Initialized git repository"
fi

# Check for .env.local
echo "🔐 Checking environment configuration..."
if [ ! -f ".env.local" ]; then
    echo "⚠️  WARNING: .env.local not found!"
    echo ""
    if [ -f ".env.example" ]; then
        echo "Creating .env.local from .env.example..."
        cp .env.example .env.local
        echo "✓ Created .env.local"
        echo ""
        echo "⚠️  IMPORTANT: Edit .env.local and add your actual API keys!"
        echo "   All values are currently placeholders."
        echo ""
    else
        echo "❌ ERROR: .env.example not found!"
        echo "Cannot create .env.local"
    fi
else
    echo "✓ .env.local exists"
fi
echo ""

# Check current remote
CURRENT_REMOTE=$(git config --get remote.origin.url 2>/dev/null || echo "none")
echo "Current git remote: $CURRENT_REMOTE"

# Check if still pointing to boilerplate
if [[ $CURRENT_REMOTE == *"claude-code-boilerplate"* ]]; then
    echo ""
    echo "⚠️  WARNING: You're still pointing to the boilerplate repository!"
    echo "Let's fix this..."
    echo ""
    
    # Get user input
    read -p "What's your GitHub username? " GITHUB_USER
    read -p "What's your repository name? " REPO_NAME
    read -p "Does this repository exist on GitHub yet? (y/n) " REPO_EXISTS
    
    if [[ $REPO_EXISTS == "n" ]]; then
        echo ""
        echo "Creating repository on GitHub..."
        
        # Check if gh CLI is installed
        if command -v gh &> /dev/null; then
            gh repo create "$REPO_NAME" --private --source=. --remote=origin
            echo "✓ Repository created!"
        else
            echo "GitHub CLI not found. Please create the repository manually:"
            echo "1. Go to https://github.com/new"
            echo "2. Name: $REPO_NAME"
            echo "3. Set as private (recommended)"
            echo "4. DON'T initialize with README"
            echo ""
            read -p "Press Enter when done..."
            
            # Update remote
            git remote set-url origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
        fi
    else
        # Update remote
        git remote set-url origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
    fi
    
    echo "✓ Updated git remote!"
    
    # Update project config
    if [ -f .claude/project-config.json ]; then
        # Backup original
        cp .claude/project-config.json .claude/project-config.json.backup
        
        # Update with new values using sed (works on both Mac and Linux)
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s/\"owner\": \".*\"/\"owner\": \"$GITHUB_USER\"/" .claude/project-config.json
            sed -i '' "s/\"name\": \".*\"/\"name\": \"$REPO_NAME\"/" .claude/project-config.json
        else
            # Linux
            sed -i "s/\"owner\": \".*\"/\"owner\": \"$GITHUB_USER\"/" .claude/project-config.json
            sed -i "s/\"name\": \".*\"/\"name\": \"$REPO_NAME\"/" .claude/project-config.json
        fi
        
        echo "✓ Updated .claude/project-config.json"
    else
        # Create new config
        cat > .claude/project-config.json << EOF
{
  "repository": {
    "owner": "$GITHUB_USER",
    "name": "$REPO_NAME",
    "branch": "main"
  },
  "project": {
    "name": "$REPO_NAME",
    "type": "Next.js Application",
    "initialized_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  },
  "github_apps": {
    "coderabbit": false,
    "claude_code": false,
    "checked_at": null
  },
  "prp": {
    "enabled": true,
    "default_template": "prp_base.md",
    "validation_levels": 4,
    "auto_research": true
  }
}
EOF
        echo "✓ Created .claude/project-config.json with PRP enabled"
    fi
    
    # Update package.json name
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/\"name\": \".*\"/\"name\": \"$REPO_NAME\"/" package.json
    else
        sed -i "s/\"name\": \".*\"/\"name\": \"$REPO_NAME\"/" package.json
    fi
    
    echo "✓ Updated package.json"
else
    echo "✓ Git remote is already configured correctly!"
    GITHUB_USER=$(echo $CURRENT_REMOTE | sed -n 's/.*github.com[:/]\([^/]*\)\/.*/\1/p')
    REPO_NAME=$(basename -s .git $CURRENT_REMOTE)
fi

# Add PRP runner script to package.json if not present
if ! grep -q "prp:run" package.json; then
    echo "📦 Adding PRP scripts to package.json..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' '/"scripts": {/a\
    "prp:run": "bun run PRPs/scripts/prp-runner.ts",\
    "prp:validate": "bun run PRPs/scripts/prp-runner.ts --prp",
' package.json
    else
        # Linux
        sed -i '/"scripts": {/a\    "prp:run": "bun run PRPs/scripts/prp-runner.ts",\n    "prp:validate": "bun run PRPs/scripts/prp-runner.ts --prp",' package.json
    fi
    echo "✓ Added PRP scripts"
fi

echo ""
echo "📱 Checking GitHub App Installation..."
echo ""
echo "Please install these GitHub Apps on your repository:"
echo ""
echo "1. CodeRabbit (AI Code Reviews)"
echo "   👉 https://github.com/marketplace/coderabbit"
echo "   - Select 'Only select repositories'"
echo "   - Choose: $GITHUB_USER/$REPO_NAME"
echo ""
echo "2. Claude Code (AI Development Assistant)"
echo "   👉 https://github.com/apps/claude"
echo "   - Select 'Only select repositories'"
echo "   - Choose: $GITHUB_USER/$REPO_NAME"
echo ""
read -p "Press Enter when you've installed both apps..."

# Create .coderabbit.yaml
if [ ! -f .coderabbit.yaml ]; then
    cat > .coderabbit.yaml << 'EOF'
# CodeRabbit Configuration
reviews:
  auto_review:
    enabled: true
  
  # Respect our design system
  custom_patterns:
    - pattern: "text-sm|text-lg|text-xl|font-bold|font-medium"
      message: "Use design tokens: text-size-[1-4], font-regular/semibold"
      level: error
    
    - pattern: "p-5|m-7|gap-5|space-x-5|space-y-5"
      message: "Use 4px grid: p-4, p-6, p-8"
      level: error
    
    - pattern: "console\\.log.*email|console\\.log.*phone|console\\.log.*ssn"
      message: "Never log PII to console"
      level: error

  # Don't review generated files
  path_filters:
    - "!pnpm-lock.yaml"
    - "!*.generated.ts"
    - "!*.d.ts"
EOF
    echo "✓ Created .coderabbit.yaml"
fi

# Create PRP Quick Start guide
if [ ! -f "PRPs/QUICK_START.md" ]; then
    cat > PRPs/QUICK_START.md << 'EOF'
# PRP Quick Start Guide

## Essential Commands

```bash
# Create a new PRP
/create-prp [feature-name]

# Convert existing PRD to PRP
/prd-to-prp [feature-name]

# Validate PRP completeness
/prp-validate [feature-name]

# Generate tasks from PRP
/gt [feature] --from-prp

# Execute validation loops
/prp-execute [feature-name]

# Check progress
/prp-status [feature-name]

# Complete and archive
/prp-complete [feature-name]
```

## Workflow

1. Create or convert: `/create-prp payment-system`
2. Validate: `/prp-validate payment-system`
3. Generate tasks: `/gt payment-system --from-prp`
4. Work: `/pt payment-system`
5. Validate: `/prp-execute payment-system`
6. Complete: `/prp-complete payment-system`

## Tips

- Always validate before starting implementation
- Run Level 1 validation continuously
- Use `--fix` flag for auto-corrections
- Check `/prp-status` for blockers
EOF
    echo "✓ Created PRP Quick Start guide"
fi

# Commit changes
echo ""
echo "💾 Saving configuration..."
git add -A
git commit -m "chore: configure repository with PRP system" || echo "No changes to commit"

# Final instructions
echo ""
echo "✅ Setup Complete!"
echo "================="
echo ""
echo "Repository: $GITHUB_USER/$REPO_NAME"
echo ""
echo "🚀 PRP System Features:"
echo "- Product Requirement Prompts for one-pass success"
echo "- 4-level validation loops"
echo "- Automated progress tracking"
echo "- Pattern extraction and learning"
echo ""
echo "Next steps:"
echo "1. Open in Claude Code: claude ."
echo "2. Run: /init"
echo "3. Run: /init-project"
echo "4. Try PRP: /create-prp test-feature"
echo ""
echo "📚 Documentation:"
echo "- PRP Guide: PRPs/QUICK_START.md"
echo "- Commands: QUICK_REFERENCE.md"
echo "- Workflow: docs/workflow/UNIFIED_PRP_WORKFLOW.md"
echo ""
echo "Your project is ready for AI-driven development with automated quality gates!"
echo ""
echo "🎉 Happy coding!"