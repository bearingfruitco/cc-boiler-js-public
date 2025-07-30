// Browser Test Utilities
// Common helpers for Playwright testing

export const testConfig = {
  baseURL: process.env.BASE_URL || 'http://localhost:3000',
  timeout: 30000,
  retries: 2,
  use: {
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure'
  }
};

// Wait for hydration to complete
export async function waitForHydration(page) {
  await page.waitForFunction(() => {
    const root = document.querySelector('#__next') || document.querySelector('#root');
    return root && !root.hasAttribute('data-reactroot');
  });
  // Additional wait for React to settle
  await page.waitForTimeout(100);
}

// Check for console errors
export async function checkConsoleErrors(page) {
  const errors = [];
  
  page.on('console', msg => {
    if (msg.type() === 'error') {
      errors.push({
        text: msg.text(),
        location: msg.location(),
        args: msg.args()
      });
    }
  });
  
  page.on('pageerror', error => {
    errors.push({
      text: error.message,
      stack: error.stack
    });
  });
  
  return errors;
}

// Check design system compliance
export async function checkDesignSystem(page, selector) {
  const element = await page.locator(selector);
  
  const styles = await element.evaluate(el => {
    const computed = window.getComputedStyle(el);
    return {
      fontSize: computed.fontSize,
      fontWeight: computed.fontWeight,
      padding: computed.padding,
      margin: computed.margin,
      minHeight: computed.minHeight,
      color: computed.color,
      backgroundColor: computed.backgroundColor
    };
  });
  
  const violations = [];
  
  // Check font sizes (must be 12px, 16px, 24px, or 32px)
  const validFontSizes = ['12px', '16px', '24px', '32px'];
  if (!validFontSizes.includes(styles.fontSize)) {
    violations.push(`Invalid font size: ${styles.fontSize}`);
  }
  
  // Check font weights (must be 400 or 600)
  const validWeights = ['400', '600'];
  if (!validWeights.includes(styles.fontWeight)) {
    violations.push(`Invalid font weight: ${styles.fontWeight}`);
  }
  
  // Check spacing (must be divisible by 4)
  const spacingValues = [
    ...styles.padding.split(' ').map(v => parseInt(v)),
    ...styles.margin.split(' ').map(v => parseInt(v))
  ].filter(v => !isNaN(v));
  
  spacingValues.forEach(value => {
    if (value % 4 !== 0) {
      violations.push(`Invalid spacing: ${value}px (must be divisible by 4)`);
    }
  });
  
  // Check touch targets (min 44px)
  const minHeight = parseInt(styles.minHeight);
  if (!isNaN(minHeight) && minHeight < 44 && element.matches('button, a, input, select, textarea')) {
    violations.push(`Touch target too small: ${minHeight}px (min 44px)`);
  }
  
  return {
    styles,
    violations,
    compliant: violations.length === 0
  };
}

// Test form functionality
export async function testForm(page, formSelector) {
  const form = await page.locator(formSelector);
  const results = {
    validation: {},
    submission: {},
    accessibility: {}
  };
  
  // Test empty submission
  await form.locator('button[type="submit"]').click();
  results.validation.emptySubmission = await page.locator('.error-message').count() > 0;
  
  // Test field validation
  const fields = await form.locator('input, textarea, select').all();
  for (const field of fields) {
    const fieldName = await field.getAttribute('name');
    const fieldType = await field.getAttribute('type');
    
    // Test invalid values
    if (fieldType === 'email') {
      await field.fill('invalid-email');
      await field.blur();
      results.validation[fieldName] = await page.locator(`[id="${fieldName}-error"]`).isVisible();
    }
  }
  
  // Test successful submission
  // Fill valid data...
  
  // Test accessibility
  results.accessibility.labels = await form.evaluate(form => {
    const inputs = form.querySelectorAll('input, textarea, select');
    return Array.from(inputs).every(input => {
      const label = form.querySelector(`label[for="${input.id}"]`);
      return label !== null;
    });
  });
  
  results.accessibility.errorAnnouncements = await form.evaluate(form => {
    const errors = form.querySelectorAll('[role="alert"]');
    return errors.length > 0;
  });
  
  return results;
}

// Capture visual regression baseline
export async function captureBaseline(page, name, options = {}) {
  const screenshotOptions = {
    path: `.claude/visual-regression/baselines/${name}.png`,
    fullPage: options.fullPage || false,
    animations: 'disabled',
    mask: options.mask || []
  };
  
  // Wait for stable state
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(options.wait || 500);
  
  // Disable animations
  await page.addStyleTag({
    content: `
      *, *::before, *::after {
        animation-duration: 0s !important;
        animation-delay: 0s !important;
        transition-duration: 0s !important;
        transition-delay: 0s !important;
      }
    `
  });
  
  await page.screenshot(screenshotOptions);
}

// Compare against baseline
export async function compareVisual(page, name, threshold = 0.01) {
  const currentPath = `.claude/visual-regression/current/${name}.png`;
  const baselinePath = `.claude/visual-regression/baselines/${name}.png`;
  const diffPath = `.claude/visual-regression/diffs/${name}.png`;
  
  // Capture current
  await page.screenshot({ path: currentPath });
  
  // Use pixelmatch or similar for comparison
  // This is a placeholder - actual implementation would use image comparison library
  const difference = 0; // Calculate actual difference
  
  return {
    difference,
    passed: difference <= threshold,
    paths: {
      current: currentPath,
      baseline: baselinePath,
      diff: diffPath
    }
  };
}

// Test accessibility
export async function testAccessibility(page, options = {}) {
  // This would integrate with axe-core or similar
  // Placeholder implementation
  
  const results = {
    violations: [],
    passes: [],
    incomplete: []
  };
  
  // Check keyboard navigation
  results.keyboardNav = await page.evaluate(() => {
    const focusableElements = document.querySelectorAll(
      'a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    return focusableElements.length > 0;
  });
  
  // Check ARIA labels
  results.ariaLabels = await page.evaluate(() => {
    const buttons = document.querySelectorAll('button');
    return Array.from(buttons).every(btn => 
      btn.textContent.trim() || btn.getAttribute('aria-label')
    );
  });
  
  return results;
}

// Performance metrics
export async function capturePerformance(page) {
  const metrics = await page.evaluate(() => {
    const navigation = performance.getEntriesByType('navigation')[0];
    const paint = performance.getEntriesByType('paint');
    
    return {
      // Navigation timing
      domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
      loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
      
      // Paint timing
      firstPaint: paint.find(p => p.name === 'first-paint')?.startTime,
      firstContentfulPaint: paint.find(p => p.name === 'first-contentful-paint')?.startTime,
      
      // Core Web Vitals (simplified)
      // Real implementation would use web-vitals library
    };
  });
  
  return metrics;
}

// Test utilities export
export default {
  testConfig,
  waitForHydration,
  checkConsoleErrors,
  checkDesignSystem,
  testForm,
  captureBaseline,
  compareVisual,
  testAccessibility,
  capturePerformance
};
