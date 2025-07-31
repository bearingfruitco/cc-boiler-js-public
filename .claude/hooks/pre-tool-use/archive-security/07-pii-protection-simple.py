#!/usr/bin/env python3
"""
PII Protection Hook - Simplified Version
Prevents PII exposure in logs, URLs, and client storage
"""

import json
import sys
import re

# Common PII patterns
PII_FIELDS = [
    'email', 'phone', 'ssn', 'social_security',
    'first_name', 'last_name', 'full_name', 'name',
    'address', 'street', 'city', 'state', 'zip',
    'date_of_birth', 'dob', 'birthdate',
    'credit_card', 'card_number', 'cvv',
    'bank_account', 'routing_number',
    'drivers_license', 'passport',
    'ip_address', 'user_id', 'customer_id'
]

def check_pii_violations(content):
    """Check for PII violations"""
    violations = []
    lines = content.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        line_lower = line.lower()
        
        # Check console.log with PII
        if 'console.' in line:
            for field in PII_FIELDS:
                if field in line_lower:
                    violations.append(f"Line {line_num}: PII '{field}' in console.log")
        
        # Check localStorage/sessionStorage
        if 'localstorage' in line_lower or 'sessionstorage' in line_lower:
            for field in PII_FIELDS:
                if field in line_lower:
                    violations.append(f"Line {line_num}: PII '{field}' in browser storage")
        
        # Check URL parameters
        if '?' in line or '&' in line or 'searchParams' in line:
            for field in PII_FIELDS:
                if f'{field}=' in line_lower or f"'{field}'" in line or f'"{field}"' in line:
                    violations.append(f"Line {line_num}: PII '{field}' in URL")
    
    return violations

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool name - handle multiple formats
        tool_name = input_data.get('tool_name', '')
        if not tool_name and 'tool_use' in input_data:
            tool_name = input_data['tool_use'].get('name', '')
        
        # Only check write operations
        if tool_name not in ['Write', 'Edit', 'str_replace']:
            sys.exit(0)
        
        # Extract parameters
        tool_input = input_data.get('tool_input', {})
        if not tool_input and 'tool_use' in input_data:
            tool_input = input_data['tool_use'].get('parameters', {})
        
        # Get file path and content
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        content = tool_input.get('content', tool_input.get('new_str', ''))
        
        # Only check code files
        if not any(file_path.endswith(ext) for ext in ['.ts', '.tsx', '.js', '.jsx']):
            sys.exit(0)
        
        # Check for violations
        violations = check_pii_violations(content)
        
        if violations:
            message = "🔒 PII PROTECTION VIOLATIONS\n\n"
            for v in violations[:5]:  # Show first 5
                message += f"• {v}\n"
            
            if len(violations) > 5:
                message += f"\n... and {len(violations) - 5} more violations\n"
            
            message += "\n📚 Security Rules:\n"
            message += "• Never log PII to console\n"
            message += "• Never store PII in localStorage\n"
            message += "• Never put PII in URLs\n"
            message += "• Use server-side storage for sensitive data\n"
            
            print(json.dumps({
                "decision": "block",
                "message": message
            }))
            sys.exit(0)
        else:
            sys.exit(0)
        
    except Exception as e:
        # On error, exit with non-zero code and error in stderr
        print(f"PII protection hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
