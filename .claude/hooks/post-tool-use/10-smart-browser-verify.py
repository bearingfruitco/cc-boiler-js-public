#!/usr/bin/env python3
"""
Minimal Smart Browser Verification
Only auto-verifies critical UI patterns: forms and click handlers
"""

import json
import sys
import re
from pathlib import Path

# Only these patterns trigger auto-verification
CRITICAL_PATTERNS = [
    r'onClick\s*=',
    r'onSubmit\s*=',
    r'<form',
    r'handleSubmit',
    r'preventDefault\(\)'
]

def main():
    try:
        input_data = json.loads(sys.stdin.read())
        
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Only check file writes/edits
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            sys.exit(0)
            
        file_path = tool_input.get('file_path', '')
        content = tool_input.get('content', '')
        
        # Skip non-UI files
        if not any(ext in file_path for ext in ['.tsx', '.jsx']):
            sys.exit(0)
            
        # Skip test files
        if '.test.' in file_path or '.spec.' in file_path:
            sys.exit(0)
            
        # Check for critical patterns
        found_critical = False
        for pattern in CRITICAL_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                found_critical = True
                break
                
        if found_critical:
            component_name = Path(file_path).stem
            
            # Determine the right command
            if 'form' in file_path.lower():
                command = f"/pw-form {component_name}"
                reason = "Form submission handler detected"
            else:
                command = f"/pw-verify {component_name}"
                reason = "Click handler detected"
                
            print(f"\n🚨 Critical UI change - browser verification required:")
            print(f"   {command} - {reason}")
            print(f"   Run now to catch issues early!\n")
            
        sys.exit(0)
        
    except Exception:
        # Silent fail - never block workflow
        sys.exit(0)

if __name__ == "__main__":
    main()
