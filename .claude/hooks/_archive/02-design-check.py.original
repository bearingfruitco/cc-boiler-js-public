#!/usr/bin/env python3
"""
Design System Enforcement Hook - Block non-compliant code before it's written
Enhanced with Suggestion Engine for educational feedback
Ensures all code follows the strict 4-size, 2-weight design system
"""

import json
import sys
import os
import re
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from utils.suggestion_engine import SuggestionEngine
    USE_SUGGESTION_ENGINE = True
except ImportError:
    USE_SUGGESTION_ENGINE = False

def get_config():
    """Load hook configuration"""
    config_path = Path(__file__).parent.parent / 'config.json'
    try:
        with open(config_path) as f:
            return json.load(f)
    except:
        return {}

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

def find_violations_legacy(content, config):
    """Legacy violation detection (fallback when suggestion engine not available)"""
    violations = {
        'critical': [],
        'warnings': []
    }
    
    design_rules = config.get('design_system', config.get('designSystem', {}))
    
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
    spacing_rules = design_rules.get('rules', {}).get('spacing', {})
    spacing_grid = spacing_rules.get('grid', 4)
    
    spacing_pattern = r'(?:className|class)=["\'][^"\']*\b(?:p|m|gap|space-[xy])-(\d+)\b'
    for match in re.finditer(spacing_pattern, content):
        value = int(match.group(1))
        # Convert Tailwind units: 1 = 4px, 2 = 8px, etc.
        pixel_value = value * 4
        if value not in [1, 2, 3, 4, 6, 8, 10, 12, 14, 16, 20, 24, 32]:
            violations['critical'].append({
                'type': 'spacing',
                'line': content[:match.start()].count('\n') + 1,
                'match': match.group(),
                'value': value,
                'fix': suggest_spacing_fix(value)
            })
    
    # Check for small touch targets (buttons, links)
    mobile_rules = design_rules.get('rules', {}).get('mobile', {})
    min_touch_target = mobile_rules.get('minTouchTarget', 44)
    
    touch_pattern = r'<(?:button|a|Button|Link)[^>]*(?:className|class)=["\'][^"\']*\b(?:h|height)-(\d+)\b'
    for match in re.finditer(touch_pattern, content, re.IGNORECASE):
        height = int(match.group(1)) * 4  # Tailwind units to pixels
        if height < min_touch_target:
            violations['warnings'].append({
                'type': 'touch-target',
                'line': content[:match.start()].count('\n') + 1,
                'match': match.group(),
                'current': height,
                'minimum': min_touch_target
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
    # Valid Tailwind spacing values that follow 4px grid
    valid_values = [1, 2, 3, 4, 6, 8, 10, 12, 14, 16, 20, 24, 32]
    
    # Find nearest valid value
    closest = min(valid_values, key=lambda x: abs(x - value))
    return closest

def format_violations_message_legacy(violations):
    """Format violations into a readable message (legacy)"""
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
                    message += f"    → Use: p-{v['fix']} or m-{v['fix']}\n"
        
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
    message += "  • Spacing: p-1, p-2, p-3, p-4, p-6, p-8 (4px grid)\n"
    message += "  • Touch targets: minimum 44px (h-11)\n"
    
    return message

def main():
    """Main hook logic with enhanced suggestion engine"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool name - handle multiple formats
        tool_name = input_data.get('tool_name', '')
        if not tool_name and 'tool_use' in input_data:
            tool_name = input_data['tool_use'].get('name', '')
        
        # Only process file write operations
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            sys.exit(0)
            return
        
        # Extract parameters
        tool_input = input_data.get('tool_input', {})
        if not tool_input and 'tool_use' in input_data:
            tool_input = input_data['tool_use'].get('parameters', {})
        
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        
        # Only validate component files
        if not is_component_file(file_path):
            sys.exit(0)
            return
        
        # Get configuration
        config = get_config()
        content = tool_input.get('content', tool_input.get('new_str', ''))
        
        # Skip if no content
        if not content:
            sys.exit(0)
            return
        
        # Use suggestion engine if enabled
        if USE_SUGGESTION_ENGINE and config.get('features', {}).get('suggestion_engine', True):
            try:
                engine = SuggestionEngine()
                violations = engine.find_violations(content, file_path)
                
                if violations:
                    # Format message with suggestions
                    message = "🚨 DESIGN SYSTEM VIOLATIONS DETECTED\n"
                    message += f"\n📍 Found {len(violations)} violation(s) in {file_path}\n"
                    
                    # Show first few violations
                    for v in violations[:5]:
                        message += f"\n• Line {v.get('line', '?')}: {v.get('type', 'violation')}\n"
                        message += f"  Current: {v.get('matched_text', '')}\n"
                        message += f"  Fix: {v.get('suggestion', '')}\n"
                    
                    if len(violations) > 5:
                        message += f"\n... and {len(violations) - 5} more violations\n"
                    
                    # Add design rules reminder
                    message += "\n📚 Remember:\n"
                    message += "  • Font sizes: text-size-[1-4] only\n"
                    message += "  • Font weights: font-regular, font-semibold only\n"
                    message += "  • Spacing: 4px grid (p-1, p-2, p-3, p-4, p-6, p-8...)\n"
                    
                    print(message
                    , file=sys.stderr)
        sys.exit(2)
                    return
            except Exception as e:
                # If suggestion engine fails, fall back to legacy
                pass
        
        # Fallback to legacy violation detection
        violations = find_violations_legacy(content, config)
        
        if violations['critical'] or violations['warnings']:
            message = format_violations_message_legacy(violations)
            print(message
            , file=sys.stderr)
        sys.exit(2)
        else:
            # No violations - continue
            sys.exit(0)
    
    except Exception as e:
        # On any error, output valid JSON to continue
        print(json.dumps({
            sys.exit(0)

if __name__ == "__main__":
    main()
    sys.exit(0)
