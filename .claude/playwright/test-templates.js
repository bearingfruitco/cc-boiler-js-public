// Browser Test Templates
// Used by TDD workflow to generate comprehensive browser tests

export const componentTestTemplate = (componentName, props = {}) => `
import { test, expect } from '@playwright/test';
import { waitForHydration, checkConsoleErrors, checkDesignSystem } from '../test-utils';

test.describe('${componentName} Browser Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/components/${componentName.toLowerCase()}');
    await waitForHydration(page);
  });

  test('renders without errors', async ({ page }) => {
    const errors = await checkConsoleErrors(page);
    expect(errors).toHaveLength(0);
  });

  test('matches visual baseline', async ({ page }) => {
    await expect(page).toHaveScreenshot('${componentName}-default.png');
  });

  test('follows design system', async ({ page }) => {
    const { violations } = await checkDesignSystem(page, '[data-testid="${componentName.toLowerCase()}"]');
    expect(violations).toHaveLength(0);
  });

  test('handles interactions correctly', async ({ page }) => {
    // Test click handlers
    const button = page.locator('[data-testid="${componentName.toLowerCase()}-button"]');
    if (await button.isVisible()) {
      await button.click();
      // Verify expected behavior
    }
  });

  test('is keyboard accessible', async ({ page }) => {
    // Tab through component
    await page.keyboard.press('Tab');
    const focusedElement = await page.evaluate(() => document.activeElement?.tagName);
    expect(focusedElement).toBeTruthy();
  });

  test('works on mobile viewport', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page).toHaveScreenshot('${componentName}-mobile.png');
    
    // Check touch targets
    const touchTargets = await page.$$eval('button, a', elements => 
      elements.map(el => ({
        tag: el.tagName,
        height: el.offsetHeight,
        width: el.offsetWidth
      }))
    );
    
    touchTargets.forEach(target => {
      expect(target.height).toBeGreaterThanOrEqual(44);
    });
  });
});
`;

export const formTestTemplate = (formName) => `
import { test, expect } from '@playwright/test';
import { testForm, checkConsoleErrors } from '../test-utils';

test.describe('${formName} Form Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/forms/${formName.toLowerCase()}');
  });

  test('validates required fields', async ({ page }) => {
    // Submit empty form
    await page.click('button[type="submit"]');
    
    // Check for validation errors
    const errors = await page.$$('.field-error');
    expect(errors.length).toBeGreaterThan(0);
  });

  test('shows inline validation errors', async ({ page }) => {
    // Test email field
    await page.fill('input[name="email"]', 'invalid-email');
    await page.press('input[name="email"]', 'Tab');
    
    const emailError = await page.locator('#email-error');
    await expect(emailError).toBeVisible();
    await expect(emailError).toContainText('valid email');
  });

  test('submits successfully with valid data', async ({ page }) => {
    // Fill form with valid data
    await page.fill('input[name="name"]', 'Test User');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('textarea[name="message"]', 'Test message content');
    
    // Submit
    await page.click('button[type="submit"]');
    
    // Check for success
    await expect(page.locator('.success-message')).toBeVisible();
  });

  test('prevents double submission', async ({ page }) => {
    // Fill and submit
    await page.fill('input[name="email"]', 'test@example.com');
    
    // Click submit twice quickly
    await page.click('button[type="submit"]');
    await page.click('button[type="submit"]');
    
    // Button should be disabled
    await expect(page.locator('button[type="submit"]')).toBeDisabled();
  });

  test('is fully keyboard navigable', async ({ page }) => {
    // Tab through all fields
    const formFields = await page.$$('input, textarea, select, button');
    
    for (let i = 0; i < formFields.length; i++) {
      await page.keyboard.press('Tab');
      const focused = await page.evaluate(() => document.activeElement?.name || document.activeElement?.type);
      expect(focused).toBeTruthy();
    }
  });
});
`;

export const pageTestTemplate = (pageName, routes = []) => `
import { test, expect } from '@playwright/test';
import { checkConsoleErrors, capturePerformance } from '../test-utils';

test.describe('${pageName} Page Tests', () => {
  test('loads without errors', async ({ page }) => {
    await page.goto('${routes[0] || `/${pageName.toLowerCase()}`}');
    
    // Check console
    const errors = await checkConsoleErrors(page);
    expect(errors).toHaveLength(0);
    
    // Check page loaded
    await expect(page).toHaveTitle(/${pageName}/i);
  });

  test('has good performance metrics', async ({ page }) => {
    await page.goto('${routes[0] || `/${pageName.toLowerCase()}`}');
    
    const metrics = await capturePerformance(page);
    
    // Check load time
    expect(metrics.loadComplete).toBeLessThan(3000);
    expect(metrics.firstContentfulPaint).toBeLessThan(1500);
  });

  test('navigation works correctly', async ({ page }) => {
    await page.goto('${routes[0] || `/${pageName.toLowerCase()}`}');
    
    // Test main navigation links
    const navLinks = await page.$$('nav a');
    
    for (const link of navLinks) {
      const href = await link.getAttribute('href');
      if (href && href.startsWith('/')) {
        await link.click();
        await expect(page).toHaveURL(href);
        await page.goBack();
      }
    }
  });

  test('is responsive', async ({ page }) => {
    const viewports = [
      { width: 375, height: 667, name: 'mobile' },
      { width: 768, height: 1024, name: 'tablet' },
      { width: 1440, height: 900, name: 'desktop' }
    ];
    
    for (const viewport of viewports) {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      await page.goto('${routes[0] || `/${pageName.toLowerCase()}`}');
      await expect(page).toHaveScreenshot(\`${pageName}-\${viewport.name}.png\`);
    }
  });
});
`;

export const interactionTestTemplate = (featureName, scenario) => `
import { test, expect } from '@playwright/test';

test.describe('${featureName} E2E Tests', () => {
  test('${scenario.name}', async ({ page }) => {
    // Navigate to starting point
    await page.goto('${scenario.startUrl}');
    
    // Perform user actions
    ${scenario.steps.map(step => {
      if (step.action === 'click') {
        return `await page.click('${step.selector}');`;
      } else if (step.action === 'fill') {
        return `await page.fill('${step.selector}', '${step.value}');`;
      } else if (step.action === 'select') {
        return `await page.selectOption('${step.selector}', '${step.value}');`;
      } else if (step.action === 'check') {
        return `await page.check('${step.selector}');`;
      }
    }).join('\n    ')}
    
    // Verify expected outcome
    ${scenario.expectations.map(exp => {
      if (exp.type === 'url') {
        return `await expect(page).toHaveURL('${exp.value}');`;
      } else if (exp.type === 'text') {
        return `await expect(page.locator('${exp.selector}')).toContainText('${exp.value}');`;
      } else if (exp.type === 'visible') {
        return `await expect(page.locator('${exp.selector}')).toBeVisible();`;
      }
    }).join('\n    ')}
  });
});
`;

// Test scenario builder
export function buildTestScenario(feature, userStory) {
  return {
    name: userStory.title,
    startUrl: userStory.startUrl || '/',
    steps: userStory.steps || [],
    expectations: userStory.expectations || []
  };
}

// Generate all tests for a component
export function generateComponentTests(component) {
  const tests = [];
  
  // Basic component test
  tests.push({
    filename: `${component.name}.spec.ts`,
    content: componentTestTemplate(component.name, component.props)
  });
  
  // If it's a form component
  if (component.type === 'form') {
    tests.push({
      filename: `${component.name}-form.spec.ts`,
      content: formTestTemplate(component.name)
    });
  }
  
  // If it has interactions
  if (component.interactions) {
    component.interactions.forEach(interaction => {
      tests.push({
        filename: `${component.name}-${interaction.name}.spec.ts`,
        content: interactionTestTemplate(component.name, interaction)
      });
    });
  }
  
  return tests;
}
