#!/usr/bin/env python3
"""
Feature State Guardian Hook - Prevents recreation of completed features
Integrated with Claude Code Boilerplate workflow and chains
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def main():
    """Main hook entry point following Anthropic hook specification."""
    try:
        # Read the tool use request from stdin
        request = json.loads(sys.stdin.read())
        
        # Extract tool and arguments - using CORRECT tool names from Anthropic docs
        tool_name = request.get('tool', '')
        args = request.get('arguments', {})
        
        # Check if this is a file modification operation
        if tool_name not in ['str_replace_based_edit_tool', 'create_file', 'write_file']:
            # Not a file operation, allow it
            return 0
        
        # Get the file path
        file_path = args.get('path', '')
        if not file_path:
            return 0
            
        # Check if design mode is off (respect existing system)
        if is_design_mode_off():
            # Design mode off means more freedom, skip strict checks
            return 0
            
        # Check if in TDD mode (respect existing workflow)
        if is_tdd_mode() and is_test_file(file_path):
            # TDD mode - always allow test file creation/modification
            return 0
        
        # Load feature state
        state = load_feature_state()
        if not state:
            # No state file yet, allow operation
            return 0
        
        # Check against PRP/PRD workflow
        if is_part_of_active_workflow(file_path):
            # Part of active PRD/PRP workflow, allow it
            return 0
        
        # Check if file belongs to a completed feature
        warning = check_feature_protection(file_path, state)
        if warning:
            # Integration with existing error format
            print(json.dumps({
                "error": "Feature Protection Triggered",
                "warning": warning,
                "suggestions": get_suggestions(file_path, state),
                "bypass": "Add --force flag or use proper enhancement workflow"
            }), file=sys.stderr)
            return 1  # Block the operation
        
        return 0
        
    except Exception as e:
        # Don't break on errors - fail open
        print(f"Hook error (allowing operation): {str(e)}", file=sys.stderr)
        return 0

def is_design_mode_off():
    """Check if design mode is disabled (integration with existing /dmoff command)."""
    try:
        config = json.loads(Path('.claude/config.json').read_text())
        return not config.get('design_system', {}).get('enforce', True)
    except:
        return False

def is_tdd_mode():
    """Check if in TDD workflow (integration with existing TDD system)."""
    try:
        # Check for active TDD workflow marker
        tdd_marker = Path('.claude/state/tdd-active.json')
        return tdd_marker.exists()
    except:
        return False

def is_test_file(file_path):
    """Check if this is a test file."""
    return any(pattern in file_path for pattern in [
        '.test.', '.spec.', '__tests__/', 'tests/'
    ])

def is_part_of_active_workflow(file_path):
    """Check if file is part of active PRD/PRP workflow."""
    try:
        # Check active PRD
        prd_state = Path('.claude/state/active-prd.json')
        if prd_state.exists():
            prd_data = json.loads(prd_state.read_text())
            if file_path in prd_data.get('planned_files', []):
                return True
        
        # Check active PRP
        prp_dir = Path('PRPs/active')
        if prp_dir.exists():
            for prp_file in prp_dir.glob('*.md'):
                # Simple check - could be enhanced
                if file_path in prp_file.read_text():
                    return True
                    
        return False
    except:
        return False

def load_feature_state():
    """Load feature state registry."""
    state_file = Path('.claude/branch-state/feature-state.json')
    if state_file.exists():
        try:
            with open(state_file, 'r') as f:
                return json.load(f)
        except:
            return None
    return None

def check_feature_protection(file_path, state):
    """Check if file modification should be blocked."""
    current_branch = get_current_branch()
    
    # Check each feature
    for feature_name, feature_data in state.get('features', {}).items():
        if feature_data.get('status') == 'completed':
            # Check if this file is part of the completed feature
            if file_path in feature_data.get('files', []):
                # Check if we should block
                if feature_data.get('do_not_recreate', False):
                    # Check if we're on a different branch
                    if current_branch != 'main' and current_branch != feature_data.get('branch', 'main'):
                        # Check if this is the correct enhancement branch
                        enhancement = feature_data.get('in_progress_enhancements', {})
                        if enhancement and current_branch == enhancement.get('branch'):
                            # On correct enhancement branch, allow
                            return None
                        
                        # Wrong branch, check if force flag is set
                        if not has_force_flag():
                            return format_protection_warning(
                                feature_name, 
                                feature_data, 
                                file_path, 
                                current_branch
                            )
    
    return None

def has_force_flag():
    """Check if --force flag was used (integration with existing commands)."""
    try:
        # Check command history for --force
        history_file = Path('.claude/logs/command-history.json')
        if history_file.exists():
            history = json.loads(history_file.read_text())
            last_command = history[-1] if history else {}
            return '--force' in last_command.get('args', [])
    except:
        pass
    return False

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

def format_protection_warning(feature_name, feature_data, file_path, current_branch):
    """Format warning that integrates with existing Claude Code style."""
    impl = feature_data.get('working_implementation', {})
    
    return f"""
⚠️  FEATURE STATE PROTECTION TRIGGERED!

You're about to modify a COMPLETED feature that's already working!

📍 Feature: {feature_name}
📄 File: {file_path}
✅ Status: {feature_data['status']} (completed {feature_data.get('completed_date', 'unknown')})
🌿 Current Branch: {current_branch}
⚠️  Main Branch Has: {impl.get('description', 'Working implementation')}

🛡️  Protection Reasons:
1. This feature is marked as complete and working
2. You're on a different branch that might not have latest code
3. Changes could overwrite the working implementation

💡 This integrates with your workflow:
- Use /feature-status {feature_name} for details
- Use /fw start [issue] to create proper enhancement
- Use /branch-status to see branch state
- Add --force to override (not recommended)
"""

def get_suggestions(file_path, state):
    """Get suggestions that integrate with existing commands."""
    return [
        "/feature-status - Check feature details",
        "/branch-status - See current branch state", 
        "/sync-main - Update from main branch",
        "/fw start [issue] - Start proper enhancement"
    ]

if __name__ == "__main__":
    sys.exit(main())
