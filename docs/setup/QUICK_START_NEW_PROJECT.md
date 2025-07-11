# 🚀 Quick Start - New Project from Boilerplate

## Prerequisites
```bash
# Verify you have these installed:
claude-code --version  # Claude Code (with Claude Pro/Max)
git --version         # Git
gh --version          # GitHub CLI
node --version        # Node v22+
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

# 4. Install dependencies
pnpm install

# 5. Start Claude Code
claude-code .

# 6. Initialize (in Claude Code)
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

# 4. Continue from step 4 above
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

## What Happens Next?

After `/init-project`, the system will:
1. Interview you about your project
2. Create PROJECT_PRD.md with your vision
3. Generate GitHub issues for each major feature
4. Set up your workflow

Then you can start building:
```bash
/fw start 1        # Start first issue
/prd feature-name  # Create feature PRD
/gt feature-name   # Generate tasks
/pt feature-name   # Process tasks
```

## 🎯 Success Checklist

- [ ] Boilerplate cloned/downloaded
- [ ] Git initialized with YOUR repo
- [ ] Dependencies installed
- [ ] Claude Code started
- [ ] `/init` completed
- [ ] `/init-project` defined YOUR project
- [ ] GitHub issues created
- [ ] Ready to build!

## Need Help?

- Full setup: `docs/setup/DAY_1_COMPLETE_GUIDE.md`
- Daily workflow: `QUICK_REFERENCE.md`
- Troubleshooting: `docs/setup/TROUBLESHOOTING.md`
