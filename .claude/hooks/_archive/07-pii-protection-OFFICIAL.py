#!/usr/bin/env python3
"""
PII Protection Hook - Compliant with Official Claude Code Hook Specification
Prevents PII exposure in logs, URLs, and client storage
"""

import json
import sys
import re

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
    """Check for PII violations in file content."""
    violations = []
    
    # Check for console.log with PII
    console_pattern = r'console\.log.*?\b(' + '|'.join(PII_PATTERNS) + r')\b'
    if re.search(console_pattern, content, re.IGNORECASE):
        violations.append({
            'type': 'console_log',
            'message': 'PII fields detected in console.log statements'
        })
    
    # Check for localStorage/sessionStorage with PII
    storage_pattern = r'(localStorage|sessionStorage)\.(setItem|getItem).*?\b(' + '|'.join(PII_PATTERNS) + r')\b'
    if re.search(storage_pattern, content, re.IGNORECASE):
        violations.append({
            'type': 'localStorage',
            'message': 'PII detected in browser storage operations'
        })
    
    # Check for PII in URL parameters
    url_pattern = r'[?&](' + '|'.join(PII_PATTERNS) + r')='
    if re.search(url_pattern, content, re.IGNORECASE):
        violations.append({
            'type': 'url_params',
            'message': 'PII detected in URL parameters'
        })
    
    return violations

def main():
    """Main hook function following official Claude Code hook specification."""
    try:
        # Read JSON input from stdin (as per official docs)
        input_data = json.loads(sys.stdin.read())
        
        # Extract fields according to official schema
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Only check write operations
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            # Exit code 0 = success, continue
            sys.exit(0)
        
        # Get file content and path from tool_input
        content = tool_input.get('content', '') or tool_input.get('new_str', '')
        file_path = tool_input.get('file_path', '') or tool_input.get('path', '')
        
        if not content:
            sys.exit(0)
        
        # Check for violations
        violations = check_file_content(content, file_path)
        
        if violations:
            # For critical violations, block with exit code 2
            critical_types = ['console_log', 'localStorage', 'url_params']
            has_critical = any(v['type'] in critical_types for v in violations)
            
            if has_critical:
                # Exit code 2 = blocking error
                # stderr is fed back to Claude
                error_msg = "⚠️ PII PROTECTION VIOLATION:\n"
                for v in violations:
                    error_msg += f"  - {v['message']}\n"
                error_msg += "\nFix: Use server-side handling for PII data. Never log or store PII client-side."
                
                print(error_msg, file=sys.stderr)
                sys.exit(2)
            else:
                # Non-critical violations - warn but continue
                sys.exit(0)
        else:
            # No violations - continue
            sys.exit(0)
    
    except Exception as e:
        # On error, log to stderr but continue (non-blocking)
        print(f"PII hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)  # Non-blocking error

if __name__ == "__main__":
    main()
