# test-requirements

Generate tests that verify locked requirements are maintained.

## Usage
```
/test-requirements [Component]
/tr-gen ContactForm
/test-req --all  # Generate for all components with locked requirements
```

## What It Does

1. **Reads Locked Requirements** - Loads requirement specifications
2. **Generates Test Cases** - Creates tests for each requirement
3. **Adds to Test Suite** - Integrates with existing tests
4. **Ensures Regression Prevention** - Tests fail if requirements violated

## Example Output

```typescript
// Generated: ContactForm.requirements.test.tsx

import { render, screen } from '@testing-library/react';
import { ContactForm } from '@/components/forms/ContactForm';

describe('ContactForm Requirement Compliance (Issue #42)', () => {
  // Requirement: Exactly 13 fields
  it('should have exactly 13 form fields as specified in Issue #42', () => {
    render(<ContactForm />);
    
    const inputs = screen.getAllByRole('textbox');
    const selects = screen.getAllByRole('combobox');
    const totalFields = inputs.length + selects.length;
    
    expect(totalFields).toBe(13);
  });
  
  // Requirement: All specified fields must exist
  it('should include all required fields from Issue #42', () => {
    render(<ContactForm />);
    
    const requiredFields = [
      'firstName', 'lastName', 'email', 'phone',
      'company', 'address', 'city', 'state', 
      'zip', 'country', 'message', 'source', 'consent'
    ];
    
    requiredFields.forEach(fieldName => {
      const field = screen.getByTestId(`field-${fieldName}`);
      expect(field).toBeInTheDocument();
    });
  });
  
  // Requirement: Email validation
  it('should validate corporate email domains', async () => {
    render(<ContactForm />);
    
    const emailInput = screen.getByLabelText('Email');
    const submitButton = screen.getByRole('button', { name: /submit/i });
    
    // Test invalid domain
    await userEvent.type(emailInput, 'user@gmail.com');
    await userEvent.click(submitButton);
    
    expect(screen.getByText(/corporate email required/i)).toBeInTheDocument();
  });
  
  // Requirement: All fields except company are required
  it('should enforce required fields except company', async () => {
    render(<ContactForm />);
    
    const submitButton = screen.getByRole('button', { name: /submit/i });
    await userEvent.click(submitButton);
    
    // Should show 12 error messages (all except company)
    const errors = screen.getAllByRole('alert');
    expect(errors).toHaveLength(12);
    
    // Company field should not show error
    expect(screen.queryByText(/company is required/i)).not.toBeInTheDocument();
  });
});

// E2E Requirement Tests
describe('ContactForm E2E Requirements (Issue #42)', () => {
  it('should successfully submit with all 13 fields filled', async () => {
    // Test implementation
  });
  
  it('should persist form data on validation errors', async () => {
    // Test implementation
  });
});
```

## Test Categories

### 1. Structure Tests
- Field count verification
- Field name validation
- Component hierarchy
- Layout requirements

### 2. Behavior Tests
- Validation rules
- Error handling
- Submit functionality
- Data persistence

### 3. Integration Tests
- API submission
- Response handling
- Error recovery
- Success flows

### 4. Accessibility Tests
- ARIA labels
- Keyboard navigation
- Screen reader support
- Focus management

## Generation Options

### Basic Generation
```bash
/test-requirements ContactForm
```

### With E2E Tests
```bash
/test-requirements ContactForm --e2e
```

### With Visual Regression
```bash
/test-requirements ContactForm --visual
```

### Update Existing Tests
```bash
/test-requirements ContactForm --update
```

## Test Execution

Generated tests run with your test suite:

```bash
# Run requirement tests only
pnpm test ContactForm.requirements

# Run all tests including requirements
pnpm test
```

## Continuous Monitoring

```json
// package.json
{
  "scripts": {
    "test:requirements": "vitest run **/*.requirements.test.*",
    "test:watch:requirements": "vitest watch **/*.requirements.test.*"
  }
}
```

## Best Practices

1. **Run After Changes** - Always run requirement tests after modifications
2. **Keep Updated** - Regenerate when requirements change
3. **Don't Skip** - Never skip requirement tests
4. **Add Custom Tests** - Extend generated tests with specific cases

## Integration with CI

```yaml
# GitHub Actions
- name: Run Requirement Tests
  run: pnpm test:requirements
  
- name: Upload Coverage
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: requirement-coverage
    path: coverage/requirements/
```

## Customization

Add custom test templates in `.claude/templates/tests/`:

```typescript
// .claude/templates/tests/requirement-test.hbs
describe('{{component}} Requirements ({{source}})', () => {
  {{#each requirements}}
  it('should {{description}}', () => {
    // {{testImplementation}}
  });
  {{/each}}
});
```
