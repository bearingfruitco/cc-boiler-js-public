#!/usr/bin/env python3
"""
Dependency Tracking Hook - Alert when modifying components with dependents
Prevents breaking changes and suggests updates
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime

def get_config():
    """Load hook configuration"""
    config_path = Path(__file__).parent.parent / 'config.json'
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {'dependencies': {'auto_track': True, 'alert_threshold': 3}}

def extract_component_name(file_path):
    """Extract component name from file path"""
    path = Path(file_path)
    if path.suffix in ['.tsx', '.jsx', '.ts', '.js']:
        return path.stem
    return None

def parse_used_by_comment(content):
    """Extract @used-by from component file"""
    # Look for @used-by comment
    used_by_pattern = r'@used-by\s+([^\n]+)'
    match = re.search(used_by_pattern, content)
    
    if match:
        # Parse comma-separated list
        components = [c.strip() for c in match.group(1).split(',')]
        return [c for c in components if c]  # Filter empty
    
    return []

def parse_depends_on_comment(content):
    """Extract @depends-on from component file"""
    depends_pattern = r'@depends-on\s+([^\n]+)'
    match = re.search(depends_pattern, content)
    
    if match:
        components = [c.strip() for c in match.group(1).split(',')]
        return [c for c in components if c]
    
    return []

def check_breaking_changes(old_content, new_content):
    """Detect potential breaking changes"""
    breaking = []
    
    # Check for removed exports
    old_exports = set(re.findall(r'export\s+(?:const|function|class)\s+(\w+)', old_content))
    new_exports = set(re.findall(r'export\s+(?:const|function|class)\s+(\w+)', new_content))
    removed_exports = old_exports - new_exports
    
    if removed_exports:
        breaking.append({
            'type': 'removed_export',
            'items': list(removed_exports)
        })
    
    # Check for changed prop interfaces
    old_props = extract_prop_interface(old_content)
    new_props = extract_prop_interface(new_content)
    
    if old_props and new_props:
        removed_props = set(old_props.keys()) - set(new_props.keys())
        if removed_props:
            breaking.append({
                'type': 'removed_props',
                'items': list(removed_props)
            })
    
    return breaking

def extract_prop_interface(content):
    """Extract props interface from TypeScript component"""
    # Simple extraction - could be enhanced
    props_pattern = r'interface\s+\w*Props\s*\{([^}]+)\}'
    match = re.search(props_pattern, content, re.DOTALL)
    
    if match:
        props = {}
        prop_lines = match.group(1).split('\n')
        for line in prop_lines:
            prop_match = re.match(r'\s*(\w+)\s*[?]?\s*:\s*(.+)', line)
            if prop_match:
                props[prop_match.group(1)] = prop_match.group(2).strip()
        return props
    
    return None

def load_dependency_manifest():
    """Load dependency manifest"""
    manifest_path = Path('.claude/dependencies/manifest.json')
    if manifest_path.exists():
        with open(manifest_path) as f:
            return json.load(f)
    return {'components': {}}

def update_dependency_manifest(component_name, data):
    """Update dependency manifest"""
    manifest_path = Path('.claude/dependencies/manifest.json')
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    
    manifest = load_dependency_manifest()
    
    if component_name not in manifest['components']:
        manifest['components'][component_name] = {}
    
    manifest['components'][component_name].update(data)
    manifest['components'][component_name]['last_modified'] = datetime.now().isoformat()
    
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

def format_dependency_alert(component_name, used_by, breaking_changes=None):
    """Format dependency alert message"""
    message = f"""📦 Dependency Alert: {component_name}

This component is used by {len(used_by)} other components:
"""
    
    for comp in used_by[:5]:  # Show first 5
        message += f"  • {comp}\n"
    
    if len(used_by) > 5:
        message += f"  ... and {len(used_by) - 5} more\n"
    
    if breaking_changes:
        message += "\n⚠️  Potential Breaking Changes Detected:\n"
        for change in breaking_changes:
            if change['type'] == 'removed_export':
                message += f"  • Removed exports: {', '.join(change['items'])}\n"
            elif change['type'] == 'removed_props':
                message += f"  • Removed props: {', '.join(change['items'])}\n"
    
    message += f"""
Quick Actions:
  • /deps check {component_name} - See full dependency tree
  • /deps breaking {component_name} - Detailed breaking change analysis
  • Continue with caution - Changes may break dependent components
"""
    
    return message

def main():
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool name - handle multiple formats
        tool_name = input_data.get('tool_name', '')
        if not tool_name and 'tool_use' in input_data:
            tool_name = input_data['tool_use'].get('name', '')
        if not tool_name:
            tool_name = input_data.get('tool', '')
        
        # Only process file modifications
        if tool_name not in ['Write', 'Edit', 'str_replace']:
            sys.exit(0)
            return
        
        # Extract parameters
        tool_input = input_data.get('tool_input', {})
        if not tool_input and 'tool_use' in input_data:
            tool_input = input_data['tool_use'].get('parameters', {})
        
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        
        # Only check component files
        if not any(file_path.endswith(ext) for ext in ['.tsx', '.jsx', '.ts', '.js']):
            sys.exit(0)
            return
            
        if '.test.' in file_path or '.spec.' in file_path:
            sys.exit(0)
            return
        
        component_name = extract_component_name(file_path)
        if not component_name:
            sys.exit(0)
            return
        
        config = get_config()
        
        # Check if dependency tracking is enabled
        if not config.get('dependencies', {}).get('auto_track', True):
            sys.exit(0)
            return
        
        # Get current content
        new_content = tool_input.get('content', tool_input.get('new_str', ''))
        
        # Parse dependency comments
        used_by = parse_used_by_comment(new_content)
        depends_on = parse_depends_on_comment(new_content)
        
        # Update manifest
        update_dependency_manifest(component_name, {
            'used_by': used_by,
            'depends_on': depends_on,
            'file_path': file_path
        })
        
        # If component has dependents, alert user
        alert_threshold = config.get('dependencies', {}).get('alert_threshold', 3)
        
        if len(used_by) >= alert_threshold:
            # Try to detect breaking changes if we have old content
            breaking_changes = None
            if tool_name in ['Edit', 'str_replace']:
                old_content = tool_input.get('old_str', '')
                if old_content:
                    breaking_changes = check_breaking_changes(old_content, new_content)
            
            message = format_dependency_alert(component_name, used_by, breaking_changes)
            
            print(message)  # Warning shown in transcript
        sys.exit(0)
        else:
            # Log for tracking but don't warn
            if used_by:
                print(json.dumps({
                    sys.exit(0)
            else:
                sys.exit(0)
                
    except Exception as e:
        print(json.dumps({
            sys.exit(0)

if __name__ == "__main__":
    main()
    sys.exit(0)
