#!/usr/bin/env python3
"""
TCPA Compliance Hook - Compliant with Official Claude Code Hook Specification
Ensures proper consent for communications in forms
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
                'message': 'Form collects phone number without TCPA consent language'
            })
    
    # Check for automated dialing/texting features
    if any(term in content.lower() for term in ['autodialer', 'bulk sms', 'mass text']):
        violations.append({
            'type': 'automated_communication',
            'message': 'Automated communication features require TCPA compliance controls'
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
        
        # Get file path from tool_input
        file_path = tool_input.get('file_path', '') or tool_input.get('path', '')
        
        # Skip non-form files
        if not any(indicator in file_path.lower() for indicator in ['form', 'contact', 'lead', 'signup']):
            sys.exit(0)
        
        # Get content
        content = tool_input.get('content', '') or tool_input.get('new_str', '')
        if not content:
            sys.exit(0)
        
        # Check for violations
        violations = check_tcpa_compliance(content, file_path)
        
        if violations:
            # Exit code 2 = blocking error
            error_msg = "⚠️ TCPA COMPLIANCE VIOLATION:\n"
            for v in violations:
                error_msg += f"  - {v['message']}\n"
            error_msg += "\nFix: Add TCPA consent language near phone number field:\n"
            error_msg += '"By providing your phone number, you consent to receive text messages..."'
            
            print(error_msg, file=sys.stderr)
            sys.exit(2)
        else:
            # No violations - continue
            sys.exit(0)
    
    except Exception as e:
        # On error, log to stderr but continue (non-blocking)
        print(f"TCPA hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)  # Non-blocking error

if __name__ == "__main__":
    main()
