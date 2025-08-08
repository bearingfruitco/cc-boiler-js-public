#!/usr/bin/env python3
"""
Design System Enforcement Hook - Block non-compliant code before it's written
Ensures all code follows the strict 4-size, 2-weight design system
UPDATED TO FOLLOW OFFICIAL CLAUDE CODE HOOKS SPECIFICATION
"""

import json
import sys
import re
from pathlib import Path

def is_component_file(file_path):
    """Check if this is a component file that needs design validation"""
    component_extensions = ['.tsx', '.jsx', '.vue', '.svelte']
    ignore_paths = ['node_modules', '.next', 'dist', 'build', '.test.', '.spec.']
    
    # Check if it's a component file
    if not any(file_path.endswith(ext) for ext in component_extensions):
        return False
    
    # Ignore certain paths
    if any(ignore in file_path for ignore in ignore_paths):
        return False
    
    return True

def find_design_violations(content):
    """Find design system violations in the content"""
    violations = []
    
    # Check for forbidden font sizes (must use text-size-1 through text-size-4)
    forbidden_sizes = r'(?:className|class)=["\'][^"\']*\b(?:text-(?:xs|sm|base|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl))\b'
    for match in re.finditer(forbidden_sizes, content):
        line_num = content[:match.start()].count('\n') + 1
        violations.append(f"Line {line_num}: Forbidden font size. Use text-size-[1-4] instead")
    
    # Check for forbidden font weights (must use font-regular or font-semibold)
    forbidden_weights = r'(?:className|class)=["\'][^"\']*\b(?:font-(?:thin|extralight|light|normal|medium|bold|extrabold|black))\b'
    for match in re.finditer(forbidden_weights, content):
        line_num = content[:match.start()].count('\n') + 1
        violations.append(f"Line {line_num}: Forbidden font weight. Use font-regular or font-semibold")
    
    # Check for non-4px grid spacing
    spacing_pattern = r'(?:className|class)=["\'][^"\']*\b(?:p|m|gap|space-[xy])-(\d+)\b'
    valid_spacing = [1, 2, 3, 4, 6, 8, 10, 12, 14, 16, 20, 24, 28, 32]
    
    for match in re.finditer(spacing_pattern, content):
        value = int(match.group(1))
        if value not in valid_spacing:
            line_num = content[:match.start()].count('\n') + 1
            violations.append(f"Line {line_num}: Invalid spacing '{value}'. Use 4px grid values")
    
    # Check for small touch targets
    touch_pattern = r'<(?:button|a|Button|Link)[^>]*(?:className|class)=["\'][^"\']*\b(?:h|height)-(\d+)\b'
    for match in re.finditer(touch_pattern, content, re.IGNORECASE):
        height = int(match.group(1))
        if height < 11:  # h-11 = 44px minimum
            line_num = content[:match.start()].count('\n') + 1
            violations.append(f"Line {line_num}: Touch target too small. Use h-11 (44px) minimum")
    
    return violations

def main():
    """Main hook logic following official specification"""
    try:
        # Read input from stdin (official format)
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool information
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Only check write operations (official tool names)
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            sys.exit(0)  # Success - continue
        
        # Get file path and content
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        content = tool_input.get('content', '')
        if 'new_str' in tool_input:  # Edit operations
            content = tool_input.get('new_str', '')
        
        # Skip if not a component file
        if not is_component_file(file_path):
            sys.exit(0)  # Not a component file - continue
        
        # Check for violations
        violations = find_design_violations(content)
        
        if violations:
            # Block with detailed message using official format
            error_msg = "🚫 Design System Violations Found\n\n"
            error_msg += "Your code must follow the strict design system:\n"
            error_msg += "• Font sizes: ONLY text-size-[1-4]\n"
            error_msg += "• Font weights: ONLY font-regular, font-semibold\n"
            error_msg += "• Spacing: ONLY 4px grid (1=4px, 2=8px, etc)\n"
            error_msg += "• Touch targets: Minimum h-11 (44px)\n\n"
            error_msg += "Violations found:\n"
            for v in violations:
                error_msg += f"• {v}\n"
            
            # OFFICIAL FORMAT: stderr + exit code 2 for blocking
            print(error_msg, file=sys.stderr)
            sys.exit(2)  # Block operation
        
        # No violations - continue
        sys.exit(0)
        
    except Exception as e:
        # Non-blocking error - show to user but continue
        print(f"Design check hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)  # Non-blocking error

if __name__ == '__main__':
    main()
