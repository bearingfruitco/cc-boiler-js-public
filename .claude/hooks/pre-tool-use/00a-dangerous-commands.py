#!/usr/bin/env python3
"""
Dangerous Commands Hook - Detect and warn about potentially dangerous operations
"""

import json
import sys

# Define dangerous commands that should be warned about
DANGEROUS_COMMANDS = [
    'rm -rf /',
    'rm -rf ~',
    'rm -rf .',
    'sudo rm -rf',
    'chmod 777 /',
    'chmod -R 777',
    'kill -9 -1',
    'pkill -9',
    'shutdown',
    'reboot',
    'format',
    '> /dev/sda',
    'dd if=/dev/zero',
    'curl | sudo bash',
    'wget | sudo sh',
    'git push --force origin main',
    'git reset --hard HEAD~',
    'DROP DATABASE',
    'DROP TABLE',
    'DELETE FROM users',
    'TRUNCATE'
]

# Safe commands that should never be blocked
SAFE_COMMANDS = [
    'gh issue',
    'gh pr',
    'gh repo',
    'git status',
    'git diff',
    'git log',
    'npm test',
    'npm run',
    'ls',
    'cat',
    'echo',
    'pwd',
    'which'
]

def is_safe_command(command):
    """Check if command is explicitly safe"""
    if not command:
        return False
    
    command_lower = command.lower()
    
    # Check for safe patterns
    for safe in SAFE_COMMANDS:
        if safe.lower() in command_lower:
            return True
    
    # GitHub CLI is always safe
    if command_lower.startswith('gh '):
        return True
    
    # Reading files is safe
    if command_lower.startswith(('cat ', 'less ', 'head ', 'tail ')):
        return True
    
    return False

def is_dangerous_command(command):
    """Check if command contains dangerous patterns"""
    if not command:
        return False
    
    # Skip if explicitly safe
    if is_safe_command(command):
        return False
    
    command_lower = command.lower()
    
    # Check for dangerous patterns
    for dangerous in DANGEROUS_COMMANDS:
        if dangerous.lower() in command_lower:
            # Special case: rm is ok if not removing root or home
            if 'rm ' in command_lower:
                if any(bad in command_lower for bad in ['rm -rf /', 'rm -rf ~', 'rm -rf .']):
                    return True
                else:
                    continue  # rm of specific files is ok
            
            # Special case: chmod is ok if not recursive on root
            if 'chmod' in command_lower:
                if 'chmod 777 /' in command_lower or 'chmod -R 777' in command_lower:
                    return True
                else:
                    continue  # chmod of specific files is ok
            
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
            # Block dangerous commands using official format
            error_msg = f"⚠️ DANGEROUS COMMAND DETECTED\n\n"
            error_msg += f"This command appears to be potentially destructive:\n{command}\n\n"
            error_msg += "Please review carefully before proceeding.\n\n"
            error_msg += "If this is a false positive, you can:\n"
            error_msg += "1. Modify the command to be more specific\n"
            error_msg += "2. Temporarily disable this hook\n"
            error_msg += "3. Update the hook's DANGEROUS_COMMANDS list"
            
            print(error_msg, file=sys.stderr)
            sys.exit(2)  # Block operation
        
        # Not dangerous - continue normally (no output)
        sys.exit(0)
        
    except Exception as e:
        # On error, log to stderr and continue (non-blocking)
        print(f"Dangerous commands hook error: {str(e)}", file=sys.stderr)
        sys.exit(0)  # Allow operation on error

if __name__ == '__main__':
    main()
