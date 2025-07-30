# Browser Context Management

Save, load, and share browser testing context across sessions and team members.

## Usage
```bash
/pw-context <action> [name] [options]

Actions:
  save     Save current browser state
  load     Load saved browser state
  list     Show available contexts
  share    Share context via GitHub gist
  clear    Clear saved contexts
```

## Examples

### Save Browser Context
```bash
# Save current testing state
/pw-context save auth-testing

# What gets saved:
- Current URL and navigation history
- Cookies and localStorage
- Test scenarios and results  
- Visual baselines
- Console error history
- Performance metrics
- Form data (sanitized)
```

### Load Browser Context
```bash
# Load previous context
/pw-context load auth-testing

# Restores:
- Browser state
- Test configurations
- Visual baselines
- Previous test results
```

### List Available Contexts
```bash
/pw-context list

Available contexts:
1. auth-testing (2 hours ago)
2. checkout-flow (yesterday)
3. mobile-testing (3 days ago)
4. visual-baseline-v2 (1 week ago)
```

### Share Context with Team
```bash
# Share via GitHub gist
/pw-context share auth-testing

Context shared:
📎 https://gist.github.com/xxx/yyy
Contains:
- Browser state
- Test scenarios
- Instructions

Team member can load with:
/pw-context load-gist https://gist.github.com/xxx/yyy
```

## Context Structure

Saved to `.claude/context/browser-state/[name]/`:

```
auth-testing/
├── state.json          # Browser state
├── cookies.json        # Cookies (encrypted)
├── storage.json        # localStorage data
├── scenarios.json      # Test scenarios
├── results.json        # Test results
├── baselines/          # Visual baselines
│   ├── login.png
│   └── dashboard.png
├── console-logs.json   # Console history
└── README.md           # Context description
```

## Advanced Usage

### Context Templates
```bash
# Save as template
/pw-context save-template e2e-standard

# Create from template
/pw-context from-template e2e-standard new-feature
```

### Selective Context
```bash
# Save only specific parts
/pw-context save visual-only --only visuals
/pw-context save cookies-only --only cookies
/pw-context save tests-only --only scenarios
```

### Context Diff
```bash
# Compare contexts
/pw-context diff auth-v1 auth-v2

Differences:
- New cookie: session_token
- Changed URL: /dashboard → /home
- New test: password-reset
```

## Integration with Testing

### Use in Test Flows
```typescript
// Load context before tests
await loadContext('auth-testing');

// Run tests with saved state
test('Dashboard access', async ({ page }) => {
  // Already logged in from context
  await page.goto('/dashboard');
  await expect(page).toHaveURL('/dashboard');
});
```

### CI/CD Integration
```yaml
# .github/workflows/e2e.yml
- name: Load test context
  run: |
    claude pw-context load ci-baseline
    
- name: Run tests
  run: |
    claude pw-test all
    
- name: Save updated context
  run: |
    claude pw-context save ci-baseline
```

## Security Considerations

### Sensitive Data
- Passwords are NEVER saved
- Tokens are encrypted
- PII is automatically redacted
- Contexts are gitignored by default

### Sharing Safety
```bash
# Before sharing, sanitize
/pw-context sanitize auth-testing

Sanitization:
✓ Removed auth tokens
✓ Redacted email addresses  
✓ Cleared form passwords
✓ Anonymized user data
```

## Team Workflows

### Handoff Scenario
```bash
# Developer A (morning)
/pw-context save morning-work
"Fixed login flow, tested checkout"

# Developer B (afternoon)  
/pw-context load morning-work
# Continues exactly where A left off
```

### Bug Reproduction
```bash
# QA saves bug state
/pw-context save bug-1234

# Developer loads and debugs
/pw-context load bug-1234
/pw-debug "reproduce issue"
```

### Visual Regression Updates
```bash
# Designer approves new visuals
/pw-context save approved-visuals

# CI uses approved baselines
/pw-context load approved-visuals
/chain visual-regression-check
```

## Maintenance

### Clean Old Contexts
```bash
# Remove contexts older than 30 days
/pw-context clean --older-than 30d

# Remove all except tagged
/pw-context clean --except-tagged
```

### Export/Import
```bash
# Export for backup
/pw-context export all > contexts-backup.tar.gz

# Import after system reset
/pw-context import contexts-backup.tar.gz
```

## Best Practices

1. **Name contexts clearly**: `feature-state`, `bug-reproduction`
2. **Tag important contexts**: `baseline`, `approved`
3. **Sanitize before sharing**: Remove sensitive data
4. **Document context purpose**: Add README to context
5. **Regular cleanup**: Remove old contexts

Context management ensures consistent browser testing! 💾🌐
