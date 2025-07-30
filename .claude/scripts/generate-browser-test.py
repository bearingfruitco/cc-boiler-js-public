#!/usr/bin/env python3
"""
Browser Test Template Generator
Generates Playwright test files alongside unit tests
"""

import sys
import os
from pathlib import Path

def generate_browser_test_template(component_name, component_path):
    """Generate a browser test template for a component"""
    
    # Determine if it's a form
    is_form = 'form' in component_name.lower()
    
    template = f'''import {{ test, expect }} from '@playwright/test';

test.describe('{component_name} Browser Tests', () => {{
  test.beforeEach(async ({{ page }}) => {{
    // Navigate to the page containing the component
    await page.goto('/'); // Update with actual route
  }});

  test('component renders without console errors', async ({{ page }}) => {{
    // Listen for console errors
    const consoleErrors: string[] = [];
    page.on('console', (msg) => {{
      if (msg.type() === 'error') {{
        consoleErrors.push(msg.text());
      }}
    }});

    // Wait for component to be visible
    await page.waitForSelector('[data-testid="{component_name.lower()}"]');
    
    // Check no console errors
    expect(consoleErrors).toHaveLength(0);
  }});
'''

    if is_form:
        template += f'''
  test('form submission works correctly', async ({{ page }}) => {{
    // Fill form fields
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'SecurePass123!');
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Verify submission (update based on your app behavior)
    await expect(page).toHaveURL('/success');
    // OR check for success message
    // await expect(page.locator('.success-message')).toBeVisible();
  }});

  test('shows validation errors for invalid input', async ({{ page }}) => {{
    // Submit empty form
    await page.click('button[type="submit"]');
    
    // Check for validation errors
    await expect(page.locator('[role="alert"]')).toContainText('required');
  }});

  test('form is keyboard accessible', async ({{ page }}) => {{
    // Tab through form
    await page.keyboard.press('Tab');
    await expect(page.locator(':focus')).toHaveAttribute('name', 'email');
    
    await page.keyboard.type('test@example.com');
    await page.keyboard.press('Tab');
    await expect(page.locator(':focus')).toHaveAttribute('name', 'password');
    
    await page.keyboard.type('password');
    await page.keyboard.press('Enter');
    
    // Verify form submitted
    await expect(page).toHaveURL('/success');
  }});
'''
    else:
        template += f'''
  test('component interactions work correctly', async ({{ page }}) => {{
    // Test click handlers
    await page.click('[data-testid="{component_name.lower()}-button"]');
    
    // Verify expected behavior (update based on your component)
    await expect(page.locator('.result')).toBeVisible();
  }});

  test('component is keyboard accessible', async ({{ page }}) => {{
    // Tab to component
    await page.keyboard.press('Tab');
    
    // Verify focus
    await expect(page.locator('[data-testid="{component_name.lower()}"]')).toBeFocused();
    
    // Activate with keyboard
    await page.keyboard.press('Enter');
    
    // Verify activation worked
    await expect(page.locator('.active')).toBeVisible();
  }});
'''

    template += f'''
  test('component meets accessibility standards', async ({{ page }}) => {{
    // Basic accessibility checks
    const component = page.locator('[data-testid="{component_name.lower()}"]');
    
    // Has proper ARIA labels
    await expect(component).toHaveAttribute('aria-label', /.+/);
    
    // Color contrast (this is a basic check - use axe-core for comprehensive testing)
    const bgColor = await component.evaluate((el) => 
      window.getComputedStyle(el).backgroundColor
    );
    expect(bgColor).not.toBe('transparent');
  }});

  test('component performs well', async ({{ page }}) => {{
    // Measure render time
    const startTime = Date.now();
    await page.goto('/');
    await page.waitForSelector('[data-testid="{component_name.lower()}"]');
    const renderTime = Date.now() - startTime;
    
    // Component should render quickly
    expect(renderTime).toBeLessThan(1000); // 1 second max
  }});
}});
'''

    return template

def main():
    if len(sys.argv) < 2:
        print("Usage: generate-browser-test.py <ComponentName>")
        sys.exit(1)
    
    component_name = sys.argv[1]
    
    # Generate test file path
    test_file = f"{component_name}.browser.test.ts"
    
    # Generate template
    template = generate_browser_test_template(component_name, "")
    
    # Write file
    with open(test_file, 'w') as f:
        f.write(template)
    
    print(f"✅ Created {test_file}")
    print(f"📝 Remember to:")
    print(f"   1. Update the page.goto() URL")
    print(f"   2. Update selectors to match your component")
    print(f"   3. Add specific interaction tests")

if __name__ == "__main__":
    main()
