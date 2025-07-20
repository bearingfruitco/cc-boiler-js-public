# Product Requirement Prompts (PRPs)

> PRD + Curated Codebase Intelligence + Validation Loops = Production-Ready Code on First Pass

## What is a PRP?

A PRP (Product Requirement Prompt) is an enhanced specification document that provides AI coding agents with everything needed to deliver production-ready code in a single implementation pass. It combines:

1. **Product Requirements** - What to build and why
2. **Codebase Intelligence** - Exact patterns, examples, and gotchas
3. **Validation Loops** - Automated quality gates at each stage

## Directory Structure

```
PRPs/
├── templates/           # PRP templates for different use cases
│   ├── prp_base.md     # General feature template
│   ├── prp_typescript.md # React/TypeScript component template
│   └── prp_planning.md  # Architecture planning template
├── ai_docs/            # AI-optimized documentation
│   ├── nextjs15-app-router.md
│   ├── supabase-patterns.md
│   └── design-system-rules.md
├── scripts/            # PRP automation tools
│   └── prp-runner.ts   # Validation loop executor
├── active/             # Current PRPs being implemented
├── completed/          # Finished PRPs for reference
└── README.md          # This file
```

## Quick Start

### 1. Create a PRP
```bash
/create-prp user authentication with JWT
# or
/prp checkout flow with Stripe
```

### 2. Review and Customize
The generated PRP will be saved to `PRPs/active/[feature-name].md`. Review and add any specific requirements.

### 3. Execute Validation Loops
```bash
/prp-execute user-auth
# or with auto-fix
/prp-run user-auth --fix
```

### 4. Begin Implementation
Follow the implementation blueprint in your PRP, running validations at each level.

## PRP Templates

### Base Template (`prp_base.md`)
- Comprehensive feature development
- Multi-phase implementation
- Full validation loops
- Integration with existing systems

### TypeScript Template (`prp_typescript.md`)
- React component focused
- Type-safe patterns
- Design system compliance
- Component testing emphasis

### Planning Template (`prp_planning.md`)
- Architecture decisions
- System design
- API contracts
- Database schemas

## Validation Loops

Each PRP includes 4 levels of validation:

### 🔴 Level 1: Code Quality (Continuous)
- Linting and formatting
- TypeScript checking
- Design system validation
- Async pattern checking

### 🟡 Level 2: Component Testing
- Unit tests
- Component tests
- Hook tests
- API tests

### 🟢 Level 3: Integration Testing
- E2E tests
- API integration
- Performance tests
- Accessibility checks

### 🔵 Level 4: Production Readiness
- Security audit
- Bundle size check
- Lighthouse scores
- Requirements compliance

## AI Documentation

The `ai_docs/` directory contains condensed, AI-optimized documentation for common technologies:

- **nextjs15-app-router.md** - Server/client components, data fetching, common gotchas
- **supabase-patterns.md** - Auth, database, RLS, realtime, storage patterns
- **design-system-rules.md** - Your specific design system requirements

These documents are referenced in PRPs to provide instant context without searching.

## Integration with Existing System

PRPs integrate seamlessly with your boilerplate:

- **Design System**: Enforces your 4-size, 2-weight typography
- **Event Queue**: Uses your async event patterns
- **Requirements**: Links to pinned GitHub requirements
- **Testing**: Leverages your existing test infrastructure
- **Hooks**: Validation loops trigger your pre/post hooks

## Best Practices

### 1. Be Specific in Goals
❌ "Create user profile"
✅ "Create user profile with avatar upload, bio editing, and privacy settings"

### 2. Include All Context Upfront
- Reference existing components to follow
- Note any API rate limits
- Include browser compatibility requirements
- Mention performance targets

### 3. Use Validation Loops
- Run Level 1 continuously during development
- Don't skip levels - they catch different issues
- Use `--fix` flag for automatic corrections

### 4. Keep PRPs Updated
- Update PRPs as requirements change
- Document new gotchas discovered
- Extract patterns for future PRPs

## Common Commands

```bash
# Create PRPs
/create-prp [feature description]
/prp [component name]

# Convert existing PRD
/prd-to-prp [feature-name]
/convert-to-prp [feature-name]

# Validate PRP
/prp-validate [prp-name]
/check-prp [prp-name]

# Execute validation
/prp-execute [prp-name]
/prp-run [prp-name] --fix
/prp-exec [prp-name] --level 1

# Check progress
/prp-status [prp-name]
/prp-progress [prp-name]

# Complete PRP
/prp-complete [prp-name]
/finish-prp [prp-name]

# Generate tasks from PRP
/gt [feature] --from-prp

# Related commands
/prd-tests [feature]      # Generate tests from PRD
/grade --prp [feature]    # Grade against PRP criteria
/pin-requirements [#]     # Lock requirements from issue
```

## Example Workflow

```bash
# 1. Start with GitHub issue
/fw start 123

# 2. Create PRP from issue
/create-prp implement user notifications

# 3. Review and enhance PRP
# Edit PRPs/active/user-notifications.md

# 4. Run initial validation
/prp-execute user-notifications --level 1

# 5. Implement following blueprint
# Code according to PRP phases

# 6. Validate after each phase
/prp-execute user-notifications --level 2

# 7. Full validation before PR
/prp-execute user-notifications

# 8. Create PR with context
/fw complete
```

## Tips

1. **Reference AI Docs**: Use `ai_docs/` for common patterns
2. **Chain PRPs**: Large features can have multiple PRPs
3. **Share Success**: Move completed PRPs to `completed/` for team reference
4. **Automate in CI**: Use `prp-runner.ts` in GitHub Actions

## Philosophy

> "The person who communicates most effectively is the most valuable programmer."

PRPs embody this philosophy by ensuring clear, comprehensive communication between humans and AI coding agents. The goal is not just working code, but production-ready implementations that follow all standards and patterns on the first attempt.

## Contributing

To improve PRP templates or add new AI documentation:

1. Test patterns thoroughly
2. Document gotchas clearly
3. Include working examples
4. Update validation loops
5. Share successful PRPs

Remember: The goal is **one-pass implementation success** through comprehensive context!
