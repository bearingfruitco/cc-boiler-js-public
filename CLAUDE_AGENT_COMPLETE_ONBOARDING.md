# Claude Agent System Onboarding & Knowledge Transfer

## 🎯 Mission Brief
You are taking over maintenance and enhancement of a sophisticated Claude Code Boilerplate System (v2.8.0) that serves as an AI-powered development framework. This system has 71 hooks, 120+ commands, 32 workflows, and 180+ aliases designed to supercharge development with Claude Code.

## 📍 Repository Information
- **Private Repo**: `git@github.com:bearingfruitco/claude-code-boilerplate.git`
- **Public Repo**: `git@github.com:bearingfruitco/cc-boiler-js-public.git`
- **Latest Commit**: `287c31db` - Complete Claude Code Boilerplate System v2.8.0
- **Both repos are synchronized** - always push to both when making updates

## 🏗️ System Architecture Overview

### Core Components:
1. **Claude Code Integration** (`.claude/` directory)
   - 71 hooks across 7 event types (PreToolUse, PostToolUse, Notification, etc.)
   - Hooks intercept and enhance Claude Code operations
   - All hooks fixed to use string matchers (not objects) per Anthropic docs

2. **Command System** (`/commands/`)
   - 120+ custom commands for development tasks
   - Commands are Python/Shell scripts that Claude can execute
   - Examples: `analyze-deps`, `security-check`, `create-component`

3. **Workflow Chains** (`chains.json`)
   - 32 pre-defined workflows that chain commands together
   - Examples: `full-stack-setup`, `deploy-production`, `test-suite`

4. **Alias System** (`aliases.json`)
   - 180+ shortcuts for common operations
   - Maps short names to full command paths

5. **Agent OS** (`.agent-os/`)
   - Advanced orchestration layer for multi-agent operations
   - Manages sub-agents and complex workflows

## 🔧 Technical Stack

### Frontend:
- **Next.js 15.3.5** with App Router
- **React 19.1.0** with Hooks
- **TypeScript 5.8.3** (strict mode)
- **Tailwind CSS 4.1.0** with custom design system
- **Framer Motion** for animations
- **Lucide React** for icons

### State & Data:
- **Zustand** for client state management
- **React Hook Form** + **Zod** for forms
- **TanStack Query** for server state
- **SWR** as alternative data fetching

### Backend & Database:
- **Supabase** for auth and database
- **Drizzle ORM** with PostgreSQL
- **Prisma** as alternative ORM
- **Upstash Redis** for caching

### Development Tools:
- **pnpm** as package manager
- **Biome** for linting/formatting
- **Vitest** for unit testing
- **Playwright** for E2E testing
- **Husky** for git hooks

### Monitoring & Analytics:
- **Sentry** for error tracking
- **Vercel Analytics**
- **RudderStack** for product analytics

## 📁 Project Structure

```
/Users/shawnsmith/dev/bfc/boilerplate/
├── .claude/                    # Claude Code configuration
│   ├── settings.json          # 71 hooks configuration
│   ├── chains.json           # 32 workflow chains
│   ├── aliases.json          # 180+ command shortcuts
│   ├── config.json           # Main Claude config
│   ├── commands/             # 120+ command scripts
│   ├── hooks/                # Hook implementation files
│   ├── scripts/              # Utility scripts
│   └── troubleshooting/      # Diagnostic tools
├── .agent-os/                # Agent orchestration system
├── app/                      # Next.js app directory
├── components/               # React components
├── lib/                      # Utilities and helpers
├── hooks/                    # React hooks
├── PRPs/                     # Pattern Recognition Protocols
├── docs/                     # Documentation
│   ├── claude-fixes/         # Hook troubleshooting
│   ├── implementation/       # Implementation guides
│   └── workflows/            # Workflow documentation
└── templates/                # Project templates
```

## 🚀 Key Features & Capabilities

### 1. Hook System (CRITICAL):
- **Event Types**: PreToolUse, PostToolUse, Notification, Stop, SubagentStop, PreCompact, UserPromptSubmit
- **Key Fix Applied**: All matchers use `"matcher": ""` (empty string), NOT `"matcher": {}`
- **Verification**: Run `python3 .claude/audit-system-complete.py`

### 2. Command Categories:
- **Development**: Component generation, boilerplate creation
- **Testing**: TDD workflows, test generation, coverage analysis
- **Security**: Vulnerability scanning, dependency auditing
- **Deployment**: Build optimization, deployment workflows
- **AI Enhancement**: Prompt engineering, context management

### 3. Design System Rules (STRICT):
```
Typography: ONLY text-size-[1-4], font-regular, font-semibold
Spacing: 4px grid (p-1, p-2, p-3, p-4, p-6, p-8)
Colors: 60/30/10 distribution rule
Mobile: 44px min touch targets, 16px min text
```

### 4. TDD & Testing Philosophy:
- Test-first development approach
- Automated test generation via commands
- Integration with Vitest and Playwright
- Coverage requirements enforced

### 5. Agent OS Capabilities:
- Multi-agent orchestration
- Sub-agent spawning and management
- Complex workflow automation
- State management across agents

## 🔐 Security & Best Practices

### What's Protected:
- `.env` files (use `.env.example` as template)
- `.mcp.json` (MCP configurations)
- API keys and credentials
- Logs and transcripts
- Personal/team data

### Git Workflow:
```bash
# Always push to BOTH repositories
git add .
git commit -m "feat: your changes"
git push origin main
git push public main
```

## 🛠️ Common Operations

### System Health Check:
```bash
python3 .claude/audit-system-complete.py
```

### Test a Hook:
```bash
# In Claude Code, press Ctrl+R for transcript mode
# Then test individual hooks
```

### Add New Command:
1. Create script in `.claude/commands/`
2. Update `command-registry.json`
3. Optionally add to `chains.json` or `aliases.json`

### Fix TypeScript Errors:
```bash
pnpm install
pnpm run typecheck
```

## 📚 Essential Documentation

1. **CLAUDE.md** - Main Claude documentation
2. **docs/CLEANUP_SUMMARY.md** - Recent organization
3. **docs/claude-fixes/CLAUDE_HOOKS_TROUBLESHOOTING_GUIDE.md** - Hook fixes
4. **CLAUDE_AGENT_HANDOFF.md** - Previous handoff notes

## 🎯 Current State & Recent Changes

### What's Working:
- ✅ All 71 hooks enabled and functional
- ✅ 120+ commands operational
- ✅ 32 workflows ready
- ✅ 180+ aliases configured
- ✅ Both GitHub repos synchronized

### Recent Improvements:
- Fixed hook matcher format issue
- Organized documentation into `/docs/`
- Cleaned up temporary files
- Enhanced `.gitignore` for security
- Created `.env.example`

### Backup Available:
- Full backup at: `.claude.full_backup_20250727_102756/`
- Keep for 1-2 weeks as safety net

## 🚦 Getting Started Tasks

1. **Clone the repository**:
   ```bash
   git clone git@github.com:bearingfruitco/claude-code-boilerplate.git
   cd claude-code-boilerplate
   ```

2. **Install dependencies**:
   ```bash
   pnpm install
   ```

3. **Run system audit**:
   ```bash
   python3 .claude/audit-system-complete.py
   ```

4. **Review key files**:
   - `.claude/settings.json` - Hook configurations
   - `.claude/chains.json` - Workflows
   - `CLAUDE.md` - Main documentation

5. **Test a simple command**:
   - Open Claude Code
   - Try: `@claude run security-check`

## 💡 Enhancement Opportunities

1. **Add more Agent OS integrations**
2. **Expand TDD command suite**
3. **Create more workflow chains**
4. **Enhance PRPs (Pattern Recognition Protocols)**
5. **Add more MCP connectors**
6. **Improve TypeScript type coverage**
7. **Expand component library**

## 🤝 Collaboration Notes

- The system is designed for AI-assisted development
- Commands should be AI-friendly with clear outputs
- Documentation should enable AI agents to self-serve
- Always maintain backwards compatibility
- Test changes thoroughly before pushing

## 🎉 Welcome to the Team!

You now have access to a powerful AI-enhanced development system. The combination of Claude Code hooks, commands, workflows, and Agent OS creates a unique development experience. Feel free to explore, enhance, and push the boundaries of what's possible!

Remember: When making updates, always push to BOTH repositories to keep them synchronized.

---

*System Version: 2.8.0 | Last Updated: 2025-07-27*
