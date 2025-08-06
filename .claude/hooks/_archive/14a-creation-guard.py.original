#!/usr/bin/env python3
"""
Creation Guard Hook - Check if components/functions exist before creating
Prevents duplicate work and maintains awareness of existing code
"""

import json
import sys
import os
import re
import subprocess
from pathlib import Path
from datetime import datetime

def get_config():
    """Load hook configuration"""
    config_path = Path(__file__).parent.parent / 'config.json'
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {'hooks': {'creation_guard': {'enabled': True}}}

def extract_creation_intent(tool_name, tool_input):
    """Detect if this is a creation operation and extract name"""
    path = tool_input.get('file_path', tool_input.get('path', ''))
    content = tool_input.get('content', '')
    
    # Check for component creation patterns
    if tool_name == 'Write':
        # New file creation
        if path.endswith(('.tsx', '.jsx', '.ts', '.js')):
            # Extract component/function name from path
            component_name = Path(path).stem
            return {
                'type': 'component',
                'name': component_name,
                'path': path
            }
        elif '/api/' in path and path.endswith('.ts'):
            # API route creation
            return {
                'type': 'api_route',
                'name': path,
                'path': path
            }
    
    # Check for function/hook creation in content
    if tool_name in ['Write', 'Edit']:
        # Look for new exports
        export_patterns = [
            r'export\s+(?:default\s+)?(?:function|const)\s+(\w+)',
            r'export\s+{\s*(\w+)',
            r'function\s+(\w+)\s*\(',
            r'const\s+(\w+)\s*=\s*\('
        ]
        
        for pattern in export_patterns:
            matches = re.findall(pattern, content)
            if matches:
                return {
                    'type': 'function',
                    'name': matches[0],
                    'path': path
                }
    
    return None

def check_exists(name, type='component'):
    """Check if component/function/route already exists"""
    results = {
        'found': False,
        'locations': [],
        'exact_match': False,
        'similar': []
    }
    
    # Search strategies based on type
    if type == 'component':
        # Search component directories
        search_dirs = ['components', 'app', 'src/components', 'src/app']
        for dir in search_dirs:
            if os.path.exists(dir):
                # Find exact matches
                cmd = f"find {dir} -name '{name}.tsx' -o -name '{name}.jsx' -o -name '{name}.ts' -o -name '{name}.js'"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if result.stdout.strip():
                    results['found'] = True
                    results['exact_match'] = True
                    results['locations'].extend(result.stdout.strip().split('\n'))
        
        # Search for exports with this name
        cmd = f"grep -r 'export.*{name}' --include='*.tsx' --include='*.jsx' --include='*.ts' --include='*.js' . 2>/dev/null | head -10"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.stdout.strip():
            results['found'] = True
            for line in result.stdout.strip().split('\n'):
                if ':' in line:
                    file_path = line.split(':')[0]
                    if file_path not in results['locations']:
                        results['locations'].append(file_path)
    
    elif type == 'api_route':
        # Check for existing API route
        if os.path.exists(name):
            results['found'] = True
            results['exact_match'] = True
            results['locations'] = [name]
    
    elif type == 'function':
        # Search for function definitions
        cmd = f"grep -r 'function {name}\\|const {name}\\|export.*{name}' --include='*.ts' --include='*.tsx' --include='*.js' --include='*.jsx' . 2>/dev/null | head -10"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.stdout.strip():
            results['found'] = True
            for line in result.stdout.strip().split('\n'):
                if ':' in line:
                    file_path = line.split(':')[0]
                    if file_path not in results['locations']:
                        results['locations'].append(file_path)
    
    # Find similar names (fuzzy match)
    if not results['exact_match']:
        similar_names = find_similar_names(name, type)
        results['similar'] = similar_names[:5]  # Top 5 similar
    
    # Get usage information
    if results['found'] and results['locations']:
        results['usage'] = find_usage_locations(name)
        results['info'] = get_component_info(results['locations'][0])
    
    return results

def find_similar_names(name, type):
    """Find components with similar names"""
    similar = []
    
    # Simple similarity check - could be enhanced with fuzzy matching
    if len(name) >= 3:
        cmd = f"find . -name '*.tsx' -o -name '*.jsx' -o -name '*.ts' -o -name '*.js' | grep -i {name[:3]} | head -10"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.stdout.strip():
            for file_path in result.stdout.strip().split('\n'):
                component_name = Path(file_path).stem
                if component_name != name and len(component_name) > 2:
                    similar.append({
                        'name': component_name,
                        'path': file_path,
                        'similarity': calculate_similarity(name, component_name)
                    })
    
    # Sort by similarity
    similar.sort(key=lambda x: x['similarity'], reverse=True)
    return similar

def calculate_similarity(str1, str2):
    """Simple similarity calculation"""
    # Levenshtein distance approximation
    longer = str1 if len(str1) > len(str2) else str2
    shorter = str2 if longer == str1 else str1
    
    if not longer:
        return 0.0
    
    # Count matching characters
    matches = sum(1 for i, char in enumerate(shorter) if i < len(longer) and char == longer[i])
    return matches / len(longer)

def find_usage_locations(name):
    """Find where component is used"""
    usage = []
    
    cmd = f"grep -r 'import.*{name}\\|<{name}' --include='*.tsx' --include='*.jsx' --include='*.ts' --include='*.js' . 2>/dev/null | grep -v '{name}\\.' | head -10"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.stdout.strip():
        for line in result.stdout.strip().split('\n'):
            if ':' in line:
                file_path = line.split(':')[0]
                usage.append(file_path)
    
    return list(set(usage))  # Unique locations

def get_component_info(file_path):
    """Extract component information"""
    if not os.path.exists(file_path):
        return None
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        info = {
            'created': get_file_creation_date(file_path),
            'modified': get_file_modified_date(file_path),
            'size': len(content),
            'exports': extract_exports(content),
            'props': extract_props(content)
        }
        
        return info
    except:
        return None

def get_file_creation_date(file_path):
    """Get file creation date from git"""
    cmd = f"git log --follow --format=%aI --diff-filter=A -- {file_path} | tail -1"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip() or 'unknown'

def get_file_modified_date(file_path):
    """Get last modified date"""
    try:
        stat = os.stat(file_path)
        return datetime.fromtimestamp(stat.st_mtime).isoformat()
    except:
        return 'unknown'

def extract_exports(content):
    """Extract exported items from file"""
    exports = []
    
    # Default export
    if 'export default' in content:
        exports.append('default')
    
    # Named exports
    named_pattern = r'export\s+(?:const|function|class)\s+(\w+)'
    exports.extend(re.findall(named_pattern, content))
    
    # Export declarations
    declaration_pattern = r'export\s+{\s*([^}]+)\s*}'
    matches = re.findall(declaration_pattern, content)
    for match in matches:
        exports.extend([e.strip() for e in match.split(',')])
    
    return list(set(exports))

def extract_props(content):
    """Extract component props interface"""
    props_pattern = r'interface\s+\w*Props\s*{([^}]+)}'
    match = re.search(props_pattern, content, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    return None

def format_exists_message(creation_intent, exists_result):
    """Format the warning message for existing component"""
    name = creation_intent['name']
    
    if not exists_result['found']:
        return None
    
    message = f"""⚠️ {name} Already Exists!

📍 Found at: {exists_result['locations'][0]}
"""
    
    if exists_result.get('info'):
        info = exists_result['info']
        message += f"""📅 Created: {info['created'][:10] if info['created'] != 'unknown' else 'unknown'}
📝 Last modified: {info['modified'][:19] if info['modified'] != 'unknown' else 'unknown'}
📦 Exports: {', '.join(info['exports']) if info['exports'] else 'none'}
"""
    
    if exists_result.get('usage'):
        message += f"""
📊 Used in {len(exists_result['usage'])} places:
"""
        for usage in exists_result['usage'][:3]:
            message += f"  • {usage}\n"
        if len(exists_result['usage']) > 3:
            message += f"  ... and {len(exists_result['usage']) - 3} more\n"
    
    message += f"""
Options:
1. Update existing component (recommended)
2. Create with different name
3. Override (requires confirmation)

To update existing:
  • Open: {exists_result['locations'][0]}
  • Or run: /open {exists_result['locations'][0]}
"""
    
    if exists_result.get('similar'):
        message += f"""
📝 Similar components found:
"""
        for similar in exists_result['similar'][:3]:
            message += f"  • {similar['name']} ({similar['path']})\n"
    
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
        
        # Only process creation operations
        if tool_name not in ['Write', 'create_file']:
            sys.exit(0)
            return
        
        # Extract parameters
        tool_input = input_data.get('tool_input', {})
        if not tool_input and 'tool_use' in input_data:
            tool_input = input_data['tool_use'].get('parameters', {})
        
        config = get_config()
        
        # Check if creation guard is enabled
        if not config.get('hooks', {}).get('creation_guard', {}).get('enabled', True):
            sys.exit(0)
            return
        
        # Extract creation intent
        creation_intent = extract_creation_intent(tool_name, tool_input)
        
        if not creation_intent:
            sys.exit(0)
            return
        
        # Check if already exists
        exists_result = check_exists(creation_intent['name'], creation_intent['type'])
        
        if exists_result['found']:
            message = format_exists_message(creation_intent, exists_result)
            
            if message:
                print(message)  # Warning shown in transcript
        sys.exit(0)
                return
        
        # If not found, log that it's safe to create
        print(json.dumps({
            sys.exit(0)
        
    except Exception as e:
        print(json.dumps({
            sys.exit(0)

if __name__ == "__main__":
    main()
    sys.exit(0)
