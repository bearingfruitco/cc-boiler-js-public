#!/usr/bin/env python3
"""
Auto-Approve Safe Operations Hook
Prevents workflow interruption by auto-approving genuinely safe operations
Only approves read operations and test file modifications
Compliant with official Claude Code hooks documentation
"""

import json
import sys
import os
from pathlib import Path

# Define safe operations that can be auto-approved
SAFE_READ_OPERATIONS = {
    'Read',
    'MultiRead',
    'ListDirectory',
    'DirectoryTree',
    'GetFileInfo',
    'SearchFiles',
    'Glob',
    'Grep'
}

# Safe directories for write operations
SAFE_WRITE_DIRECTORIES = [
    '/tests/',
    '/test/',
    '/__tests__/',
    '/.claude/checkpoints/',
    '/.claude/transcripts/',
    '/tmp/',
    '/.cache/'
]

# Safe shell commands that can be auto-approved
SAFE_SHELL_COMMANDS = [
    'npm test',
    'npm run test',
    'npm run lint',
    'npm run typecheck',
    'npm run type-check',
    'npm run validate',
    'jest',
    'vitest',
    'playwright test',
    'tsc --noEmit',
    'eslint',
    'prettier --check',
    'biome check',
    'biome format'
]

def is_safe_write_path(path):
    """Check if the path is in a safe directory for auto-approval"""
    if not path:
        return False
    
    # Normalize path
    path_str = str(path).replace('\\', '/')
    
    # Check if path is in any safe directory
    for safe_dir in SAFE_WRITE_DIRECTORIES:
        if safe_dir in path_str:
            return True
    
    # Check if it's a test file by name
    path_obj = Path(path_str)
    if path_obj.name.endswith(('.test.ts', '.test.tsx', '.test.js', '.test.jsx', 
                              '.spec.ts', '.spec.tsx', '.spec.js', '.spec.jsx')):
        return True
    
    return False

def is_safe_shell_command(command):
    """Check if the shell command is safe for auto-approval"""
    if not command:
        return False
    
    # Check if command starts with any safe command
    command_lower = command.strip().lower()
    for safe_cmd in SAFE_SHELL_COMMANDS:
        if command_lower.startswith(safe_cmd.lower()):
            return True
    
    return False

def should_auto_approve(tool_name, tool_input):
    """Determine if this operation should be auto-approved"""
    # Auto-approve all read operations
    if tool_name in SAFE_READ_OPERATIONS:
        return True, "Read operation - auto-approved"
    
    # Check write operations in safe directories
    if tool_name in ['Write', 'Edit', 'MultiEdit']:
        path = tool_input.get('file_path', tool_input.get('path', ''))
        if is_safe_write_path(path):
            return True, f"Test/cache file operation - auto-approved"
    
    # Check safe shell commands
    if tool_name == 'Bash':
        command = tool_input.get('command', '')
        if is_safe_shell_command(command):
            return True, f"Safe command - auto-approved"
    
    # Default to not auto-approving
    return False, None

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        hook_input = json.loads(sys.stdin.read())
        
        # Extract tool name
        tool_name = hook_input.get('tool_name', '')
        
        # Extract tool input
        tool_input = hook_input.get('tool_input', {})
        
        # Check if this operation should be auto-approved
        should_approve, reason = should_auto_approve(tool_name, tool_input)
        
        if should_approve:
            # Auto-approve using the official format for PreToolUse
            print(json.dumps({
                "decision": "approve",
                "reason": reason
            }))
        else:
            # Let normal flow continue - exit code 0
            sys.exit(0)
        
    except Exception as e:
        # On any error, fail safely by continuing normally
        print(f"Auto-approval hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)  # Non-blocking error

if __name__ == '__main__':
    main()
