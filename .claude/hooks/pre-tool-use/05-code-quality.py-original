#!/usr/bin/env python3
"""
Code Quality Hook - Enforce code quality standards
Inspired by community hooks but enhanced for our needs
"""

import json
import sys
import re
from pathlib import Path

def check_code_quality(content, file_path):
    """Check various code quality metrics"""
    issues = []
    
    # Check for console.logs in production code
    if not any(test in file_path for test in ['.test.', '.spec.', 'test/']):
        console_logs = len(re.findall(r'console\.(log|error|warn|info)', content))
        if console_logs > 0:
            issues.append({
                'type': 'console-log',
                'severity': 'warning',
                'message': f'Found {console_logs} console statements in production code'
            })
    
    # Check for TODO comments that need tracking
    todos = re.findall(r'//\s*TODO:?\s*(.+?)(?:\n|$)', content, re.IGNORECASE)
    if todos:
        issues.append({
            'type': 'untracked-todo',
            'severity': 'info',
            'message': f'Found {len(todos)} TODO comments',
            'todos': todos[:3]  # First 3
        })
    
    # Check for any or unknown types in TypeScript
    if file_path.endswith(('.ts', '.tsx')):
        any_types = len(re.findall(r':\s*any\b', content))
        if any_types > 0:
            issues.append({
                'type': 'any-type',
                'severity': 'warning',
                'message': f'Found {any_types} uses of "any" type'
            })
    
    # Check for missing error handling
    try_without_catch = len(re.findall(r'\btry\s*{(?:(?!catch).)*?}\s*(?!catch)', content, re.DOTALL))
    if try_without_catch > 0:
        issues.append({
            'type': 'missing-error-handling',
            'severity': 'error',
            'message': 'Found try block without catch'
        })
    
    # Check component file structure
    if '/components/' in file_path and file_path.endswith('.tsx'):
        has_interface = 'interface' in content or 'type' in content
        has_export = 'export' in content
        
        if not has_interface:
            issues.append({
                'type': 'missing-types',
                'severity': 'warning',
                'message': 'Component missing TypeScript interface/type'
            })
        
        if not has_export:
            issues.append({
                'type': 'missing-export',
                'severity': 'error',
                'message': 'Component missing export'
            })
    
    return issues

def calculate_complexity(content):
    """Simple cyclomatic complexity estimate"""
    complexity_indicators = [
        r'\bif\b',
        r'\belse\b',
        r'\bfor\b',
        r'\bwhile\b',
        r'\bcase\b',
        r'\bcatch\b',
        r'\?.*:',  # ternary
        r'&&',
        r'\|\|'
    ]
    
    complexity = 1  # Base complexity
    for pattern in complexity_indicators:
        complexity += len(re.findall(pattern, content))
    
    return complexity

def format_quality_report(issues, complexity, file_path):
    """Format quality issues into readable report"""
    if not issues and complexity < 10:
        return None
    
    report = f"📊 Code Quality Check: {Path(file_path).name}\n\n"
    
    # Complexity warning
    if complexity > 15:
        report += f"⚠️ High Complexity: {complexity} (consider refactoring)\n\n"
    
    # Group by severity
    errors = [i for i in issues if i['severity'] == 'error']
    warnings = [i for i in issues if i['severity'] == 'warning']
    info = [i for i in issues if i['severity'] == 'info']
    
    if errors:
        report += "❌ Errors (must fix):\n"
        for issue in errors:
            report += f"  • {issue['message']}\n"
    
    if warnings:
        report += "\n⚠️ Warnings (should fix):\n"
        for issue in warnings:
            report += f"  • {issue['message']}\n"
    
    if info:
        report += "\n💡 Info:\n"
        for issue in info:
            report += f"  • {issue['message']}\n"
            if issue['type'] == 'untracked-todo' and issue.get('todos'):
                for todo in issue['todos']:
                    report += f"    - TODO: {todo}\n"
    
    return report

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool name
        tool_name = input_data.get('tool_name', '')
        
        # Only check on write operations
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            # Not a write operation - continue normally
            sys.exit(0)
        
        # Extract parameters
        tool_input = input_data.get('tool_input', {})
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        content = tool_input.get('content', tool_input.get('new_str', ''))
        
        # Skip non-code files
        if not any(file_path.endswith(ext) for ext in ['.ts', '.tsx', '.js', '.jsx']):
            sys.exit(0)
        
        # Check code quality
        issues = check_code_quality(content, file_path)
        complexity = calculate_complexity(content)
        
        # Generate report
        report = format_quality_report(issues, complexity, file_path)
        
        if report:
            # Get severity level
            has_errors = any(i['severity'] == 'error' for i in issues)
            
            if has_errors:
                # Block on errors using official format
                print(report, file=sys.stderr)
                sys.exit(2)  # Block operation
            else:
                # Warn on warnings/info - output to stderr
                print(report, file=sys.stderr)
        
        # Continue normally
        sys.exit(0)
            
    except Exception as e:
        # On error, log to stderr and continue (non-blocking)
        print(f"Code quality hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)  # Non-blocking error

if __name__ == "__main__":
    main()
