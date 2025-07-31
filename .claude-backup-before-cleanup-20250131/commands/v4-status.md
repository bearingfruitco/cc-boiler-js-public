# /v4-status

Show the status of all v4.0 automation features and their current enforcement state.

## Usage
```
/v4-status
```

## What This Shows

### 1. Enforcement Status
- 🔒 **Security-First**: API creation requires security rules
- 📊 **Performance Budgets**: Real-time monitoring and enforcement
- 📚 **Documentation-First**: Auto-generated docs for components/APIs
- ♿ **Accessibility-First**: WCAG compliance enforcement

### 2. Hook Status
Shows which v4.0 hooks are currently active:
- `17-performance-budget-enforcer.py`
- `18-security-first-enforcer.py`
- `19-auto-rls-generator.py`
- `21-docs-first-enforcer.py`
- `22-api-docs-generator.py`
- `23-a11y-enforcer.py`
- `01-auto-error-recovery.py`

### 3. Knowledge Base Stats
- Error patterns learned
- Successful auto-fixes
- Fix success rate

### 4. Performance Metrics
- Current performance scores
- Budget compliance
- Baseline comparisons

### 5. Security Coverage
- APIs with RLS policies
- Security test coverage
- Threat models generated

### 6. Documentation Coverage
- Components documented
- APIs with OpenAPI specs
- Storybook stories

### 7. Accessibility Scores
- Average a11y score
- Components tested
- WCAG compliance level

## Example Output
```
🚀 V4.0 Automation Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 Enforcement Status:
  ✅ Security-First: ENABLED
  ✅ Performance Budgets: ENABLED
  ✅ Documentation-First: ENABLED
  ✅ Accessibility-First: ENABLED

🪝 Active Hooks: 7/7
  ✅ All v4.0 hooks operational

🧠 Error Knowledge Base:
  • Patterns: 45
  • Auto-fixes: 127
  • Success rate: 87%

📊 Performance:
  • Bundle size: 342KB / 500KB ✅
  • Avg render: 28ms / 50ms ✅
  • API response: 89ms / 200ms ✅

🔒 Security Coverage:
  • APIs with RLS: 12/12 (100%)
  • Security tests: 48 passing
  • Threat models: 8 generated

📚 Documentation:
  • Components: 24/26 (92%)
  • APIs: 12/12 (100%)
  • Storybook: 22 stories

♿ Accessibility:
  • Average score: 97/100
  • Tested components: 24/26
  • WCAG Level: AA compliant

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Run /chain-v4 full-stack-feature-v4 to use all features
```

## Configuration Files

The status is read from:
- `.claude/performance-budgets.json` - Performance settings
- `.claude/a11y-config.json` - Accessibility settings
- `.claude/error-knowledge-base.json` - Error patterns
- `.claude/security/` - Security configurations
- `.claude/api-docs/openapi/` - API documentation

## Toggle Features

To enable/disable specific features:
```
/enforce-security on|off
/enforce-performance on|off
/enforce-docs on|off
/enforce-a11y on|off
```

## Related Commands
- `/chain-v4` - Run v4.0 automation chains
- `/performance-monitor` - Performance details
- `/error-kb` - Error knowledge base
- `/security-matrix` - Security permissions
