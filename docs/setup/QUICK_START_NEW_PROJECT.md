# 🚀 Quick Start - New Project from Boilerplate

## Prerequisites
```bash
# Verify you have these installed:
claude-code --version  # Claude Code (with Claude Pro/Max)
git --version         # Git
gh --version          # GitHub CLI
node --version        # Node v22+
bun --version         # Bun v1.0+
pnpm --version        # pnpm v9+
```

## Option 1: Clone from GitHub (Recommended)

```bash
# 1. Clone the boilerplate with your project name
git clone https://github.com/bearingfruitco/claude-code-boilerplate.git my-awesome-project
cd my-awesome-project

# 2. Remove boilerplate history and create your own
rm -rf .git
git init
git add .
git commit -m "Initial commit from Claude Code boilerplate"

# 3. Create YOUR GitHub repo and push
gh repo create my-awesome-project --private --source=. --remote=origin --push

# 4. Install dependencies with pnpm
pnpm install

# 5. Verify Bun and Biome
bun --version          # Should show 1.0+
pnpm biome --version   # Should show 1.5+

# 6. Start Claude Code
claude-code .

# 7. Initialize (in Claude Code)
/init              # One-time boilerplate setup
/init-project      # Define YOUR project (interview)
/gi PROJECT        # Generate GitHub issues
```

## Option 2: Use GitHub Template (If Available)

```bash
# 1. Go to https://github.com/bearingfruitco/claude-code-boilerplate
# 2. Click "Use this template" → "Create a new repository"
# 3. Clone your new repo:
git clone https://github.com/YOUR-USERNAME/YOUR-PROJECT.git
cd YOUR-PROJECT

# 4. Continue from step 4 above (pnpm install)
```

## Option 3: Download ZIP

```bash
# 1. Download latest release
curl -L https://github.com/bearingfruitco/claude-code-boilerplate/archive/main.zip -o boilerplate.zip
unzip boilerplate.zip
mv claude-code-boilerplate-main my-awesome-project
cd my-awesome-project

# 2. Initialize Git
git init
git add .
git commit -m "Initial commit from Claude Code boilerplate"

# 3. Continue from step 3 in Option 1
```

## Quick Setup Commands

```bash
# After cloning, run these in sequence:
pnpm install              # Install dependencies
bun test                  # Verify Bun is working
pnpm lint                 # Verify Biome is working
chmod +x scripts/*.sh     # Make scripts executable
./scripts/setup-enhanced-boilerplate.sh  # Run setup

# Start developing
bun dev                   # Start Next.js dev server
```

## What's Included

### Core Technologies
- **Runtime**: Bun v1.0+ (fast JavaScript runtime)
- **Package Manager**: pnpm v9 (efficient dependency management)
- **Linting/Formatting**: Biome (fast, unified tooling)
- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS v4
- **Database**: Supabase + Drizzle ORM
- **Testing**: Bun test + Playwright

### Claude Code Features
- **90+ Custom Commands** with aliases
- **PRD-driven development** workflow
- **Auto-save** to GitHub gists every 60s
- **Design system** enforcement (4 sizes, 2 weights, 4px grid)
- **Multi-agent** orchestration (9 personas)
- **Security-first** forms with PII protection

## Development Commands

```bash
# Start development
bun dev                   # Next.js dev server

# Code quality (Biome)
pnpm lint                 # Check for issues
pnpm lint:fix            # Auto-fix issues
pnpm format              # Format code

# Testing (Bun)
bun test                  # Run all tests
bun test:watch           # Watch mode
bun test:coverage        # Coverage report

# Type checking
pnpm typecheck           # TypeScript validation

# Build
bun build                # Production build
bun start                # Start production server
```

## What Happens Next?

After `/init-project`, the system will:
1. Interview you about your project
2. Create PROJECT_PRD.md with your vision
3. Generate GitHub issues for each major feature
4. Set up your workflow

Then you can start building:
```bash
/fw start 1        # Start first issue
/prd feature       # Define feature
/gt feature        # Generate tasks
/pt feature        # Process tasks
```

## 🎯 Success Checklist

- [ ] Boilerplate cloned/downloaded
- [ ] Git initialized with YOUR repo
- [ ] Dependencies installed with pnpm
- [ ] Bun verified (`bun --version`)
- [ ] Biome working (`pnpm lint`)
- [ ] Claude Code started
- [ ] `/init` completed
- [ ] `/init-project` defined YOUR project
- [ ] GitHub issues created
- [ ] Ready to build!

## Need Help?

- Full setup: `docs/setup/DAY_1_COMPLETE_GUIDE.md`
- Daily workflow: `QUICK_REFERENCE.md`
- Bun docs: https://bun.sh/docs
- Biome docs: https://biomejs.dev/

## Common Issues

**"bun: command not found"**
```bash
curl -fsSL https://bun.sh/install | bash
source ~/.zshrc  # or ~/.bashrc
```

**"pnpm: command not found"**
```bash
npm install -g pnpm@9
```

**Biome errors on commit**
```bash
pnpm lint:fix    # Auto-fix most issues
pnpm format      # Format code
```

---

Ready to build fast with Bun + Biome + Claude Code! 🚀
