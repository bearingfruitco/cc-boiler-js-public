#!/usr/bin/env python3
"""
Design System Enforcement Hook - Block non-compliant code before it's written
Ensures all code follows the strict 4-size, 2-weight design system
"""

import json
import sys
import re
from pathlib import Path

def get_config():
    """Load hook configuration"""
    config_path = Path(__file__).parent.parent / 'config.json'
    with open(config_path) as f:
        return json.load(f)

def is_component_file(file_path):
    """Check if this is a component file that needs design validation"""
    component_extensions = ['.tsx', '.jsx', '.vue', '.svelte']
    ignore_paths = ['node_modules', '.next', 'dist', 'build']
    
    # Check if it's a component file
    if not any(file_path.endswith(ext) for ext in component_extensions):
        return False
    
    # Ignore certain paths
    if any(ignore in file_path for ignore in ignore_paths):
        return False
    
    return True

def find_violations(content, config):
    """Find all design system violations in the content"""
    violations = {
        'critical': [],
        'warnings': []
    }
    
    design_rules = config['design_system']
    
    # Check for forbidden font sizes
    forbidden_sizes = r'(?:className|class)=["\'][^"\']*\b(?:text-(?:xs|sm|base|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl))\b'
    for match in re.finditer(forbidden_sizes, content):
        violations['critical'].append({
            'type': 'font-size',
            'line': content[:match.start()].count('\n') + 1,
            'match': match.group(),
            'fix': suggest_font_size_fix(match.group())
        })
    
    # Check for forbidden font weights
    forbidden_weights = r'(?:className|class)=["\'][^"\']*\b(?:font-(?:thin|extralight|light|normal|medium|bold|extrabold|black))\b'
    for match in re.finditer(forbidden_weights, content):
        violations['critical'].append({
            'type': 'font-weight',
            'line': content[:match.start()].count('\n') + 1,
            'match': match.group(),
            'fix': suggest_font_weight_fix(match.group())
        })
    
    # Check for non-grid spacing
    spacing_pattern = r'(?:className|class)=["\'][^"\']*\b(?:p|m|gap|space-[xy])-(\d+)\b'
    for match in re.finditer(spacing_pattern, content):
        value = int(match.group(1))
        if value % design_rules['spacing_grid'] != 0:
            violations['critical'].append({
                'type': 'spacing',
                'line': content[:match.start()].count('\n') + 1,
                'match': match.group(),
                'value': value,
                'fix': suggest_spacing_fix(value)
            })
    
    # Check for small touch targets (buttons, links)
    touch_pattern = r'<(?:button|a|Button|Link)[^>]*(?:className|class)=["\'][^"\']*\b(?:h|height)-(\d+)\b'
    for match in re.finditer(touch_pattern, content, re.IGNORECASE):
        height = int(match.group(1)) * 4  # Tailwind units to pixels
        if height < design_rules['min_touch_target']:
            violations['warnings'].append({
                'type': 'touch-target',
                'line': content[:match.start()].count('\n') + 1,
                'match': match.group(),
                'current': height,
                'minimum': design_rules['min_touch_target']
            })
    
    return violations

def suggest_font_size_fix(match):
    """Suggest replacement for forbidden font size"""
    size_map = {
        'text-xs': 'text-size-4',
        'text-sm': 'text-size-4',
        'text-base': 'text-size-3',
        'text-lg': 'text-size-2',
        'text-xl': 'text-size-2',
        'text-2xl': 'text-size-1',
        'text-3xl': 'text-size-1',
        'text-4xl': 'text-size-1',
        'text-5xl': 'text-size-1',
        'text-6xl': 'text-size-1'
    }
    
    for old, new in size_map.items():
        if old in match:
            return match.replace(old, new)
    
    return match

def suggest_font_weight_fix(match):
    """Suggest replacement for forbidden font weight"""
    weight_map = {
        'font-thin': 'font-regular',
        'font-extralight': 'font-regular',
        'font-light': 'font-regular',
        'font-normal': 'font-regular',
        'font-medium': 'font-semibold',
        'font-bold': 'font-semibold',
        'font-extrabold': 'font-semibold',
        'font-black': 'font-semibold'
    }
    
    for old, new in weight_map.items():
        if old in match:
            return match.replace(old, new)
    
    return match

def suggest_spacing_fix(value):
    """Suggest nearest valid spacing value"""
    grid = 4
    if value % grid == 0:
        return value
    
    # Find nearest multiple of 4
    lower = (value // grid) * grid
    upper = lower + grid
    
    # Return closer value
    if value - lower < upper - value:
        return lower
    return upper

def auto_fix_content(content, violations):
    """Automatically fix violations in content"""
    fixed_content = content
    
    # Sort violations by line number in reverse to avoid offset issues
    all_violations = violations['critical'] + violations['warnings']
    sorted_violations = sorted(all_violations, key=lambda v: v['line'], reverse=True)
    
    for violation in sorted_violations:
        if 'fix' in violation:
            if isinstance(violation['fix'], str):
                # Direct string replacement
                fixed_content = fixed_content.replace(violation['match'], violation['fix'])
            elif isinstance(violation['fix'], int):
                # Spacing fix
                old_class = f"-{violation['value']}"
                new_class = f"-{violation['fix'] // 4}"  # Convert back to Tailwind units
                fixed_content = fixed_content.replace(old_class, new_class)
    
    return fixed_content

def format_violations_message(violations):
    """Format violations into a readable message"""
    if not violations['critical'] and not violations['warnings']:
        return None
    
    message = "🚨 DESIGN SYSTEM VIOLATIONS DETECTED\n\n"
    
    if violations['critical']:
        message += "❌ CRITICAL (must fix):\n"
        for v in violations['critical'][:5]:  # Show first 5
            message += f"  Line {v['line']}: {v['type']} - {v['match']}\n"
            if 'fix' in v:
                if isinstance(v['fix'], str):
                    message += f"    → Fix: {v['fix']}\n"
                elif v['type'] == 'spacing':
                    message += f"    → Use: {v['fix'] // 4} (multiple of 4)\n"
        
        if len(violations['critical']) > 5:
            message += f"  ... and {len(violations['critical']) - 5} more\n"
    
    if violations['warnings']:
        message += "\n⚠️ WARNINGS:\n"
        for v in violations['warnings'][:3]:
            if v['type'] == 'touch-target':
                message += f"  Line {v['line']}: Touch target only {v['current']}px (min: {v['minimum']}px)\n"
    
    message += "\n📚 Design Rules:\n"
    message += "  • Font sizes: text-size-1, text-size-2, text-size-3, text-size-4\n"
    message += "  • Font weights: font-regular, font-semibold\n"
    message += "  • Spacing: multiples of 4 (p-1, p-2, p-3, p-4, p-6, p-8...)\n"
    message += "  • Touch targets: minimum 44px (h-11)\n"
    
    return message

def main():
    """Main hook logic"""
    # Read input from Claude Code
    input_data = json.loads(sys.stdin.read())
    
    # Only process file write operations
    if input_data['tool'] not in ['write_file', 'edit_file', 'str_replace']:
        print(json.dumps({"action": "continue"}))
        return
    
    file_path = input_data.get('path', '')
    
    # Only validate component files
    if not is_component_file(file_path):
        print(json.dumps({"action": "continue"}))
        return
    
    config = get_config()
    content = input_data.get('content', '')
    
    # Find violations
    violations = find_violations(content, config)
    
    if violations['critical'] or violations['warnings']:
        # Auto-fix if enabled
        if config['design_system']['auto_fix']:
            fixed_content = auto_fix_content(content, violations)
            
            # Create response
            response = {
                "action": "suggest_fix",
                "message": format_violations_message(violations),
                "original_content": content,
                "fixed_content": fixed_content,
                "fix_description": f"Auto-fixed {len(violations['critical'])} critical violations"
            }
            
            # If only warnings, allow but notify
            if not violations['critical']:
                response["action"] = "warn"
                response["continue"] = True
            
            print(json.dumps(response))
        else:
            # Block with violations message
            print(json.dumps({
                "action": "block",
                "message": format_violations_message(violations),
                "violations": violations
            }))
    else:
        # No violations - continue
        print(json.dumps({"action": "continue"}))

if __name__ == "__main__":
    main()
