# Next.js 15 Boilerplate with Claude Code

This is a production-ready boilerplate for Next.js 15 projects with TypeScript, Tailwind CSS, Supabase, and advanced Claude Code automation.

## 🚀 Quick Start

### New Project
```bash
git clone https://github.com/bearingfruitco/claude-code-boilerplate.git my-project
cd my-project
rm -rf .git && git init
# Follow: docs/setup/QUICK_START_NEW_PROJECT.md
```

### Existing Project
```bash
# Quick add (minimal - just commit control)
curl -sSL https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/boilerplate/scripts/add-to-existing.sh | bash -s minimal

# Or follow the full guide:
# docs/setup/ADD_TO_EXISTING_PROJECT.md
```

### Complete Setup Guide
For detailed walkthrough: **[docs/setup/DAY_1_COMPLETE_GUIDE.md](docs/setup/DAY_1_COMPLETE_GUIDE.md)**

## 🎯 What You Get

### Instant Productivity
- **90+ Custom Commands** - Everything from `/sr` (smart resume) to `/orch` (orchestrate agents)
- **Zero Context Loss** - Auto-saves work state to GitHub gists (not commits!)
- **PRD-Driven Development** - Start with requirements, get working code
- **Multi-Agent System** - 9 specialized personas work in parallel

### Enforced Quality
- **Design System** - Only 4 font sizes, 2 weights, 4px grid (enforced by hooks)
- **Security-First** - PII detection, field encryption, audit logging
- **Test Everything** - "Actually Works" protocol blocks untested code
- **Clean Architecture** - Consistent patterns across all features

### Team Collaboration
- **Perfect Handoffs** - Context transfers seamlessly between developers
- **GitHub Integration** - Issues, PRs, gists all connected
- **Conflict Prevention** - Know who's editing what in real-time
- **Knowledge Sharing** - Patterns discovered by one help all

### 🆕 Latest Enhancements
- **Truth Enforcement** - Prevents changing established values (`/facts`, `/exists`)
- **Deletion Protection** - Warns before removing code or files
- **Hydration Safety** - Catches Next.js SSR errors automatically
- **Import Validation** - Fixes path issues as you code
- **Field Registry Generation** - Auto-generate Zod schemas, test factories, masking

## 📊 The Complete Workflow

```
PROJECT IDEA → PROJECT PRD → GITHUB ISSUES → FEATURE PRDS → TASKS → CODE → PR → DEPLOY
     ↓              ↓              ↓              ↓           ↓       ↓      ↓      ↓
/init-project  /gi PROJECT    /fw start #   /prd feature  /gt,/pt  Auto  Complete  Ship
```

## 🔑 Essential Commands

```bash
# Every Day
/sr                # Smart Resume - start here always!
/help              # Context-aware help

# Feature Development  
/fw start 1        # Start working on issue #1
/prd feature       # Create Product Requirements
/gt feature        # Generate tasks
/pt feature        # Process tasks
/fw complete 1     # Create PR

# Quality & Testing
/vd                # Validate design
/btf feature       # Browser test
/sc                # Security check

# State Management
/checkpoint        # Manual save
/compress          # Reduce token usage
```

See **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** for all commands.

## 📁 What's Inside

```
├── .claude/           # 🧠 The brain - commands, hooks, automation
├── CLAUDE.md          # 📜 AI instructions (don't delete!)
├── QUICK_REFERENCE.md # 🎯 Daily command cheat sheet
├── docs/              # 📚 All documentation
│   ├── setup/        # Getting started guides
│   ├── workflow/     # Daily usage patterns
│   ├── technical/    # System architecture
│   └── claude/       # AI-specific docs
├── field-registry/    # 🔒 Security definitions
├── scripts/          # 🔧 Setup and utilities
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

## 💡 Key Features

### 1. **PRD-Driven Development**
```bash
/prd user-auth     # Generate requirements
/gt user-auth      # Break into 5-15 min tasks
/pt user-auth      # Work through systematically
```

### 2. **Design System Enforcement**
```typescript
// ❌ BLOCKED by hooks:
<p className="text-sm font-bold">

// ✅ ALLOWED:
<p className="text-size-3 font-semibold">
```

### 3. **Security-First Forms**
```bash
/ctf ContactForm   # Creates secure form with:
                   # - PII detection
                   # - Field encryption
                   # - Audit logging
                   # - TCPA compliance
```

### 4. **Multi-Agent Orchestration**
```bash
/orch feature      # Assigns to specialized agents:
                   # - Frontend: UI/UX
                   # - Backend: APIs
                   # - Security: Compliance
                   # - QA: Testing
```

## 📈 Results

Teams using this boilerplate report:
- **70% faster** feature development
- **90% fewer** design inconsistencies  
- **Zero** context loss between sessions
- **95% less** documentation time

## 🚦 Getting Started

### Option 1: New Project (5 minutes)
1. Clone repo
2. Run setup script
3. Start Claude Code
4. Run `/init`
5. Define project with `/init-project`

### Option 2: Existing Project (10 minutes)
1. Copy `.claude/` directory
2. Add CLAUDE.md and QUICK_REFERENCE.md
3. Run `/init`
4. Start using commands

## 📚 Documentation

- **Setup**
  - [Quick Start - New Project](docs/setup/QUICK_START_NEW_PROJECT.md)
  - [Add to Existing Project](docs/setup/ADD_TO_EXISTING_PROJECT.md)
  - [Day 1 Complete Guide](docs/setup/DAY_1_COMPLETE_GUIDE.md)
  
- **Daily Use**
  - [Quick Reference](QUICK_REFERENCE.md)
  - [Workflow Guide](docs/workflow/DAILY_WORKFLOW.md)
  
- **Deep Dives**
  - [System Overview](docs/technical/SYSTEM_OVERVIEW.md)
  - [Command List](docs/claude/CLAUDE_CODE_GUIDE.md)
  - [Security Guide](docs/SECURITY_GUIDE.md)

## 🎓 Philosophy

**"Vibe Coding"**: You define WHAT to build (strategy), the system handles HOW (implementation).

- Small verifiable tasks > Large ambiguous features
- Automated enforcement > Manual reviews
- Context preservation > Human memory
- Observable systems > Black boxes

## 🤝 Contributing

This boilerplate evolves with usage. Share your:
- Custom commands
- Workflow improvements  
- Bug fixes
- Success stories

---

Built by developers tired of:
- 🚫 Losing context between sessions
- 🚫 Inconsistent implementations
- 🚫 "It should work" syndrome
- 🚫 Manual documentation

Ready to build something amazing? Start with `/init-project` 🚀
