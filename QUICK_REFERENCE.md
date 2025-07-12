# 🎯 Claude Code Quick Reference Card

## 🚀 Daily Flow
```bash
# Start day
/sr                     # Resume context (ALWAYS FIRST!)
/cp load [profile]      # Load context profile
/bt list                # Check open bugs

# Feature work
/fw start [#]           # Start issue
/prd [name]             # Create feature PRD
/gt [name]              # Generate tasks
/pt [name]              # Process tasks
/sv check 1             # Validate stage

# During work
/vd                     # Validate design
/bt add "bug"           # Track bugs
/dc search "topic"      # Search cached docs
/checkpoint             # Manual save

# Complete stage
/sv require 1           # Enforce stage gate
/fw complete [#]        # Create PR
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
