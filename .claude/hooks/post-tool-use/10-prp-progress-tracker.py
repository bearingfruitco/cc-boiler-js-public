#!/usr/bin/env python3
"""
Track PRP execution progress and update status automatically
"""

import json
import sys
import os
import re
from datetime import datetime
from pathlib import Path

def update_prp_progress(file_path, content):
    """Update progress tracking for active PRPs"""
    
    # Find which PRP this relates to
    active_prp = find_active_prp(file_path, content)
    if not active_prp:
        return
    
    progress_file = Path(f'.claude/metrics/prp_progress/{active_prp}.json')
    progress_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Load or create progress data
    if progress_file.exists():
        with open(progress_file) as f:
            progress = json.load(f)
    else:
        progress = {
            'name': active_prp,
            'started': datetime.now().isoformat(),
            'files_modified': [],
            'tasks_completed': [],
            'validation_runs': [],
            'last_activity': datetime.now().isoformat()
        }
    
    # Update progress
    if file_path not in progress['files_modified']:
        progress['files_modified'].append(file_path)
    
    # Check for task completion markers
    if '✅' in content or 'DONE:' in content or 'Completed:' in content:
        task = extract_task_name(content)
        if task and task not in progress['tasks_completed']:
            progress['tasks_completed'].append(task)
    
    progress['last_activity'] = datetime.now().isoformat()
    
    # Save progress
    with open(progress_file, 'w') as f:
        json.dump(progress, f, indent=2)
    
    # Log progress
    print(f"📊 PRP Progress: {active_prp}")
    print(f"   Files modified: {len(progress['files_modified'])}")
    print(f"   Tasks completed: {len(progress['tasks_completed'])}")

def find_active_prp(file_path, content):
    """Determine which PRP this file change relates to"""
    
    # Check PRPs/active/ directory
    active_prps = list(Path('PRPs/active/').glob('*.md'))
    
    for prp_path in active_prps:
        prp_name = prp_path.stem
        
        # Check if file path matches PRP patterns
        if prp_name.replace('-', '_') in file_path:
            return prp_name
            
        # Check if content references the PRP
        if prp_name in content or prp_name.replace('-', '_') in content:
            return prp_name
    
    return None

def track_validation_run(command, output):
    """Track validation runs and results"""
    
    # Determine validation level
    level = determine_validation_level(command)
    if not level:
        return
    
    # Check if it passed or failed
    passed = 'PASSED' in output or 'All tests passed' in output or '✓' in output
    
    # Find active PRP from command
    prp_name = extract_prp_from_command(command)
    if not prp_name:
        return
    
    # Update validation history
    validation_file = Path(f'.claude/metrics/prp_validation/{prp_name}.json')
    validation_file.parent.mkdir(parents=True, exist_ok=True)
    
    if validation_file.exists():
        with open(validation_file) as f:
            history = json.load(f)
    else:
        history = {'runs': []}
    
    history['runs'].append({
        'timestamp': datetime.now().isoformat(),
        'level': level,
        'command': command,
        'passed': passed,
        'output_snippet': output[:500] if not passed else 'All passed'
    })
    
    # Keep only last 50 runs
    history['runs'] = history['runs'][-50:]
    
    with open(validation_file, 'w') as f:
        json.dump(history, f, indent=2)
    
    # Log result
    status = '✅' if passed else '❌'
    print(f"{status} Validation Level {level}: {prp_name}")

def determine_validation_level(command):
    """Determine which validation level this command represents"""
    
    if any(cmd in command for cmd in ['lint', 'typecheck', 'mypy', 'ruff']):
        return 1
    elif 'test' in command and not 'e2e' in command and not 'integration' in command:
        return 2
    elif any(cmd in command for cmd in ['e2e', 'integration', 'api']):
        return 3
    elif any(cmd in command for cmd in ['lighthouse', 'security', 'performance']):
        return 4
    
    return None

def extract_task_name(content):
    """Extract task name from content"""
    
    # Look for task markers
    patterns = [
        r'(?:Task|TODO|DONE):\s*(.+?)(?:\n|$)',
        r'✅\s*(.+?)(?:\n|$)',
        r'Completed:\s*(.+?)(?:\n|$)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return match.group(1).strip()
    
    return None

def extract_prp_from_command(command):
    """Extract PRP name from command"""
    
    # Look for common patterns
    patterns = [
        r'test[s]?[/\\]test[_-](\w+)',
        r'src[/\\](\w+)',
        r'--prp\s+(\w+)',
        r'components[/\\](\w+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, command)
        if match:
            name = match.group(1)
            # Check if this matches an active PRP
            if Path(f'PRPs/active/{name}.md').exists():
                return name
            # Try with hyphens
            name_hyphen = name.replace('_', '-')
            if Path(f'PRPs/active/{name_hyphen}.md').exists():
                return name_hyphen
    
    return None

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool information
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        tool_result = input_data.get('tool_result', {})
        
        # Check if working with PRP files
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            sys.exit(0)
            
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        content = tool_input.get('content', tool_input.get('new_str', ''))
        
        # Track PRP-related file changes
        if 'PRPs/active/' in file_path or any(marker in file_path for marker in [
            '/src/', '/components/', '/tests/', '/api/'
        ]):
            update_prp_progress(file_path, content)
        
        # Exit successfully
        sys.exit(0)
        
    except Exception as e:
        # Log error to stderr and exit
        print(f"PRP progress tracker error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
