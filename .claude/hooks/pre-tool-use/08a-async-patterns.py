#!/usr/bin/env python3
"""Async Pattern Checker - Simplified Version"""

import json
import sys
import re

def check_async_patterns(content):
    """Check for async anti-patterns"""
    issues = []
    
    # Check for multiple sequential awaits
    sequential_awaits = re.findall(r'await\s+\w+\([^)]*\);\s*\n?\s*await\s+\w+\([^)]*\);', content)
    if len(sequential_awaits) > 2:
        issues.append(f"Found {len(sequential_awaits)} sequential awaits - consider Promise.all()")
    
    # Check for missing loading states
    if 'useState(true)' in content or 'useState(false)' in content:
        if 'loading' in content.lower() and 'await' in content:
            if not re.search(r'set\w*[Ll]oading\(true\)', content):
                issues.append("Async operation without loading state")
    
    # Check for missing error handling
    if 'try' in content and 'catch' in content:
        if 'console.log(error)' in content or 'console.error(error)' in content:
            issues.append("Error logged to console - show user-friendly message instead")
    
    return issues

def main():
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool name
        tool_name = input_data.get('tool_name', '')
        if not tool_name and 'tool_use' in input_data:
            tool_name = input_data['tool_use'].get('name', '')
        
        # Only check write operations
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            # Not a write operation - continue normally
            sys.exit(0)
        
        # Extract tool input
        tool_input = input_data.get('tool_input', {})
        if not tool_input and 'tool_use' in input_data:
            tool_input = input_data['tool_use'].get('parameters', {})
        
        # Get file path and content
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        content = tool_input.get('content', tool_input.get('new_str', ''))
        
        # Only check TypeScript/JavaScript files
        if not any(file_path.endswith(ext) for ext in ['.ts', '.tsx', '.js', '.jsx']):
            # Not a JS/TS file - continue normally
            sys.exit(0)
        
        # Check for async patterns
        issues = check_async_patterns(content)
        
        if issues:
            # Build warning message
            message = "⚡ ASYNC PATTERN SUGGESTIONS\n\n"
            for issue in issues:
                message += f"• {issue}\n"
            
            message += "\n📚 Best Practices:\n"
            message += "• Use Promise.all() for parallel operations\n"
            message += "• Always show loading states\n"
            message += "• Handle errors gracefully\n"
            
            # Output warning to stderr (shows in transcript)
            print(message, file=sys.stderr)
        
        # PreToolUse hook: Exit normally to continue with permission flow
        sys.exit(0)
            
    except Exception as e:
        # On error, log to stderr and exit with error code
        print(f"Async pattern hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
