#!/usr/bin/env python3
"""
Feature State Awareness Hook - Provides warnings about completed features
Fully integrated with Claude Code Boilerplate systems
Non-blocking, educational approach
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def is_test_file(file_path):
    """Check if this is a test file."""
    test_patterns = ['.test.', '.spec.', '__tests__/', 'tests/', 'test-']
    return any(pattern in file_path.lower() for pattern in test_patterns)

def is_design_mode_off():
    """Check if design mode is disabled."""
    try:
        # Check for design mode marker
        design_mode_file = Path('.claude/state/design-mode.json')
        if design_mode_file.exists():
            state = json.loads(design_mode_file.read_text())
            return state.get('mode') == 'off'
    except:
        pass
    return False

def is_active_workflow_file(file_path):
    """Check if file is part of active PRP/PRD workflow."""
    try:
        # Check active PRP
        active_prp = Path('.claude/state/active-prp.json')
        if active_prp.exists():
            prp_data = json.loads(active_prp.read_text())
            if file_path in prp_data.get('target_files', []):
                return True
        
        # Check active PRD tasks
        active_tasks = Path('.claude/state/active-tasks.json')
        if active_tasks.exists():
            tasks_data = json.loads(active_tasks.read_text())
            for task in tasks_data.get('tasks', []):
                if file_path in task.get('files', []):
                    return True
                    
    except:
        pass
    return False

def load_feature_state():
    """Load feature state from GitHub gist or local cache."""
    try:
        # Try local cache first
        cache_file = Path('.claude/state/feature-awareness-cache.json')
        if cache_file.exists():
            # Check if cache is recent (within 1 hour)
            if (datetime.now().timestamp() - cache_file.stat().st_mtime) < 3600:
                return json.loads(cache_file.read_text())
        
        # Otherwise load from branch state if exists
        state_file = Path('.claude/branch-state/feature-state.json')
        if state_file.exists():
            return json.loads(state_file.read_text())
            
    except:
        pass
    return None

def check_feature_awareness(file_path, state):
    """Check if we should show awareness about this file."""
    current_branch = get_current_branch()
    
    # Check each completed feature
    for feature_name, feature_data in state.get('features', {}).items():
        if feature_data.get('status') == 'completed':
            if file_path in feature_data.get('files', []):
                # Check if on enhancement branch
                enhancement = feature_data.get('in_progress_enhancements', {})
                if enhancement and current_branch == enhancement.get('branch'):
                    # On correct enhancement branch
                    return None
                
                # Show helpful awareness
                return format_awareness_message(feature_name, feature_data, file_path, current_branch)
    
    return None

def get_current_branch():
    """Get current git branch."""
    try:
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True
        )
        return result.stdout.strip() if result.returncode == 0 else 'unknown'
    except:
        return 'unknown'

def format_awareness_message(feature_name, feature_data, file_path, current_branch):
    """Format helpful awareness message."""
    impl = feature_data.get('working_implementation', {})
    
    # Non-blocking, educational tone
    return f"""ℹ️  Feature Awareness: {feature_name}

This file ({file_path}) is part of a completed feature.
• Status: {feature_data.get('status')} 
• Implementation: {impl.get('description', 'Working implementation exists')}
• Current branch: {current_branch}

💡 Helpful context:
- If enhancing: Consider using /fw start [issue] for proper tracking
- If fixing: Make sure to preserve existing functionality
- Run: /feature-status {feature_name} for full details

This is just information - your edit will proceed normally."""

def log_feature_awareness_event(file_path, info):
    """Log awareness event to metrics system."""
    try:
        # Use existing event system
        event_file = Path('.claude/metrics/events.jsonl')
        event_file.parent.mkdir(parents=True, exist_ok=True)
        
        event = {
            'timestamp': datetime.now().isoformat(),
            'event': 'feature_awareness_shown',
            'file': file_path,
            'branch': get_current_branch()
        }
        
        with open(event_file, 'a') as f:
            f.write(json.dumps(event) + '\n')
            
    except:
        # Don't fail on metrics
        pass

def main():
    """Main hook entry point following Claude Code hook specification."""
    try:
        # Read input from Claude Code
        request = json.loads(sys.stdin.read())
        
        # Extract tool name and arguments
        tool_name = request.get('tool_name', '')
        tool_input = request.get('tool_input', {})
        
        # Only check file modification operations
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            # Not a write operation - continue normally
            sys.exit(0)
        
        # Get the file path
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        if not file_path:
            sys.exit(0)
            
        # Check if this is a test file (always allow in TDD workflow)
        if is_test_file(file_path):
            sys.exit(0)
            
        # Check if design mode is off (more freedom)
        if is_design_mode_off():
            sys.exit(0)
            
        # Check if part of active PRP/PRD workflow
        if is_active_workflow_file(file_path):
            sys.exit(0)
        
        # Load feature state if it exists
        state = load_feature_state()
        if not state:
            sys.exit(0)
        
        # Check for feature awareness (non-blocking)
        awareness_info = check_feature_awareness(file_path, state)
        if awareness_info:
            # Just inform via stderr, don't block
            print(f"\n{awareness_info}\n", file=sys.stderr)
            
            # Log to metrics for tracking
            log_feature_awareness_event(file_path, awareness_info)
        
        # Always continue normally
        sys.exit(0)
        
    except Exception as e:
        # On error, log to stderr and exit with error code
        print(f"Feature awareness hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
