#!/usr/bin/env python3
"""
Security Command Enhancer Hook
Enhances commands with security options when relevant
"""

import json
import sys

def main():
    """Main hook entry point following Claude Code hook specification."""
    try:
        # Read input from Claude Code
        event = json.loads(sys.stdin.read())
        
        # Extract tool name and input
        tool_name = event.get('tool_name', '')
        tool_input = event.get('tool_input', {})
        
        # Commands that should have security enhancements
        security_commands = {
            'create-component': {
                'suggest': '--secure flag for XSS protection'
            },
            'create-api': {
                'suggest': '--secure flag adds rate limiting and validation'
            },
            'create-tracked-form': {
                'suggest': '--captcha flag for bot protection'
            },
            'ctf': {
                'suggest': '--captcha flag for bot protection'
            },
            'cc': {
                'suggest': '--secure flag for security best practices'
            }
        }
        
        # Check if running a command that could use security
        if tool_name == 'Bash':
            command = tool_input.get('command', '')
            
            for cmd, info in security_commands.items():
                if cmd in command and '--secure' not in command and '--captcha' not in command:
                    # Output suggestion to stderr
                    message = f"💡 Security Tip: Consider using {info['suggest']} with {cmd}\n"
                    message += "This adds important security features to protect against common vulnerabilities."
                    print(message, file=sys.stderr)
                    break
        
        # Always continue normally
        sys.exit(0)
        
    except Exception as e:
        # On error, log to stderr and exit with error code
        print(f"Security command enhancer hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
