# Browser Performance - Core Web Vitals

Measure Core Web Vitals and performance metrics in real browser.

## Usage
```bash
/pw-vitals [page] [options]

Options:
  --mobile      Test mobile performance
  --throttle    Network: Fast3G|Slow3G|Offline
  --cpu         CPU throttling: 1x|2x|4x|6x
  --runs        Number of test runs (default: 3)
```

## Examples

```bash
# Test current page
/pw-vitals

# Test specific page
/pw-vitals /dashboard

# Mobile performance
/pw-vitals / --mobile

# Slow network test
/pw-vitals /products --throttle Slow3G

# Multiple runs for accuracy
/pw-vitals / --runs 5
```

## Metrics Measured

### Core Web Vitals
- **LCP** (Largest Contentful Paint) - Target: <2.5s
- **FID** (First Input Delay) - Target: <100ms
- **CLS** (Cumulative Layout Shift) - Target: <0.1
- **INP** (Interaction to Next Paint) - Target: <200ms

### Additional Metrics
- **FCP** (First Contentful Paint)
- **TTFB** (Time to First Byte)
- **TTI** (Time to Interactive)
- **TBT** (Total Blocking Time)
- **Speed Index**

## Output Example

```
📊 Core Web Vitals Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Page: /dashboard
Device: Desktop
Network: Fast 3G

Core Web Vitals:
✅ LCP: 1.8s (Good)
✅ FID: 45ms (Good)
⚠️ CLS: 0.15 (Needs Improvement)
✅ INP: 120ms (Good)

Performance Metrics:
- FCP: 0.9s
- TTFB: 320ms
- TTI: 2.1s
- TBT: 230ms
- Speed Index: 1.4s

Score: 85/100 (Good)

Recommendations:
1. Fix layout shift on image load
2. Preload critical fonts
3. Optimize largest image
```

## Detailed Analysis

```bash
# Get detailed breakdown
/pw-vitals / --detailed

LCP Breakdown:
- Resource load: 0.8s
- Render delay: 0.6s
- Load delay: 0.4s
Element: <img class="hero-image">

CLS Issues:
- Banner ad loads late (0.08)
- Font swap causes shift (0.05)
- Dynamic content insertion (0.02)

Resource Timing:
1. document: 320ms
2. styles.css: 450ms
3. app.js: 780ms
4. hero.webp: 1.2s (LCP element)
```

## Performance Budget

```bash
# Check against budgets
/pw-vitals / --budget

Performance Budget Check:
✅ LCP: 1.8s < 2.5s (PASS)
✅ FID: 45ms < 100ms (PASS)
❌ CLS: 0.15 > 0.1 (FAIL)
✅ Bundle: 245kb < 300kb (PASS)

Budget compliance: 75%
```

## Compare Performance

```bash
# Before/after comparison
/pw-vitals / --compare baseline

Performance Comparison:
         Baseline → Current
LCP:     2.1s    → 1.8s ✅ (-14%)
FID:     67ms    → 45ms ✅ (-33%)
CLS:     0.12    → 0.15 ❌ (+25%)
Score:   78      → 85 ✅ (+9%)

Improvements:
- Optimized images
- Reduced JavaScript

Regressions:
- Layout shift increased
```

## Mobile-Specific Testing

```bash
/pw-vitals / --mobile --throttle Slow3G

Mobile Performance (Slow 3G):
⚠️ LCP: 4.2s (Needs Improvement)
✅ FID: 89ms (Good)
❌ CLS: 0.23 (Poor)

Mobile Issues:
- Images too large for mobile
- Viewport issues cause shifts
- JavaScript blocks main thread
```

## Integration with CI/CD

```yaml
# Check vitals in CI
- name: Performance test
  run: |
    claude pw-vitals / --budget
    claude pw-vitals /products --budget
    claude pw-vitals /checkout --budget
```

## Quick Actions

Based on results:
1. **Optimize images**: Use next/image
2. **Fix CLS**: Add size attributes
3. **Reduce JavaScript**: Code split
4. **Preload resources**: Critical CSS/fonts

Keep your site fast! 🚀
