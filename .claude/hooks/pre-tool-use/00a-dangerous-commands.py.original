#!/usr/bin/env python3
"""
00a-dangerous-commands - Compliant minimal version
"""

import json
import sys

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool name
        tool_name = input_data.get('tool_name', '')
        
        # TODO: Add hook-specific logic here
        
        # Continue normally
        sys.exit(0)
        
    except Exception as e:
        # Non-blocking error
        print(f"Hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
