# dependency-scan

Scans project dependencies for security vulnerabilities.

## Usage
```bash
dependency-scan [options]
```

## Options
- `--production` - Only scan production dependencies
- `--fix` - Attempt to auto-fix vulnerabilities
- `--audit-level` - Minimum level to report: `low`, `moderate` (default), `high`, `critical`
- `--update` - Check for outdated packages too

## Examples
```bash
# Basic vulnerability scan
dependency-scan

# Production dependencies only
dependency-scan --production

# Auto-fix vulnerabilities
dependency-scan --fix

# Include all severity levels
dependency-scan --audit-level=low

# Full scan with updates
dependency-scan --update
```

## What it checks

### Vulnerability Scanning
- Known CVEs in dependencies
- Security advisories
- License compliance
- Deprecated packages

### Dependency Health
- Outdated major versions
- Unmaintained packages
- Missing types
- Circular dependencies

## Output Format
```
🔍 Dependency Security Scan
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Found 3 vulnerabilities (1 critical, 2 high)

CRITICAL: prototype-pollution in lodash@4.17.20
  → Fix available: Update to lodash@4.17.21
  
HIGH: RegEx DoS in ansi-regex@5.0.0
  → Fix available: Update to ansi-regex@5.0.1

📊 Summary:
- Total dependencies: 245
- Direct dependencies: 42
- Vulnerabilities: 3
- Outdated: 12
```

## Integration with CI/CD
Add to your workflow:
```yaml
- name: Security Scan
  run: |
    npm run security:scan
    if [ $? -ne 0 ]; then
      echo "Security vulnerabilities found!"
      exit 1
    fi
```

## Automatic Fixes
When using `--fix`:
1. Updates package versions
2. Runs tests to verify
3. Creates fix report
4. Updates lock file

## Best Practices
- Run weekly in development
- Run on every PR
- Block deployments on critical
- Review license changes
- Track security debt
