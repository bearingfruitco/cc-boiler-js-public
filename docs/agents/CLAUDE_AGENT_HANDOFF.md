# Claude Agent Handoff - Boilerplate System Context

## Project Overview
You're working on a sophisticated Claude Code boilerplate system located at:
`/Users/shawnsmith/dev/bfc/boilerplate`

This is an AI-powered development system with:
- 71 custom hooks for automation
- 120+ custom commands
- 32 command chains (workflows)
- 180+ aliases
- Comprehensive configuration system

## Current Status
✅ **WORKING**: All 71 hooks are enabled and functioning
✅ **FIXED**: The matcher format issue (`{}` → `""`) has been resolved
✅ **ORGANIZED**: Project was just cleaned up, docs moved to `/docs/`
⚠️ **NEEDS ATTENTION**: Elements from backup need to be restored to active `.claude`

## Immediate Task
Compare `.claude.full_backup_20250727_102756/` with `.claude/` and restore any missing elements that should be active. The backup contains the complete original system.

## Key Documentation to Read

### In Project Root:
1. **CLAUDE.md** - Main Claude documentation
2. **docs/CLEANUP_SUMMARY.md** - What was just organized

### Critical Troubleshooting Docs:
1. **docs/claude-fixes/CLAUDE_HOOKS_TROUBLESHOOTING_GUIDE.md** - Complete troubleshooting guide
2. **docs/claude-fixes/CLAUDE_HOOKS_FIX_COMPLETE.md** - Detailed fix history

### Quick Status Check:
```bash
python3 .claude/audit-system-complete.py
```

## Key Technical Context

### The Hook System
- **Problem we solved**: Hooks had `"matcher": {}` instead of `"matcher": ""`
- **Solution**: All matchers are now strings per Anthropic documentation
- **Current state**: 71 hooks across 7 event types all working

### Hook Event Types:
- PreToolUse (35 hooks)
- PostToolUse (17 hooks)
- Notification (9 hooks)
- Stop (5 hooks)
- SubagentStop (1 hook)
- PreCompact (2 hooks)
- UserPromptSubmit (2 hooks)

### Important Scripts:
- `.claude/audit-system-complete.py` - Full system audit
- `.claude/troubleshooting/fix-matcher-format.py` - Fixes the matcher issue
- `.claude/troubleshooting/enable-all-hooks-complete-final.py` - Enables all 71 hooks

## What to Check in Backup vs Active

Compare these directories:
```bash
# Scripts directory
ls .claude.full_backup_20250727_102756/scripts/
ls .claude/scripts/

# Any subdirectories in commands
find .claude.full_backup_20250727_102756/commands -type d
find .claude/commands -type d

# Check for any unique files
diff -r .claude.full_backup_20250727_102756/ .claude/
```

## Known Issues Already Fixed
1. **Worktree command** - Was in subdirectory, created wrapper at root level
2. **Missing scripts** - Already restored 13 scripts from backup
3. **Command references** - Fixed: spawn→spawn-agent, test-security→security-check

## Project Structure
```
.claude/
├── settings.json (71 hooks configured)
├── chains.json (32 workflows)
├── aliases.json (180+ shortcuts)
├── config.json (main config)
├── commands/ (120+ commands)
├── hooks/ (all hook files)
├── scripts/ (utility scripts)
├── troubleshooting/ (fix scripts)
└── backups/ (organized backups)
```

## Official Documentation Context
The hook system follows Anthropic's official Claude Code hooks documentation:
- Matchers must be strings (not objects)
- Event names are capitalized (PreToolUse, not preToolUse)
- Hooks receive JSON input and can control tool execution

## Next Steps After Restoration
1. Run `python3 .claude/audit-system-complete.py` to verify system
2. Check for any remaining missing elements
3. Test a hook in Claude Code (Ctrl+R for transcript mode)
4. Document any additional restorations made

## If You Encounter Issues
1. Check the troubleshooting guide first
2. The matcher format (`{}` vs `""`) was the main issue - already fixed
3. Use scripts in `.claude/troubleshooting/` for diagnostics
4. Full backup is at `.claude.full_backup_20250727_102756/`

The system is sophisticated but currently working. Focus on comparing backup with active directory and restoring any missing components that should be active.
