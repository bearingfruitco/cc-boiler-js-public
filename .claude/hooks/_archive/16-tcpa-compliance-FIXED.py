#!/usr/bin/env python3
"""
TCPA Compliance Hook - Ensures proper consent for communications
Validates TCPA compliance in forms and communication features
"""

import json
import sys
import re

def check_tcpa_compliance(content, file_path):
    """Check for TCPA compliance issues."""
    violations = []
    
    # Check for forms collecting phone numbers without consent
    if 'phone' in content.lower() or 'mobile' in content.lower():
        # Look for consent checkbox or text
        has_consent = any(term in content.lower() for term in [
            'consent', 'agree', 'opt-in', 'permission', 
            'tcpa', 'text messages', 'sms consent'
        ])
        
        if not has_consent:
            violations.append({
                'type': 'missing_consent',
                'message': 'Form collects phone number without TCPA consent'
            })
    
    # Check for automated dialing/texting features
    if any(term in content.lower() for term in ['autodialer', 'bulk sms', 'mass text']):
        violations.append({
            'type': 'automated_communication',
            'message': 'Automated communication features require TCPA compliance'
        })
    
    return violations

def main():
    """Main hook function."""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool name
        tool_name = input_data.get('tool', '')
        if not tool_name and 'tool_name' in input_data:
            tool_name = input_data['tool_name']
        
        # Extract parameters
        params = input_data.get('params', {})
        if not params and 'tool_input' in input_data:
            params = input_data['tool_input']
        
        # Only check write operations
        if tool_name not in ['write_file', 'str_replace_editor', 'str_replace_based_edit_tool']:
            print(json.dumps({"action": "continue"}))
            return
        
        # Get file content
        content = params.get('content', '') or params.get('new_str', '')
        file_path = params.get('path', '') or params.get('file_path', '')
        
        # Skip non-form files
        if not any(indicator in file_path.lower() for indicator in ['form', 'contact', 'lead', 'signup']):
            print(json.dumps({"action": "continue"}))
            return
        
        # Check for violations
        violations = check_tcpa_compliance(content, file_path)
        
        if violations:
            warning = "⚠️ TCPA COMPLIANCE WARNING:\\n"
            for v in violations:
                warning += f"  - {v['message']}\\n"
            warning += "\\nEnsure proper consent language is included for phone number collection."
            
            print(json.dumps({
                "action": "continue",
                "warning": warning
            }))
        else:
            print(json.dumps({"action": "continue"}))
    
    except Exception as e:
        # On error, continue but log
        print(json.dumps({
            "action": "continue",
            "error": f"TCPA hook error: {str(e)}"
        }))

if __name__ == '__main__':
    main()
