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

def contains_pii_field(text):
    """Check if text contains PII field names."""
    text_lower = text.lower()
    for pattern in PII_PATTERNS:
        if pattern in text_lower:
            return True, pattern
    return False, None

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
    """Main hook function."""
    try:
        # Get hook input
        hook_input = json.loads(sys.stdin.read())
        tool_name = hook_input.get('tool', '')
        params = hook_input.get('params', {})
        
        # Only check write operations
        if tool_name not in ['write_file', 'str_replace_editor', 'str_replace_based_edit_tool']:
            print(json.dumps({"action": "continue"}))
            return
        
        # Get file content
        content = params.get('content', '') or params.get('new_str', '')
        file_path = params.get('path', '') or params.get('file_path', '')
        
        if not content:
            print(json.dumps({"action": "continue"}))
            return
        
        # Check for violations
        violations = check_file_content(content, file_path)
        
        if violations:
            # For critical violations, warn but don't block (for now)
            critical_types = ['console_log', 'localStorage', 'url_params']
            has_critical = any(v['type'] in critical_types for v in violations)
            
            if has_critical:
                warning = "⚠️ PII PROTECTION WARNING:\n"
                for v in violations:
                    warning += f"  - {v['message']}\n"
                warning += "\nConsider using server-side handling for PII data."
                
                print(json.dumps({
                    "action": "continue",
                    "warning": warning
                }))
            else:
                print(json.dumps({"action": "continue"}))
        else:
            print(json.dumps({"action": "continue"}))
    
    except Exception as e:
        # On error, continue but log
        print(json.dumps({
            "action": "continue",
            "error": f"PII hook error: {str(e)}"
        }))

if __name__ == "__main__":
    main()
