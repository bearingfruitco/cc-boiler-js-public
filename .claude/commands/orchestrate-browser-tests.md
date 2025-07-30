# Orchestrate Browser Testing Suite

Coordinate multiple agents to perform comprehensive browser testing.

## Usage
```bash
/orchestrate browser-test-suite [scope]

Scope:
- component [name] - Test specific component
- feature [name] - Test entire feature
- critical-paths - Test core user flows
- full - Complete browser test suite
```

## What happens:

### 1. Planning Phase
The PM orchestrator analyzes what needs testing and assigns specialists:
- playwright-specialist: Browser testing
- qa-test-engineer: Test scenarios
- performance-optimizer: Performance metrics
- ui-systems: Visual validation

### 2. Execution Phase

#### Component Testing
```yaml
playwright-specialist:
  - Launch component in isolation
  - Check rendering
  - Test interactions
  - Verify console logs
  
ui-systems:
  - Validate design compliance
  - Check responsive behavior
  - Verify animations
  
qa-test-engineer:
  - Edge case testing
  - Error state validation
  - Integration scenarios
```

#### Feature Testing
```yaml
Full user flow testing:
1. Navigation paths
2. Form submissions
3. Data operations
4. Error handling
5. Success states
```

#### Critical Path Testing
```yaml
Essential user journeys:
- Authentication flow
- Checkout process
- Data creation/editing
- Search functionality
```

### 3. Reporting Phase

Consolidated report includes:
- Console errors found
- Visual regressions
- Performance metrics
- Accessibility issues
- Failed interactions
- Screenshots/videos

## Example Orchestration

```bash
# Test new Button component
/orchestrate browser-test-suite component Button

# Output:
Starting browser test orchestration...

Phase 1: Planning
- playwright-specialist: Assigned browser testing
- ui-systems: Assigned visual validation
- qa-test-engineer: Assigned scenario testing

Phase 2: Execution
[playwright] ✓ Component renders
[playwright] ✓ No console errors
[playwright] ✓ Click handler works
[ui-systems] ✓ Design tokens correct
[ui-systems] ⚠ Hover state missing
[qa] ✓ Disabled state works
[qa] ✓ Loading state works

Phase 3: Report
- Total tests: 7
- Passed: 6
- Warnings: 1
- Time: 4.2s
```

## Integration with CI/CD

```yaml
# .github/workflows/browser-tests.yml
- name: Browser Test Suite
  run: |
    claude orchestrate browser-test-suite critical-paths
    claude pw-screenshot --full-page
```

## Parallel Execution

For faster testing, agents work in parallel:
- playwright-specialist: Core functionality
- performance-optimizer: Metrics collection
- ui-systems: Visual regression
- qa-test-engineer: Edge cases

## Success Criteria

All tests must pass:
- Zero console errors
- All interactions work
- Design compliance 100%
- Accessibility score > 90
- Performance budgets met

This orchestration ensures nothing ships with browser issues! 🚀
