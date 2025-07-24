# Next.js 15 Boilerplate with Claude Code + Agent OS

This is a production-ready boilerplate for Next.js 15 projects with TypeScript, Tailwind CSS, Supabase, advanced Claude Code automation, PRP methodology, Agent OS integration for spec-driven development, and intelligent branch awareness.

## 🚀 Quick Start

### New Project
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

# Setup Branch Awareness
chmod +x setup-branch-awareness-integrated.sh
./setup-branch-awareness-integrated.sh

# Setup Agent OS Standards (NEW in v2.7.0)
mkdir -p ~/.agent-os/standards
# Then customize standards files in .agent-os/standards/
```

### Existing Project (NEW Drop-in Capability!)
```bash
# For existing projects, use the new analyze command
cd existing-project

# Quick add Claude Code
curl -sSL https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/scripts/add-to-existing.sh | bash -s full

# Then in Claude Code:
/analyze-existing     # Analyzes codebase and sets up full system
/migrate-to-strict-design analyze  # Check design compliance
/chain onboard-existing  # Run complete onboarding
```

### 📖 Essential Guides
- **[MASTER_WORKFLOW_GUIDE.md](MASTER_WORKFLOW_GUIDE.md)** - Complete workflow reference (START HERE!)
- **[docs/AGENCY_OS_GUIDE.md](docs/AGENCY_OS_GUIDE.md)** - Agency OS integration guide (NEW!)
- **[docs/setup/DAY_1_COMPLETE_GUIDE.md](docs/setup/DAY_1_COMPLETE_GUIDE.md)** - Detailed setup walkthrough
- **[.agent-os/INTEGRATION_GUIDE.md](.agent-os/INTEGRATION_GUIDE.md)** - Technical integration details

## 🎯 What You Get

### Core Features
- **118+ Custom Commands** - Everything from `/sr` (smart resume) to `/ut` (ultra-think)
- **Agent OS Integration** 🎨 - Centralized standards, drop-in capability, spec-driven development (NEW!)
- **Task Ledger** 📋 - Persistent task tracking across all features
- **UltraThink Mode** 🤯 - 32k+ token deep thinking with parallel agents
- **Visual Planning** 📸 - Ray Fernando-style screenshot-based iteration
- **PRP Methodology** 🚀 - One-pass implementation with validation loops
- **Zero Context Loss** - Auto-saves work state to GitHub gists

### Design System (Strict Enforcement)
- **4 Font Sizes Only**: `text-size-1` through `text-size-4`
- **2 Font Weights Only**: `font-regular` and `font-semibold`
- **4px Grid Spacing**: Only multiples of 4 (p-1, p-2, p-3, p-4, p-6, p-8...)
- **Automated Migration**: `/migrate-to-strict-design` for existing projects (NEW!)

### Automated Protections
- **21+ Pre-Tool Hooks** - Catch violations before they're written
- **Git Pre-Commit Validation** - Final checks before commits
- **Design System Toggle** - `/dmoff` for flexibility, `/dmon` for strictness
- **Standards-Based Rules** - Centralized in `.agent-os/standards/` (NEW!)

### Async Event Architecture
```typescript
// Fire-and-forget for non-critical operations
eventQueue.emit(LEAD_EVENTS.PIXEL_FIRE, data);
// Loading states required for all async operations
```

## 🆕 What's New in v2.7.0

### Agent OS Integration
- **Centralized Standards**: Single source of truth in `.agent-os/standards/`
- **Drop-in Capability**: `/analyze-existing` command for existing projects
- **Design Migration**: `/migrate-to-strict-design` to convert any codebase
- **Cross-Tool Sharing**: Standards work in Claude Code, Cursor, any AI tool
- **Spec-Driven Development**: Three-layer context system (Standards → Product → Specs)

### Enhanced Workflows
```bash
# Existing project onboarding
/chain analyze-existing-project

# Design system migration
/chain migrate-design-system

# Standards synchronization
/chain standards-sync
```

## 📚 Documentation Structure

```
docs/
├── setup/              # Getting started
├── workflow/           # Daily workflows
├── technical/          # System architecture
├── examples/           # Clear examples
├── updates/            # Feature changelogs
└── claude/             # AI-specific docs

.agent-os/              # NEW in v2.7.0
├── standards/          # Centralized rules
├── product/            # Mission, roadmap
└── specs/              # Feature specs

PRPs/                   # Product Requirement Prompts
├── templates/          # PRP templates
├── ai_docs/            # AI-optimized docs
└── scripts/            # Automation tools
```

## 🎮 Key Commands

### Daily Essentials
```bash
/sr                    # Smart Resume - restores full context
/ae                    # Analyze Existing - for existing projects (NEW!)
/fw start [#]          # Start feature from GitHub issue
/prd [name]            # Create specification
/prp [name]            # Create implementation prompt
/gt [name]             # Generate tasks
/pt [name]             # Process tasks with TDD
/grade                 # Check implementation alignment
```

### Design & Migration (NEW!)
```bash
/mds analyze           # Analyze design violations
/mds migrate           # Migrate to strict design
/vd                    # Validate current file
/dmoff                 # Disable enforcement temporarily
```

### Advanced Features
```bash
/ut [problem]          # UltraThink deep analysis
/vp [feature]          # Visual planning mode
/orch [feature]        # Multi-agent orchestration
/cti "Title"           # Capture to GitHub issue
/chain [name]          # Run command chains
```

## 🔧 Installation Requirements

- Node.js 18+
- pnpm (recommended) or npm
- Git
- Claude Code (with MCP enabled)
- Supabase account (for database)

## 🏗️ Project Structure

```
my-project/
├── app/                # Next.js 15 app directory
├── components/         # React components
│   ├── ui/            # Design system components
│   ├── forms/         # Form components
│   └── features/      # Feature components
├── lib/               # Utilities and helpers
│   ├── events/        # Async event system
│   ├── api/           # API client
│   └── utils/         # Helpers
├── .claude/           # Claude Code configuration
│   ├── commands/      # 113+ custom commands
│   ├── hooks/         # Automated enforcement
│   └── chains.json    # Workflow automation
├── .agent-os/         # Agent OS integration (NEW!)
│   └── standards/     # Centralized standards
├── PRPs/              # Product Requirement Prompts
│   ├── active/        # Current PRPs
│   └── templates/     # PRP templates
└── public/            # Static assets
```

## 🚀 Getting Started

1. **Clone and Setup**
   ```bash
   git clone https://github.com/bearingfruitco/claude-code-boilerplate.git my-project
   cd my-project
   ./scripts/quick-setup.sh
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env.local
   # Add your Supabase credentials
   ```

3. **Start Development**
   ```bash
   pnpm install
   pnpm dev
   ```

4. **In Claude Code**
   ```bash
   /sr                    # Load context
   /init-project          # Initialize project
   /fw start              # Start first feature
   ```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT - see [LICENSE](LICENSE) for details.

## 🙏 Credits

Built with insights from:
- Sean Grove's spec-driven development philosophy
- Brian Casel's Agent OS system
- The Claude Code community

---

**Ready to build faster?** Star this repo and start with `/sr` in Claude Code!
