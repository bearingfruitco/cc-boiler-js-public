# TDD Workflow

Execute Test-Driven Development workflow for a feature.

## Arguments: $ARGUMENTS

## Workflow Steps:

### 1. Generate Tests from PRP/PRD
```bash
# Check for existing PRP
PRP_FILE=$(find PRPs/active -name "*$ARGUMENTS*.md" | head -1)

if [ -z "$PRP_FILE" ]; then
  echo "❌ No PRP found for: $ARGUMENTS"
  echo "   Create PRP first: /create-prp $ARGUMENTS"
  exit 1
fi

echo "📋 Found PRP: $PRP_FILE"
```

### 2. Extract Test Requirements
```bash
echo "🧪 Extracting test requirements..."

# Extract success criteria from PRP
grep -A 20 "Success Criteria\|✅" "$PRP_FILE" | grep "^- " | while read -r line; do
  echo "  Test: $line"
done
```

### 3. Generate Test File
```bash
COMPONENT_NAME=$(echo "$ARGUMENTS" | sed 's/-/_/g' | awk '{print toupper(substr($0,1,1))substr($0,2)}')
TEST_FILE="components/__tests__/${COMPONENT_NAME}.test.tsx"

echo "📝 Generating test file: $TEST_FILE"
```

### 4. Create Test Template
```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ${COMPONENT_NAME} } from '../${COMPONENT_NAME}';

describe('${COMPONENT_NAME}', () => {
  // Rendering tests
  it('should render without errors', () => {
    render(<${COMPONENT_NAME} />);
    expect(screen.getByRole('...')).toBeInTheDocument();
  });

  // Interaction tests
  it('should handle user interaction', async () => {
    render(<${COMPONENT_NAME} />);
    
    const button = screen.getByRole('button');
    fireEvent.click(button);
    
    await waitFor(() => {
      expect(screen.getByText('...')).toBeInTheDocument();
    });
  });

  // Business logic tests
  it('should meet business requirement X', () => {
    // Test specific requirement from PRP
  });

  // Edge cases
  it('should handle edge case Y', () => {
    // Test edge case
  });

  // Error states
  it('should display error when Z', () => {
    // Test error handling
  });

  // Accessibility
  it('should be keyboard navigable', () => {
    // Test keyboard navigation
  });

  // Performance
  it('should render quickly', () => {
    const start = performance.now();
    render(<${COMPONENT_NAME} />);
    const end = performance.now();
    
    expect(end - start).toBeLessThan(100);
  });
});
```

### 5. Run Tests (Should Fail)
```bash
echo "🔴 Running tests (expecting failure)..."
npm test "$TEST_FILE" -- --run

echo "✅ Tests failing as expected (RED phase)"
echo "   Now implement the component to make tests pass"
```

### 6. Set Up Test Watcher
```bash
echo "👀 Starting test watcher..."
echo "   Tests will run automatically as you code"
echo ""
echo "   Run in another terminal:"
echo "   npm test $TEST_FILE -- --watch"
```

### 7. Implementation Checklist
```bash
echo ""
echo "📋 TDD Implementation Checklist:"
echo "   1. ❌ Tests are RED (failing)"
echo "   2. 💻 Write minimal code to pass tests"
echo "   3. 🟢 Tests turn GREEN (passing)"
echo "   4. ♻️  Refactor while keeping tests GREEN"
echo "   5. 🔄 Repeat for each test case"
```

## Benefits:

1. **Specification Compliance**: Tests enforce PRD/PRP requirements
2. **Confidence**: Know immediately when something breaks
3. **Documentation**: Tests document expected behavior
4. **Design Feedback**: Hard-to-test code = poor design
5. **Refactoring Safety**: Change implementation freely

## Tips:

- Write one test at a time
- Only write enough code to pass the current test
- Refactor only when tests are green
- Keep test watcher running while coding
