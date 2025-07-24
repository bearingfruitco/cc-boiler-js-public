# Agent OS Standards Integration Guide

## What We've Added

### 1. Centralized Standards Directory
Location: `.agent-os/standards/`

Files created:
- `design-system.md` - Your strict design rules (4 sizes, 2 weights, 4px grid)
- `tech-stack.md` - Your default technology choices
- `best-practices.md` - Your development philosophy and patterns

### 2. Standards-Aware Hook
Created: `.claude/hooks/pre-tool-use/02-design-check-standards.py`

This enhanced version:
- Reads design rules from `design-system.md` instead of hardcoding
- Falls back to hardcoded rules if file doesn't exist
- Maintains exact same behavior and compliance with Claude Code hooks

### 3. Enhanced Smart Resume
Created: `.claude/commands/smart-resume-standards.md`

Enhancements:
- Loads standards files on resume
- Shows standards in context summary
- Makes standards available to subsequent commands

## Integration Benefits

1. **Single Source of Truth**: Update design rules in one place
2. **Cross-Tool Compatibility**: Standards work in Claude Code, Cursor, any tool
3. **Team Alignment**: Everyone reads from same standards
4. **Easy Updates**: Change rules without modifying code
5. **No Disruption**: All existing workflows continue unchanged

## What Stays The Same

- ✅ All 113+ commands work exactly as before
- ✅ PRD/PRP/TDD workflows unchanged
- ✅ Task ledger system unchanged
- ✅ All validation and grading unchanged
- ✅ Event system unchanged
- ✅ All other hooks unchanged

## Activation Steps

### Option 1: Test First (Recommended)
1. Keep existing hook active: `02-design-check-simple.py`
2. Test new hook separately: `python 02-design-check-standards.py`
3. When satisfied, swap them

### Option 2: Direct Swap
1. Rename old hook: `mv 02-design-check-simple.py 02-design-check-simple.py.backup`
2. Rename new hook: `mv 02-design-check-standards.py 02-design-check-simple.py`

### Option 3: Use Aliases
Update `.claude/aliases.json`:
```json
{
  "sr": "smart-resume-standards",
  // ... rest of aliases
}
```

## No Configuration Changes Needed

- ❌ No changes to `settings.json`
- ❌ No changes to `config.json`
- ❌ No changes to chains (unless you want to)
- ❌ No changes to other hooks
- ❌ No changes to workflows

## Optional Chain Enhancement

If you want chains to load standards:

```json
// .claude/chains.json - Add ONE new chain
{
  "daily-startup-standards": {
    "description": "Start day with standards loaded",
    "steps": [
      "Load .agent-os/standards/*",
      "/sr",
      "/ts",
      "/branch-status"
    ]
  }
}
```

## Usage

1. **View Standards**: 
   ```bash
   cat .agent-os/standards/design-system.md
   ```

2. **Update Standards**:
   ```bash
   # Edit the file directly
   # Changes take effect immediately
   # No restart needed
   ```

3. **Check Hook is Reading Standards**:
   ```bash
   # The hook will now show:
   # 📖 See: .agent-os/standards/design-system.md
   ```

## Migration Path

Week 1: Run in parallel, test thoroughly
Week 2: Switch to standards-based hook
Week 3: Update other hooks to read from standards (optional)
Week 4: Consider adding product-level docs (optional)

## Summary

This minimal integration:
- Adds centralized standards without disrupting anything
- Enhances ONE hook to read from standards
- Provides optional enhanced smart resume
- Requires ZERO configuration changes
- Works immediately with fallbacks
- Can be rolled back instantly
