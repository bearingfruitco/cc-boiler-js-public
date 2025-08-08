#!/usr/bin/env python3
"""Hydration Guard - Simplified Version"""

import json
import sys
import re

def check_hydration_issues(content):
    """Check for common Next.js hydration issues"""
    issues = []
    
    # Check for Date() in render
    if re.search(r'new Date\(\)(?!\.toISOString)', content):
        issues.append("Using new Date() without toISOString() can cause hydration errors")
    
    # Check for Math.random() in render
    if 'Math.random()' in content and '"use client"' not in content:
        issues.append("Math.random() in server components causes hydration mismatch")
    
    # Check for window/document access
    if re.search(r'(?:window|document)\.', content) and '"use client"' not in content:
        issues.append("Accessing window/document in server components causes errors")
    
    return issues

def main():
    """Main hook logic"""
    try:
        input_data = json.loads(sys.stdin.read())
        
        tool_name = input_data.get('tool_name', '')
        
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            sys.exit(0)
        
        tool_input = input_data.get('tool_input', {})
        
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        content = tool_input.get('content', tool_input.get('new_str', ''))
        
        if not any(file_path.endswith(ext) for ext in ['.tsx', '.jsx']):
            sys.exit(0)
        
        issues = check_hydration_issues(content)
        
        if issues:
            message = "⚠️ NEXT.JS HYDRATION ISSUES\n\n"
            for issue in issues:
                message += f"• {issue}\n"
            
            message += "\n📚 Fix by:\n"
            message += "• Add 'use client' directive\n"
            message += "• Use useEffect for client-only code\n"
            message += "• Call Date().toISOString() for timestamps\n"
            
            # Print warning to stderr
            print(message, file=sys.stderr)
            sys.exit(0)
        else:
            sys.exit(0)
            
    except Exception as e:
        # On error, exit with non-zero code and error in stderr
        print(f"Hydration guard hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
