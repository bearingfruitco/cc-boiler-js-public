# /performance-monitor

Real-time performance monitoring and budget enforcement for your application.

## Usage
```
/performance-monitor <action> [options]
```

## Actions

### `check` - Check current performance
```
/performance-monitor check
```
Shows current performance metrics against budgets.

### `baseline` - Create performance baseline
```
/performance-monitor baseline
```
Captures current metrics as baseline for comparison.

### `compare` - Compare against baseline
```
/performance-monitor compare [baseline-name]
```
Shows performance changes since baseline.

### `report` - Generate performance report
```
/performance-monitor report
```
Creates detailed performance analysis.

### `overlay` - Add performance overlay
```
/performance-monitor overlay
```
Adds real-time performance overlay to your app.

## What Gets Monitored

### 1. Bundle Size
- JavaScript bundle size
- CSS bundle size
- Code splitting effectiveness
- Tree shaking efficiency

### 2. Component Performance
- Render time per component
- Re-render frequency
- Memory usage
- Props drilling depth

### 3. API Performance
- Response times
- Payload sizes
- Cache hit rates
- Error rates

### 4. Core Web Vitals
- Largest Contentful Paint (LCP)
- First Input Delay (FID)
- Cumulative Layout Shift (CLS)
- Time to First Byte (TTFB)

## Performance Budgets

Default budgets (configurable in `.claude/performance-budgets.json`):
```json
{
  "budgets": {
    "bundle": {
      "max_size_kb": 500,
      "warning_size_kb": 400
    },
    "component_render": {
      "max_ms": 50,
      "warning_ms": 30
    },
    "api_response": {
      "max_ms": 200,
      "warning_ms": 100
    },
    "page_load": {
      "max_ms": 3000,
      "warning_ms": 2000
    }
  }
}
```

## Real-Time Overlay

The performance overlay shows:
```
┌─── Performance Monitor ─────────────┐
│ Component      Render   Memory  Alert│
│ Header         12ms     2.1MB    ✅  │
│ UserList       234ms    15.2MB   ⚠️  │
│ Dashboard      45ms     8.7MB    ✅  │
│                                      │
│ Bundle Size: 342KB / 500KB          │
│ API Avg: 89ms                       │
│ FPS: 60                             │
└──────────────────────────────────────┘
```

## Automated Optimizations

When performance issues are detected:

1. **Bundle Size Issues**
   - Suggests code splitting points
   - Identifies large dependencies
   - Recommends lazy loading
   - Shows tree-shaking opportunities

2. **Render Performance Issues**
   - Identifies expensive renders
   - Suggests memo opportunities
   - Detects unnecessary re-renders
   - Recommends virtualization

3. **API Performance Issues**
   - Suggests caching strategies
   - Identifies N+1 queries
   - Recommends pagination
   - Shows parallel fetch opportunities

## Integration with CI/CD

Add to your CI pipeline:
```yaml
- name: Performance Check
  run: |
    /performance-monitor baseline
    # Run tests
    /performance-monitor compare
```

## Example Workflow

1. **Set Baseline**
   ```
   /performance-monitor baseline
   ```

2. **Make Changes**
   Implement new features or optimizations

3. **Check Impact**
   ```
   /performance-monitor compare
   ```

4. **Get Optimization Suggestions**
   ```
   /performance-monitor report
   ```

## Performance Tracking Code

The command automatically adds performance tracking:

```typescript
// Automatic performance measurement
export function UserList() {
  // Added by performance monitor
  usePerformanceMeasure('UserList');
  
  return (
    // Your component code
  );
}
```

## Alerts and Notifications

Configure alerts in `.claude/performance-budgets.json`:
```json
{
  "alerts": {
    "enabled": true,
    "channels": {
      "console": true,
      "overlay": true,
      "slack": "webhook-url",
      "email": "team@example.com"
    },
    "thresholds": {
      "critical": 150,  // % of budget
      "warning": 80     // % of budget
    }
  }
}
```

## Related Commands
- `/optimize` - Run performance optimizations
- `/bundle-analyze` - Analyze bundle composition
- `/lighthouse` - Run Lighthouse audit
- `/profile` - Profile specific components
