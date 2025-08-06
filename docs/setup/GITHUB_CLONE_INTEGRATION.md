# GitHub Clone to Boilerplate Integration Guide

> **The Complete Guide**: Clone any GitHub repository and safely integrate the Claude Code Boilerplate v4.0.0 without breaking anything.

## 🎯 Quick Start (5 Minutes)

```bash
# 1. Clone the GitHub project
git clone https://github.com/[user]/[project].git
cd [project]

# 2. Create integration branch
git checkout -b integrate-boilerplate

# 3. Open in Claude Code
claude .

# 4. In Claude Code, run:
/analyze-existing full      # Analyze what you have
/integrate-boilerplate      # Add boilerplate safely
/sr                        # Load everything
/fw start                  # Start building!
```

That's it! Your project now has 150+ commands, 31 AI agents, and complete automation.

## 📋 Table of Contents

1. [Pre-Integration Checklist](#pre-integration-checklist)
2. [Step-by-Step Integration](#step-by-step-integration)
3. [Integration Methods](#integration-methods)
4. [Handling Existing Boilerplate Versions](#handling-existing-boilerplate-versions)
5. [What Gets Added vs Protected](#what-gets-added-vs-protected)
6. [Post-Integration Setup](#post-integration-setup)
7. [Common Scenarios](#common-scenarios)
8. [Troubleshooting](#troubleshooting)
9. [Rollback & Recovery](#rollback--recovery)

## Pre-Integration Checklist

Before starting, ensure you have:

- [ ] **Git repository cloned locally**
- [ ] **Claude Code installed** (`claude` command works)
- [ ] **Node.js 18+** and **pnpm** installed
- [ ] **5-10 minutes** for integration
- [ ] **Admin access** to the repository (for pushing changes)

## Step-by-Step Integration

### Step 1: Clone and Prepare

```bash
# Clone the repository you want to enhance
git clone https://github.com/[username]/[repository].git my-project
cd my-project

# Create a branch for integration (recommended)
git checkout -b integrate-boilerplate

# Check what you're starting with
ls -la
git status
```

### Step 2: Open in Claude Code

```bash
# Open the project in Claude Code
claude .

# Or if using VS Code with Claude extension
code .
```

### Step 3: Analyze Existing Project

In Claude Code, run:

```bash
/analyze-existing full
```

This powerful command will:
- 🔍 **Detect your tech stack** (Next.js, React, Vue, etc.)
- 📁 **Map your project structure**
- 🎯 **Identify existing features**
- 📊 **Count components and complexity**
- 📝 **Generate initial documentation**

**Output created:**
```
.agent-os/
├── product/
│   ├── mission.md          # Project purpose (extracted)
│   ├── roadmap.md          # Phase 0 = what exists
│   ├── tech-stack.md       # Your dependencies
│   └── decisions.md        # Ready for ADRs
└── MIGRATION_GUIDE.md      # Custom for your project
```

### Step 4: Check for Existing Boilerplate

```bash
# Check if they have an older boilerplate version
/boilerplate-version
```

**If version detected (v1.0 - v3.5):**
```bash
# Upgrade to v4.0
/upgrade-boilerplate --dry-run  # See what will change
/upgrade-boilerplate             # Actually upgrade
```

**If no boilerplate detected:**
Continue to Step 5.

### Step 5: Choose Integration Method

#### Method A: Smart Integration (Recommended)

```bash
# See what will happen without making changes
/integrate-boilerplate --dry-run

# Review the report, then actually integrate
/integrate-boilerplate --mode=full
```

**What this does:**
- ✅ Creates backup of everything
- ✅ Never overwrites your files
- ✅ Adds `-project` suffix to conflicting commands
- ✅ Numbers your hooks to run first
- ✅ Creates `CLAUDE_BOILERPLATE.md` if you have `CLAUDE.md`

#### Method B: Selective Integration

```bash
/integrate-boilerplate --mode=selective
```

**Interactive menu appears:**
```
Select components to integrate (comma-separated):
1. Commands & Automation (.claude/)
2. Design System Enforcement
3. PRP System (one-pass implementation)
4. Agent OS Standards
5. Field Registry (security)
6. Git Hooks (.husky/)
7. Playwright Testing
8. Biome Linting
9. Component Templates
10. Documentation

Enter: 1,3,5,7  # Choose what you need
```

#### Method C: Sidecar Mode (Zero Conflicts)

```bash
/integrate-boilerplate --mode=sidecar
```

**Creates parallel installation:**
```
.claude/                    # Your existing (if any)
.claude-boilerplate/        # Our complete system
```

Access with `/bb [command]` prefix. Perfect for testing!

### Step 6: Install Dependencies

The integration will list any missing dependencies:

```bash
# Exit Claude Code temporarily
exit

# Install missing dependencies
pnpm add @supabase/supabase-js framer-motion lucide-react
pnpm add -D @biomejs/biome @playwright/test husky

# Return to Claude Code
claude .
```

### Step 7: Configure Project

```bash
# In Claude Code
/config set project.name "Your Project Name"
/config set repository.owner "your-github-username"
/config set repository.name "repository-name"

# Or edit directly
/edit .claude/project-config.json
```

### Step 8: Load and Verify

```bash
# Load the complete system
/sr

# Verify installation
/v4-status           # Check all systems
/chain list          # See available workflows
/help               # View all commands
```

## Integration Methods

### Full Integration (Default)
```bash
/integrate-boilerplate --mode=full
```
- **Best for:** Most projects
- **Result:** Complete boilerplate with intelligent conflict resolution
- **Time:** 5 minutes

### Selective Integration
```bash
/integrate-boilerplate --mode=selective
```
- **Best for:** Projects with existing Claude setups
- **Result:** Only chosen components
- **Time:** 3-10 minutes

### Sidecar Integration
```bash
/integrate-boilerplate --mode=sidecar
```
- **Best for:** Testing or very custom setups
- **Result:** Parallel installation, no conflicts
- **Time:** 2 minutes

### Manual Script Method
```bash
# Download integration script
curl -sSL https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/scripts/integrate-boilerplate-v2.sh -o integrate.sh
chmod +x integrate.sh

# Run integration
./integrate.sh --mode=full
```

## Handling Existing Boilerplate Versions

### Version Detection
```bash
/boilerplate-version
```

Shows:
- Current version (if any)
- Feature analysis
- Health score
- Upgrade availability

### Upgrade Paths

**From v1.0 (Original)**
```bash
/upgrade-boilerplate --from-version=1.0
```
- Backs up all customizations
- Installs v4.0 structure
- Restores custom commands with `-custom` suffix

**From v2.0 (PRD System)**
```bash
/upgrade-boilerplate --from-version=2.0
```
- Adds agents and hooks
- Updates commands
- Preserves PRD system

**From v3.0/3.5 (PRP System)**
```bash
/upgrade-boilerplate --from-version=3.0
```
- Adds orchestration
- Updates hook compliance
- Minor additions

**Auto-Detection**
```bash
/upgrade-boilerplate  # Detects version automatically
```

## What Gets Added vs Protected

### ✅ What Gets Added

**Core System:**
```
.claude/
├── commands/           # 150+ commands
├── agents/            # 31 AI agents
├── hooks/             # Automation
├── config/            # Settings
└── VERSION            # v4.0.0

.agent-os/             # Standards
field-registry/        # Security
PRPs/                 # Templates
templates/            # Components
```

**Configuration:**
- `CLAUDE_BOILERPLATE.md` (if you have CLAUDE.md)
- `biome.json` (linting)
- `playwright.config.ts` (testing)
- `.husky/` (git hooks)

### 🛡️ What's Protected (Never Touched)

**Your Code:**
```
app/                   # Application routes
components/            # Your components
lib/                   # Your libraries
pages/                 # Page routes
public/                # Static assets
prisma/                # Database
src/                   # Source code
```

**Your Config:**
```
package.json           # Dependencies
.env*                  # Environment vars
next.config.js         # Your config
tsconfig.json          # Your TS config
```

### 🔄 What Gets Merged Intelligently

**Commands:**
- Conflicts: Yours renamed to `[name]-project.md`
- You can use both versions

**Hooks:**
- Yours renumbered to 00-09 (run first)
- Ours numbered 10+ (run after)

**Documentation:**
- Your CLAUDE.md stays primary
- Ours added as CLAUDE_BOILERPLATE.md

## Post-Integration Setup

### 1. Commit Integration

```bash
# Review changes
git status
git diff --stat

# Commit
git add -A
git commit -m "feat: Integrate Claude Code Boilerplate v4.0.0"

# Push to your branch
git push origin integrate-boilerplate
```

### 2. Create PR

```bash
# Or use Claude command
/gh create-pr "Add Claude Code Boilerplate v4.0.0" "integrate-boilerplate"
```

### 3. Team Onboarding

```bash
# Generate team guide
/chain team-onboarding

# Creates:
# - TEAM_GUIDE.md
# - Quick reference card
# - Common patterns doc
```

### 4. Configure CI/CD

```bash
# Add to your CI pipeline
/generate-ci-config github-actions
/generate-ci-config gitlab-ci
```

## Common Scenarios

### Scenario: Next.js App Router Project

```bash
git clone https://github.com/user/nextjs-app.git
cd nextjs-app
claude .

/analyze-existing full
# Detects: Next.js 14, App Router, Tailwind

/integrate-boilerplate
# Adds commands, preserves app/ structure

/migrate-to-strict-design
# Converts to 4-size, 2-weight system
```

### Scenario: React SPA with Redux

```bash
git clone https://github.com/user/react-spa.git
cd react-spa
claude .

/analyze-existing full
# Detects: React 18, Redux, Material-UI

/integrate-boilerplate --mode=selective
# Choose: 1,3,5 (commands, PRP, security)
# Skip: 2 (design system - keep Material-UI)
```

### Scenario: Vue.js Project

```bash
git clone https://github.com/user/vue-app.git
cd vue-app
claude .

/analyze-existing full
# Detects: Vue 3, Vuex, Vuetify

/integrate-boilerplate --mode=sidecar
# Parallel installation for testing
# Access with /bb prefix
```

### Scenario: Monorepo

```bash
git clone https://github.com/user/monorepo.git
cd monorepo
claude .

/analyze-existing full
/config set project.type monorepo
/config set project.packages ["web", "api", "shared"]
/integrate-boilerplate
```

### Scenario: Project with Tests

```bash
git clone https://github.com/user/tested-app.git
cd tested-app
claude .

# Keep existing test framework
/config set testing.framework jest  # or vitest
/config set testing.runner "npm test"
/integrate-boilerplate
```

## Troubleshooting

### Issue: "Command not found: /integrate-boilerplate"

**Solution:**
```bash
# The command might be archived
/search integrate
# Or download manually
curl -sSL https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/.claude/commands/integrate-boilerplate.md -o .claude/commands/integrate-boilerplate.md
```

### Issue: "Conflicts detected"

**Solution:**
```bash
# Use dry-run to see conflicts
/integrate-boilerplate --dry-run

# Review .claude-integration/CONFLICT_REPORT.md
# Then proceed with integration (conflicts handled automatically)
```

### Issue: "Version mismatch"

**Solution:**
```bash
/boilerplate-version        # Check current
/upgrade-boilerplate        # Upgrade to v4.0
```

### Issue: "Git merge conflicts after integration"

**Solution:**
```bash
# Integration creates backups
ls .claude-integration/backup/

# Restore if needed
/integration-rollback

# Or manually
git reset --hard HEAD~1
```

### Issue: "Dependencies not installing"

**Solution:**
```bash
# Clear cache and reinstall
rm -rf node_modules pnpm-lock.yaml
pnpm install

# Or use npm/yarn
npm install
yarn install
```

## Rollback & Recovery

### Instant Rollback

```bash
# If something goes wrong
/integration-rollback

# Restores from automatic backup
# Returns to exact pre-integration state
```

### Manual Rollback

```bash
# Find backup
ls -la .claude-integration/backup/

# Restore specific backup
cp -r .claude-integration/backup/[timestamp]/* .

# Remove boilerplate files
rm -rf .claude .agent-os field-registry PRPs
rm -f CLAUDE_BOILERPLATE.md
```

### Git Rollback

```bash
# If you committed
git reset --hard HEAD~1

# If you pushed
git revert HEAD
git push
```

### Selective Removal

```bash
# Remove specific components
rm -rf .claude/agents      # Remove agents only
rm -rf field-registry      # Remove security only
rm -rf PRPs               # Remove PRP system only
```

## Best Practices

### 1. Always Branch First
```bash
git checkout -b integrate-boilerplate
```

### 2. Use Dry Run
```bash
/integrate-boilerplate --dry-run
```

### 3. Review Reports
```bash
# After integration
cat .claude-integration/INTEGRATION_COMPLETE.md
cat BOILERPLATE_INTEGRATION.md
```

### 4. Test Thoroughly
```bash
/v4-status              # System check
/test                   # Run tests
/vd                     # Validate design
```

### 5. Document Changes
```bash
# Update README
/update-readme-with-boilerplate

# Create changelog entry
/changelog add "Integrated Claude Code Boilerplate v4.0.0"
```

## Next Steps After Integration

1. **Learn the System**
   ```bash
   /help                    # See all commands
   /chain list             # View workflows
   /docs                   # Open documentation
   ```

2. **Start Building**
   ```bash
   /fw start new-feature   # Start feature
   /create-prp            # Create implementation guide
   /orch                  # Orchestrate agents
   ```

3. **Enable Automation**
   ```bash
   git config core.hooksPath .husky
   pnpm run prepare       # Install git hooks
   ```

4. **Share with Team**
   ```bash
   /generate-team-guide
   /create-onboarding-video-script
   ```

## Support & Resources

### Documentation
- [SYSTEM_WORKFLOWS.md](./SYSTEM_WORKFLOWS.md) - Complete workflows
- [GETTING_STARTED.md](./GETTING_STARTED.md) - New projects
- [Integration Command](.claude/commands/integrate-boilerplate.md) - Command details

### Getting Help
- Check `/help` for command list
- Run `/docs search [topic]` for documentation
- Use `/support` for common issues

### Version Info
- **Current Version**: 4.0.0
- **Released**: January 2025
- **Check Updates**: `/boilerplate-version`

---

*Last Updated: January 2025 | Version 4.0.0*
