# 🎯 Claude Code Quick Reference Card

## 🚀 Daily Flow - What Each Command Does
```bash
# Start day
/sr                     # Smart Resume - Restores all context from last session
/cp load [profile]      # Load a saved context profile (e.g., "frontend", "backend")
/bt list                # Show all unresolved bugs you're tracking

# Feature work
/fw start [#]           # Start working on GitHub issue # (creates branch)
/prd [name]             # Create detailed Product Requirements Document
/gt [name]              # Generate ~20 implementation tasks from PRD
/pt [name]              # Process tasks one by one with auto-testing
/sv check 1             # Validate that stage 1 requirements are met

# During work
/vd                     # Validate design - checks CSS classes & spacing
/bt add "bug"           # Track a bug to fix later
/dc search "topic"      # Search your cached documentation
/checkpoint             # Manually save current state (auto-saves every 60s)

# Complete stage
/sv require 1           # Block progress until stage 1 is complete
/fw complete [#]        # Create PR that closes GitHub issue #
```

## 📊 Command Categories

### Context & State
- `/sr` - Smart Resume
- `/cp` - Context Profile (save/load/list)
- `/checkpoint` - Save progress
- `/compress` - Compress context

### Development
- `/cc` - Create component
  - `--wireframe` - ASCII layout first
  - `--animate` - Plan animations
- `/es` - Extract style from reference
- `/vd` - Validate design
- `/fw` - Feature workflow
- `/bt` - Bug tracking (add/list/resolve)

### Documentation
- `/dc` - Doc cache (cache/search/show)
- `/research-docs` - Research & cache

### Stage Control
- `/sv` - Stage validate (check/require/status)
- `/prd` - PRD with stage gates

### Testing
- `/btf` - Browser test flow
- `/tr` - Test runner

### Multi-Agent
- `/orch` - Orchestrate agents
- `/persona` - Switch persona
- `/sas` - Agent status

## 🆕 New Features
- **Context Profiles**: Switch between focused work modes
- **Bug Tracking**: Persistent across sessions
- **Doc Cache**: Offline documentation access
- **Stage Gates**: Enforce completion criteria
- **PRD Clarity**: Catches ambiguous language (`/prd` with linting)
- **Pattern Library**: Reuse successful specs (`/specs`)
- **Test Generation**: PRD → Tests (`/prd-tests`)
- **Implementation Grading**: Score alignment (`/grade`)

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
