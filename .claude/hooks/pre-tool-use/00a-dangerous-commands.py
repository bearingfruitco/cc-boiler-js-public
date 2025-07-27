#!/usr/bin/env python3
"""
Dangerous Commands Hook - Detect and warn about potentially dangerous operations
"""

import json
import sys

# Define dangerous commands that should be warned about
DANGEROUS_COMMANDS = [
    'rm -rf',
    'sudo rm',
    'chmod 777',
    'kill -9',
    'pkill',
    'shutdown',
    'reboot',
    'format',
    '> /dev/null',
    'curl | bash',
    'wget | sh'
]

def is_dangerous_command(command):
    """Check if command contains dangerous patterns"""
    if not command:
        return False
    
    command_lower = command.lower()
    for dangerous in DANGEROUS_COMMANDS:
        if dangerous.lower() in command_lower:
            return True
    
    return False

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool name
        tool_name = input_data.get('tool_name', '')
        
        # Only check Bash commands
        if tool_name != 'Bash':
            # Not a bash command - continue normally
            sys.exit(0)
        
        # Get command
        tool_input = input_data.get('tool_input', {})
        command = tool_input.get('command', '')
        
        # Check if dangerous
        if is_dangerous_command(command):
            # Block dangerous commands
            print(json.dumps({
                "decision": "block",
                "message": f"⚠️ DANGEROUS COMMAND DETECTED\n\nThis command appears to be potentially destructive:\n{command}\n\nPlease review carefully before proceeding."
            }))
            sys.exit(0)
        
        # Not dangerous - continue normally (no output)
        sys.exit(0)
        
    except Exception as e:
        # On error, log to stderr and continue
        print(f"Dangerous commands hook error: {str(e)}", file=sys.stderr)
        sys.exit(0)

if __name__ == '__main__':
    main()
