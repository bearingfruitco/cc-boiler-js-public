#!/usr/bin/env python3
"""
Security Analyzer - Post Tool Hook
Analyzes created files and suggests security improvements
"""

import json
import sys
import os
from pathlib import Path

def get_security_suggestions(file_path, operation):
    """Generate security suggestions based on what was created"""
    suggestions = []
    
    # API route suggestions
    if '/api/' in file_path and file_path.endswith('.ts'):
        suggestions.extend([
            f"Run: /security-audit {file_path}",
            f"Add rate limiting: /enhance-api security {os.path.basename(file_path)}",
            "Generate tests: /test-security api"
        ])
    
    # Form component suggestions
    elif any(indicator in file_path for indicator in ['form', 'Form', 'contact', 'Contact']):
        suggestions.extend([
            f"Add CAPTCHA: /enhance-form security {os.path.basename(file_path)}",
            "Validate PII handling: /validate-pii-handling",
            "Audit form security: /audit-form-security"
        ])
    
    # Database/model suggestions
    elif any(indicator in file_path for indicator in ['schema', 'model', 'db/', 'database']):
        suggestions.extend([
            "Generate RLS policies: /generate-rls",
            "Review data access: /security-audit database",
            "Add field encryption: /enhance-security encryption"
        ])
    
    # General suggestions for new files
    if operation == 'Write':
        suggestions.append("Quick security check: /security-check current")
    
    return suggestions

def check_security_status():
    """Check overall security status of the project"""
    status = {
        'apis_without_rate_limit': [],
        'forms_without_captcha': [],
        'tables_without_rls': [],
        'last_security_audit': None
    }
    
    # This would normally check actual files
    # For now, return empty status
    return status

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool information
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        tool_result = input_data.get('tool_result', {})
        
        # Only analyze successful file operations
        if tool_name not in ['Write', 'Edit'] or not tool_result.get('success', True):
            sys.exit(0)
        
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        suggestions = get_security_suggestions(file_path, tool_name)
        
        if suggestions:
            output = "\n🔒 Security Next Steps:\n"
            for i, suggestion in enumerate(suggestions, 1):
                output += f"{i}. {suggestion}\n"
            
            # PostToolUse hooks output to stdout for transcript mode
            print(output)
        
        # Exit successfully
        sys.exit(0)
        
    except Exception as e:
        # Log error to stderr and exit
        print(f"Security analyzer error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
