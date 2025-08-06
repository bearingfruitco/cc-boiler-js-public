#!/usr/bin/env python3
"""
Security Validator Hook - Compliant with Official Claude Code Hook Specification
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
                'fix': 'Add rate limiting middleware to protect against abuse'
            })
    
    # Check for input validation
    if 'parse(' not in content and '.parse(' not in content:
        if 'await req.json()' in content or 'await request.json()' in content:
            issues.append({
                'type': 'missing_validation',
                'severity': 'high',
                'message': 'API route accepts JSON without validation',
                'fix': 'Use zod or similar to validate input data'
            })
    
    # Check for authentication
    if 'public' not in file_path.lower():
        if not any(auth in content for auth in ['withAuth', 'requireAuth', 'getServerSession', 'auth.uid()']):
            issues.append({
                'type': 'missing_auth',
                'severity': 'medium',
                'message': 'API route may need authentication',
                'fix': 'Add authentication middleware if this is a protected route'
            })
    
    return issues

def check_form_security(content, file_path):
    """Check forms for security issues"""
    issues = []
    
    # Check if this is a form component
    if '<form' not in content.lower() and 'useform' not in content.lower():
        return issues
    
    # Check for CSRF protection
    if 'csrf' not in content.lower() and 'csrftoken' not in content.lower():
        issues.append({
            'type': 'missing_csrf',
            'severity': 'medium',
            'message': 'Form may need CSRF protection',
            'fix': 'Add CSRF token to form submissions'
        })
    
    # Check for client-side validation
    if 'required' in content or 'validate' in content:
        if 'server' not in content.lower():
            issues.append({
                'type': 'client_only_validation',
                'severity': 'info',
                'message': 'Ensure server-side validation matches client-side',
                'fix': 'Always validate on the server, even with client validation'
            })
    
    return issues

def check_database_security(content, file_path):
    """Check for database security issues"""
    issues = []
    
    # Check for SQL injection risks
    if any(db in content for db in ['query(', 'execute(', 'raw(']):
        if '${' in content or 'f"' in content or "f'" in content:
            issues.append({
                'type': 'sql_injection_risk',
                'severity': 'critical',
                'message': 'Potential SQL injection - use parameterized queries',
                'fix': 'Use parameterized queries or an ORM to prevent SQL injection'
            })
    
    # Check for exposed credentials
    sensitive_patterns = ['password', 'secret', 'key', 'token', 'api_key']
    for pattern in sensitive_patterns:
        if f'"{pattern}":' in content.lower() or f"'{pattern}':" in content.lower():
            if 'process.env' not in content:
                issues.append({
                    'type': 'hardcoded_secrets',
                    'severity': 'critical',
                    'message': f'Possible hardcoded {pattern}',
                    'fix': 'Use environment variables for sensitive data'
                })
    
    return issues

def main():
    """Main hook function following official Claude Code hook specification."""
    try:
        # Read JSON input from stdin (as per official docs)
        input_data = json.loads(sys.stdin.read())
        
        # Extract fields according to official schema
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Only validate write operations
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            # Exit code 0 = success, continue
            sys.exit(0)
        
        # Get file content and path
        file_path = tool_input.get('file_path', '') or tool_input.get('path', '')
        content = tool_input.get('content', '') or tool_input.get('new_str', '')
        
        if not content:
            sys.exit(0)
        
        # Run security checks
        all_issues = []
        all_issues.extend(check_api_security(content, file_path))
        all_issues.extend(check_form_security(content, file_path))
        all_issues.extend(check_database_security(content, file_path))
        
        # Filter critical issues
        critical_issues = [i for i in all_issues if i['severity'] == 'critical']
        high_issues = [i for i in all_issues if i['severity'] == 'high']
        
        if critical_issues:
            # Exit code 2 = blocking error for critical issues
            error_msg = "🚨 CRITICAL SECURITY ISSUES:\n"
            for issue in critical_issues:
                error_msg += f"  - {issue['message']}\n"
                error_msg += f"    Fix: {issue['fix']}\n"
            
            print(error_msg, file=sys.stderr)
            sys.exit(2)
        elif high_issues:
            # Non-blocking warning for high issues
            warning_msg = "⚠️ Security warnings:\n"
            for issue in high_issues:
                warning_msg += f"  - {issue['message']}\n"
            
            print(warning_msg, file=sys.stderr)
            sys.exit(1)  # Non-blocking error
        else:
            # No critical issues - continue
            sys.exit(0)
    
    except Exception as e:
        # On error, log to stderr but continue (non-blocking)
        print(f"Security validator hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)  # Non-blocking error

if __name__ == "__main__":
    main()
