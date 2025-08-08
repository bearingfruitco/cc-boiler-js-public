#!/usr/bin/env python3
"""
Dependency Tracker Hook - Track component usage with @used-by comments
Compliant with official Claude Code hooks documentation
"""

import json
import sys
import re
import subprocess
from pathlib import Path

def extract_component_name(file_path):
    """Extract component name from file path"""
    path = Path(file_path)
    
    # Handle index files
    if path.stem == 'index':
        return path.parent.name
    
    return path.stem

def get_used_by_comment(component_name, usage_file):
    """Generate @used-by comment"""
    return f"// @used-by {usage_file}"

def check_existing_used_by(content, usage_file):
    """Check if used-by comment already exists"""
    pattern = rf'//\s*@used-by\s+{re.escape(usage_file)}'
    return bool(re.search(pattern, content))

def find_component_file(component_name, import_path=None):
    """Find the actual component file"""
    
    # If we have an import path, try to resolve it
    if import_path:
        if import_path.startswith('@/'):
            # Resolve @ alias
            possible_path = import_path[2:]
            
            # Check with various extensions
            for ext in ['.tsx', '.ts', '.jsx', '.js', '/index.tsx', '/index.ts']:
                file_path = Path(possible_path + ext)
                if file_path.exists():
                    return str(file_path)
        
        elif import_path.startswith('./') or import_path.startswith('../'):
            # Relative import - would need calling file context
            pass
    
    # Fallback: search for component
    search_paths = ['components', 'app', 'lib', 'src/components']
    
    for base_path in search_paths:
        if not Path(base_path).exists():
            continue
        
        # Search for the component file
        cmd = f"find {base_path} -name '{component_name}.tsx' -o -name '{component_name}.ts' -o -name '{component_name}.jsx' -o -name '{component_name}.js' 2>/dev/null | head -1"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.stdout.strip():
            return result.stdout.strip()
    
    return None

def extract_imports(content):
    """Extract imported components from file content"""
    imports = []
    
    # Match import statements
    import_patterns = [
        # import { Component } from './path'
        r'import\s+{([^}]+)}\s+from\s+[\'"]([^\'"]+)[\'"]',
        # import Component from './path'
        r'import\s+(\w+)\s+from\s+[\'"]([^\'"]+)[\'"]',
    ]
    
    for pattern in import_patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            if isinstance(match[0], str) and '{' not in match[0]:
                # Default import
                imports.append({
                    'name': match[0],
                    'path': match[1]
                })
            else:
                # Named imports
                names = match[0].split(',')
                for name in names:
                    name = name.strip()
                    if name:
                        imports.append({
                            'name': name,
                            'path': match[1]
                        })
    
    return imports

def extract_component_usage(content):
    """Extract component usage from JSX"""
    # Find JSX component usage
    pattern = r'<(\w+)[\s/>]'
    matches = re.findall(pattern, content)
    
    # Filter out HTML elements
    html_elements = {
        'div', 'span', 'p', 'a', 'button', 'input', 'form', 'h1', 'h2', 'h3', 
        'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'table', 'tr', 'td', 'th', 'img',
        'header', 'footer', 'main', 'section', 'article', 'nav', 'aside'
    }
    
    components = []
    for match in matches:
        if match[0].isupper() and match.lower() not in html_elements:
            components.append(match)
    
    return list(set(components))

def update_dependency_tracking(file_path, content):
    """Update @used-by comments in imported components"""
    updates_needed = []
    
    # Extract imports
    imports = extract_imports(content)
    
    # Extract component usage
    used_components = extract_component_usage(content)
    
    # Match imports to usage
    for imp in imports:
        component_name = imp['name']
        import_path = imp['path']
        
        # Check if this component is used
        if component_name in used_components:
            # Find the component file
            component_file = find_component_file(component_name, import_path)
            
            if component_file:
                updates_needed.append({
                    'component': component_name,
                    'file': component_file,
                    'used_by': file_path
                })
    
    return updates_needed

def main():
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool information
        tool_name = input_data.get('tool_name', '')
        
        # Only process write operations
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            # Not a write operation - continue normally
            sys.exit(0)
        
        # Extract tool input
        tool_input = input_data.get('tool_input', {})
        
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        content = tool_input.get('content', tool_input.get('new_str', ''))
        
        # Only check TS/JS files
        if not any(file_path.endswith(ext) for ext in ['.ts', '.tsx', '.js', '.jsx']):
            # Not a JS/TS file - continue normally
            sys.exit(0)
        
        # Find components that need dependency tracking
        updates_needed = update_dependency_tracking(file_path, content)
        
        if updates_needed:
            # Format informational message
            info_msg = f"📊 Dependency Tracking: Found {len(updates_needed)} component dependencies\n\n"
            
            for update in updates_needed:
                info_msg += f"  • {update['component']} ({update['file']})\n"
                info_msg += f"    Used by: {update['used_by']}\n"
            
            info_msg += "\nConsider updating these components with @used-by comments\n"
            info_msg += "to track their usage across the codebase.\n\n"
            info_msg += "Run: /deps update"
            
            # Output to stderr for informational message
            print(info_msg, file=sys.stderr)
        
        # Always continue normally
        sys.exit(0)
            
    except Exception as e:
        # On error, log to stderr and exit with error code
        print(f"Dependency tracker error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
