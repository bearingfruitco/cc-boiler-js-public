# Example Workflows

> Real-world examples of using Claude Code Boilerplate v4.0.0 for common development tasks

## 📚 Quick Navigation

### By Task Type
- [Building a Feature from Scratch](#building-a-feature-from-scratch)
- [Adding Authentication](#adding-authentication)
- [Creating a Dashboard](#creating-a-dashboard)
- [Implementing Real-time Updates](#implementing-real-time-updates)
- [Optimizing Performance](#optimizing-performance)

### By Workflow Type
- [PRP-Driven Development](#prp-driven-development)
- [Multi-Agent Orchestration](#multi-agent-orchestration)
- [TDD Workflow](#tdd-workflow)
- [Bug Fix Workflow](#bug-fix-workflow)

---

## 🚀 Building a Feature from Scratch

### Scenario: User Profile Management

```bash
# 1. Start from GitHub issue
/fw start 45  # Issue: "Add user profile management"

# 2. Create comprehensive PRP
/create-prp user-profile-management

# 3. Review the generated PRP
# PRPs/active/user-profile-management.md created with:
# - Database schema
# - API endpoints
# - UI components
# - Validation rules
# - Security considerations

# 4. Execute with validation
/prp-execute user-profile --level 1  # Environment check

# 5. Implement database layer
/cc UserProfileSchema
# Implements schema from PRP...

# 6. Create API endpoints
/cc api/user-profile
# Uses exact patterns from PRP...

# 7. Build UI components
/cc UserProfileForm
# Follows design system strictly...

# 8. Progressive validation
/prp-execute user-profile --level 2  # Component tests
/prp-execute user-profile --level 3  # Integration
/prp-execute user-profile --level 4  # Production ready

# 9. Complete feature
/fw complete
```

**Result**: Feature implemented in one pass with all requirements met!

---

## 🔐 Adding Authentication

### Using Multi-Agent Orchestration

```bash
# 1. Orchestrate specialists
/orch implement Supabase authentication with social logins

# This automatically coordinates:
# - supabase-specialist: Auth schema and RLS
# - security: Threat modeling
# - backend: API implementation
# - frontend: UI components
# - qa: Test scenarios

# 2. Agents work in sequence
# Each agent builds on previous work
# Context flows naturally

# 3. Review combined output
/deps check auth  # See all created components

# 4. Test the implementation
/chain auth-testing
```

**Key Pattern**: Let orchestration handle complexity!

---

## 📊 Creating a Dashboard

### Visual-First Development

```bash
# 1. Visual planning
/vp analytics dashboard with charts and KPIs

# Creates visual mockup first
# Identifies all components needed

# 2. Generate component PRPs
/generate-component-prps dashboard

# Creates PRPs for each component:
# - ChartWidget.prp
# - KPICard.prp
# - DateRangePicker.prp

# 3. Parallel implementation
/chain parallel-components --prps=ChartWidget,KPICard,DateRangePicker

# 4. Compose into dashboard
/cc AnalyticsDashboard --compose
```

**Pattern**: Visual → Components → Composition

---

## 🔄 Implementing Real-time Updates

### Event-Driven Architecture

```bash
# 1. Design event schema
/spawn event-schema
"Design real-time notification system"

# 2. Implement event system
/create-event-handler notification-received

# Generates:
# - Type-safe event handler
# - Async processing
# - Error recovery
# - Audit logging

# 3. Connect to Supabase real-time
/chain supabase-realtime --table=notifications

# 4. Add UI updates
/cc NotificationBell --real-time
```

**Pattern**: Events → Handlers → UI Updates

---

## ⚡ Optimizing Performance

### Performance Chain Workflow

```bash
# 1. Baseline current performance
/performance-baseline

# 2. Run optimization chain
/chain performance-optimization-v4

# Coordinates:
# - performance agent: Identifies bottlenecks
# - analyzer: Deep dive into issues
# - refactoring-expert: Proposes solutions
# - qa: Validates improvements

# 3. Apply optimizations
/refactor --performance

# 4. Verify improvements
/performance-compare baseline
# Shows: 35% improvement in LCP
```

---

## 🧪 TDD Workflow

### Test-First Development

```bash
# 1. Start with TDD chain
/chain tdd-component --name=PricingCalculator

# Generates comprehensive test suite first

# 2. Run tests (should fail)
/tr PricingCalculator.test.tsx
# ❌ RED phase - tests fail

# 3. Implement minimal code
/cc PricingCalculator --minimal
# Just enough to make tests pass

# 4. Run tests again
/tr PricingCalculator.test.tsx
# ✅ GREEN phase - tests pass

# 5. Refactor with confidence
/refactor PricingCalculator --optimize
# Tests ensure nothing breaks

# 6. Add edge cases
/enhance-tests PricingCalculator
```

**Pattern**: Red → Green → Refactor → Enhance

---

## 🐛 Bug Fix Workflow

### Systematic Debugging

```bash
# 1. Capture bug
/bug-track "Users report checkout fails on mobile"

# 2. Visual debugging
# Take screenshot of issue
# Ctrl+V in Claude Code
"Why is the checkout button not working on mobile?"

# 3. Reproduce in browser
/btf checkout-flow
/pw-screenshot

# 4. Fix with validation
/fix-bug mobile-checkout

# 5. Verify fix
/pw-test mobile --flow=checkout

# 6. Prevent regression
/create-test checkout-mobile-regression
```

---

## 📝 Common Patterns

### Pattern 1: Always Validate Design
```bash
# Before any UI work
/vd

# After creating components
/validate-design

# In git pre-commit
# Automatic validation!
```

### Pattern 2: Use PRPs for Complex Features
```bash
# Don't jump to code
/create-prp feature-name

# PRPs include everything:
# - Exact code patterns
# - Security rules
# - Performance budgets
# - Test scenarios
```

### Pattern 3: Progressive Validation
```bash
# Don't wait until the end
/prp-execute feature --level 1  # Quick syntax
/prp-execute feature --level 2  # Components work
/prp-execute feature --level 3  # Integration OK
/prp-execute feature --level 4  # Production ready
```

### Pattern 4: Context Preservation
```bash
# Start of day
/sr  # Smart resume with full context

# Before break
/checkpoint create lunch

# Context never lost!
```

### Pattern 5: Parallel Work
```bash
# Don't do everything sequentially
/orch complex-feature

# Or manual parallel
/spawn frontend & /spawn backend

# Merge results
/merge-work frontend backend
```

---

## 🎯 Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Skipping PRPs
```bash
# Bad: Jump straight to code
/cc ComplexFeature  # Missing requirements!

# Good: PRP first
/create-prp complex-feature
/prp-execute complex-feature
```

### ❌ Anti-Pattern 2: Ignoring Validation
```bash
# Bad: Assume it works
/cc Button
# Move on...

# Good: Validate each step
/cc Button
/validate-design
/tr Button.test.tsx
```

### ❌ Anti-Pattern 3: Manual Orchestration
```bash
# Bad: Coordinate agents yourself
/spawn frontend
# wait...
/spawn backend
# wait...

# Good: Let orchestration handle it
/orch user-management-system
```

### ❌ Anti-Pattern 4: Late Testing
```bash
# Bad: Test after everything is built
# Build entire feature...
/test  # Find issues late!

# Good: Test continuously
/tdd feature  # Tests first
/prp-execute --level 2  # Test components
/prp-execute --level 3  # Test integration
```

---

## 💡 Pro Tips

1. **Use Command Aliases**: `/sr` instead of `/smart-resume`
2. **Chain Commands**: `/cc Button && /vd && /tr`
3. **Trust the System**: PRPs know your codebase better than you might
4. **Let Agents Specialize**: Don't make frontend agent do backend work
5. **Checkpoint Often**: The system auto-saves, but manual checkpoints help

---

## 📚 More Examples

- [Component Library Patterns](./component-patterns.md)
- [API Development Examples](./api-examples.md)
- [Testing Strategies](./testing-examples.md)
- [Deployment Workflows](./deployment-examples.md)

---

**Remember**: The boilerplate is designed to make you faster while maintaining quality. Trust the patterns, use the validation, and let the automation work for you!
