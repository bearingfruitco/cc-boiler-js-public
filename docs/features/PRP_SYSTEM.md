# Product Requirement Prompts (PRP) System

> One-pass implementation with complete context and validation

## 🎯 What is a PRP?

A PRP (Product Requirement Prompt) is an AI-optimized specification that provides everything needed for production-ready implementation in a single pass:

1. **Product Requirements** - Clear definition of what to build
2. **Codebase Intelligence** - Exact patterns, gotchas, and examples from your code
3. **Validation Loops** - 4-level quality gates ensuring production readiness
4. **AI Documentation** - Pre-digested technical knowledge

## 🚀 Quick Start

### 1. Create a PRP
```bash
/create-prp user authentication
# or
/prp checkout flow with Stripe
```

### 2. Review Generated PRP
The PRP is saved to `PRPs/active/[feature-name].md`

### 3. Execute Validation
```bash
/prp-execute user-auth
# or with auto-fix
/prp-execute user-auth --fix
```

### 4. Implement Following Blueprint
The PRP provides step-by-step implementation guidance

## 📊 PRP Structure

### 1. Header Section
```markdown
# PRP: [Feature Name]
Version: 1.0
Status: Active
Requirements: Links to GitHub issues/PRDs
```

### 2. Objective & Context
- Clear goal statement
- User value proposition
- Success metrics
- Non-goals and constraints

### 3. Technical Blueprint
```markdown
## Implementation Blueprint

### Phase 1: Database Schema
[Exact Drizzle/Prisma schema with RLS policies]

### Phase 2: API Endpoints
[Complete endpoint definitions with validation]

### Phase 3: Frontend Components
[Component structure with design system compliance]

### Phase 4: Integration
[How everything connects together]
```

### 4. Codebase Intelligence
```markdown
## Patterns to Follow
- Use existing Button component from components/ui/
- Follow form pattern from ContactForm.tsx
- Implement loading states like UserDashboard

## Gotchas to Avoid
- Don't use localStorage for PII (blocked by hooks)
- Always use field registry for new fields
- Remember mobile-first (test at 375px)
```

### 5. Validation Loops
```markdown
## Validation Requirements

### 🔴 Level 1: Syntax & Standards
- [ ] Linting passes
- [ ] TypeScript compiles
- [ ] Design system compliance
- [ ] Import paths correct

### 🟡 Level 2: Component Testing
- [ ] Unit tests written
- [ ] Component tests pass
- [ ] Hooks tested
- [ ] Edge cases covered

### 🟢 Level 3: Integration Testing
- [ ] E2E tests pass
- [ ] API integration works
- [ ] Database queries optimized
- [ ] Real user flows tested

### 🔵 Level 4: Production Readiness
- [ ] Performance budgets met
- [ ] Security audit passed
- [ ] Accessibility AA compliant
- [ ] Bundle size acceptable
```

## 🔄 PRP Workflow

### Traditional PRD → PRP Flow
```bash
# Start with PRD
/prd user management system

# Convert to PRP
/prd-to-prp user-management

# Execute implementation
/prp-execute user-management
```

### Direct PRP Creation
```bash
# Skip PRD for clear features
/create-prp shopping cart

# Review and customize
# Edit PRPs/active/shopping-cart.md

# Validate and implement
/prp-execute shopping-cart --level 1
```

### From GitHub Issue
```bash
# Start from issue
/fw start 234

# Generate PRP
/create-prp --from-issue 234

# Implement with context
/prp-execute feature-234
```

## 📁 PRP File Structure

```
PRPs/
├── templates/
│   ├── prp_base.md         # General features
│   ├── prp_typescript.md   # React components
│   └── prp_planning.md     # Architecture
├── ai_docs/
│   ├── nextjs15-app-router.md
│   ├── supabase-patterns.md
│   └── design-system-rules.md
├── scripts/
│   └── prp-runner.ts       # Validation executor
├── active/                 # Current PRPs
│   ├── user-auth.md
│   └── shopping-cart.md
└── completed/             # Reference PRPs
    └── contact-form.md
```

## 🎨 PRP Templates

### Base Template
For general feature development:
- Multi-phase implementation
- Full validation loops
- Integration patterns
- Performance considerations

### TypeScript Template
For React component development:
- Component structure
- Type definitions
- Design system usage
- Testing patterns

### Planning Template
For architecture decisions:
- System design
- API contracts
- Database schemas
- Integration points

## ✅ Validation Levels Explained

### Level 1: Syntax & Standards (Continuous)
Runs automatically on save:
- Biome linting
- TypeScript checking
- Design token validation
- Import path verification

```bash
/prp-execute feature --level 1
```

### Level 2: Component Testing
After implementing components:
- Unit test coverage
- Component behavior
- Hook functionality
- Isolated testing

```bash
/prp-execute feature --level 2
```

### Level 3: Integration Testing
When components connect:
- E2E scenarios
- API integration
- Database operations
- User workflows

```bash
/prp-execute feature --level 3
```

### Level 4: Production Readiness
Before PR/deployment:
- Lighthouse scores
- Bundle analysis
- Security scanning
- Requirement grading

```bash
/prp-execute feature --level 4
```

## 🔧 Auto-Fix Capabilities

The PRP system can automatically fix common issues:

```bash
/prp-execute feature --fix
```

Fixes:
- Design system violations
- Import path issues
- Formatting problems
- Simple TypeScript errors
- Missing exports

## 📊 PRP vs PRD

| Aspect | PRD | PRP |
|--------|-----|-----|
| Purpose | Define what to build | Enable implementation |
| Audience | Humans | AI + Humans |
| Content | Requirements | Requirements + How-to |
| Validation | Manual review | Automated loops |
| Codebase Knowledge | Generic | Specific patterns |
| Success Rate | Variable | One-pass implementation |

## 🚀 Best Practices

### 1. Start with Clear Requirements
PRPs work best with well-defined features. Use PRDs for exploration.

### 2. Customize Generated PRPs
Add project-specific patterns and constraints.

### 3. Run Validation Early
Don't wait until the end - validate at each phase.

### 4. Use Auto-Fix
Let the system handle mechanical fixes.

### 5. Learn from Completed PRPs
Reference successful implementations for patterns.

## 📈 Metrics

PRPs enable:
- **One-pass success**: Implementation works first time
- **70% time reduction**: Less back-and-forth
- **Higher quality**: Validation catches issues early
- **Knowledge capture**: Patterns documented and reused

## 🔗 Integration with Other Systems

- **GitHub Issues**: Link PRPs to issues
- **Stage Validation**: PRPs respect stage gates
- **Agent System**: Agents use PRPs for context
- **Chain Automation**: Chains can generate PRPs

## 📚 Related Documentation

- [PRP Templates](../../PRPs/templates/)
- [Workflow Guide](../workflow/PRP_WORKFLOW_GUIDE.md)
- [Validation Scripts](../../PRPs/scripts/)
- [AI Documentation](../../PRPs/ai_docs/)
