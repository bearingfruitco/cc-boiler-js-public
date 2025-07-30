#!/usr/bin/env python3
"""
Auto Browser Verification Enhancement
Makes browser checking fully automatic
"""

import json
import sys
import os
import subprocess
from pathlib import Path

def should_auto_verify(file_path):
    """Check if file should trigger automatic browser verification"""
    ui_patterns = ['components/', '.tsx', '.jsx', 'app/', 'pages/']
    exclude = ['.test.', '.spec.', 'node_modules']
    
    # Check exclusions
    if any(ex in file_path for ex in exclude):
        return False
    
    # Check if it's a UI file
    return any(pattern in file_path for pattern in ui_patterns)

def auto_invoke_playwright(file_path, action):
    """Automatically invoke playwright verification"""
    component_name = Path(file_path).stem
    
    # Determine the appropriate command
    if 'form' in file_path.lower():
        command = f"use playwright-specialist subagent to verify the form {component_name} renders correctly and all interactions work"
    elif 'button' in file_path.lower() or 'component' in file_path.lower():
        command = f"use playwright-specialist subagent to verify {component_name} renders without console errors"
    else:
        command = f"use playwright-specialist subagent to check the browser console for errors after changes to {file_path}"
    
    # Return the command to be injected
    return {
        "auto_command": command,
        "priority": "high",
        "reason": f"Automatic browser verification after {action} to {file_path}"
    }

def main():
    """Main hook logic"""
    try:
        input_data = json.loads(sys.stdin.read())
        
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Check if this is a file modification
        if tool_name in ['Write', 'Edit', 'MultiEdit']:
            file_path = tool_input.get('file_path', '')
            
            if file_path and should_auto_verify(file_path):
                result = auto_invoke_playwright(file_path, tool_name)
                
                # Output the automatic command
                output = {
                    "continue": True,
                    "inject_command": result["auto_command"],
                    "message": f"🤖 Auto-verifying in browser: {result['reason']}"
                }
                
                print(json.dumps(output))
                sys.exit(0)
        
        # Continue normally if no auto-verification needed
        sys.exit(0)
        
    except Exception as e:
        print(f"Auto-verify error: {str(e)}", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
