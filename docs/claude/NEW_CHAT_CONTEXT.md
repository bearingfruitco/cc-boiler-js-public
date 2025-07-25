# NEW CHAT CONTEXT - Claude Code Boilerplate System v2.7.1

## 🚀 Quick Start for New Session

```bash
# 1. Start Claude Code
claude-code .

# 2. Resume with full context
/sr

# 3. Check active PRPs (NEW)
ls PRPs/active/

# 4. Load your context profile
/cp load frontend   # or backend, debug, etc.

# 5. Check open bugs
/bt list

# 6. Continue where you left off
```

## 🎯 System Overview

This is a production-ready boilerplate for AI-assisted development with:

### Core Features
1. **PRP Methodology** 🆕 - One-pass implementation with validation loops
2. **PRD-Driven Development** - Start with requirements, generate tasks automatically
3. **Design System Enforcement** - 4 sizes, 2 weights, 4px grid (enforced by hooks)
4. **Context Preservation** - Never lose work between sessions
5. **Security-First Forms** - PII/PHI protection with field registry
6. **Persona-Based Sub-Agents** - 9 specialized agents for parallel work
7. **110+ Custom Commands** - Streamlined workflows with aliases
8. **4-Level Validation** 🆕 - Syntax → Components → Integration → Production
9. **AI Documentation** 🆕 - Pre-digested docs for common patterns
10. **Git Pre-Commit Hooks** 🆕 - Catch issues before commits
11. **Native Claude Features** 🆕 - Visual debugging with Ctrl+V

## 📋 Current Capabilities

### 1. Next Command Suggestions (v2.7.0)
- **Intelligent Workflow Guidance**: After every command execution
- **Context-Aware Suggestions**: Based on results, state, and patterns
- **Time-Based Hints**: End-of-day saves, morning resume tips
- **Orchestration Detection**: Knows when parallel work saves time
- No more wondering "what's next?" - just follow the suggestions!

### 2. Git Pre-Commit Hooks (NEW v2.7.1)
- **Complements MCP Hooks**: Different validation at commit time
- **Quick Checks**: Only validates staged files for speed
- **Automatic Running**: No manual validation needed
- **Clear Errors**: Actionable fix suggestions
- Pre-commit runs:
  - Design system validation
  - TypeScript check (staged only)
  - Test runner (affected tests)
  - Console.log detection
  - PRP validation (if active)

### 3. Native Claude Code Features (NEW v2.7.1)
- **Visual Debugging**: `Ctrl+V` to paste screenshots for instant analysis
- **Non-Interactive Mode**: `claude --non-interactive "/sv status"` for CI/CD
- **Session History**: `claude --resume` shows branch context
- **Undo Typing**: `Ctrl+-` to recover lost commands
- **Multi-Directory**: `claude --add ../shared-components` for references
- See `docs/workflow/CLAUDE_CODE_NATIVE_FEATURES.md` for details

### 4. PRP System (v2.6.0)
- `/create-prp [feature]` or `/prp` - Generate comprehensive PRP
- `/prp-execute [name]` - Run validation loops
- `/prp-exec --fix` - Auto-fix common issues
- `/prp-exec --level 1` - Run specific validation level
- PRPs include:
  - Complete implementation blueprint
  - Curated codebase patterns
  - Known gotchas and warnings
  - 4-level validation loops
  - Links to pinned requirements

### 5. Smart Issue & Context Management
- `/cti [title]` - Capture Claude's response to GitHub issue
  - Checks for duplicate issues automatically
  - Links to PRDs and parent issues
  - Tracks components and dependencies
- `/deps check [component]` - See what uses a component
- `/deps scan` - Update all dependency tracking
- `/exists [name]` - Check before creating (now automatic)

### 6. PRD & Task Management
- `/prd [feature]` - Generate PRD with stage validation gates
- `/gt [feature]` - Generate granular tasks (5-15 min each)
- `/pt [feature]` - Process tasks one by one
- `/sv check [stage]` - Validate stage completion
- `/sv require [stage]` - Enforce stage gates
- `/ts` - Task status overview
- `/tb` - Visual task board

### 7. Design System (STRICTLY ENFORCED)
```
Font Sizes: ONLY text-size-1, text-size-2, text-size-3, text-size-4
Font Weights: ONLY font-regular, font-semibold
Spacing: ONLY multiples of 4 (p-1, p-2, p-3, p-4, p-6, p-8)
Colors: 60/30/10 distribution rule
Touch Targets: Minimum 44px (h-11)
Toggle: /dmoff to disable, /dmon to re-enable

NEW: Also enforced at git commit time!
```

### 8. Security & Data Protection
- **Field Registry**: `/field-registry/` defines all data fields
- **PII/PHI Protection**: Automatic detection and blocking
- **Encryption**: Field-level encryption for sensitive data
- **Audit Logging**: Every data access tracked
- **Compliance**: HIPAA/GDPR support built-in

Commands:
- `/ctf [form-name]` - Create secure tracked form
- `/afs [file]` - Audit form security
- `/gft` - Generate field types from registry

### 9. Persona-Based Sub-Agents
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

### 10. Hooks System
Active hooks enforce rules automatically:

**Pre-tool-use**:
- `02-design-check.py` - Blocks design violations
- `07-pii-protection.py` - Prevents PII exposure
- `03-conflict-check.py` - Prevents file conflicts
- `10-hydration-guard.py` - Prevents Next.js SSR errors
- `11-truth-enforcer.py` - Blocks changes to established facts
- `12-deletion-guard.py` - Warns before deletions
- `13-import-validator.py` - Fixes import paths
- `14-creation-guard.py` - Prevents duplicate components
- `15-dependency-tracker.py` - Alerts on shared component changes

**Post-tool-use**:
- `01-state-save.py` - Auto-saves to GitHub
- `02-metrics.py` - Tracks compliance
- `03-response-capture.py` - Captures Claude responses for issues

**Git pre-commit** (NEW):
- Design system validation
- TypeScript checking
- Test execution
- Debug code detection

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
- **Git Hooks**: Husky for pre-commit validation

## 📁 Key Directories

```
.claude/
├── commands/        # 110+ custom commands
├── hooks/          # Automation & safety
├── personas/       # Agent personalities
├── orchestration/  # Multi-agent coordination
├── checkpoints/    # State snapshots
├── bugs/           # Bug tracking
├── profiles/       # Context profiles
└── doc-cache/      # Documentation cache

.husky/             # Git pre-commit hooks (NEW)
├── pre-commit      # Runs validation checks

PRPs/               # Product Requirement Prompts (NEW)
├── templates/      # PRP templates
├── ai_docs/        # AI-optimized documentation
├── scripts/        # Validation runner
├── active/         # Current PRPs
└── completed/      # Reference PRPs

scripts/            # Helper scripts (NEW)
├── check-design-staged.js    # Pre-commit design check
├── test-staged-files.js      # Pre-commit test runner
└── typecheck-staged.js       # Pre-commit TypeScript

field-registry/
├── core/           # Universal tracking fields
├── verticals/      # Industry-specific (debt, healthcare)
└── compliance/     # PII/PHI rules

lib/
├── security/       # Encryption, PII detection
└── forms/          # Secure form handling
```

## 🚦 Workflow Examples

### PRP Workflow (NEW - Recommended)
```bash
# Start from GitHub issue
/fw start 45

# Create PRP for one-pass implementation
/create-prp user avatar upload

# Validate environment
/prp-execute avatar-upload --level 1

# Implement following blueprint
# ... code ...

# Validate after each phase
/prp-execute avatar-upload --level 2  # After components
/prp-execute avatar-upload --level 3  # After integration
/prp-execute avatar-upload --level 4  # Before PR

# Complete
/fw complete
```

### Traditional PRD Workflow
```bash
/prd user-profile        # Generate PRD with stage gates
/dc cache "React hooks"  # Cache relevant docs
/cp create "profile-work" # Create context profile
/gt user-profile        # Break into tasks
/at user-profile        # Assign to agents
/orch user-profile      # Start parallel work
/sv check 1             # Validate stage 1 before proceeding
```

### Visual Debugging (NEW)
```bash
# Quick UI debug without commands
1. Take screenshot of issue
2. Ctrl+V in Claude Code
3. "Why is this button misaligned?"
4. Get instant visual analysis

# Or use existing command for complex planning
/vp dashboard redesign
```

### Create Secure Form
```bash
/ctf ContactForm --vertical=debt
/afs components/forms/ContactForm.tsx
/gft                    # Generate types
```

### Daily Development
```bash
/sr                     # Smart resume
/cp load "frontend"     # Load context profile
/bt list --open         # Check open bugs
ls PRPs/active/         # Check active PRPs (NEW)
/sv status              # Check stage progress
/sas                    # Check agent status
/vd                     # Validate design
/checkpoint create      # Save progress

# When committing (NEW)
git add .
git commit -m "feat: add user profile"
# Pre-commit hooks run automatically!
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

### Git Commits (NEW)
- Design violations blocked
- TypeScript errors blocked
- Failing tests blocked
- Console.logs warned
- PRP violations blocked (if active)

## 📊 Command Categories

### PRP Commands (NEW)
- `/create-prp` or `/prp` - Generate PRP
- `/prp-execute` or `/prp-exec` - Run validation
- `/prp-run` - Alias for execute

### Essential Daily
- `/sr` - Smart Resume
- `/cp` - Context profiles
- `/bt` - Bug tracking
- `/help` - Context-aware help
- `/todo` - Task management

### Development
- `/cc` - Create component (validated)
- `/vd` - Validate design
- `/fw` - Feature workflow
- `/sv` - Stage validation
- `/dc` - Documentation cache
- `/deps` - Check dependencies
- `/cti` - Capture to issue
- `/exists` - Check before creating

### Testing
- `/btf` - Browser test flow
- `/tr` - Test runner
- `/pp` - Pre-PR validation

### Visual & Native (NEW)
- `Ctrl+V` - Paste screenshot for debugging
- `Ctrl+-` - Undo typing
- `/vp` - Visual planning (complex)

### Security
- `/ctf` - Create tracked form
- `/afs` - Audit form security
- `/sc` - Security check

### Orchestration
- `/orch` - Start multi-agent
- `/persona` - Switch persona
- `/sas` - Agent status

### Non-Interactive Mode (NEW)
```bash
# For CI/CD automation
claude --non-interactive "/sv check"
claude --non-interactive "/bt list --open"
claude --non-interactive "/deps scan"
```

## 🎯 PRP Validation Levels

### 🔴 Level 1: Syntax & Standards
- Linting and formatting
- TypeScript checking
- Design system validation
- Import validation

### 🟡 Level 2: Component Testing
- Unit tests
- Component tests
- Hook tests
- Isolated functionality

### 🟢 Level 3: Integration Testing
- E2E tests
- API integration
- Real database queries
- User workflows

### 🔵 Level 4: Production Readiness
- Lighthouse scores
- Bundle size analysis
- Security audit
- Requirement grading

## 💡 Key Innovations

1. **One-Pass Implementation**: PRPs provide everything needed upfront
2. **4-Level Validation**: Quality gates at each development stage
3. **Zero Context Loss**: Everything auto-saved and restored
4. **Design Enforcement**: Violations blocked before they happen
5. **Parallel Development**: Multiple specialized agents
6. **Security by Default**: PII protection built-in
7. **Natural Documentation**: From PRDs and handoffs
8. **Evidence-Based Development**: Claims backed by proof
9. **Smart Persona Selection**: Auto-suggests right expert
10. **Token Optimization**: `/compress` command when needed
11. **Git-Level Validation**: Pre-commit hooks catch final issues
12. **Visual Debugging**: Ctrl+V for instant UI analysis

## 🔗 Important Files

- 🚀 **`MASTER_WORKFLOW_GUIDE.md`** - Complete workflow reference (START HERE!)
- `CLAUDE.md` - AI behavior rules
- `docs/SYSTEM_OVERVIEW.md` - Complete system docs
- `docs/workflow/CLAUDE_CODE_NATIVE_FEATURES.md` - Native features guide (NEW!)
- `PRPs/README.md` - PRP methodology guide
- `docs/workflow/PRP_WORKFLOW_GUIDE.md` - PRP workflow
- `field-registry/README.md` - Data field docs
- `docs/SECURITY_GUIDE.md` - Security documentation

## 🆘 Troubleshooting

If something seems wrong:
1. Run `/sr` to restore context
2. Check `/sas` for agent status
3. Run `/help` for suggestions
4. Check hooks with `/error-recovery`
5. For PRPs: `/prp-execute --verbose`
6. For commits: Check `.husky/pre-commit` output

## 📈 Metrics

This system enables:
- One-pass implementation success (NEW)
- 70% faster development
- 90% fewer design inconsistencies
- Zero context loss between sessions
- 95% reduction in documentation effort
- 2-5x speedup with parallel agents
- 50% fewer broken commits (NEW)

---

**Remember**: 
- Choose PRPs for clear implementation, PRDs for exploration
- MCP hooks catch issues as you write, Git hooks catch issues at commit
- Use Ctrl+V for quick visual debugging, `/vp` for complex planning
- Non-interactive mode enables CI/CD automation
