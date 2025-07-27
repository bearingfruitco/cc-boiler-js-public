#!/usr/bin/env python3
"""
Design System Enforcement Hook - Standards-Based Version
Reads design rules from centralized standards file
Compliant with official Claude Code hooks documentation
"""

import json
import sys
import re
import os

# Cache for standards to avoid repeated file reads
_cached_standards = None

def load_design_standards():
    """Load design standards from centralized file"""
    global _cached_standards
    
    if _cached_standards is not None:
        return _cached_standards
    
    standards_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '../../../.agent-os/standards/design-system.md'
    )
    
    # Fallback to hardcoded if file doesn't exist
    if not os.path.exists(standards_path):
        return get_default_standards()
    
    try:
        with open(standards_path, 'r') as f:
            content = f.read()
            
        # Parse forbidden classes from markdown
        forbidden_sizes = []
        forbidden_weights = []
        valid_spacing = []
        
        # Extract forbidden font sizes
        if '❌ NEVER use:' in content:
            lines = content.split('\n')
            for line in lines:
                if '❌ NEVER use:' in line and 'text-' in line:
                    # Extract text-* classes
                    sizes = re.findall(r'text-\w+', line)
                    forbidden_sizes.extend(sizes)
                elif '❌ NEVER use:' in line and 'font-' in line:
                    # Extract font-* classes
                    weights = re.findall(r'font-\w+', line)
                    forbidden_weights.extend(weights)
        
        # Extract valid spacing values
        if 'Valid Spacing Values' in content:
            # Find the line with valid values
            spacing_match = re.search(r'p-(\d+(?:,\s*p-\d+)*)', content)
            if spacing_match:
                valid_nums = re.findall(r'p-(\d+)', spacing_match.group())
                valid_spacing = [int(n) for n in valid_nums]
        
        # If we didn't find values, use defaults
        if not forbidden_sizes:
            forbidden_sizes = get_default_standards()['forbidden_sizes']
        if not forbidden_weights:
            forbidden_weights = get_default_standards()['forbidden_weights']
        if not valid_spacing:
            valid_spacing = get_default_standards()['valid_spacing']
            
        _cached_standards = {
            'forbidden_sizes': forbidden_sizes,
            'forbidden_weights': forbidden_weights,
            'valid_spacing': valid_spacing
        }
        
        return _cached_standards
        
    except Exception:
        # On any error, fall back to defaults
        return get_default_standards()

def get_default_standards():
    """Hardcoded fallback standards"""
    return {
        'forbidden_sizes': [
            'text-xs', 'text-sm', 'text-base', 'text-lg', 'text-xl', 
            'text-2xl', 'text-3xl', 'text-4xl', 'text-5xl', 'text-6xl'
        ],
        'forbidden_weights': [
            'font-thin', 'font-extralight', 'font-light', 'font-normal',
            'font-medium', 'font-bold', 'font-extrabold', 'font-black'
        ],
        'valid_spacing': [1,2,3,4,6,8,10,12,14,16,20,24,32]
    }

def check_design_violations(content):
    """Check for design system violations"""
    violations = []
    standards = load_design_standards()
    
    # Check for forbidden font sizes
    for size in standards['forbidden_sizes']:
        if size in content:
            violations.append(f"Forbidden font size: {size} (use text-size-[1-4])")
    
    # Check for forbidden font weights
    for weight in standards['forbidden_weights']:
        if weight in content:
            violations.append(f"Forbidden font weight: {weight} (use font-regular or font-semibold)")
    
    # Check for non-grid spacing
    spacing_pattern = r'\b(?:p|m|gap|space-[xy])-(\d+)\b'
    matches = re.findall(spacing_pattern, content)
    
    for match in matches:
        value = int(match)
        if value not in standards['valid_spacing']:
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
            sys.exit(0)
        
        # Extract tool input
        tool_input = input_data.get('tool_input', {})
        
        # Get file path and content
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        content = tool_input.get('content', tool_input.get('new_str', ''))
        
        # Only check component files
        if not any(file_path.endswith(ext) for ext in ['.tsx', '.jsx']):
            sys.exit(0)
        
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
            message += "\n📖 See: .agent-os/standards/design-system.md"
            
            # Block the operation with exit code 2
            # stderr goes to Claude for automatic handling
            print(message, file=sys.stderr)
            sys.exit(2)
        else:
            # No violations - continue normally
            sys.exit(0)
        
    except Exception as e:
        # Non-blocking error - show to user but continue
        print(f"Design check error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
