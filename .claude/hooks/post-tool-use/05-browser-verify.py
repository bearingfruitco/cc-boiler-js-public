#!/usr/bin/env python3
"""
Browser Verification Hook - Automatically suggest browser testing after UI changes
"""

import json
import sys
import os
from pathlib import Path

# File patterns that should trigger browser verification
UI_FILE_PATTERNS = [
    'components/',
    'app/',
    'pages/',
    '.tsx',
    '.jsx',
    'form',
    'Form',
    'button',
    'Button',
    'modal',
    'Modal'
]

# File patterns to exclude
EXCLUDE_PATTERNS = [
    '.test.',
    '.spec.',
    '.d.ts',
    'types/',
    '__tests__/',
    'node_modules/'
]

def should_verify_in_browser(file_path):
    """Determine if file changes need browser verification"""
    # Check exclusions first
    for pattern in EXCLUDE_PATTERNS:
        if pattern in file_path:
            return False
    
    # Check if it's a UI file
    for pattern in UI_FILE_PATTERNS:
        if pattern in file_path:
            return True
    
    return False

def get_component_name(file_path):
    """Extract component name from file path"""
    path = Path(file_path)
    name = path.stem
    
    # Remove common suffixes
    for suffix in ['.component', '.view', '.page', '.form']:
        if name.endswith(suffix):
            name = name[:-len(suffix)]
    
    return name

def suggest_browser_tests(file_path, action):
    """Generate browser test suggestions based on file type"""
    suggestions = []
    component_name = get_component_name(file_path)
    
    # Component verification
    if 'component' in file_path.lower():
        suggestions.append({
            'command': f'/pw-verify {component_name}',
            'reason': 'Verify component renders correctly'
        })
    
    # Form testing
    if 'form' in file_path.lower():
        suggestions.append({
            'command': f'/pw-form {component_name}',
            'reason': 'Test form submission and validation'
        })
        suggestions.append({
            'command': '/pw-a11y',
            'reason': 'Check form accessibility'
        })
    
    # Page testing
    if '/app/' in file_path or '/pages/' in file_path:
        suggestions.append({
            'command': '/pw-console',
            'reason': 'Check for console errors'
        })
        suggestions.append({
            'command': '/pw-perf',
            'reason': 'Check page performance'
        })
    
    # General suggestions
    suggestions.append({
        'command': '/pw-screenshot',
        'reason': 'Capture visual state'
    })
    
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
            
            if file_path and should_verify_in_browser(file_path):
                suggestions = suggest_browser_tests(file_path, tool_name)
                
                if suggestions:
                    # Output suggestions
                    print("\n🔍 Browser verification recommended:")
                    for i, sugg in enumerate(suggestions[:3], 1):
                        print(f"   {i}. {sugg['command']} - {sugg['reason']}")
                    
                    # Track for metrics
                    metrics_file = Path('.claude/metrics/browser-suggestions.json')
                    metrics_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    try:
                        if metrics_file.exists():
                            with open(metrics_file, 'r') as f:
                                metrics = json.load(f)
                        else:
                            metrics = {'total_suggestions': 0, 'by_file_type': {}}
                        
                        metrics['total_suggestions'] += len(suggestions)
                        file_type = Path(file_path).suffix
                        metrics['by_file_type'][file_type] = metrics['by_file_type'].get(file_type, 0) + 1
                        
                        with open(metrics_file, 'w') as f:
                            json.dump(metrics, f, indent=2)
                    except:
                        pass  # Don't fail hook on metrics error
        
        # Always exit successfully
        sys.exit(1)
        
    except Exception as e:
        # Log error but don't fail
        print(f"Browser verify hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)  # Exit successfully to not block workflow

if __name__ == "__main__":
    main()
