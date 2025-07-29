# Boilerplate Update Tracking & Migration System

## Overview

When updating the boilerplate system while projects are using it, we need a systematic way to:
1. Track what changed in boilerplate
2. Identify which changes apply to existing projects
3. Safely migrate projects to new boilerplate versions

## Quick Solution: Update Commands

### For the debt-tofu-report project:

```bash
# In debt-tofu-report directory
/boilerplate-sync

# Or manually:
git remote add boilerplate https://github.com/[your-boilerplate-repo]
git fetch boilerplate
git cherry-pick [specific commits]
```

## Comprehensive Tracking System

### 1. Boilerplate Change Log

Create a change log that tracks all significant updates:

<function_calls>
<invoke name="filesystem:write_file">
<parameter name="content"># Boilerplate Changelog

## [2024-01-15] Architecture-Driven Development

### New Commands
- `/create-architecture` - Generate complete architecture from PRD
- `/validate-architecture` - Validate architecture completeness
- `/architecture-viz` - Create architecture visualizations
- `/generate-component-prps` - Auto-generate PRPs from architecture

### New Agents
- `prp-writer` - Specialized PRP creation agent

### New Scripts
- `scripts/validate-architecture.py`
- `scripts/visualize-architecture.py`
- `scripts/generate-component-prps.py`

### New Hooks
- `04a-architecture-suggester.py` - Architecture workflow suggestions

### Modified Files
- `.claude/command-registry.json` - Added new commands
- `.claude/aliases.json` - Added shortcuts
- `.claude/agents/QUICK_REFERENCE.md` - Updated agent list

### Migration Required
- Projects should run `/create-architecture` after PRD
- Existing PRPs remain compatible
- No breaking changes

---

## [2024-01-10] TDD Dashboard System

### New Commands
- `/tdd-dashboard` - TDD metrics visualization
- `/tdd-status` - Current TDD status
- `/tdd-coverage` - Coverage reports

### Migration Required
- Optional - adds enhanced TDD tracking

---

## Template for New Entries

## [DATE] Feature Name

### New Commands
- List new commands and their purposes

### New/Modified Files
- List all files added or significantly changed

### Breaking Changes
- Any incompatible changes

### Migration Required
- Steps to update existing projects
- Whether update is mandatory or optional
