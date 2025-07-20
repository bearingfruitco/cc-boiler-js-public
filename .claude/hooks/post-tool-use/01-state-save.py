#!/usr/bin/env python3
"""
State Save Hook - Automatically save work state
Simplified version that saves locally instead of GitHub
Compliant with official Claude Code hooks documentation
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
                context['files_modified'] = [line.strip() for line in f.readlines()[-10:]]
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
    
    recent_files_file = state_dir / "recent-files.txt"
    
    # Read existing files
    recent_files = []
    if recent_files_file.exists():
        try:
            with open(recent_files_file, 'r') as f:
                recent_files = [line.strip() for line in f.readlines()]
        except:
            pass
    
    # Add new file if not already in list
    if file_path not in recent_files:
        recent_files.append(file_path)
    
    # Keep only last 20 files
    recent_files = recent_files[-20:]
    
    # Write back
    try:
        with open(recent_files_file, 'w') as f:
            for file in recent_files:
                f.write(f"{file}\n")
    except:
        pass

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool info
        tool_name = input_data.get('tool_name', '')
        
        # Only save on write operations
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            sys.exit(0)
        
        # Get file path from tool input
        tool_input = input_data.get('tool_input', {})
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        
        # Update recent files
        if file_path:
            update_recent_files(file_path)
        
        # Save state periodically (every 10th write)
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
            if save_state(state):
                # PostToolUse: stdout shows in transcript mode
                print("Work state saved locally")
            
        # Always exit 0 for success
        sys.exit(0)
        
    except Exception as e:
        # Non-blocking error - show to user
        print(f"State save error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
