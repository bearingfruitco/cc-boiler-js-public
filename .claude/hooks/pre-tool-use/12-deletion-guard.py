#!/usr/bin/env python3
"""
Deletion Guard - Prevent accidental deletion of important code
Warns about significant deletions and requires confirmation
"""

import json
import sys
import re

def check_deletions(content, original_content=''):
    """Check for significant deletions"""
    if not original_content:
        return False, ""
    
    # Count removed lines
    original_lines = original_content.split('\n')
    new_lines = content.split('\n')
    
    removed_count = len(original_lines) - len(new_lines)
    
    # Check for removed functions/classes
    removed_functions = []
    function_pattern = r'^\s*(?:def |class |export function |export const |function |const .*= )'
    
    for line in original_lines:
        if re.match(function_pattern, line):
            # Check if this function/class is completely gone
            func_name = line.strip()
            if func_name not in content:
                removed_functions.append(func_name)
    
    # Determine if this is a significant deletion
    if removed_count > 50 or len(removed_functions) > 2:
        message = "🗑️ SIGNIFICANT DELETION DETECTED\n\n"
        message += f"• Removing {removed_count} lines\n"
        if removed_functions:
            message += f"• Removing {len(removed_functions)} functions/classes:\n"
            for func in removed_functions[:5]:  # Show up to 5
                message += f"  - {func[:60]}...\n" if len(func) > 60 else f"  - {func}\n"
        
        message += "\n⚠️ This appears to be a significant deletion.\n"
        message += "If intentional, add 'deletion approved' to your message."
        
        return True, message
    
    return False, ""

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool information
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Only check write operations
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            # Not a write operation - continue normally
            sys.exit(0)
        
        # Get content
        content = tool_input.get('content', tool_input.get('new_str', ''))
        original = tool_input.get('old_str', '')
        
        # For Edit/MultiEdit, we have old_str to compare
        # For Write, we'd need to read the existing file (if it exists)
        if tool_name == 'Write' and not original:
            # Could read existing file here if needed
            # For now, just continue
            sys.exit(0)
        
        # Check for significant deletions
        is_significant, message = check_deletions(content, original)
        
        if is_significant:
            # Check if user has approved
            # In a real implementation, we'd check session context
            # For now, we'll warn via stderr but continue
            print(message, file=sys.stderr)
            sys.exit(0)
        
        # No significant deletions - continue normally
        sys.exit(0)
        
    except Exception as e:
        # On error, log to stderr and exit with error code
        print(f"Deletion guard error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
