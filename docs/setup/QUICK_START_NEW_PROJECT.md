# Quick Start - New Project

Get up and running with a new project in under 5 minutes.

## Prerequisites

- Node.js 22+ and pnpm
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
```

The setup script will:
- ✅ Configure YOUR repository (not the boilerplate)
- ✅ Update all configuration files
- ✅ Guide you through GitHub Apps installation
- ✅ Create initial commit

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

## 5. Start Building!

```bash
# Start development server
pnpm dev

# Begin work on first feature
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
- ✅ 90+ productivity commands
- ✅ Automated quality assurance

## Common Issues

### Still seeing boilerplate repo?
Run `./scripts/quick-setup.sh` again - it will fix the configuration.

### GitHub Apps not reviewing?
- Check they're installed on YOUR repo (not boilerplate)
- Wait 2-3 minutes for initial setup
- Verify in Settings → Integrations

### Commands creating issues in wrong repo?
Your `.claude/project-config.json` might be wrong. The setup script fixes this.

## Next Steps

- Read [QUICK_REFERENCE.md](../../QUICK_REFERENCE.md) for all commands
- Check [DAY_1_COMPLETE_GUIDE.md](./DAY_1_COMPLETE_GUIDE.md) for detailed walkthrough
- Start with `/fw start 1` to work on your first feature

---

**Need help?** The automated setup script handles 90% of configuration. If you hit issues, check the complete guide or run `/help setup`.
