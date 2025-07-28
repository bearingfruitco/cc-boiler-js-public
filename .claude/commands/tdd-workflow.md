# TDD Workflow Enhanced

Complete Test-Driven Development workflow with automated test generation and validation.

## Arguments: $ARGUMENTS

## Usage:
```bash
/tdd user-profile          # Start TDD for a feature
/tdd ContactForm --e2e     # Include E2E tests
/tdd api/auth --unit       # API endpoint with unit tests
```

## Workflow:

### 1. Check Prerequisites
```bash
# Find related PRP/PRD
echo "🔍 Checking for requirements..."

# Look for PRP
PRP_FILE=$(find PRPs/active -name "*$ARGUMENTS*.md" -o -name "*${ARGUMENTS//-/_}*.md" | head -1)

# Look for PRD
PRD_FILE=$(find . -name "*$ARGUMENTS*PRD.md" -o -name "*${ARGUMENTS//-/_}*prd.md" | head -1)

if [ -n "$PRP_FILE" ]; then
    echo "✅ Found PRP: $PRP_FILE"
    SOURCE="$PRP_FILE"
elif [ -n "$PRD_FILE" ]; then
    echo "✅ Found PRD: $PRD_FILE"
    SOURCE="$PRD_FILE"
else
    echo "⚠️  No PRP/PRD found. Creating basic test structure..."
    SOURCE=""
fi
```

### 2. Extract Test Requirements
If we have a PRP/PRD, extract test cases:

```bash
if [ -n "$SOURCE" ]; then
    echo ""
    echo "📋 Test Requirements:"
    echo ""
    
    # Extract success criteria
    grep -A 30 "Success Criteria\|✅\|Acceptance" "$SOURCE" | grep "^- " | while IFS= read -r line; do
        echo "  Test: $line"
    done
fi
```

### 3. Generate Test Structure
```bash
# Determine component path
COMPONENT_NAME=$(echo "$ARGUMENTS" | sed 's/-/_/g' | sed 's/\b\(.\)/\u\1/g')
COMPONENT_PATH="components/${COMPONENT_NAME}.tsx"
TEST_PATH="components/__tests__/${COMPONENT_NAME}.test.tsx"

echo ""
echo "📁 File Structure:"
echo "  Component: $COMPONENT_PATH"
echo "  Tests: $TEST_PATH"
```

### 4. Create Test File
Generate comprehensive test file based on requirements:

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ${COMPONENT_NAME} } from '../${COMPONENT_NAME}';

describe('${COMPONENT_NAME}', () => {
  const user = userEvent.setup();
  
  // 🔴 RED: Basic Rendering
  describe('Component Rendering', () => {
    it('should render without crashing', () => {
      render(<${COMPONENT_NAME} />);
      // Add specific element checks based on requirements
    });
    
    it('should display required elements', () => {
      render(<${COMPONENT_NAME} />);
      // Test for specific UI elements from PRD
    });
  });
  
  // 🔴 RED: Props and State
  describe('Props and State Management', () => {
    it('should handle required props correctly', () => {
      const props = {
        // Add required props from interface
      };
      render(<${COMPONENT_NAME} {...props} />);
    });
    
    it('should update state on user interaction', async () => {
      render(<${COMPONENT_NAME} />);
      // Test state changes
    });
  });
  
  // 🔴 RED: User Interactions
  describe('User Interactions', () => {
    it('should handle click events', async () => {
      const handleClick = jest.fn();
      render(<${COMPONENT_NAME} onClick={handleClick} />);
      
      await user.click(screen.getByRole('button'));
      expect(handleClick).toHaveBeenCalledTimes(1);
    });
    
    it('should validate form inputs', async () => {
      render(<${COMPONENT_NAME} />);
      // Test form validation
    });
  });
  
  // 🔴 RED: Business Logic
  describe('Business Requirements', () => {
    // Tests generated from PRD/PRP success criteria
    ${generateTestsFromCriteria(SOURCE)}
  });
  
  // 🔴 RED: Edge Cases
  describe('Edge Cases and Error Handling', () => {
    it('should handle empty data gracefully', () => {
      render(<${COMPONENT_NAME} data={[]} />);
      expect(screen.getByText(/no data/i)).toBeInTheDocument();
    });
    
    it('should show error state on failure', async () => {
      render(<${COMPONENT_NAME} />);
      // Test error scenarios
    });
  });
  
  // 🔴 RED: Accessibility
  describe('Accessibility', () => {
    it('should be keyboard navigable', async () => {
      render(<${COMPONENT_NAME} />);
      
      // Tab through interactive elements
      await user.tab();
      expect(screen.getByRole('button')).toHaveFocus();
    });
    
    it('should have proper ARIA labels', () => {
      render(<${COMPONENT_NAME} />);
      expect(screen.getByRole('button')).toHaveAccessibleName();
    });
  });
  
  // 🔴 RED: Performance
  describe('Performance', () => {
    it('should render quickly', () => {
      const start = performance.now();
      render(<${COMPONENT_NAME} />);
      const end = performance.now();
      
      expect(end - start).toBeLessThan(100);
    });
  });
});
```

### 5. Create Component Stub
Create minimal component that will fail tests:

```typescript
// ${COMPONENT_PATH}
export function ${COMPONENT_NAME}() {
  return null; // Start with failing implementation
}
```

### 6. Run Tests (RED Phase)
```bash
echo ""
echo "🔴 Running tests (RED phase)..."
npm test "$TEST_PATH" -- --run

echo ""
echo "✅ Tests are failing as expected!"
echo "   This confirms our test suite is working."
```

### 7. Set Up Test Watcher
```bash
echo ""
echo "👀 Setting up test watcher..."
echo ""
echo "Run in another terminal:"
echo "npm test $TEST_PATH -- --watch"
echo ""
echo "Tests will run automatically as you implement!"
```

### 8. Implementation Guide
```bash
echo ""
echo "📝 TDD Implementation Steps:"
echo ""
echo "1. 🔴 RED: Confirm tests are failing"
echo "2. 🟢 GREEN: Write minimal code to pass each test"
echo "3. ♻️  REFACTOR: Improve code while keeping tests green"
echo ""
echo "Work on one test at a time:"
echo "  - Make it pass with simplest solution"
echo "  - Refactor if needed"
echo "  - Move to next test"
echo ""
echo "Remember: Write ONLY enough code to pass the current test!"
```

### 9. Create Test Helpers
Generate helper functions for common test scenarios:

```typescript
// ${TEST_PATH}.helpers.ts
export const ${COMPONENT_NAME}TestHelpers = {
  renderWithProps: (props = {}) => {
    const defaultProps = {
      // Default test props
    };
    return render(<${COMPONENT_NAME} {...defaultProps} {...props} />);
  },
  
  mockData: () => ({
    // Mock data for tests
  }),
  
  setupUserInteraction: () => {
    return userEvent.setup();
  }
};
```

### 10. Coverage Check
```bash
echo ""
echo "📊 Coverage Requirements:"
echo "  - Statement coverage: > 80%"
echo "  - Branch coverage: > 75%"
echo "  - Function coverage: > 80%"
echo ""
echo "Run coverage: npm test -- --coverage $TEST_PATH"
```

## Integration with Hooks

The TDD workflow integrates with:

1. **Pre-Tool Hook**: `/19-tdd-enforcer.py`
   - Blocks implementation without tests
   - Suggests this workflow

2. **Post-Tool Hook**: `/06-test-auto-runner.py`
   - Runs tests after each save
   - Provides immediate feedback

3. **PRP Integration**:
   - Extracts test cases from success criteria
   - Links tests to requirements

## Benefits:

- 🎯 **Requirements-Driven**: Tests match PRD/PRP exactly
- 🔄 **Immediate Feedback**: Know when implementation is complete
- 🛡️ **Regression Prevention**: Changes can't break existing features
- 📚 **Living Documentation**: Tests show how to use component
- 🏗️ **Better Design**: TDD forces modular, testable code

## Tips:

1. **Start Simple**: One test at a time
2. **Baby Steps**: Smallest change to pass test
3. **Refactor Often**: Keep code clean
4. **Trust the Process**: Let tests guide design
5. **Document Intent**: Test names explain "why"

The TDD workflow ensures your implementation matches requirements perfectly!
