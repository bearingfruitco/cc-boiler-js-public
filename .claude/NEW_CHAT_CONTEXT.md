# New Chat Context - Claude Code Boilerplate v2.7.1

## 🆕 What's New in v2.7.1

### Parallel Development Features (Kieran-Inspired)
- **Git Worktrees** (`/wt`) - True filesystem isolation for parallel development
- **Multi-Perspective Review** (`/mpr`) - Security, performance, UX, architecture reviews in parallel
- **Enhanced Suggestions** - Intelligent command suggestions for worktrees and reviews
- **Automatic Context** - Worktree awareness shows relevant info and commands

### New Commands
- `/wt` (`/worktree`) - Create isolated worktrees for parallel features
- `/wt-status` - View all active worktrees
- `/wt-switch [name]` - Switch between worktrees
- `/wt-pr [name]` - Create PR from worktree
- `/wt-clean` - Clean up worktrees
- `/mpr` (`/multi-review`) - Review from multiple expert perspectives
- `/chain multi-perspective-review` - Run reviews as workflow

## 🆕 What's New in v2.7.0

### Agent OS Integration 🎨
- **Problem Solved**: Scattered standards, no drop-in capability for existing projects
- **Centralized Standards**: All rules in `.agent-os/standards/` - single source of truth
- **Drop-in Capability**: `/analyze-existing` command analyzes any codebase
- **Design Migration**: `/migrate-to-strict-design` converts to our strict system
- **Cross-Tool Sharing**: Standards work in Claude Code, Cursor, any AI tool
- **Spec-Driven Development**: Three-layer context (Standards → Product → Specs)

### New Commands
- `/analyze-existing` (`/ae`, `/drop-in`) - Analyze existing project and set up
- `/migrate-to-strict-design` (`/mds`) - Migrate to strict design system
- `/smart-resume-standards` - Enhanced resume that loads standards

### Enhanced Workflows
- **Existing Project Onboarding**: `/chain analyze-existing-project`
- **Design Migration**: `/chain migrate-design-system`
- **Complete Onboarding**: `/chain onboard-existing`
- **Standards Sync**: `/chain standards-sync`

## 🆕 What's New in v2.6.0

### Branch Awareness & Feature Protection System 🌿
- **Problem Solved**: AI can no longer recreate completed features or create conflicting branches
- **Feature Awareness**: Shows helpful context when editing completed features (non-blocking)
- **Branch Health**: Periodic tips about branch hygiene and maintenance
- **Smart Integration**: Works seamlessly with existing PRD/PRP workflows
- **Progressive Enhancement**: Info-only mode by default, can add warnings/protection later

### New Commands
- `/branch-info` (`/bi`) - Lightweight branch status for automation
- `/branch-status` (`/bs`) - Comprehensive branch overview
- `/feature-status` (`/fs`) - Check feature completion and details
- `/sync-main` (`/sync`) - Safely sync main branch
- `/feature-complete` (`/fc`) - Mark features as completed
- `/branch-clean` (`/bc`) - Clean up merged branches
- `/branch-switch` (`/bsw`) - Smart branch switching with context

### Enhanced Workflows
- **Smart Resume**: Now shows branch health and feature warnings
- **PRP Integration**: Feature awareness in validation loops
- **Event System**: Branch events fire to async queue
- **Chain Support**: New chains for branch-aware workflows

## 🆕 What's New in v2.5.0

### Requirement Fidelity System 🔒
- **Problem Solved**: AI can no longer change requirements (e.g., reducing 13 fields to 7)
- **Requirement Locking**: `/pin-requirements 42 ContactForm` - Lock specs from GitHub issues
- **Context Anchoring**: `/anchor-context "13 fields required"` - Add immutable context
- **Drift Detection**: Hooks block any changes that violate locked requirements
- **Compliance Reviews**: `/review-requirements` - Validate implementation matches specs
- **Test Generation**: `/test-requirements` - Auto-generate tests from requirements

### New Commands
- `/pin-requirements` (`/pin`, `/pr`) - Lock requirements from issues
- `/anchor-context` (`/ac`) - Add permanent context
- `/review-requirements` (`/rr`) - Check compliance
- `/test-requirements` (`/tr-gen`) - Generate requirement tests
- `/grade --requirements` - Pre-implementation confidence check

## 🆕 What's New in v2.3.6

### Async Event-Driven Architecture
- **Event Queue System**: Fire-and-forget pattern for non-critical operations
- **No More Blocking**: Analytics and tracking run asynchronously
- **Parallel Processing**: Automatic detection of operations that can run in parallel
- **Required Loading States**: Every async operation must show user feedback
- **Smart Form Events**: Built-in tracking hooks for lead generation
- **Timeout Protection**: All external calls have automatic timeout handling

### New Commands
- `/create-event-handler` - Create async event handler with retry logic
- `/prd-async` - Add async requirements section to any PRD
- `/validate-async` - Check code for async anti-patterns
- `/test-async-flow` - Test event chains end-to-end

### Enhanced Form Generation
```typescript
// Forms now include automatic event tracking that flows through Rudderstack
const { trackFormSubmit, trackSubmissionResult } = useLeadFormEvents('form-name');

// All events automatically sent to Rudderstack with proper formatting:
// - Form Viewed
// - Form Started  
// - Form Field Changed
// - Form Submitted
// - Lead Captured
// - Consent Given

// Non-blocking tracking through existing analytics infrastructure
eventQueue.emit(LEAD_EVENTS.FORM_SUBMIT, data);
// → Automatically bridged to: rudderanalytics.track('Form Submitted', data)
```

## 🚀 Quick Start

You're working with an advanced AI-assisted development system that treats specifications (PRDs) as the primary development artifact, following Sean Grove's "The New Code" philosophy, enhanced with Brian Casel's Agent OS for spec-driven development.

### First Commands

#### For New Projects:
```bash
/sr                    # Smart Resume - restores full context
/init-project          # Initialize new project
/help new              # See latest features
```

#### For Existing Projects (NEW!):
```bash
/ae                    # Analyze existing codebase
/mds analyze           # Check design compliance
/chain onboard-existing # Complete onboarding
```

#### For Parallel Development (NEW!):
```bash
/wt feat1 feat2 feat3  # Create isolated worktrees
/wt-status             # Monitor all worktrees
/wt-switch feat1       # Work on specific feature
/mpr                   # Multi-perspective review before PR
```

### One-Time Setup (2 minutes)
1. Install CodeRabbit extension in Cursor
2. Sign up at app.coderabbit.ai (free)
3. Select "Claude Code" as AI agent
4. Customize `.agent-os/standards/` files (NEW!)
5. Start coding with real-time review!

## 🌟 Latest Features

### Agent OS Standards (v2.7.0)
```bash
# Standards live in:
.agent-os/standards/
├── design-system.md    # Your 4-size, 2-weight rules
├── tech-stack.md       # Your technology choices
└── best-practices.md   # Your development philosophy

# Commands automatically reference these
/vd                     # Reads from design-system.md
/sr                     # Loads all standards
```

### Drop-in for Existing Projects (v2.7.0)
```bash
cd existing-project
/ae                     # Analyzes and sets up everything

# Creates:
.agent-os/product/
├── mission.md          # What you're building
├── roadmap.md          # Features (Phase 0 = existing)
├── tech-stack.md       # Detected stack
└── decisions.md        # Architectural choices
```

### Design Migration (v2.7.0)
```bash
/mds analyze            # Find all violations
# Output: DESIGN_MIGRATION_REPORT.md

/mds migrate            # Auto-migrate to strict system
# Creates backup, updates all files

/vd                     # Verify compliance
```

### Async Event System (v2.3.6)
```typescript
import { eventQueue, LEAD_EVENTS } from '@/lib/events';

// Critical path - await required
await api.submitForm(data);

// Non-critical - fire and forget
eventQueue.emit(LEAD_EVENTS.PIXEL_FIRE, data);
eventQueue.emit(LEAD_EVENTS.WEBHOOK_SEND, data);

// Parallel operations
const [user, prefs, perms] = await Promise.all([
  fetchUser(),
  fetchPreferences(),
  fetchPermissions()
]);
```

### Design System Toggle (v2.3.5)
```bash
/dmoff                  # Freedom mode - use any Tailwind classes
# Now you can use: text-sm, p-5, font-bold, etc.

/dmon                   # Strict mode - back to 4 sizes, 2 weights
# Only: text-size-[1-4], font-regular/semibold, 4px grid
```

## 🎯 Core Workflow

### New Projects:
```
IDEA → /init-project → /prd → /prd-async → /gt → /pt → /grade → /fw complete
```

### Existing Projects (NEW!):
```
PROJECT → /ae → /mds analyze → /create-prd-from-existing → /gt → /pt → /grade
```

1. **Define** specifications clearly (PRD)
2. **Add** async requirements 
3. **Generate** tests from acceptance criteria
4. **Implement** through micro-tasks
5. **Grade** alignment with original intent
6. **Extract** patterns for future reuse

## 📋 Essential Commands

### Daily Development
```bash
/sr                    # Resume where you left off
/ae                    # Analyze existing project (NEW)
/fw start [#]          # Start GitHub issue
/prd [name]            # Create specification
/prd-async [name]      # Add async requirements
/prd-tests [name]      # Generate test suite
/gt [name]             # Generate tasks
/pt [name]             # Process tasks (with real-time review)
/grade                 # Check alignment
/specs extract         # Save successful pattern
```

### Design & Migration (NEW)
```bash
/mds analyze           # Check design violations
/mds migrate           # Migrate to strict system
/vd                    # Validate current file
/dmoff                 # Disable enforcement
/dmon                  # Re-enable enforcement
```

### Quality & Safety
```bash
/validate-async        # Check async patterns
/sv check              # Stage validation
/facts                 # Protected values
/exists [name]         # Check before creating
/bt add "bug"          # Track bugs
```

### Branch Management
```bash
/bs                    # Branch status
/fs                    # Feature status
/sync                  # Sync with main
/fc                    # Complete feature
/bc                    # Clean branches
```

## 🛡️ Automatic Protections

The system automatically:
- **Reads** standards from `.agent-os/standards/` (NEW!)
- **Approves** safe operations (no more waiting!)
- **Blocks** design violations (wrong CSS classes)
- **Warns** about ambiguous PRD language
- **Detects** async anti-patterns
- **Saves** context every 60 seconds
- **Prevents** PII exposure
- **Tracks** bugs persistently
- **Grades** implementation quality
- **Reviews** code in real-time (CodeRabbit)
- **Suggests** fixes before commit
- **Migrates** existing code to strict standards (NEW!)

## 💡 Key Principles

1. **Specifications are primary** - PRDs drive everything
2. **Standards are centralized** - One source of truth (NEW!)
3. **Clear communication** - Ambiguity is the enemy
4. **Automated enforcement** - Hooks handle compliance
5. **Pattern learning** - Success builds on success
6. **Objective quality** - Measurable alignment
7. **User experience first** - Never block on non-critical ops

## 🔑 Quick Reference

```
SPECIFICATIONS          DEVELOPMENT            QUALITY
/prd    - create       /cc  - component       /grade  - alignment
/prp    - create PRP   /vd  - design check    /sv     - stages
/specs  - patterns     /bt  - bug track       /btf    - browser
/prd-tests - tests     /validate-async        /mds    - migrate (NEW)

CONTEXT                COLLABORATION          EXISTING PROJECTS (NEW)
/sr     - resume       /fw  - workflow        /ae     - analyze
/cp     - profiles     /orch - agents         /mds    - migrate design
/dc     - doc cache    /team - status         /chain  - onboard-existing
/research - organize   

BRANCH MANAGEMENT      EVENTS                 REVIEW
/bs     - status       /create-event-handler  /pr-feedback
/fs     - features     /test-async-flow       CodeRabbit (IDE)
/sync   - sync main                           /mpr    - multi-review (NEW)
/fc     - complete

PARALLEL DEV (NEW)     WORKTREES             MULTI-REVIEW
/wt     - create       /wt-status             /mpr --pr [#]
/wt-switch             /wt-pr                 /mpr --worktree
/wt-clean              /chain wte             /chain mpr
```

## 🔑 Key Files

- `.agent-os/standards/` - Centralized standards (NEW!)
- `CLAUDE.md` - AI agent instructions
- `QUICK_REFERENCE.md` - All commands
- `INTEGRATION_GUIDE.md` - Agent OS details (NEW!)
- `docs/releases/` - Detailed release notes
- `.claude/config.json` - System configuration

## 🎨 Design System

**Centralized in `.agent-os/standards/design-system.md`:**
- Font sizes: `text-size-1` through `text-size-4` only
- Font weights: `font-regular`, `font-semibold` only
- Spacing: 4px grid (p-1, p-2, p-3, p-4, p-6, p-8)
- Colors: 60% neutral, 30% primary, 10% accent

**Toggle with:**
- `/dmoff` - Disable enforcement, use any Tailwind
- `/dmon` - Re-enable strict mode

## 🚦 Getting Help

```bash
/help              # Context-aware help
/help new          # Latest features
/help existing     # Existing project guide (NEW!)
/help workflows    # Common patterns
/help [command]    # Specific command
```

## 💭 Philosophy

> "The person who communicates most effectively is the most valuable programmer." - Sean Grove

> "Your coding agents are capable of so much more—they just need an operating system." - Brian Casel

This system helps you:
- Write clear specifications
- Centralize standards across tools
- Drop into any existing project
- Generate code from intent
- Measure alignment objectively
- Learn from successes
- Collaborate seamlessly
- Build performant UIs

Ready to start? 
- New project: `/init-project`
- Existing project: `/ae` (NEW!)
- Resume work: `/sr`
