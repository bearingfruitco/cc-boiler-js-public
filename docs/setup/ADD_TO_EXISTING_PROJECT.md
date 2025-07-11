# 🔧 Adding Claude Code Boilerplate to Existing Projects

## Overview

This guide helps you integrate Claude Code automation into your existing project without overwriting your code. You'll cherry-pick the parts you need.

## What You'll Add

### Core Systems (Recommended for All)
- `.claude/` directory - Commands, hooks, automation
- `CLAUDE.md` - AI agent instructions
- `QUICK_REFERENCE.md` - Command reference
- GitHub integration hooks

### Optional Systems
- Field Registry (for secure forms)
- Design system enforcement
- Multi-agent orchestration
- PRD-driven workflow

## Step 1: Backup Your Project

```bash
# Create a backup branch
git checkout -b pre-claude-backup
git push origin pre-claude-backup

# Return to main
git checkout main
```

## Step 2: Download Boilerplate

```bash
# In a temporary directory
cd /tmp
git clone https://github.com/bearingfruitco/claude-code-boilerplate.git
cd claude-code-boilerplate
```

## Step 3: Copy Core Claude Systems

```bash
# From your project root, copy essential Claude files
cp -r /tmp/claude-code-boilerplate/.claude .
cp /tmp/claude-code-boilerplate/CLAUDE.md .
cp /tmp/claude-code-boilerplate/QUICK_REFERENCE.md .

# Copy helpful scripts
mkdir -p scripts
cp /tmp/claude-code-boilerplate/scripts/setup-hooks.sh scripts/
cp /tmp/claude-code-boilerplate/scripts/setup-enhanced-boilerplate.sh scripts/
chmod +x scripts/*.sh
```

## Step 4: Merge .gitignore Entries

```bash
# Add these to your existing .gitignore:
cat >> .gitignore << 'EOF'

# Claude Code logs and artifacts
.claude/logs/
.claude/transcripts/
.claude/checkpoints/
.claude/team/
.claude/orchestration/active/
EOF
```

## Step 5: Selective Feature Integration

### Option A: Just Commands & Automation
```bash
# This gives you all commands without changing your code
# You already copied .claude/ in Step 3
# Just run:
./scripts/setup-hooks.sh
```

### Option B: Add Design System
```bash
# Copy design tokens and validation
cp /tmp/claude-code-boilerplate/tailwind.config.js tailwind.config.js.example
# Manually merge with your existing config

# The hooks will enforce design rules automatically
```

### Option C: Add Secure Forms System
```bash
# Copy field registry
cp -r /tmp/claude-code-boilerplate/field-registry .

# Copy security utilities
mkdir -p lib/security lib/forms
cp -r /tmp/claude-code-boilerplate/lib/security/* lib/security/
cp -r /tmp/claude-code-boilerplate/lib/forms/* lib/forms/
```

### Option D: Add PRD Templates
```bash
# Copy project templates
mkdir -p docs/project
cp /tmp/claude-code-boilerplate/docs/project/PRD_TEMPLATE.md docs/project/
cp /tmp/claude-code-boilerplate/docs/project/BUSINESS_LOGIC_TEMPLATE.md docs/project/
```

## Step 6: Configure for Your Project

### Update .claude/project-config.json
```json
{
  "projectName": "YOUR-PROJECT-NAME",
  "projectType": "existing",
  "features": {
    "prdDriven": true,
    "designSystem": true,
    "securityForms": false,
    "multiAgent": true
  },
  "integrations": {
    "github": true,
    "supabase": false
  }
}
```

### Create Initial Context
```bash
# In Claude Code
/init              # Initialize boilerplate
/cg                # Grab existing project context
/checkpoint init   # Save initial state
```

## Step 7: Test Integration

```bash
# Start Claude Code
claude-code .

# Test basic commands
/help              # Should show all commands
/sr                # Smart resume
/vd                # Validate design (if enabled)
```

## Migration Strategies

### 1. Gradual Adoption (Recommended)
- Start with just commands and hooks
- Add features as needed
- Let team get comfortable

### 2. Feature-by-Feature
- Pick one feature (e.g., secure forms)
- Implement fully
- Move to next feature

### 3. New Features Only
- Use Claude automation for new features
- Leave existing code untouched
- Gradually refactor

## Common Integration Patterns

### Existing Next.js Projects
```bash
# Your structure stays the same
# Claude adds:
.claude/           # All automation
CLAUDE.md         # AI instructions
QUICK_REFERENCE.md # Commands

# Optional additions:
field-registry/    # If using secure forms
docs/project/      # If using PRDs
```

### Existing Component Library
```bash
# Keep your components
# Add design validation:
/vd components/Button.tsx  # Validates existing components
```

### Existing Forms
```bash
# Enhance with security:
/ctf ContactForm --analyze  # Analyzes existing form
/afs components/ContactForm.tsx  # Security audit
```

## Troubleshooting

### "Command not found"
```bash
# Ensure Claude Code is started in project root
# Run /init if needed
```

### Conflicts with Existing Tools
```bash
# Disable conflicting features in .claude/config.json
# Example: disable design enforcement if you have your own
```

### Git Issues
```bash
# Claude expects Git initialized
# If not: git init
```

## What You Get

### Immediately
- 90+ commands with `/` prefix
- Auto-save to GitHub gists
- Smart resume between sessions
- GitHub issue workflow

### With Configuration
- Design system enforcement
- Security scanning
- Multi-agent orchestration
- PRD-driven development

## Next Steps

1. **Try Core Commands**
   - `/sr` - Smart resume
   - `/todo` - Task tracking
   - `/fw` - Feature workflow

2. **Explore Advanced Features**
   - `/prd` - Generate PRDs
   - `/orch` - Multi-agent work
   - `/ctf` - Secure forms

3. **Customize for Your Needs**
   - Edit `.claude/config.json`
   - Modify hooks in `.claude/hooks/`
   - Add custom commands

## Getting Help

- Quick reference: `QUICK_REFERENCE.md`
- Full guide: `docs/setup/DAY_1_COMPLETE_GUIDE.md`
- Troubleshooting: Run `/help` in Claude Code
