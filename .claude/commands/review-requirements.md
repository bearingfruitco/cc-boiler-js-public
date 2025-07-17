# review-requirements

Post-implementation review to ensure all locked requirements are met.

## Usage
```
/review-requirements [Component]
/rr ContactForm
/req-review  # Reviews all components with locked requirements
```

## What It Does

1. **Loads Locked Requirements** - Retrieves all locked requirements for component
2. **Analyzes Implementation** - Examines actual code
3. **Compares Against Requirements** - Validates each requirement
4. **Generates Compliance Report** - Shows what passed/failed
5. **Blocks on Violations** - Prevents proceeding if requirements not met

## Example Output

```
📋 REQUIREMENT COMPLIANCE REVIEW
================================
Component: ContactForm
Source: Issue #42
Review Date: 2024-01-15 10:30:00

✅ PASSED (4/7):
- Component exists at correct path
- Form structure follows design system
- Validation logic implemented
- Accessibility attributes present

❌ FAILED (3/7):
1. Field Count Mismatch
   - Expected: 13 fields
   - Found: 7 fields
   - Missing: lastName, phone, address, city, state, zip

2. Required Features Missing
   - Corporate email validation not implemented
   - Phone number formatting absent

3. Test Coverage
   - Expected: 80%
   - Actual: 45%

📊 COMPLIANCE SCORE: 57% (FAIL)

🔧 RECOMMENDED ACTIONS:
1. Run: /fix-requirements ContactForm
2. Or manually add missing fields
3. Implement corporate email validation
4. Add missing test cases

⚠️  Cannot proceed with deployment until compliance reaches 100%
```

## Review Process

### 1. Field Analysis
- Counts all form fields
- Verifies field names match requirements
- Checks required vs optional fields
- Validates field types

### 2. Feature Verification
- Confirms all required features present
- Checks business logic implementation
- Verifies validation rules
- Tests accessibility compliance

### 3. Code Quality Checks
- Design system compliance
- Test coverage
- Type safety
- Documentation completeness

### 4. Integration Testing
- API connections
- Data flow
- Error handling
- Performance metrics

## Command Options

### Review Specific Component
```bash
/review-requirements ContactForm
```

### Review All Components
```bash
/review-requirements --all
```

### Generate Fix Script
```bash
/review-requirements ContactForm --generate-fixes
```

### Export Report
```bash
/review-requirements ContactForm --export
# Creates: .claude/reports/ContactForm-compliance-{timestamp}.md
```

## Integration with CI/CD

The review can be integrated into your pipeline:

```yaml
# .github/workflows/requirement-check.yml
- name: Check Requirement Compliance
  run: |
    claude-code review-requirements --all --ci
```

## Automated Fixes

When possible, the command suggests automated fixes:

```bash
/rr ContactForm --auto-fix

🔧 AUTO-FIX AVAILABLE
====================
The following can be fixed automatically:
- Add missing fields (6)
- Update test cases
- Add validation rules

Proceed? [Y/n]
```

## Best Practices

1. **Run After Implementation** - Always review before marking complete
2. **Fix Immediately** - Don't let violations accumulate
3. **Document Deviations** - If requirements change, update locks
4. **Test After Fixes** - Ensure fixes don't break existing functionality

## Requirement Evolution

If requirements legitimately need to change:

```bash
# 1. Unlock the requirement
/unlock-requirements ContactForm --reason="Client approved reduction to 10 fields"

# 2. Update the requirement
/pin-requirements 42 ContactForm --update

# 3. Review again
/review-requirements ContactForm
```

This maintains an audit trail of all requirement changes.
