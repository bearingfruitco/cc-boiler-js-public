#!/usr/bin/env python3
"""
PII Protection Hook - Prevent PII exposure in logs, URLs, and client storage
Ensures compliance with privacy regulations
"""

import json
import sys
import re
from pathlib import Path

# Load field registry
def load_field_registry():
    """Load field definitions from registry"""
    registry_path = Path(__file__).parent.parent.parent.parent / 'field-registry'
    
    pii_fields = set()
    phi_fields = set()
    sensitive_fields = set()
    
    # Common PII field patterns
    pii_patterns = [
        'email', 'phone', 'ssn', 'social_security',
        'first_name', 'last_name', 'full_name', 'name',
        'address', 'street', 'city', 'state', 'zip',
        'date_of_birth', 'dob', 'birthdate',
        'credit_card', 'card_number', 'cvv',
        'bank_account', 'routing_number',
        'drivers_license', 'passport',
        'ip_address', 'user_id', 'customer_id'
    ]
    
    # Add patterns to sets
    for pattern in pii_patterns:
        pii_fields.add(pattern)
        sensitive_fields.add(pattern)
    
    # Try to load from actual registry
    try:
        core_fields = registry_path / 'core' / 'tracking-fields.json'
        if core_fields.exists():
            import json as json_lib
            with open(core_fields) as f:
                fields = json_lib.load(f)
                for field_name, field_def in fields.items():
                    if field_def.get('pii'):
                        pii_fields.add(field_name.lower())
                    if field_def.get('phi'):
                        phi_fields.add(field_name.lower())
                    if field_def.get('sensitive'):
                        sensitive_fields.add(field_name.lower())
    except:
        pass  # Use defaults if registry not available
    
    return pii_fields, phi_fields, sensitive_fields

# Load fields once
PII_FIELDS, PHI_FIELDS, SENSITIVE_FIELDS = load_field_registry()

def check_file_content(content, file_path):
    """Check file content for PII violations"""
    violations = []
    lines = content.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        line_lower = line.lower()
        
        # Check console.log with PII
        if 'console.log' in line or 'console.error' in line or 'console.warn' in line:
            for field in PII_FIELDS:
                if field in line_lower:
                    violations.append({
                        'type': 'console_log',
                        'line': line_num,
                        'field': field,
                        'content': line.strip()
                    })
        
        # Check localStorage/sessionStorage
        if 'localstorage' in line_lower or 'sessionstorage' in line_lower:
            for field in SENSITIVE_FIELDS:
                if field in line_lower:
                    violations.append({
                        'type': 'localStorage',
                        'line': line_num,
                        'field': field,
                        'content': line.strip()
                    })
        
        # Check URL parameters
        url_patterns = [
            r'[?&]email=',
            r'[?&]phone=',
            r'[?&]ssn=',
            r'[?&]name=',
            r'[?&]address=',
            r'searchParams\.set\([\'"](?:email|phone|ssn|name)',
            r'searchParams\.append\([\'"](?:email|phone|ssn|name)'
        ]
        
        for pattern in url_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                violations.append({
                    'type': 'url_params',
                    'line': line_num,
                    'pattern': pattern,
                    'content': line.strip()
                })
        
        # Check form fields without encryption
        if '<input' in line and any(field in line_lower for field in PII_FIELDS):
            if 'useFieldTracking' not in content[:lines.index(line) * 100]:  # Check context
                violations.append({
                    'type': 'unencrypted_field',
                    'line': line_num,
                    'content': line.strip()
                })
    
    return violations

def suggest_fixes(violations):
    """Suggest fixes for each violation"""
    fixes = []
    
    for v in violations:
        if v['type'] == 'console_log':
            fixes.append({
                'violation': v,
                'fix': f"Remove {v['field']} from console.log or use: console.log('User data processed') without PII"
            })
        elif v['type'] == 'localStorage':
            fixes.append({
                'violation': v,
                'fix': f"Don't store {v['field']} in localStorage. Use secure server-side storage instead."
            })
        elif v['type'] == 'url_params':
            fixes.append({
                'violation': v,
                'fix': "Don't put PII in URLs. Use POST requests or encrypted tokens instead."
            })
        elif v['type'] == 'unencrypted_field':
            fixes.append({
                'violation': v,
                'fix': "Use useFieldTracking hook for PII fields:\n  const { register } = useFieldTracking('form-name');"
            })
    
    return fixes

def format_violation_message(violations, fixes):
    """Format violations into readable message"""
    message = "🔒 PII PROTECTION VIOLATIONS\n\n"
    
    # Group by type
    by_type = {}
    for v in violations:
        if v['type'] not in by_type:
            by_type[v['type']] = []
        by_type[v['type']].append(v)
    
    # Console.log violations
    if 'console_log' in by_type:
        message += "❌ PII in Console Logs:\n"
        for v in by_type['console_log'][:3]:
            message += f"  Line {v['line']}: Logging {v['field']} field\n"
            message += f"    {v['content'][:60]}...\n"
    
    # localStorage violations
    if 'localStorage' in by_type:
        message += "\n❌ PII in Client Storage:\n"
        for v in by_type['localStorage'][:3]:
            message += f"  Line {v['line']}: Storing {v['field']} in localStorage\n"
    
    # URL violations
    if 'url_params' in by_type:
        message += "\n❌ PII in URLs:\n"
        for v in by_type['url_params'][:3]:
            message += f"  Line {v['line']}: PII in URL parameters\n"
    
    # Unencrypted fields
    if 'unencrypted_field' in by_type:
        message += "\n⚠️ Unencrypted PII Fields:\n"
        for v in by_type['unencrypted_field'][:3]:
            message += f"  Line {v['line']}: PII field without encryption\n"
    
    message += "\n📚 Security Rules:\n"
    message += "  • Never log PII to console\n"
    message += "  • Never store PII in localStorage/sessionStorage\n"
    message += "  • Never put PII in URLs or query parameters\n"
    message += "  • Always use field-level encryption for PII\n"
    message += "  • Use useFieldTracking hook for forms with PII\n"
    
    return message

def main():
    """Main hook logic"""
    try:
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool name - handle multiple formats
        tool_name = input_data.get('tool_name', '')
        if not tool_name and 'tool_use' in input_data:
            tool_name = input_data['tool_use'].get('name', '')
        
        # Only check write operations
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            sys.exit(0)
            return
        
        # Extract parameters
        tool_input = input_data.get('tool_input', {})
        if not tool_input and 'tool_use' in input_data:
            tool_input = input_data['tool_use'].get('parameters', {})
        
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        
        # Only check code files
        if not any(file_path.endswith(ext) for ext in ['.ts', '.tsx', '.js', '.jsx']):
            sys.exit(0)
            return
            
        content = tool_input.get('content', tool_input.get('new_str', ''))
        
        # Skip if no content
        if not content:
            sys.exit(0)
            return
        
        # Check for violations
        violations = check_file_content(content, file_path)
        
        if violations:
            fixes = suggest_fixes(violations)
            message = format_violation_message(violations, fixes)
            
            # For critical violations (PII in logs/storage), block
            critical_types = ['console_log', 'localStorage', 'url_params']
            has_critical = any(v['type'] in critical_types for v in violations)
            
            if has_critical:
                print(message
                , file=sys.stderr)
            sys.exit(2)
            else:
                # Warn but allow for other issues
                print(message)  # Warning
            sys.exit(0)
        else:
            sys.exit(0)
    
    except Exception as e:
        # On error, continue but log
        print(json.dumps({
            sys.exit(0)

if __name__ == "__main__":
    main()
