# Comprehensive Testing Guide

> Complete testing strategy and implementation guide for Claude Code Boilerplate v4.0.0, covering unit tests, component tests, integration tests, E2E tests, and performance testing.

## ? Table of Contents

1. [Testing Philosophy](#testing-philosophy)
2. [Test Pyramid Approach](#test-pyramid-approach)
3. [Unit Testing with Vitest](#unit-testing-with-vitest)
4. [Component Testing](#component-testing)
5. [Integration Testing](#integration-testing)
6. [E2E Testing with Playwright](#e2e-testing-with-playwright)
7. [Performance Testing](#performance-testing)
8. [Test Data Management](#test-data-management)
9. [CI/CD Integration](#cicd-integration)
10. [TDD Workflow](#tdd-workflow)
11. [Testing Commands](#testing-commands)
12. [Best Practices](#best-practices)

## Testing Philosophy

### Core Principles

1. **Test First, Code Second** - TDD is mandatory for all features
2. **Fast Feedback** - Tests should run quickly and frequently
3. **Isolated Tests** - Each test should be independent
4. **Clear Failures** - Test failures should pinpoint the problem
5. **Confidence Through Coverage** - Aim for 80%+ coverage
6. **Real Browser Testing** - Verify in actual browser context

### Testing Strategy

```
???????????????????????????????????????
?          E2E Tests (10%)            ?  ? Slow, High Confidence
???????????????????????????????????????
?     Integration Tests (20%)         ?  ? Medium Speed
???????????????????????????????????????
?    Component Tests (30%)            ?  ? Fast, UI Focused
???????????????????????????????????????
?      Unit Tests (40%)               ?  ? Very Fast, Logic
???????????????????????????????????????
```

## Test Pyramid Approach

### 1. Unit Tests (40%)
- Business logic
- Utility functions
- Data transformations
- Validation logic
- Pure functions

### 2. Component Tests (30%)
- React components
- User interactions
- Props validation
- Rendering logic
- State management

### 3. Integration Tests (20%)
- API endpoints
- Database operations
- External services
- Authentication flows
- Multi-component interactions

### 4. E2E Tests (10%)
- Critical user journeys
- Cross-browser testing
- Performance metrics
- Visual regression
- Accessibility checks

## Unit Testing with Vitest

### Setup

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./tests/setup.ts'],
    coverage: {
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'tests/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/mockData.ts'
      ]
    },
    alias: {
      '@': path.resolve(__dirname, './'),
      '@/components': path.resolve(__dirname, './components'),
      '@/lib': path.resolve(__dirname, './lib')
    }
  }
});
```

### Test Setup File

```typescript
// tests/setup.ts
import '@testing-library/jest-dom';
import { cleanup } from '@testing-library/react';
import { afterEach, vi } from 'vitest';

// Cleanup after each test
afterEach(() => {
  cleanup();
});

// Mock Next.js router
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    prefetch: vi.fn(),
    back: vi.fn()
  }),
  useSearchParams: () => ({
    get: vi.fn()
  }),
  usePathname: () => '/test'
}));

// Mock environment variables
process.env.NEXT_PUBLIC_API_URL = 'http://localhost:3000';
```

### Unit Test Examples

#### Testing Utility Functions

```typescript
// lib/utils/validation.test.ts
import { describe, it, expect } from 'vitest';
import { 
  validateEmail, 
  validatePhone, 
  sanitizeInput 
} from './validation';

describe('Validation Utils', () => {
  describe('validateEmail', () => {
    it('should validate correct email formats', () => {
      expect(validateEmail('user@example.com')).toBe(true);
      expect(validateEmail('user+tag@example.co.uk')).toBe(true);
    });
    
    it('should reject invalid email formats', () => {
      expect(validateEmail('invalid')).toBe(false);
      expect(validateEmail('user@')).toBe(false);
      expect(validateEmail('@example.com')).toBe(false);
    });
  });
  
  describe('validatePhone', () => {
    it('should validate 10-digit phone numbers', () => {
      expect(validatePhone('1234567890')).toBe(true);
      expect(validatePhone('123-456-7890')).toBe(true);
    });
    
    it('should reject invalid phone numbers', () => {
      expect(validatePhone('123')).toBe(false);
      expect(validatePhone('abcdefghij')).toBe(false);
    });
  });
  
  describe('sanitizeInput', () => {
    it('should remove harmful content', () => {
      expect(sanitizeInput('<script>alert("xss")</script>'))
        .toBe('');
      expect(sanitizeInput('Hello <b>World</b>'))
        .toBe('Hello World');
    });
  });
});
```

#### Testing Custom Hooks

```typescript
// hooks/useDebounce.test.ts
import { renderHook, act } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { useDebounce } from './useDebounce';

describe('useDebounce', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });
  
  afterEach(() => {
    vi.useRealTimers();
  });
  
  it('should debounce value changes', () => {
    const { result, rerender } = renderHook(
      ({ value, delay }) => useDebounce(value, delay),
      { initialProps: { value: 'initial', delay: 500 } }
    );
    
    expect(result.current).toBe('initial');
    
    // Change value
    rerender({ value: 'updated', delay: 500 });
    
    // Value shouldn't change immediately
    expect(result.current).toBe('initial');
    
    // Fast-forward time
    act(() => {
      vi.advanceTimersByTime(500);
    });
    
    // Now value should be updated
    expect(result.current).toBe('updated');
  });
  
  it('should cancel previous timeout on rapid changes', () => {
    const { result, rerender } = renderHook(
      ({ value }) => useDebounce(value, 300),
      { initialProps: { value: 'first' } }
    );
    
    rerender({ value: 'second' });
    vi.advanceTimersByTime(200);
    
    rerender({ value: 'third' });
    vi.advanceTimersByTime(200);
    
    // Still should be initial value
    expect(result.current).toBe('first');
    
    // Complete the debounce
    vi.advanceTimersByTime(100);
    
    // Should have latest value
    expect(result.current).toBe('third');
  });
});
```

#### Testing API Utilities

```typescript
// lib/api/client.test.ts
import { describe, it, expect, vi } from 'vitest';
import { apiClient, ApiError } from './client';

// Mock fetch
global.fetch = vi.fn();

describe('API Client', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });
  
  it('should make successful GET request', async () => {
    const mockData = { id: 1, name: 'Test' };
    
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockData
    });
    
    const result = await apiClient('/users/1');
    
    expect(global.fetch).toHaveBeenCalledWith('/api/users/1', {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    expect(result).toEqual(mockData);
  });
  
  it('should handle API errors', async () => {
    (global.fetch as any).mockResolvedValueOnce({
      ok: false,
      status: 404,
      text: async () => 'Not found'
    });
    
    await expect(apiClient('/users/999'))
      .rejects
      .toThrow(ApiError);
    
    try {
      await apiClient('/users/999');
    } catch (error) {
      expect(error).toBeInstanceOf(ApiError);
      expect(error.status).toBe(404);
      expect(error.message).toBe('Not found');
    }
  });
  
  it('should add auth token when available', async () => {
    const token = 'test-token';
    
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => ({})
    });
    
    await apiClient('/protected', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    expect(global.fetch).toHaveBeenCalledWith('/api/protected', {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });
  });
});
```

## Component Testing

### Testing Library Setup

```typescript
// tests/utils/render.tsx
import { render as rtlRender } from '@testing-library/react';
import { ReactElement } from 'react';

// Custom providers
function AllTheProviders({ children }: { children: React.ReactNode }) {
  return (
    <>
      {/* Add your providers here */}
      {children}
    </>
  );
}

function customRender(
  ui: ReactElement,
  options?: Parameters<typeof rtlRender>[1]
) {
  return rtlRender(ui, { wrapper: AllTheProviders, ...options });
}

export * from '@testing-library/react';
export { customRender as render };
```

### Component Test Examples

#### Basic Component Test

```typescript
// components/ui/Button.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@/tests/utils/render';
import { Button } from './Button';

describe('Button Component', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>);
    
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });
  
  it('applies correct design system classes', () => {
    render(<Button variant="primary">Test</Button>);
    
    const button = screen.getByRole('button');
    
    // Check design system compliance
    expect(button).toHaveClass('text-size-3');
    expect(button).toHaveClass('font-semibold');
    expect(button).toHaveClass('h-12'); // 48px touch target
    expect(button).not.toHaveClass('text-sm'); // Forbidden class
  });
  
  it('handles click events', () => {
    const handleClick = vi.fn();
    
    render(<Button onClick={handleClick}>Click</Button>);
    
    fireEvent.click(screen.getByRole('button'));
    
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
  
  it('can be disabled', () => {
    const handleClick = vi.fn();
    
    render(
      <Button onClick={handleClick} disabled>
        Disabled
      </Button>
    );
    
    const button = screen.getByRole('button');
    
    expect(button).toBeDisabled();
    expect(button).toHaveClass('disabled:bg-gray-200');
    
    fireEvent.click(button);
    expect(handleClick).not.toHaveBeenCalled();
  });
  
  it('supports different variants', () => {
    const { rerender } = render(<Button variant="primary">Primary</Button>);
    
    expect(screen.getByRole('button')).toHaveClass('bg-blue-600');
    
    rerender(<Button variant="secondary">Secondary</Button>);
    
    expect(screen.getByRole('button')).toHaveClass('bg-gray-800');
  });
});
```

#### Form Component Test

```typescript
// components/forms/LoginForm.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@/tests/utils/render';
import userEvent from '@testing-library/user-event';
import { LoginForm } from './LoginForm';

describe('LoginForm Component', () => {
  const mockOnSubmit = vi.fn();
  
  beforeEach(() => {
    mockOnSubmit.mockClear();
  });
  
  it('renders all form fields', () => {
    render(<LoginForm onSubmit={mockOnSubmit} />);
    
    expect(screen.getByLabelText('Email')).toBeInTheDocument();
    expect(screen.getByLabelText('Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Login' })).toBeInTheDocument();
  });
  
  it('validates required fields', async () => {
    render(<LoginForm onSubmit={mockOnSubmit} />);
    
    const submitButton = screen.getByRole('button', { name: 'Login' });
    
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText('Email is required')).toBeInTheDocument();
      expect(screen.getByText('Password is required')).toBeInTheDocument();
    });
    
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });
  
  it('validates email format', async () => {
    const user = userEvent.setup();
    
    render(<LoginForm onSubmit={mockOnSubmit} />);
    
    const emailInput = screen.getByLabelText('Email');
    
    await user.type(emailInput, 'invalid-email');
    await user.tab(); // Trigger blur
    
    await waitFor(() => {
      expect(screen.getByText('Invalid email format')).toBeInTheDocument();
    });
  });
  
  it('submits form with valid data', async () => {
    const user = userEvent.setup();
    
    render(<LoginForm onSubmit={mockOnSubmit} />);
    
    await user.type(screen.getByLabelText('Email'), 'user@example.com');
    await user.type(screen.getByLabelText('Password'), 'SecurePass123');
    
    await user.click(screen.getByRole('button', { name: 'Login' }));
    
    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        email: 'user@example.com',
        password: 'SecurePass123'
      });
    });
  });
  
  it('shows loading state during submission', async () => {
    const slowSubmit = vi.fn(() => 
      new Promise(resolve => setTimeout(resolve, 1000))
    );
    
    render(<LoginForm onSubmit={slowSubmit} />);
    
    const user = userEvent.setup();
    
    await user.type(screen.getByLabelText('Email'), 'user@example.com');
    await user.type(screen.getByLabelText('Password'), 'password');
    
    const submitButton = screen.getByRole('button', { name: 'Login' });
    
    await user.click(submitButton);
    
    // Check loading state
    expect(submitButton).toBeDisabled();
    expect(screen.getByText('Logging in...')).toBeInTheDocument();
    
    // Wait for submission to complete
    await waitFor(() => {
      expect(submitButton).not.toBeDisabled();
    });
  });
});
```

#### Testing with Mocked Hooks

```typescript
// components/UserProfile.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@/tests/utils/render';
import { UserProfile } from './UserProfile';
import { useUser } from '@/hooks/useUser';

// Mock the hook
vi.mock('@/hooks/useUser');

describe('UserProfile Component', () => {
  it('shows loading state', () => {
    vi.mocked(useUser).mockReturnValue({
      user: null,
      isLoading: true,
      error: null
    });
    
    render(<UserProfile userId="123" />);
    
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });
  
  it('shows error state', () => {
    vi.mocked(useUser).mockReturnValue({
      user: null,
      isLoading: false,
      error: new Error('Failed to load user')
    });
    
    render(<UserProfile userId="123" />);
    
    expect(screen.getByText('Error: Failed to load user')).toBeInTheDocument();
  });
  
  it('displays user information', () => {
    vi.mocked(useUser).mockReturnValue({
      user: {
        id: '123',
        name: 'John Doe',
        email: 'john@example.com',
        avatar: '/avatar.jpg'
      },
      isLoading: false,
      error: null
    });
    
    render(<UserProfile userId="123" />);
    
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
    expect(screen.getByRole('img')).toHaveAttribute('src', '/avatar.jpg');
  });
});
```

## Integration Testing

### Database Testing

```typescript
// tests/integration/userRepository.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { userRepository } from '@/lib/repositories/userRepository';
import { testDb, cleanupDb, seedUser } from '@/tests/utils/testDb';

describe('User Repository Integration', () => {
  beforeEach(async () => {
    await cleanupDb();
  });
  
  describe('create', () => {
    it('should create a new user', async () => {
      const userData = {
        email: 'test@example.com',
        name: 'Test User',
        passwordHash: 'hashed'
      };
      
      const user = await userRepository.create(userData);
      
      expect(user.id).toBeDefined();
      expect(user.email).toBe(userData.email);
      expect(user.createdAt).toBeInstanceOf(Date);
    });
    
    it('should enforce unique email constraint', async () => {
      await seedUser({ email: 'existing@example.com' });
      
      await expect(
        userRepository.create({
          email: 'existing@example.com',
          name: 'Another User',
          passwordHash: 'hashed'
        })
      ).rejects.toThrow(/unique constraint/i);
    });
  });
  
  describe('findById', () => {
    it('should find user by id', async () => {
      const seeded = await seedUser();
      
      const found = await userRepository.findById(seeded.id);
      
      expect(found).toEqual(seeded);
    });
    
    it('should return null for non-existent id', async () => {
      const found = await userRepository.findById('non-existent');
      
      expect(found).toBeNull();
    });
  });
  
  describe('update', () => {
    it('should update user fields', async () => {
      const user = await seedUser({ name: 'Original Name' });
      
      const updated = await userRepository.update(user.id, {
        name: 'Updated Name'
      });
      
      expect(updated.name).toBe('Updated Name');
      expect(updated.updatedAt).not.toEqual(user.updatedAt);
    });
  });
});
```

### API Integration Testing

```typescript
// tests/integration/auth.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { createMocks } from 'node-mocks-http';
import bcrypt from 'bcryptjs';
import { POST as login } from '@/app/api/auth/login/route';
import { GET as profile } from '@/app/api/auth/profile/route';
import { testDb, cleanupDb } from '@/tests/utils/testDb';

describe('Auth API Integration', () => {
  let testUser: any;
  
  beforeEach(async () => {
    await cleanupDb();
    
    // Create test user
    testUser = await testDb.user.create({
      data: {
        email: 'test@example.com',
        passwordHash: await bcrypt.hash('password123', 10),
        name: 'Test User'
      }
    });
  });
  
  describe('POST /api/auth/login', () => {
    it('should login with valid credentials', async () => {
      const { req, res } = createMocks({
        method: 'POST',
        body: {
          email: 'test@example.com',
          password: 'password123'
        }
      });
      
      await login(req as any);
      
      const data = JSON.parse(res._getData());
      
      expect(res._getStatusCode()).toBe(200);
      expect(data.success).toBe(true);
      expect(data.data.user.email).toBe('test@example.com');
      
      // Check auth cookie was set
      const cookies = res._getHeaders()['set-cookie'];
      expect(cookies).toBeDefined();
      expect(cookies[0]).toContain('auth-token');
    });
    
    it('should reject invalid password', async () => {
      const { req, res } = createMocks({
        method: 'POST',
        body: {
          email: 'test@example.com',
          password: 'wrongpassword'
        }
      });
      
      await login(req as any);
      
      expect(res._getStatusCode()).toBe(401);
      expect(JSON.parse(res._getData()).error).toBe('Invalid credentials');
    });
  });
  
  describe('GET /api/auth/profile', () => {
    it('should return profile for authenticated user', async () => {
      // First login to get token
      const loginReq = createMocks({
        method: 'POST',
        body: {
          email: 'test@example.com',
          password: 'password123'
        }
      });
      
      await login(loginReq.req as any);
      
      const authCookie = loginReq.res._getHeaders()['set-cookie'][0];
      
      // Then get profile
      const { req, res } = createMocks({
        method: 'GET',
        headers: {
          cookie: authCookie
        }
      });
      
      await profile(req as any);
      
      const data = JSON.parse(res._getData());
      
      expect(res._getStatusCode()).toBe(200);
      expect(data.data.email).toBe('test@example.com');
    });
    
    it('should reject unauthenticated request', async () => {
      const { req, res } = createMocks({
        method: 'GET'
      });
      
      await profile(req as any);
      
      expect(res._getStatusCode()).toBe(401);
    });
  });
});
```

## E2E Testing with Playwright

### Playwright Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  
  use: {
    baseURL: process.env.PLAYWRIGHT_TEST_BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure'
  },
  
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],
  
  webServer: {
    command: 'npm run dev',
    port: 3000,
    reuseExistingServer: !process.env.CI,
  },
});
```

### E2E Test Examples

#### User Journey Test

```typescript
// e2e/auth-flow.spec.ts
import { test, expect } from '@playwright/test';
import { createTestUser, deleteTestUser } from './utils/testHelpers';

test.describe('Authentication Flow', () => {
  let testUser: { email: string; password: string };
  
  test.beforeEach(async () => {
    testUser = await createTestUser();
  });
  
  test.afterEach(async () => {
    await deleteTestUser(testUser.email);
  });
  
  test('complete authentication flow', async ({ page }) => {
    // Navigate to login
    await page.goto('/login');
    
    // Check page loaded
    await expect(page).toHaveTitle(/Login/);
    
    // Fill login form
    await page.fill('[name="email"]', testUser.email);
    await page.fill('[name="password"]', testUser.password);
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Wait for navigation
    await page.waitForURL('/dashboard');
    
    // Verify logged in
    await expect(page.locator('text=' + testUser.email)).toBeVisible();
    
    // Test logout
    await page.click('button:has-text("Logout")');
    
    // Should redirect to login
    await page.waitForURL('/login');
    
    // Verify logged out
    await expect(page.locator('text=Login')).toBeVisible();
  });
  
  test('shows validation errors', async ({ page }) => {
    await page.goto('/login');
    
    // Submit empty form
    await page.click('button[type="submit"]');
    
    // Check validation messages
    await expect(page.locator('text=Email is required')).toBeVisible();
    await expect(page.locator('text=Password is required')).toBeVisible();
    
    // Try invalid email
    await page.fill('[name="email"]', 'invalid-email');
    await page.click('button[type="submit"]');
    
    await expect(page.locator('text=Invalid email format')).toBeVisible();
  });
  
  test('handles incorrect credentials', async ({ page }) => {
    await page.goto('/login');
    
    await page.fill('[name="email"]', testUser.email);
    await page.fill('[name="password"]', 'wrongpassword');
    await page.click('button[type="submit"]');
    
    // Should show error
    await expect(page.locator('text=Invalid credentials')).toBeVisible();
    
    // Should not navigate
    await expect(page).toHaveURL('/login');
  });
});
```

#### Visual Regression Test

```typescript
// e2e/visual-regression.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Visual Regression', () => {
  test('homepage appearance', async ({ page }) => {
    await page.goto('/');
    
    // Wait for content to load
    await page.waitForLoadState('networkidle');
    
    // Take screenshot
    await expect(page).toHaveScreenshot('homepage.png', {
      fullPage: true,
      animations: 'disabled'
    });
  });
  
  test('component library', async ({ page }) => {
    await page.goto('/components');
    
    // Screenshot each component state
    const components = ['Button', 'Card', 'Form', 'Modal'];
    
    for (const component of components) {
      await page.click(`text=${component}`);
      await page.waitForTimeout(500); // Wait for animations
      
      await expect(page.locator('[data-component-preview]'))
        .toHaveScreenshot(`${component.toLowerCase()}.png`);
    }
  });
  
  test('responsive design', async ({ page }) => {
    const viewports = [
      { width: 375, height: 667, name: 'mobile' },
      { width: 768, height: 1024, name: 'tablet' },
      { width: 1920, height: 1080, name: 'desktop' }
    ];
    
    for (const viewport of viewports) {
      await page.setViewportSize({
        width: viewport.width,
        height: viewport.height
      });
      
      await page.goto('/');
      
      await expect(page).toHaveScreenshot(`homepage-${viewport.name}.png`, {
        fullPage: true
      });
    }
  });
});
```

#### Accessibility Test

```typescript
// e2e/accessibility.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility', () => {
  test('homepage accessibility', async ({ page }) => {
    await page.goto('/');
    
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();
    
    expect(accessibilityScanResults.violations).toEqual([]);
  });
  
  test('form accessibility', async ({ page }) => {
    await page.goto('/contact');
    
    // Check form labels
    const inputs = await page.locator('input').all();
    
    for (const input of inputs) {
      const label = await input.evaluate((el) => {
        const labelElement = document.querySelector(`label[for="${el.id}"]`);
        return labelElement?.textContent;
      });
      
      expect(label).toBeTruthy();
    }
    
    // Check ARIA attributes
    const form = page.locator('form');
    await expect(form).toHaveAttribute('aria-label');
    
    // Run axe scan
    const results = await new AxeBuilder({ page })
      .include('form')
      .analyze();
    
    expect(results.violations).toEqual([]);
  });
  
  test('keyboard navigation', async ({ page }) => {
    await page.goto('/');
    
    // Tab through interactive elements
    await page.keyboard.press('Tab');
    
    // First focusable element should be skip link
    const skipLink = page.locator(':focus');
    await expect(skipLink).toHaveText('Skip to main content');
    
    // Tab through navigation
    const navItems = await page.locator('nav a').count();
    
    for (let i = 0; i < navItems; i++) {
      await page.keyboard.press('Tab');
      const focused = page.locator(':focus');
      await expect(focused).toBeVisible();
    }
    
    // Test button activation with Enter
    await page.keyboard.press('Tab');
    await page.keyboard.press('Enter');
    
    // Verify action was triggered
    await expect(page).toHaveURL(/clicked/);
  });
});
```

## Performance Testing

### Performance Test Setup

```typescript
// e2e/performance.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Performance', () => {
  test('page load metrics', async ({ page }) => {
    // Start measuring
    await page.goto('/', { waitUntil: 'networkidle' });
    
    // Get performance metrics
    const metrics = await page.evaluate(() => {
      const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
      
      return {
        domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
        loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
        firstPaint: performance.getEntriesByName('first-paint')[0]?.startTime,
        firstContentfulPaint: performance.getEntriesByName('first-contentful-paint')[0]?.startTime,
        largestContentfulPaint: 0 // Will be set below
      };
    });
    
    // Get LCP
    const lcp = await page.evaluate(() => {
      return new Promise((resolve) => {
        new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const lastEntry = entries[entries.length - 1];
          resolve(lastEntry.startTime);
        }).observe({ entryTypes: ['largest-contentful-paint'] });
      });
    });
    
    metrics.largestContentfulPaint = lcp as number;
    
    // Assert performance budgets
    expect(metrics.firstContentfulPaint).toBeLessThan(1500);
    expect(metrics.largestContentfulPaint).toBeLessThan(2500);
    expect(metrics.domContentLoaded).toBeLessThan(3000);
  });
  
  test('bundle size check', async ({ page }) => {
    const coverage = await page.coverage.startJSCoverage();
    
    await page.goto('/');
    await page.click('button'); // Trigger some JS
    
    const jsCoverage = await page.coverage.stopJSCoverage();
    
    // Calculate total JS size
    const totalBytes = jsCoverage.reduce((total, entry) => {
      return total + entry.text.length;
    }, 0);
    
    // Check bundle size budget (e.g., 200KB)
    expect(totalBytes).toBeLessThan(200 * 1024);
    
    // Check unused code
    const usedBytes = jsCoverage.reduce((total, entry) => {
      return total + entry.ranges.reduce((sum, range) => {
        return sum + (range.end - range.start);
      }, 0);
    }, 0);
    
    const unusedPercentage = ((totalBytes - usedBytes) / totalBytes) * 100;
    
    // Expect less than 30% unused code
    expect(unusedPercentage).toBeLessThan(30);
  });
});
```

### Load Testing

```typescript
// tests/load/api-load.test.ts
import { check } from 'k6';
import http from 'k6/http';
import { Rate } from 'k6/metrics';

export const errorRate = new Rate('errors');

export const options = {
  stages: [
    { duration: '30s', target: 10 },  // Ramp up
    { duration: '1m', target: 50 },   // Stay at 50
    { duration: '30s', target: 0 },   // Ramp down
  ],
  thresholds: {
    errors: ['rate<0.1'],            // Error rate < 10%
    http_req_duration: ['p(95)<500'], // 95% of requests < 500ms
  },
};

export default function () {
  // Test login endpoint
  const loginRes = http.post(
    'http://localhost:3000/api/auth/login',
    JSON.stringify({
      email: 'load@test.com',
      password: 'password123'
    }),
    { headers: { 'Content-Type': 'application/json' } }
  );
  
  check(loginRes, {
    'login successful': (r) => r.status === 200,
    'response time OK': (r) => r.timings.duration < 500,
  });
  
  errorRate.add(loginRes.status !== 200);
  
  // Extract token
  const token = loginRes.json('data.token');
  
  // Test authenticated endpoint
  const profileRes = http.get(
    'http://localhost:3000/api/users/profile',
    {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    }
  );
  
  check(profileRes, {
    'profile retrieved': (r) => r.status === 200,
    'has user data': (r) => r.json('data.email') !== undefined,
  });
  
  errorRate.add(profileRes.status !== 200);
}
```

## Test Data Management

### Test Database Setup

```typescript
// tests/utils/testDb.ts
import { PrismaClient } from '@prisma/client';
import { execSync } from 'child_process';

const testDbUrl = process.env.DATABASE_TEST_URL || 'postgresql://test:test@localhost:5432/test';

// Create test client
export const testDb = new PrismaClient({
  datasources: {
    db: {
      url: testDbUrl
    }
  }
});

// Database utilities
export async function cleanupDb() {
  const tableNames = await testDb.$queryRaw<
    Array<{ tablename: string }>
  >`SELECT tablename FROM pg_tables WHERE schemaname='public'`;
  
  const tables = tableNames
    .map(({ tablename }) => tablename)
    .filter((name) => name !== '_prisma_migrations')
    .map((name) => `"public"."${name}"`)
    .join(', ');
  
  try {
    await testDb.$executeRawUnsafe(`TRUNCATE TABLE ${tables} RESTART IDENTITY CASCADE;`);
  } catch (error) {
    console.log('Error cleaning database:', error);
  }
}

export async function resetDb() {
  execSync('npm run db:test:reset', { stdio: 'inherit' });
}

// Seed helpers
export async function seedUser(data?: Partial<User>) {
  return testDb.user.create({
    data: {
      email: data?.email || 'test@example.com',
      name: data?.name || 'Test User',
      passwordHash: data?.passwordHash || 'hashed',
      ...data
    }
  });
}

export async function seedPost(userId: string, data?: Partial<Post>) {
  return testDb.post.create({
    data: {
      title: data?.title || 'Test Post',
      content: data?.content || 'Test content',
      published: data?.published ?? true,
      authorId: userId,
      ...data
    }
  });
}
```

### Test Factories

```typescript
// tests/factories/userFactory.ts
import { faker } from '@faker-js/faker';
import bcrypt from 'bcryptjs';

export function createUserData(overrides?: Partial<UserData>) {
  return {
    email: faker.internet.email(),
    name: faker.person.fullName(),
    passwordHash: bcrypt.hashSync('password123', 10),
    avatar: faker.image.avatar(),
    bio: faker.lorem.paragraph(),
    ...overrides
  };
}

export function createManyUsers(count: number) {
  return Array.from({ length: count }, () => createUserData());
}

// tests/factories/postFactory.ts
export function createPostData(overrides?: Partial<PostData>) {
  return {
    title: faker.lorem.sentence(),
    content: faker.lorem.paragraphs(3),
    excerpt: faker.lorem.paragraph(),
    published: faker.datatype.boolean(),
    tags: faker.helpers.arrayElements(['tech', 'news', 'tutorial'], 2),
    ...overrides
  };
}
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Test Suite

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 20
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run unit tests
        run: npm run test:unit
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/coverage-final.json
  
  integration-tests:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 20
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Setup test database
        run: npm run db:test:setup
        env:
          DATABASE_TEST_URL: postgresql://postgres:test@localhost:5432/test
      
      - name: Run integration tests
        run: npm run test:integration
        env:
          DATABASE_TEST_URL: postgresql://postgres:test@localhost:5432/test
  
  e2e-tests:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 20
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Install Playwright
        run: npx playwright install --with-deps
      
      - name: Run E2E tests
        run: npm run test:e2e
      
      - name: Upload test artifacts
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

## TDD Workflow

### TDD Process

1. **Write Failing Test** (Red)
```typescript
// Button.test.tsx
it('should change color on hover', () => {
  render(<Button>Hover me</Button>);
  const button = screen.getByRole('button');
  
  fireEvent.mouseEnter(button);
  
  expect(button).toHaveClass('bg-blue-700'); // Fails - not implemented
});
```

2. **Write Minimal Code** (Green)
```typescript
// Button.tsx
export function Button({ children }: ButtonProps) {
  const [isHovered, setIsHovered] = useState(false);
  
  return (
    <button
      className={`${isHovered ? 'bg-blue-700' : 'bg-blue-600'}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {children}
    </button>
  );
}
```

3. **Refactor** (Refactor)
```typescript
// Button.tsx - Improved
export function Button({ children }: ButtonProps) {
  const [isHovered, setIsHovered] = useState(false);
  
  const buttonClasses = cn(
    'h-12 px-4 rounded-xl font-semibold text-size-3',
    'transition-colors duration-200',
    isHovered ? 'bg-blue-700' : 'bg-blue-600'
  );
  
  return (
    <button
      className={buttonClasses}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {children}
    </button>
  );
}
```

### TDD Commands

```bash
# Generate tests for component
/tdd Button

# Run tests in watch mode
/tr --watch

# Check coverage
/tr --coverage

# TDD dashboard
/tdd-dashboard
```

## Testing Commands

### Command Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `/tr` | Run tests | `/tr all` |
| `/tdd` | Start TDD workflow | `/tdd Button` |
| `/btf` | Browser test flow | `/btf LoginForm` |
| `/test` | Run specific test | `/test Button.test` |
| `/pw-verify` | Playwright verify | `/pw-verify` |
| `/pw-console` | Check console errors | `/pw-console` |
| `/pw-screenshot` | Take screenshot | `/pw-screenshot` |
| `/pw-a11y` | Accessibility test | `/pw-a11y` |

### Test Scripts

```json
// package.json
{
  "scripts": {
    "test": "vitest",
    "test:unit": "vitest run --dir tests/unit",
    "test:integration": "vitest run --dir tests/integration",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:coverage": "vitest run --coverage",
    "test:watch": "vitest watch",
    "test:debug": "vitest --inspect-brk --single-thread",
    "test:ci": "vitest run --reporter=json --reporter=default",
    "test:staged": "vitest related --run"
  }
}
```

## Best Practices

### 1. Test Organization
- Group related tests with `describe`
- Use clear test names
- One assertion per test (when possible)
- Follow AAA pattern (Arrange, Act, Assert)

### 2. Test Data
- Use factories for consistent data
- Clean up after tests
- Avoid hardcoded values
- Use meaningful test data

### 3. Async Testing
- Always await async operations
- Use `waitFor` for eventual consistency
- Set reasonable timeouts
- Handle loading states

### 4. Mocking
- Mock external dependencies
- Keep mocks close to tests
- Reset mocks between tests
- Prefer real implementations when possible

### 5. Performance
- Run tests in parallel
- Use test.skip for slow tests
- Optimize database queries
- Cache test builds

### 6. Debugging
- Use `test.only` to isolate
- Add console.logs temporarily
- Use debugger statements
- Check test artifacts

### 7. Coverage
- Aim for 80%+ coverage
- Focus on critical paths
- Don't test implementation details
- Cover edge cases

## Summary

A comprehensive testing strategy ensures:
- **Confidence** in code changes
- **Fast feedback** during development
- **Documentation** through tests
- **Regression prevention**
- **Quality maintenance**

Remember: Tests are not a burden, they're your safety net. Write tests first, and your code will thank you!
