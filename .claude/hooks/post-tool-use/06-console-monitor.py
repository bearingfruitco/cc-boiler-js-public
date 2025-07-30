#!/usr/bin/env python3
"""
Console Monitor Hook - Automatically check for browser console errors after changes
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Track console errors over time
CONSOLE_LOG_PATH = Path('.claude/metrics/console-errors.json')

def should_monitor(file_path):
    """Determine if file changes need console monitoring"""
    # UI files that could cause console errors
    ui_patterns = ['.tsx', '.jsx', '.ts', '.js', '.css']
    return any(file_path.endswith(pattern) for pattern in ui_patterns)

def load_error_history():
    """Load historical console error data"""
    if CONSOLE_LOG_PATH.exists():
        try:
            with open(CONSOLE_LOG_PATH, 'r') as f:
                return json.load(f)
        except:
            pass
    return {
        'total_checks': 0,
        'errors_found': 0,
        'common_errors': {},
        'files_with_errors': {}
    }

def save_error_history(history):
    """Save console error history"""
    CONSOLE_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONSOLE_LOG_PATH, 'w') as f:
        json.dump(history, f, indent=2)

def suggest_console_check(file_path, action):
    """Suggest console error check after UI changes"""
    component_name = Path(file_path).stem
    
    suggestions = [
        f"/pw-console - Check for JavaScript errors",
        f"/pw-verify {component_name} - Full browser verification"
    ]
    
    # Load history
    history = load_error_history()
    
    # Check if this file has had errors before
    if file_path in history.get('files_with_errors', {}):
        error_count = history['files_with_errors'][file_path]
        print(f"\n⚠️ This file has had {error_count} console errors before!")
        suggestions.insert(0, "/pw-debug - Debug previous issues")
    
    return suggestions

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract information
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Check if this is a file modification
        if tool_name in ['Write', 'Edit', 'MultiEdit']:
            file_path = tool_input.get('file_path', '')
            
            if file_path and should_monitor(file_path):
                suggestions = suggest_console_check(file_path, tool_name)
                
                if suggestions:
                    print("\n🔍 Console monitoring suggested:")
                    for sugg in suggestions:
                        print(f"   • {sugg}")
                    
                    # Update metrics
                    history = load_error_history()
                    history['total_checks'] += 1
                    save_error_history(history)
        
        # Always exit successfully
        sys.exit(0)
        
    except Exception as e:
        # Log error but don't fail
        print(f"Console monitor hook error: {str(e)}", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
