#!/usr/bin/env python3
"""
Command Logger - Structured logging of all Claude commands for analytics
Tracks command usage, duration, success/failure, and enables querying
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def extract_command_info(tool_name, tool_input):
    """Extract command information from tool use data"""
    # Use the official spec parameters
    
    # Handle Bash commands (official tool name)
    if tool_name == 'Bash':
        command = tool_input.get('command', '')
        if command.startswith('/'):
            # It's a Claude command
            parts = command.split()
            return {
                'type': 'claude_command',
                'command': parts[0],
                'args': parts[1:] if len(parts) > 1 else [],
                'full_command': command
            }
    
    # Handle file operations (official tool names)
    if tool_name in ['Write', 'Edit', 'Read', 'MultiEdit']:
        return {
            'type': 'file_operation',
            'command': tool_name,
            'args': [tool_input.get('file_path', '')],
            'full_command': f"{tool_name} {tool_input.get('file_path', '')}"
        }
    
    # Handle other tools
    return {
        'type': 'tool',
        'command': tool_name,
        'args': list(tool_input.values()) if tool_input else [],
        'full_command': f"{tool_name} {json.dumps(tool_input)}"
    }

def extract_changed_files(tool_name, tool_input, tool_result):
    """Extract list of files changed by the command"""
    # Use official spec parameters
    
    changed_files = []
    
    if tool_name in ['Write', 'Edit', 'MultiEdit']:
        file_path = tool_input.get('file_path', '')
        if file_path:
            changed_files.append(file_path)
    
    # For Bash commands, try to parse output for file changes
    if tool_name == 'Bash' and tool_result:
        output = tool_result.get('output', '')
        
        # Look for common patterns indicating file changes
        import re
        file_patterns = [
            r'created?\s+([^\s]+\.[a-zA-Z]+)',
            r'modified?\s+([^\s]+\.[a-zA-Z]+)',
            r'wrote?\s+to\s+([^\s]+\.[a-zA-Z]+)',
            r'Generated?\s+([^\s]+\.[a-zA-Z]+)'
        ]
        
        for pattern in file_patterns:
            matches = re.findall(pattern, output, re.IGNORECASE)
            changed_files.extend(matches)
    
    return list(set(changed_files))  # Remove duplicates

def calculate_duration(tool_result):
    """Calculate command duration if available"""
    # Look for timing information in result
    duration_ms = 0
    if tool_result:
        duration_ms = tool_result.get('duration_ms', 0)
    return duration_ms

def update_command_stats(command_name, log_entry):
    """Maintain quick statistics for common queries"""
    stats_file = Path(".claude/logs/commands/stats.json")
    
    stats = {}
    if stats_file.exists():
        try:
            with open(stats_file) as f:
                stats = json.load(f)
        except:
            stats = {}
    
    # Initialize command stats if needed
    if command_name not in stats:
        stats[command_name] = {
            'count': 0,
            'total_duration': 0,
            'success_count': 0,
            'error_count': 0,
            'last_used': None,
            'first_used': log_entry['timestamp'],
            'files_changed_count': 0
        }
    
    # Update stats
    cmd_stats = stats[command_name]
    cmd_stats['count'] += 1
    cmd_stats['total_duration'] += log_entry['duration']
    cmd_stats['last_used'] = log_entry['timestamp']
    
    if log_entry['status'] == 'success':
        cmd_stats['success_count'] += 1
    elif log_entry['status'] == 'error':
        cmd_stats['error_count'] += 1
    
    # Track files changed
    if log_entry['files_changed']:
        cmd_stats['files_changed_count'] += len(log_entry['files_changed'])
    
    # Calculate averages
    if cmd_stats['count'] > 0:
        cmd_stats['avg_duration'] = cmd_stats['total_duration'] / cmd_stats['count']
        cmd_stats['success_rate'] = (cmd_stats['success_count'] / cmd_stats['count']) * 100
    
    # Save updated stats
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)

def main():
    """Main hook logic for command logging"""
    try:
        # Read input according to official spec
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool information according to official spec
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        tool_result = input_data.get('tool_result', {})  # PostToolUse gets result
        
        if not tool_name:
            sys.exit(0)  # Exit success if no tool
        
        # Extract command information
        cmd_info = extract_command_info(tool_name, tool_input)
        
        # Only log Claude commands and important operations
        if cmd_info['type'] not in ['claude_command', 'file_operation']:
            sys.exit(0)

        status = 'unknown'
        error = None
        
        if tool_result:
            if 'error' in tool_result:
                status = 'error'
                error = tool_result['error']
            elif tool_result.get('success', False) or tool_result.get('output'):
                status = 'success'
        
        # Create log entry
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'session_id': input_data.get('session_id', os.environ.get('CLAUDE_SESSION_ID', 'unknown')),
            'command_type': cmd_info['type'],
            'command': cmd_info['command'],
            'args': cmd_info['args'],
            'full_command': cmd_info['full_command'],
            'status': status,
            'duration': calculate_duration(tool_result),
            'files_changed': extract_changed_files(tool_name, tool_input, tool_result),
            'error': error,
            'user': os.environ.get('USER', 'unknown')
        }
        
        # Ensure log directory exists
        log_dir = Path(".claude/logs/commands")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Save to daily log file (JSON Lines format)
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = log_dir / f"{today}.jsonl"
        
        try:
            with open(log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            # Don't fail the hook chain
            pass
        
        # Update statistics
        try:
            update_command_stats(cmd_info['command'], log_entry)
        except Exception as e:
            # Don't fail the hook chain
            pass
        
        # PostToolUse hooks exit with success
        sys.exit(0)
        
    except Exception as e:
        # Log error to stderr and exit
        print(f"Command logger error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
