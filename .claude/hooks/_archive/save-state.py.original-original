#!/usr/bin/env python3
"""
Save State Hook - Saves session state when Claude Code stops
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def extract_key_info(transcript):
    """Extract key information from the session transcript"""
    if not transcript:
        return {}
    
    # Basic analysis of the transcript
    lines = transcript.split('\n')
    
    # Count different types of activities
    files_edited = set()
    commands_run = []
    errors_encountered = 0
    
    for line in lines:
        # Look for file operations
        if 'Wrote to' in line or 'Edited' in line:
            parts = line.split()
            for part in parts:
                if '/' in part and '.' in part:
                    files_edited.add(part.strip())
        
        # Look for bash commands
        if '$ ' in line:
            command = line.split('$ ', 1)[-1].strip()
            if command:
                commands_run.append(command[:100])  # Truncate long commands
        
        # Look for errors
        if 'error' in line.lower() or 'failed' in line.lower():
            errors_encountered += 1
    
    return {
        "files_edited": list(files_edited)[:10],  # Limit to 10 files
        "commands_run": commands_run[:10],  # Limit to 10 commands
        "errors_encountered": errors_encountered,
        "total_lines": len(lines)
    }

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract transcript and check if already in stop hook
        transcript = input_data.get('transcript', '')
        stop_hook_active = input_data.get('stop_hook_active', False)
        
        # Don't save state if we're already in a stop hook loop
        if stop_hook_active:
            sys.exit(0)
            return
        
        # Create state data
        state_data = {
            "timestamp": datetime.now().isoformat(),
            "session_info": extract_key_info(transcript),
            "stop_hook_active": stop_hook_active
        }
        
        # Ensure directories exist
        state_dir = Path(".claude/state")
        state_dir.mkdir(parents=True, exist_ok=True)
        
        # Save current state
        state_file = state_dir / "last-session.json"
        with open(state_file, "w") as f:
            json.dump(state_data, f, indent=2)
        
        # Also append to history
        history_file = state_dir / "session-history.jsonl"
        with open(history_file, "a") as f:
            f.write(json.dumps(state_data) + "\n")
        
        # Check if we should remind about unfinished work
        session_info = state_data['session_info']
        if session_info.get('errors_encountered', 0) > 0:
            # There were errors - might want to continue
            print(json.dumps({
                sys.exit(0)
        else:
            # Clean session
            sys.exit(0)
        
    except Exception as e:
        # Always output valid JSON even on error
        print(json.dumps({
            sys.exit(0)

if __name__ == '__main__':
    main()
    sys.exit(0)
