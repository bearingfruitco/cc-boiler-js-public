# Sub-Agents Terminology Update Guide

> Aligning our agent system with official Claude Code sub-agents terminology

## Overview

Our system already uses the **exact same format** as official Claude Code sub-agents. The main update needed is terminology alignment in documentation.

## Terminology Changes

| Our Current Term | Official Term | Update Needed |
|------------------|---------------|---------------|
| "agents" | "sub-agents" | Documentation only |
| "spawn" | "invoke" or "delegate" | Command descriptions |
| "31 agents" | "31 sub-agents" | All references |

## What Stays the Same ✅

1. **File Format** - Already correct YAML frontmatter
2. **File Location** - Already in `.claude/agents/`
3. **Tools Field** - Already comma-separated
4. **Descriptions** - Already encourage proactive use

## Documentation Updates Needed

### 1. AGENT_USAGE_GUIDE.md
```diff
- # Agent Usage Quick Reference
+ # Sub-Agent Usage Quick Reference

- This guide helps you choose the right agent for your task.
+ This guide helps you choose the right sub-agent for your task.
```

### 2. Command Descriptions
Update command files to use "sub-agent" terminology:
- `/spawn` command docs
- `/agent` shortcuts
- `/orchestrate` descriptions

### 3. Main Documentation
- README.md - Update agent references
- SYSTEM_OVERVIEW.md - Use sub-agent terminology
- QUICK_REFERENCE.md - Update descriptions

## Sub-Agent Best Practices (from Official Docs)

### 1. Start with Claude
> "We highly recommend generating your initial sub-agent with Claude and then iterating on it to make it personally yours."

Our approach aligns perfectly - we provide templates that users can customize.

### 2. Focused Purpose
> "Create sub-agents with single, clear responsibilities"

✅ Our 31 sub-agents each have specific roles.

### 3. Detailed Prompts
> "Include specific instructions, examples, and constraints"

✅ All our sub-agents have comprehensive system prompts.

### 4. Limited Tool Access
> "Only grant tools that are necessary"

✅ Each sub-agent has minimal required tools.

## Integration with Official `/agents` Command

Users can manage our pre-built sub-agents with the official command:

```bash
/agents              # Opens official manager
# Shows all 31 pre-built sub-agents
# Can edit, delete, or create new ones
```

Our shortcuts still work for productivity:
```bash
/spawn backend      # Quick invocation
/be                # Even shorter
```

## Migration Script

To update all documentation automatically:

```bash
#!/bin/bash
# Update agent → sub-agent in docs
find docs/ -name "*.md" -exec sed -i 's/\bagent\b/sub-agent/g' {} \;
find docs/ -name "*.md" -exec sed -i 's/\bAgent\b/Sub-agent/g' {} \;
find docs/ -name "*.md" -exec sed -i 's/\bagents\b/sub-agents/g' {} \;
find docs/ -name "*.md" -exec sed -i 's/\bAgents\b/Sub-agents/g' {} \;

# Update in .claude directory
find .claude/ -name "*.md" -exec sed -i 's/\b31 agents\b/31 sub-agents/g' {} \;

echo "Terminology updated to match official docs!"
```

## Summary

Our system is **already 100% compatible** with official sub-agents. We just need to:

1. Update terminology in documentation
2. Reference official `/agents` command
3. Keep our productivity shortcuts

No functional changes needed - just documentation alignment!
