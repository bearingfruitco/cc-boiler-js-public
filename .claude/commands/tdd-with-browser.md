# TDD with Browser Testing

Generate and run both unit tests and browser tests in your TDD workflow.

## Command
```bash
/tdd-with-browser <component-name>
# or alias
/tddb <component-name>
```

## What It Does

1. **Generates Two Test Files:**
   - `Component.test.tsx` - Unit tests (Vitest)
   - `Component.browser.test.ts` - Browser tests (Playwright)

2. **Follows TDD Cycle:**
   - RED: Both test suites fail
   - GREEN: Implement until both pass
   - REFACTOR: Maintain both test suites

## Example Workflow

```bash
/tddb LoginForm
```

Creates:
```typescript
// LoginForm.test.tsx
import { render, screen } from '@testing-library/react';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('renders email and password fields', () => {
    render(<LoginForm />);
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
  });
  
  it('shows validation errors for invalid input', () => {
    // Test validation logic
  });
});

// LoginForm.browser.test.ts
import { test, expect } from '@playwright/test';

test.describe('LoginForm Browser Tests', () => {
  test('form submits successfully with valid data', async ({ page }) => {
    await page.goto('/login');
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    
    // Should redirect to dashboard
    await expect(page).toHaveURL('/dashboard');
  });
  
  test('shows inline validation errors', async ({ page }) => {
    await page.goto('/login');
    await page.click('button[type="submit"]');
    
    // Should show validation errors
    await expect(page.locator('.error-message')).toContainText('Email is required');
  });
  
  test('form is keyboard accessible', async ({ page }) => {
    await page.goto('/login');
    await page.keyboard.press('Tab'); // Focus email
    await page.keyboard.type('test@example.com');
    await page.keyboard.press('Tab'); // Focus password
    await page.keyboard.type('password123');
    await page.keyboard.press('Enter'); // Submit
    
    await expect(page).toHaveURL('/dashboard');
  });
});
```

## Integration with Existing TDD

The browser tests run separately from unit tests:

```bash
# Run unit tests (fast, during development)
npm test LoginForm.test.tsx

# Run browser tests (slower, after unit tests pass)
npx playwright test LoginForm.browser.test.ts

# Or use our command
/pw-test LoginForm
```

## Smart Features

1. **Deferred Execution** - Browser tests only run after unit tests pass
2. **Focused Testing** - Only test the component you're working on
3. **No Context Pollution** - Browser tests run in separate process

## Tips

- Write browser tests for user interactions
- Write unit tests for logic and state
- Browser tests catch integration issues
- Unit tests catch logic errors

This gives you the best of both worlds without slowing down TDD!
