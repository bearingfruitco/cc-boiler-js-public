#!/usr/bin/env python3
"""
Collaboration Sync Hook - Track and sync collaborative changes
Monitors file changes for team collaboration awareness
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool information
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Only track write operations
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            # Not a write operation - continue normally
            sys.exit(0)
        
        # Get file path
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        
        if file_path:
            # Track file modification
            collab_dir = Path('.claude/collab')
            collab_dir.mkdir(parents=True, exist_ok=True)
            
            # Log the change
            change_log = collab_dir / 'changes.log'
            with open(change_log, 'a') as f:
                f.write(f"{datetime.now().isoformat()} - Modified: {file_path}\n")
        
        # PreToolUse hooks exit with code 0 to continue (no output)
        sys.exit(0)
        
    except Exception as e:
        # Non-blocking error - show to user but continue
        print(f"Collab sync error: {str(e)}", file=sys.stderr)
        sys.exit(1)  # Non-blocking error

if __name__ == '__main__':
    main()
