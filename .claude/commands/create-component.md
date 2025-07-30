# Create Component with TDD & Browser Verification - Enhanced

Create a new component with MANDATORY test-first development, design system validation, browser verification, and optional ASCII wireframe step.

⚠️ **TDD + BROWSER TESTING IS NOW STANDARD**: Tests will be generated BEFORE the component is created, and browser verification happens automatically.

## Usage
```bash
/create-component [type] [name] [options]
/cc [type] [name] [options]

# Options:
--wireframe    # Start with ASCII wireframe
--style=ref    # Use reference image for style
--animate      # Include animation planning
--no-tdd       # Skip test generation (NOT RECOMMENDED - requires confirmation)
--no-browser   # Skip browser verification (NOT RECOMMENDED)
--browser-only # Only run browser tests
```

## Enhanced TDD + Browser Flow

### Step 0: Test Generation (MANDATORY)

Before ANY component is created, comprehensive tests are generated:

```typescript
// UserProfile.test.tsx - Generated automatically
describe('UserProfile', () => {
  // Rendering tests
  it('renders user information correctly');
  it('displays placeholder when no image provided');
  
  // Props validation
  it('validates required props');
  it('handles optional props correctly');
  
  // Interaction tests
  it('calls onEdit when edit button clicked');
  it('shows loading state during updates');
  
  // Accessibility tests
  it('has proper ARIA labels');
  it('is keyboard navigable');
  
  // Design system compliance
  it('uses only approved font sizes');
  it('maintains 44px touch targets');
});
```

### Step 0.5: Browser Test Generation (NEW!)

```typescript
// UserProfile.browser.test.ts - Auto-generated
test('UserProfile browser behavior', async ({ page }) => {
  await page.goto('/components/user-profile');
  
  // Visual verification
  await expect(page).toHaveScreenshot();
  
  // Console errors
  const errors = await page.evaluate(() => window.console.errors);
  expect(errors).toHaveLength(0);
  
  // Interaction testing
  await page.click('[data-testid="edit-button"]');
  await expect(page).toHaveURL('/profile/edit');
  
  // Accessibility
  await expect(page.getByRole('button')).toBeFocusable();
});
```

**This happens automatically!** The tdd-engineer and playwright-specialist agents will:
1. Analyze your component requirements
2. Generate unit AND browser tests
3. Ensure real-world behavior is tested
4. Verify in actual browser context

### Step 1: ASCII Wireframe (Optional with --wireframe)

When using `--wireframe`, first generate a quick ASCII layout:

```
┌─────────────────────────────────┐
│ UserProfile Component           │
├─────────────────────────────────┤
│ ┌─────┐  Name: John Doe        │
│ │     │  Role: Developer        │
│ │ IMG │  ─────────────────      │
│ │     │  Bio text here...       │
│ └─────┘  spanning multiple      │
│          lines                  │
├─────────────────────────────────┤
│ [Edit Profile] [Settings]       │
└─────────────────────────────────┘
```

### Step 2: Apply Design System

After wireframe approval, generate with our strict rules:
- Font sizes: text-size-[1-4] only
- Font weights: font-regular, font-semibold only
- Spacing: 4px grid (p-1, p-2, p-3, etc.)
- Touch targets: minimum 44px (h-11)

### Step 3: Animation Planning (Optional with --animate)

Define micro-interactions:
```typescript
const animations = {
  hover: {
    trigger: "onMouseEnter",
    duration: "200ms",
    effect: "scale(1.02) + shadow-lg"
  },
  click: {
    trigger: "onClick", 
    duration: "150ms",
    effect: "scale(0.98)"
  }
};
```

### Step 4: Component Generation & Browser Verification (NEW!)

Generate the actual component with all constraints applied.

**TDD + Browser Enforcement**: The component will ONLY be created after:
- ✅ Unit tests are written and failing
- ✅ Browser tests are written and failing
- ✅ Component implemented to pass unit tests
- ✅ Browser verification passes:
  - No console errors
  - Renders correctly
  - Interactions work
  - Design system compliant
  - Performance acceptable

### Step 5: Automatic Browser Verification (NEW!)

After component creation:
```bash
# Automatically runs:
/pw-verify UserProfile
/pw-console
/pw-screenshot UserProfile

# Reports:
✅ Component renders correctly
✅ No console errors
✅ Click handlers work
✅ Design tokens verified
📸 Screenshot saved
```

## Examples

### Basic Component (Now with TDD + Browser)
```bash
/cc ui Button

# Automatically:
# 1. Generates Button.test.tsx
# 2. Generates Button.browser.test.ts
# 3. Runs tests (fail)
# 4. Creates Button.tsx
# 5. Helps implement to pass tests
# 6. Verifies in real browser
# 7. Captures screenshot
```

### With Wireframe First
```bash
/cc ui Card --wireframe

# Shows ASCII:
┌──────────────────┐
│ ┌────┐           │
│ │IMG │ Title     │
│ └────┘ Subtitle  │
│ Description...   │
│ [Action]         │
└──────────────────┘

# Then generates component with browser tests
```

### Browser-Only Testing (Quick Iteration)
```bash
/cc ui QuickFix --browser-only

# Skips unit tests (not recommended)
# Only runs browser verification
# Useful for rapid prototyping
```

### Complete Flow (With All Features)
```bash
/cc feature Dashboard --wireframe --animate

# 0. Generate Dashboard.test.tsx (AUTOMATIC)
# 1. Generate Dashboard.browser.test.ts (AUTOMATIC)
# 2. ASCII wireframe
# 3. Confirm layout
# 4. Apply design system
# 5. Plan animations
# 6. Generate component
# 7. Verify unit tests pass
# 8. Verify browser tests pass
# 9. Check console errors
# 10. Capture screenshot
```

### Skipping Browser Tests (Not Recommended)
```bash
/cc ui ServerComponent --no-browser

# ⚠️  WARNING: Skipping browser tests!
# Only for server-only components
```

## Integration with Existing Commands

Works with:
- `/vd` - Validates generated component (now includes browser)
- `/pw-verify` - Automatically called after creation
- `/orch` - Can use frontend + playwright agents
- Design hooks - Enforce rules in browser too

## Why Browser Verification Matters

1. **Catches Runtime Errors** - Console errors found immediately
2. **Visual Verification** - Actually looks correct
3. **Interaction Testing** - Clicks/forms actually work
4. **Performance** - Render time measured
5. **Cross-browser** - Works everywhere

## Enhanced Workflow

```
/cc Button
   ↓
[Auto] Generate Button.test.tsx
   ↓
[Auto] Generate Button.browser.test.ts
   ↓
[Auto] Run tests (RED - failing)
   ↓
[User] Create Button.tsx
   ↓
[User] Implement until unit tests pass (GREEN)
   ↓
[Auto] Launch browser and verify
   ↓
[Auto] Check console errors
   ↓
[Auto] Test interactions
   ↓
[Auto] Capture screenshot
   ↓
[Auto] Report results
```

## Browser Test Results

After component creation:
```
📊 Browser Verification Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Rendering: Component displays correctly
✅ Console: No errors detected
✅ Interactions: All handlers work
✅ Design System: 
   - Font sizes: 16px, 24px ✓
   - Spacing: All 4px grid ✓
   - Touch targets: 48px ✓
✅ Performance: 45ms render time
📸 Screenshot: .claude/screenshots/Button.png

Component ready for use!
```

This ensures EVERY component works in real browsers! 🌐
