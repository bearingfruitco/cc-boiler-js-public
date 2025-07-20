# TDD Workflow Guide

## Overview

This project now includes automated Test-Driven Development (TDD) enforcement through Claude Code hooks.

## How It Works

### 1. Pre-Implementation Hook
When you try to create a component without tests, the TDD Enforcer will:
- Block the implementation
- Suggest creating tests first
- Provide test templates
- Link to relevant PRPs/PRDs

### 2. Test Auto-Runner
After you modify code, the Test Auto-Runner will:
- Find related test files
- Run them automatically
- Report failures immediately
- Ensure tests stay green

### 3. TDD Suggester
When you mention creating features, the suggester will:
- Recommend TDD workflow
- Provide command shortcuts
- Link to documentation

## Workflow

### Starting a New Feature

1. **Create/Find Requirements**
   ```bash
   /create-prp user-profile
   # or use existing PRD
   ```

2. **Generate Tests**
   ```bash
   /tdd-workflow user-profile
   # or
   /prd-generate-tests user-profile
   ```

3. **Run Tests (RED)**
   ```bash
   npm test UserProfile.test
   ```

4. **Implement Feature**
   ```bash
   /cc UserProfile
   # TDD hook will ensure tests exist
   ```

5. **Tests Pass (GREEN)**
   - Auto-runner reports success
   - Continue implementing

6. **Refactor (REFACTOR)**
   - Improve code
   - Tests ensure nothing breaks

## Configuration

### Enable/Disable TDD

In `.claude/hooks/config.json`:
```json
{
  "tdd": {
    "enabled": true,
    "enforcement_level": "warn",  // or "block"
    "auto_run_tests": true
  }
}
```

### Skip TDD (Emergency Only)

If you need to skip TDD temporarily:
1. Set enforcement_level to "warn"
2. Or disable specific hooks in config.json

## Best Practices

1. **Write One Test at a Time**
   - Focus on current behavior
   - Don't over-engineer

2. **Keep Tests Simple**
   - Test one thing per test
   - Clear test names
   - Minimal setup

3. **Let Tests Drive Design**
   - Hard to test = poor design
   - Refactor when tests are green

4. **Use Test Helpers**
   - Create reusable test utilities
   - Mock data factories
   - Common assertions

## Troubleshooting

### Tests Not Running
- Check test file naming: `*.test.tsx` or `*.spec.tsx`
- Verify test runner installed: `npm install -D vitest`

### Hook Not Triggering
- Restart Claude Code after changes
- Check hooks are in settings.json
- Verify Python 3 is available

### Tests Timing Out
- Increase timeout in config.json
- Simplify test setup
- Use test.skip for slow tests

## Benefits

- ✅ Requirements always met
- ✅ Instant feedback on changes  
- ✅ Safe refactoring
- ✅ Living documentation
- ✅ Better code design
