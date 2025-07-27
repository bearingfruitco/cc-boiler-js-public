---
name: create-tests
description: Generate comprehensive test suites using TDD principles with qa-test-engineer and tdd-engineer sub-agents
---

# Create Tests Command

Uses the qa-test-engineer and tdd-engineer sub-agents to generate comprehensive test suites following TDD principles.

## Usage
```
/create-tests [feature-or-file] [options]
```

## Arguments
- `feature-or-file`: Feature name, component path, or PRD reference
- `options`: 
  - `--type`: unit|integration|e2e|all (default: all)
  - `--framework`: vitest|jest|playwright
  - `--coverage`: target percentage (default: 80)

## Examples
```bash
# Create tests for a feature
/create-tests authentication

# Create tests for a specific component
/create-tests components/UserProfile.tsx

# Create only unit tests
/create-tests checkout --type=unit

# Create E2E tests with Playwright
/create-tests user-journey --type=e2e --framework=playwright
```

## Workflow
1. **qa-test-engineer** analyzes requirements and generates test structure
2. **tdd-engineer** implements tests following TDD workflow
3. Tests created before implementation (red-green-refactor)

## Execution

First, use qa-test-engineer subagent to analyze ${ARGUMENTS:-the feature} and generate a comprehensive test plan including test structure, scenarios, edge cases, and acceptance criteria mapping.

Then, use tdd-engineer subagent to implement the test suite following TDD principles - write failing tests first, ensure they fail correctly, then guide implementation to make them pass.

The qa-test-engineer should focus on:
- Extracting testable requirements
- Identifying all test scenarios
- Creating test structure and organization
- Mapping tests to acceptance criteria
- Defining edge cases and error scenarios

The tdd-engineer should focus on:
- Writing actual test implementations
- Following red-green-refactor cycle
- Ensuring tests fail appropriately first
- Creating minimal passing implementations
- Refactoring while maintaining green tests
- Achieving coverage targets

## Test Structure Generated

```
__tests__/
├── unit/
│   ├── components/
│   │   └── UserProfile.test.tsx
│   └── utils/
│       └── validation.test.ts
├── integration/
│   ├── api/
│   │   └── auth.test.ts
│   └── services/
│       └── userService.test.ts
└── e2e/
    ├── auth-flow.spec.ts
    └── user-journey.spec.ts
```

## Output Format

The agents will provide:
1. **Test Plan** (from qa-test-engineer)
   - Test scenarios mapped to requirements
   - Test structure and organization
   - Coverage strategy

2. **Test Implementation** (from tdd-engineer)
   - Failing tests (red phase)
   - Implementation guidance
   - Passing tests (green phase)
   - Refactoring suggestions

3. **Coverage Report**
   - Current coverage percentage
   - Uncovered scenarios
   - Recommendations for improvement

## Integration Points

- Works with `/prd-generate-tests` for PRD-driven testing
- Integrates with `/test-runner` for execution
- Links to `/security-check` for security test scenarios
- Connects with `/performance-test` for load testing

## Best Practices Enforced

1. **Test First**: Always write tests before implementation
2. **Single Assertion**: One concept per test
3. **Descriptive Names**: Clear test descriptions
4. **Fast Execution**: Optimize for speed
5. **Isolation**: No test interdependencies
6. **Deterministic**: Same result every run
