# PRP: [Feature Name] - Test-Driven Development Template

## 🎯 Goal
[Clear description of what we're building]

## ✅ Success Criteria (Test Requirements)
These will become our test cases:

- [ ] Component renders without errors
- [ ] [Specific user interaction works]
- [ ] [Business logic requirement met]
- [ ] [Edge case handled]
- [ ] [Error state properly displayed]
- [ ] Accessibility: keyboard navigation works
- [ ] Performance: renders in < 100ms

## 🧪 Test Strategy

### Unit Tests
```typescript
describe('ComponentName', () => {
  it('should render with required props', () => {
    // Test basic rendering
  });
  
  it('should handle user interaction', () => {
    // Test specific interaction from success criteria
  });
});
```

### Integration Tests
```typescript
describe('Feature Integration', () => {
  it('should work with API', () => {
    // Test API integration
  });
});
```

### E2E Tests (if applicable)
```typescript
test('user can complete flow', async ({ page }) => {
  // Test complete user journey
});
```

## 📚 Required Context
[Documentation and patterns needed]

## 🏗️ Implementation Blueprint
[Step-by-step implementation guide]

## 🔄 TDD Workflow

1. **Generate Tests** ✅
   ```bash
   /prd-generate-tests this-feature
   ```

2. **Run Tests (RED)** 🔴
   ```bash
   npm test ComponentName.test.tsx
   ```

3. **Implement Feature** 💻
   - Follow implementation blueprint
   - Run tests continuously

4. **Tests Pass (GREEN)** 🟢
   ```bash
   npm test ComponentName.test.tsx
   ```

5. **Refactor (REFACTOR)** ♻️
   - Improve code while keeping tests green

## 🧪 Validation Loops

### Level 0: Tests First ✓
```bash
npm test
```

### Level 1: Syntax & Standards ✓
```bash
bun run lint && bun run typecheck
```

[Rest of validation levels...]
