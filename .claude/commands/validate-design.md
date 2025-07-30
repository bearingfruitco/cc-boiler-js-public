# Validate Design System Compliance (Enhanced with Browser Verification)

Comprehensive validation including design system rules, Biome linting, Bun tests, and browser verification.

## Arguments:
- $SCOPE: current|all|fix|browser
- $TYPE: design|lint|test|browser|all (default: all)

## Usage:
```bash
/validate-design              # Full validation of current file
/validate-design all          # Validate entire project
/validate-design fix          # Auto-fix what's possible
/validate-design browser      # Include browser verification
/vd                          # Short alias
```

## Steps:

### 1. Design System Check

```typescript
// Typography violations
const fontSizeViolations = findClasses(/(text-(xs|sm|base|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl))/g);
const fontWeightViolations = findClasses(/(font-(thin|extralight|light|normal|medium|bold|extrabold|black))/g);

// Spacing violations (non-4px grid)
const spacingViolations = findClasses(/(p|m|gap|space)-(5|7|9|10|11|13|14|15|17|18|19)/g);

// Touch target analysis
const smallTargets = findElements('h-[0-9]+').filter(h => parseInt(h) < 44);

// Color distribution
const backgrounds = countClasses(/bg-(white|gray-50)/g);
const textColors = countClasses(/text-(gray-[67]00)/g);
const accents = countClasses(/(bg|text)-(blue|red|green)-[56]00/g);
```

### 2. Biome Linting

```bash
# Run Biome check on file
if [[ "$TYPE" == "lint" || "$TYPE" == "all" ]]; then
  echo "🔍 Running Biome linting..."
  
  if [[ "$SCOPE" == "current" ]]; then
    pnpm biome check "$CURRENT_FILE"
  else
    pnpm lint
  fi
  
  BIOME_EXIT=$?
fi
```

### 3. Test Validation

```bash
# Run related tests
if [[ "$TYPE" == "test" || "$TYPE" == "all" ]]; then
  echo "🧪 Running tests..."
  
  # Find test file
  TEST_FILE="${CURRENT_FILE%.tsx}.test.tsx"
  
  if [ -f "$TEST_FILE" ]; then
    bun test "$TEST_FILE"
    TEST_EXIT=$?
  else
    echo "⚠️ No test file found"
    TEST_EXIT=1
  fi
fi
```

### 4. Browser Verification (NEW!)

```bash
# Verify in real browser using Playwright
if [[ "$TYPE" == "browser" || "$TYPE" == "all" || "$SCOPE" == "browser" ]]; then
  echo "🌐 Running browser verification..."
  
  # Use playwright-specialist agent
  /pw "verify design compliance for $CURRENT_FILE"
  
  # The agent will:
  # 1. Launch browser
  # 2. Navigate to component
  # 3. Check computed styles
  # 4. Verify rendering
  # 5. Check console errors
  # 6. Test interactions
  
  BROWSER_EXIT=$?
fi
```

### 5. Full Validation Report

```markdown
# 📊 Validation Report: ComponentName.tsx

## 🎨 Design System (3 issues)
❌ **Critical Violations:**
- Line 42: `text-sm` → use `text-size-4`
- Line 67: `font-bold` → use `font-semibold`
- Line 89: `p-5` → use `p-4` or `p-6`

⚠️ **Warnings:**
- Touch target on line 34 is only 40px (min: 44px)
- Color distribution: 70/25/5 (target: 60/30/10)

## 🔍 Biome Linting (2 issues)
⚠️ **Warnings:**
- Line 15: noConsoleLog - Remove console.log
- Line 23: noUnusedVariables - 'temp' is declared but never used

## 🧪 Test Coverage
✅ **Tests Passing:** 5/5
📊 **Coverage:** 87% (target: 80%)

## 🌐 Browser Verification (NEW!)
✅ **Rendering:** Component renders correctly
✅ **Console:** No errors detected
✅ **Computed Styles:** 
  - Font sizes: 16px, 24px ✓
  - Font weights: 400, 600 ✓
  - Spacing: All divisible by 4 ✓
⚠️ **Interactions:** Click handler on line 45 not firing
📸 **Screenshot:** Saved to .claude/screenshots/ComponentName.png

## 📋 Summary
- Design: 3 critical, 2 warnings
- Linting: 0 errors, 2 warnings  
- Tests: All passing
- Browser: 1 issue found
- **Status:** ❌ Fix required
```

### 6. Auto-Fix Mode

```bash
if [[ "$SCOPE" == "fix" ]]; then
  echo "🔧 Auto-fixing issues..."
  
  # 1. Fix design system violations
  echo "Fixing design violations..."
  # Run design fix script
  
  # 2. Fix Biome issues
  echo "Running Biome auto-fix..."
  pnpm biome check --apply "$CURRENT_FILE"
  pnpm biome format --write "$CURRENT_FILE"
  
  # 3. Update tests if needed
  echo "Updating tests..."
  # Generate missing tests
  
  # 4. Verify fixes in browser
  echo "Verifying fixes in browser..."
  /pw-verify "$CURRENT_FILE"
  
  echo "✅ Auto-fix complete! Review changes with: git diff"
fi
```

## Integration with Hooks

This command is called by pre-commit hooks and enhanced with browser checks:

```python
# .claude/hooks/pre-tool-use/02-design-check.py
# Runs validate-design before file changes

# .claude/hooks/post-tool-use/05-browser-verify.py
# Suggests browser verification after UI changes
```

## Quick Checks

For specific validation only:

```bash
/vd design     # Only design system
/vd lint       # Only Biome linting  
/vd test       # Only run tests
/vd browser    # Only browser verification (NEW!)
```

## CI Integration

```bash
# In CI pipeline
/validate-design all --ci

# With browser tests on PR
/validate-design browser --pr

# Fails with exit code 1 if any issues
```

## Performance Metrics

Track validation performance:
```json
{
  "validation-times": {
    "design": "50ms",
    "biome": "200ms",
    "tests": "800ms",
    "browser": "2500ms",
    "total": "3550ms"
  },
  "browser-metrics": {
    "console-errors": 0,
    "render-time": "45ms",
    "interaction-tests": 12,
    "accessibility-score": 98
  }
}
```

## Auto-fix Mapping

```javascript
const fixes = {
  'text-sm': 'text-size-4',
  'text-base': 'text-size-3',
  'text-lg': 'text-size-2',
  'text-xl': 'text-size-2',
  'text-2xl': 'text-size-1',
  'font-bold': 'font-semibold',
  'font-medium': 'font-semibold',
  'p-5': 'p-6',
  'p-7': 'p-8',
  'h-10': 'h-11' // 40px → 44px
};
```

## Browser-Specific Validations

The playwright-specialist agent performs:
1. **Computed Style Verification** - Actual rendered values
2. **Console Error Detection** - Runtime JavaScript issues
3. **Interaction Testing** - Click handlers, hover states
4. **Visual Regression** - Screenshot comparison
5. **Performance Metrics** - Render time, reflows

This ensures comprehensive validation with design system, Biome, tests, AND real browser verification! 🚀
