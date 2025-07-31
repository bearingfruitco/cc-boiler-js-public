# Quick Setup Instructions

## Prerequisites

1. **Claude Pro/Max Subscription** - Claude Code is included
2. **Node.js v22+** - Required for tools
3. **Bun v1.0+** - JavaScript runtime
4. **pnpm v9+** - Package manager
5. **GitHub CLI** - For repo creation and integration

## One-Command Setup (After Cloning)

```bash
# Clone and setup in one go
git clone https://github.com/bearingfruitco/claude-code-boilerplate.git my-project && \
cd my-project && \
rm -rf .git && \
git init && \
git add . && \
git commit -m "Initial commit from boilerplate" && \
gh repo create my-project --private --source=. --remote=origin --push && \
pnpm install && \
chmod +x scripts/*.sh && \
./scripts/setup-enhanced-boilerplate.sh && \
./setup-prp.sh
```

## Step-by-Step Alternative

```bash
# 1. Clone the boilerplate
git clone https://github.com/bearingfruitco/claude-code-boilerplate.git my-project
cd my-project

# 2. Create your own repo
rm -rf .git
git init
git add .
git commit -m "Initial commit from boilerplate"

# 3. Push to GitHub
gh repo create my-project --private --source=. --remote=origin --push

# 4. Install with pnpm and setup
pnpm install
chmod +x scripts/*.sh
./scripts/setup-enhanced-boilerplate.sh

# 5. Setup PRP system (NEW in v2.6.0)
./setup-prp.sh

# 6. Verify tools
bun --version        # Should show 1.0+
pnpm biome --version # Should show 1.5+

# 7. Start Claude Code
claude-code .

# 8. Initialize
/init                # One-time setup
/init-project        # Define YOUR project
```

## What Gets Set Up

✅ **Development Environment**
- Bun runtime for fast execution
- Biome for linting and formatting
- pnpm for efficient package management
- Next.js 15 with TypeScript

✅ **GitHub Integration**
- Repo created and connected
- Auto-save to gists every 60s
- Issue/PR automation ready

✅ **Claude Code System**
- 110+ custom commands
- Hooks for automation
- Design system enforcement
- Multi-agent orchestration
- PRP methodology (NEW v2.6.0)
  - One-pass implementation
  - 4-level validation loops
  - AI documentation
- Safety features
  - Truth enforcement
  - Deletion protection
  - Hydration safety
  - Import validation

✅ **Code Quality**
- Biome pre-configured
- Git hooks with Husky
- TypeScript strict mode
- Test setup with Bun
- PRP validation runner

## Quick Commands

```bash
# Development
bun dev              # Start dev server
bun build            # Build for production
bun test             # Run tests

# Code Quality
pnpm lint            # Check with Biome
pnpm lint:fix        # Fix issues
pnpm format          # Format code
pnpm typecheck       # Check types

# Claude Code (Traditional)
/sr                  # Smart resume
/help                # Show all commands
/init-project        # Start new project
/prd                 # Create PRD

# Claude Code (PRP - NEW)
/create-prp          # Create PRP for one-pass success
/prp-execute         # Run validation loops
/prp feature-name    # Quick PRP creation
```

## Quick Verification

```bash
# Check tools
bun --version          # Should show 1.0+
pnpm --version         # Should show 9+
pnpm biome --version   # Should show 1.5+

# Check GitHub
gh auth status         # Should be logged in
git remote -v          # Should show your repo

# Check Claude Code
claude-code --version  # Should work
ls .claude/           # Should see config files
ls PRPs/              # Should see PRP structure (NEW)

# In Claude Code
/help                 # Should show commands
/sr                   # Should show smart resume + safety status
/facts                # Should show protected values
/help new             # Should show new features
/prp --help           # Should show PRP help (NEW)
```

## Next Steps

### Option 1: Traditional PRD Workflow
```bash
/init-project      # Interactive setup
/gi PROJECT        # Generate issues
/fw start 1        # Start first issue
/prd feature       # Define feature
/gt feature        # Generate tasks
/pt feature        # Process tasks
```

### Option 2: PRP Workflow (NEW - Recommended)
```bash
/init-project             # Interactive setup
/gi PROJECT               # Generate issues
/fw start 1               # Start first issue
/create-prp feature-name  # Generate comprehensive PRP
/prp-execute feature-name # Validate readiness
# Implement following PRP blueprint
/prp-execute feature-name # Re-validate after implementation
```

## Troubleshooting

**"command not found: bun"**
```bash
curl -fsSL https://bun.sh/install | bash
source ~/.zshrc
```

**"command not found: claude-code"**
```bash
npm install -g @anthropic-ai/claude-code
source ~/.zshrc
```

**"command not found: gh"**
```bash
brew install gh
gh auth login
```

**"command not found: pnpm"**
```bash
npm install -g pnpm@9
```

**Biome errors**
```bash
pnpm lint:fix     # Auto-fix most issues
pnpm format       # Format code
```

**PRP validation failures**
```bash
/prp-execute feature --fix     # Try auto-fix
/prp-execute feature --level 1 # Run specific level
/prp-execute feature --verbose # See detailed output
```

## For Detailed Instructions

- [DAY_1_COMPLETE_GUIDE.md](./DAY_1_COMPLETE_GUIDE.md) - Full setup guide
- [PRP_WORKFLOW_GUIDE.md](../workflow/PRP_WORKFLOW_GUIDE.md) - PRP methodology guide
- [DAILY_WORKFLOW.md](../workflow/DAILY_WORKFLOW.md) - Daily development workflow
