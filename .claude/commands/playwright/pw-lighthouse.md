# Lighthouse Performance Audit

Run comprehensive Lighthouse audits for performance, accessibility, best practices, and SEO.

## Usage
```bash
/pw-lighthouse [url] [options]

Options:
  --categories   Categories to test: performance,accessibility,best-practices,seo,pwa
  --mobile       Run mobile audit
  --desktop      Run desktop audit (default)
  --throttle     Network throttling preset
  --report       Output format: html|json|csv
```

## Examples

```bash
# Full audit
/pw-lighthouse /

# Performance only
/pw-lighthouse / --categories performance

# Mobile audit
/pw-lighthouse / --mobile

# Multiple categories
/pw-lighthouse / --categories performance,accessibility,seo

# Generate HTML report
/pw-lighthouse / --report html
```

## Audit Results

```
🏗️ Lighthouse Audit Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall Scores:
🟢 Performance: 92/100
🟢 Accessibility: 98/100
🟡 Best Practices: 85/100
🟢 SEO: 95/100
🟡 PWA: 73/100

Performance Breakdown:
✅ First Contentful Paint: 0.8s
✅ Speed Index: 1.2s
✅ Largest Contentful Paint: 1.9s
✅ Time to Interactive: 2.1s
✅ Total Blocking Time: 120ms
✅ Cumulative Layout Shift: 0.02

Accessibility Issues (2):
⚠️ Missing alt text on 2 images
⚠️ Low contrast on footer links

Best Practices Issues (3):
⚠️ Uses document.write()
⚠️ Browser errors logged
⚠️ Missing HTTPS on 1 resource

SEO Issues (1):
⚠️ Missing meta description

PWA Missing Features:
❌ No service worker
❌ No web app manifest
❌ Not installable
```

## Detailed Opportunities

```bash
/pw-lighthouse / --opportunities

💡 Performance Opportunities:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Eliminate render-blocking resources
   Potential savings: 0.47s
   - Inline critical CSS
   - Defer non-critical CSS
   
2. Properly size images
   Potential savings: 0.33s
   - hero.jpg: 1.2MB → 245KB
   - gallery-*.jpg: Serve responsive images
   
3. Remove unused JavaScript
   Potential savings: 0.28s
   - vendor.js: 67% unused
   - analytics.js: Load async

4. Enable text compression
   Potential savings: 89KB
   - Enable gzip/brotli

5. Preload key requests
   - Preload main font
   - Preload hero image
```

## Accessibility Audit

```bash
/pw-lighthouse / --categories accessibility --detailed

♿ Accessibility Audit:
━━━━━━━━━━━━━━━━━━━━━━━

✅ Passed (25):
- ARIA attributes valid
- Buttons have accessible names
- Document has title
- Form elements have labels
- Headings in order
- Sufficient color contrast (mostly)

❌ Failed (2):
1. Images missing alt text
   - /images/product-1.jpg
   - /images/product-2.jpg
   Fix: Add descriptive alt=""

2. Links lack contrast
   - Footer links: 2.8:1 (need 4.5:1)
   Fix: Darken to #595959

⚠️ Warnings (3):
- Consider adding skip-to-content
- Video lacks captions
- Some touch targets <44px
```

## Compare with Previous

```bash
/pw-lighthouse / --compare previous

📊 Lighthouse Score Comparison:
                 Previous → Current
Performance:     85      → 92 ✅ (+7)
Accessibility:   92      → 98 ✅ (+6)
Best Practices:  85      → 85 (same)
SEO:            90      → 95 ✅ (+5)

Key Improvements:
- Optimized images (-0.5s LCP)
- Fixed color contrast
- Added meta descriptions
```

## CI Integration

```yaml
# .github/workflows/lighthouse.yml
- name: Run Lighthouse
  run: |
    claude pw-lighthouse / --categories performance,accessibility
    claude pw-lighthouse /products --mobile
    
- name: Upload results
  uses: actions/upload-artifact@v3
  with:
    name: lighthouse-reports
    path: .claude/lighthouse-reports/
```

## Budget Enforcement

```javascript
// lighthouse.config.js
module.exports = {
  budgets: [{
    path: '/*',
    timings: [
      { metric: 'interactive', budget: 3000 },
      { metric: 'first-contentful-paint', budget: 1000 }
    ],
    resourceSizes: [
      { resourceType: 'script', budget: 125 },
      { resourceType: 'total', budget: 300 }
    ],
    resourceCounts: [
      { resourceType: 'third-party', budget: 10 }
    ]
  }]
};
```

## Quick Fixes

Based on common issues:
1. **Images**: Use WebP, lazy load
2. **JavaScript**: Split bundles
3. **CSS**: Inline critical, defer rest
4. **Fonts**: Preload, font-display: swap
5. **Third-party**: Load async

Comprehensive performance auditing! 🚦
