#!/usr/bin/env python3
"""
Conflict Check Hook - Check for potential file conflicts with team members
Prevents overwriting active work by other developers
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

def check_active_work(file_path):
    """Check if another team member is actively working on this file"""
    # Team registry file
    registry_file = Path('.claude/team/registry.json')
    
    if not registry_file.exists():
        return None
    
    try:
        with open(registry_file, 'r') as f:
            registry = json.load(f)
        
        active_work = registry.get('active_work', {})
        
        # Check if file is being worked on
        for user, files in active_work.items():
            if file_path in files:
                # Check timestamp
                timestamp = files[file_path].get('timestamp', '')
                if timestamp:
                    last_edit = datetime.fromisoformat(timestamp)
                    # Consider active if edited within last 30 minutes
                    if datetime.now() - last_edit < timedelta(minutes=30):
                        return user
    except:
        pass
    
    return None

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
        
        # Extract file path
        tool_input = input_data.get('tool_input', {})
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        
        if not file_path:
            # No file path - continue
            sys.exit(0)
        
        # Check for active work
        active_user = check_active_work(file_path)
        
        if active_user:
            # Someone else is working on this file - warn
            message = f"⚠️ POTENTIAL CONFLICT\n\n"
            message += f"Team member '{active_user}' is actively working on:\n{file_path}\n\n"
            message += f"They last edited this file within the past 30 minutes.\n"
            message += f"Consider:\n"
            message += f"• Checking with them before making changes\n"
            message += f"• Using /collab-sync {active_user} to sync changes\n"
            message += f"• Working on a different file\n\n"
            message += f"Proceed with caution to avoid conflicts."
            
            # Block with warning
            print(json.dumps({
                "decision": "block",
                "message": message
            }))
            sys.exit(0)
        
        # No conflict - continue normally
        sys.exit(0)
        
    except Exception as e:
        # On error, log to stderr and continue
        print(f"Conflict check error: {str(e)}", file=sys.stderr)
        sys.exit(0)

if __name__ == '__main__':
    main()
