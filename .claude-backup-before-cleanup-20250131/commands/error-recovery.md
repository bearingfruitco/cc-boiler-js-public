# Error Recovery (Enhanced with Browser Debugging)

Recover from common development errors and issues with browser context awareness.

## Arguments:
- $TYPE: git|build|test|design|deps|browser|all
- $ACTION: diagnose|fix|rollback|debug

## Why This Command:
- Quick recovery from common issues
- Browser-aware debugging for UI problems
- Maintains context during fixes
- Prevents work loss
- Reduces debugging time

## Steps:

### Type: GIT
Handle git-related issues:

```bash
# Diagnose
/error-recovery git diagnose
> "Detached HEAD detected"
> "3 uncommitted files at risk"
> "Suggested: /error-recovery git fix"

# Fix common issues
case "$ISSUE" in
  "detached-head")
    git checkout -b temp-recovery-$(date +%s)
    echo "✅ Created recovery branch"
    ;;
  "merge-conflict")
    echo "Conflicts in:"
    git diff --name-only --diff-filter=U
    echo "Run: git mergetool"
    ;;
  "large-file")
    git reset HEAD~1
    echo "Use: git lfs track '*.psd'"
    ;;
esac
```

### Type: BUILD
Fix build errors:

```bash
# Common Next.js issues
"Module not found" -> npm install
"Type error" -> Run tsc --noEmit
"Build failed" -> Clear cache and retry

# Auto-fix attempt
rm -rf .next node_modules
npm install
npm run build

# NEW: Check if build errors affect browser
if [[ "$BUILD_ERROR" == *"client"* ]]; then
  echo "🌐 Browser impact detected!"
  /pw-console  # Check for runtime errors
fi
```

### Type: DESIGN
Fix design violations:

```bash
# Auto-fix common violations
find . -name "*.tsx" -type f -exec sed -i '' \
  -e 's/text-sm/text-size-3/g' \
  -e 's/text-lg/text-size-2/g' \
  -e 's/font-bold/font-semibold/g' \
  -e 's/p-5/p-4/g' \
  {} \;

echo "✅ Fixed common violations"
echo "Run: /validate-design"

# NEW: Verify fixes in browser
echo "🌐 Verifying design fixes in browser..."
/pw-verify --design-only
```

### Type: BROWSER (NEW!)
Debug browser-specific issues:

```bash
# Diagnose browser problems
/error-recovery browser diagnose

# Common browser issues and fixes:
case "$BROWSER_ISSUE" in
  "console-errors")
    /pw-console --detailed
    /pw-debug "console errors"
    ;;
  
  "not-rendering")
    # Check if component renders
    /pw-verify $COMPONENT
    # Check for hydration errors
    /pw "check for hydration mismatches"
    ;;
  
  "click-not-working")
    # Debug event handlers
    /pw-debug "click handler on $ELEMENT"
    # Check z-index issues
    /pw "evaluate z-index stacking"
    ;;
  
  "style-broken")
    # Verify computed styles
    /pw "check computed styles for $COMPONENT"
    # Compare with design system
    /validate-design browser
    ;;
  
  "form-not-submitting")
    # Test form flow
    /pw-form $FORM_NAME
    # Check validation
    /pw "test form validation"
    ;;
esac

# Automated browser diagnostics
echo "🔍 Running browser diagnostics..."
/pw "navigate to problem page and check:"
/pw "- Console errors"
/pw "- Network failures"  
/pw "- JavaScript exceptions"
/pw "- CSS loading issues"
/pw "- Event listener problems"
```

### Type: DEPS
Fix dependency issues:

```bash
# Clear all caches
rm -rf node_modules .next .turbo
rm package-lock.json pnpm-lock.yaml

# Reinstall
pnpm install --force

# Verify
pnpm run typecheck

# NEW: Check if deps affect browser
echo "🌐 Checking browser impact..."
/pw-test smoke  # Quick browser smoke test
```

### Browser Error Patterns (NEW!)

Common browser errors and automated fixes:

```javascript
// Console Error: "Cannot read property 'map' of undefined"
Fix: Check for null/undefined before mapping
/pw "verify data exists before .map()"

// Console Error: "Hydration mismatch"
Fix: Ensure server/client render match
/pw "check for dynamic content causing hydration issues"

// Console Error: "Failed to fetch"
Fix: Check API endpoints and CORS
/pw "test API calls and network requests"

// No visible error but broken
Fix: Check event propagation
/pw "verify event bubbling and handlers"
```

### Emergency Rollback
When all else fails:

```bash
# Save current state
/checkpoint create emergency-$(date +%s)

# Save browser state too (NEW!)
/pw-screenshot --full-page --label "pre-rollback"
/browser-test-status --export

# Find last working commit
LAST_GOOD=$(git log --format="%h %s" -20 | \
  grep -E "(feat|fix|chore)" | head -1 | cut -d' ' -f1)

# Create recovery branch
git checkout -b recovery-$(date +%s) $LAST_GOOD

echo "✅ Rolled back to: $LAST_GOOD"
echo "Lost work saved in checkpoint"

# Verify browser works after rollback (NEW!)
echo "🌐 Verifying browser functionality..."
/pw-test smoke
```

## Browser-Aware Recovery Workflow (NEW!)

```
Error Detected
     ↓
/error-recovery browser diagnose
     ↓
Playwright agent investigates:
- Console errors
- Network issues
- Rendering problems
- Event handlers
     ↓
Automated fix suggested
     ↓
Apply fix and verify:
/pw-verify
/pw-console
     ↓
Problem resolved!
```

## Integration:
- Captures context before any fixes
- Includes browser state in diagnostics
- Updates context after resolution
- Links to relevant documentation
- Suggests preventive measures
- Verifies fixes in real browser

## Quick Commands:

```bash
# Quick browser debug
/er browser debug

# Fix console errors
/er browser fix console

# Debug click issues  
/er browser debug clicks

# Fix rendering problems
/er browser fix render
```

Browser debugging is now part of error recovery! 🔧🌐
