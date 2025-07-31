# Claude Code Boilerplate v4.0.0 - Complete Workflow Guide

> Master the AI-assisted development workflows that make you 70% faster while maintaining higher quality.

## 🎯 Core Development Workflows

### 1. The Modern Flow: PRD → Architecture → PRP → Implementation

This is the v4.0.0 recommended workflow for maximum efficiency:

```bash
# 1. Start with requirements (from issue or idea)
/fw start 123              # From GitHub issue #123
# OR
/create-prd user-profile   # From scratch

# 2. Architecture phase (v4.0.0 feature)
/chain architecture-design

# This spawns multiple agents:
# - system-architect: Overall design
# - database-architect: Optimal schemas  
# - security-threat-analyst: Threat model
# - event-schema: Data model design

# Outputs:
# - system-design.md
# - database-schema.md
# - security-design.md
# - Multiple PRPs for implementation

# 3. Implementation phase with PRPs
/prp-execute database-prp --level 1    # Validate environment
# ... implement database ...

/prp-execute api-prp --level 1         # Validate API setup
# ... implement API ...

/prp-execute frontend-prp --level 1    # Validate UI setup
# ... implement UI ...

# 4. Progressive validation
/prp-execute [name] --level 2  # Component testing
/prp-execute [name] --level 3  # Integration testing  
/prp-execute [name] --level 4  # Production readiness

# 5. Completion
/grade                  # Score alignment with PRD
/fw complete           # Create PR with full context
```

### 2. Quick Feature Development (When Requirements are Clear)

```bash
# Direct to PRP when you know what to build
/fw start 45
/create-prp contact-form

# PRP includes everything needed:
# - Exact code patterns from your codebase
# - Database schema with RLS
# - API endpoints with validation
# - UI components with design system
# - Event tracking implementation
# - Test scenarios

# Implement with confidence
/gt contact-form       # Break into micro-tasks
/pt contact-form       # Process systematically

# Validate at each level
/prp-execute contact-form --level 1  # Quick checks
/prp-execute contact-form --level 2  # Component tests
/prp-execute contact-form --level 3  # Integration
/prp-execute contact-form --level 4  # Production
```

### 3. Exploratory Development (When Discovering Requirements)

```bash
# Start with exploration
/prd experimental-feature

# Deep thinking mode
/ut "What's the best approach for [feature]?"

# Visual planning
/vp experimental-feature

# Iterate on PRD
/enhance-prd experimental-feature

# Once clear, generate PRP
/prd-to-prp experimental-feature

# Then follow standard flow
```

## 🔄 Daily Development Patterns

### Morning Routine

```bash
# 1. Smart resume with context
/sr

# 2. Check for automated suggestions
/chain check
# May suggest:
# - morning-startup (if first command)
# - error-recovery (if issues detected)
# - continue-feature (if work in progress)

# 3. Review status
/bt list --open        # Open bugs
/fw status            # Active features
/deps health          # Dependency issues
/todo                 # Task list

# 4. Load working profile
/cp load frontend     # Or backend, fullstack, etc.
```

### During Development

#### Creating Components
```bash
# Always check first (automatic in v4.0.0)
/exists Button

# Create with validation
/cc Button
# Automatically:
# - Validates design system
# - Generates tests
# - Adds to exports
# - Updates dependencies

# With specific options
/cc Button --variant=primary,secondary --size=sm,md,lg
```

#### Working with Forms
```bash
# Secure form with tracking
/ctf LeadForm --vertical=debt --compliance=tcpa

# This generates:
# - PII field encryption
# - Non-blocking event tracking
# - TCPA compliance features
# - Loading states
# - Error handling
```

#### Debugging Issues
```bash
# Visual debugging (NEW in v4.0.0)
# 1. Take screenshot of issue
# 2. Ctrl+V in Claude Code
# 3. "Why is the button misaligned?"
# 4. Get visual analysis with fix

# Traditional debugging
/spawn analyzer
"Trace through checkout flow"

# Browser debugging
/btf
/pw-console           # See browser console
/pw-screenshot       # Capture state
```

#### Managing Dependencies
```bash
# Before modifying shared components
/deps check Button
# Shows:
# - 5 components use Button
# - 2 tests import Button
# - No circular dependencies

# After modifications
/deps scan
# Updates all dependency tracking
```

### Before Committing

```bash
# Automated validation chain
/chain pre-commit

# Or manually:
/vd                    # Design system check
/validate-async        # Async patterns
/tr                    # Run tests
/lint                  # Fix formatting

# Git commit (pre-commit hooks run automatically)
git add .
git commit -m "feat: add contact form"

# Pre-commit validates:
# ✓ Design compliance
# ✓ TypeScript validity
# ✓ Test coverage
# ✓ No console.logs
# ✓ PRP compliance (if active)
```

## 🤖 Multi-Agent Orchestration

### Understanding the 31 Agents

#### Technology Specialists (v4.0.0 additions)
- `supabase-specialist` - Database, RLS, real-time
- `playwright-specialist` - Browser automation, testing
- `analytics-engineer` - Tracking, data pipelines
- `platform-deployment` - Vercel, edge optimization
- `privacy-compliance` - GDPR, CCPA, data handling
- `orm-specialist` - Drizzle, Prisma optimization
- `event-schema` - Event design, taxonomy

#### Core Development Team
- `frontend` - React, Next.js, UI
- `backend` - APIs, server logic
- `security` - Vulnerabilities, auth
- `qa` - Test strategies, quality
- `performance` - Optimization, metrics

#### Architecture & Planning
- `system-architect` - Technical design
- `database-architect` - Schema optimization
- `pm-orchestrator` - Coordination, planning

### Orchestration Patterns

#### Automatic Orchestration
```bash
# Let system choose agents
/orch user-authentication

# System analyzes needs and spawns:
# - security (auth strategy)
# - database-architect (user schema)
# - backend (API implementation)
# - frontend (UI components)
# - qa (test scenarios)
```

#### Manual Orchestration
```bash
# Specific agent combination
/spawn backend
"Design payment processing API"

/spawn security
"Review payment API for PCI compliance"

/spawn qa
"Create test scenarios for payment flow"
```

#### Parallel Analysis
```bash
# Multiple perspectives simultaneously
/chain multi-perspective-review

# Spawns in parallel:
# - security review
# - performance analysis
# - UX evaluation
# - architecture review
# Then synthesizes findings
```

## 🔗 Smart Chains (Automated Workflows)

### Understanding Chain Features

Chains support:
- **Auto-triggers** - Detect conditions and prompt
- **Prerequisites** - Ensure readiness
- **Context passing** - Share data between steps
- **Conditional logic** - Dynamic flow
- **Parallel execution** - Speed up workflows

### Common Chain Workflows

#### Feature Development Chain (v4.0.0)
```bash
/chain feature-development-v4 --feature="shopping-cart"

# Phases:
# 1. Planning (parallel)
#    - PM breaks down requirements
#    - Architect designs system
#    - QA creates test plan
#
# 2. Implementation (parallel)
#    - TDD engineer writes tests
#    - Backend implements API
#    - Frontend builds UI
#    - Analytics adds tracking
#
# 3. Review (parallel)
#    - Code review
#    - Security audit
#    - Performance check
#    - Compliance review
```

#### Morning Setup Chain
```bash
/chain morning-setup

# Automatically runs:
# - Smart resume
# - Dependency check
# - Test status
# - Security scan
# - Open issues review
```

#### Pre-PR Chain
```bash
/chain pre-pr

# Ensures:
# - All tests pass
# - Design compliance
# - No security issues
# - Performance budgets met
# - Documentation updated
```

### Creating Custom Chains

Add to `.claude/chains.json`:

```json
{
  "my-deployment": {
    "description": "Custom deployment workflow",
    "triggers": {
      "conditions": {
        "all": ["tests.passing", "pr.approved"]
      },
      "prompt": "Ready to deploy. Proceed? (y/n)"
    },
    "steps": [
      "/sv check production",
      "/chain pre-deploy-security",
      "/deploy staging",
      "/smoke-test staging",
      {
        "condition": "smokeTest.passing",
        "command": "/deploy production"
      }
    ],
    "on-success": "/notify team 'Deployment successful'",
    "on-failure": "/rollback && /notify team 'Deployment failed'"
  }
}
```

## 🎭 Advanced Workflows

### Test-Driven Development (TDD)

```bash
# 1. Start with tests
/tdd Button
# Generates comprehensive test suite

# 2. Run tests (should fail)
/tr Button.test.tsx
# ❌ RED phase

# 3. Implement minimal code
/cc Button --minimal

# 4. Run tests (should pass)
/tr Button.test.tsx
# ✅ GREEN phase

# 5. Refactor with safety
/refactor Button
# Tests ensure nothing breaks
```

### Browser-Driven Development

```bash
# 1. Create with browser testing
/chain browser-verified-component --name=SearchBar

# Agents work together:
# - UI creates component
# - Playwright verifies rendering
# - QA creates interaction tests
# - Performance checks metrics

# 2. Visual regression testing
/pw-baseline capture     # Before changes
# ... make changes ...
/pw-baseline compare     # After changes
```

### Security-First API Development

```bash
# 1. Start with security
/chain security-first-api-v4 --name=payments

# Process:
# - Threat analysis first
# - Security rules generation
# - RLS policies created
# - Tests written for vulnerabilities
# - Implementation with controls
# - Security audit

# 2. Continuous security
/spawn-security-auditor --watch
# Monitors all changes for security issues
```

### Performance-Driven Refactoring

```bash
# 1. Baseline current performance
/performance-baseline

# 2. Analyze bottlenecks
/chain performance-optimization-v4

# 3. Implement improvements
# Agents optimize:
# - Database queries
# - Bundle sizes
# - API responses
# - Edge caching

# 4. Verify improvements
/performance-compare baseline
# Expect 20%+ improvement
```

## 📊 Validation & Quality Gates

### The 4-Level System

#### Level 1: Syntax & Standards (Continuous)
```bash
# Runs automatically on save
# Can run manually:
/prp-execute feature --level 1

# Checks:
# ✓ Linting (Biome)
# ✓ TypeScript
# ✓ Design system
# ✓ Import paths
```

#### Level 2: Component Testing (Per Component)
```bash
/prp-execute feature --level 2

# Runs:
# ✓ Unit tests
# ✓ Component tests
# ✓ Hook tests
# ✓ Isolated checks
```

#### Level 3: Integration Testing (Connected Systems)
```bash
/prp-execute feature --level 3

# Validates:
# ✓ E2E tests
# ✓ API integration
# ✓ Database queries
# ✓ User workflows
```

#### Level 4: Production Readiness (Pre-Deploy)
```bash
/prp-execute feature --level 4

# Ensures:
# ✓ Performance budgets
# ✓ Security audit
# ✓ Accessibility
# ✓ Bundle size
# ✓ Error handling
```

### Automatic Fixes

```bash
# Run validation with auto-fix
/prp-execute feature --fix

# Fixes:
# - Simple design violations
# - Import paths
# - Formatting issues
# - Some TypeScript errors
```

## 🚀 Deployment Workflows

### Staging Deployment

```bash
/chain safe-staging-deploy

# Validates:
# - Environment variables
# - All tests pass
# - Security clearance
# - Performance baseline

# Deploys and verifies:
# - Smoke tests
# - Performance comparison
# - Error monitoring
```

### Production Deployment

```bash
/chain safe-production-deploy

# Requires:
# - Manual confirmation
# - All staging tests pass
# - Performance verification
# - Security sign-off

# Includes:
# - Automatic rollback
# - Team notifications
# - Monitoring alerts
```

## 💡 Productivity Tips

### Context Management
```bash
# Save specialized contexts
/cp create "payment-feature"
/cp save "Working on Stripe integration"

# Quick switch between features
/cp load "user-dashboard"
/cp load "payment-feature"
```

### Token Optimization
```bash
# When context gets large
/compress

# Intelligently:
# - Summarizes old conversations
# - Keeps critical context
# - Archives research
# - Maintains continuity
```

### Parallel Development
```bash
# Work on multiple features
/wt create feature-1
/wt create feature-2

# Switch between them
/wt switch feature-1
# ... work ...
/wt switch feature-2
# ... work ...

# Merge when ready
/wt merge feature-1
```

### Knowledge Building
```bash
# Extract patterns from success
/specs extract

# Builds library of:
# - Successful PRD→Implementation patterns
# - Common solutions
# - Team conventions
# - Reusable components
```

## 🎓 Learning & Improvement

### For New Team Members
```bash
# Generate personalized onboarding
/chain team-onboarding --role=frontend

# Creates:
# - Codebase overview
# - Common patterns
# - Workflow guide
# - First tasks
```

### Continuous Learning
```bash
# Weekly reviews
/metrics report        # See productivity gains
/patterns review      # New patterns to adopt
/bugs analyze        # Common issues to avoid

# Monthly optimization
/optimize-commands    # Streamline workflows
/update-agents       # Enhance capabilities
```

## 🆘 Troubleshooting Workflows

### When Stuck
```bash
# Context-aware help
/help

# Deep analysis
/ut "I'm stuck on [problem]"

# Get expert help
/spawn mentor
"How do I approach [challenge]?"
```

### When Things Break
```bash
# Automatic recovery
/chain error-recovery

# Manual recovery
/checkpoint restore [name]
/deps check --health
/error-recovery build
```

### When Slow
```bash
# Performance analysis
/performance-monitor check
/validate-async          # Find blocking code
/optimize-bundle        # Reduce size
/chain performance-optimization-v4
```

---

**Remember**: The system adapts to your workflow. Start simple, add complexity as needed.

**Pro Tip**: Let the system work for you. Use `/chain check` frequently - it knows when to help.

**Version**: 4.0.0 - "Automation & Intelligence"
