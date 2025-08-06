# Official Claude Code Alignment Guide

> How the Claude Code Boilerplate v4.0.1 aligns with official Anthropic documentation

## Overview

This guide shows how our boilerplate system complements and extends the official Claude Code features while maintaining full compatibility.

## 🤖 Sub-Agents (Official Feature)

### Official Implementation
- **Location**: `.claude/agents/` (project) or `~/.claude/agents/` (user)
- **Format**: Markdown with YAML frontmatter
- **Command**: `/agents` to manage

### Our Implementation ✅ FULLY COMPATIBLE
- **Same location**: `.claude/agents/`
- **Same format**: Markdown with YAML frontmatter
- **31 pre-built sub-agents** ready to use
- **Custom commands**: `/spawn [agent]` for quick access

### Example Sub-Agent (Matches Official Format)
```yaml
---
name: tdd-engineer
description: Test-Driven Development specialist. Use PROACTIVELY for test-first approach.
tools: Read, Write, Edit, Bash
---

# System prompt content...
```

### Key Alignments
✅ Exact same file format  
✅ Same directory structure  
✅ Tools field works identically  
✅ Description encourages proactive use  
✅ Can be managed with official `/agents` command  

## 🪝 Hooks System (Official Feature)

### Official Implementation
- **Configuration**: In settings.json files
- **Events**: PreToolUse, PostToolUse, Notification, Stop
- **Output**: Exit codes or JSON

### Our Implementation ✅ FULLY COMPATIBLE
- **Same configuration**: `settings.json` and `hooks-config.json`
- **Same events**: All official events supported
- **25+ pre-built hooks** for common tasks
- **Proper JSON output** following official schema

### Example Hook (Matches Official Format)
```python
#!/usr/bin/env python3
# PreToolUse hook - matches official schema
input_data = json.loads(sys.stdin.read())
tool_name = input_data.get('tool_name')

# JSON output per official docs
print(json.dumps({
    "decision": "block",  # or "approve"
    "message": "Validation failed"
}))
```

### Security Considerations ✅
We follow all official security guidelines:
- Clear warnings about hook permissions
- Input validation best practices
- Safe command execution patterns

## 📋 Commands

### Official Commands
| Command | Purpose | Our Support |
|---------|---------|-------------|
| `/agents` | Manage sub-agents | ✅ Supported + custom shortcuts |
| `/hooks` | Configure hooks | ✅ Supported + presets |
| `/mcp` | MCP tools | ✅ Supported |

### Our Extensions (150+ Commands)
We add productivity commands that complement official ones:
- `/sr` - Smart resume (loads context)
- `/spawn [agent]` - Quick agent access
- `/chain [workflow]` - Multi-agent orchestration
- `/vd` - Validate design system
- And 140+ more...

## 🔧 Settings & Configuration

### Official Structure
```
~/.claude/settings.json      # User settings
.claude/settings.json        # Project settings
.claude/settings.local.json  # Local settings
```

### Our Structure ✅ EXTENDS OFFICIAL
```
# All official files supported, plus:
.claude/config/             # Modular configs
├── chains.json            # Workflow automation
├── aliases.json           # Command shortcuts
├── hooks-config.json      # Hook presets
└── feature-flags.json     # Feature toggles
```

## 🚀 MCP (Model Context Protocol) Support

### Official Feature
- Connect to external tools via MCP
- Tools appear as `mcp__[server]__[tool]`

### Our Implementation ✅ FULL SUPPORT
- All MCP tools work with our system
- Hooks can target MCP tools
- Sub-agents can use MCP tools
- Documentation includes MCP examples

## 📚 Best Practices Alignment

### Official Recommendations
1. Generate sub-agents with Claude first
2. Create focused, single-purpose agents
3. Write detailed prompts
4. Limit tool access appropriately
5. Version control project agents

### Our Implementation ✅ FOLLOWS ALL
1. ✅ Agent generation commands included
2. ✅ 31 focused specialists
3. ✅ Detailed prompt templates
4. ✅ Minimal tool permissions
5. ✅ Git-ready structure

## 🔄 Migration Path

### For Existing Claude Code Users
```bash
# Your official setup works as-is
# Add our boilerplate for extra features:
./scripts/integrate-boilerplate-v2.sh --mode=selective

# Choose what to add:
# - Pre-built sub-agents
# - Workflow automation
# - Design system enforcement
# - Custom commands
```

### For Our Users
```bash
# Already compatible with official features!
# Just update to use official commands:
/agents  # Instead of our agent management
/hooks   # Instead of our hook management
```

## 📊 Compatibility Matrix

| Feature | Official | Ours | Compatible |
|---------|----------|------|------------|
| Sub-agents format | ✅ | ✅ | 100% |
| Hooks system | ✅ | ✅ | 100% |
| MCP support | ✅ | ✅ | 100% |
| Settings structure | ✅ | ✅+ | 100% |
| Commands | Basic | 150+ | Additive |

## 🎯 Key Advantages

### What Official Provides
- Core sub-agent system
- Hook event system
- MCP integration
- Basic commands

### What We Add
- 31 pre-built specialist sub-agents
- 25+ production-ready hooks
- 150+ productivity commands
- Workflow automation (chains)
- Design system enforcement
- Architecture tracking
- Zero-config setup

## 🚦 Using Both Together

```bash
# Official commands for management
/agents              # Manage sub-agents
/hooks              # Configure hooks

# Our commands for productivity
/sr                 # Smart resume
/spawn backend      # Quick agent access
/chain feature      # Run workflows
/vd                 # Validate design
```

## 📝 Summary

The Claude Code Boilerplate v4.0.1 is **100% compatible** with official Claude Code features while adding:

1. **Pre-built content**: 31 agents, 25 hooks, 150 commands
2. **Automation**: Workflow chains, design validation
3. **Best practices**: Enforced through hooks
4. **Productivity**: Smart shortcuts and aliases
5. **Documentation**: Comprehensive guides

Think of it as "Claude Code++" - everything official, plus a complete development system ready to use.

---

*Last updated: 2025-01-31*  
*Version: v4.0.1-clean*  
*Compatibility: Claude Code 1.0+*
