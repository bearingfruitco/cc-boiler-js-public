---
title: Complete Command Reference Documentation
labels: documentation, enhancement, priority:high, help wanted
assignees: ''
---

## 📋 Description

Create a comprehensive reference guide for all 116+ commands in the Claude Code Boilerplate system, organized by category with examples and use cases.

## 🎯 Acceptance Criteria

- [ ] All commands documented with consistent format
- [ ] Commands organized by logical categories
- [ ] Each command includes syntax, parameters, examples
- [ ] Aliases and shortcuts clearly indicated
- [ ] Common command combinations documented
- [ ] Search/navigation friendly format

## 📝 Tasks

### 1. Audit All Commands
- [ ] Count total commands: `ls -1 .claude/commands/*.md | wc -l`
- [ ] Create spreadsheet of all commands with:
  - Command name
  - Aliases
  - Category
  - One-line description
  - Dependencies

### 2. Create Command Categories

**Suggested Categories**:
- **Context Management** (sr, cp, checkpoint, compress)
- **Development** (cc, vd, fw, prd, prp)
- **Testing** (tr, tdd, btf, validate)
- **Orchestration** (orch, spawn, chain, persona)
- **Git/GitHub** (cti, branch, sync)
- **Debugging** (debug, analyze, trace)
- **Security** (sec, audit, pii)
- **Performance** (perf, optimize, monitor)
- **Documentation** (doc, help, examples)
- **Utility** (todo, metrics, clean)

### 3. Document Each Command

**Template for each command**:
```markdown
## /command-name (aliases: /alias1, /alias2)

**Category**: Development  
**Added**: v2.3.0  
**Requires**: [any prerequisites]

### Description
Brief description of what the command does and when to use it.

### Syntax
```
/command-name [required] <optional> --flag
```

### Parameters
- `required` - Description of required parameter
- `<optional>` - Description of optional parameter
- `--flag` - Description of flag

### Examples
```bash
# Basic usage
/command-name feature-x

# With options
/command-name feature-x --verbose

# Common workflow
/fw start 123
/create-prp feature-x
/prp-execute feature-x
```

### Related Commands
- `/related1` - How it relates
- `/related2` - How it relates

### Notes
Any special considerations, tips, or warnings.
```

### 4. Create Quick Reference Card

**File**: `/docs/commands/QUICK_REFERENCE.md`
- [ ] One-line description for each command
- [ ] Organized by frequency of use
- [ ] Printable cheat sheet format

### 5. Create Power User Guide

**File**: `/docs/commands/POWER_USER.md`
- [ ] Advanced command combinations
- [ ] Workflow automation examples
- [ ] Custom aliases setup
- [ ] Performance tips

### 6. Add Search Functionality

- [ ] Create command index with tags
- [ ] Add "common tasks" mapping to commands
- [ ] Include troubleshooting command map

## 🔗 Example Commands to Document

Priority commands that need immediate documentation:
- `/sr` - Smart Resume
- `/cc` - Create Component  
- `/fw` - Feature Workflow
- `/prp` - Product Requirement Prompt
- `/orch` - Orchestrate Agents
- `/chain` - Run Automation Chain
- `/vd` - Validate Design
- `/cti` - Capture to Issue

## ⏱️ Time Estimate

4 hours (can be split among multiple contributors)

## 🏷️ Labels

- documentation
- enhancement
- priority: high
- help wanted

## 💡 Tips for Contributors

- Start with the most frequently used commands
- Test each command before documenting
- Include real-world examples
- Note any version-specific features
- Cross-reference related commands
