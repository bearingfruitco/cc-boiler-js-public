#!/usr/bin/env python3
"""
PII Protection Hook - Prevent PII exposure in logs, URLs, and client storage
Ensures compliance with privacy regulations
"""

import json
import sys
import re
from pathlib import Path

# Common PII field patterns
PII_PATTERNS = [
    'email', 'phone', 'ssn', 'social_security',
    'first_name', 'last_name', 'full_name', 'name',
    'address', 'street', 'city', 'state', 'zip',
    'date_of_birth', 'dob', 'birthdate',
    'credit_card', 'card_number', 'cvv',
    'bank_account', 'routing_number',
    'drivers_license', 'passport',
    'ip_address', 'user_id', 'customer_id'
]

def check_file_content(content, file_path):
    """Check file content for PII violations"""
    violations = []
    lines = content.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        line_lower = line.lower()
        
        # Check console.log with PII
        if any(console in line for console in ['console.log', 'console.error', 'console.warn']):
            for field in PII_PATTERNS:
                if field in line_lower:
                    violations.append({
                        'type': 'console_log',
                        'line': line_num,
                        'field': field,
                        'content': line.strip()[:80]
                    })
        
        # Check localStorage/sessionStorage
        if 'localstorage' in line_lower or 'sessionstorage' in line_lower:
            for field in PII_PATTERNS:
                if field in line_lower:
                    violations.append({
                        'type': 'localStorage',
                        'line': line_num,
                        'field': field,
                        'content': line.strip()[:80]
                    })
        
        # Check URL parameters
        url_patterns = [
            r'[?&]email=',
            r'[?&]phone=',
            r'[?&]ssn=',
            r'[?&]name=',
            r'[?&]address=',
            r'searchParams\.set\([\'"](?:email|phone|ssn|name)',
            r'searchParams\.append\([\'"](?:email|phone|ssn|name)'
        ]
        
        for pattern in url_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                violations.append({
                    'type': 'url_params',
                    'line': line_num,
                    'pattern': pattern,
                    'content': line.strip()[:80]
                })
    
    return violations

def format_violation_message(violations):
    """Format violations into readable message"""
    message = "🔒 PII PROTECTION VIOLATIONS\n\n"
    
    # Group by type
    by_type = {}
    for v in violations:
        if v['type'] not in by_type:
            by_type[v['type']] = []
        by_type[v['type']].append(v)
    
    # Console.log violations
    if 'console_log' in by_type:
        message += "❌ PII in Console Logs:\n"
        for v in by_type['console_log'][:3]:
            message += f"  Line {v['line']}: Logging {v['field']} field\n"
    
    # localStorage violations
    if 'localStorage' in by_type:
        message += "\n❌ PII in Client Storage:\n"
        for v in by_type['localStorage'][:3]:
            message += f"  Line {v['line']}: Storing {v['field']} in localStorage\n"
    
    # URL violations
    if 'url_params' in by_type:
        message += "\n❌ PII in URLs:\n"
        for v in by_type['url_params'][:3]:
            message += f"  Line {v['line']}: PII in URL parameters\n"
    
    message += "\n📚 Security Rules:\n"
    message += "  • Never log PII to console\n"
    message += "  • Never store PII in localStorage/sessionStorage\n"
    message += "  • Never put PII in URLs or query parameters\n"
    message += "  • Use server-side storage for sensitive data\n"
    
    return message

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool name
        tool_name = input_data.get('tool_name', '')
        
        # Only check write operations
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            sys.exit(0)
        
        # Extract tool input
        tool_input = input_data.get('tool_input', {})
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        
        # Only check code files
        if not any(file_path.endswith(ext) for ext in ['.ts', '.tsx', '.js', '.jsx']):
            sys.exit(0)
            
        content = tool_input.get('content', tool_input.get('new_str', ''))
        
        # Skip if no content
        if not content:
            sys.exit(0)
        
        # Check for violations
        violations = check_file_content(content, file_path)
        
        if violations:
            message = format_violation_message(violations)
            
            # For critical violations (PII in logs/storage), block
            critical_types = ['console_log', 'localStorage', 'url_params']
            has_critical = any(v['type'] in critical_types for v in violations)
            
            if has_critical:
                # Block using official format: stderr + exit code 2
                print(message, file=sys.stderr)
                sys.exit(2)  # Block operation
        
        # No violations or non-critical - continue normally
        sys.exit(0)
    
    except Exception as e:
        # Non-blocking error - show to user but continue
        print(f"PII Protection hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)  # Non-blocking error

if __name__ == "__main__":
    main()
