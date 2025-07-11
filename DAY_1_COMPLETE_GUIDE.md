# 🚀 Day 1 Complete Setup Guide - Zero to Production-Ready

## What This Guide Gives You
By the end of this guide, you'll have:
- ✅ Complete project setup with Claude Code
- ✅ PRD-driven development workflow
- ✅ Task-based feature building
- ✅ Auto-updating documentation
- ✅ Browser testing with Playwright
- ✅ All automation working

## Prerequisites
```bash
# Verify you have these installed:
claude-code --version
git --version
gh --version
node --version  # Need v22+
pnpm --version  # Need v9+
python3 --version
bun --version   # Need v1.0+

# If missing any:
# Claude Code: Download from Anthropic
# Git: brew install git
# GitHub CLI: brew install gh
# Node: brew install node@22
# pnpm: npm install -g pnpm@9
# Python: brew install python@3
# Bun: curl -fsSL https://bun.sh/install | bash
```

## Step 1: Project Creation (5 minutes)

```bash
# Create and setup project
mkdir my-awesome-project && cd my-awesome-project

# Copy boilerplate
cp -r /Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate/* .
cp -r /Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate/.claude .

# Initialize git
git init && git add . && git commit -m "Initial boilerplate"

# Create GitHub repo
gh repo create my-awesome-project --private
git push -u origin main
```

## Step 2: Create Your Documentation Structure (10 minutes)

### Create PRD (Product Requirements Document)
```bash
mkdir -p docs/project/features

cat > docs/project/prd.md << 'EOF'
# [Project Name] - Product Requirements Document

## Executive Summary
[One paragraph: What is this and why does it matter?]

## Problem Statement
- What problem are we solving?
- Who experiences this problem?
- What's the impact of not solving it?

## Target Users
- Primary: [Specific user type]
- Secondary: [Other users]

## Core Features (MVP)
1. **Feature Name**
   - What it does
   - Why it's essential
   - Success criteria

## User Stories
- As a [user], I want to [action] so that [benefit]
- As a [user], I want to [action] so that [benefit]

## Technical Requirements
- Performance: [Page load < 3s]
- Security: [Requirements]
- Accessibility: [WCAG 2.1 AA]
- Mobile: [Responsive, touch-friendly]

## Success Metrics
- [Metric 1]: Target value
- [Metric 2]: Target value

## Out of Scope (v1)
- [What we're NOT building yet]
EOF
```

### Create Business Logic Document
```bash
cat > docs/project/business-logic.md << 'EOF'
# Business Logic & Rules

## Purpose
This document defines HOW the system works - all rules, validations, and workflows that must be enforced in code.

## Core Business Rules

### User Management
1. **Registration Rules**
   - Email must be unique
   - Password: min 8 chars, 1 upper, 1 lower, 1 number
   - Email verification required

2. **Authentication**
   - Session timeout: 30 days
   - Max login attempts: 5
   - 2FA optional but recommended

### Data Validation Rules
| Field | Rules |
|-------|-------|
| Email | Valid format, max 255 chars |
| Name | Required, 2-100 chars |
| Phone | Optional, valid format |

### Business Workflows

#### User Onboarding Flow
1. User submits registration
2. System sends verification email
3. User clicks verification link (valid 24h)
4. System activates account
5. User redirected to welcome screen

### API Business Rules
- Rate limiting: 100 req/min per user
- All timestamps in UTC
- Soft delete only (no hard deletes)
- Audit log all changes

### Security Rules
- PII must be encrypted at rest
- No sensitive data in logs
- HTTPS required for all endpoints
EOF
```

### Evidence-Based Development (NEW)
```bash
# The system now enforces evidence-based language
# Never say: "best", "optimal", "faster" without proof
# Always say: "testing shows", "metrics indicate"
# Hook 08-evidence-language.py enforces this automatically
```

### Auto-Persona Selection (NEW)
```bash
# The system automatically suggests the right persona based on:
# - File type (e.g., *.tsx → frontend persona)
# - Keywords (e.g., "security audit" → security persona)
# Hook 09-auto-persona.py handles this
```

### Update CLAUDE.md
```bash
cat > CLAUDE.md << 'EOF'
# Claude Code Instructions - [Project Name]

## 📍 Project Documentation Locations
- **PRD**: `docs/project/prd.md` - WHAT we're building
- **Business Logic**: `docs/project/business-logic.md` - HOW it works
- **Design System**: `docs/design/design-system.md` - HOW it looks
- **Features**: `docs/project/features/` - Feature-specific docs

## 🤖 Automated Features
- **Context Updates**: This project auto-updates documentation nightly
- **Browser Testing**: Playwright MCP enabled for E2E testing
- **Task Management**: PRD-driven task decomposition

## 🎯 Development Workflow
1. Start with `/sr` (smart resume) every session
2. For new features: `/project:create-prd` → `/project:generate-tasks` → `/project:process-tasks`
3. Use `/project:auto-update-context` to refresh documentation
4. Run `/project:browser-test-flow` for E2E testing

## 🚀 Available Commands
- `/init` - One-time setup (already done if you see this)
- `/sr` - Smart resume (use this daily)
- `/help` - See all commands
- Task commands: `/project:create-prd`, `/project:generate-tasks`, `/project:process-tasks`
- Testing: `/project:browser-test-flow`, `/project:verify-task`
- Maintenance: `/project:auto-update-context`
- **NEW**: `/compress-context` or `/compress` - Compress context when approaching token limits
- **AUTO**: Persona switching based on file type and keywords
- **AUTO**: Evidence-based language enforcement

## 🏗️ Design System Rules (MANDATORY)

### Typography - STRICT ENFORCEMENT
You MUST ONLY use these font sizes and weights:
- text-size-1: 32px (mobile: 28px) - Major headings only
- text-size-2: 24px (mobile: 20px) - Section headers
- text-size-3: 16px - ALL body text, buttons, inputs
- text-size-4: 12px - Small labels, captions

Font weights:
- font-regular: 400 - For ALL body text
- font-semibold: 600 - For ALL headings and buttons

❌ NEVER use: text-sm, text-lg, text-xl, text-2xl, font-bold, font-medium
✅ ALWAYS use: text-size-[1-4], font-regular, font-semibold

### Spacing - 4px Grid ONLY
ALL spacing must be divisible by 4:
- ✅ Valid: p-1(4px), p-2(8px), p-3(12px), p-4(16px), p-6(24px), p-8(32px)
- ❌ Invalid: p-5, p-7, p-10, m-5, gap-5, space-y-5

### Color Distribution
Every screen must follow 60/30/10 rule:
- 60%: Neutral backgrounds (white, gray-50)
- 30%: Text and borders (gray-700, gray-200)
- 10%: Primary actions (blue-600, red-600 for errors)

### Mobile Requirements
- Minimum touch targets: 44px (use h-11 or h-12)
- Minimum body text: 16px (text-size-3)
- Maximum content width: max-w-md for mobile-first
EOF
```

## Step 3: Install Dependencies & Tools (5 minutes)

```bash
# Install Bun (if not already installed)
curl -fsSL https://bun.sh/install | bash
# Or with Homebrew:
brew install oven-sh/bun/bun

# Verify Bun is installed
bun --version

# Install project dependencies
pnpm install

# Biome is installed as a dev dependency, verify it works
pnpm biome --version

# Install Playwright MCP globally
npm install -g @modelcontextprotocol/server-playwright

# Install Python dependencies for automation
pip3 install gitpython

# Make scripts executable
chmod +x .claude/scripts/*.sh
chmod +x .claude/scripts/*.py
chmod +x .claude/hooks/pre-tool-use/*.py
chmod +x .claude/hooks/post-tool-use/*.py

# Set up Claude Code hooks for observability
./setup-hooks.sh
```

## Step 4: Initialize Claude Code (2 minutes)

```bash
# Start Claude Code
claude-code .

# Run initialization (ONCE only)
/init

# Set up Playwright MCP
/project:setup-playwright-mcp

# Enable auto-updates
/project:auto-update-context
```

## Step 5: Your First Feature - PRD to Production (20 minutes)

### 5.1 Create GitHub Issue
```bash
gh issue create --title "Feature: User Authentication" \
  --body "Implement user registration and login as defined in PRD"
# Note the issue number (e.g., #1)
```

### 5.2 Generate PRD for Feature
```bash
# In Claude Code
/project:create-prd user-authentication

# This creates: docs/project/features/user-authentication-PRD.md
```

### 5.3 Generate Task List
```bash
/project:generate-tasks user-authentication

# This creates: docs/project/features/user-authentication-tasks.md
# With ~15-20 small, verifiable tasks
```

### 5.4 Start Feature Development
```bash
/fw start 1  # Using issue number

# This:
# - Creates feature branch
# - Sets up worktree
# - Loads PRD and tasks
# - Prepares context
```

### 5.5 Process Tasks One by One
```bash
/project:process-tasks user-authentication

# Claude will:
# - Show task 1.1
# - Implement it
# - Wait for your approval
# - Move to next task
# 
# You just review and say "yes" or provide feedback
```

### 5.6 Test with Browser Automation
```bash
/project:browser-test-flow user-registration

# This:
# - Opens browser
# - Tests the flow
# - Takes screenshots
# - Reports results
```

### 5.7 Complete Feature
```bash
# After all tasks done
/fw complete 1

# This:
# - Runs all validations
# - Creates PR
# - Updates documentation
```

## Step 6: Enable Nightly Updates (2 minutes)

```bash
# Set up cron job for nightly updates
crontab -e

# Add this line:
0 2 * * * cd /path/to/your/project && python3 .claude/scripts/nightly-update.py

# Or use GitHub Actions (see .github/workflows/nightly-update.yml)
```

## Daily Workflow Summary

### Morning (2 minutes)
```bash
claude-code .
/sr  # Smart resume - shows everything you need
```

### During Development
```bash
# For new features
/project:create-prd feature-name
/project:generate-tasks feature-name
/project:process-tasks feature-name

# For testing
/project:browser-test-flow feature-name
/project:verify-task

# Keep context fresh
/project:auto-update-context
```

### Before PR
```bash
/pp  # Pre-PR checks
/fw complete [issue#]
```

### End of Day
```bash
/checkpoint create "end of day"
# Just close - hooks handle everything else
```

## What Makes This Special

1. **PRD-Driven**: Start with clear requirements
2. **Task Decomposition**: AI handles one small task at a time
3. **Auto-Documentation**: Context updates itself
4. **Browser Testing**: See your app actually work
5. **Zero Context Loss**: Everything is tracked and saved
6. **Evidence-Based Development (NEW)**: Claims require proof - "testing shows 40% faster" not "this is better"
7. **Auto-Persona Selection (NEW)**: Right expert for the right task - frontend specialist for UI, security analyst for audits
8. **Token Optimization (NEW)**: Compress context command (`/compress`) when approaching limits

## Troubleshooting

### "Command not found"
```bash
/help  # See all commands
ls .claude/commands/  # Verify files exist
```

### "Context seems stale"
```bash
/project:auto-update-context  # Refresh documentation
/sr full  # Full context restoration
```

### "Browser tests failing"
```bash
# Check Playwright MCP is installed
npm list -g @modelcontextprotocol/server-playwright

# Reinstall if needed
npm install -g @modelcontextprotocol/server-playwright
```

## Next Steps

1. Customize PRD template for your domain
2. Add project-specific commands
3. Set up team notifications
4. Configure CI/CD integration

You're now ready to build with AI-assisted development that's structured, verifiable, and maintains itself!