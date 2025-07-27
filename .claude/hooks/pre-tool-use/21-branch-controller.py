#!/usr/bin/env python3
"""
Branch Controller Hook - Enforces branch management rules
Prevents conflicts and ensures orderly branch progression
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

def is_branch_creation_command(command):
    """Check if command creates a new branch."""
    branch_commands = ['git checkout -b', 'git branch']
    return any(cmd in command for cmd in branch_commands)

def validate_branch_creation():
    """Validate if new branch can be created."""
    registry = load_branch_registry()
    if not registry:
        # No registry yet, allow
        return None
    
    rules = registry.get('branch_rules', {})
    
    # Check active branch limit
    active_branches = [b for b in registry.get('active_branches', []) 
                      if b.get('status') == 'in_progress']
    
    max_allowed = rules.get('max_active_branches', 3)
    if len(active_branches) >= max_allowed:
        return format_branch_limit_error(active_branches, max_allowed)
    
    # Check main sync requirement
    if rules.get('require_main_sync', True):
        main_info = registry.get('main_branch', {})
        last_pulled = main_info.get('last_pulled')
        if last_pulled:
            last_pull_time = datetime.fromisoformat(last_pulled)
            if datetime.now() - last_pull_time > timedelta(hours=24):
                return format_sync_required_error()
    
    # Check for unfinished work
    if rules.get('require_tests_before_new', False):
        if has_failing_tests():
            return format_tests_required_error()
    
    return None

def validate_file_modification(file_path):
    """Check if file can be modified on current branch."""
    registry = load_branch_registry()
    if not registry:
        return None
    
    if not file_path:
        return None
    
    # Check if file is blocked
    blocked_files = registry.get('blocked_files', {})
    if file_path in blocked_files:
        block_info = blocked_files[file_path]
        current_branch = get_current_branch()
        
        if current_branch != block_info.get('blocked_by'):
            return format_file_blocked_error(file_path, block_info)
    
    return None

def load_branch_registry():
    """Load branch registry."""
    registry_file = Path('.claude/branch-state/branch-registry.json')
    if registry_file.exists():
        try:
            with open(registry_file, 'r') as f:
                return json.load(f)
        except:
            return None
    return None

def get_current_branch():
    """Get current git branch."""
    try:
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True,
            cwd='.'
        )
        return result.stdout.strip() if result.returncode == 0 else 'unknown'
    except:
        return 'unknown'

def has_failing_tests():
    """Check if there are failing tests."""
    # This is a simplified check - in practice would run actual tests
    try:
        result = subprocess.run(
            ['npm', 'test', '--', '--run'],
            capture_output=True,
            text=True,
            cwd='.'
        )
        return result.returncode != 0
    except:
        return False

def format_branch_limit_error(active_branches, max_allowed):
    """Format error for too many active branches."""
    branch_list = '\n'.join([
        f"  • {b['name']} (Issue: {b.get('issue', 'N/A')})"
        for b in active_branches
    ])
    
    return f"""
🚫 BRANCH LIMIT EXCEEDED!

You already have {len(active_branches)} active branch(es) (max: {max_allowed}):

{branch_list}

📋 Branch Policy: Maximum {max_allowed} active feature branch(es) at a time

💡 To create a new branch, first:
1. Complete current work: /fw complete [issue]
2. Or stash work: /branch stash
3. Or close branch: /branch close

Run: /branch-status to see all branches
"""

def format_sync_required_error():
    """Format error for outdated main branch."""
    return """
🔄 MAIN BRANCH SYNC REQUIRED!

Your main branch is over 24 hours old. You must sync before creating new branches.

💡 To sync:
1. Save current work: /checkpoint
2. Sync main: /sync-main
3. Then create your new branch

This prevents conflicts and ensures you're building on latest code!
"""

def format_tests_required_error():
    """Format error for failing tests."""
    return """
❌ TESTS MUST PASS BEFORE NEW BRANCH!

You have failing tests on the current branch. Fix them before starting new work.

💡 To fix:
1. Run tests: /test
2. Fix failures
3. Then create new branch

This maintains code quality and prevents accumulating technical debt!
"""

def format_file_blocked_error(file_path, block_info):
    """Format error for blocked file."""
    return f"""
🚫 FILE IS BLOCKED!

This file is currently being modified on another branch:

📄 File: {file_path}
🌿 Blocked by: {block_info.get('blocked_by', 'Unknown')}
📝 Reason: {block_info.get('reason', 'Active modifications')}

💡 Options:
1. Switch to the branch: git checkout {block_info.get('blocked_by', 'Unknown')}
2. Wait for that branch to complete
3. Work on different files

This prevents merge conflicts before they happen!
"""

def main():
    """Main hook entry point following Claude Code hook specification."""
    try:
        # Read input from Claude Code
        request = json.loads(sys.stdin.read())
        
        # Extract tool name and arguments
        tool_name = request.get('tool_name', '')
        tool_input = request.get('tool_input', {})
        
        # Check for branch operations via Bash tool
        if tool_name == 'Bash':
            command = tool_input.get('command', '')
            if is_branch_creation_command(command):
                error = validate_branch_creation()
                if error:
                    # Block the operation
                    print(json.dumps({
                        "decision": "block",
                        "message": error
                    }))
                    sys.exit(0)
        
        # Check for file modifications
        if tool_name in ['Write', 'Edit', 'MultiEdit']:
            file_path = tool_input.get('file_path', tool_input.get('path', ''))
            error = validate_file_modification(file_path)
            if error:
                # Block the operation
                print(json.dumps({
                    "decision": "block",
                    "message": error
                }))
                sys.exit(0)
        
        # No issues - continue normally
        sys.exit(0)
        
    except Exception as e:
        # On error, log to stderr and exit with error code
        print(f"Branch controller hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
