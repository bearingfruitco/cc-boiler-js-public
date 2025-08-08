---
description: Claude Code specific configuration that extends CLAUDE.md
priority: high
---

# Claude Code Configuration (claw.md)

This file provides Claude Code compatibility while maintaining our comprehensive CLAUDE.md system.

## 🔗 Primary Configuration
**IMPORTANT**: All rules in [CLAUDE.md](../CLAUDE.md) apply. This file adds Claude Code specific enhancements.

## 📚 Reference Documents
You MUST read and follow these documents:
- **Main System**: [CLAUDE.md](../CLAUDE.md) - Primary configuration
- **Workflows**: [.claude/docs/WORKFLOWS.md](.claude/docs/WORKFLOWS.md) - Development workflows
- **Design System**: [.claude/docs/DESIGN_SYSTEM.md](.claude/docs/DESIGN_SYSTEM.md) - UI/UX rules
- **MCP Mapping**: [.claude/docs/MCP_AGENT_MAPPING.md](.claude/docs/MCP_AGENT_MAPPING.md) - MCP connections
- **Agents**: [.claude/agents/](.claude/agents/) - Specialized sub-agents

## 🎯 Claude Code Specific Enhancements

### MCP Servers
- **IMPORTANT**: Use Octocode MCP for enhanced code generation
- **PROACTIVELY**: Leverage Serena MCP for codebase understanding
- Available MCPs are listed in `.claude/config/mcp-registry.json`

### Testing Workflow
1. **FIRST**: Use `tdd-engineer` for test-first development
2. **THEN**: Use `validation-gates` for comprehensive validation
3. **NEVER**: Skip either step - they complement each other

### Parallel Development
- **USE**: `/parallel-prep` and `/parallel-execute` for 3x faster development
- **WHEN**: Multiple approaches could work
- **RESULT**: Best implementation selected from parallel attempts

### Sub-Agents
- **ULTRAIMPORTANT**: Use specialized agents for their domains
- Over 35 agents available in `.claude/agents/`
- Each agent has specific MCP permissions

### Commands
- Over 50 custom commands in `.claude/commands/`
- **PROACTIVELY** use appropriate commands for workflows
- Commands are prefixed with `/` 

## 🚫 Critical Rules (from CLAUDE.md)
- **NEVER** modify the 4-tier typography system
- **NEVER** use spacing not divisible by 4
- **NEVER** skip validation gates
- **ALWAYS** follow the 60/30/10 color rule

## 🔧 Claude Code Keywords
These keywords have special meaning in Claude Code:
- **IMPORTANT**: High priority instruction
- **PROACTIVELY**: Do this without being asked
- **ULTRAIMPORTANT**: Critical rule, never violate
- **ULTRAVERYIMPORTANT**: Highest priority rule

## 🏗️ Project Structure
```
.claude/
├── agents/          # 35+ specialized agents
├── commands/        # 50+ workflow commands
├── config/          # MCP and system config
├── docs/            # Documentation
├── hooks/           # Automation scripts
└── mcp-servers/     # MCP implementations
```

## 🎯 Development Philosophy
- **Production Ready**: No over-engineering
- **Test Everything**: TDD first, validation second
- **Use Agents**: Delegate to specialists
- **Parallel When Possible**: 3x faster with work trees
- **Follow Design System**: Strict compliance

## 🔗 Integration Points
This claw.md integrates with:
1. **CLAUDE.md**: Inherits all rules
2. **MCP Servers**: Enhanced capabilities
3. **Sub-Agents**: Specialized intelligence
4. **Hooks**: Automated workflows
5. **Commands**: Reusable workflows

## ✨ Remember
You are part of a sophisticated system with:
- 35+ specialized agents
- 18+ MCP connections
- 50+ custom commands
- Comprehensive workflows
- Strict design system

Use ALL available tools to deliver exceptional results!
