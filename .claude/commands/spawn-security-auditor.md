# spawn-security-auditor

Spawns the Security Auditor sub-agent to perform security analysis.

## Usage
```bash
spawn-security-auditor [options]
```

## Options
- `--scope <scope>` - What to audit: `full` (default), `apis`, `forms`, `database`, `dependencies`
- `--quick` - Run quick security check only
- `--fix` - Attempt to auto-fix simple issues
- `--report` - Generate detailed report

## Examples
```bash
# Full security audit
spawn-security-auditor

# Quick API security check
spawn-security-auditor --scope apis --quick

# Audit with auto-fix
spawn-security-auditor --fix

# Generate detailed report
spawn-security-auditor --report
```

## What the Security Auditor Does

### Full Audit Mode
1. Scans all API routes for security issues
2. Checks forms for CAPTCHA and validation
3. Verifies RLS policies on database tables
4. Runs dependency vulnerability scan
5. Checks for exposed secrets
6. Generates security score and report

### Quick Check Mode
- Focuses on recently changed files
- Basic security validation
- Returns immediate results

### Auto-Fix Mode
- Adds missing rate limiting
- Generates basic validation schemas
- Adds security headers
- Creates RLS policy templates

## Output
The auditor returns:
- Security score (0-100)
- List of issues by severity
- Specific recommendations
- Auto-fix commands if available

## Integration
Works seamlessly with:
- `/security-audit` - Wrapper command
- `/enhance-security` - Apply fixes
- `/grade` - Includes security in grading

## Sub-Agent Context
The Security Auditor receives:
- Current file paths
- Project configuration
- Security requirements from PRD
- Previous audit results

And returns:
- Structured findings
- Actionable recommendations
- Generated code fixes
- Updated security metrics
