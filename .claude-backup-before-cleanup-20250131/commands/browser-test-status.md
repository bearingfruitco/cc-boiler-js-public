# Browser Test Status

View comprehensive browser testing metrics and status.

## Usage
```bash
/browser-test-status [options]

Options:
  --report      Generate detailed report
  --metrics     Show performance metrics
  --errors      List console errors
  --coverage    Show test coverage
```

## Dashboard View

```
📊 Browser Testing Dashboard
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧪 Test Summary (Last 24h)
├─ Total Tests Run: 127
├─ Passed: 119 (93.7%)
├─ Failed: 8 (6.3%)
└─ Average Duration: 3.2s

🚨 Console Errors
├─ Total Found: 12
├─ Critical: 3
├─ Warnings: 9
└─ Top Error: "Cannot read property 'map' of undefined"

📸 Visual Regression
├─ Baselines: 45
├─ Changes Detected: 3
├─ Approved: 2
└─ Pending Review: 1

♿ Accessibility
├─ Average Score: 94.2
├─ WCAG Violations: 4
├─ Components Tested: 23/28
└─ Keyboard Nav: 100% ✅

📱 Mobile Testing
├─ Viewports Tested: 5
├─ Touch Targets: 98% compliant
├─ Responsive Issues: 2
└─ Performance: Good

⚡ Performance Metrics
├─ Avg LCP: 1.8s (Good)
├─ Avg FID: 52ms (Good)
├─ Avg CLS: 0.03 (Good)
└─ Slowest Component: DataTable (3.2s)

🔄 Recent Activity
├─ 10:32 - Button component tested ✅
├─ 10:28 - Form validation failed ❌
├─ 10:15 - Visual regression detected 📸
└─ 09:45 - PR #234 browser checked ✅
```

## Detailed Reports

### Error Report
```bash
/browser-test-status --errors

🚨 Console Error Report
━━━━━━━━━━━━━━━━━━━━━━━━━━

Critical Errors (3):
1. components/DataTable.tsx
   Error: Cannot read property 'map' of undefined
   Line: 45
   Occurrences: 5
   Last seen: 2 hours ago

2. lib/api.ts  
   Error: Network request failed
   Line: 123
   Occurrences: 3
   Last seen: 1 hour ago

Warnings (9):
1. Deprecation warning: componentWillMount
2. React key warning in List component
...
```

### Coverage Report
```bash
/browser-test-status --coverage

📊 Browser Test Coverage
━━━━━━━━━━━━━━━━━━━━━━━━━━

Components:
✅ Button         100% (12/12 scenarios)
✅ Form           95%  (19/20 scenarios)
⚠️  DataTable     75%  (9/12 scenarios)
❌ Chart          45%  (5/11 scenarios)

User Flows:
✅ Authentication  100%
✅ Checkout        100%
⚠️  Search         80%
❌ Admin Panel     60%

Browser Coverage:
✅ Chrome         100%
⚠️  Safari        80%
❌ Firefox        60%
```

## Integration Points

### With PR Workflow
```yaml
Automatic browser checks on:
- PR creation
- New commits
- Deploy preview ready
- Pre-merge validation
```

### With Development Flow
```yaml
Suggested after:
- Component creation
- UI modifications
- API integrations
- Performance optimizations
```

## Metrics Tracking

```json
{
  "browser_testing": {
    "daily_stats": {
      "tests_run": 127,
      "pass_rate": 0.937,
      "avg_duration_ms": 3200,
      "errors_caught": 12,
      "prevented_issues": 8
    },
    "trends": {
      "pass_rate_7d": "+2.3%",
      "errors_7d": "-15%",
      "coverage_7d": "+5%"
    },
    "impact": {
      "bugs_prevented": 23,
      "time_saved_hours": 15,
      "user_issues_avoided": 45
    }
  }
}
```

## Quick Actions

From the status view:
- `1` - Run failed tests again
- `2` - View error details
- `3` - Open visual diffs
- `4` - Generate report
- `5` - Fix common issues

## Export Options

```bash
# Generate reports
/browser-test-status --report > browser-report.md
/browser-test-status --metrics --json > metrics.json

# CI integration
/browser-test-status --ci --fail-on-errors
```

## Health Indicators

🟢 **Healthy**: >95% pass rate, <5 errors/day
🟡 **Warning**: 85-95% pass rate, 5-10 errors/day  
🔴 **Critical**: <85% pass rate, >10 errors/day

Keep your browser tests healthy! 🏥
