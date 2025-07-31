# Agent System Documentation

> 31 specialized AI agents working in orchestrated harmony

## 🤖 Agent Overview

The Claude Code Boilerplate includes 31 specialized agents, each with specific expertise, tool access, and file ownership. These agents can work independently or be orchestrated together for complex tasks.

## 📊 Agent Categories

### 1. Technology Specialists (v4.0.0)
- **supabase-specialist**: Database, RLS, real-time features
- **playwright-specialist**: Browser automation, E2E testing
- **analytics-engineer**: Tracking, data pipelines, metrics
- **platform-deployment**: Vercel, edge optimization, CDN
- **privacy-compliance**: GDPR, CCPA, data handling
- **orm-specialist**: Drizzle, Prisma optimization
- **event-schema**: Event design, taxonomy

### 2. Core Development Team
- **frontend**: UI/UX, React, design system compliance
- **backend**: APIs, server logic, authentication
- **security**: Vulnerabilities, compliance, threat modeling
- **qa**: Testing strategies, quality metrics
- **performance**: Optimization, caching, metrics

### 3. Architecture & Planning
- **system-architect**: Technical design, patterns
- **database-architect**: Schema optimization, migrations
- **pm-orchestrator**: Coordination, planning, workflows

### 4. Specialized Roles
- **analyzer**: Root cause analysis, debugging
- **refactoring-expert**: Code quality, technical debt
- **integration-specialist**: Third-party APIs, webhooks
- **documentation-writer**: Technical writing, guides
- **mentor**: Teaching, onboarding, best practices

## 🎯 Agent Capabilities

### Auto-Triggering
Agents automatically activate based on:
- **File patterns**: Working in specific directories
- **Keywords**: Detecting relevant terms in commands
- **Context**: Understanding current task needs

Example:
```bash
# Working on components/Button.tsx triggers 'frontend' agent
# Mentioning "slow" or "performance" triggers 'performance' agent
# Database queries trigger 'database-architect'
```

### Tool Access
Each agent has specific tool permissions:
- **Primary tools**: Core tools for their work
- **Specialized tools**: Domain-specific capabilities
- **Validation tools**: Quality checking abilities

### File Ownership
Agents respect boundaries:
- Frontend owns: `components/`, `app/(routes)/`, `styles/`
- Backend owns: `app/api/`, `lib/server/`, `middleware.ts`
- Security owns: `lib/security/`, `.env*`

## 🔄 Orchestration Patterns

### 1. Feature Development
```bash
/orch user-authentication
```
Spawns: architect → backend → frontend → security → qa

### 2. Bug Investigation
```bash
/orch investigate-checkout-bug
```
Spawns: analyzer → relevant specialists → qa

### 3. Performance Optimization
```bash
/orch optimize-dashboard
```
Spawns: performance → analyzer → frontend/backend → qa

### 4. Security Audit
```bash
/orch security-review
```
Spawns: security → analyzer → backend → qa

### 5. Full Stack Feature
```bash
/orch payment-system
```
Spawns: All relevant agents in coordinated phases

## 📝 Using Agents

### Manual Spawning
```bash
/spawn frontend
"Create a responsive navigation component"

/spawn security
"Review authentication flow for vulnerabilities"

/spawn analyzer
"Debug why checkout is failing intermittently"
```

### Automatic Orchestration
```bash
/orch [feature-name]
# System analyzes needs and spawns appropriate agents
```

### Multi-Perspective Review
```bash
/chain multi-perspective-review
# Spawns 4 agents for different viewpoints
```

## 🎨 Agent Personalities

Each agent has:
- **Expertise**: Specific knowledge domains
- **Constraints**: What they won't do
- **Communication style**: How they interact
- **Decision patterns**: How they approach problems

### Example: Frontend Agent
```json
{
  "expertise": [
    "React/Next.js components",
    "Design system compliance",
    "Responsive design",
    "Performance optimization"
  ],
  "constraints": {
    "no_backend": "Never modify API routes",
    "design_system": "Always use design tokens",
    "mobile_first": "Test on 375px first"
  }
}
```

## 🚀 Best Practices

### 1. Let Agents Focus
Don't ask frontend agents to write APIs or backend agents to style components.

### 2. Use Orchestration for Complex Tasks
Multiple agents working together are more effective than one trying to do everything.

### 3. Trust Auto-Triggering
The system knows when to involve specialists based on context.

### 4. Review Agent Boundaries
Agents respect file ownership - this prevents conflicts.

### 5. Leverage Parallel Execution
Many agents can work simultaneously on different aspects.

## 📊 Agent Metrics

Track agent effectiveness:
- Tasks completed
- Quality scores
- Collaboration patterns
- Time saved

## 🔧 Customizing Agents

Add custom agents in `.claude/agents/`:
```json
{
  "name": "Custom Specialist",
  "focus": "Your domain",
  "expertise": ["skill1", "skill2"],
  "tools": {
    "primary": ["filesystem", "context"]
  },
  "file_ownership": ["custom/**/*"]
}
```

## 📚 Related Documentation

- [Orchestration Guide](../workflow/PARALLEL_ORCHESTRATION_GUIDE.md)
- [Agent Personas](../../.claude/personas/agent-personas.json)
- [Chain Automation](../CHAIN_AUTOMATION.md)
