#!/usr/bin/env python3
"""
TCPA Compliance Hook - Ensure messaging compliance
Checks for TCPA compliance in messaging features
"""

import json
import sys
import re
from pathlib import Path

def check_tcpa_compliance(content, file_path):
    """Check for TCPA compliance requirements in messaging code"""
    issues = []
    
    # Keywords that indicate messaging functionality
    messaging_keywords = [
        'sendSMS', 'sendMessage', 'sendText', 
        'twillio', 'sendgrid', 'messagebird',
        'sms', 'text message', 'notification'
    ]
    
    # Check if this file contains messaging code
    content_lower = content.lower()
    is_messaging = any(keyword in content_lower for keyword in messaging_keywords)
    
    if not is_messaging:
        return issues
    
    # TCPA compliance checks
    compliance_checks = {
        'consent': {
            'patterns': ['consent', 'opt-in', 'optin', 'permission', 'agree'],
            'message': 'Messaging feature must verify user consent'
        },
        'opt_out': {
            'patterns': ['stop', 'unsubscribe', 'opt-out', 'optout', 'cancel'],
            'message': 'Must provide opt-out mechanism (STOP command)'
        },
        'time_restrictions': {
            'patterns': ['time check', 'business hours', 'quiet hours', 'time zone'],
            'message': 'Must respect quiet hours (8am-9pm in recipient timezone)'
        },
        'record_keeping': {
            'patterns': ['audit', 'log', 'record', 'consent record'],
            'message': 'Must maintain consent records for compliance'
        }
    }
    
    # Check each compliance requirement
    for requirement, config in compliance_checks.items():
        found = False
        for pattern in config['patterns']:
            if pattern in content_lower:
                found = True
                break
        
        if not found:
            issues.append({
                'requirement': requirement,
                'message': config['message']
            })
    
    return issues

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool name
        tool_name = input_data.get('tool_name', '')
        
        # Only check write operations
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            # Not a write operation - continue normally
            sys.exit(0)
        
        # Extract tool input
        tool_input = input_data.get('tool_input', {})
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        content = tool_input.get('content', tool_input.get('new_str', ''))
        
        # Skip non-code files
        if not any(file_path.endswith(ext) for ext in ['.ts', '.tsx', '.js', '.jsx', '.py']):
            sys.exit(0)
        
        # Check TCPA compliance
        issues = check_tcpa_compliance(content, file_path)
        
        if issues:
            # Build warning message
            warning_msg = "⚖️ TCPA COMPLIANCE WARNING\n\n"
            warning_msg += "Detected messaging functionality without required compliance checks:\n\n"
            
            for issue in issues:
                warning_msg += f"❌ {issue['message']}\n"
            
            warning_msg += "\n📋 TCPA Requirements:\n"
            warning_msg += "1. Obtain express written consent before sending messages\n"
            warning_msg += "2. Provide clear opt-out instructions (STOP to cancel)\n"
            warning_msg += "3. Respect quiet hours (8am-9pm recipient timezone)\n"
            warning_msg += "4. Maintain consent records and audit logs\n"
            warning_msg += "5. Include business identification in messages\n\n"
            warning_msg += "Consider using the /tcpa-setup command for compliance templates."
            
            # Output warning to stderr
            print(warning_msg, file=sys.stderr)
        
        # Always continue (this is a warning hook)
        sys.exit(0)
        
    except Exception as e:
        # On error, log to stderr and exit with error code
        print(f"TCPA compliance hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
