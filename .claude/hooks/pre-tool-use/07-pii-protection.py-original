#!/usr/bin/env python3
"""
PII Protection Hook - Prevent PII exposure in code
Follows official Claude Code hooks specification
"""

import json
import sys
import re

# PII patterns to detect
PII_PATTERNS = {
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'phone': r'\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
    'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
    'credit_card': r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
    'ip_address': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
}

# Fields that commonly contain PII
PII_FIELD_NAMES = [
    'email', 'phone', 'ssn', 'social_security',
    'credit_card', 'card_number', 'cvv',
    'date_of_birth', 'dob', 'address',
    'full_name', 'first_name', 'last_name',
    'passport', 'driver_license'
]

def check_for_pii(content):
    """Check content for PII patterns"""
    violations = []
    
    # Check for hardcoded PII patterns
    for pii_type, pattern in PII_PATTERNS.items():
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            # Skip if it's in a comment or looks like example data
            line_start = content.rfind('\n', 0, match.start()) + 1
            line = content[line_start:content.find('\n', match.end())]
            
            # Skip comments and example data
            if '//' in line[:match.start()-line_start] or '#' in line[:match.start()-line_start]:
                continue
            if 'example' in line.lower() or 'test' in line.lower() or 'demo' in line.lower():
                continue
                
            line_num = content[:match.start()].count('\n') + 1
            violations.append(f"Line {line_num}: Potential {pii_type} detected: {match.group()[:20]}...")
    
    # Check for console.log with PII fields
    console_pattern = r'console\.(log|error|warn|info)\([^)]*\b(' + '|'.join(PII_FIELD_NAMES) + r')\b'
    for match in re.finditer(console_pattern, content, re.IGNORECASE):
        line_num = content[:match.start()].count('\n') + 1
        violations.append(f"Line {line_num}: Console logging PII field '{match.group(2)}'")
    
    # Check for PII in localStorage
    storage_pattern = r'localStorage\.(setItem|getItem)\(["\']([^"\']*(' + '|'.join(PII_FIELD_NAMES) + r')[^"\']*)["\']\s*,'
    for match in re.finditer(storage_pattern, content, re.IGNORECASE):
        line_num = content[:match.start()].count('\n') + 1
        violations.append(f"Line {line_num}: Storing PII in localStorage: '{match.group(2)}'")
    
    return violations

def main():
    """Main hook logic following official specification"""
    try:
        # Read input from stdin (official format)
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool information
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Only check write operations
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            sys.exit(0)  # Success - continue
        
        # Get file content
        content = tool_input.get('content', '')
        if 'new_str' in tool_input:  # Edit operations
            content = tool_input.get('new_str', '')
        
        # Check for PII
        violations = check_for_pii(content)
        
        if violations:
            # Block operation with exit code 2
            error_msg = "🔒 PII Protection Violation\n\n"
            error_msg += "Potential PII detected in code. This is blocked to prevent data exposure.\n\n"
            error_msg += "Violations:\n"
            for v in violations:
                error_msg += f"• {v}\n"
            error_msg += "\nSolutions:\n"
            error_msg += "• Use environment variables for sensitive data\n"
            error_msg += "• Implement field-level encryption for PII\n"
            error_msg += "• Use the field registry for approved PII handling\n"
            error_msg += "• Never log PII to console or store in localStorage\n"
            
            # Official format: stderr + exit code 2 for blocking
            print(error_msg, file=sys.stderr)
            sys.exit(2)  # Block operation
        
        # No violations - continue
        sys.exit(0)
        
    except Exception as e:
        # Non-blocking error - show to user but continue
        print(f"PII protection hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)  # Non-blocking error

if __name__ == '__main__':
    main()
