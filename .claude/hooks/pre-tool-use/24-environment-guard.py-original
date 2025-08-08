#!/usr/bin/env python3
"""
Environment Guard Hook - Prevents dangerous operations based on environment
Blocks destructive operations in production, warns in staging
"""

import json
import sys
import os
from pathlib import Path

def get_current_environment():
    """Get the current environment from NODE_ENV"""
    return os.environ.get('NODE_ENV', 'development')

def is_destructive_operation(tool_name, tool_input):
    """Check if the operation is potentially destructive"""
    destructive_patterns = {
        'Bash': [
            'rm -rf', 'rm -f',
            'DROP TABLE', 'DROP DATABASE',
            'TRUNCATE', 'DELETE FROM',
            'git push --force',
            'npm publish',
            ':>/dev/null',
            'dd if=',
        ],
        'Write': [
            '.env.production',
            'prod.env',
            'production.env',
        ],
        'Delete': True,  # All delete operations are destructive
    }
    
    if tool_name == 'Delete':
        return True
    
    if tool_name in destructive_patterns:
        patterns = destructive_patterns[tool_name]
        if isinstance(patterns, bool):
            return patterns
            
        command = tool_input.get('command', '') if tool_name == 'Bash' else ''
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        
        for pattern in patterns:
            if pattern in command or pattern in file_path:
                return True
    
    return False

def is_sensitive_file(file_path):
    """Check if the file contains sensitive information"""
    sensitive_patterns = [
        '.env',
        'secrets',
        'credentials',
        'key',
        'token',
        '.pem',
        '.key',
        'config.production',
    ]
    
    return any(pattern in file_path.lower() for pattern in sensitive_patterns)

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool information
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Get current environment
        env = get_current_environment()
        
        # Production environment checks
        if env == 'production':
            # Check for destructive operations
            if is_destructive_operation(tool_name, tool_input):
                error_msg = {
                    "action": "block",
                    "message": "🚫 PRODUCTION ENVIRONMENT: Destructive operations are blocked!\n\n"
                              "This operation could damage production data.\n"
                              "Please use staging environment for testing.\n\n"
                              "To proceed, you must:\n"
                              "1. Switch to staging/development environment\n"
                              "2. Test the operation thoroughly\n"
                              "3. Use proper deployment procedures"
                }
                print(json.dumps(error_msg))
                sys.exit(1)
            
            # Check for sensitive file modifications
            if tool_name in ['Write', 'Edit', 'MultiEdit']:
                file_path = tool_input.get('file_path', tool_input.get('path', ''))
                if is_sensitive_file(file_path):
                    # Log the attempt
                    with open('.claude/logs/production-attempts.log', 'a') as f:
                        f.write(f"Attempted to modify {file_path} in production\n")
                    
                    error_msg = {
                        "action": "block",
                        "message": f"🚫 PRODUCTION: Cannot modify sensitive file '{file_path}'\n\n"
                                  "Sensitive files cannot be modified directly in production.\n"
                                  "Use environment variables or deployment procedures."
                    }
                    print(json.dumps(error_msg))
                    sys.exit(1)
        
        # Staging environment warnings
        elif env == 'staging':
            if is_destructive_operation(tool_name, tool_input):
                # Warn but allow in staging
                warning_msg = {
                    "action": "allow",
                    "message": "⚠️  STAGING ENVIRONMENT: Destructive operation detected!\n\n"
                              "This operation will be executed in STAGING.\n"
                              "Make sure you have backups if needed.\n"
                              "This would be BLOCKED in production."
                }
                print(json.dumps(warning_msg))
                sys.exit(0)
        
        # Log all operations by environment
        log_dir = Path('.claude/logs/environments')
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"{env}-operations.log"
        with open(log_file, 'a') as f:
            f.write(f"{tool_name}: {json.dumps(tool_input)}\n")
        
        # Allow operation to proceed
        sys.exit(0)
        
    except Exception as e:
        # In case of any error, log but allow operation
        error_output = {
            "action": "allow",
            "message": f"Environment guard error: {str(e)}"
        }
        print(json.dumps(error_output))
        sys.exit(1)

if __name__ == '__main__':
    main()
