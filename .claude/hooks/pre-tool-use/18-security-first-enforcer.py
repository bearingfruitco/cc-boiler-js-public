#!/usr/bin/env python3
"""
Security-First Enforcer Hook
Ensures security rules and tests are defined before API implementation
Similar to TDD but for security
"""

import sys
import json
import os
from pathlib import Path

def check_for_api_creation(input_data):
    """Check if this is creating an API endpoint"""
    tool_name = input_data.get('tool_name', '')
    if tool_name not in ['Write', 'Edit', 'MultiEdit']:
        return False
    
    tool_input = input_data.get('tool_input', {})
    path = tool_input.get('path', '') or tool_input.get('file_path', '')
    
    # Check for API route patterns
    api_patterns = [
        'app/api/',
        'pages/api/',
        'src/api/',
        '/routes/api/'
    ]
    
    return any(pattern in path for pattern in api_patterns) and path.endswith(('.ts', '.js', '.tsx', '.jsx'))

def check_for_security_rules(api_path):
    """Check if security rules exist for this API"""
    api_name = Path(api_path).stem
    
    # Security file patterns to check
    security_files = [
        f'.claude/security/rules/{api_name}.json',
        f'.claude/security/policies/{api_name}.md',
        f'security/rules/{api_name}.json',
        f'docs/security/{api_name}.md',
        f'.security/{api_name}.json'
    ]
    
    project_root = Path.cwd()
    for security_file in security_files:
        if (project_root / security_file).exists():
            return True
    
    return False

def generate_security_warning(path):
    """Generate a helpful warning message"""
    api_name = Path(path).stem
    
    return f"""🔒 SECURITY-FIRST DEVELOPMENT ENFORCED

You're creating an API endpoint without security rules. This violates our security-first policy.

API detected: {path}

Required before implementation:
1. Security rules and policies
2. RLS (Row Level Security) policies for Supabase
3. Permission matrix defining who can access what
4. Security tests

To proceed, either:

Option 1 - Auto-generate security (RECOMMENDED):
Use: /spawn-agent security-auditor generate-api-security {api_name}

Option 2 - Create security manually:
1. Create .claude/security/rules/{api_name}.json
2. Define RLS policies
3. Create permission tests
4. Run /verify-security {api_name}

Option 3 - Skip security (NOT RECOMMENDED):
Add --no-security flag and provide justification

This is similar to TDD - no implementation without security tests!"""

def should_allow_without_security(content):
    """Check if the operation explicitly opts out of security"""
    no_security_patterns = [
        '--no-security',
        'SKIP_SECURITY_CHECK',
        '// @security-skip:',
        '/* @no-security'
    ]
    
    for pattern in no_security_patterns:
        if pattern in content:
            return True
    
    return False

def main():
    """Main hook logic"""
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read())
        
        # Check if this is API creation
        if not check_for_api_creation(input_data):
            sys.exit(0)  # Not an API, continue normally
        
        tool_input = input_data.get('tool_input', {})
        tool_name = input_data.get('tool_name', '')
        path = tool_input.get('path', '') or tool_input.get('file_path', 'unknown')
        
        # Get content based on tool
        if tool_name == 'Write':
            content = tool_input.get('content', '')
        else:
            content = tool_input.get('new_str', '')
        
        # Check if explicitly skipping security
        if should_allow_without_security(content):
            print("⚠️  Security check skipped (--no-security flag detected)", file=sys.stderr)
            print("📝 Please document why security is not needed for this endpoint", file=sys.stderr)
            sys.exit(0)
        
        # Check if security rules exist
        if not check_for_security_rules(path):
            # Block the operation
            print(json.dumps({
                "decision": "block",
                "message": generate_security_warning(path)
            }))
            sys.exit(0)
        
        # Security rules exist, allow operation
        print("✅ Security rules detected - API creation allowed", file=sys.stderr)
        
    except Exception as e:
        # Log error to stderr and continue
        print(f"Security enforcer hook error: {str(e)}", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
