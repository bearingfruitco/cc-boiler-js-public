#!/usr/bin/env python3
"""
State Save Hook - Automatically save work state after operations
Tracks file modifications and saves state locally
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

def get_work_context():
    """Get current work context"""
    context = {
        'timestamp': datetime.now().isoformat(),
        'files_modified': [],
        'session_id': os.getenv('CLAUDE_SESSION_ID', 'unknown')
    }
    
    # Track recently modified files
    recent_files_file = Path(".claude/state/recent-files.txt")
    if recent_files_file.exists():
        try:
            with open(recent_files_file, 'r') as f:
                lines = f.readlines()
                context['files_modified'] = [line.strip() for line in lines[-10:]]
        except:
            pass
    
    return context

def save_state(state):
    """Save state to local file"""
    state_dir = Path(".claude/state")
    state_dir.mkdir(parents=True, exist_ok=True)
    
    # Save current state
    state_file = state_dir / "current-state.json"
    try:
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
        return True
    except:
        return False

def update_recent_files(file_path):
    """Update list of recently modified files"""
    if not file_path:
        return
    
    state_dir = Path(".claude/state")
    state_dir.mkdir(parents=True, exist_ok=True)
    
    recent_files = state_dir / "recent-files.txt"
    
    try:
        # Read existing files
        existing = set()
        if recent_files.exists():
            with open(recent_files, 'r') as f:
                existing = set(line.strip() for line in f.readlines())
        
        # Add new file
        existing.add(file_path)
        
        # Keep only last 50 files
        files_list = list(existing)
        if len(files_list) > 50:
            files_list = files_list[-50:]
        
        # Write back
        with open(recent_files, 'w') as f:
            for fp in files_list:
                f.write(f"{fp}\n")
    except:
        pass

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        try:
            input_data = json.loads(sys.stdin.read())
        except (json.JSONDecodeError, ValueError):
            # No valid JSON on stdin (e.g., when run directly for testing)
            sys.exit(0)
        
        # Extract tool information
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Only track write operations
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            # Not a write operation - exit normally
            sys.exit(0)
        
        # Get file path
        file_path = tool_input.get('file_path', '')
        
        # Update recent files
        if file_path:
            update_recent_files(file_path)
        
        # Save state periodically (every 10th operation)
        state_dir = Path(".claude/state")
        counter_file = state_dir / "save-counter.txt"
        
        counter = 0
        if counter_file.exists():
            try:
                with open(counter_file, 'r') as f:
                    counter = int(f.read().strip())
            except:
                counter = 0
        
        counter += 1
        
        # Save counter
        state_dir.mkdir(parents=True, exist_ok=True)
        with open(counter_file, 'w') as f:
            f.write(str(counter))
        
        # Save state every 10 operations
        if counter % 10 == 0:
            state = get_work_context()
            save_state(state)
        
        # PostToolUse hooks exit with 0 for success
        sys.exit(0)
        
    except Exception as e:
        # On error, log to stderr and exit normally
        print(f"State save hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
