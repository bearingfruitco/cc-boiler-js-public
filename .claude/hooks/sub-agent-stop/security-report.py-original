#!/usr/bin/env python3
"""
Security Report - SubAgent Stop Hook
Collects security findings from sub-agents
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
        # TODO: Implement security-report logic
        
        # SubagentStop hooks should just exit with code 0
        sys.exit(1)
        
    except Exception as e:
        # Exit silently even on error
        sys.exit(1)

if __name__ == '__main__':
    main()
