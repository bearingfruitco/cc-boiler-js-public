# New Chat Context - Claude Code Boilerplate v2.7.0

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

## 🆕 What's New in v2.3.5

### Design System Flexibility
- **Instant Toggle**: `/dmoff` to disable, `/dmon` to enable design system
- **Full Tailwind Freedom**: Use any classes when disabled (text-sm, p-5, etc.)
- **Smart Switching**: Toggle between strict and creative modes instantly

### Research Management System (RMS)
- **Smart Document Updates**: No more auth-v1, auth-v2, auth-final versions
- **Intelligent Merging**: Updates existing research instead of creating duplicates
- **Context-Aware Loading**: Only includes relevant research, respects limits
- **Clean Codebase**: Research organized in .claude/research/, not scattered
- **Compaction Support**: Research automatically preserved and restored

## 🆕 What's New in v2.3.4

### CodeRabbit IDE Integration
- **Dual-AI Workflow**: Claude generates, CodeRabbit reviews in real-time
- **95% Bug Catch Rate**: Issues caught before commit, not after PR
- **Design System Enforcement**: Automatic compliance checking as you type
- **Educational Feedback**: Learn from mistakes with clear explanations

## 🆕 What's New in v2.3.3

### Hook System Enhancements
- **PreCompact Support**: Context preserved during conversation compaction
- **Suggestion Engine**: Design violations now show helpful corrections
- **Command Logging**: Query your command history and performance

## 🆕 What's New in v2.3.2

### GitHub Apps Integration
- **CodeRabbit**: AI code reviews on every PR (catches 95%+ bugs)
- **Claude Code App**: PRD alignment validation (included with Max plan)
- **Smart Setup**: New `scripts/quick-setup.sh` prevents repo confusion
- **Enhanced Commands**: `/init-project` and `/gi` now verify correct repository

## 🆕 What's New in v2.7.0

### Task Ledger System 📋
- **Problem Solved**: Tasks scattered across multiple files, easy to lose progress
- **Task Ledger**: Single `.task-ledger.md` file tracks ALL tasks across features
- **Automatic Updates**: Hook system maintains it as you work
- **Persistent Progress**: Survives session restarts, included in gist saves
- **GitHub Integration**: Direct links between tasks and issues

### New Command
- `/task-ledger` (`/tl`) - View and manage task ledger
  - `/tl summary` - Quick stats overview
  - `/tl sync` - Sync with all task files
  - `/tl feature [name]` - Focus on specific feature

### Enhanced Workflows
- **Smart Resume**: Now shows task ledger summary
- **Task Commands**: `/ts`, `/tb`, `/pt` all use persistent ledger
- **Chains**: Updated daily-startup, task-sprint chains

## 🚀 Quick Start

You're working with an advanced AI-assisted development system that treats specifications (PRDs) as the primary development artifact. This follows Sean Grove's "The New Code" philosophy.

### First Commands
```bash
/sr                    # Smart Resume - restores full context
/help new              # See latest features
/cp load [profile]     # Load focused context
```

### One-Time Setup (2 minutes)
1. Install CodeRabbit extension in Cursor
2. Sign up at app.coderabbit.ai (free)
3. Select "Claude Code" as AI agent
4. Start coding with real-time review!

## 🌟 Latest Features

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

### Research Management (v2.3.5)
```bash
/research review        # See pending research docs
/research update        # Update existing instead of creating new
/research search auth   # Find past analysis
/research context       # Add relevant docs to current session
```

### CodeRabbit Integration (v2.3.4)
- **Real-Time Review** - Catch issues as you type, not after PR
- **One-Click Fixes** - Simple issues fixed automatically
- **Complex Fix Handoff** - Copy suggestions back to Claude
- **PR Status Command** - `/pr-feedback` for quick checks

### Hook System Enhancements (v2.3.3)
- **PreCompact Support** - Never lose context during long sessions
  - Automatically saves critical files before compaction
  - `/sr` restores everything after compaction
  - No more "Claude forgot what we were doing"
- **Suggestion Engine** - Learn from design violations
  - See: "You used 'text-sm' → Use 'text-size-3' instead"
  - Tracks your common mistakes
  - Educational explanations for each rule
- **Command Analytics** - Understand your workflow
  ```bash
  /query-logs --stats     # See command usage statistics
  /query-logs --errors    # Find what's failing
  /query-logs --sessions  # Analyze work sessions
  ```

### GitHub Apps Integration (v2.3.2)
- **CodeRabbit + Claude Code** for comprehensive AI reviews
- **Repository safety** - can't accidentally pollute boilerplate repo
- **Automated setup** - one script configures everything
- **Design enforcement** - AI learns and enforces your rules

### Workflow Enhancement (v2.3.1)
- **Smart Auto-Approval** - No more "Can I edit this file?" interruptions!
  - Read operations proceed automatically
  - Test file edits auto-approved
  - Safe commands (lint, test) run without prompts
  - Production code still protected

### Grove-Inspired Enhancements (v2.3.0)
1. **PRD Clarity Linter** - Catches ambiguous language automatically
2. **Specification Patterns** - Extract/reuse successful implementations (`/specs`)
3. **Test Generation** - PRD acceptance criteria → tests (`/prd-tests`)
4. **Implementation Grading** - Score alignment with PRD (`/grade`)

### Context Management (v2.2.0)
- **Context Profiles** - Focused work modes (`/cp`)
- **Bug Tracking** - Persistent across sessions (`/bt`)
- **Doc Cache** - Offline documentation (`/dc`)
- **Stage Gates** - Enforce completion (`/sv`)

## 🎯 Core Workflow

```
IDEA → /init-project → /prd → /prd-async → /gt → /pt → /grade → /fw complete
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
/sr                    # Resume where you left off (now with branch awareness)
/branch-status         # Check branch health (NEW)
/fw start [#]          # Start GitHub issue
/prd [name]            # Create specification
/prd-async [name]      # Add async requirements
/prd-tests [name]      # Generate test suite
/gt [name]             # Generate tasks
/pt [name]             # Process tasks (with real-time review)
/grade                 # Check alignment
/specs extract         # Save successful pattern
/feature-complete      # Mark feature as done (NEW)
/pr-feedback           # Quick PR status check
/research review       # Organize research docs
```

### Quality & Safety
```bash
/vd                    # Validate design
/validate-async        # Check async patterns (NEW)
/sv check              # Stage validation
/facts                 # Protected values
/exists [name]         # Check before creating
/bt add "bug"          # Track bugs
```

### Async Development (NEW)
```bash
/create-event-handler  # Create event handler
/test-async-flow       # Test event chains
```

## 🛡️ Automatic Protections

The system automatically:
- **Approves** safe operations (no more waiting!)
- **Blocks** design violations (wrong CSS classes)
- **Warns** about ambiguous PRD language
- **Detects** async anti-patterns (NEW)
- **Saves** context every 60 seconds
- **Prevents** PII exposure
- **Tracks** bugs persistently
- **Grades** implementation quality
- **Reviews** code in real-time (CodeRabbit)
- **Suggests** fixes before commit

## 💡 Key Principles

1. **Specifications are primary** - PRDs drive everything
2. **Clear communication** - Ambiguity is the enemy
3. **Automated enforcement** - Hooks handle compliance
4. **Pattern learning** - Success builds on success
5. **Objective quality** - Measurable alignment
6. **User experience first** - Never block on non-critical ops

## 🔑 Quick Reference

```
SPECIFICATIONS          DEVELOPMENT            QUALITY
/prd    - create       /cc  - component       /grade  - alignment
/prd-async - async     /vd  - design check    /sv     - stages
/specs  - patterns     /bt  - bug track       /btf    - browser
/prd-tests - tests     /validate-async        

CONTEXT                COLLABORATION          HELP
/sr     - resume       /fw  - workflow        /help new
/cp     - profiles     /orch - agents         /help [cmd]
/dc     - doc cache    /team - status         /?
/research - organize   

BRANCH MANAGEMENT      EVENTS                 REVIEW
/bs     - status       /create-event-handler  /pr-feedback
/fs     - features     /test-async-flow       CodeRabbit (IDE)
/sync   - sync main
/fc     - complete
```

## 🔑 Key Files

- `CLAUDE.md` - AI agent instructions
- `QUICK_REFERENCE.md` - All commands
- `RELEASES.md` - Release notes index
- `docs/releases/` - Detailed release notes
- `docs/updates/` - Feature enhancement docs
- `.claude/config.json` - System configuration

## 🎨 Design System

**Enforced automatically:**
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
/help workflows    # Common patterns
/help [command]    # Specific command
```

## 💭 Philosophy

> "The person who communicates most effectively is the most valuable programmer." - Sean Grove

This system helps you:
- Write clear specifications
- Generate code from intent
- Measure alignment objectively
- Learn from successes
- Collaborate seamlessly
- Build performant UIs

Ready to start? Try `/init-project` or `/sr` to resume existing work!
