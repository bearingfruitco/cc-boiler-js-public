# TDD Browser Flow

Implement Test-Driven Development with integrated browser verification.

## Usage
```bash
/tdd-browser [component-name]

# Or use the chain
/chain browser-tdd-flow
```

## The Enhanced TDD Cycle

### 1. RED Phase - Write Failing Tests

```typescript
// Unit test (Vitest)
describe('Button', () => {
  it('should handle click events', () => {
    const onClick = vi.fn();
    const { getByRole } = render(<Button onClick={onClick}>Click me</Button>);
    
    fireEvent.click(getByRole('button'));
    expect(onClick).toHaveBeenCalledOnce();
  });
});

// Browser test (Playwright via Claude)
/pw "create browser test for Button click handling that should fail"
```

### 2. Verify Tests Fail

```bash
# Run both test suites
/test Button           # Unit test fails ❌
/pw-test Button fail   # Browser test fails ❌

# Good! Tests are properly failing
```

### 3. GREEN Phase - Implement

```typescript
// Implement the Button
export function Button({ children, onClick }) {
  return (
    <button 
      onClick={onClick}
      className="h-12 px-4 rounded-xl bg-blue-600 text-white"
    >
      {children}
    </button>
  );
}
```

### 4. Verify Tests Pass

```bash
# Run tests again
/test Button          # Unit test passes ✅
/pw-test Button       # Browser test passes ✅

# But wait! Browser test found an issue:
# ⚠️ Console warning: Missing hover state
# ⚠️ Touch target only 48px (mobile needs 44px minimum)
```

### 5. REFACTOR Phase - With Browser Insights

```typescript
// Refactor based on browser feedback
export function Button({ children, onClick, disabled }) {
  return (
    <button 
      onClick={onClick}
      disabled={disabled}
      className="h-12 px-4 rounded-xl bg-blue-600 text-white 
                 hover:bg-blue-700 transition-colors
                 disabled:bg-gray-300 disabled:cursor-not-allowed
                 min-w-[44px]" // Mobile touch target
    >
      {children}
    </button>
  );
}
```

### 6. Final Verification

```bash
/tdd-browser verify Button

✅ Unit Tests: 5/5 passing
✅ Browser Tests: 
   - Renders correctly
   - No console errors
   - Click handler works
   - Hover state present
   - Touch target compliant
   - Keyboard accessible
✅ Visual: Screenshot captured
✅ Coverage: 100%
```

## Automated Workflow

The chain coordinates:

```yaml
tdd-engineer:
  - Writes comprehensive test suite
  - Includes edge cases
  
playwright-specialist:
  - Creates browser-specific tests
  - Tests real interactions
  - Verifies visual appearance
  
developer:
  - Implements to pass all tests
  
playwright-specialist:
  - Verifies in real browser
  - Catches runtime issues
  - Checks accessibility
  
refactoring-expert:
  - Improves based on browser insights
```

## Benefits Over Traditional TDD

1. **Catches Browser-Specific Issues**
   - Console errors
   - Event handler problems
   - CSS rendering issues

2. **Visual Verification**
   - Component actually looks correct
   - Responsive behavior works
   - Animations perform well

3. **Real User Interaction**
   - Touch events work
   - Keyboard navigation functions
   - Focus management correct

4. **Performance Validation**
   - Render performance
   - JavaScript execution time
   - Memory leaks

## Example Test Structure

```typescript
// button.test.ts - Unit tests
describe('Button', () => {
  it('renders children', () => {});
  it('handles clicks', () => {});
  it('supports disabled state', () => {});
  it('applies correct styles', () => {});
});

// button.browser.test.ts - Browser tests (via Playwright)
test('Button browser behavior', async ({ page }) => {
  await page.goto('/components/button');
  
  // Visual regression
  await expect(page).toHaveScreenshot();
  
  // Interaction testing
  await page.click('button');
  await expect(page).toHaveURL('/clicked');
  
  // Console errors
  const logs = await page.evaluate(() => window.console.logs);
  expect(logs.errors).toHaveLength(0);
  
  // Accessibility
  await expect(page.getByRole('button')).toBeVisible();
  await expect(page.getByRole('button')).toBeFocusable();
});
```

## Quick Commands

```bash
# Start TDD cycle
/tdd-browser Button

# Run specific phase
/tdd-browser Button --red
/tdd-browser Button --green
/tdd-browser Button --refactor

# Verify everything
/tdd-browser Button --verify-all
```

## Integration with CI

```yaml
test:
  - name: TDD Browser Tests
    run: |
      npm run test:unit
      npm run test:browser
      npm run test:visual
```

This ensures your tests catch everything! 🧪🌐
