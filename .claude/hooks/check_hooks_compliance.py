#!/usr/bin/env python3
"""
Hook Compliance Checker
Checks all hooks for compliance with official Claude Code specification
"""

import os
import re
from pathlib import Path
import json

# Official tool names
OFFICIAL_TOOLS = [
    'Write', 'Edit', 'MultiEdit', 'Read', 'Bash',
    'ListDirectory', 'SearchFiles', 'CreateDirectory',
    'DeleteFile', 'Task', 'Glob', 'Grep', 
    'WebFetch', 'WebSearch'
]

# Wrong tool names that need fixing
WRONG_TOOL_NAMES = {
    'write_file': 'Write',
    'edit_file': 'Edit',
    'str_replace': 'MultiEdit',
    'multi_edit': 'MultiEdit',
    'read_file': 'Read',
    'bash': 'Bash',  # must be capital
    'list_directory': 'ListDirectory',
    'search_files': 'SearchFiles',
    'create_directory': 'CreateDirectory',
    'delete_file': 'DeleteFile',
    'create_task': 'Task',
    'web_fetch': 'WebFetch',
    'web_search': 'WebSearch'
}

def check_hook(file_path):
    """Check a single hook for compliance issues"""
    issues = []
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except:
        return ['Cannot read file']
    
    # Check for wrong tool names
    for wrong, correct in WRONG_TOOL_NAMES.items():
        if f"'{wrong}'" in content or f'"{wrong}"' in content:
            issues.append(f"Wrong tool name: '{wrong}' should be '{correct}'")
    
    # Check for JSON decision format (wrong)
    if re.search(r'json\.dumps.*decision.*block', content, re.IGNORECASE):
        issues.append("Uses JSON decision format - should use stderr + exit code")
    if '"decision"' in content and 'json.dumps' in content:
        issues.append("Uses JSON decision format - should use stderr + exit code")
    
    # Check for wrong field names
    if 'tool_response' in content:
        issues.append("Uses 'tool_response' - should be 'tool_result' in PostToolUse")
    if "'params'" in content or '"params"' in content:
        issues.append("Uses 'params' - should be 'tool_input'")
    if "'parameters'" in content or '"parameters"' in content:
        if 'tool_use' not in content:  # Allow if it's fallback logic
            issues.append("Uses 'parameters' - should be 'tool_input'")
    
    # Check for wrong exit codes in exception handlers
    if re.search(r'except.*?:.*?sys\.exit\(0\)', content, re.DOTALL):
        issues.append("Uses sys.exit(0) in exception handler - should be sys.exit(1)")
    
    # Check for unnecessary fallback logic
    if "tool_use" in content and "get('name'" in content:
        issues.append("Has unnecessary fallback logic for tool names")
    
    # Check for lowercase 'bash'
    if re.search(r"tool_name.*==.*['\"]bash['\"]", content):
        issues.append("Checks for lowercase 'bash' - should be 'Bash'")
    
    return issues

def check_directory(dir_path):
    """Check all Python hooks in a directory"""
    results = {}
    
    for file_path in Path(dir_path).glob('*.py'):
        if file_path.name.startswith('_'):
            continue
        issues = check_hook(file_path)
        if issues:
            results[str(file_path.relative_to(dir_path.parent))] = issues
    
    return results

def main():
    hooks_dir = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude/hooks")
    
    directories = [
        'pre-tool-use',
        'post-tool-use',
        'notification',
        'stop',
        'sub-agent-stop',
        'user-prompt-submit',
        'pre-compact'
    ]
    
    all_results = {}
    total_issues = 0
    
    for dir_name in directories:
        dir_path = hooks_dir / dir_name
        if dir_path.exists():
            results = check_directory(dir_path)
            if results:
                all_results[dir_name] = results
                total_issues += sum(len(issues) for issues in results.values())
    
    # Print results
    print("# Hook Compliance Check Results\n")
    print(f"Total hooks with issues: {sum(len(v) for v in all_results.values())}")
    print(f"Total issues found: {total_issues}\n")
    
    for dir_name, hooks in all_results.items():
        print(f"\n## {dir_name}/")
        for hook_name, issues in sorted(hooks.items()):
            print(f"\n### {hook_name}")
            for issue in issues:
                print(f"- {issue}")
    
    # Print summary
    print("\n## Summary of Required Fixes\n")
    
    # Count issue types
    issue_counts = {}
    for dir_hooks in all_results.values():
        for issues in dir_hooks.values():
            for issue in issues:
                key = issue.split(' - ')[0].split(':')[0]
                issue_counts[key] = issue_counts.get(key, 0) + 1
    
    for issue_type, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"- {issue_type}: {count} occurrences")

if __name__ == "__main__":
    main()
