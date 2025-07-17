# Lightweight PRP for Quick Features

A focused template for smaller features that need comprehensive context but less ceremony.
Perfect for single components, bug fixes, or minor enhancements.

## Goal
[One sentence: What needs to be built]

## Why
[One sentence: Business value]

## What
[Brief description and acceptance criteria]

### Success Criteria ✓
- [ ] [Specific outcome 1]
- [ ] [Specific outcome 2]
- [ ] [Specific outcome 3]

## Context Dump
### Copy These Patterns
```typescript
// From: components/ui/Button.tsx
// Pattern: How we structure interactive components
export function Button({ 
  children, 
  variant = 'primary',
  onClick,
  disabled,
  className = '' 
}: ButtonProps) {
  // Note: Always use design system classes
  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-800 text-white hover:bg-gray-900'
  };
  
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`h-12 px-4 rounded-xl font-semibold text-size-3 
        transition-all ${variants[variant]} ${className}`}
    >
      {children}
    </button>
  );
}
```

### Critical Gotchas ⚠️
```markdown
# DON'T: Use Tailwind's default sizes (text-sm, p-5)
# DO: Use our design system (text-size-3, p-4)

# DON'T: Block on analytics
# DO: Use eventQueue.emit() for fire-and-forget

# DON'T: Forget loading states
# DO: Every async operation needs user feedback
```

### Required Reading 📚
```yaml
- file: lib/utils/form-helpers.ts
  why: Standard validation approach

- url: https://nextjs.org/docs/app/building-your-application/rendering/server-components
  why: This component will be server-first
```

## Quick Implementation

### 1️⃣ Setup (2 min)
```bash
# Check if component exists first
/exists $COMPONENT_NAME

# Create with our generator
/cc ui $COMPONENT_NAME
```

### 2️⃣ Implementation (Follow patterns above)
- Copy the structure from similar components
- Use only approved design tokens
- Include proper TypeScript types
- Add loading states for async ops

### 3️⃣ Quick Validation
```bash
# Lint and type check
bun run lint:fix && bun run typecheck

# Visual check
/vd

# Quick test
bun test $COMPONENT_NAME
```

## Test Cases
### Minimum Required Tests
```typescript
describe('$COMPONENT_NAME', () => {
  it('renders without crashing', () => {
    render(<$COMPONENT_NAME />);
  });
  
  it('handles click events', async () => {
    const onClick = vi.fn();
    const { user } = render(<$COMPONENT_NAME onClick={onClick} />);
    await user.click(screen.getByRole('button'));
    expect(onClick).toHaveBeenCalled();
  });
  
  it('shows loading state', () => {
    render(<$COMPONENT_NAME loading />);
    expect(screen.getByTestId('loading')).toBeInTheDocument();
  });
});
```

## Checklist
- [ ] Component exists check (`/exists`)
- [ ] Design system compliance (`/vd`)
- [ ] Loading states for async
- [ ] Error states handled  
- [ ] Mobile responsive (min 44px touch)
- [ ] Tests passing
- [ ] No TypeScript errors

## Common Issues & Fixes

### Issue: "Unknown Tailwind class"
```bash
# You used: text-sm
# Fix: Use text-size-3 instead
```

### Issue: "No loading state"
```typescript
// Add this pattern:
if (isLoading) {
  return <LoadingSpinner />;
}
```

### Issue: "Touch target too small"
```bash
# Minimum height: h-11 (44px)
# Better: h-12 (48px)
```

---

**Quick Commands**:
```bash
/vd                  # Validate design
/exists Component    # Check before creating  
/test-runner         # Run tests
/grade              # Check implementation quality
```

Remember: This is for QUICK features. Use the full PRD template for complex features.
