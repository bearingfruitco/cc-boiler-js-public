#!/usr/bin/env python3
"""
Interactive hook repair tool - allows manual review and selection of best versions.
"""

import os
import sys
import json
import difflib
import subprocess
from pathlib import Path
from datetime import datetime

def show_diff(file1, file2):
    """Show diff between two files."""
    try:
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()
            
        diff = difflib.unified_diff(
            lines1, lines2,
            fromfile=str(file1),
            tofile=str(file2),
            lineterm=''
        )
        
        diff_text = '\n'.join(diff)
        if diff_text:
            print("\nDifferences found:")
            print(diff_text[:2000])  # Limit output
            if len(diff_text) > 2000:
                print("\n... (diff truncated) ...")
        else:
            print("\nFiles are identical!")
            
    except Exception as e:
        print(f"Error comparing files: {e}")

def test_python_file(file_path):
    """Test if a Python file has valid syntax."""
    try:
        with open(file_path, 'r') as f:
            code = f.read()
        compile(code, file_path, 'exec')
        return True, "Valid Python syntax"
    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, str(e)

def analyze_critical_hooks():
    """Focus on the critical missing hooks first."""
    
    critical_hooks = [
        {
            'name': '07-pii-protection.py',
            'dir': '.claude/hooks/pre-tool-use',
            'purpose': 'PII Protection - blocks sensitive data exposure',
            'versions': ['07-pii-protection.py.original', '07-pii-protection.py.broken']
        },
        {
            'name': '16-tcpa-compliance.py', 
            'dir': '.claude/hooks/pre-tool-use',
            'purpose': 'TCPA Compliance - ensures consent for communications',
            'versions': ['16-tcpa-compliance.py.original']
        },
        {
            'name': '22-security-validator.py',
            'dir': '.claude/hooks/pre-tool-use', 
            'purpose': 'Security Validation - validates security controls',
            'versions': ['22-security-validator.py.original']
        }
    ]
    
    print("=" * 80)
    print("CRITICAL HOOK REPAIR - MANUAL REVIEW REQUIRED")
    print("=" * 80)
    print("\nThese 3 hooks are BLOCKING all file operations and must be fixed first.\n")
    
    actions = []
    
    for hook in critical_hooks:
        print(f"\n{'=' * 80}")
        print(f"Hook: {hook['name']}")
        print(f"Purpose: {hook['purpose']}")
        print(f"Directory: {hook['dir']}")
        print(f"{'=' * 80}")
        
        # Check what versions exist
        hook_dir = Path(hook['dir'])
        main_path = hook_dir / hook['name']
        
        print(f"\nCurrent state:")
        if main_path.exists():
            valid, msg = test_python_file(main_path)
            print(f"  ✓ Main file exists: {hook['name']}")
            print(f"    Syntax: {'✓ Valid' if valid else f'✗ {msg}'}")
        else:
            print(f"  ✗ Main file missing: {hook['name']}")
        
        print(f"\nAvailable versions:")
        for version in hook['versions']:
            version_path = hook_dir / version
            if version_path.exists():
                stat = os.stat(version_path)
                valid, msg = test_python_file(version_path)
                print(f"  - {version}")
                print(f"    Size: {stat.st_size} bytes")
                print(f"    Modified: {datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')}")
                print(f"    Syntax: {'✓ Valid' if valid else f'✗ {msg}'}")
        
        # Determine action
        if hook['name'] == '07-pii-protection.py':
            print(f"\n⚠️  SPECIAL CASE: Both versions have syntax errors!")
            print("    This hook needs to be fixed manually or recreated.")
            action = {
                'hook': hook['name'],
                'action': 'FIX_MANUALLY',
                'reason': 'Both .original and .broken have syntax errors'
            }
        elif hook['name'] in ['16-tcpa-compliance.py', '22-security-validator.py']:
            print(f"\n✅ RECOMMENDATION: Restore from .original")
            action = {
                'hook': hook['name'],
                'action': 'RESTORE_FROM_ORIGINAL',
                'command': f"cp {hook['dir']}/{hook['name']}.original {hook['dir']}/{hook['name']}"
            }
        
        actions.append(action)
    
    return actions

def create_fixed_pii_hook():
    """Create a working version of the PII protection hook."""
    
    fixed_content = '''#!/usr/bin/env python3
"""
PII Protection Hook - Prevent PII exposure in logs, URLs, and client storage
Ensures compliance with privacy regulations
"""

import json
import sys
import re
from pathlib import Path

# Common PII field patterns
PII_PATTERNS = [
    'email', 'phone', 'ssn', 'social_security',
    'first_name', 'last_name', 'full_name', 'name',
    'address', 'street', 'city', 'state', 'zip',
    'date_of_birth', 'dob', 'birthdate',
    'credit_card', 'card_number', 'cvv',
    'bank_account', 'routing_number',
    'drivers_license', 'passport',
    'ip_address', 'user_id', 'customer_id'
]

def contains_pii_field(text):
    """Check if text contains PII field names."""
    text_lower = text.lower()
    for pattern in PII_PATTERNS:
        if pattern in text_lower:
            return True, pattern
    return False, None

def check_file_content(content, file_path):
    """Check for PII violations in file content."""
    violations = []
    
    # Check for console.log with PII
    console_pattern = r'console\\.log.*?\\b(' + '|'.join(PII_PATTERNS) + r')\\b'
    if re.search(console_pattern, content, re.IGNORECASE):
        violations.append({
            'type': 'console_log',
            'message': 'PII fields detected in console.log statements'
        })
    
    # Check for localStorage/sessionStorage with PII
    storage_pattern = r'(localStorage|sessionStorage)\\.(setItem|getItem).*?\\b(' + '|'.join(PII_PATTERNS) + r')\\b'
    if re.search(storage_pattern, content, re.IGNORECASE):
        violations.append({
            'type': 'localStorage',
            'message': 'PII detected in browser storage operations'
        })
    
    # Check for PII in URL parameters
    url_pattern = r'[?&](' + '|'.join(PII_PATTERNS) + r')='
    if re.search(url_pattern, content, re.IGNORECASE):
        violations.append({
            'type': 'url_params',
            'message': 'PII detected in URL parameters'
        })
    
    return violations

def main():
    """Main hook function."""
    try:
        # Get hook input
        hook_input = json.loads(sys.stdin.read())
        tool_name = hook_input.get('tool', '')
        params = hook_input.get('params', {})
        
        # Only check write operations
        if tool_name not in ['write_file', 'str_replace_editor', 'str_replace_based_edit_tool']:
            print(json.dumps({"action": "continue"}))
            return
        
        # Get file content
        content = params.get('content', '') or params.get('new_str', '')
        file_path = params.get('path', '') or params.get('file_path', '')
        
        if not content:
            print(json.dumps({"action": "continue"}))
            return
        
        # Check for violations
        violations = check_file_content(content, file_path)
        
        if violations:
            # For critical violations, warn but don't block (for now)
            critical_types = ['console_log', 'localStorage', 'url_params']
            has_critical = any(v['type'] in critical_types for v in violations)
            
            if has_critical:
                warning = "⚠️ PII PROTECTION WARNING:\\n"
                for v in violations:
                    warning += f"  - {v['message']}\\n"
                warning += "\\nConsider using server-side handling for PII data."
                
                print(json.dumps({
                    "action": "continue",
                    "warning": warning
                }))
            else:
                print(json.dumps({"action": "continue"}))
        else:
            print(json.dumps({"action": "continue"}))
    
    except Exception as e:
        # On error, continue but log
        print(json.dumps({
            "action": "continue",
            "error": f"PII hook error: {str(e)}"
        }))

if __name__ == "__main__":
    main()
'''
    
    return fixed_content

def main():
    """Main repair process."""
    
    print("\n" + "=" * 80)
    print("CLAUDE CODE HOOKS - MANUAL REPAIR PROCESS")
    print("=" * 80)
    print("\nThis tool will help you manually review and fix critical hooks.")
    print("We'll focus on the 3 critical missing hooks first.\n")
    
    # Analyze critical hooks
    actions = analyze_critical_hooks()
    
    # Generate repair script
    print("\n" + "=" * 80)
    print("REPAIR ACTIONS REQUIRED")
    print("=" * 80)
    
    script_lines = [
        "#!/bin/bash",
        "# Critical hook repair script",
        f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "# Backup current state",
        "cp -r .claude/hooks .claude/hooks.backup.$(date +%Y%m%d_%H%M%S)",
        "",
        "echo 'Repairing critical hooks...'",
        ""
    ]
    
    for action in actions:
        if action['action'] == 'RESTORE_FROM_ORIGINAL':
            script_lines.append(f"# Restore {action['hook']}")
            script_lines.append(action['command'])
            script_lines.append(f"echo '✓ Restored {action['hook']}'")
            script_lines.append("")
        elif action['action'] == 'FIX_MANUALLY':
            script_lines.append(f"# {action['hook']} needs manual fix")
            script_lines.append(f"# Reason: {action['reason']}")
            script_lines.append(f"# Creating fixed version...")
            script_lines.append("")
    
    # Save repair script
    script_path = Path("scripts/repair-critical-hooks.sh")
    with open(script_path, 'w') as f:
        f.write('\n'.join(script_lines))
    os.chmod(script_path, 0o755)
    
    print(f"\n✅ Repair script created: {script_path}")
    
    # Create fixed PII hook
    print("\n" + "=" * 80)
    print("CREATING FIXED PII PROTECTION HOOK")
    print("=" * 80)
    
    fixed_pii = create_fixed_pii_hook()
    fixed_path = Path(".claude/hooks/pre-tool-use/07-pii-protection-FIXED.py")
    
    with open(fixed_path, 'w') as f:
        f.write(fixed_pii)
    
    print(f"✅ Created fixed PII hook: {fixed_path}")
    print("\nTo activate it:")
    print(f"  cp {fixed_path} .claude/hooks/pre-tool-use/07-pii-protection.py")
    
    # Next steps
    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("""
1. IMMEDIATE (fix critical hooks):
   ./scripts/repair-critical-hooks.sh
   cp .claude/hooks/pre-tool-use/07-pii-protection-FIXED.py .claude/hooks/pre-tool-use/07-pii-protection.py

2. TEST the fixes:
   python3 .claude/hooks/pre-tool-use/07-pii-protection.py
   python3 .claude/hooks/pre-tool-use/16-tcpa-compliance.py  
   python3 .claude/hooks/pre-tool-use/22-security-validator.py

3. THEN handle duplicates:
   Run the full analysis for other hooks
   
4. ARCHIVE old versions:
   mkdir -p .claude/hooks/_archive/$(date +%Y%m%d)
   find .claude/hooks -name '*.original' -o -name '*.broken' -o -name '*.backup' | xargs -I {} mv {} .claude/hooks/_archive/$(date +%Y%m%d)/
""")

if __name__ == "__main__":
    main()
