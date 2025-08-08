#!/usr/bin/env python3
"""
Security Validator Hook - Check for common security issues
Follows official Claude Code hooks specification
"""

import json
import sys
import re

def check_security_issues(file_path, content):
    """Check for common security vulnerabilities"""
    violations = []
    
    # Skip non-code files
    code_extensions = ['.ts', '.tsx', '.js', '.jsx', '.py', '.go', '.java']
    if not any(file_path.endswith(ext) for ext in code_extensions):
        return []
    
    # 1. Check for unvalidated input in API routes
    if '/api/' in file_path or 'route.ts' in file_path:
        # Look for direct JSON parsing without validation
        if 'await req.json()' in content or 'await request.json()' in content:
            if not any(word in content for word in ['parse', 'validate', 'schema', 'zod', 'yup']):
                line_num = content.find('await req.json()') 
                if line_num == -1:
                    line_num = content.find('await request.json()')
                line_num = content[:line_num].count('\n') + 1 if line_num != -1 else 0
                violations.append(f"Line {line_num}: Unvalidated user input in API route. Use zod or another validator")
    
    # 2. Check for SQL injection vulnerabilities
    sql_patterns = [
        r'query\([^)]*\$\{[^}]+\}',  # Template literal in query
        r'query\([^)]*\+[^)]*\)',     # String concatenation in query
        r'WHERE.*=.*\$\{',            # Template literal in WHERE clause
    ]
    for pattern in sql_patterns:
        if re.search(pattern, content):
            violations.append("Potential SQL injection: Use parameterized queries")
    
    # 3. Check for hardcoded secrets
    secret_patterns = [
        r'(?:api[_-]?key|secret|token|password)\s*[:=]\s*["\'][^"\']{10,}["\']',
        r'Bearer\s+[A-Za-z0-9\-_]{20,}',
        r'["\'](?:sk|pk)_(?:test|live)_[A-Za-z0-9]{24,}["\']',  # Stripe keys
    ]
    for pattern in secret_patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            # Skip if it's accessing env vars
            if 'process.env' not in content[max(0, match.start()-50):match.end()]:
                line_num = content[:match.start()].count('\n') + 1
                violations.append(f"Line {line_num}: Hardcoded secret detected. Use environment variables")
    
    # 4. Check for unsafe innerHTML usage
    unsafe_patterns = [
        r'dangerouslySetInnerHTML',
        r'\.innerHTML\s*=',
        r'v-html=',
    ]
    for pattern in unsafe_patterns:
        if re.search(pattern, content):
            violations.append("Unsafe HTML rendering detected. This can lead to XSS attacks")
    
    # 5. Check for missing CSRF protection
    if 'form' in content.lower() and '/api/' in file_path:
        if not any(csrf in content for csrf in ['csrf', 'CSRF', 'X-CSRF-Token']):
            violations.append("API route handling forms without CSRF protection")
    
    # 6. Check for eval() usage
    if 'eval(' in content or 'new Function(' in content:
        violations.append("eval() or Function constructor usage detected - security risk")
    
    # 7. Check for missing authentication
    if '/api/' in file_path and file_path not in ['/api/auth', '/api/public']:
        auth_patterns = ['getSession', 'getServerSession', 'requireAuth', 'isAuthenticated', 'userId']
        if not any(auth in content for auth in auth_patterns):
            violations.append("API route without authentication check")
    
    return violations

def main():
    """Main hook logic following official specification"""
    try:
        # Read input from stdin (official format)
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool information
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Only check write operations
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            sys.exit(0)  # Success - continue
        
        # Get file path and content
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        content = tool_input.get('content', '')
        if 'new_str' in tool_input:  # Edit operations
            content = tool_input.get('new_str', '')
        
        # Check for security issues
        violations = check_security_issues(file_path, content)
        
        if violations:
            # For security issues, we'll warn but not block (exit code 1)
            # Change to exit code 2 if you want to block
            warning_msg = "⚠️ Security Warning\n\n"
            warning_msg += "Potential security issues detected:\n\n"
            for v in violations:
                warning_msg += f"• {v}\n"
            warning_msg += "\nRecommendations:\n"
            warning_msg += "• Always validate user input with zod schemas\n"
            warning_msg += "• Use parameterized queries for database operations\n"
            warning_msg += "• Store secrets in environment variables\n"
            warning_msg += "• Implement proper authentication and authorization\n"
            warning_msg += "• Avoid eval() and innerHTML\n"
            
            # Official format: stderr for message
            print(warning_msg, file=sys.stderr)
            sys.exit(1)  # Warning - non-blocking error
            # Use sys.exit(2) if you want to block the operation
        
        # No issues - continue
        sys.exit(0)
        
    except Exception as e:
        # Non-blocking error - show to user but continue
        print(f"Security validator hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)  # Non-blocking error

if __name__ == '__main__':
    main()
