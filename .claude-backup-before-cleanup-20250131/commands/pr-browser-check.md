# PR Browser Check

Automated browser testing for pull request preview deployments.

## Usage
```bash
/pr-browser-check [pr-number]

# Or use the chain
/chain pr-browser-check
```

## Automated Workflow

### 1. Detect Preview URL
```javascript
// Automatically find Vercel/Netlify preview URL
const previewUrl = await detectPreviewUrl(prNumber);
// Example: https://my-app-pr-123.vercel.app
```

### 2. Run Test Suite
```yaml
Tests performed:
- Smoke tests (critical paths)
- Console error detection
- Visual regression
- Performance metrics
- Accessibility scan
- Mobile responsiveness
```

### 3. Generate Report
```markdown
## 🔍 Browser Test Results for PR #123

### ✅ Smoke Tests (5/5 passed)
- Homepage loads correctly
- Navigation works
- Forms submit successfully
- Auth flow completes
- Data displays properly

### 🚨 Console Errors (2 found)
```
❌ Button.tsx:45 - Cannot read property 'onClick' of undefined
⚠️ api.ts:23 - Deprecated API warning
```

### 📸 Visual Changes
| Before | After |
|--------|-------|
| ![](baseline.png) | ![](current.png) |

**Changed:** Button hover state color

### 📊 Performance Metrics
- LCP: 1.2s ✅ (threshold: 2.5s)
- FID: 45ms ✅ (threshold: 100ms)  
- CLS: 0.05 ✅ (threshold: 0.1)
- Bundle size: +2.3kb ⚠️

### ♿ Accessibility
- Score: 94/100
- Issues: 1 low contrast warning
- Keyboard nav: ✅ Working

### 📱 Mobile Testing
- Responsive breakpoints: ✅
- Touch targets: ✅ All ≥ 44px
- Viewport scaling: ✅ Correct
```

### 4. Post to PR
```typescript
// Automatically comment on PR
await github.createComment({
  issue_number: prNumber,
  body: testReport
});

// Update PR status
await github.createStatus({
  state: consoleErrors.length > 0 ? 'failure' : 'success',
  description: `Browser tests: ${passed}/${total} passed`,
  context: 'browser-tests'
});
```

### 5. Block Merge on Failures
```yaml
# GitHub branch protection rules
required_status_checks:
  - browser-tests
  - visual-regression
  - accessibility
```

## Integration with GitHub Actions

```yaml
# .github/workflows/pr-browser-tests.yml
name: PR Browser Tests

on:
  pull_request:
    types: [opened, synchronize]
  deployment_status:
    
jobs:
  browser-tests:
    if: github.event.deployment_status.state == 'success'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Wait for deployment
        run: sleep 30
        
      - name: Run browser tests
        env:
          PREVIEW_URL: ${{ github.event.deployment_status.target_url }}
        run: |
          npx claude pr-browser-check ${{ github.event.pull_request.number }}
```

## Test Configuration

```javascript
// .claude/playwright/pr-config.js
export default {
  criticalPaths: [
    { name: 'Homepage', path: '/' },
    { name: 'Login', path: '/login', actions: ['fill', 'submit'] },
    { name: 'Dashboard', path: '/dashboard', auth: true }
  ],
  
  performanceBudgets: {
    lcp: 2500,
    fid: 100,
    cls: 0.1,
    bundleSize: 500000 // 500kb
  },
  
  visualRegression: {
    threshold: 0.01, // 1% difference
    ignoreAreas: ['.dynamic-content', '[data-testid="timestamp"]']
  },
  
  accessibility: {
    standard: 'WCAG2.1AA',
    ignoreRules: ['color-contrast'] // if needed
  }
};
```

## Quick Commands

```bash
# Run specific tests only
/pr-browser-check 123 --smoke-only
/pr-browser-check 123 --visual-only
/pr-browser-check 123 --a11y-only

# Skip certain checks
/pr-browser-check 123 --skip-performance
/pr-browser-check 123 --skip-mobile

# Custom threshold
/pr-browser-check 123 --performance-threshold 10
```

## Debugging Failures

When tests fail:

1. **Check screenshots**: Saved to `.claude/pr-screenshots/`
2. **View console logs**: Full logs in report
3. **Reproduce locally**: 
   ```bash
   /pw "navigate to preview URL and reproduce issue"
   ```
4. **Get detailed trace**:
   ```bash
   /pw-debug "specific failing test"
   ```

## Success Metrics

Track PR testing effectiveness:
- Issues caught before merge
- False positive rate
- Test execution time
- Coverage of critical paths

This ensures every PR is browser-tested before merge! 🚀
