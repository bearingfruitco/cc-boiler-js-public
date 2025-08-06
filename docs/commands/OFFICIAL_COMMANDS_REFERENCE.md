# Official Claude Code Commands Reference

> How our 150+ commands complement the official Claude Code commands

## Official Commands (from Anthropic)

### Core Commands

| Command | Description | Our Extensions |
|---------|-------------|----------------|
| `/agents` | Manage sub-agents interactively | We add: `/spawn [agent]` for quick access |
| `/hooks` | Configure hook scripts | We add: Pre-built hooks for common tasks |
| `/mcp` | Manage MCP connections | Fully supported |
| `/settings` | View/edit settings | We add: Modular config system |

### Built-in Commands (Inferred from Docs)
- `/help` - Show available commands
- `/clear` - Clear the terminal
- `/exit` - Exit Claude Code

## Our Command System (150+ Commands)

We extend the official commands with a comprehensive productivity system:

### 🚀 Quick Access Commands

#### Agent Management (Extends `/agents`)
```bash
/spawn [agent]     # Quick sub-agent invocation
/agent [name]      # Shorthand for specific agents
/orch [task]       # Multi-agent orchestration
/at [task]         # Analyze task, recommend agents
```

#### Development Workflow
```bash
/sr               # Smart Resume - load full context
/fw start [#]     # Feature workflow from GitHub issue
/prd [name]       # Create product requirements
/prp [name]       # Create technical implementation plan
/gt [name]        # Generate tasks from requirements
/pt [name]        # Process tasks systematically
```

#### Validation & Quality
```bash
/vd               # Validate design system compliance
/sv               # Stage validation (multi-level)
/sc               # Security check
/tr               # Test runner
/lint             # Code formatting
/deps             # Dependency analysis
```

### 📊 How They Work Together

```bash
# Official command for management
/agents           # Opens interactive agent manager

# Our shortcuts for productivity
/spawn backend    # Instantly invoke backend agent
/be              # Even shorter alias
```

### 🔧 Configuration Harmony

#### Official Settings Structure
```
~/.claude/settings.json      # User settings (official)
.claude/settings.json        # Project settings (official)
```

#### Our Extended Structure
```
.claude/config/              # Modular configurations
├── chains.json             # Workflow automation
├── aliases.json            # Command shortcuts
├── hooks-config.json       # Hook configurations
└── feature-flags.json      # Feature toggles
```

## Command Categories

### 1. Context & State Management
- `/sr` - Smart Resume with full context
- `/checkpoint` - Save/restore project state
- `/cp` - Context profiles for different features
- `/compress` - Token optimization

### 2. Development Commands
- `/cc` - Create component with validation
- `/ch` - Create hook with testing
- `/ctf` - Create tracked form
- `/ca` - Create API endpoint
- `/exists` - Check before creating

### 3. Agent Commands (31 Specialists)
- `/spawn [agent]` - Invoke any agent
- `/pm` - Project Manager
- `/be` - Backend Engineer
- `/fe` - Frontend Developer
- `/qa` - QA Engineer
- `/sec` - Security Analyst
- Plus 25 more specialists...

### 4. Workflow Automation
- `/chain [name]` - Run automated workflows
- `/chains` - List available workflows
- Examples:
  - `/chain morning-setup`
  - `/chain feature-complete`
  - `/chain pre-pr`

### 5. Testing & Validation
- `/test` - Run tests
- `/tdd` - Test-driven development
- `/vd` - Validate design system
- `/sv` - Stage validation
- `/sc` - Security check

### 6. Documentation
- `/docs` - Generate documentation
- `/api-docs` - API documentation
- `/comp-docs` - Component docs
- `/update-docs` - Refresh all docs

### 7. Git & GitHub Integration
- `/pr` - Create pull request
- `/issue` - Create GitHub issue
- `/sync` - Sync with main
- `/branch` - Branch management

## Using Official + Our Commands

### Example: Setting Up Sub-Agents

```bash
# Official way
/agents                    # Open agent manager
# Navigate UI to create agent

# Our productivity boost
/spawn pm                  # Use pre-built PM agent instantly
/create-agent my-agent     # Generate new agent with template
```

### Example: Configuring Hooks

```bash
# Official way
/hooks                     # Open hooks configurator
# Manually add hook commands

# Our productivity boost
/enable-hook design-check  # Enable pre-built hook
/ch my-hook               # Create custom hook with template
```

## Command Aliases

We provide short aliases for common commands:

| Full Command | Alias | Purpose |
|--------------|-------|---------|
| `/spawn backend` | `/be` | Backend engineer |
| `/spawn frontend` | `/fe` | Frontend developer |
| `/spawn security` | `/sec` | Security analyst |
| `/validate-design` | `/vd` | Design validation |
| `/smart-resume` | `/sr` | Resume context |

## Best Practices

1. **Use Official for Configuration**
   - `/agents` - When setting up new agents
   - `/hooks` - When configuring hook behavior
   - `/settings` - For core Claude Code settings

2. **Use Ours for Productivity**
   - `/spawn` - Quick agent access
   - `/chain` - Automated workflows
   - `/sr` - Context management
   - Short aliases for speed

3. **Combine for Power**
   ```bash
   /agents          # Set up new agent
   /spawn my-agent  # Use it immediately
   /chain feature   # Run full workflow
   ```

## Migration Guide

### From Official Only
No changes needed! Our commands are additive:
```bash
# Keep using official commands
/agents
/hooks

# Add our productivity commands as needed
/sr              # Better context management
/spawn [agent]   # Faster agent access
/chain [flow]    # Automated workflows
```

### From Our System
You already have everything! Official commands work perfectly:
```bash
/agents          # Manage all 31 pre-built agents
/hooks          # Configure all 25 pre-built hooks
```

## Summary

- **Official Commands**: Core functionality and configuration
- **Our Commands**: Productivity, automation, and shortcuts
- **Together**: A complete development system

Think of official commands as the engine, and our commands as the full vehicle built around it - everything you need for production development.

---

*For full command reference, see `.claude/QUICK_REFERENCE.md`*
