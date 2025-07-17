# PRP: [Task Name] - Focused Implementation Task

> **Task-Focused PRP for Single Responsibility Implementation**
> Use for micro-tasks that can be completed in 1-2 hours

## 🎯 Task Objective
[One sentence describing what needs to be done]

**Parent Feature**: [Link to parent PRP or issue]
**Estimated Time**: [15min | 30min | 1hr | 2hr]
**Complexity**: [Low | Medium | High]

## ✅ Success Criteria
- [ ] [Specific measurable outcome 1]
- [ ] [Specific measurable outcome 2]
- [ ] [Specific measurable outcome 3]

## 📋 Task Context

### Current State
```typescript
// What exists now
const currentImplementation = {
  // Show current code structure
};
```

### Desired State
```typescript
// What should exist after task
const desiredImplementation = {
  // Show target code structure
};
```

### Files to Modify
```yaml
- path: components/feature/Component.tsx
  changes: Add new prop interface
  
- path: lib/utils/helpers.ts
  changes: Create helper function
  
- path: types/index.ts
  changes: Export new types
```

## 🛠️ Implementation Steps

### Step 1: [First Action]
```typescript
// Example code for step 1
export function helperFunction(input: string): string {
  // Implementation
  return processedInput;
}
```

### Step 2: [Second Action]
```typescript
// Example code for step 2
interface ComponentProps {
  existingProp: string;
  newProp?: boolean; // Add this
}
```

### Step 3: [Third Action]
```typescript
// Example code for step 3
// Update component to use new prop
```

## 🧪 Verification Steps

### Quick Checks
```bash
# 1. Type checking passes
bun run typecheck

# 2. Lint passes
bun run lint

# 3. Component renders
# Visual check in browser
```

### Test Cases
```typescript
// Add to existing test file
it('handles new prop correctly', () => {
  render(<Component newProp={true} />);
  expect(screen.getByText('...')).toBeInTheDocument();
});
```

## ⚠️ Gotchas & Warnings

### Don't Forget
- Update types/index.ts exports
- Check mobile view (min touch target 44px)
- Use design system classes only
- Handle loading states for async

### Common Mistakes
- ❌ Adding non-grid spacing (p-5, m-7)
- ❌ Using forbidden font classes (text-sm, font-bold)
- ❌ Forgetting error boundaries
- ❌ Missing loading indicators

## 🔗 Dependencies

### Prerequisite Tasks
- [x] Parent component created
- [x] Types defined
- [x] API endpoint ready

### Blocks Other Tasks
- [ ] [Task that depends on this]
- [ ] [Another dependent task]

## 📊 Task Validation

### Definition of Done
- [ ] Code implemented and working
- [ ] Types added/updated
- [ ] Tests passing
- [ ] Design system compliant
- [ ] No console errors
- [ ] PR ready for review

### Self-Review Checklist
```bash
# Run before marking complete
/vd                  # Validate design
/typecheck          # Check types
/test Component     # Run tests
/lint-check         # Check formatting
```

## 💡 Quick Reference

### Relevant Patterns
```typescript
// Pattern from similar component
const ExistingPattern = () => {
  // Reference implementation
};
```

### Useful Commands
```bash
# Generate types from schema
/gft

# Check component dependencies
/deps check Component

# Validate before commit
/pp
```

---

**Time Check**: If this task is taking > 2 hours, break it down further or escalate blockers.
