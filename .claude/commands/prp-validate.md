---
name: prp-validate
aliases: [validate-prp, check-prp, prp-check]
description: Validate PRP completeness and readiness for execution
category: PRPs
---

# Validate PRP: $ARGUMENTS

Check if a PRP has all required sections and is ready for implementation.

## Validation Checklist:

### 1. Structure Validation
- [ ] Goal section exists and is clear
- [ ] Success criteria are measurable
- [ ] Context section has references
- [ ] Implementation blueprint present
- [ ] Validation loops defined
- [ ] Confidence score provided

### 2. Context Completeness
```yaml
Required context types:
- Documentation URLs: At least 1
- Codebase examples: At least 2
- Known gotchas: At least 1
- Pattern references: At least 1
```

### 3. Implementation Readiness
- [ ] Task breakdown is detailed
- [ ] File structure is clear
- [ ] Dependencies identified
- [ ] Code patterns provided
- [ ] Anti-patterns listed

### 4. Validation Loops Check
```bash
Level 1: Syntax commands present
Level 2: Test commands specified
Level 3: Integration tests defined
Level 4: Production checks listed
```

### 5. Automation Compatibility
- [ ] Commands are executable
- [ ] Paths are relative
- [ ] No hardcoded values
- [ ] Environment vars defined

## Scoring:

Each section scores points:
- Structure: 20%
- Context: 30%
- Implementation: 30%
- Validation: 15%
- Automation: 5%

**Minimum passing score: 80%**

## Output Format:

```
PRP Validation: user-authentication
===================================

✅ Structure (20/20)
  ✓ All required sections present
  
⚠️ Context (22/30)
  ✓ Documentation: 3 references
  ✓ Codebase: 4 examples
  ✗ Gotchas: Only 0 found (need 1+)
  ✓ Patterns: 2 references

✅ Implementation (28/30)
  ✓ Task breakdown: 12 tasks
  ✓ File structure: Clear
  ⚠️ Dependencies: Partially defined
  ✓ Code patterns: 5 examples

✅ Validation (15/15)
  ✓ All 4 levels defined
  ✓ Commands executable

✅ Automation (5/5)
  ✓ Ready for prp_runner.py

Overall Score: 90% ✅ PASSED

Recommendations:
- Add at least 1 known gotcha
- Clarify task dependencies
```

## Actions on Failure:

If validation fails:
1. Show specific missing sections
2. Provide examples of what's needed
3. Offer to help fill gaps
4. Suggest relevant commands

## Integration:

```bash
# Validate before execution
/prp-validate auth && /prp-execute auth

# Validate after creation
/create-prp feature && /prp-validate feature

# Validate with auto-fix suggestions
/prp-validate feature --suggest-fixes
```

## Best Practices:

1. Always validate after PRP creation
2. Re-validate after significant edits
3. Use validation as quality gate
4. Track validation scores over time