#!/usr/bin/env python3
"""
TCPA Compliance Hook - Ensure phone consent language
Follows official Claude Code hooks specification
"""

import json
import sys
import re

# Required consent language patterns
CONSENT_PATTERNS = [
    r'consent\s+to\s+receive',
    r'agree\s+to\s+receive',
    r'opt[- ]?in',
    r'message\s+and\s+data\s+rates',
    r'standard\s+message\s+rates',
    r'reply\s+STOP\s+to\s+cancel',
    r'text\s+messaging\s+terms'
]

def check_tcpa_compliance(file_path, content):
    """Check if phone fields have proper TCPA consent"""
    
    # Only check form-related files
    if not any(x in file_path.lower() for x in ['form', 'contact', 'lead', 'signup', 'register']):
        return []
    
    violations = []
    
    # Look for phone input fields
    phone_patterns = [
        r'<input[^>]*(?:name|id)=["\'](?:phone|mobile|cell|tel)["\'][^>]*>',
        r'<input[^>]*type=["\']tel["\'][^>]*>',
        r'(?:phone|mobile|cell|telephone).*?(?:input|field|textfield)',
    ]
    
    has_phone_field = False
    for pattern in phone_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            has_phone_field = True
            break
    
    if has_phone_field:
        # Check for consent language
        has_consent = False
        for consent_pattern in CONSENT_PATTERNS:
            if re.search(consent_pattern, content, re.IGNORECASE):
                has_consent = True
                break
        
        if not has_consent:
            violations.append("Phone field detected without TCPA consent language")
        
        # Check for specific required elements
        if not re.search(r'message\s+and\s+data\s+rates', content, re.IGNORECASE):
            violations.append("Missing 'Message and data rates may apply' disclosure")
        
        if not re.search(r'STOP|stop\s+to\s+(?:cancel|unsubscribe|opt[- ]?out)', content, re.IGNORECASE):
            violations.append("Missing STOP instructions for opt-out")
    
    return violations

def main():
    """Main hook logic following official specification"""
    try:
        # Read input from stdin (official format)
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool information
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Only check write operations on forms
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            sys.exit(0)  # Success - continue
        
        # Get file path and content
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        content = tool_input.get('content', '')
        if 'new_str' in tool_input:  # Edit operations
            content = tool_input.get('new_str', '')
        
        # Skip non-form files
        if not any(ext in file_path for ext in ['.tsx', '.jsx', '.vue', '.html']):
            sys.exit(0)
        
        # Check TCPA compliance
        violations = check_tcpa_compliance(file_path, content)
        
        if violations:
            # Block operation with exit code 2
            error_msg = "📱 TCPA Compliance Violation\n\n"
            error_msg += "Phone number collection requires proper consent language.\n\n"
            error_msg += "Issues found:\n"
            for v in violations:
                error_msg += f"• {v}\n"
            error_msg += "\nRequired elements:\n"
            error_msg += "• Clear consent to receive text messages\n"
            error_msg += "• 'Message and data rates may apply' disclosure\n"
            error_msg += "• Instructions to reply STOP to cancel\n"
            error_msg += "• Link to messaging terms and conditions\n\n"
            error_msg += "Example consent language:\n"
            error_msg += '"By providing your phone number, you consent to receive text messages from us. '
            error_msg += 'Message and data rates may apply. Reply STOP to cancel at any time."'
            
            # Official format: stderr + exit code 2 for blocking
            print(error_msg, file=sys.stderr)
            sys.exit(2)  # Block operation
        
        # Compliant - continue
        sys.exit(0)
        
    except Exception as e:
        # Non-blocking error - show to user but continue
        print(f"TCPA compliance hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)  # Non-blocking error

if __name__ == '__main__':
    main()
