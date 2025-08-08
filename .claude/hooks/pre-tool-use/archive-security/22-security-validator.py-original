#!/usr/bin/env python3
"""
Security Validator Hook
Validates security requirements in API routes and forms
"""

import json
import sys
import re

def check_api_security(content, file_path):
    """Check API routes for security requirements"""
    issues = []
    
    # Check if this is an API route
    if '/api/' not in file_path or not file_path.endswith('.ts'):
        return issues
    
    # Check for rate limiting
    if 'rateLimit' not in content and 'rateLimiter' not in content:
        if any(method in content for method in ['POST', 'PUT', 'DELETE', 'PATCH']):
            issues.append({
                'type': 'missing_rate_limit',
                'severity': 'high',
                'message': 'API route missing rate limiting',
                'fix': 'import { rateLimit } from "@/lib/security/middleware";\n\nexport const POST = rateLimit(async (req) => { ... });'
            })
    
    # Check for input validation
    if 'parse(' not in content and '.parse(' not in content:
        if 'await req.json()' in content or 'await request.json()' in content:
            issues.append({
                'type': 'missing_validation',
                'severity': 'high',
                'message': 'API route accepts JSON without validation',
                'fix': 'import { z } from "zod";\nconst schema = z.object({ ... });\nconst data = schema.parse(await req.json());'
            })
    
    # Check for authentication
    if 'public' not in file_path.lower():
        if not any(auth in content for auth in ['withAuth', 'requireAuth', 'getServerSession', 'auth.uid()']):
            issues.append({
                'type': 'missing_auth',
                'severity': 'medium',
                'message': 'API route may need authentication',
                'fix': 'import { withAuth } from "@/lib/auth";\n\nexport const GET = withAuth(async (req) => { ... });'
            })
    
    return issues

def check_form_security(content, file_path):
    """Check forms for security requirements"""
    issues = []
    
    # Check if this is a form component
    if not any(indicator in content.lower() for indicator in ['form', 'submit', '<form']):
        return issues
    
    # Check for CSRF protection (Next.js has built-in, but check for custom implementations)
    if 'fetch(' in content and 'POST' in content:
        if 'csrf' not in content.lower() and 'x-csrf-token' not in content.lower():
            issues.append({
                'type': 'csrf_consideration',
                'severity': 'info',
                'message': 'Ensure CSRF protection is enabled (Next.js provides this by default)',
                'fix': 'Next.js App Router provides CSRF protection automatically'
            })
    
    # Check for rate limiting on form submission
    if 'onSubmit' in content or 'handleSubmit' in content:
        if 'rateLimit' not in content and 'useRateLimit' not in content:
            issues.append({
                'type': 'form_rate_limit',
                'severity': 'medium',
                'message': 'Consider rate limiting form submissions',
                'fix': 'import { useRateLimit } from "@/hooks/useRateLimit";\nconst { checkLimit } = useRateLimit("form-name");'
            })
    
    return issues

def check_database_security(content, file_path):
    """Check database queries for security issues"""
    issues = []
    
    # Check for raw SQL concatenation
    if any(db in content for db in ['supabase', 'postgres', 'sql']):
        # Look for string concatenation in SQL
        if re.search(r'(INSERT|UPDATE|DELETE|SELECT).*\+.*[\'"]', content):
            issues.append({
                'type': 'sql_injection_risk',
                'severity': 'critical',
                'message': 'Potential SQL injection via string concatenation',
                'fix': 'Use parameterized queries or query builders'
            })
    
    # Check for missing RLS mentions in Supabase queries
    if 'supabase' in content and any(method in content for method in ['.from(', '.select(', '.insert(', '.update(', '.delete(']):
        if 'service_role' not in content and 'rls' not in content.lower():
            issues.append({
                'type': 'rls_reminder',
                'severity': 'info',
                'message': 'Ensure RLS policies are configured for this table',
                'fix': 'Add RLS policies in Supabase dashboard or migration files'
            })
    
    return issues

def main():
    """Main hook entry point following Claude Code hook specification."""
    try:
        # Read input from Claude Code
        event = json.loads(sys.stdin.read())
        
        # Extract tool name and input
        tool_name = event.get('tool_name', '')
        tool_input = event.get('tool_input', {})
        
        # Only validate file writes
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            # Not a write operation - continue normally
            sys.exit(0)
        
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        content = tool_input.get('content', tool_input.get('new_str', ''))
        
        # Run security checks
        all_issues = []
        all_issues.extend(check_api_security(content, file_path))
        all_issues.extend(check_form_security(content, file_path))
        all_issues.extend(check_database_security(content, file_path))
        
        # If there are critical issues, warn but don't block
        if any(issue['severity'] == 'critical' for issue in all_issues):
            critical = [i for i in all_issues if i['severity'] == 'critical']
            message = "🚨 CRITICAL Security Issues:\n"
            for issue in critical:
                message += f"- {issue['message']}\n  Fix: {issue['fix']}\n"
            
            # Output warning to stderr
            print(message, file=sys.stderr)
        
        # If there are high/medium issues, provide suggestions
        elif all_issues:
            message = "🔒 Security Suggestions:\n"
            for issue in sorted(all_issues, key=lambda x: ['info', 'medium', 'high'].index(x['severity'])):
                icon = {'high': '⚠️', 'medium': '💡', 'info': 'ℹ️'}[issue['severity']]
                message += f"{icon} {issue['message']}\n"
            
            # Output suggestions to stderr
            print(message, file=sys.stderr)
        
        # Always continue normally (this is a warning hook)
        sys.exit(0)
        
    except Exception as e:
        # On error, log to stderr and exit with error code
        print(f"Security validator hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
