# PRP (Product Requirement Prompt) Workflow Guide

> Complete guide to using PRPs for one-pass implementation success

## What is a PRP?

A **Product Requirement Prompt (PRP)** is an enhanced specification that provides AI coding agents with everything needed to deliver production-ready code on the first attempt. It combines:

1. **Product Requirements** - What to build and why
2. **Codebase Intelligence** - Exact patterns, examples, and gotchas from your codebase
3. **Validation Loops** - Automated quality gates at each development stage

## PRP vs PRD

| Aspect | PRD | PRP |
|--------|-----|-----|
| **Focus** | What & Why | What, Why & How |
| **Level** | Business/Feature | Implementation |
| **Context** | General requirements | Specific code patterns |
| **Validation** | Manual review | Automated loops |
| **Goal** | Define the problem | Solve it in one pass |

## When to Use PRPs

### Use PRPs for:
- ✅ New features with clear scope
- ✅ Component development
- ✅ API endpoints
- ✅ Refactoring with specific goals
- ✅ Bug fixes with known solutions

### Use PRDs for:
- 📋 High-level product planning
- 📋 Multi-phase features
- 📋 Exploratory development
- 📋 Stakeholder communication

## Basic PRP Workflow

### 1. Create a PRP

```bash
# From a description
/create-prp user authentication with JWT and refresh tokens

# Short alias
/prp responsive data table with sorting

# From GitHub issue
/fw start 123
/prp implement issue #123
```

### 2. Review and Enhance

The PRP will be created in `PRPs/active/[feature-name].md`. Review it and:

- ✅ Verify goal matches your intent
- ✅ Check success criteria are measurable
- ✅ Add any missing context or gotchas
- ✅ Ensure validation loops are appropriate

### 3. Run Initial Validation

```bash
# Check if environment is ready
/prp-execute user-auth --level 1

# Output:
# ✅ Level 1: Syntax & Standards
#   ✓ bun run lint:fix (312ms)
#   ✓ bun run typecheck (1847ms)
#   ✓ /vd (89ms)
```

### 4. Implement Following Blueprint

The PRP provides a step-by-step implementation plan. Follow it phase by phase:

```typescript
// Phase 1: Data Layer (from PRP)
// 1. Create schema as specified
// 2. Enable RLS with provided policies
// 3. Create API routes

// Phase 2: Components (from PRP)
// 1. Build with design system classes
// 2. Add loading states
// 3. Implement error boundaries
```

### 5. Validate After Each Phase

```bash
# After Phase 1 (backend)
/prp-execute user-auth --level 2

# After Phase 2 (frontend)
/prp-execute user-auth --level 3

# Before PR
/prp-execute user-auth --level 4
```

## Advanced Workflows

### Interactive Development

```bash
# Interactive mode prompts on failures
/prp-execute feature --interactive

# Example interaction:
# ❌ Level 2 failed: Component test missing
# Continue anyway? (y/N): y
```

### Auto-Fix Mode

```bash
# Automatically fix what's possible
/prp-execute feature --fix

# What gets auto-fixed:
# - Linting issues
# - Formatting
# - Simple TypeScript errors
# - Import sorting
```

### Parallel Development

```bash
# Create multiple PRPs for a large feature
/prp user-profile-display
/prp user-profile-edit
/prp user-avatar-upload

# Work on them in parallel
/prp-execute user-profile-* --level 1
```

### CI/CD Integration

```yaml
# .github/workflows/prp-validation.yml
- name: Validate PRP Implementation
  run: |
    bun run PRPs/scripts/prp-runner.ts \
      --prp ${{ github.event.pull_request.title }} \
      --output-format json \
      > validation-results.json
```

## PRP Validation Levels

### 🔴 Level 1: Syntax & Standards
**When**: Continuously during development
**What**: Code quality basics
```bash
/prp-execute feature --level 1
```
- Linting (Biome)
- TypeScript checking
- Design system compliance
- Import validation

### 🟡 Level 2: Component Testing  
**When**: After building each component
**What**: Isolated functionality
```bash
/prp-execute feature --level 2
```
- Unit tests
- Component tests
- Hook tests
- Mocked dependencies

### 🟢 Level 3: Integration Testing
**When**: After connecting components
**What**: Full feature flow
```bash
/prp-execute feature --level 3
```
- E2E tests
- API integration
- Real database queries
- User workflows

### 🔵 Level 4: Production Readiness
**When**: Before creating PR
**What**: Performance & quality
```bash
/prp-execute feature --level 4
```
- Lighthouse scores
- Bundle size analysis
- Security audit
- Requirement grading

## Common PRP Patterns

### Component PRP
```bash
/prp data table with virtual scrolling

# Creates PRP with:
# - TypeScript interfaces
# - Design system compliance
# - Performance requirements
# - Accessibility standards
```

### API Endpoint PRP
```bash
/prp REST API for user management

# Creates PRP with:
# - Route structure
# - Request/response types
# - Error handling patterns
# - Rate limiting
```

### Feature PRP
```bash
/prp checkout flow with Stripe

# Creates PRP with:
# - Multi-phase implementation
# - External API integration
# - Security requirements
# - Testing strategies
```

## Tips for Success

### 1. Be Specific in PRPs
```bash
# ❌ Too vague
/prp user settings

# ✅ Specific
/prp user notification settings with email/SMS preferences and frequency control
```

### 2. Include Performance Requirements
```bash
/prp infinite scroll feed with <100ms render time for 1000 items
```

### 3. Reference Existing Patterns
```bash
# In your PRP request
/prp payment form similar to ContactForm but with Stripe Elements
```

### 4. Chain PRPs for Large Features
```bash
# Break down large features
/prp step 1: authentication flow UI
/prp step 2: authentication API endpoints  
/prp step 3: authentication state management
```

## Troubleshooting

### "PRP not found"
```bash
# Check active PRPs
ls PRPs/active/

# Use exact name
/prp-execute exact-feature-name
```

### "Validation keeps failing"
```bash
# Run with verbose output
/prp-execute feature --verbose

# Check specific level
/prp-execute feature --level 2 --verbose

# Skip problematic validation
/prp-execute feature --skip "E2E Tests"
```

### "Takes too long"
```bash
# Run only critical levels during development
/prp-execute feature --level 1,2

# Run full validation before PR
/prp-execute feature
```

## Best Practices

### 1. PRP Lifecycle
```
Create → Validate L1 → Implement → Validate L2 → 
Connect → Validate L3 → Polish → Validate L4 → PR
```

### 2. Keep PRPs Updated
- Update PRPs as requirements change
- Document new gotchas discovered
- Extract patterns for future PRPs

### 3. Use AI Documentation
Reference the pre-digested docs in `PRPs/ai_docs/`:
- `nextjs15-app-router.md`
- `supabase-patterns.md`
- Add your own for frequently used libraries

### 4. Combine with Existing Tools
```bash
# Start with issue
/fw start 123

# Create PRP
/prp implement issue #123

# Pin requirements
/pin-requirements 123

# Validate includes pinned requirements
/prp-execute feature

# Grade final implementation
/grade --requirements
```

## Example: Complete Feature with PRP

```bash
# 1. Start from GitHub issue
/fw start 45  # "Add user avatar upload"

# 2. Create comprehensive PRP
/prp user avatar upload with crop and preview

# 3. Initial validation
/prp-execute user-avatar-upload --level 1

# 4. Implement Phase 1 (Backend)
# - Create storage bucket
# - Add API endpoint
# - Set up policies

# 5. Validate backend
/prp-execute user-avatar-upload --level 2

# 6. Implement Phase 2 (Frontend)
# - Upload component
# - Crop interface
# - Preview display

# 7. Validate integration
/prp-execute user-avatar-upload --level 3

# 8. Polish and optimize
# - Add loading states
# - Error handling
# - Performance optimization

# 9. Final validation
/prp-execute user-avatar-upload

# 10. Create PR with context
/fw complete
```

## Integration with Team Workflow

### For Solo Development
1. Use PRPs for all new features
2. Run Level 1 continuously
3. Full validation before commits

### For Team Development
1. Share PRPs in `PRPs/completed/`
2. Reference successful patterns
3. Update AI docs with learnings
4. Use PR validation in CI

### For AI Pair Programming
1. Generate PRP at start of session
2. AI follows blueprint exactly
3. Validation ensures compliance
4. Grade measures success

## Summary

PRPs transform AI-assisted development by providing:
- **Complete Context**: Everything needed upfront
- **Quality Gates**: Automated validation at each stage  
- **One-Pass Success**: No back-and-forth iterations
- **Pattern Reuse**: Learn from successful implementations

The goal: Production-ready code on the first attempt through comprehensive context and validation.
