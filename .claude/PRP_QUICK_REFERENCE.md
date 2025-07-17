# PRP Quick Reference

## Essential Commands

```bash
# Create new PRP
/create-prp user-authentication
/prp auth-feature              # Short alias

# Execute with validation
/prp-execute auth-feature       # All levels
/prp-exec auth --level 2        # Specific level
/prp-exec auth --fix            # Auto-fix issues

# Chain PRPs
/prp-chain auth → profile → settings

# View metrics
/prp-metrics auth-feature       # Individual
/prp-metrics --summary          # Overall stats
```

## PRP Structure

1. **Goal** - What we're building
2. **Success Criteria** - Measurable outcomes
3. **Required Context** - Docs, files, patterns
4. **Implementation** - Step-by-step blueprint
5. **Validation** - 4-level quality gates
6. **Metrics** - Track success

## Validation Levels

1. **Syntax & Standards** - Lint, types, design
2. **Component Testing** - Unit & component tests  
3. **Integration Testing** - E2E, API tests
4. **Production Readiness** - Security, performance

## Tips

- Reference AI docs for patterns
- Include gotchas upfront
- Be specific in success criteria
- Test each level before proceeding
- Update metrics after completion
