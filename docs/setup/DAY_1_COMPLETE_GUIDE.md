# 🚀 Day 1 Complete Setup Guide - Zero to Production-Ready

## What This Guide Gives You
By the end of this guide, you'll have:
- ✅ Complete project setup with Claude Code
- ✅ PRD-driven development workflow
- ✅ Task-based feature building
- ✅ Auto-updating documentation
- ✅ Browser testing with Playwright
- ✅ All automation working
- ✅ **GitHub integration with auto-saves**
- ✅ **Regular commits every 3 tasks**
- ✅ **Context that never gets lost**

## 🐙 How GitHub Integration Works

**Automatic Features:**
- **Gist saves**: Every 60 seconds your work state saves to GitHub gists
- **Regular commits**: Every 3 tasks or 30 minutes
- **Issue tracking**: All work linked to GitHub issues
- **Smart resume**: Restores context from multiple GitHub sources

## Prerequisites
```bash
# Verify you have these installed:
claude-code --version  # Need @anthropic-ai/claude-code
git --version
gh --version
node --version  # Need v22+
pnpm --version  # Need v9+
python3 --version
bun --version   # Need v1.0+

# If missing any:
# Claude Code: npm install -g @anthropic-ai/claude-code (included with Claude Pro/Max)
# Git: brew install git
# GitHub CLI: brew install gh
# Node: brew install node@22
# pnpm: npm install -g pnpm@9
# Python: brew install python@3
# Bun: curl -fsSL https://bun.sh/install | bash
```

## Step 0: Install Claude Code (REQUIRED)

⚠️ **Claude Code is required for all automation features in this boilerplate**

```bash
# Install Claude Code (included with Claude Pro/Max subscriptions)
npm install -g @anthropic-ai/claude-code

# Verify installation
claude-code --version

# If command not found, reload your shell:
source ~/.zshrc  # or restart terminal
```

## Step 0.5: Configure GitHub Access (CRITICAL)

**This enables all automatic features:**

```bash
# Authenticate GitHub CLI
gh auth login
# Choose: GitHub.com → HTTPS → Yes → Browser

# Verify authentication
gh auth status
# Should show: ✓ Logged in to github.com

# Test GitHub access
gh issue list --repo cli/cli --limit 3

# Configure git identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**Why this matters:**
- Enables auto-save to gists every 60 seconds
- Allows automatic issue/PR creation
- Powers the `/sr` smart resume feature
- Makes `/fw` commands work properly

## Step 1: Project Creation (5 minutes)

### Option A: Clone from GitHub (RECOMMENDED)

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
```

### Option B: Copy from Local (If you have it)

```bash
# Create and setup project
mkdir my-awesome-project && cd my-awesome-project

# Copy boilerplate
cp -r /path/to/claude-code-boilerplate/* .
cp -r /path/to/claude-code-boilerplate/.claude .

# Initialize git
git init && git add . && git commit -m "Initial boilerplate"

# Create GitHub repo
gh repo create my-awesome-project --private --source=. --remote=origin --push
```

## Step 2: Initial Setup (2 minutes)

```bash
# Install dependencies
pnpm install

# Make scripts executable
chmod +x scripts/*.sh

# Run setup script
./scripts/setup-enhanced-boilerplate.sh

# Create .env.local (add your keys later)
cp .env.example .env.local
```

## Step 3: Start Claude Code (30 seconds)

```bash
# Start Claude Code in your project
claude-code .

# The AI will greet you. Your first commands:
/init              # One-time initialization (creates .claude/ configs)
```

## Step 4: Define Your Project (10 minutes)

Run the project initialization interview:

```bash
/init-project      # or /ip
```

This interactive process will:
1. Ask about your project type
2. Define your tech stack preferences
3. Create PROJECT_PRD.md with your vision
4. Set up BUSINESS_RULES.md
5. Configure project settings

Example responses:
```
Q: "What type of project?"
A: "A task management app for remote teams"

Q: "Key features?"
A: "Task creation, assignment, progress tracking, team chat"

Q: "Target users?"
A: "Remote teams of 5-50 people"
```

## Step 5: Generate GitHub Issues (2 minutes)

```bash
# Convert your PROJECT_PRD into GitHub issues
/generate-issues PROJECT    # or /gi PROJECT
```

This creates issues like:
- Issue #1: User Authentication
- Issue #2: Task Management
- Issue #3: Team Dashboard
- Issue #4: Real-time Chat

## Step 6: Start Your First Feature (20 minutes)

```bash
# 1. Start working on first issue
/fw start 1                # Creates branch: feature/1-user-authentication

# 2. Generate detailed PRD for this feature
/prd user-authentication

# 3. Generate tasks from PRD
/gt user-authentication     # Creates ~20 tasks

# 4. Start processing tasks
/pt user-authentication
```

The system will:
- Work through each task (5-15 minutes each)
- Auto-save progress every 60 seconds
- Test implementations before moving on
- Commit every 3 tasks

## Step 7: Verify Everything Works

### Check GitHub Integration
```bash
# In terminal (not Claude Code)
gh gist list --limit 3     # Should show your saved states
git log --oneline -5       # Should show commits
gh issue list              # Should show your issues
```

### Check Claude Commands
```bash
# In Claude Code
/help                      # See all commands
/sr                        # Smart resume (shows saved state)
/ts                        # Task status
/sas                       # Sub-agent status
```

### Quick Component Test
```bash
# Create a test component
/cc ui TestButton

# Validate design system
/vd

# You should see the component created with proper styling
```

## Step 8: Daily Workflow Setup

### Morning Routine
```bash
/sr                        # Resume where you left off
/ws                        # Check work status
/todo list                 # See any TODOs
```

### During Development
```bash
/cc ui ComponentName       # Create components
/vd                        # Validate continuously
/checkpoint create         # Manual saves
/btf feature-name         # Browser test
```

### End of Day
```bash
/fw complete 1            # When feature is done
/checkpoint create "EOD"  # Final save
```

## Common Issues & Solutions

### "Command not found"
```bash
# Make sure you're in Claude Code, not terminal
# Run /init if needed
```

### "Git not configured"
```bash
gh auth login
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### "Can't push to GitHub"
```bash
# Check remote
git remote -v
# If missing, add it:
gh repo create --private
```

## Success Checklist

- [ ] Claude Code installed and working
- [ ] GitHub CLI authenticated
- [ ] Project cloned/created
- [ ] Dependencies installed
- [ ] `/init` completed
- [ ] `/init-project` defined your project
- [ ] GitHub issues created
- [ ] First feature started
- [ ] Auto-save verified (check gists)

## What's Next?

1. **Continue First Feature**
   ```bash
   /pt user-authentication   # Continue tasks
   /btf user-authentication  # Test in browser
   /fw complete 1           # Create PR
   ```

2. **Start Next Feature**
   ```bash
   /fw start 2              # Start issue #2
   /prd task-management     # Define it
   /gt task-management      # Generate tasks
   /orch task-management    # Use multi-agent
   ```

3. **Explore Advanced Features**
   - `/orch` - Multi-agent orchestration
   - `/ctf` - Create secure forms
   - `/compress` - Optimize context

## 🎉 Congratulations!

You now have:
- ✅ A working project with Claude automation
- ✅ GitHub integration saving every 60 seconds
- ✅ PRD-driven development workflow
- ✅ Design system enforcement
- ✅ Multi-agent capabilities
- ✅ Perfect context preservation

**Pro tip**: Keep `QUICK_REFERENCE.md` open in another tab for easy command access.

## Need Help?

- Run `/help` for command assistance
- Check `/error-recovery` if something breaks
- Review logs in `.claude/logs/`

---

Welcome to the future of AI-assisted development! 🚀
