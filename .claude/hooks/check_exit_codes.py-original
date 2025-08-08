#!/usr/bin/env python3
"""
Check all hooks for proper exit codes
"""

import os
import re
from pathlib import Path

def check_hook(file_path):
    """Check if a hook has proper exit codes"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    issues = []
    
    # Check if main function exists
    if 'def main():' not in content:
        return issues  # Skip files without main function
    
    # Extract main function
    main_match = re.search(r'def main\(\):.*?(?=\nif __name__|$)', content, re.DOTALL)
    if not main_match:
        return issues
    
    main_content = main_match.group(0)
    
    # Check for sys.exit(0) outside of except blocks
    # Remove all except blocks first
    main_without_except = re.sub(r'except.*?(?=except|\Z)', '', main_content, flags=re.DOTALL)
    
    # Check if there's at least one sys.exit(0) in the non-exception code
    if 'sys.exit(0)' not in main_without_except:
        issues.append('Missing sys.exit(0) for success case')
    
    # Check hook type from path
    hook_type = 'unknown'
    if 'pre-tool-use' in str(file_path):
        hook_type = 'PreToolUse'
    elif 'post-tool-use' in str(file_path):
        hook_type = 'PostToolUse'
    elif 'stop' in str(file_path):
        hook_type = 'Stop'
    elif 'notification' in str(file_path):
        hook_type = 'Notification'
    
    # Check for incorrect exit codes based on hook type
    if hook_type == 'PostToolUse':
        # PostToolUse should not use sys.exit(2)
        if 'sys.exit(2)' in content:
            issues.append('PostToolUse should not use sys.exit(2)')
    
    # Check for JSON output (deprecated)
    if '"decision":' in content or '"action":' in content:
        if 'json.dumps' in content and any(x in content for x in ['"decision"', '"action"']):
            issues.append('Using deprecated JSON decision format')
    
    return issues

def main():
    hooks_dir = Path('/Users/shawnsmith/dev/bfc/boilerplate/.claude/hooks')
    
    all_issues = {}
    
    # Check all Python files
    for py_file in hooks_dir.rglob('*.py'):
        # Skip __pycache__ and backup files
        if '__pycache__' in str(py_file) or py_file.suffix == '.backup':
            continue
        
        issues = check_hook(py_file)
        if issues:
            all_issues[str(py_file.relative_to(hooks_dir))] = issues
    
    # Report results
    if all_issues:
        print(f"Found issues in {len(all_issues)} hooks:\n")
        for file_path, issues in sorted(all_issues.items()):
            print(f"{file_path}:")
            for issue in issues:
                print(f"  - {issue}")
            print()
    else:
        print("✅ All hooks appear to have correct exit codes!")

if __name__ == '__main__':
    main()
