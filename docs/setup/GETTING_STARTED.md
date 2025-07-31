# Getting Started with Claude Code Boilerplate v4.0.0

> The comprehensive AI-assisted development system with 31 specialized agents, automated workflows, and production-ready patterns.

## 🚀 Quick Start (5 minutes)

For those who want to dive in immediately:

```bash
# Clone and setup
git clone https://github.com/bearingfruitco/claude-code-boilerplate.git my-awesome-app
cd my-awesome-app
rm -rf .git

# Quick setup
chmod +x scripts/quick-setup.sh
./scripts/quick-setup.sh

# This will:
# ✅ Create YOUR GitHub repository
# ✅ Update all configurations
# ✅ Guide you through GitHub Apps
# ✅ Set up PRP system
# ✅ Initialize Git hooks
```

## 📋 Prerequisites

- **Claude Code** installed (`npm install -g @anthropic-ai/claude-code`)
- **Node.js 22+** and **pnpm** (or bun)
- **GitHub account** with CLI configured
- **Git** configured with your credentials

## 🔧 Step-by-Step Setup

### Step 1: Clone and Initialize

```bash
# Clone the boilerplate
git clone https://github.com/bearingfruitco/claude-code-boilerplate.git my-awesome-app
cd my-awesome-app

# Remove boilerplate Git history
rm -rf .git
git init

# Run automated setup
chmod +x scripts/quick-setup.sh
./scripts/quick-setup.sh
```

The setup script will:
1. Create YOUR GitHub repository (not the boilerplate)
2. Update all configuration files with your details
3. Guide you through GitHub Apps installation
4. Set up the PRP (Product Requirement Prompts) system
5. Configure Git hooks for quality enforcement

### Step 2: Install GitHub Apps

**CRITICAL**: Install these on YOUR repository, not the boilerplate!

#### CodeRabbit (AI Code Reviews)
1. Go to [github.com/marketplace/coderabbit](https://github.com/marketplace/coderabbit)
2. Choose plan (Free for individuals, Pro for teams)
3. Select "Only select repositories" → Choose YOUR repo
4. Complete installation

#### Claude Code GitHub Integration
1. Go to [github.com/apps/claude](https://github.com/apps/claude)
2. Click "Install"
3. Select "Only select repositories" → Choose YOUR repo
4. Grant permissions (code, issues, PRs)

### Step 3: Environment Configuration

```bash
# Copy environment template
cp .env.example .env.local

# Edit with your values
# Required:
# - DATABASE_URL (Supabase)
# - NEXT_PUBLIC_SUPABASE_URL
# - NEXT_PUBLIC_SUPABASE_ANON_KEY

# Optional but recommended:
# - Analytics (Rudderstack)
# - Error tracking (Sentry)
```

### Step 4: Install Dependencies & Initialize

```bash
# Install dependencies
pnpm install

# Set up Git hooks (Husky)
pnpm prepare

# Initialize database (if using Supabase)
pnpm db:push

# Start Claude Code
claude .
```

### Step 5: Project Initialization in Claude Code

Run these commands in Claude Code:

```bash
# 1. System initialization
/init

# 2. Define YOUR project (not boilerplate)
/init-project

# Answer questions about:
# - What you're building
# - Target users
# - Core problem
# - MVP scope
# - Tech preferences

# 3. Generate GitHub issues for your roadmap
/gi PROJECT

# This creates issues in YOUR repo based on your project definition
```

## 🎯 Your First Feature

Let's build your first feature using the v4.0.0 workflow:

### 1. Start from a GitHub Issue

```bash
# Pick an issue from your generated roadmap
/fw start 1  # Start working on issue #1
```

### 2. Choose Your Approach

#### Option A: PRP Workflow (Recommended for Clear Features)
```bash
# Generate comprehensive implementation guide
/create-prp user-authentication

# This creates a PRP with:
# - Complete implementation blueprint
# - Exact code patterns from your codebase
# - 4-level validation loops
# - Known gotchas and warnings
```

#### Option B: PRD → Architecture → PRP (For Complex Features)
```bash
# Start with requirements
/create-prd user-dashboard

# Generate full architecture
/chain architecture-design

# This creates:
# - System design documents
# - Database schemas
# - API specifications
# - Multiple PRPs for each component
```

### 3. Implementation with Validation

```bash
# Level 1: Syntax & Standards (continuous)
/vd                    # Design system check
/validate-async        # Async pattern check

# Level 2: Component Testing (after each component)
/tr components         # Run component tests

# Level 3: Integration Testing (after connecting pieces)
/btf                   # Browser test flow
/test:e2e              # End-to-end tests

# Level 4: Production Readiness (before PR)
/grade                 # Alignment scoring
/pp                    # Pre-PR validation
```

### 4. Complete the Feature

```bash
# Final validation
/sv check              # Stage validation
/fw complete           # Create PR with full context
```

## 📚 Understanding the System

### Core Components

1. **116+ Custom Commands** - Streamlined workflows with aliases
2. **31 Specialized Agents** - From frontend to security experts
3. **4-Level Validation** - Quality gates at each phase
4. **Smart Chains** - Automated multi-step workflows
5. **Native Sub-Agents** - Task delegation with separate contexts
6. **Git Pre-commit Hooks** - Final safety net before commits

### The Modern Development Flow

```
GitHub Issue → PRP Generation → Implementation → 4-Level Validation → PR
     ↓              ↓                  ↓                ↓              ↓
  Context      One-pass guide    AI assists      Quality gates    Clean code
```

### Key Innovations

- **Zero Context Loss**: Everything persists between sessions
- **Design System Enforcement**: 4 sizes, 2 weights, 4px grid
- **Security-First**: PII protection, field encryption built-in
- **Async Event System**: Non-blocking analytics and tracking
- **Visual Debugging**: Ctrl+V to paste screenshots for analysis

## 🔄 Daily Workflow

### Morning Routine
```bash
# Resume with full context
/sr

# Check for triggered chains
/chain check

# Review open work
/bt list               # Open bugs
/fw status             # Active features
/todo                  # Task list
```

### During Development
```bash
# Create components with validation
/cc Button             # Checks existence first

# Visual debugging
Ctrl+V                 # Paste screenshot
"Fix alignment issue"  # Describe problem

# Run tests continuously
/tr --watch            # Test runner in watch mode

# Check dependencies before modifying
/deps check Button     # See what uses this component
```

### Before Committing
```bash
# Validate everything
/vd                    # Design compliance
/validate-async        # Async patterns
/tr                    # Run tests

# Git commit (hooks run automatically)
git add .
git commit -m "feat: add user dashboard"

# Pre-commit hooks will:
# - Validate design system
# - Check TypeScript
# - Run affected tests
# - Detect console.logs
# - Validate PRPs (if active)
```

## 🎭 Working with Agents

The system includes 31 specialized agents. Here are key ones:

### Technology Specialists (v4.0.0)
- `supabase-specialist` - Database and RLS expert
- `playwright-specialist` - Browser automation
- `analytics-engineer` - Tracking implementation
- `platform-deployment` - Vercel optimization

### Core Team
- `frontend` - UI/UX implementation
- `backend` - API and server logic
- `security` - Vulnerability analysis
- `qa` - Testing strategies

### Using Agents
```bash
# Spawn specific agent
/spawn security

# Orchestrate multiple agents
/orch user-authentication

# Let system choose
/ut "How should I handle auth?"  # UltraThink with auto-agent selection
```

## 🚨 Common Issues & Solutions

### Issue: Commands reference boilerplate repo
**Fix**: Update `.claude/project-config.json` with YOUR repository details

### Issue: Design violations when committing
**Fix**: Run `/vd --fix` to auto-fix common issues

### Issue: "Component already exists" errors
**Fix**: Use `/exists ComponentName` before creating

### Issue: Slow async operations
**Fix**: Run `/validate-async` to find sequential awaits

### Issue: Context getting too large
**Fix**: Use `/compress` to optimize context

## 📖 Next Steps

1. **Explore Commands**: Run `/help` to see context-aware suggestions
2. **Read Workflows**: Check [SYSTEM_WORKFLOWS.md](./SYSTEM_WORKFLOWS.md)
3. **Try Chains**: Run `/chain list` to see automated workflows
4. **Join Community**: [Discord/Slack link if applicable]

## 🎯 Success Metrics

This system enables:
- **70% faster** feature development
- **90% fewer** design inconsistencies  
- **Zero** context loss between sessions
- **95% bug detection** before commit
- **One-pass** implementation success

---

**Remember**: The boilerplate is a template. Once cloned, everything should reference YOUR project, not the boilerplate repository.

**Version**: 4.0.0 - "Automation & Intelligence"  
**Support**: [Your support channels]  
**License**: [Your license]
