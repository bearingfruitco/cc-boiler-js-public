# Next.js 15 Boilerplate with Claude Code

This is a production-ready boilerplate for Next.js 15 projects with TypeScript, Tailwind CSS, Supabase, advanced Claude Code automation, PRP methodology for one-pass implementation success, and intelligent branch awareness.

## 🚀 Quick Start

### New Project (Updated with Branch Awareness)
```bash
# Clone boilerplate
git clone https://github.com/bearingfruitco/claude-code-boilerplate.git my-project
cd my-project

# Run quick setup (handles repo config + GitHub Apps)
chmod +x scripts/quick-setup.sh
./scripts/quick-setup.sh

# Setup PRP system
chmod +x setup-prp.sh
./setup-prp.sh

# Setup Branch Awareness (NEW in v2.6.0)
chmod +x setup-branch-awareness-integrated.sh
./setup-branch-awareness-integrated.sh
```

### Existing Project
```bash
# Quick add (minimal - just commands)
curl -sSL https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/scripts/add-to-existing.sh | bash -s minimal

# Or full integration with AI reviews
curl -sSL https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/scripts/add-to-existing.sh | bash -s full

# Then run setup: ./scripts/quick-setup.sh
# And PRP setup: ./setup-prp.sh
```

### 📖 Essential Guides
- **[MASTER_WORKFLOW_GUIDE.md](MASTER_WORKFLOW_GUIDE.md)** - Complete workflow reference (START HERE!)
- **[docs/setup/DAY_1_COMPLETE_GUIDE.md](docs/setup/DAY_1_COMPLETE_GUIDE.md)** - Detailed setup walkthrough

## 🎯 What You Get

### Instant Productivity
- **113+ Custom Commands** - Everything from `/sr` (smart resume) to `/ut` (ultra-think)
- **Task Ledger** 📋 - Persistent task tracking across all features (NEW!)
- **UltraThink Mode** 🤯 - 32k+ token deep thinking with parallel agents
- **Visual Planning** 📸 - Ray Fernando-style screenshot-based iteration
- **PRP Methodology** 🚀 - One-pass implementation with validation loops (v2.6.0)
- **Zero Context Loss** - Auto-saves work state to GitHub gists (not commits!)
- **PRD-Driven Development** - Start with requirements, get working code
- **Multi-Agent System** - 9 specialized personas work in parallel
- **Async Event System** ⚡ - Fire-and-forget for analytics, never block users
- **Smart Issue Creation** 🎯 - Capture Claude responses directly to GitHub with duplicate detection
- **Dependency Tracking** 📦 - Know what components depend on each other
- **Git Pre-Commit Hooks** 🛡️ - Catch issues before commits (NEW in v2.7.1)
- **Native Claude Code Features** 🎮 - Visual debugging, non-interactive mode

### PRP System (NEW in v2.6.0)
- **Product Requirement Prompts** - Everything needed for one-pass success
- **Automated Validation** - 4-level quality gates (syntax → production)
- **Deep Research** - Multi-agent research for comprehensive context
- **Pattern Extraction** - Learn from successful implementations
- **CI/CD Ready** - Optional automation with prp-runner.ts

### Enforced Quality
- **Design System** - Only 4 font sizes, 2 weights, 4px grid (enforced by hooks)
- **4-Level Validation** - Syntax → Components → Integration → Production (v2.6.0)
- **Security-First** - PII detection, field encryption, audit logging
- **Test Everything** - "Actually Works" protocol blocks untested code
- **Clean Architecture** - Consistent patterns across all features
- **Async Patterns** ⚡ - Required loading states, parallel operations, timeout protection
- **Git Pre-Commit Checks** 🆕 - Design system, TypeScript, tests validated before commit

### Team Collaboration
- **Perfect Handoffs** - Context transfers seamlessly between developers
- **GitHub Integration** - Issues, PRs, gists all connected
- **Real-Time Review** - CodeRabbit catches issues as you type
- **Conflict Prevention** - Know who's editing what in real-time
- **Knowledge Sharing** - Patterns discovered by one help all

### 🎯 Latest Enhancement: Git Pre-Commit Hooks (v2.7.1)
- **Complements MCP Hooks** - Catches issues at commit time
- **Quick Validation** - Only checks staged files for speed
- **Design System Check** - Ensures compliance before commit
- **TypeScript Validation** - Catches type errors early
- **Test Runner** - Runs tests for changed components
- **Debug Code Detection** - Warns about console.logs
- See [Git Hooks Setup](#git-pre-commit-hooks) for details

### 🎮 Native Claude Code Features (v2.7.1)
- **Visual Debugging** - Ctrl+V to paste screenshots for instant analysis
- **Non-Interactive Mode** - `claude --non-interactive` for CI/CD automation
- **Session History** - Resume with branch context
- **Undo Support** - Ctrl+- to undo typing
- See [docs/workflow/CLAUDE_CODE_NATIVE_FEATURES.md](docs/workflow/CLAUDE_CODE_NATIVE_FEATURES.md)

### ⚡ Previous Enhancements (v2.3.6)
- **Async Event System** - Fire-and-forget pattern for tracking/analytics
- **Form Event Tracking** - Built-in `useLeadFormEvents` hook for automatic tracking
- **Parallel Detection** - Warns about sequential awaits that could run in parallel
- **Required Loading States** - Every async operation must show user feedback
- **Rudderstack Bridge** - Events automatically convert to `rudderanalytics.track()` calls
- **Timeout Protection** - All external calls have 5s timeout by default

### 🌟 Grove-Inspired Enhancements
- **PRD Clarity Linter** - Catches ambiguous language in requirements
- **Specification Patterns** - Extract and reuse successful implementations (`/specs`)
- **Test Generation from PRDs** - Acceptance criteria → executable tests (`/prd-tests`)
- **Implementation Grading** - Score code alignment with PRD (`/grade`)

## 📊 The Complete Workflow

### Traditional PRD Flow
```
PROJECT IDEA → PROJECT PRD → GITHUB ISSUES → FEATURE PRDS → TASKS → CODE → PR → DEPLOY
     ↓              ↓              ↓              ↓           ↓       ↓      ↓      ↓
/init-project  /gi PROJECT    /fw start #   /prd feature  /gt,/pt  Auto  Complete  Ship
```

### New PRP Flow (Recommended)
```
GITHUB ISSUE → CREATE PRP → VALIDATE L1 → IMPLEMENT → VALIDATE L2-4 → PR → DEPLOY
      ↓            ↓            ↓            ↓            ↓          ↓      ↓
/fw start #   /create-prp   /prp-execute   Code    /prp-execute  /fw    Ship
```

## 🔑 Essential Commands

```bash
# Every Day
/sr                # Smart Resume - start here always!
/cp load frontend  # Load context profile
/bt list           # Check open bugs
/help              # Context-aware help

# PRP Development (NEW!)
/prp feature       # Create Product Requirement Prompt
/prp-execute name  # Run validation loops
/prp-exec --fix    # Auto-fix issues
/prp-exec --level 1 # Run specific validation level

# Traditional Development  
/fw start 1        # Start working on issue #1
/prd feature       # Create Product Requirements
/gt feature        # Generate tasks
/pt feature        # Process tasks
/sv check 1        # Validate stage completion
/fw complete 1     # Create PR

# Quality & Testing
/vd                # Validate design
/btf feature       # Browser test
/sc                # Security check
/grade             # Check PRD alignment

# State Management
/checkpoint        # Manual save
/compress          # Reduce token usage

# Native Claude Features (NEW!)
Ctrl+V             # Paste screenshot for visual debugging
Ctrl+-             # Undo typing
```

See **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** for all commands.

## 📁 What's Inside

```
├── .claude/           # 🧠 The brain - commands, hooks, automation
├── .husky/            # 🛡️ Git pre-commit hooks (NEW!)
├── PRPs/              # 🎯 Product Requirement Prompts (NEW!)
│   ├── templates/     # PRP templates
│   ├── ai_docs/      # AI-optimized documentation
│   ├── scripts/      # Validation runner
│   ├── active/       # Current PRPs
│   └── completed/    # Reference PRPs
├── scripts/           # 🔧 Setup and utilities
│   ├── check-design-staged.js    # Pre-commit design check
│   ├── test-staged-files.js      # Pre-commit test runner
│   └── typecheck-staged.js       # Pre-commit TypeScript
├── CLAUDE.md          # 📜 AI instructions (don't delete!)
├── QUICK_REFERENCE.md # 🎯 Daily command cheat sheet
├── docs/              # 📚 All documentation
│   ├── setup/        # Getting started guides
│   ├── workflow/     # Daily usage patterns
│   ├── technical/    # System architecture
│   └── claude/       # AI-specific docs
├── field-registry/    # 🔒 Security definitions
└── [your code]       # 💻 Your application
```

## 🏗️ Technical Stack

- **Framework**: Next.js 15 (App Router + Turbopack)
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS + Radix UI primitives
- **Database**: Supabase (Auth + DB) + Drizzle ORM
- **Auth**: Auth.js v5 (next-auth)
- **State**: Zustand + TanStack Query
- **Testing**: Vitest + Playwright + MSW
- **Date Handling**: date-fns v4 with timezone support
- **Build Tools**: Turbopack + SWC + Biome
- **Security**: Field-level encryption, audit logging, PII protection
- **Git Hooks**: Husky for pre-commit validation

## 💡 Key Features

### 1. **PRP-Driven Development** (NEW!)
```bash
/prp user-auth        # Generate comprehensive PRP
/prp-execute user-auth # Validate implementation
# Implement following blueprint...
/prp-execute user-auth # Final validation
```

### 2. **PRD-Driven Development**
```bash
/prd user-auth     # Generate requirements
/gt user-auth      # Break into 5-15 min tasks
/pt user-auth      # Work through systematically
```

### 3. **Design System Enforcement**
```typescript
// ❌ BLOCKED by hooks:
<p className="text-sm font-bold">

// ✅ ALLOWED:
<p className="text-size-3 font-semibold">

// Also enforced at git commit time!
```

### 4. **Security-First Forms**
```bash
/ctf ContactForm   # Creates secure form with:
                   # - PII detection
                   # - Field encryption
                   # - Audit logging
                   # - TCPA compliance
```

### 5. **Multi-Agent Orchestration**
```bash
/orch feature      # Assigns to specialized agents:
                   # - Frontend: UI/UX
                   # - Backend: APIs
                   # - Security: Compliance
                   # - QA: Testing
```

### 6. **Git Pre-Commit Hooks** (NEW!)
```bash
git commit -m "feat: add user profile"
# Automatically runs:
# ✓ Design system validation (staged files)
# ✓ TypeScript check (staged files)
# ✓ Test runner (affected tests)
# ✓ Console.log detection
# ✓ PRP validation (if active)
```

## 📈 Results

Teams using this boilerplate report:
- **70% faster** feature development
- **90% fewer** design inconsistencies  
- **Zero** context loss between sessions
- **95% less** documentation time
- **One-pass implementation** success with PRPs
- **50% fewer** broken commits with pre-commit hooks

## 🚦 Getting Started

### Option 1: New Project (5 minutes)
1. Clone repo
2. Run setup scripts
3. Start Claude Code
4. Run `/init`
5. Define project with `/init-project`

### Option 2: Existing Project (10 minutes)
1. Copy `.claude/`, `.husky/`, and `PRPs/` directories
2. Add CLAUDE.md and QUICK_REFERENCE.md
3. Run `/init` and `./setup-prp.sh`
4. Install husky: `npm install husky --save-dev`
5. Start using commands

## 📚 Documentation

- **Essential Reading**
  - 🚀 **[MASTER WORKFLOW GUIDE](MASTER_WORKFLOW_GUIDE.md)** - One document with everything!
  - [Quick Reference](QUICK_REFERENCE.md) - Command cheat sheet
  - [Native Features Guide](docs/workflow/CLAUDE_CODE_NATIVE_FEATURES.md) - Ctrl+V and more (NEW!)
  
- **Setup**
  - [Day 1 Complete Guide](docs/setup/DAY_1_COMPLETE_GUIDE.md)
  - [Quick Start - New Project](docs/setup/QUICK_START_NEW_PROJECT.md)
  - [Add to Existing Project](docs/setup/ADD_TO_EXISTING_PROJECT.md)
  
- **Daily Use**
  - [PRP Workflow Guide](docs/workflow/PRP_WORKFLOW_GUIDE.md) 🆕
  - [Daily Workflow](docs/workflow/DAILY_WORKFLOW.md)
  - [TDD Workflow](docs/workflow/TDD_WORKFLOW_GUIDE.md)
  
- **Deep Dives**
  - [System Overview](docs/SYSTEM_OVERVIEW.md)
  - [PRP Methodology](PRPs/README.md) 🆕
  - [Command List](docs/claude/CLAUDE_CODE_GUIDE.md)
  - [Security Guide](docs/SECURITY_GUIDE.md)

- **Release Information**
  - [Current Release (v2.7.1)](RELEASES.md)
  - [All Release Notes](docs/releases/)
  - [Changelog](CHANGELOG.md)

## 🎓 Philosophy

**"Vibe Coding"**: You define WHAT to build (strategy), the system handles HOW (implementation).

- One-pass implementation > Multiple iterations
- Complete context > Partial information
- Automated validation > Manual review
- Observable systems > Black boxes

## 🤝 Contributing

This boilerplate evolves with usage. Share your:
- Custom commands
- PRP templates
- Workflow improvements  
- Bug fixes
- Success stories

---

Built by developers tired of:
- 🚫 Multiple implementation attempts
- 🚫 Losing context between sessions
- 🚫 Inconsistent implementations
- 🚫 "It should work" syndrome
- 🚫 Manual documentation
- 🚫 Broken commits

Ready to build something amazing? Start with `/init-project` and `/prp` 🚀

## 🔒 Security

This boilerplate contains no secrets or API keys. All sensitive values in configuration files are placeholders.

**Important:**
- Copy `.env.example` to `.env.local` and add your real values
- Update `.mcp.json` with your actual API keys
- Never commit `.env.local` or any file with real secrets
- Keep all API keys and tokens in environment variables

**MCP Configuration:**
The `.mcp.json` file contains placeholder values for various services. Replace these before use:
- `YOUR_BRAVE_API_KEY` - For web search functionality
- `YOUR_GITHUB_PAT` - For GitHub integration
- `YOUR_SUPABASE_SERVICE_ROLE_KEY` - For database access
- And other service-specific keys

See [SETUP_SECURITY.md](docs/setup/SETUP_SECURITY.md) for detailed security setup instructions.

## 🛡️ Git Pre-Commit Hooks

The boilerplate includes Git pre-commit hooks that complement the MCP hooks:

**MCP Hooks**: Catch issues as Claude writes code (real-time)
**Git Hooks**: Catch issues before commit (batch validation)

Pre-commit checks:
1. **Design System**: Validates only staged files
2. **TypeScript**: Checks only staged files
3. **Tests**: Runs tests for changed components
4. **Debug Code**: Warns about console.logs
5. **PRP Validation**: If active PRPs exist

To skip temporarily (emergency only):
```bash
git commit --no-verify -m "Emergency fix"
```

See scripts in `.husky/` and `scripts/` for implementation details.
