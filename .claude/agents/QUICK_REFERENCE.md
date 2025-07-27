# Sub-Agent Quick Reference Guide

## 🚀 Available Sub-Agents (24 total)

Your Claude Code system includes 24 specialized sub-agents that can be invoked to handle specific tasks with expertise.

## 📍 Quick Start

### Basic Usage
```
use [agent-name] subagent to [task description]
```

### Using Aliases (Faster!)
```
[alias] [task description]
```

## ⚡ Essential Aliases

| Alias | Full Agent Name | Best For |
|-------|----------------|----------|
| `fe` | frontend-ux-specialist | UI components, design system compliance |
| `be` | backend-reliability-engineer | APIs, error handling, reliability |
| `qa` | qa-test-engineer | Test generation, test automation |
| `sec` | security-threat-analyst | Security audits, vulnerability scanning |
| `tdd` | tdd-engineer | Test-driven development workflow |
| `cr` | code-reviewer | Code reviews, PR analysis |
| `doc` | documentation-writer | Technical docs, API references |
| `pm` | product-manager-orchestrator | Multi-agent coordination |

## 🤖 All Sub-Agents by Category

### Core Development (5)
- **frontend-ux-specialist** (`fe`) - UI/UX with strict design system
- **backend-reliability-engineer** (`be`) - Reliable APIs and services  
- **systems-architect** (`arch`) - System design and architecture
- **senior-engineer** (`senior`) - Full-stack implementation
- **tdd-engineer** (`tdd`) - Test-driven development

### Quality & Testing (4)
- **qa-test-engineer** (`qa`) - Test generation and automation
- **code-reviewer** (`cr`) - Code review and quality checks
- **production-code-validator** (`prod-val`) - Production readiness
- **mentor** (`mentor`) - Code guidance and best practices

### Analysis & Security (5)
- **security-threat-analyst** (`sec`/`sa`) - Security audits
- **analyzer** (`debug`/`analyzer`) - Code analysis and debugging
- **performance** (`perf`) - Performance optimization
- **researcher** (`research`) - Deep technical research
- **pii-guardian** (`pii`) - PII protection and compliance

### Data & Infrastructure (3)
- **database-architect** (`db`) - Database design
- **migration-specialist** (`migrate`) - Data migrations
- **automation-workflow-engineer** (`auto`) - Workflow automation

### Documentation & Planning (4)
- **documentation-writer** (`doc`) - Technical documentation
- **prd-writer** (`prd-writer`) - Product requirements
- **report-generator** (`report`) - Comprehensive reports
- **pm-orchestrator** (`pm`) - Project coordination

### Specialized (3)
- **form-builder-specialist** (`forms`) - Advanced forms
- **refactoring-expert** (`refactor`) - Code refactoring
- **financial-analyst** (`fin`) - Financial analysis

## 💡 Common Workflows

### Feature Development
```bash
# Full TDD workflow
pm orchestrate new feature → arch design → tdd tests → fe/be implement → cr review

# Quick implementation
fe build login form
be create auth endpoint
qa test authentication flow
```

### Security Audit
```bash
# Comprehensive security check
sec audit entire codebase
be implement security fixes
qa verify security measures
doc update security documentation
```

### Code Quality
```bash
# Review and refactor
cr review recent changes
refactor improve code structure
perf optimize performance
doc update documentation
```

### Database Work
```bash
# Schema design and migration
db design user schema
migrate create migration plan
be update API endpoints
qa test data integrity
```

## 🔄 Automatic Suggestions

The system automatically suggests relevant agents based on:
- File type you're working on
- Keywords in file paths
- Current task context
- Previous agent usage

## 📝 Examples

### Quick Tasks
```bash
# Frontend work
fe make navbar responsive

# Backend work  
be add rate limiting

# Testing
qa create unit tests

# Security
sec check for vulnerabilities

# Documentation
doc update API docs
```

### Complex Tasks
```bash
# Full feature with description
pm orchestrate complete user authentication system with email verification, password reset, and 2FA support

# Detailed security audit
sec perform comprehensive security audit focusing on authentication, authorization, input validation, and API security

# Architecture design
arch design scalable microservices architecture for e-commerce platform with high availability requirements
```

## 🎯 Best Practices

1. **Start with PM for complex features** - Orchestrates other agents
2. **Use TDD for new development** - Write tests first
3. **Always run security checks** - Before deployment
4. **Document as you go** - Keep docs updated
5. **Review before merging** - Use code-reviewer

## 🔗 Chaining Agents

Agents work best when chained for complex workflows:

```bash
# Sequential execution
arch design → tdd test → be implement → cr review → doc document

# Parallel execution  
pm orchestrate parallel execution:
  - fe build UI components
  - be create API endpoints
  - qa write test suites
```

## 📊 Agent Capabilities

### Full Access Agents
These agents can read, write, and execute:
- pm-orchestrator
- senior-engineer
- backend-reliability-engineer
- migration-specialist
- automation-workflow-engineer

### Implementation Agents
These agents can read and write code:
- frontend-ux-specialist
- systems-architect
- qa-test-engineer
- database-architect
- refactoring-expert

### Analysis Agents
These agents primarily read and analyze:
- security-threat-analyst
- code-analyzer-debugger
- performance-optimizer
- researcher
- production-code-validator

## 🛠️ Troubleshooting

### Agent Not Found?
- Check spelling of agent name
- Use full name: `use [full-agent-name] subagent to`
- Check if agent file exists in `.claude/agents/`

### Alias Not Working?
- Check `.claude/aliases.json` for correct mapping
- Use the `/help` command to see all aliases
- Try the full agent invocation syntax

### Need Help Choosing?
- Let the system suggest based on context
- Use `pm` to orchestrate multiple agents
- Check this guide for best agent match

## 🚦 Quick Decision Tree

```
Need to build UI? → fe
Need to build API? → be
Need to write tests? → qa or tdd
Need security review? → sec
Need code review? → cr
Need documentation? → doc
Need system design? → arch
Need to coordinate? → pm
Not sure? → pm orchestrate and describe your need
```

---

Remember: Agents are here to help! Use them liberally to maintain high code quality and productivity.
