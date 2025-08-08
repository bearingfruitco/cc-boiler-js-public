#!/usr/bin/env python3
"""
Design System Enforcement Hook - Simplified Version
Ensures all code follows the strict 4-size, 2-weight design system
Compliant with official Claude Code hooks documentation
"""

import json
import sys
import re

def check_design_violations(content):
    """Check for design system violations"""
    violations = []
    
    # Check for forbidden font sizes
    forbidden_sizes = [
        'text-xs', 'text-sm', 'text-base', 'text-lg', 'text-xl', 
        'text-2xl', 'text-3xl', 'text-4xl', 'text-5xl', 'text-6xl'
    ]
    
    for size in forbidden_sizes:
        if size in content:
            violations.append(f"Forbidden font size: {size} (use text-size-[1-4])")
    
    # Check for forbidden font weights
    forbidden_weights = [
        'font-thin', 'font-extralight', 'font-light', 'font-normal',
        'font-medium', 'font-bold', 'font-extrabold', 'font-black'
    ]
    
    for weight in forbidden_weights:
        if weight in content:
            violations.append(f"Forbidden font weight: {weight} (use font-regular or font-semibold)")
    
    # Check for non-grid spacing
    spacing_pattern = r'\b(?:p|m|gap|space-[xy])-(\d+)\b'
    matches = re.findall(spacing_pattern, content)
    
    for match in matches:
        value = int(match)
        # Valid values: 1,2,3,4,6,8,10,12,14,16,20,24,32
        valid = [1,2,3,4,6,8,10,12,14,16,20,24,32]
        if value not in valid:
            violations.append(f"Invalid spacing: {value} (use 4px grid)")
    
    return violations

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool name
        tool_name = input_data.get('tool_name', '')
        
        # Only check write operations
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            print(json.dumps({
            "action": "block",
            "message": json.dumps({"action": "continue"}))
        return
        
        # Extract tool input
        tool_input = input_data.get('tool_input', {})
        
        # Get file path and content
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        content = tool_input.get('content', tool_input.get('new_str', ''))
        
        # Only check component files
        if not any(file_path.endswith(ext) for ext in ['.tsx', '.jsx']):
            print(json.dumps({"action": "continue"}))
        return
        
        # Check for violations
        violations = check_design_violations(content)
        
        if violations:
            message = "🚨 DESIGN SYSTEM VIOLATIONS\n\n"
            for v in violations[:5]:  # Show first 5
                message += f"• {v}\n"
            
            if len(violations) > 5:
                message += f"\n... and {len(violations) - 5} more violations\n"
            
            message += "\n📚 Remember:\n"
            message += "• Font sizes: text-size-1, text-size-2, text-size-3, text-size-4\n"
            message += "• Font weights: font-regular, font-semibold\n"
            message += "• Spacing: 4px grid (p-1, p-2, p-3, p-4, p-6, p-8...)\n"
            
            # Block the operation with exit code 2
            # stderr goes to Claude for automatic handling
            print(message
        }))
        return
        else:
            # No violations - continue normally
            print(json.dumps({"action": "continue"}))
        return
        
    except Exception as e:
        # Non-blocking error - show to user but continue
        print(f"Design check error: {str(e)}", file=sys.stderr)
        print(json.dumps({"action": "continue"}))
        return

if __name__ == "__main__":
    main()
