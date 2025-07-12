# 🎯 Claude Code Quick Reference Card

## 🚀 Daily Flow
```bash
# Start day
/sr                     # Resume context (ALWAYS FIRST!)

# Feature work
/fw start [#]           # Start issue
/prd [name]             # Create feature PRD
/gt [name]              # Generate tasks
/pt [name]              # Process tasks

# During work
/vd                     # Validate design
/todo add "note"        # Quick reminders
/checkpoint             # Manual save

# Complete
/fw complete [#]        # Create PR
```

## 📊 Command Categories

### Context & State
- `/sr` - Smart Resume
- `/checkpoint` - Save progress
- `/compress` - Compress context

### Development
- `/cc` - Create component
  - `--wireframe` - ASCII layout first
  - `--animate` - Plan animations
- `/es` - Extract style from reference
- `/vd` - Validate design
- `/fw` - Feature workflow

### Testing
- `/btf` - Browser test flow
- `/tr` - Test runner

### Multi-Agent
- `/orch` - Orchestrate agents
- `/persona` - Switch persona
- `/sas` - Agent status

## 🔑 Key Files
- `docs/project/PROJECT_PRD.md` - Vision
- `docs/project/features/*` - Feature PRDs
- `.claude/orchestration/*` - Agent plans

## 💡 Remember
- Context auto-saves every 60s
- Design violations blocked automatically
- Everything tracked in GitHub issues
