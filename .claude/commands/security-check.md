---
name: security-check
description: Run comprehensive security audit using the security-threat-analyst sub-agent
---

# Security Check Command

Delegates to the security-threat-analyst sub-agent for comprehensive security analysis.

## Usage
```
/security-check [focus-area]
```

## Focus Areas
- `all` - Complete security audit (default)
- `deps` - Dependency vulnerabilities
- `auth` - Authentication security
- `api` - API endpoint security
- `secrets` - Exposed secrets scan
- `code` - Code vulnerability analysis

## Examples
```bash
# Full security audit
/security-check

# Check dependencies only
/security-check deps

# Scan for exposed secrets
/security-check secrets

# Review authentication
/security-check auth
```

## Execution

use security-threat-analyst subagent to perform comprehensive security audit focusing on ${ARGUMENTS:-all aspects}. Please scan for vulnerabilities, check dependencies, review authentication patterns, validate API security, scan for exposed secrets, and provide a detailed security report with actionable recommendations.

## Integration with CI/CD

The security-threat-analyst will provide recommendations for:
- Pre-commit hooks
- CI/CD pipeline integration
- Automated security checks
- Vulnerability remediation

## Report Format

The agent will deliver:
1. Executive Summary
2. Critical Issues (if any)
3. Detailed Findings by Category
4. Risk Assessment
5. Remediation Steps
6. Compliance Checklist
7. Integration Recommendations

## Follow-up Actions

After the security audit:
- Review critical findings immediately
- Create tickets for remediation
- Update security documentation
- Schedule regular audits
