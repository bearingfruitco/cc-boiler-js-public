# NEW CHAT CONTEXT - Claude Code Boilerplate System

## 🚀 Quick Start for New Session

```bash
# 1. Start Claude Code
claude-code .

# 2. Resume with full context
/sr

# 3. Check current status
/sas

# 4. Continue where you left off
```

## 🎯 System Overview

This is a production-ready boilerplate for AI-assisted development with:

### Core Features
1. **PRD-Driven Development** - Start with requirements, generate tasks automatically
2. **Design System Enforcement** - 4 sizes, 2 weights, 4px grid (enforced by hooks)
3. **Context Preservation** - Never lose work between sessions
4. **Security-First Forms** - PII/PHI protection with field registry
5. **Persona-Based Sub-Agents** - 9 specialized agents for parallel work
6. **90+ Custom Commands** - Streamlined workflows with aliases

## 📋 Current Capabilities

### 1. PRD & Task Management
- `/prd [feature]` - Generate Product Requirements Document
- `/gt [feature]` - Generate granular tasks (5-15 min each)
- `/pt [feature]` - Process tasks one by one
- `/ts` - Task status overview
- `/tb` - Visual task board

### 2. Design System (STRICTLY ENFORCED)
```
Font Sizes: ONLY text-size-1, text-size-2, text-size-3, text-size-4
Font Weights: ONLY font-regular, font-semibold
Spacing: ONLY multiples of 4 (p-1, p-2, p-3, p-4, p-6, p-8)
Colors: 60/30/10 distribution rule
Touch Targets: Minimum 44px (h-11)
```

### 3. Security & Data Protection
- **Field Registry**: `/field-registry/` defines all data fields
- **PII/PHI Protection**: Automatic detection and blocking
- **Encryption**: Field-level encryption for sensitive data
- **Audit Logging**: Every data access tracked
- **Compliance**: HIPAA/GDPR support built-in

Commands:
- `/ctf [form-name]` - Create secure tracked form
- `/afs [file]` - Audit form security
- `/gft` - Generate field types from registry

### 4. Persona-Based Sub-Agents
Available personas:
- **frontend** - UI/UX specialist
- **backend** - Server architect
- **security** - Compliance analyst
- **qa** - Quality engineer
- **architect** - System designer
- **performance** - Optimization expert
- **integrator** - API specialist
- **data** - Database engineer
- **mentor** - Documentation guide

Commands:
- `/orch [feature]` - Orchestrate multiple agents
- `/spawn [persona]` - Create specialized agent
- `/persona [type]` - Switch to persona mode
- `/at [feature]` - Visualize task assignments
- `/orchestration-view` - See visual diagram

### 5. Hooks System
Active hooks enforce rules automatically:

**Pre-tool-use**:
- `02-design-check.py` - Blocks design violations
- `07-pii-protection.py` - Prevents PII exposure
- `03-conflict-check.py` - Prevents file conflicts
- `10-hydration-guard.py` - Prevents Next.js SSR errors (NEW)
- `11-truth-enforcer.py` - Blocks changes to established facts (NEW)
- `12-deletion-guard.py` - Warns before deletions (NEW)
- `13-import-validator.py` - Fixes import paths (NEW)

**Post-tool-use**:
- `01-state-save.py` - Auto-saves to GitHub
- `02-metrics.py` - Tracks compliance

## 🔧 Technical Stack

- **Framework**: Next.js 15 (App Router + Turbopack)
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS + Radix UI primitives
- **Database**: Supabase + Drizzle ORM
- **Authentication**: Auth.js v5 (next-auth)
- **State**: Zustand + TanStack Query
- **Testing**: Vitest + Playwright + MSW
- **Date/Time**: date-fns v4 with timezones
- **Build**: Turbopack (dev) + Biome (lint/format)
- **Security**: Field-level encryption, audit logging, PII protection

## 📁 Key Directories

```
.claude/
├── commands/        # 90+ custom commands
├── hooks/          # Automation & safety
├── personas/       # Agent personalities
├── orchestration/  # Multi-agent coordination
└── checkpoints/    # State snapshots

field-registry/
├── core/           # Universal tracking fields
├── verticals/      # Industry-specific (debt, healthcare)
└── compliance/     # PII/PHI rules

lib/
├── security/       # Encryption, PII detection
└── forms/          # Secure form handling
```

## 🚦 Workflow Examples

### Start New Feature
```bash
/prd user-profile        # Generate PRD
/gt user-profile        # Break into tasks
/at user-profile        # Assign to agents
/orch user-profile      # Start parallel work
```

### Create Secure Form
```bash
/ctf ContactForm --vertical=debt
/afs components/forms/ContactForm.tsx
/gft                    # Generate types
```

### Enhanced UI Design Flow
```bash
# 1. Extract style from reference (optional)
/extract-style https://dribbble.com/shots/123456

# 2. Create component with wireframe
/cc ui ProductCard --wireframe --animate
# - Shows ASCII layout first
# - Plans animations
# - Applies design system

# 3. Validate design compliance
/vd components/ui/ProductCard.tsx
```

### Daily Development
```bash
/sr                     # Smart resume
/sas                    # Check agent status
/vd                     # Validate design
/checkpoint create      # Save progress
```

## 🔒 Security Rules (ENFORCED)

### NEVER (Blocked by Hooks)
- Log PII to console
- Store PII in localStorage
- Put PII in URLs
- Use forbidden CSS classes
- Modify files outside persona boundaries

### ALWAYS (Automated)
- Encrypt PII fields
- Audit log access
- Test before claiming "done"
- Use design system tokens
- Sync before editing

## 📊 Command Categories

### Essential Daily
- `/sr` - Smart Resume
- `/help` - Context-aware help
- `/todo` - Task management

### Development
- `/cc` - Create component (validated)
  - `--wireframe` - Start with ASCII layout
  - `--animate` - Plan animations first
- `/extract-style` - Extract design from reference
- `/vd` - Validate design
- `/fw` - Feature workflow

### Testing
- `/btf` - Browser test flow
- `/tr` - Test runner
- `/pp` - Pre-PR validation

### Security
- `/ctf` - Create tracked form
- `/afs` - Audit form security
- `/sc` - Security check

### Orchestration
- `/orch` - Start multi-agent
- `/persona` - Switch persona
- `/sas` - Agent status

## 🎯 Current Project State

[This section should be updated with your specific project details]

### Active Features
- Feature: [name]
- Branch: [current-branch]
- Tasks: [X/Y complete]
- Agents: [active personas]

### Recent Changes
- [List recent significant changes]

### Next Steps
- [Immediate next actions]

## 💡 Key Innovations

1. **Zero Context Loss**: Everything auto-saved and restored
2. **Design Enforcement**: Violations blocked before they happen
3. **Parallel Development**: Multiple specialized agents
4. **Security by Default**: PII protection built-in
5. **Natural Documentation**: From PRDs and handoffs
6. **Evidence-Based Development (NEW)**: Claims backed by proof - "testing shows" not "this is best"
7. **Smart Persona Selection (NEW)**: Auto-suggests right expert based on file/task
8. **Token Optimization (NEW)**: `/compress` command compresses context when needed

## 🔗 Important Files

- `CLAUDE.md` - AI behavior rules
- `SYSTEM_OVERVIEW.md` - Complete system docs
- `DAY_1_COMPLETE_GUIDE.md` - Setup instructions
- `field-registry/README.md` - Data field docs
- `docs/SECURITY_GUIDE.md` - Security documentation

## 🆘 Troubleshooting

If something seems wrong:
1. Run `/sr` to restore context
2. Check `/sas` for agent status
3. Run `/help` for suggestions
4. Check hooks with `/error-recovery`

## 📈 Metrics

This system enables:
- 70% faster development
- 90% fewer design inconsistencies
- Zero context loss between sessions
- 95% reduction in documentation effort
- 2-5x speedup with parallel agents

## 🆕 Latest Safety Features

### New Commands
- `/facts` or `/truth` - See protected values
- `/exists` or `/check` - Verify before creating
- `/field-generate` or `/fg` - Generate code from registry
- `/truth-override` - Allow intentional changes

### New Chains
- `/chain safe-commit` - Validate before committing
- `/chain field-sync` - Regenerate field code
- `/chain pre-component` - Check before creating

### New Protections (Automatic)
- ✅ Changes to API routes blocked unless intentional
- ✅ Warns before deleting code
- ✅ Catches Next.js hydration errors
- ✅ Fixes import path issues

---

**Remember**: You don't need to remember anything - the system remembers for you. Just run `/sr` at the start of each session!
