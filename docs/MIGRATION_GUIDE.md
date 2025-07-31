# Claude Code Boilerplate Migration Guide

This guide helps you migrate from the previous persona-based system to the new native Claude Code agent system.

## Overview of Changes

### 🔄 Major Updates

1. **Native Agent System**: Replaced custom persona spawning with Claude Code's native agents
2. **Non-Interactive Mode**: Added CI/CD support with `--non-interactive` flag
3. **Smart Chains**: Enhanced chains with triggers, prerequisites, and context
4. **Consolidated Security**: Single comprehensive security hook
5. **Improved Documentation**: Complete guides for all features

## Migration Steps

### Step 1: Update Commands

#### Persona → Agent Mapping

| Old Command | New Command | Notes |
|-------------|-------------|-------|
| `/spawn frontend` | `Use the frontend agent` | Natural language invocation |
| `/persona backend` | `Use the backend agent` | No parameters needed |
| `/spawn-agent security` | `Use the security agent` | Automatic context |
| `/p qa` | `Use the qa agent` | Simplified syntax |

#### Specific Agent Mappings

| Old Persona | Native Agent | Purpose |
|-------------|--------------|---------|
| `frontend` | `frontend` | UI/UX development |
| `backend` | `backend` | Server and API development |
| `security` | `security` | Security reviews |
| `qa` | `qa` | Testing and quality assurance |
| `architect` | `system-architect` | Architecture design |
| `performance` | `performance` | Performance optimization |
| `integrator` | `integration-specialist` | External integrations |
| `data` | `database-architect` | Data modeling |
| `analyzer` | `analyzer` | Code analysis |
| `refactorer` | `refactoring-expert` | Code refactoring |
| `devops` | `platform-deployment` | Deployment and DevOps |

### Step 2: Update Workflows

#### Old Workflow (Spawn-based)
```bash
# Old way - manual spawning
/spawn-agent frontend --tasks=2.1,2.2 --feature=user-auth
/spawn backend --parallel
/coordinate-agents
```

#### New Workflow (Native)
```bash
# New way - natural invocation
Use the frontend agent to implement the login form component
Use the backend agent to create the authentication API

# Or use orchestration
/orchestrate user authentication system
```

### Step 3: Update Chains

#### Old Chain Format
```json
{
  "morning-setup": {
    "description": "Morning routine",
    "commands": ["smart-resume", "todo list"]
  }
}
```

#### New Chain Format
```json
{
  "morning-startup": {
    "description": "Comprehensive morning setup",
    "triggers": {
      "conditions": {
        "any": [
          "hoursSinceLastCommand > 8",
          "isFirstCommandToday === true"
        ]
      },
      "prompt": "Welcome back! Run morning setup? (y/n)"
    },
    "prerequisites": {
      "all": ["exists(.claude/)"],
      "error": "Not in a Claude project"
    },
    "steps": [
      "echo '☀️ Good morning!'",
      "/sr",
      "/bt list --open",
      "/branch-status"
    ],
    "on-success": "echo '✅ Ready to work!'"
  }
}
```

### Step 4: Enable CI/CD

#### Add Non-Interactive Support
```yaml
# GitHub Actions
- name: Validate Design
  env:
    CLAUDE_NON_INTERACTIVE: true
  run: |
    claude --non-interactive "/validate-design all"
```

#### Update Scripts
```bash
# Old script
echo "y" | claude "/stage-validate check 1"  # Risky!

# New script
claude --non-interactive "/stage-validate check 1"  # Safe
```

### Step 5: Update Security Hooks

#### Remove Old Hooks
```bash
# Archive old security hooks
mkdir -p .claude/hooks/pre-tool-use/archive
mv .claude/hooks/pre-tool-use/07-pii-protection.py .claude/hooks/pre-tool-use/archive/
mv .claude/hooks/pre-tool-use/16-tcpa-compliance.py .claude/hooks/pre-tool-use/archive/
mv .claude/hooks/pre-tool-use/22-security-validator.py .claude/hooks/pre-tool-use/archive/
```

#### Enable New Hook
```bash
# Ensure new comprehensive hook is active
chmod +x .claude/hooks/pre-tool-use/security-comprehensive.py
```

## Command Changes

### Deprecated Commands

These commands show deprecation notices:
- `/spawn-agent` → Use native agents
- `/spawn` → Use native agents
- `/persona` → Use native agents
- `/coordinate-agents` → Use `/orchestrate`

### New Commands

- `/chain` - Smart chain execution
- `/chain check` - Check for triggered chains
- `/chain status` - View chain execution status

### Enhanced Commands

These commands now support non-interactive mode:
- `/validate-design` (`/vd`)
- `/stage-validate` (`/sv`)
- `/prp-execute`
- `/security-check` (`/sc`)
- `/deps scan`
- `/test-runner` (`/tr`)
- `/validate-async`
- `/grade`

## Breaking Changes

### 1. Agent Parameters
```bash
# Old: Parameters passed to spawn
/spawn frontend --tasks=2.1,2.2 --context=auth

# New: Context passed naturally
Use the frontend agent to implement tasks 2.1 and 2.2 for authentication
```

### 2. Parallel Execution
```bash
# Old: Explicit parallel flag
/spawn-agent backend --parallel
/spawn-agent frontend --parallel

# New: Orchestration handles parallelism
/orchestrate implement user dashboard with backend API
```

### 3. Context Files
```bash
# Old: Context files in .agent-context/
.agent-context/frontend-context.md

# New: Agents use conversation context
# No separate context files needed
```

## Troubleshooting

### Issue: "Command not found"
```bash
# Old command fails
/spawn frontend
> Error: Command not found

# Solution: Use new syntax
Use the frontend agent to build the component
```

### Issue: "Agent not recognized"
```bash
# Check available agents
ls .claude/agents/

# Use exact agent name
Use the frontend agent  # ✓ Correct
Use the frontend-ux-specialist agent  # ✗ Wrong - doesn't exist
```

### Issue: "Chain not triggering"
```bash
# Debug chain conditions
/chain check --verbose

# Test conditions manually
ls .claude/ && echo "exists" || echo "not exists"
```

### Issue: "CI/CD failing"
```bash
# Ensure non-interactive mode
export CLAUDE_NON_INTERACTIVE=true

# Check command supports it
claude --non-interactive "/help" | grep "validate-design"
```

## Rollback Plan

If you need to temporarily use old commands:

### 1. Re-enable Spawn Commands
The spawn commands show deprecation notices but still work for 6 months.

### 2. Use Compatibility Mode
```bash
# Set environment variable
export CLAUDE_LEGACY_MODE=true
```

### 3. Restore Old Hooks
```bash
# Restore from archive
cp .claude/hooks/pre-tool-use/archive/*.py .claude/hooks/pre-tool-use/
```

## Benefits of Migration

### 1. **Better Performance**
- Native agents have isolated contexts
- No cross-contamination between agents
- Faster execution

### 2. **Simpler Workflow**
- Natural language invocation
- No parameter management
- Automatic context handling

### 3. **CI/CD Ready**
- Non-interactive mode for automation
- Structured JSON output
- Standard exit codes

### 4. **Smart Automation**
- Chains detect when to run
- Prerequisites prevent errors
- Automatic recovery

### 5. **Unified Security**
- Single comprehensive hook
- All checks in one place
- Consistent enforcement

## Timeline

### Immediate
- Native agents work now
- Non-interactive mode available
- Smart chains ready

### Next 6 Months
- Spawn commands show deprecation
- Both systems work
- Time to migrate

### After 6 Months
- Spawn commands removed
- Native agents only
- Full migration required

## Getting Help

### Documentation
- See `/help` for all commands
- Read `docs/` for guides
- Check `.claude/agents/` for agent docs

### Quick Reference
```bash
# See all agents
ls .claude/agents/

# Test new orchestration
/orchestrate simple task

# Check chain triggers
/chain check

# Validate in CI/CD
claude --non-interactive "/vd all"
```

### Support Resources
- GitHub Issues for bugs
- Discord community
- Stack Overflow tag: `claude-code`

## Summary

The migration brings:
- ✅ Native agent system (better performance)
- ✅ CI/CD automation (non-interactive mode)
- ✅ Smart workflows (enhanced chains)
- ✅ Unified security (single hook)
- ✅ Better documentation

Start by trying:
```bash
# Morning routine
/chain check

# Use an agent
Use the frontend agent to build a button component

# Run validation
claude --non-interactive "/validate-design all"
```

The new system is simpler, more powerful, and ready for production use!
