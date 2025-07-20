#!/usr/bin/env python3
"""
context-db-awareness - Minimal working version
"""

import json
import sys

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool name - handle multiple formats
        tool_name = input_data.get('tool_name', '')
        if not tool_name and 'tool_use' in input_data:
            tool_name = input_data['tool_use'].get('name', '')
        
        # Extract parameters
        tool_input = input_data.get('tool_input', {})
        if not tool_input and 'tool_use' in input_data:
            tool_input = input_data['tool_use'].get('parameters', {})
        
        # TODO: Add hook-specific logic here
        
        # Always output valid JSON
        sys.exit(0)
        
    except Exception as e:
        # Always output valid JSON even on error
        print(json.dumps({
            sys.exit(0)

if __name__ == '__main__':
    main()
    sys.exit(0)
