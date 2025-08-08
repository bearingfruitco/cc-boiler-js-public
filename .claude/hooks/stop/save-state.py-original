#!/usr/bin/env python3
"""
Save State Hook - Saves session state when Claude Code stops
"""

import json
import sys
import os
from pathlib import Path

def main():
    """Main hook logic"""
    try:
        # Read input if provided
        input_data = {}
        if not sys.stdin.isatty():
            try:
                input_data = json.loads(sys.stdin.read())
            except:
                pass
        
        # Hook-specific logic goes here
        # TODO: Implement save-state logic
        
        # For Stop hooks: exit with code 0 to allow stopping
        # Or exit with code 2 and message to stderr to block
        sys.exit(0)
        
    except Exception as e:
        # Log error to stderr (non-blocking error)
        print(f"save-state error: {str(e)}", file=sys.stderr)
        sys.exit(1)  # Non-blocking error

if __name__ == '__main__':
    main()
