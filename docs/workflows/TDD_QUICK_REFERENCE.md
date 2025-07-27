# TDD Quick Reference Card

## 🚦 TDD Workflow Commands

### Start TDD for a Feature
```bash
/tdd-workflow user-profile      # Full TDD workflow
/prd-generate-tests auth        # Generate from PRD
/create-prp login-form          # Create PRP with tests
```

### Manual Test Commands
```bash
npm test                        # Run all tests
npm test UserProfile.test       # Run specific test
npm test -- --watch            # Watch mode
npm test -- --coverage         # Coverage report
```

## 🪝 Active TDD Hooks

| Hook | Trigger | Action |
|------|---------|--------|
| **TDD Enforcer** | Creating component without tests | Blocks & guides to tests |
| **Test Auto-Runner** | After code changes | Runs related tests |
| **TDD Suggester** | "create component" prompts | Suggests TDD workflow |

## 🔄 TDD Cycle

```
1. 🔴 RED     Write failing test
2. 🟢 GREEN   Write minimal code to pass
3. ♻️ REFACTOR Improve code, tests stay green
```

## 📝 Test Structure

```typescript
describe('Component', () => {
  // Arrange
  const setup = () => render(<Component />);
  
  it('should do something', () => {
    // Act
    const { getByRole } = setup();
    fireEvent.click(getByRole('button'));
    
    // Assert
    expect(getByRole('alert')).toBeInTheDocument();
  });
});
```

## 🎯 What to Test

### ✅ DO Test
- Component renders
- Props affect output
- User interactions
- State changes
- Error handling
- Edge cases
- Accessibility

### ❌ DON'T Test
- Implementation details
- Third-party libraries
- Styles/CSS
- Framework internals

## 🛠️ Configuration

### Disable TDD Temporarily
```json
// .claude/hooks/config.json
{
  "tdd": {
    "enabled": false
  }
}
```

### Change Enforcement Level
```json
{
  "tdd": {
    "enforcement_level": "warn"  // or "block"
  }
}
```

## 💡 Tips

1. **Start Simple**: One test, one feature
2. **Test Behavior**: Not implementation
3. **Clear Names**: Test name = requirement
4. **Fast Tests**: Mock external dependencies
5. **Trust Process**: Let tests guide design

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| Hook not triggering | Restart Claude Code |
| Tests not found | Check file naming `*.test.tsx` |
| Tests timing out | Increase timeout or simplify |
| Can't implement | Write tests first! |

## 📚 Resources

- `/tdd-workflow [feature]` - Start TDD
- `docs/workflow/TDD_WORKFLOW_GUIDE.md` - Full guide
- `templates/tests/` - Test templates
