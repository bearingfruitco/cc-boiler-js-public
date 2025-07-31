# Sub-Agent Alias Patterns

## Quick Reference

### Primary Aliases (Most Used)
- `fe` → frontend-ux-specialist
- `be` → backend-reliability-engineer
- `qa` → qa-test-engineer
- `sec` or `sa` → security-threat-analyst
- `pm` → product-manager-orchestrator
- `tdd` → tdd-engineer
- `cr` → code-reviewer
- `doc` → documentation-writer

### Development Aliases
- `arch` → systems-architect
- `senior` → senior-engineer
- `debug` or `analyzer` → code-analyzer-debugger
- `perf` → performance-optimizer
- `refactor` → refactoring-expert

### Data & Infrastructure
- `db` → database-architect
- `migrate` → migration-specialist
- `auto` → automation-workflow-engineer

### Specialized Aliases
- `form` → smart-form-builder
- `forms` → form-builder-specialist
- `pii` → pii-guardian
- `mentor` → technical-mentor-guide
- `report` → report-generator
- `fin` → financial-analyst
- `research` → researcher
- `prod-val` → production-code-validator
- `prd-writer` → prd-writer

## Usage Patterns

### Basic Pattern
```
[alias] [task description]
```

### Examples

#### Frontend Development
```bash
# Review UI component
fe review and enhance the UserProfile component

# Quick alias
fe make this responsive
```

#### Backend Development
```bash
# API development
be create reliable user authentication API

# Quick alias
be add error handling
```

#### Security Review
```bash
# Full security audit
sec analyze authentication system for vulnerabilities

# Quick alias
sa check this code
```

#### Test Development
```bash
# Create comprehensive tests
qa generate test suite for checkout feature

# TDD approach
tdd implement user registration with tests first
```

#### Code Review
```bash
# Review changes
cr review these changes for best practices

# Quick alias
cr check this PR
```

## Chaining Agents

You can chain multiple agents for workflows:

```bash
# TDD workflow
tdd create tests → fe implement UI → cr review

# Security workflow
sec audit → be fix issues → qa test fixes

# Full feature workflow
pm orchestrate → arch design → tdd tests → fe/be implement
```

## Context-Aware Aliases

The system suggests agents based on context:

- Working on `.tsx` files → suggests `fe`
- Working on `/api/` files → suggests `be`
- Working on test files → suggests `qa` and `tdd`
- Working on auth files → suggests `sec`
- Working on `.md` files → suggests `doc`

## Advanced Patterns

### Multi-Agent Workflows
```bash
# Parallel execution
pm orchestrate parallel: fe build UI, be create API, qa write tests

# Sequential execution
arch design system → tdd create tests → be implement → cr review
```

### Specialized Tasks
```bash
# Database work
db design user schema → migrate create migration scripts

# Form building
form create dynamic registration form with validation

# Documentation
doc create API documentation for webhook system

# Performance optimization
perf analyze and optimize dashboard rendering
```

## Tips

1. **Use shortest alias** when context is clear
2. **Be specific** in task descriptions
3. **Chain agents** for complex workflows
4. **Let context** guide agent selection
5. **Check suggestions** from hooks for best agent

## Quick Decision Guide

| Task | Use Agent | Alias |
|------|-----------|-------|
| UI Component | frontend-ux-specialist | `fe` |
| API Endpoint | backend-reliability-engineer | `be` |
| Write Tests | qa-test-engineer or tdd-engineer | `qa` or `tdd` |
| Security Check | security-threat-analyst | `sec` |
| Code Review | code-reviewer | `cr` |
| Documentation | documentation-writer | `doc` |
| System Design | systems-architect | `arch` |
| Database Work | database-architect | `db` |
| Coordinate Work | product-manager-orchestrator | `pm` |
