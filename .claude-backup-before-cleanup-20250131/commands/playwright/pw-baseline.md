# Visual Regression Baseline Management

Manage visual regression testing baselines and comparisons.

## Usage
```bash
/pw-baseline <action> [component] [options]

Actions:
  capture    Capture new baselines
  update     Update existing baselines
  compare    Compare against baselines
  approve    Approve visual changes
  list       List all baselines
  clean      Remove old baselines
```

## Examples

### Capture Initial Baselines
```bash
# Capture all components
/pw-baseline capture all

# Capture specific component
/pw-baseline capture Button

# Capture with variants
/pw-baseline capture Button --variants "default,hover,disabled,loading"

# Capture responsive
/pw-baseline capture Header --viewports "mobile,tablet,desktop"
```

### Update Baselines
```bash
# Update after intentional changes
/pw-baseline update Button

# Update with review
/pw-baseline update Card --review

# Batch update
/pw-baseline update all --changed-only
```

### Compare Visuals
```bash
# Run comparison
/pw-baseline compare Button

Output:
📸 Visual Comparison: Button
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

States Tested: 4
✅ default: No changes
❌ hover: 2.3% difference
✅ disabled: No changes  
⚠️ loading: 0.8% difference

Diff images saved to:
.claude/visual-regression/diffs/Button-hover.png
.claude/visual-regression/diffs/Button-loading.png
```

## Directory Structure

```
.claude/visual-regression/
├── baselines/
│   ├── Button/
│   │   ├── default.png
│   │   ├── hover.png
│   │   ├── disabled.png
│   │   └── loading.png
│   ├── Card/
│   └── Header/
├── current/
│   └── [test-run-images]
├── diffs/
│   └── [difference-images]
├── approved/
│   └── [approved-changes]
└── config.json
```

## Configuration

```json
// .claude/visual-regression/config.json
{
  "threshold": 0.01,  // 1% difference threshold
  "animations": "disabled",
  "waitBeforeScreenshot": 500,
  "fullPage": false,
  "clip": null,
  "viewports": {
    "mobile": { "width": 375, "height": 667 },
    "tablet": { "width": 768, "height": 1024 },
    "desktop": { "width": 1440, "height": 900 }
  },
  "ignore": [
    { "selector": ".timestamp" },
    { "selector": "[data-testid='dynamic']" }
  ]
}
```

## Approval Workflow

```bash
# Review changes
/pw-baseline compare Button --review

Visual Changes Detected:
1. Button hover state
   - Background color changed
   - Shadow added
   
Review at: http://localhost:3000/__visual-regression__

Approve? (y/n): y

# Bulk approve
/pw-baseline approve all --threshold 2

Approved:
- Button (1.8% change)
- Card (0.9% change)
Skipped:
- Header (5.2% change - exceeds threshold)
```

## Advanced Features

### Variant Testing
```bash
# Define variants
/pw-baseline capture Button --variants-config
{
  "default": {},
  "hover": { "pseudo": ":hover" },
  "focus": { "pseudo": ":focus" },
  "active": { "pseudo": ":active" },
  "disabled": { "attribute": "disabled" },
  "loading": { "class": "loading" },
  "sizes": {
    "small": { "class": "size-sm" },
    "medium": { "class": "size-md" },
    "large": { "class": "size-lg" }
  }
}
```

### Mask Dynamic Content
```bash
# Mask changing content
/pw-baseline capture Dashboard --mask ".live-data,.timestamp"

# Custom masks
--mask-color "pink"
--mask-style "striped"
```

### Cross-Browser Baselines
```bash
# Capture in multiple browsers
/pw-baseline capture all --browsers "chromium,firefox,webkit"

# Compare across browsers
/pw-baseline compare Header --cross-browser
```

## CI/CD Integration

```yaml
# Visual regression in CI
- name: Visual tests
  run: |
    # Capture current state
    claude pw-baseline capture all
    
    # Compare with baselines
    claude pw-baseline compare all --ci
    
    # Fail if differences exceed threshold
    claude pw-baseline compare all --fail-on-diff --threshold 1
```

### PR Comments
```bash
# Auto-comment on PR
/pw-baseline compare all --pr-comment

Posts to PR:
📸 Visual Regression Results
- ✅ 23 components unchanged
- ⚠️ 2 components with minor changes (<2%)
- ❌ 1 component needs review (Button)

[View Diff Report](link-to-report)
```

## Maintenance

### Clean Old Baselines
```bash
# Remove unused baselines
/pw-baseline clean --unused

# Archive old versions
/pw-baseline clean --archive --older-than 30d

# Remove specific component
/pw-baseline clean Button --confirm
```

### Baseline History
```bash
# View history
/pw-baseline history Button

Baseline History: Button
- v3: 2024-01-15 (current)
- v2: 2024-01-08 (archived)
- v1: 2024-01-01 (archived)

# Restore previous version
/pw-baseline restore Button --version v2
```

## Best Practices

1. **Capture after stable state**: Wait for animations
2. **Mask dynamic content**: Dates, random IDs
3. **Set appropriate thresholds**: 0-1% for strict
4. **Review before approving**: Check intentional changes
5. **Document changes**: Add notes when updating

## Quick Commands

```bash
# Daily workflow
/pw-baseline capture --changed-only
/pw-baseline compare all
/pw-baseline approve --auto-approve --threshold 0.5

# Before release
/pw-baseline compare all --strict
/pw-baseline report --format html
```

Catch visual regressions before users do! 👁️
