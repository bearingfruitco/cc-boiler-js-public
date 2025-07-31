---
name: spawn-agent
description: |
  [DEPRECATED] Use native Claude Code agents instead.
  This command is deprecated in favor of using native agents directly.
  See 'Use the [agent-name] agent' pattern or /orchestrate for multi-agent tasks.
argument-hint: <persona> [options]
aliases: ["spawn"]
---

# ⚠️ DEPRECATED: Spawn Agent Command

## 🚨 This command is deprecated!

The persona spawning system has been replaced with Claude Code's native agent system, which provides:
- Better performance through isolated contexts
- Automatic agent activation based on task context  
- Built-in agent management
- Native orchestration support

## 🔄 Migration Guide

### Persona to Native Agent Mapping:

| Old Persona | Native Agent | Usage |
|------------|--------------|--------|
| frontend | frontend | `Use the frontend agent to...` |
| backend | backend | `Use the backend agent to...` |
| security | security | `Use the security agent to...` |
| qa | qa | `Use the qa agent to...` |
| architect | system-architect | `Use the system-architect agent to...` |
| performance | performance | `Use the performance agent to...` |
| integrator | integration-specialist | `Use the integration-specialist agent to...` |
| data | database-architect | `Use the database-architect agent to...` |
| analyzer | analyzer | `Use the analyzer agent to...` |
| refactorer | refactoring-expert | `Use the refactoring-expert agent to...` |
| devops | platform-deployment | `Use the platform-deployment agent to...` |
| mentor | mentor | `Use the mentor agent to...` |

### Instead of spawning agents:

**OLD WAY** (Deprecated):
```bash
/spawn-agent frontend --tasks=2.1,2.2 --feature=user-auth
/spawn frontend  # short alias
/persona frontend
```

**NEW WAY** (Recommended):
```bash
# For single agent work, just say:
Use the frontend agent to implement the login form component

# For multi-agent orchestration:
/orchestrate user authentication system
```

### Key Differences:

1. **No Manual Spawning**: Agents activate automatically when mentioned
2. **Natural Language**: Use "Use the [agent-name] agent to..." pattern
3. **Context Isolation**: Each agent has its own clean context
4. **Better Performance**: Native Claude Code optimization
5. **Simpler Workflow**: No complex spawn parameters

### Available Native Agents

We have 36+ specialized native agents:
- `frontend` - UI/UX development
- `backend` - Server and API development  
- `security` - Security reviews
- `database-architect` - Data modeling
- `qa` - Testing and quality assurance
- `system-architect` - Architecture design
- `supabase-specialist` - Supabase integration
- `orm-specialist` - Database query optimization
- `migration-specialist` - Database migrations
- `ui-systems` - Design system components
- And many more!

### Backward Compatibility

For the next 6 months, this command will:
1. Show this deprecation notice
2. Suggest the equivalent native agent
3. Provide the correct usage pattern

After that, the command will be removed entirely.

## 💡 Quick Examples

```bash
# Instead of: /spawn frontend
Use the frontend agent to build the dashboard component

# Instead of: /spawn-agent backend --feature=api
Use the backend agent to implement the REST API endpoints

# Instead of: /spawn security --audit
Use the security agent to audit the authentication flow

# For complex tasks with multiple agents:
/orchestrate complete user management system with auth, UI, and database
```

## 📚 Learn More

- See all agents: Check `.claude/agents/` directory
- Multi-agent work: Use `/orchestrate`
- Agent docs: Each agent has detailed documentation in their file

---

**Note**: If you see this message, please update your workflow to use native agents directly. The spawn system is no longer maintained.