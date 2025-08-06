#!/usr/bin/env python3
"""
Fix remaining exit code issues in hooks - targeted fixes only
"""

import re
from pathlib import Path

# List of hooks with their specific issues
hooks_to_fix = {
    'pre-tool-use/05c-tdd-context-loader.py': {'exit_code_lines': [118]},
    'pre-tool-use/06-requirement-drift-detector.py': {'exit_code_lines': []},  # Already fixed
    'pre-tool-use/06a-biome-lint.py': {'exit_code_lines': [202]},
    'pre-tool-use/09-auto-persona.py': {'exit_code_lines': [], 'has_fallback': True},
    'pre-tool-use/10-hydration-guard.py': {'has_fallback': True},
    'pre-tool-use/11-truth-enforcer.py': {'exit_code_lines': []},  # Already fixed
    'pre-tool-use/14-prd-clarity.py': {'has_fallback': True},
    'pre-tool-use/14a-creation-guard.py': {'has_fallback': True},
    'pre-tool-use/16a-prp-validator.py': {'has_fallback': True},
    'pre-tool-use/17-ai-docs-check.py': {'has_fallback': True},
    'pre-tool-use/18-auto-parallel-agents.py': {'has_fallback': True},
    'pre-tool-use/20-feature-awareness.py': {'exit_code_lines': []},  # Already fixed
    'pre-tool-use/26-database-environment-check.py': {'exit_code_lines': []},  # Check this
    
    'post-tool-use/01b-tdd-progress-logger.py': {'exit_code_lines': []},
    'post-tool-use/02-coverage-tracker.py': {'exit_code_lines': []},
    'post-tool-use/02-metrics.py': {'exit_code_lines': []},
    'post-tool-use/03-pattern-learning.py': {'exit_code_lines': []},
    'post-tool-use/03a-auto-orchestrate.py': {'exit_code_lines': []},
    'post-tool-use/03b-command-logger.py': {'has_fallback': True},
    'post-tool-use/03c-response-capture.py': {'exit_code_lines': []},
    'post-tool-use/06-test-auto-runner.py': {'exit_code_lines': []},
    'post-tool-use/14-completion-verifier.py': {'field_name': 'tool_response'},
    
    'notification/worktree-awareness.py': {'exit_code_lines': []},
    'user-prompt-submit/02-security-suggester.py': {'exit_code_lines': []},
}

def check_hook(file_path):
    """Check what needs fixing in a hook"""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    issues = []
    
    # Check for sys.exit(0) in exception handlers
    in_except = False
    for i, line in enumerate(lines):
        if 'except' in line and ':' in line:
            in_except = True
        elif in_except and 'sys.exit(0)' in line:
            issues.append(f"Line {i+1}: sys.exit(0) in exception handler")
            in_except = False
        elif in_except and not line.strip().startswith('#') and line.strip() != '':
            if 'except' not in line and 'pass' not in line and 'print' not in line:
                in_except = False
    
    # Check for fallback logic
    content = ''.join(lines)
    if "'tool_use' in input_data" in content and "get('name'" in content:
        issues.append("Has fallback logic for tool names")
    
    # Check for tool_response
    if "'tool_response'" in content:
        issues.append("Uses 'tool_response' instead of 'tool_result'")
        
    return issues

# Check all hooks
hooks_dir = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude/hooks")

for hook_path, expected_issues in hooks_to_fix.items():
    full_path = hooks_dir / hook_path
    if full_path.exists():
        issues = check_hook(full_path)
        if issues:
            print(f"\n{hook_path}:")
            for issue in issues:
                print(f"  - {issue}")
