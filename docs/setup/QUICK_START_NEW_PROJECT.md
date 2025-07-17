# Quick Start - New Project

Get up and running with a new project in under 5 minutes with full PRP support.

## Prerequisites

- Node.js 22+ and pnpm (or bun)
- GitHub account
- Claude Code installed (claude.ai/code)

## 1. Clone and Setup (2 minutes)

```bash
# Clone the boilerplate
git clone https://github.com/bearingfruitco/claude-code-boilerplate.git my-awesome-app
cd my-awesome-app

# Run the automated setup script
chmod +x scripts/quick-setup.sh
./scripts/quick-setup.sh

# Setup PRP system (NEW)
chmod +x setup-prp.sh
./setup-prp.sh
```

The setup scripts will:
- ✅ Configure YOUR repository (not the boilerplate)
- ✅ Update all configuration files
- ✅ Guide you through GitHub Apps installation
- ✅ Create initial commit
- ✅ Setup PRP templates and validation loops

## 2. Install GitHub Apps (2 minutes)

When prompted by the setup script, install these apps on YOUR repository:

### CodeRabbit (AI Code Reviews)
- Go to: https://github.com/marketplace/coderabbit
- Choose "Pro" plan ($24/developer/month)
- Select "Only select repositories" → Choose YOUR repo

### Claude Code (GitHub Integration)
- Go to: https://github.com/apps/claude
- Click "Install"
- Select "Only select repositories" → Choose YOUR repo

## 3. Configure Environment (1 minute)

```bash
# Install dependencies
pnpm install

# Setup environment
cp .env.example .env.local

# Edit .env.local with your values:
# - Supabase credentials
# - Any API keys you need
```

## 4. Initialize Your Project

```bash
# Open in Claude Code
claude .

# Or use VSCode/Cursor with Claude Code extension
code .
```

Run these commands in Claude Code:

```bash
/init                  # Initialize the system
/init-project          # Setup YOUR project (answer questions)
/gi PROJECT            # Generate GitHub issues
```

## 5. Start Building with PRPs!

### Option A: PRP Workflow (Recommended)
```bash
# Start development server
pnpm dev

# Begin work with PRP methodology
/fw start 1            # Start working on issue #1
/create-prp implement issue #1  # Generate comprehensive PRP
/prp-execute feature-name       # Validate environment
# ... implement following PRP blueprint ...
/prp-execute feature-name       # Final validation
/fw complete           # Create PR
```

### Option B: Traditional PRD Workflow
```bash
# Start development server
pnpm dev

# Traditional PRD approach
/fw start 1            # Start working on issue #1
/prd [feature-name]    # Create detailed PRD
/gt [feature-name]     # Generate tasks
/pt [feature-name]     # Process tasks
```

## What You Get

- ✅ Properly configured repository
- ✅ AI-powered code reviews on every PR
- ✅ Design system enforcement
- ✅ PRD-driven development workflow
- ✅ **PRP methodology for one-pass implementation**
- ✅ **4-level validation loops**
- ✅ **AI-optimized documentation**
- ✅ 110+ productivity commands
- ✅ Automated quality assurance

## PRP Quick Reference

```bash
# Create PRPs
/prp user authentication      # Short alias
/create-prp checkout flow     # Full command

# Execute validation
/prp-execute auth            # Run all validations
/prp-execute auth --fix      # Auto-fix issues
/prp-execute auth --level 1  # Just syntax checks

# Validation levels
Level 1: Syntax & Standards (continuous)
Level 2: Component Testing (after components)
Level 3: Integration Testing (after connecting)
Level 4: Production Readiness (before PR)
```

## Common Issues

### Still seeing boilerplate repo?
Run `./scripts/quick-setup.sh` again - it will fix the configuration.

### GitHub Apps not reviewing?
- Check they're installed on YOUR repo (not boilerplate)
- Wait 2-3 minutes for initial setup
- Verify in Settings → Integrations

### Commands creating issues in wrong repo?
Your `.claude/project-config.json` might be wrong. The setup script fixes this.

### PRP validation failing?
- Run with `--verbose` flag for details
- Use `--fix` to auto-fix common issues
- Check `/bt list` for known bugs

## Next Steps

- Read [PRP_WORKFLOW_GUIDE.md](../workflow/PRP_WORKFLOW_GUIDE.md) for PRP methodology
- Check [QUICK_REFERENCE.md](../../QUICK_REFERENCE.md) for all commands
- Review [DAY_1_COMPLETE_GUIDE.md](./DAY_1_COMPLETE_GUIDE.md) for detailed walkthrough
- Start with `/fw start 1` and `/prp` for your first feature

---

**Need help?** 
- PRP issues: Check `PRPs/README.md`
- Setup issues: Run `/help setup`
- Validation issues: Use `/prp-execute --help`
