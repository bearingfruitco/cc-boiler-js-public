#!/usr/bin/env python3
"""Test hooks for correct exit codes"""

import re
from pathlib import Path

def check_hook_exit_codes():
    hooks_dir = Path('/Users/shawnsmith/dev/bfc/boilerplate/.claude/hooks')
    
    issues = []
    checked = 0
    
    for py_file in hooks_dir.rglob('*.py'):
        if '__pycache__' in str(py_file) or py_file.suffix == '.backup':
            continue
        
        checked += 1
        with open(py_file, 'r') as f:
            content = f.read()
        
        # Determine hook type from path
        hook_type = 'unknown'
        if 'pre-tool-use' in str(py_file):
            hook_type = 'PreToolUse'
        elif 'post-tool-use' in str(py_file):
            hook_type = 'PostToolUse'
        elif 'stop' in str(py_file):
            hook_type = 'Stop'
        
        # Check for issues
        if hook_type == 'PostToolUse':
            # PostToolUse should not use exit(2)
            if 'sys.exit(2)' in content:
                issues.append(f"{py_file.name}: PostToolUse should not use sys.exit(2)")
        
        # Check for JSON decision format (deprecated)
        if '"decision":' in content and 'json.dumps' in content:
            issues.append(f"{py_file.name}: Using deprecated JSON decision format")
        
        # Check if main function has at least one sys.exit(0)
        if 'def main' in content:
            main_section = content[content.find('def main'):]
            if 'sys.exit(0)' not in main_section:
                issues.append(f"{py_file.name}: Missing sys.exit(0) for success case")
    
    print(f"✅ Checked {checked} hooks")
    
    if issues:
        print(f"❌ Found {len(issues)} issues:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ All hooks have correct exit codes")
        return True

if __name__ == '__main__':
    success = check_hook_exit_codes()
    exit(0 if success else 1)
