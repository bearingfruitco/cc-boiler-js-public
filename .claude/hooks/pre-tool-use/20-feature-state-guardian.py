#!/usr/bin/env python3
"""
Feature State Guardian Hook - Prevents recreation of completed features
Ensures branch awareness and protects working implementations
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def main():
    """Main hook entry point following Anthropic hook specification."""
    # Read the tool use request from stdin
    request = json.loads(sys.stdin.read())
    
    # Extract tool and arguments
    tool_name = request.get('tool', '')
    args = request.get('arguments', {})
    
    # Check if this is a file modification operation
    if tool_name not in ['str_replace_editor', 'create', 'write']:
        # Not a file operation, allow it
        return 0
    
    # Get the file path
    file_path = args.get('path', '')
    if not file_path:
        return 0
    
    # Load feature state
    state = load_feature_state()
    if not state:
        # No state file yet, allow operation
        return 0
    
    # Check if file belongs to a completed feature
    warning = check_feature_protection(file_path, state)
    if warning:
        print(warning, file=sys.stderr)
        return 1  # Block the operation
    
    return 0

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
                        return format_protection_warning(
                            feature_name, 
                            feature_data, 
                            file_path, 
                            current_branch
                        )
                
                # Check for in-progress enhancements
                if 'in_progress_enhancements' in feature_data:
                    enhancement = feature_data['in_progress_enhancements']
                    if current_branch != enhancement.get('branch'):
                        return format_branch_mismatch_warning(
                            feature_name,
                            enhancement,
                            current_branch
                        )
    
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

def format_protection_warning(feature_name, feature_data, file_path, current_branch):
    """Format warning about recreating completed feature."""
    return f"""
⚠️  FEATURE STATE PROTECTION TRIGGERED!

You're about to modify a COMPLETED feature that's already working!

📍 Feature: {feature_name}
📄 File: {file_path}
✅ Status: {feature_data['status']} (completed {feature_data.get('completed_date', 'unknown')})
🌿 Current Branch: {current_branch}
⚠️  Main Branch Has: {feature_data.get('working_implementation', {}).get('description', 'Working implementation')}

🛡️  Protection Reasons:
1. This feature is marked as complete and working
2. You're on a different branch that might not have latest code
3. Changes could overwrite the working implementation

💡 Recommended Actions:
1. Switch to main: git checkout main && git pull
2. Create new branch FROM main: git checkout -b feature/enhance-{feature_name}
3. Or continue enhancement on: {feature_data.get('in_progress_enhancements', {}).get('branch', 'N/A')}

To understand more: /feature-status {feature_name}
"""

def format_branch_mismatch_warning(feature_name, enhancement, current_branch):
    """Format warning about wrong branch for enhancement."""
    return f"""
⚠️  WRONG BRANCH FOR THIS ENHANCEMENT!

You're trying to modify {feature_name} from the wrong branch!

📍 Feature: {feature_name}
🎯 Enhancement Issue: {enhancement.get('issue', 'Unknown')}
✅ Correct Branch: {enhancement.get('branch', 'Unknown')}
❌ Current Branch: {current_branch}
📝 Enhancement Goal: {enhancement.get('adding', 'Unknown enhancement')}

💡 To fix:
1. Stash current changes: git stash
2. Switch to correct branch: git checkout {enhancement.get('branch', 'Unknown')}
3. Apply changes: git stash pop

This prevents duplicate work and merge conflicts!
"""

if __name__ == "__main__":
    sys.exit(main())
