---
name: spawn-agent
description: |
  [DEPRECATED] Use native Claude Code agents instead.
  This command is deprecated in favor of using native agents directly.
  See /agents for managing native agents or /orchestrate for multi-agent tasks.
argument-hint: <persona> [options]
aliases: ["spawn"]
---

# ⚠️ DEPRECATED: Spawn Agent Command

## 🚨 This command is deprecated!

The persona spawning system has been replaced with Claude Code's native agent system, which provides:
- Better performance through isolated contexts
- Automatic agent activation based on task context
- Built-in agent management with `/agents`
- Native orchestration support

## 🔄 Migration Guide

### Instead of spawning agents:

**OLD WAY** (Deprecated):
```bash
/spawn-agent frontend --tasks=2.1,2.2 --feature=user-auth
```

**NEW WAY** (Recommended):
```bash
# For single agent work:
Use the frontend-ux-specialist agent to implement the login form component

# For multi-agent orchestration:
/orchestrate user authentication system
```

### Available Native Agents

We have 36 specialized native agents already available:
- `frontend-ux-specialist` - UI/UX development
- `backend` - Server and API development
- `security-threat-analyst` - Security reviews
- `database-architect` - Data modeling
- `qa` - Testing and quality assurance
- And 31 more specialized agents!

Use `/agents` to see and manage all available agents.

### Why This Change?

1. **Native Integration**: Leverages Claude Code's built-in features
2. **Better Performance**: Each agent has isolated context
3. **Automatic Activation**: Agents activate based on task context
4. **Simplified Workflow**: No manual spawning needed

### Need Help?

- View all agents: `/agents`
- Orchestrate multiple agents: `/orchestrate <task>`
- Get help: `/help agents`

## ⏰ Deprecation Timeline

This command will be removed in 6 months. Please update your workflows to use native agents.

---

*Original spawn functionality preserved below for reference during transition period:*

$ARGUMENTS