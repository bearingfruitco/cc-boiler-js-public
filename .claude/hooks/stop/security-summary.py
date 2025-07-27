#!/usr/bin/env python3
"""
Security Summary - Stop Hook
Saves security status when session ends
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
        # TODO: Implement security-summary logic
        
        # For Stop hooks: exit with code 0 to allow stopping
        # Or output {"action": "block", "reason": "..."} to prevent stopping
        sys.exit(0)
        
    except Exception as e:
        # Log error to stderr and still allow stopping
        print(f"security-summary error: {str(e)}", file=sys.stderr)
        sys.exit(0)

if __name__ == '__main__':
    main()
