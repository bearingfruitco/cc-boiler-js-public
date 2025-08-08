#!/usr/bin/env python3
"""
Deployment Validator Hook - Ensures code is production-ready before deployment
Checks for console.logs, proper error handling, and environment variables
"""

import json
import sys
import re
import os
from pathlib import Path

def check_console_logs(content, file_path):
    """Check for console.log statements in production code"""
    if not file_path.endswith(('.ts', '.tsx', '.js', '.jsx')):
        return []
    
    violations = []
    
    # Skip test files
    if '.test.' in file_path or '.spec.' in file_path:
        return violations
    
    # Find console.log statements
    console_pattern = r'console\.(log|debug|info|warn|error|trace)\s*\('
    
    for i, line in enumerate(content.split('\n'), 1):
        if re.search(console_pattern, line):
            # Check if it's commented out
            if not line.strip().startswith('//') and not line.strip().startswith('*'):
                violations.append(f"Line {i}: Console statement found")
    
    return violations

def check_error_handling(content, file_path):
    """Check for proper error handling in async functions"""
    if not file_path.endswith(('.ts', '.tsx', '.js', '.jsx')):
        return []
    
    violations = []
    
    # Check for async functions without try-catch
    async_pattern = r'async\s+(?:function\s+)?(?:\w+\s*)?\([^)]*\)\s*(?::\s*[^{]+)?\s*{'
    try_pattern = r'\btry\s*{'
    
    # Simple check: count async functions and try blocks
    async_count = len(re.findall(async_pattern, content))
    try_count = len(re.findall(try_pattern, content))
    
    if async_count > 0 and try_count < async_count:
        violations.append(f"Found {async_count} async functions but only {try_count} try-catch blocks")
    
    # Check for unhandled promise rejections
    if '.catch(' not in content and 'Promise' in content:
        violations.append("Promises found without .catch() handlers")
    
    return violations

def check_env_variables(content, file_path):
    """Check for hardcoded values that should be environment variables"""
    if not file_path.endswith(('.ts', '.tsx', '.js', '.jsx', '.env')):
        return []
    
    violations = []
    
    # Patterns for hardcoded values
    patterns = {
        'API URLs': r'https?://(?:localhost|127\.0\.0\.1|api\.|backend\.)',
        'API Keys': r'[\'"][a-zA-Z0-9]{32,}[\'"]',
        'Secrets': r'(?:secret|key|token|password)\s*[:=]\s*[\'"][^\'"\s]+[\'"]',
        'Database URLs': r'(?:postgresql|mysql|mongodb)://[^\'"\s]+',
    }
    
    for name, pattern in patterns.items():
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            # Skip if it's already using process.env
            for match in matches:
                if 'process.env' not in content[max(0, content.find(match)-50):content.find(match)]:
                    violations.append(f"Hardcoded {name}: {match[:30]}...")
    
    return violations

def check_deployment_readiness(tool_name, tool_input):
    """Check if code is ready for deployment"""
    env = os.environ.get('NODE_ENV', 'development')
    
    # Only validate in staging/production or when deploying
    if env == 'development' and 'deploy' not in tool_name.lower():
        return None
    
    if tool_name not in ['Write', 'Edit', 'MultiEdit']:
        return None
    
    file_path = tool_input.get('file_path', tool_input.get('path', ''))
    content = tool_input.get('content', tool_input.get('new_str', ''))
    
    all_violations = []
    
    # Run all checks
    console_violations = check_console_logs(content, file_path)
    if console_violations:
        all_violations.extend([f"Console logs: {v}" for v in console_violations])
    
    error_violations = check_error_handling(content, file_path)
    if error_violations:
        all_violations.extend([f"Error handling: {v}" for v in error_violations])
    
    env_violations = check_env_variables(content, file_path)
    if env_violations:
        all_violations.extend([f"Environment: {v}" for v in env_violations])
    
    return all_violations

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool information
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Check deployment readiness
        violations = check_deployment_readiness(tool_name, tool_input)
        
        if violations:
            env = os.environ.get('NODE_ENV', 'development')
            
            if env == 'production':
                # Block in production
                error_msg = {
                    "action": "block",
                    "message": "🚫 PRODUCTION: Code not deployment-ready!\n\n"
                              "Issues found:\n" + 
                              "\n".join(f"• {v}" for v in violations) +
                              "\n\nFix these issues before deploying to production."
                }
                print(json.dumps(error_msg))
                sys.exit(1)
            else:
                # Warn in other environments
                warning_msg = {
                    "action": "allow",
                    "message": f"⚠️  Deployment readiness issues found:\n" +
                              "\n".join(f"• {v}" for v in violations[:5]) +
                              ("\n... and more" if len(violations) > 5 else "") +
                              "\n\nConsider fixing these before deployment."
                }
                print(json.dumps(warning_msg))
        
        # Allow operation to proceed
        sys.exit(0)
        
    except Exception as e:
        # In case of any error, log but allow operation
        error_output = {
            "action": "allow",
            "message": f"Deployment validator error: {str(e)}"
        }
        print(json.dumps(error_output))
        sys.exit(1)

if __name__ == '__main__':
    main()
