# 🎯 Claude Code Quick Reference Card v2.7.0

> 🚀 **For complete workflow guide, see: [MASTER_WORKFLOW_GUIDE.md](../MASTER_WORKFLOW_GUIDE.md)**

## 🚀 Daily Flow - What Each Command Does
```bash
# Start day
/sr                     # Smart Resume - Restores all context (now shows branch health)
/cp load [profile]      # Load a saved context profile (e.g., "frontend", "backend")
/bt list                # Show all unresolved bugs you're tracking
/branch-status          # Check branch health and active work 🆕

# Feature work (with CodeRabbit real-time review)
/fw start [#]           # Start working on GitHub issue # (creates branch)
/prd [name]             # Create detailed Product Requirements Document
/prd-async [name]       # Add async requirements to PRD ⚡
/gt [name]              # Generate ~20 implementation tasks from PRD
/pt [name]              # Process tasks (CodeRabbit reviews as you code)
/sv check 1             # Validate that stage 1 requirements are met

# Create forms with tracking
/create-tracked-form ContactForm --vertical=standard --compliance=tcpa  # ⚡
# Options: --vertical=[debt|healthcare|standard] --compliance=[standard|hipaa|gdpr|tcpa]

# During work
/vd                     # Validate design - checks CSS classes & spacing
/validate-async         # Check async patterns compliance ⚡
/dmoff                  # Turn OFF design system - use any Tailwind classes
/dmon                   # Turn ON design system - back to strict mode
/bt add "bug"           # Track a bug to fix later
/dc search "topic"      # Search your cached documentation
/checkpoint             # Manually save current state (auto-saves every 60s)
/feature-status [name]  # Check if feature already exists 🆕
# CodeRabbit IDE      # Reviews automatically as you type in Cursor

# Complete stage
/sv require 1           # Block progress until stage 1 is complete
/feature-complete       # Mark feature as done and protected 🆕
/pr-feedback            # Quick PR status check (most issues already fixed)
/fw complete [#]        # Create PR that closes GitHub issue #

# Branch maintenance
/sync-main              # Safely sync main branch 🆕
/branch-clean           # Clean up merged branches 🆕
```

## 📊 Command Categories

### Context & State
- `/sr` - Smart Resume
- `/cp` - Context Profile (save/load/list)
- `/checkpoint` - Save progress
- `/compress` - Compress context

### Branch Management 🆕
- `/branch-status` (`/bs`) - Branch overview & health
- `/feature-status` (`/fs`) - Feature details & protection  
- `/sync-main` (`/sync`) - Sync main branch safely
- `/branch-switch` (`/switch`) - Smart branch switching
- `/branch-clean` (`/clean`) - Clean merged branches
- `/feature-complete` (`/fc`) - Mark feature as done

### Development
- `/cc` - Create component
  - `--wireframe` - ASCII layout first
  - `--animate` - Plan animations
- `/es` - Extract style from reference
- `/vd` - Validate design
- `/dm` - Design mode (on/off/custom/shadcn) 🆕
- `/fw` - Feature workflow
- `/bt` - Bug tracking (add/list/resolve)

### Async & Events ⚡ NEW
- `/create-event-handler [name]` - Create async event handler with retry logic
  - Example: `/create-event-handler pixel-fire`
- `/prd-async [feature]` - Add async requirements section to PRD
  - Defines critical vs non-critical operations
  - Specifies loading states and timeouts
- `/validate-async` - Check code for async anti-patterns
  - Sequential awaits that could be parallel
  - Missing loading states
  - Blocking analytics calls
- `/test-async-flow [form-name]` - Test complete event chain
- `/create-tracked-form [name] [options]` - Generate form with event tracking
  - `--vertical=[debt|healthcare|standard]`
  - `--compliance=[standard|hipaa|gdpr|tcpa]`

### Documentation
- `/dc` - Doc cache (cache/search/show)
- `/research-docs` - Research & cache
- `/research` - Organize internal research (NEW)
  - `review` - Review pending docs
  - `update` - Update existing research
  - `search` - Find past analysis
  - `context` - Add to current session
- `/create-prd-from-existing` - Generate PRD from existing code (NEW)
  - `prd-existing` - Short alias
  - `doc-existing` - Alternative alias

### Stage Control
- `/sv` - Stage validate (check/require/status)

### Analytics & Monitoring
- `/query-logs` - Query command history
  - `--stats` - View usage statistics
  - `--errors-only` - Find recent errors
  - `--command /cc` - Filter by command
  - `--min-duration 5000` - Find slow operations
  - `--sessions` - View session analysis
- `/check-work` - Quick quality check
  - `versions` - Check version consistency
  - `todos` - Find incomplete work
  - `imports` - Validate imports
- `/prd` - PRD with stage gates

### Testing
- `/btf` - Browser test flow
- `/tr` - Test runner

### Code Review
- `/pr-feedback` - Quick PR status check
- CodeRabbit IDE - Real-time review in Cursor

### Multi-Agent
- `/orch` - Orchestrate agents
- `/persona` - Switch persona
- `/sas` - Agent status

## ⚡ Async Event Patterns (v2.3.6)

### Fire-and-Forget Pattern
```typescript
// ❌ OLD - Blocks user
await analytics.track('Form Submit');
await sendWebhook(data);

// ✅ NEW - Non-blocking
eventQueue.emit(LEAD_EVENTS.FORM_SUBMIT, data);
```

### When to Use Each
**Use `await` for:**
- API submissions
- Payment processing  
- Authentication
- Data user needs to see

**Use `eventQueue.emit()` for:**
- Analytics (Rudderstack, GA)
- Marketing pixels
- Webhooks
- Email notifications
- Audit logs

### Loading States Required
```typescript
// Hook enforces this pattern
const [isSubmitting, setIsSubmitting] = useState(false);
// Must show loading state during async operations
```

## 🆕 New Features (v2.3.6)
- **Async Event System**: Fire-and-forget for non-critical operations
- **Automatic Rudderstack Bridge**: Events auto-convert to track() calls
- **Form Event Tracking**: Built-in hooks for lead generation
- **Parallel Detection**: Warns about sequential awaits
- **Required Loading States**: Every async op needs user feedback
- **Timeout Protection**: All external calls have 5s default timeout

## 🔄 Previous Features (v2.3.5)
- **Design System Toggle**: `/dmoff` to disable, `/dmon` to enable
- **Research Management**: Smart doc updates, no more v1/v2/v3 versions

## 🔑 Key Files
- `docs/project/PROJECT_PRD.md` - Vision
- `docs/project/features/*` - Feature PRDs
- `.claude/orchestration/*` - Agent plans
- `.claude/bugs/active.json` - Open bugs
- `.claude/profiles/*` - Context profiles

## 💡 Remember
- Context auto-saves every 60s
- Design violations blocked automatically
- Everything tracked in GitHub issues
- Bugs persist across sessions
- Stage gates prevent incomplete work
- CodeRabbit reviews code in real-time
- Clean code before commits = faster PRs
