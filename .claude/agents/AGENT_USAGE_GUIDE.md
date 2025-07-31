# Agent Usage Quick Reference

This guide helps you choose the right agent for your task.

## Development Agents

### Frontend Development
- **frontend** - UI components, responsive design, accessibility, forms, animations
- **ui-systems** - Design system components, component libraries, Storybook
- **form-builder-specialist** - Complex forms, multi-step forms, file uploads

### Backend Development
- **backend** - REST APIs, business logic, auth, webhooks, background jobs
- **database-architect** - Database schema, performance, migrations, indexes
- **orm-specialist** - ORM queries (Drizzle/Prisma), query optimization
- **supabase-specialist** - Supabase setup, RLS policies, real-time features

### Integration & APIs
- **integration-specialist** - Third-party APIs, webhooks, OAuth, data transformation
- **migration-specialist** - Database/framework migrations, breaking changes

## Quality & Testing

### Testing
- **qa** - Test suites, e2e testing, test automation, bug review
- **tdd-engineer** - Test-driven development, test-first approach
- **playwright-specialist** - Browser automation, visual regression tests

### Code Quality
- **code-reviewer** - Pull request reviews, code quality, best practices
- **analyzer** - Deep code analysis, debugging, performance bottlenecks
- **refactoring-expert** - Legacy code refactoring, design patterns
- **production-code-validator** - Production readiness, error handling

## Architecture & Planning

### System Design
- **system-architect** - System architecture, ADRs, API contracts, scalability
- **pm-orchestrator** - Requirements breakdown, roadmaps, prioritization
- **senior-engineer** - Complex problems, architectural decisions, mentoring

### Documentation
- **documentation-writer** - Technical docs, API docs, user guides, READMEs
- **prd-writer** - Product requirements, user flows, acceptance criteria
- **prp-writer** - Technical specs from PRDs, implementation plans

## Specialized Agents

### Security & Compliance
- **security** - Security audits, OWASP checks, API security, PII risks
- **privacy-compliance** - GDPR/CCPA, consent management, data policies
- **pii-guardian** - PII handling, data masking, encryption

### Performance & DevOps
- **performance** - Performance optimization, caching, monitoring
- **platform-deployment** - CI/CD, Docker, monitoring, deployments
- **automation-workflow-engineer** - Workflow automation, scheduled jobs

### Analytics & Reporting
- **analytics-engineer** - Analytics tracking, data pipelines, dashboards
- **event-schema** - Event taxonomies, tracking plans, event validation
- **report-generator** - Project reports, status updates, dashboards
- **progress-logger** - Progress tracking, burndown charts

### Support & Research
- **mentor** - Learning guidance, best practices, code review feedback
- **researcher** - Technology evaluation, documentation research
- **financial-analyst** - Project costs, budgets, ROI analysis

## Quick Decision Guide

**Building UI?** → frontend, ui-systems, form-builder-specialist

**Building APIs?** → backend, integration-specialist

**Database work?** → database-architect, orm-specialist, supabase-specialist

**Need testing?** → qa, tdd-engineer, playwright-specialist

**Code review?** → code-reviewer, analyzer, senior-engineer

**Security concern?** → security, privacy-compliance, pii-guardian

**Documentation?** → documentation-writer, prd-writer, prp-writer

**Performance issue?** → performance, analyzer

**DevOps/Deploy?** → platform-deployment, automation-workflow-engineer

**Planning?** → pm-orchestrator, system-architect

## Usage Examples

```bash
# Simple UI component
Use the frontend agent to create a user profile card

# Complex form
Use the form-builder-specialist agent to build a multi-step onboarding form

# API development
Use the backend agent to create user authentication endpoints

# Database design
Use the database-architect agent to design the schema for our e-commerce platform

# Security review
Use the security agent to audit our payment processing implementation

# Performance optimization
Use the performance agent to analyze and fix slow page loads

# Documentation
Use the documentation-writer agent to create API documentation
```

## Multi-Agent Workflows

For complex tasks, use `/orchestrate`:

```bash
# Full feature development
/orchestrate build a complete user authentication system

# This will coordinate:
# - pm-orchestrator (planning)
# - system-architect (design)
# - database-architect (schema)
# - backend (API)
# - frontend (UI)
# - security (audit)
# - qa (testing)
# - documentation-writer (docs)
```

## Tips

1. **Start specific**: Use the most specialized agent for your task
2. **Don't overlap**: Each agent has a specific purpose
3. **Chain agents**: Use multiple agents in sequence for complex tasks
4. **Use orchestrate**: For tasks needing 3+ agents
5. **Check agent docs**: Each agent file has detailed capabilities

Remember: The right agent makes all the difference in getting quality results!
