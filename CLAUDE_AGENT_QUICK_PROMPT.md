# Quick Claude Agent Onboarding Prompt

Copy and paste this to a new Claude agent:

---

I need you to help me maintain and enhance my Claude Code Boilerplate System. Here's what you need to know:

## System Overview
I have a sophisticated AI-powered development framework at `/Users/shawnsmith/dev/bfc/boilerplate/` with:
- 71 Claude Code hooks (event interceptors)
- 120+ custom commands
- 32 workflow chains
- 180+ aliases
- Agent OS for multi-agent orchestration
- Full Next.js 15 + TypeScript + Tailwind boilerplate

## Key Files to Review
1. `CLAUDE_AGENT_COMPLETE_ONBOARDING.md` - Full system documentation
2. `CLAUDE.md` - Main Claude documentation
3. `.claude/settings.json` - Hook configurations
4. `.claude/chains.json` - Workflow definitions
5. `docs/claude-fixes/CLAUDE_HOOKS_TROUBLESHOOTING_GUIDE.md` - Critical fixes

## Repositories
- Private: `git@github.com:bearingfruitco/claude-code-boilerplate.git`
- Public: `git@github.com:bearingfruitco/cc-boiler-js-public.git`
- **IMPORTANT**: Always push to BOTH repos when updating

## Quick Status Check
Run this to verify system health:
```bash
python3 .claude/audit-system-complete.py
```

## Critical Knowledge
1. All hook matchers use `"matcher": ""` (empty string), NOT `"matcher": {}`
2. The system integrates with MCP connectors (GitHub, Supabase, etc.)
3. Design system uses strict rules: text-size-[1-4], 4px grid, 60/30/10 colors
4. TDD is built into workflows with automated test generation
5. Agent OS enables complex multi-agent operations

## Current State
- Version 2.8.0
- All systems operational
- Both repos synchronized at commit `287c31db`
- TypeScript pre-commit hooks may need `pnpm install` to work

Please review the `CLAUDE_AGENT_COMPLETE_ONBOARDING.md` file for comprehensive details about:
- System architecture
- Technical stack
- Command categories
- Workflow chains
- Security practices
- Enhancement opportunities

What would you like to work on first?

---

End of prompt. The agent should then read the comprehensive onboarding document for full details.
