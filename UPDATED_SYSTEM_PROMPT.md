# Updated Claude Code Boilerplate System Prompt

Use the MCP filesystem and AppleScript to review our enhanced project boilerplate and setup for Claude Code.

**Project Location**: `/Users/shawnsmith/dev/bfc/claude-code-boilerplate-docs/boilerplate/`

## System Overview
This is our enhanced Claude Code boilerplate project that we use to launch new code sessions and projects. It now includes:

### Core Features
- **SYSTEM_OVERVIEW.md** - Complete technical documentation
- **NEW_CHAT_CONTEXT.md** - Quick reference for new sessions
- **90+ custom commands** with aliases
- **PRD-driven development workflow** with stage validation gates
- **Automated design system** (4 sizes, 2 weights, 4px grid)
- **Hooks for safety and observability**
- **Zero context loss between sessions**

### New Enhancements (v2.2.0)
- **Bug Tracking** (`/bt`) - Persistent across sessions with GitHub sync
- **Context Profiles** (`/cp`) - Focused work modes (frontend, backend, debug)
- **Documentation Cache** (`/dc`) - Offline access to library docs
- **Stage Validation** (`/sv`) - Enforce phase completion gates

### Integrated Systems
1. **Hooks System** - Automated enforcement and safety
2. **Custom Commands** - 90+ commands for every workflow
3. **Ryan Carson PRD System** - Requirements to code workflow
4. **Context Engineering** - Smart context management
5. **GitHub Integration** - Issues, PRs, and gists
6. **Multi-Agent Orchestration** - 9 specialized personas

### Key Directories
```
.claude/
  ├── commands/      # 90+ custom commands
  ├── hooks/         # Automation & safety
  ├── personas/      # Agent personalities
  ├── bugs/          # Bug tracking (NEW)
  ├── profiles/      # Context profiles (NEW)
  └── doc-cache/     # Documentation cache (NEW)
```

## Your Task
Review the entire system to understand:
1. How all components work together
2. The complete workflow from PRD to deployment
3. How the new features enhance the existing system
4. The getting started experience for new users

Focus areas:
- Integration between systems
- Command workflows
- Hook automation
- Context preservation
- New feature adoption

You don't need to make changes - just gain a comprehensive understanding of this sophisticated AI-assisted development system that combines PRD-driven development, automated quality enforcement, persistent bug tracking, focused context management, and seamless team collaboration.