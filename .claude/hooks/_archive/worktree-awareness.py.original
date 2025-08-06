#!/usr/bin/env python3
"""
Worktree Awareness Hook
Detects when working in worktrees and provides appropriate context and suggestions
"""

import json
import sys
import os
from pathlib import Path
import subprocess

def get_current_worktree():
    """Get current worktree info if in one."""
    try:
        # Check if we're in a worktree
        result = subprocess.run(['git', 'worktree', 'list', '--porcelain'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            return None
            
        current_dir = os.getcwd()
        worktree_info = None
        
        # Parse worktree list
        lines = result.stdout.strip().split('\n')
        for i in range(0, len(lines), 3):
            if i < len(lines) and lines[i].startswith('worktree '):
                path = lines[i].replace('worktree ', '')
                if current_dir.startswith(path) and '.worktrees' in path:
                    worktree_info = {
                        'path': path,
                        'name': Path(path).name,
                        'branch': lines[i+2].replace('branch refs/heads/', '') if i+2 < len(lines) else 'unknown'
                    }
                    break
                    
        return worktree_info
    except:
        return None

def get_worktree_config(worktree_path):
    """Get worktree configuration if exists."""
    config_file = Path(worktree_path) / '.claude' / 'worktree-config.json'
    if config_file.exists():
        try:
            with open(config_file) as f:
                return json.load(f)
        except:
            pass
    return None

def get_other_worktrees():
    """Get list of other active worktrees."""
    try:
        result = subprocess.run(['git', 'worktree', 'list'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            return []
            
        worktrees = []
        for line in result.stdout.strip().split('\n'):
            if '.worktrees' in line:
                parts = line.split()
                if parts:
                    path = parts[0]
                    name = Path(path).name
                    branch = parts[2].strip('[]') if len(parts) > 2 else 'unknown'
                    worktrees.append({
                        'name': name,
                        'branch': branch,
                        'path': path
                    })
        return worktrees
    except:
        return []

def main():
    """Main hook execution."""
    try:
        # Read input
        input_data = json.loads(sys.stdin.read())
        
        # Check if we're in a worktree
        worktree = get_current_worktree()
        if not worktree:
            # Not in worktree, exit silently
            sys.exit(0)
            
        # Get worktree config
        config = get_worktree_config(worktree['path'])
        task = config.get('worktree', {}).get('task', 'No task description') if config else 'No task description'
        
        # Get other worktrees
        others = get_other_worktrees()
        other_count = len([w for w in others if w['name'] != worktree['name']])
        
        # Only show context for commands that would benefit
        tool_name = input_data.get('tool_name', '')
        relevant_tools = [
            'run_command', 'str_replace', 'create_file', 
            'write_file', 'edit_file', 'bash'
        ]
        
        if tool_name not in relevant_tools:
            sys.exit(0)
            
        # Check if this is the first command in worktree
        # (would need to track this in state - simplified for now)
        show_context = True  # Always show for now
        
        if show_context:
            # Build context message
            context_msg = f"\n🌳 **Worktree Context: `{worktree['name']}`**\n"
            context_msg += f"  • Branch: `{worktree['branch']}`\n"
            context_msg += f"  • Task: {task}\n"
            
            if other_count > 0:
                context_msg += f"  • Other worktrees: {other_count} running in parallel\n"
                
            # Add relevant commands
            context_msg += "\n📍 **Worktree Commands:**\n"
            context_msg += f"  • `/wt-status` - View all worktrees\n"
            context_msg += f"  • `/wt-switch [name]` - Switch to another worktree\n"
            context_msg += f"  • `/wt-pr {worktree['name']}` - Create PR when ready\n"
            context_msg += f"  • `cd {Path(worktree['path']).parent.parent}` - Return to main\n"
            
            # Add to result
            result = input_data.get('result', {})
            if isinstance(result, dict):
                result['worktree_context'] = context_msg
            else:
                # Print to stderr for visibility
                print(context_msg, file=sys.stderr)
                
        sys.exit(0)
        
    except Exception as e:
        # Don't fail the hook
        sys.exit(0)

if __name__ == "__main__":
    main()
