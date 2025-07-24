# 🚀 Parallel Orchestration Guide

> Master the art of multi-agent development with Claude Code's parallel orchestration features

## 📋 Table of Contents
1. [Overview](#overview)
2. [When to Use Parallel Orchestration](#when-to-use-parallel-orchestration)
3. [Core Commands](#core-commands)
4. [Orchestration Patterns](#orchestration-patterns)
5. [Git Worktrees](#git-worktrees)
6. [Multi-Agent Workflows](#multi-agent-workflows)
7. [Multi-Perspective Review](#multi-perspective-review)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

## Overview

Parallel orchestration enables multiple AI agents to work simultaneously on different aspects of your project, reducing development time by up to 70% for complex features.

### Key Benefits
- **3-5x faster** for multi-component features
- **Isolated development** prevents conflicts
- **Specialized agents** for optimal results
- **Automatic coordination** handles merging

## When to Use Parallel Orchestration

```mermaid
graph TD
    Task[New Task] --> Complexity{Complexity Check}
    
    Complexity -->|Single File| Sequential[Regular /pt]
    Complexity -->|2-3 Files| Consider[Consider /orch]
    Complexity -->|4+ Files| Parallel[Use /orch]
    Complexity -->|Multiple Domains| Definitely[Definitely /orch]
    
    Consider --> TimeCheck{Time Estimate}
    TimeCheck -->|< 30 min| Sequential
    TimeCheck -->|> 30 min| Parallel
    
    Definitely --> Types{Task Types}
    Types -->|Frontend + Backend| MultiAgent[/orch with specialized agents]
    Types -->|Multiple Features| Worktrees[/wt for isolation]
    Types -->|Review Needed| MPR[/mpr for perspectives]
```

### Ideal Scenarios

| Scenario | Command | Time Saved | Example |
|----------|---------|------------|---------|
| **Full CRUD Feature** | `/orch crud-feature` | 45-60 min | User management system |
| **Frontend + Backend** | `/orch --agents=2` | 30-40 min | API + React components |
| **Multiple Components** | `/wt ui api db` | 60-90 min | Complex features |
| **Architecture Changes** | `/mpr --full` | 2-3 hours | System refactoring |
| **Bug Fix + Tests** | `/orch --parallel` | 20-30 min | Fix with test coverage |

## Core Commands

### 1. Orchestrate Command (`/orch`)

```bash
# Basic orchestration
/orch feature-name

# With agent specification
/orch feature-name --agents=3

# Preview time savings
/orch feature-name --preview

# With specific domains
/orch auth --domains="frontend,backend,tests"
```

**Auto-spawned Agent Types:**
- **Frontend Agent**: UI/UX specialist
- **Backend Agent**: API/Database expert  
- **Test Agent**: Testing specialist
- **Security Agent**: Security analyzer
- **Performance Agent**: Optimization expert

### 2. Worktree Command (`/wt`)

```bash
# Create multiple worktrees
/wt auth payment ui

# List all worktrees
/wt-status

# Switch between worktrees
/wt-switch auth

# Create PR from worktree
/wt-pr auth

# Clean up worktree
/wt-clean auth
```

### 3. Multi-Perspective Review (`/mpr`)

```bash
# Review current changes
/mpr

# Review specific PR
/mpr --pr 156

# Full architecture review
/mpr --full

# Specific perspectives
/mpr --perspectives="security,performance"
```

## Orchestration Patterns

### Pattern 1: Feature Development

```mermaid
flowchart LR
    Feature[New Feature] --> Analyze[/orch --preview]
    
    Analyze --> Spawn{Spawn Agents}
    
    Spawn --> A1[Frontend Agent]
    Spawn --> A2[Backend Agent]
    Spawn --> A3[Test Agent]
    
    A1 --> Work1[Create Components]
    A2 --> Work2[Build API]
    A3 --> Work3[Write Tests]
    
    Work1 --> Monitor[/sas]
    Work2 --> Monitor
    Work3 --> Monitor
    
    Monitor --> Overview[/ov]
    Overview --> Merge[Auto-merge]
    Merge --> Review[/mpr]
```

### Pattern 2: Worktree Isolation

```mermaid
flowchart TD
    Complex[Complex Project] --> Split{Split Work}
    
    Split --> WT1[/wt auth]
    Split --> WT2[/wt payment]  
    Split --> WT3[/wt ui-refresh]
    
    WT1 --> Dev1[Develop Auth]
    WT2 --> Dev2[Develop Payment]
    WT3 --> Dev3[Refresh UI]
    
    Dev1 --> Test1[Test Isolated]
    Dev2 --> Test2[Test Isolated]
    Dev3 --> Test3[Test Isolated]
    
    Test1 --> PR1[/wt-pr auth]
    Test2 --> PR2[/wt-pr payment]
    Test3 --> PR3[/wt-pr ui-refresh]
    
    PR1 --> Merge[Merge Strategy]
    PR2 --> Merge
    PR3 --> Merge
```

### Pattern 3: Multi-Perspective Analysis

```mermaid
graph TB
    Code[Code Changes] --> MPR[/mpr]
    
    MPR --> P1[Security Review]
    MPR --> P2[Performance Analysis]
    MPR --> P3[UX Evaluation]
    MPR --> P4[Architecture Check]
    
    P1 --> R1[Security Report]
    P2 --> R2[Performance Metrics]
    P3 --> R3[UX Improvements]
    P4 --> R4[Architecture Issues]
    
    R1 --> Summary[Unified Report]
    R2 --> Summary
    R3 --> Summary
    R4 --> Summary
    
    Summary --> Action[Actionable Items]
```

## Git Worktrees

### Setup Workflow

```bash
# 1. Create feature worktrees
/wt auth payment notifications

# 2. Check status
/wt-status
# Shows:
# - auth (feature/auth) - Active
# - payment (feature/payment) - Active  
# - notifications (feature/notifications) - Active

# 3. Switch to work on auth
/wt-switch auth
/fw start 123  # Work normally

# 4. Switch to payment
/wt-switch payment
/fw start 124

# 5. Create PRs when ready
/wt-pr auth
/wt-pr payment
```

### Benefits
- **True isolation**: No file conflicts
- **Parallel testing**: Run tests simultaneously
- **Easy switching**: Context preserved
- **Clean PRs**: One feature per PR

## Multi-Agent Workflows

### Automatic Agent Specialization

```typescript
// The system automatically assigns specialists based on task analysis

interface AgentSpecialization {
  "UI/UX Expert": ["components", "styling", "responsive", "accessibility"],
  "Backend Specialist": ["api", "database", "authentication", "validation"],
  "Test Engineer": ["unit tests", "integration", "e2e", "coverage"],
  "Security Analyst": ["vulnerabilities", "authentication", "encryption"],
  "Performance Expert": ["optimization", "caching", "queries", "bundle size"]
}
```

### Example: E-commerce Checkout

```bash
# 1. Analyze the feature
/orch checkout-flow --preview
# Output: "Can save ~45 minutes with 3 parallel agents"

# 2. Start orchestration
/orch checkout-flow --agents=3

# Agent 1 (Frontend): Cart UI, payment form, confirmation page
# Agent 2 (Backend): Payment processing, order creation, inventory
# Agent 3 (Testing): Unit tests, integration tests, e2e flows

# 3. Monitor progress
/sas  # See all sub-agents
# Shows real-time progress of each agent

# 4. Get overview
/ov   # Orchestration view
# Shows task dependencies and completion

# 5. Review all work
/mpr --full
# Multi-perspective review of all changes
```

## Multi-Perspective Review

### Review Perspectives

| Perspective | Focus Areas | Key Questions |
|-------------|-------------|---------------|
| **Security** | Auth, data, vulnerabilities | Is data protected? Any OWASP issues? |
| **Performance** | Speed, memory, efficiency | Bundle size? Query optimization? |
| **UX** | Usability, accessibility | Intuitive? A11y compliant? |
| **Architecture** | Structure, patterns, scaling | Maintainable? Scalable? |
| **Business** | ROI, features, value | Meets requirements? Business value? |

### Review Workflow

```bash
# Standard review
/mpr
# Analyzes current changes from all perspectives

# PR-specific review  
/mpr --pr 234
# Reviews PR #234 from multiple angles

# Custom perspectives
/mpr --perspectives="security,performance,business"
# Focused review on specific areas

# Full architecture review
/mpr --full --include-tests
# Comprehensive system analysis
```

### Review Output Example

```markdown
## Multi-Perspective Review Report

### 🔒 Security Perspective
- ✅ Authentication properly implemented
- ⚠️ Consider rate limiting on /api/checkout
- ✅ PII encryption in place

### ⚡ Performance Perspective  
- ✅ Bundle size within limits (142kb)
- ⚠️ Database query in loop detected (line 234)
- 💡 Consider caching user preferences

### 🎨 UX Perspective
- ✅ Mobile responsive
- ⚠️ Loading states missing on 2 buttons
- ✅ Accessibility score: 98/100

### 🏗️ Architecture Perspective
- ✅ Follows established patterns
- 💡 Consider extracting payment logic to service
- ✅ Good test coverage (87%)

### Recommended Actions
1. Add rate limiting to checkout API
2. Fix N+1 query issue  
3. Add loading states to form buttons
```

## Best Practices

### 1. Choose the Right Approach

```mermaid
graph LR
    Start[Task] --> Size{Size?}
    
    Size -->|Small| Regular[/pt]
    Size -->|Medium| Check{Check Complexity}
    Size -->|Large| Orchestrate[/orch]
    
    Check -->|Simple| Regular
    Check -->|Complex| Orchestrate
    
    Orchestrate --> Isolated{Need Isolation?}
    Isolated -->|Yes| Worktree[/wt]
    Isolated -->|No| Standard[/orch]
```

### 2. Agent Communication

- Agents automatically share context via `.claude/orchestration/`
- Use `/sas` to monitor agent communication
- Conflicts are auto-resolved with priorities

### 3. Efficient Worktree Usage

```bash
# DO: Create worktrees for independent features
/wt auth payment ui

# DON'T: Create worktrees for dependent features
/wt api api-tests  # Tests depend on API

# DO: Clean up after merging
/wt-clean auth

# DON'T: Keep stale worktrees
/wt-status  # Check regularly
```

### 4. Timing Your Reviews

- **Early**: `/mpr --draft` for approach validation
- **Mid-development**: `/mpr` for course correction  
- **Pre-PR**: `/mpr --full` for comprehensive check
- **Post-merge**: `/mpr --retro` for learnings

## Troubleshooting

### Common Issues

| Issue | Solution | Prevention |
|-------|----------|------------|
| **Agents conflicting** | Use `/ov` to see dependencies | Better task splitting |
| **Worktree merge conflicts** | `/wt-sync main` regularly | Frequent syncs |
| **Agent stuck** | `/sa-abort [id]` to stop | Clearer task definition |
| **Review too broad** | Use `--perspectives` flag | Focused reviews |
| **Orchestration slow** | Check with `--preview` first | Right-size agent count |

### Debug Commands

```bash
# Check orchestration health
/orch-health

# View agent logs
/sa-logs [agent-id]

# Force sync worktrees
/wt-sync --all

# Reset orchestration
/orch-reset
```

## Real-World Examples

### Example 1: SaaS Dashboard

```bash
# 1. Plan the work
/ut "saas dashboard implementation"

# 2. Create worktrees for parallel development
/wt analytics billing usage-charts

# 3. In each worktree, run specialized work
/wt-switch analytics
/orch analytics-feature --agents=2

/wt-switch billing  
/orch billing-feature --agents=2

/wt-switch usage-charts
/cc UsageChart && /vp "chart design"

# 4. Review everything
/mpr --full --all-worktrees

# 5. Create PRs
/wt-pr analytics
/wt-pr billing
/wt-pr usage-charts
```

### Example 2: API Refactoring

```bash
# 1. Analyze impact
/ut "api v2 migration strategy"

# 2. Orchestrate the refactor
/orch api-v2 --agents=4
# Agent 1: Core API changes
# Agent 2: Update tests
# Agent 3: Migration scripts
# Agent 4: Documentation

# 3. Monitor progress
/sas --watch

# 4. Multi-perspective review
/mpr --perspectives="architecture,performance,security"

# 5. Create unified PR
/fw complete --squash
```

## Performance Metrics

Based on real project data:

| Feature Type | Sequential Time | Parallel Time | Time Saved | Agents Used |
|--------------|----------------|---------------|------------|-------------|
| CRUD Feature | 120 min | 35 min | 71% | 3 |
| UI Component Set | 90 min | 30 min | 67% | 3 |
| API + Frontend | 150 min | 50 min | 67% | 2 |
| Full Feature | 240 min | 75 min | 69% | 4 |
| Bug Fix + Tests | 45 min | 20 min | 56% | 2 |

## Summary

Parallel orchestration transforms complex development tasks from sequential slogs into efficient parallel workflows. Key takeaways:

1. **Use `/orch` for any task over 30 minutes**
2. **Use `/wt` for truly independent features**
3. **Always `/mpr` before merging**
4. **Monitor with `/sas` and `/ov`**
5. **Trust the preview estimates**

Remember: The system automatically handles the complexity of parallel work - you just need to choose when to use it!
