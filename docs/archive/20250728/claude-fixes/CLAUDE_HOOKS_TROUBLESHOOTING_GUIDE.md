# Claude Code Hooks System - Complete Troubleshooting Guide

## Quick Start for New Claude Agents

**If hooks are broken, start here:**

1. The most common issue is `"matcher": {}` (empty object) instead of `"matcher": ""` (empty string)
2. Check the complete fix documentation at: `CLAUDE_HOOKS_FIX_COMPLETE.md`
3. Use the scripts in `.claude/` directory to diagnose and fix

## Common Error and Solution

### The Error
```
⚠ Found invalid settings files. They will be ignored. Run /doctor for details.
ERROR  Cannot assign to read only property '0' of object '[object String]'
```

### The Root Cause
The hooks configuration uses incorrect matcher format:
- ❌ Wrong: `"matcher": {}`
- ✅ Correct: `"matcher": ""`

### Quick Fix
```bash
# Run the fix script that already exists
python3 .claude/fix-matcher-format.py
cp .claude/settings-fixed.json .claude/settings.json
claude doctor
```

## Complete System Overview

### What This System Contains
- **71 Hooks** across 7 event types (PreToolUse, PostToolUse, Notification, Stop, SubagentStop, PreCompact, UserPromptSubmit)
- **32+ Command Chains** for complex workflows
- **180+ Aliases** for quick command access
- **120+ Custom Commands** in `.claude/commands/`
- **13 Scripts** in `.claude/scripts/`
- **Comprehensive configuration** in `config.json`

### Key Directories
```
.claude/
├── hooks/
│   ├── pre-tool-use/      (35 hooks)
│   ├── post-tool-use/     (17 hooks)
│   ├── notification/      (9 hooks)
│   ├── stop/              (5 hooks)
│   ├── sub-agent-stop/    (1 hook)
│   ├── pre-compact/       (2 hooks)
│   ├── user-prompt-submit/(2 hooks)
│   └── utils/             (shared utilities)
├── commands/              (120+ commands)
│   ├── worktree/         (subdirectory commands)
│   ├── git-operations/
│   └── ...
├── scripts/              (13 utility scripts)
├── settings.json         (hooks configuration)
├── chains.json          (command chains)
├── aliases.json         (command shortcuts)
└── config.json          (main configuration)
```

## Troubleshooting Steps

### 1. Diagnosing Hook Issues

```bash
# Check if settings are valid
claude doctor

# Run comprehensive audit
python3 .claude/audit-system-complete.py

# Test hooks individually
python3 .claude/test-hooks-individually-fixed.py
```

### 2. Common Issues and Fixes

#### Issue: "Invalid settings files" error
```bash
# Fix matcher format
python3 .claude/fix-matcher-format.py
cp .claude/settings-fixed.json .claude/settings.json
```

#### Issue: Missing hooks (less than 71 active)
```bash
# Enable all hooks
python3 .claude/enable-all-hooks-complete-final.py
cp .claude/settings-all-hooks-final-complete.json .claude/settings.json
```

#### Issue: Missing commands in chains
```bash
# Fix command references
python3 .claude/fix-missing-commands.py

# Common fixes:
# - spawn → spawn-agent or spawn-security-auditor
# - test-security → security-check
# - Commands in subdirectories need full path or wrapper
```

#### Issue: Broken aliases
```bash
# Check which aliases are broken
python3 .claude/audit-system-complete.py

# Fix worktree aliases specifically
python3 .claude/fix-worktree-aliases.py
```

#### Issue: Missing scripts directory
```bash
# Restore from backup
cp -r .claude.full_backup_*/scripts .claude/
```

### 3. Recovery Procedures

#### Minimal Working State
```bash
# If everything is broken, start with minimal config
cat > .claude/settings.json << 'EOF'
{
  "permissions": {
    "file_system": {"read": true, "write": true},
    "shell": {"execute": true}
  }
}
EOF
```

#### Restore from Backup
```bash
# Check for backups
ls -la .claude*backup*

# Restore complete system
cp -r .claude.full_backup_*/* .claude/
# Then fix the matcher format issue
python3 .claude/fix-matcher-format.py
```

## Verification Steps

### 1. Check Hook Count
Should show 71 total hooks:
- PreToolUse: 35
- PostToolUse: 17
- Notification: 9
- Stop: 5
- SubagentStop: 1
- PreCompact: 2
- UserPromptSubmit: 2

### 2. Test Hook Execution
```bash
claude
# Press Ctrl+R for transcript mode
# Type: read README.md
# Should see hooks executing
```

### 3. Verify All Components
```bash
python3 .claude/final-system-audit.py
```

## Key Scripts for Troubleshooting

1. **fix-matcher-format.py** - Fixes the empty object matcher issue
2. **test-hooks-individually-fixed.py** - Tests each hook one by one
3. **enable-all-hooks-complete-final.py** - Enables all 71 hooks
4. **audit-system-complete.py** - Complete system audit
5. **fix-missing-commands.py** - Fixes command references
6. **fix-worktree-aliases.py** - Fixes worktree command aliases

## Understanding the Matcher Format

### Official Documentation
According to Anthropic docs, matchers must be strings:
- `""` - Empty string matches all tools
- `"Bash"` - Matches specific tool
- `"Edit|Write"` - Regex pattern
- `"Read(node_modules/**)"` - With gitignore patterns

### The Critical Fix
Always ensure:
```json
{
  "matcher": "",  // ✅ String type
  "hooks": [...]
}
```

Never:
```json
{
  "matcher": {},  // ❌ Object type
  "hooks": [...]
}
```

## For Future Agents - Complete Fix Process

1. **Check current status:**
   ```bash
   cd /Users/shawnsmith/dev/bfc/boilerplate
   claude doctor
   python3 .claude/audit-system-complete.py
   ```

2. **If hooks are broken:**
   ```bash
   python3 .claude/fix-matcher-format.py
   python3 .claude/enable-all-hooks-complete-final.py
   cp .claude/settings-all-hooks-final-complete.json .claude/settings.json
   ```

3. **If commands are missing:**
   ```bash
   python3 .claude/fix-missing-commands.py
   python3 .claude/fix-worktree-aliases.py
   ```

4. **Verify everything:**
   ```bash
   claude doctor
   python3 .claude/final-system-audit.py
   ```

## Success Criteria

When fully operational:
- ✅ 71 hooks active
- ✅ No "invalid settings" errors  
- ✅ All chain commands exist
- ✅ All aliases work
- ✅ Scripts directory present
- ✅ Hooks execute in transcript mode

## Important Files

- **CLAUDE_HOOKS_FIX_COMPLETE.md** - Detailed documentation of the fix
- **.claude.full_backup_*/** - Complete system backup
- **.claude/settings-all-hooks-final-complete.json** - Working configuration with all hooks
- **.claude/command-registry.json** - Registry of all commands and locations

This system is sophisticated with auto-approval, security checks, TDD enforcement, task tracking, and much more. When working properly, it significantly enhances Claude Code's capabilities.
