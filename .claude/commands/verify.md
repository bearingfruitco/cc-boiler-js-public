# Verify Implementation - TDD Focused

Run verification to ensure feature/task follows TDD workflow and is actually complete.

## Arguments:
- $1: feature-name or task-id (optional, defaults to current work)
- --quick: Quick verification only (tests exist, TypeScript compiles)
- --full: Full verification including coverage and regression
- --update-baseline: Update regression baseline after successful verification

## Purpose:
Enhances TDD workflow by verifying:
1. Tests exist (and were written first for TDD)
2. All tests pass
3. TypeScript compiles without errors
4. Coverage meets threshold
5. No regressions introduced

## Usage Examples:

```bash
# Verify current work
/verify

# Verify specific feature
/verify UserAuth

# Quick check only
/verify --quick

# Full verification with regression
/verify ContactForm --full

# Update baseline after major changes
/verify --update-baseline
```

## Verification Process:

### 1. TDD Compliance Check
```
✓ Tests exist for feature
✓ Tests were written before implementation (TDD)
✓ Test count: 15
```

### 2. Test Execution
```
Running: npm test UserAuth.test.tsx
✓ All 15 tests passing
✓ No skipped tests
```

### 3. TypeScript Validation
```
Running: tsc --noEmit
✓ No TypeScript errors
```

### 4. Coverage Analysis (if --full)
```
✓ Line coverage: 85%
✓ Branch coverage: 78%
✓ Meets threshold (70%)
```

### 5. Regression Check (if --full)
```
Running baseline tests...
✓ 156/156 baseline tests still passing
✓ No regressions detected
```

## Integration with TDD Workflow:

### Standard TDD Flow:
```bash
1. /test ContactForm        # Create test file
2. Write failing tests      # Red phase
3. /verify ContactForm      # Confirm tests fail
4. Implement feature        # Green phase
5. /verify ContactForm      # Confirm tests pass
6. Refactor if needed       # Refactor phase
7. /verify ContactForm      # Confirm still works
```

### With Process Tasks:
```bash
/pt contact-form
# After implementing task...
# Automatic quick verification runs
# If passes: ✓ Task complete
# If fails: Shows what needs fixing
```

## Example Output:

### Success Case:
```
🧪 TDD VERIFICATION: ContactForm
================================

✅ TDD Compliance
   • Tests found: 3 files
   • Tests written first: Yes (true TDD!)
   • components/__tests__/ContactForm.test.tsx

✅ Test Execution (12/12 passed)
   • Form renders: ✓
   • Validation works: ✓
   • Submission flow: ✓
   • Error handling: ✓

✅ TypeScript (Clean)
   • No type errors
   • Strict mode compliant

✅ Quick Verification PASSED

Feature "ContactForm" is properly tested and working.
Safe to mark as complete.
```

### Failure Case:
```
🧪 TDD VERIFICATION: UserProfile
================================

❌ TDD Compliance Issues
   • No test files found!
   • TDD requires tests first

Required Actions:
1. Create test file:
   /test UserProfile

2. Write tests for:
   - Component renders
   - Props handling
   - User interactions
   - Error states

3. See tests fail:
   npm test UserProfile.test

4. Then implement the feature

Use: /tdd-workflow UserProfile for guided flow
```

### Partial Success:
```
🧪 TDD VERIFICATION: PaymentForm
================================

✅ TDD Compliance
   • Tests found: PaymentForm.test.tsx
   • Tests written first: Yes

⚠️  Test Execution (8/10 passed)
   ❌ "handles card validation" - FAILED
   ❌ "shows error on invalid input" - FAILED

Required Fixes:
1. Fix failing tests:
   npm test PaymentForm.test.tsx

2. Debug failures:
   - Check validation logic
   - Verify error state handling

3. Re-run verification:
   /verify PaymentForm

Cannot mark complete until all tests pass!
```

## Verification Manifest:

Results are saved to `.claude/verification-manifest.json`:
- Tracks TDD compliance metrics
- Records test-first development
- Monitors completion claim accuracy
- Provides data for /sr context

## Quick Reference:

```bash
# During development
/verify                    # Quick check current work
/verify --quick            # Even faster (skip coverage)

# Before marking complete
/verify FeatureName        # Ensure ready
/verify FeatureName --full # Comprehensive check

# After major refactor
/verify --update-baseline  # Reset regression baseline
```

## Benefits:
- Enforces TDD workflow
- Catches incomplete implementations
- Prevents false completion claims
- Tracks testing metrics
- Integrates with existing tools
