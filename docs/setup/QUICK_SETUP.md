# Quick Setup Instructions

## Prerequisites

1. **Claude Pro/Max Subscription** - Claude Code is included
2. **Node.js v22+** - Required for all tools
3. **GitHub CLI** - For repo creation and integration

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
./scripts/setup-enhanced-boilerplate.sh
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

# 4. Install and setup
pnpm install
chmod +x scripts/*.sh
./scripts/setup-enhanced-boilerplate.sh

# 5. Start Claude Code
claude-code .

# 6. Initialize
/init
/init-project
```

## What Gets Set Up

✅ **GitHub Integration**
- Repo created and connected
- Auto-save to gists every 60s
- Issue/PR automation ready

✅ **Claude Code System**
- 90+ custom commands
- Hooks for automation
- Design system enforcement
- Multi-agent orchestration

✅ **Development Environment**
- Next.js 15 with TypeScript
- Tailwind with design tokens
- Supabase ready
- Testing configured

## Quick Verification

```bash
# Check GitHub
gh auth status          # Should be logged in
git remote -v          # Should show your repo

# Check Claude Code
claude-code --version  # Should work
ls .claude/           # Should see config files

# In Claude Code
/help                 # Should show commands
/sr                   # Should show smart resume
```

## Next Steps

1. **Define Your Project**
   ```bash
   /init-project      # Interactive setup
   /gi PROJECT        # Generate issues
   ```

2. **Start Building**
   ```bash
   /fw start 1        # Start first issue
   /prd feature       # Define feature
   /gt feature        # Generate tasks
   /pt feature        # Process tasks
   ```

## Troubleshooting

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

## For Detailed Instructions

See [DAY_1_COMPLETE_GUIDE.md](./DAY_1_COMPLETE_GUIDE.md)
