# security-audit

Runs a comprehensive security audit of the project.

## Usage
```bash
security-audit [target]
```

## Arguments
- `target` - What to audit: `all` (default), `api`, `forms`, `database`, `dependencies`

## Examples
```bash
# Full security audit
security-audit

# Audit only APIs
security-audit api

# Audit forms
security-audit forms

# Check dependencies
security-audit dependencies
```

## What it checks

### API Security
- Rate limiting implementation
- Input validation
- Authentication requirements
- CORS configuration
- Security headers

### Form Security
- CAPTCHA implementation
- CSRF protection
- Rate limiting
- Input sanitization
- Honeypot fields

### Database Security
- RLS policies exist
- No exposed service keys
- Parameterized queries
- Soft delete support

### Dependencies
- Known vulnerabilities
- Outdated packages
- License compliance
- Supply chain risks

## Output
Generates a `SECURITY_AUDIT_REPORT.md` with:
- Executive summary
- Critical issues (must fix)
- High priority issues
- Medium priority suggestions
- Security score (0-100)

## Integration
This command is automatically run:
- Before major deployments
- In CI/CD pipeline
- Weekly via cron job
