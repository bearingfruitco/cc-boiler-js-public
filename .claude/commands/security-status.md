# security-status

Shows comprehensive security status of the project.

## Usage
```bash
security-status [filter]
```

## Arguments
- `filter` - Optional: `api`, `forms`, `database`, `dependencies`, `summary`

## Examples
```bash
# Full security status
security-status

# API security only
security-status api

# Quick summary
security-status summary
```

## What it shows

### Security Dashboard
```
╔══════════════════════════════════════════════════════════╗
║                 🔒 Security Status                       ║
╠══════════════════════════════════════════════════════════╣
║ Overall Score: B+ (85/100)                               ║
╠══════════════════════════════════════════════════════════╣
║ APIs:                                                    ║
║ ✅ With rate limiting:        12/15 (80%)               ║
║ ✅ With authentication:       10/12 (83%)               ║
║ ⚠️  Missing validation:        3 endpoints              ║
╠══════════════════════════════════════════════════════════╣
║ Forms:                                                   ║
║ ✅ With CAPTCHA:              3/5 (60%)                 ║
║ ✅ With rate limiting:        5/5 (100%)                ║
║ ✅ With validation:           5/5 (100%)                ║
╠══════════════════════════════════════════════════════════╣
║ Database:                                                ║
║ ✅ Tables with RLS:           8/10 (80%)                ║
║ ⚠️  Missing policies:          users_audit, logs        ║
╠══════════════════════════════════════════════════════════╣
║ Dependencies:                                            ║
║ ✅ Last scan:                 2 days ago                ║
║ ⚠️  Vulnerabilities:          1 moderate               ║
║ ✅ Up to date:                95%                       ║
╠══════════════════════════════════════════════════════════╣
║ Recent Security Events (24h):                            ║
║ • Rate limit hits:            23                        ║
║ • Failed auth attempts:       2                         ║
║ • Validation failures:        5                         ║
║ • Suspicious activity:        0 ✅                      ║
╚══════════════════════════════════════════════════════════╝
```

### Detailed Reports

#### API Report
- List of all endpoints
- Security features per endpoint
- Missing protections
- Recommendations

#### Form Report
- Form inventory
- Security features
- Bot protection status
- Submission metrics

#### Database Report
- RLS coverage
- Policy effectiveness
- Access patterns
- Audit trail status

## Security Score Calculation
- Rate limiting: 25%
- Authentication: 20%
- Input validation: 20%
- RLS policies: 15%
- Dependencies: 10%
- Security headers: 10%

## Integration
- Updated by security hooks
- Shown in `/sr` summary
- Used by `/grade` scoring
- Tracked in metrics

## Actions
Based on status, suggests:
- `/es api` - Enhance API security
- `/rls users_audit` - Generate missing policies
- `/ds --fix` - Fix vulnerabilities
- `/sa` - Run full audit
