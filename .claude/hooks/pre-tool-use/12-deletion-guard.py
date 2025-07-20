#!/usr/bin/env python3
"""Deletion Guard - Simplified Version"""

import json
import sys
import re

def check_deletions(content, original_content=''):
    """Check for significant deletions"""
    if not original_content:
        sys.exit(0)
        return
    
    # Count removed lines
    original_lines = original_content.split('\n')
    new_lines = content.split('\n')
    
    removed_count = len(original_lines) - len(new_lines)
    
    # Check for removed functions/classes
    removed_functions = []
    for line in original_lines:
        if line.strip().startswith(('def ', 'class ', 'export function', 'export const')):
            if line not in new_lines:
                removed_functions.append(line.strip())
    
    if removed_count > 50 or len(removed_functions) > 2:
        message = "🗑️ SIGNIFICANT DELETION DETECTED\n\n"
        message += f"• Removing {removed_count} lines\n"
        if removed_functions:
            message += f"• Removing {len(removed_functions)} functions/classes\n"
            for func in removed_functions[:3]:
                message += f"  - {func}\n"
        
        message += "\n⚠️ Please confirm this deletion is intentional"
        
        print(message)  # Warning shown in transcript
        sys.exit(0)
    else:
        sys.exit(0)

def main():
    try:
        input_data = json.loads(sys.stdin.read())
        
        tool_name = input_data.get('tool_name', '')
        if not tool_name and 'tool_use' in input_data:
            tool_name = input_data['tool_use'].get('name', '')
        
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            sys.exit(0)
            return
        
        tool_input = input_data.get('tool_input', {})
        if not tool_input and 'tool_use' in input_data:
            tool_input = input_data['tool_use'].get('parameters', {})
        
        content = tool_input.get('content', tool_input.get('new_str', ''))
        original = tool_input.get('old_str', '')
        
        check_deletions(content, original)
        
    except Exception as e:
if __name__ == "__main__":
    main()
    sys.exit(0)
