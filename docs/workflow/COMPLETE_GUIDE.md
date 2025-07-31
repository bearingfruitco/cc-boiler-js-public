# 📚 Claude Code Boilerplate - Complete Documentation Guide

> **Version 4.0.0** - Your single source of truth for all workflows, commands, and setup procedures

## 🎯 What Do You Want To Do?

### 🆕 Starting Fresh
- **[New Project Setup](#new-project-setup)** - Create a new project with the boilerplate
- **[Quick Start Commands](#quick-start-commands)** - Essential commands to get going

### 📦 Existing Project
- **[Add to Existing Project](#add-to-existing-project)** - Drop the boilerplate into your current project
- **[Migration Guide](#migration-guide)** - Migrate from older versions

### 🚀 Daily Development
- **[Daily Workflow](#daily-workflow)** - Your everyday development flow
- **[Command Reference](#command-reference)** - All 133 commands explained
- **[Workflow Chains](#workflow-chains)** - Pre-built command sequences

### 🛠️ Advanced Features
- **[PRP Methodology](#prp-methodology)** - One-pass implementation
- **[Multi-Agent Orchestration](#multi-agent-orchestration)** - Parallel development
- **[Security & Compliance](#security--compliance)** - PII/TCPA/GDPR features

---

## 🆕 New Project Setup

### Quick Setup (Recommended)
```bash
# 1. Clone the boilerplate
git clone https://github.com/yourusername/claude-code-boilerplate.git my-project
cd my-project

# 2. Run setup script
./scripts/quick-setup.sh

# 3. Start Claude Code
claude

# 4. Initialize project
/init-project
```

### Manual Setup
```bash
# 1. Install dependencies
pnpm install

# 2. Configure environment
cp .env.example .env.local
# Edit .env.local with your values

# 3. Set up database
pnpm db:push

# 4. Start development
pnpm dev
```

---

## 📦 Add to Existing Project

### Agent OS Drop-in Method (NEW v2.7.0)
```bash
# 1. In your existing project, start Claude Code
claude

# 2. Analyze your project
/analyze-existing

# 3. Check design system compliance
/migrate-to-strict-design analyze

# 4. Run complete onboarding
/chain onboard-existing
```

This will:
- ✅ Set up .claude directory with all commands
- ✅ Create .agent-os/standards for cross-tool compatibility
- ✅ Analyze your codebase structure
- ✅ Set up PRDs for existing features
- ✅ Configure hooks and automation

### Manual Integration
```bash
# 1. Copy core files
cp -r path/to/boilerplate/.claude .
cp -r path/to/boilerplate/.agent-os .
cp path/to/boilerplate/CLAUDE.md .

# 2. Install Git hooks
npx husky install
cp -r path/to/boilerplate/.husky/* .husky/

# 3. Add to package.json scripts
{
  "scripts": {
    "design:check:staged": "node scripts/check-design-staged.js",
    "prp:validate:quick": "bun run PRPs/scripts/prp-runner.ts --level 1 --staged-only"
  }
}
```

---

## 🚀 Daily Workflow

### Morning Startup
```bash
# 1. Resume context from previous session
/sr

# 2. Check what needs attention
/bt list          # Open bugs
/fw status        # Active features
/todo list        # Tasks

# 3. Load your work profile
/cp load frontend  # or backend, fullstack
```

### Feature Development

#### Option 1: Clear Requirements (Use PRP)
```bash
# Start from GitHub issue
/fw start 123

# Create Product Requirement Prompt
/create-prp user-authentication

# Validate and implement
/prp-execute user-authentication --level 1  # Syntax check
# ... implement code ...
/prp-execute user-authentication --level 2  # Component tests
# ... more implementation ...
/prp-execute user-authentication --level 3  # Integration
/prp-execute user-authentication --level 4  # Production ready

# Complete feature
/fw complete
```

#### Option 2: Exploratory Development (Use PRD)
```bash
# Create Product Requirements Document
/prd new-feature

# Generate tasks
/gt new-feature

# Process tasks one by one
/pt new-feature

# Grade implementation
/grade
```

### Testing & Validation
```bash
# Design system check
/vd

# Run tests
pnpm test

# Browser testing
/btf

# Security audit
/security-check all

# Full validation
/chain pre-pr
```

### Committing Work
```bash
# Stage changes
git add .

# Pre-commit hooks run automatically:
# - Design validation
# - TypeScript check
# - Tests
# - PRP validation

git commit -m "feat: add user authentication"

# Create PR
/fw complete
```

---

## 📖 Command Reference

### Essential Commands (Use Daily)
| Command | Alias | Description |
|---------|-------|-------------|
| `/sr` | - | Smart Resume - restores context |
| `/cp` | - | Context Profile - save/load work modes |
| `/bt` | - | Bug Track - persistent bug tracking |
| `/vd` | - | Validate Design - check compliance |
| `/checkpoint` | `/cp` | Manual state save |

### Development Commands
| Command | Alias | Description |
|---------|-------|-------------|
| `/cc` | - | Create Component with design rules |
| `/ctf` | - | Create Tracked Form with PII protection |
| `/prd` | - | Create PRD for exploration |
| `/prp` | `/create-prp` | Create PRP for implementation |
| `/gt` | - | Generate Tasks from PRD |
| `/pt` | - | Process Tasks systematically |

### v4 Advanced Commands
| Command | Alias | Description |
|---------|-------|-------------|
| `/chain fsf` | - | Full-stack feature with TDD |
| `/chain sfa` | - | Security-first API |
| `/v4-status` | `/v4s` | Check v4 automation status |
| `/performance-monitor` | `/pm` | Real-time monitoring |
| `/auto-fix-error` | `/afe` | AI-powered error fixing |

### Multi-Agent Commands
| Command | Alias | Description |
|---------|-------|-------------|
| `/orch` | - | Orchestrate multiple agents |
| `/spawn` | - | Create specialized agent |
| `/ut` | - | UltraThink - deep analysis |
| `/vp` | - | Visual Plan - screenshot-based |

[Full command list: 133 commands available]

---

## 🔗 Workflow Chains

### Daily Chains
```bash
/chain ms    # morning-setup - Resume, check status, load profile
/chain ds    # daily-startup - Full startup with health checks
/chain pp    # pre-pr - Complete validation before PR
```

### Feature Development Chains
```bash
/chain fsf   # full-stack-feature-v4 - TDD with phases
/chain prf   # production-ready-feature - All requirements
/chain fdc   # feature-development-chain - Multi-agent
```

### Security Chains
```bash
/chain sfa   # security-first-api-v4 - Mandatory security
/chain sb    # security-baseline - Establish baseline
/chain sac   # security-audit-chain - Comprehensive audit
```

### Maintenance Chains
```bash
/chain poc   # performance-optimization-chain
/chain rc    # refactoring-chain
/chain dmc   # database-migration-chain
```

---

## 🎓 PRP Methodology

### What is PRP?
**Product Requirement Prompt** = PRD + Codebase Intelligence + Validation Loops

### When to Use PRP vs PRD
- **Use PRP**: Clear requirements, known solution, implementation focus
- **Use PRD**: Exploration needed, unclear requirements, discovery phase

### PRP Workflow
```bash
# 1. Create PRP from requirements
/create-prp feature-name

# 2. Validate at each level
/prp-execute feature-name --level 1  # Syntax & Standards
/prp-execute feature-name --level 2  # Component Testing  
/prp-execute feature-name --level 3  # Integration Testing
/prp-execute feature-name --level 4  # Production Readiness

# 3. Auto-fix common issues
/prp-execute feature-name --fix
```

### PRP Benefits
- ✅ One-pass implementation success
- ✅ Curated codebase patterns included
- ✅ Known gotchas documented
- ✅ Validation at each phase
- ✅ Links to pinned requirements

---

## 🤖 Multi-Agent Orchestration

### Available Agents (31 specialists)
- **Frontend**: `ui-systems`, `frontend-ux-specialist`
- **Backend**: `backend-reliability-engineer`, `supabase-specialist`
- **Security**: `security-threat-analyst`, `privacy-compliance`
- **Database**: `database-architect`, `orm-specialist`
- **Testing**: `qa-test-engineer`, `tdd-engineer`
- **Performance**: `performance-optimizer`
- **Documentation**: `documentation-writer`

### Orchestration Example
```bash
# Automatic orchestration for complex tasks
/orch "Build complete authentication system"

# Manual multi-agent review
/chain mpr  # multi-perspective-review

# Spawn specific agent
/spawn security-threat-analyst --task "Audit API endpoints"
```

---

## 🔒 Security & Compliance

### PII Protection
```bash
# Create secure form with field-level encryption
/ctf ContactForm --vertical=debt

# Audit form security
/afs components/forms/ContactForm.tsx

# Generate field types from registry
/gft
```

### Security Features
- Field-level encryption for PII
- Audit logging for all access
- TCPA/GDPR compliance built-in
- Server-side only processing
- No PII in URLs/logs/client storage

### Security Commands
```bash
/security-check all       # Full security audit
/generate-rls            # Generate RLS policies
/chain security-baseline # Establish baseline
/spawn-security-auditor  # Deep security analysis
```

---

## 🛠️ Configuration

### Key Files
- `.claude/settings.json` - Hook configuration
- `.claude/chains.json` - Workflow chains
- `.claude/aliases.json` - Command shortcuts
- `.agent-os/standards/` - Design system rules

### Feature Flags
```json
{
  "v4_features": true,
  "auto_triggers": true,
  "performance_budgets": true
}
```

### Environment Variables
```bash
# Required
DATABASE_URL=
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=

# Optional
NEXT_PUBLIC_RUDDERSTACK_KEY=
NEXT_PUBLIC_SENTRY_DSN=
```

---

## 🚨 Troubleshooting

### Common Issues

#### "Command not found"
```bash
# Reload commands
/sr
# Check command registry
cat .claude/command-registry.json | grep "command-name"
```

#### Design violations
```bash
# Check what's wrong
/vd

# Auto-fix common issues
/vd --fix

# Toggle design mode
/dmoff  # Disable temporarily
/dmon   # Re-enable
```

#### Context lost
```bash
# Restore from GitHub gist
/sr

# Load specific profile
/cp load frontend

# Manual checkpoint
/checkpoint
```

### Getting Help
```bash
/help              # Context-aware help
/help-decide       # Workflow guidance
/error-recovery    # Fix common errors
```

---

## 📚 Additional Resources

### In-Depth Guides
- [PRP Methodology Deep Dive](./PRPs/README.md)
- [Hook System Reference](./.claude/hooks/README.md)
- [Design System Rules](./.agent-os/standards/design-system.md)
- [Security Implementation](./docs/SECURITY_GUIDE.md)

### Quick References
- [Command Cheatsheet](./docs/QUICK_REFERENCE.md)
- [Keyboard Shortcuts](./docs/SHORTCUTS.md)
- [Troubleshooting Guide](./docs/TROUBLESHOOTING.md)

### Updates & Changes
- [Changelog](./CHANGELOG.md)
- [Version 4.0 Features](./docs/releases/v4.0.0.md)
- [Roadmap](./docs/roadmap/2025.md)

---

## 💡 Pro Tips

1. **Always start with `/sr`** - Context is everything
2. **Use chains for complex workflows** - They handle the sequence
3. **Trust the design system** - It's there to help
4. **Let hooks do the work** - They prevent mistakes
5. **Grade your implementations** - Aim for >80% PRD alignment
6. **Use the right tool**:
   - Clear requirements → PRP
   - Exploration needed → PRD
   - Visual issues → /vp with screenshots
   - Deep thinking → /ut

---

**Need more help?** The system provides intelligent next-command suggestions after each operation. Just follow the flow! 🚀
