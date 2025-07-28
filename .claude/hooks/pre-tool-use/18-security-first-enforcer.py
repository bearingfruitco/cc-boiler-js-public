#!/usr/bin/env python3
"""
Security-First API Development Enforcer
Part of v4.0 automation - Makes security checks mandatory before API creation
"""

import os
import json
import re
import sys
from pathlib import Path

def check_for_api_creation(tool_use):
    """Detect if the tool use is creating an API endpoint"""
    if tool_use.tool != 'str_replace_editor':
        return False
    
    # Check for common API patterns
    api_patterns = [
        r'app/api/.+\.ts',
        r'pages/api/.+\.ts',
        r'export\s+async\s+function\s+(GET|POST|PUT|DELETE|PATCH)',
        r'export\s+default\s+async\s+function\s+handler',
        r'NextRequest',
        r'NextResponse'
    ]
    
    path = tool_use.path or ''
    content = getattr(tool_use, 'new_str', '') or getattr(tool_use, 'content', '')
    
    # Check if it's an API file
    if 'api/' in path and path.endswith('.ts'):
        return True
    
    # Check content for API patterns
    for pattern in api_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return True
    
    return False

def check_for_security_rules(path):
    """Check if security rules exist for this API"""
    api_name = Path(path).stem
    security_files = [
        f'.claude/security/rules/{api_name}.json',
        f'.claude/security/policies/{api_name}.sql',
        f'app/api/{api_name}/security.ts',
        f'lib/security/{api_name}.ts'
    ]
    
    project_root = Path.cwd()
    for security_file in security_files:
        if (project_root / security_file).exists():
            return True
    
    return False

def generate_security_warning(path):
    """Generate a helpful warning message"""
    api_name = Path(path).stem
    
    return f"""
🔒 SECURITY-FIRST DEVELOPMENT ENFORCED

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

This is similar to TDD - no implementation without security tests!
"""

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

def main(tool_use):
    # Check if this is API creation
    if not check_for_api_creation(tool_use):
        return  # Not an API, continue normally
    
    path = tool_use.path or 'unknown'
    content = getattr(tool_use, 'new_str', '') or getattr(tool_use, 'content', '')
    
    # Check if explicitly skipping security
    if should_allow_without_security(content):
        print("⚠️  Security check skipped (--no-security flag detected)")
        print("📝 Please document why security is not needed for this endpoint")
        return
    
    # Check if security rules exist
    if not check_for_security_rules(path):
        # Block the operation
        print(generate_security_warning(path))
        
        # Suggest spawning security agent
        print("\n🤖 Auto-spawning security-auditor agent...")
        print("Run: /spawn-agent security-auditor")
        
        # Exit to prevent the tool use
        sys.exit(1)
    
    # Security rules exist, allow operation
    print("✅ Security rules detected - API creation allowed")

if __name__ == "__main__":
    import json
    tool_use_data = json.loads(os.environ.get('TOOL_USE', '{}'))
    
    # Create a simple object to hold the data
    class ToolUse:
        def __init__(self, data):
            self.tool = data.get('tool', '')
            self.path = data.get('path', '')
            for key, value in data.items():
                setattr(self, key, value)
    
    tool_use = ToolUse(tool_use_data)
    main(tool_use)
