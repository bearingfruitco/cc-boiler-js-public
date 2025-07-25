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
        
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        content = tool_input.get('content', tool_input.get('new_str', ''))
        
        if not any(file_path.endswith(ext) for ext in ['.tsx', '.jsx']):
            sys.exit(0)
            return
        
        issues = check_hydration_issues(content)
        
        if issues:
            message = "⚠️ NEXT.JS HYDRATION ISSUES\n\n"
            for issue in issues:
                message += f"• {issue}\n"
            
            message += "\n📚 Fix by:\n"
            message += "• Add 'use client' directive\n"
            message += "• Use useEffect for client-only code\n"
            message += "• Call Date().toISOString() for timestamps\n"
            
            print(message)  # Warning shown in transcript
        sys.exit(0)
        else:
            sys.exit(0)
            
    except Exception as e:
if __name__ == "__main__":
    main()
    sys.exit(0)
