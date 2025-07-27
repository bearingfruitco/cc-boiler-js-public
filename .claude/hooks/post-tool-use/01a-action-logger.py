#!/usr/bin/env python3
"""
Action Logger Hook - Logs all tool uses for audit trail
Tracks what tools are used and provides analytics
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def get_safe_summary(tool_name, tool_input, tool_result=None):
    """Get a safe summary of the action without exposing sensitive data"""
    summaries = {
        'Write': lambda: f"Wrote to {tool_input.get('file_path', tool_input.get('path', 'unknown'))}",
        'Edit': lambda: f"Edited {tool_input.get('file_path', tool_input.get('path', 'unknown'))}",
        'MultiEdit': lambda: f"Multi-edited {tool_input.get('file_path', tool_input.get('path', 'unknown'))}",
        'Read': lambda: f"Read {tool_input.get('file_path', tool_input.get('path', 'unknown'))}",
        'Bash': lambda: f"Ran command: {tool_input.get('command', 'unknown')[:50]}...",
        'ListDirectory': lambda: f"Listed {tool_input.get('path', 'unknown')}",
        'SearchFiles': lambda: f"Searched for '{tool_input.get('pattern', 'unknown')}'",
        'Task': lambda: f"Created task: {tool_input.get('title', 'unknown')[:30]}...",
    }
    
    if tool_name in summaries:
        return summaries[tool_name]()
    
    return f"Used tool: {tool_name}"

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool information
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        tool_result = input_data.get('tool_result', {})
        
        # Create log entry
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "tool_name": tool_name,
            "summary": get_safe_summary(tool_name, tool_input, tool_result),
            "success": tool_result.get('success', True) if tool_result else True
        }
        
        # Don't log full details for sensitive operations
        sensitive_patterns = ['.env', 'secret', 'password', 'key', 'token']
        is_sensitive = any(
            pattern in str(tool_input).lower() 
            for pattern in sensitive_patterns
        )
        
        if not is_sensitive:
            # Add more details for non-sensitive operations
            if tool_name == 'Bash':
                log_entry['command'] = tool_input.get('command', '')
            elif tool_name in ['Write', 'Edit', 'Read']:
                log_entry['file_path'] = tool_input.get('file_path', tool_input.get('path', ''))
        
        # Ensure log directory exists
        log_dir = Path(".claude/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Write to daily log file
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = log_dir / f"actions-{today}.jsonl"
        
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        # Also update session summary
        session_file = log_dir / "session-summary.json"
        session_data = {}
        
        if session_file.exists():
            try:
                with open(session_file, "r") as f:
                    session_data = json.load(f)
            except:
                session_data = {}
        
        # Update counters
        if 'tool_usage' not in session_data:
            session_data['tool_usage'] = {}
        
        session_data['tool_usage'][tool_name] = session_data['tool_usage'].get(tool_name, 0) + 1
        session_data['last_activity'] = datetime.now().isoformat()
        
        # Track most used files
        if tool_name in ['Write', 'Edit', 'Read']:
            file_path = tool_input.get('file_path', tool_input.get('path', ''))
            if file_path and not is_sensitive:
                if 'frequent_files' not in session_data:
                    session_data['frequent_files'] = {}
                session_data['frequent_files'][file_path] = session_data['frequent_files'].get(file_path, 0) + 1
        
        with open(session_file, "w") as f:
            json.dump(session_data, f, indent=2)
        
        # PostToolUse hooks should just exit with code 0
        sys.exit(0)
        
    except Exception as e:
        # Log error to stderr and exit
        print(f"Action logger error: {str(e)}", file=sys.stderr)
        sys.exit(0)

if __name__ == '__main__':
    main()
