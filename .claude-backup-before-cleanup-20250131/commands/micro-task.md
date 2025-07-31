# Micro Task - Quick Task Creation (TDD Enhanced)

🧪 **MICRO-TESTS**: Even 5-minute tasks get test coverage!

## Command: micro-task
**Aliases:** `mt`, `quick-task`, `tiny`

## Description
Creates micro-tasks (< 5 minutes) with AUTOMATIC micro-test generation. Even the smallest changes get test coverage to prevent regressions.

## Usage
```bash
/micro-task "Add loading spinner to submit button"
# Automatically generates: test('shows loading spinner on submit')

/mt "Fix typo in header" --no-tdd
# ⚠️ Requires confirmation to skip tests

/quick-task "Update color to blue-600" --component Button
# Generates: test('button uses blue-600 color')
```

## Options
- `--component [name]` - Specify component for focused work
- `--no-tdd` - Skip testing (requires confirmation)
- `--chain` - Chain multiple micro-tasks
- `--convert` - Convert to full task if grows beyond 5 min
- `--quick-test` - Generate minimal test (1-2 assertions)

## Task Hierarchy

```
PRD Level (Strategic)
└── Generated Tasks (5-15 min)
    └── Micro Tasks (< 5 min)  ← You are here
```

## When to Use Micro Tasks

### Perfect For (with micro-tests):
- Typo fixes → `test('displays correct text')`
- Color/style adjustments → `test('applies correct styles')`
- Adding simple props → `test('handles new prop correctly')`
- Updating text content → `test('shows updated content')`
- Simple validation rules → `test('validates input correctly')`
- Minor refactors → `test('maintains behavior after refactor')`
- Console.logs for debugging → No test needed (use --no-tdd)

### Use Regular Tasks For:
- New components
- API changes
- Business logic
- Database modifications
- Complex debugging
- Feature additions

## Examples

### Simple UI Fix (with micro-test)
```bash
/mt "Change button text from 'Submit' to 'Save Changes'"

# Auto-generates:
test('button displays "Save Changes" text', () => {
  render(<Button />);
  expect(screen.getByRole('button')).toHaveTextContent('Save Changes');
});

# Then makes the 1-line change
```

### Quick Style Update (with test)
```bash
/micro-task "Add hover state to card component" --component Card

# Auto-generates:
test('card shows hover state', () => {
  const { container } = render(<Card />);
  const card = container.firstChild;
  
  fireEvent.mouseEnter(card);
  expect(card).toHaveClass('hover:shadow-lg');
});

# Then adds the hover styles
```

### Debugging Addition (no test needed)
```bash
/mt "Add console.log to track form submission values" --no-tdd

# ⚠️  Skipping TDD for debug code
# Confirm: Debug code doesn't need tests (y/N): y
# ✓ Added console.log (remember to remove later!)
```

### Chained Micro Tasks (with test suite)
```bash
/micro-task "Fix button alignment" --chain
/mt "Update padding to p-4" --chain
/mt "Center text with text-center" --chain

# Generates combined test:
test('button has correct alignment and spacing', () => {
  render(<Button />);
  const button = screen.getByRole('button');
  
  expect(button).toHaveClass('p-4');
  expect(button).toHaveClass('text-center');
  expect(button).toHaveClass('mx-auto'); // centered
});
```

## Auto-Conversion

If a micro-task exceeds 5 minutes:
1. Automatically converts to regular task
2. Updates task tracking
3. Notifies about scope creep
4. Suggests breaking into smaller pieces

## Integration with Task System

```bash
# Current task context
/ts
> Feature: User Profile
> Current: Task 3 of 8 - "Add form validation"

# Add quick fix without disrupting flow
/mt "Fix email regex pattern"
> Micro-task completed in 2 min
> Continuing with Task 3...
```

## Best Practices

1. **Keep it atomic** - One change per micro-task
2. **Be specific** - "Change color" → "Change button color to blue-600"
3. **Skip ceremony** - No PRD needed for typos
4. **Trust the hooks** - Design validation still applies
5. **Document later** - Micro-tasks auto-document in session

## Micro Task Rules

- Max 5 minutes execution time
- **TESTS GENERATED AUTOMATICALLY**
- Single file changes preferred
- No architectural decisions
- No database migrations
- No breaking changes
- Coverage maintained above 80%

## Tracking

Micro-tasks are:
- Logged with test coverage metrics
- Included in TDD dashboard
- Summarized in handoff docs
- Not tracked as formal tasks
- **Test coverage reported**

## Micro-Test Templates

Common patterns auto-generated:

```typescript
// Text change
test('displays correct text', () => {
  expect(screen.getByText('new text')).toBeInTheDocument();
});

// Style change
test('applies correct styles', () => {
  expect(element).toHaveClass('expected-class');
});

// Prop addition
test('handles new prop', () => {
  render(<Component newProp={value} />);
  // assertion based on prop effect
});
```

## Why Micro-Tests Matter

1. **Prevent Regressions** - Even small changes can break things
2. **Document Intent** - Tests explain why the change was made
3. **Fast Feedback** - Know immediately if something breaks
4. **Compound Safety** - Many micro-changes = potential for bugs
5. **Zero Overhead** - Tests generated automatically

This ensures even the smallest changes are protected by tests!
