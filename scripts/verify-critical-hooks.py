#!/usr/bin/env python3
"""
Quick test to verify critical hooks are installed and working
"""

import json
import subprocess
import sys

def test_hook(hook_name, test_input):
    """Test a hook with given input"""
    hook_path = f".claude/hooks/pre-tool-use/{hook_name}"
    
    try:
        result = subprocess.run(
            ['python3', hook_path],
            input=json.dumps(test_input),
            capture_output=True,
            text=True,
            timeout=2
        )
        return result.returncode, result.stderr
    except Exception as e:
        return -1, str(e)

def main():
    print("=" * 60)
    print("Testing Critical Hooks")
    print("=" * 60)
    
    # Test PII Protection
    print("\n1. Testing 07-pii-protection.py...")
    code, stderr = test_hook('07-pii-protection.py', {
        'tool_name': 'Write',
        'tool_input': {
            'file_path': 'test.ts',
            'content': 'const email = "user@company.com";'
        }
    })
    if code == 2:
        print("   ✅ PII detection working (blocks with exit code 2)")
    else:
        print(f"   ❌ PII detection FAILED (exit code: {code})")
    
    # Test TCPA Compliance
    print("\n2. Testing 16-tcpa-compliance.py...")
    code, stderr = test_hook('16-tcpa-compliance.py', {
        'tool_name': 'Write',
        'tool_input': {
            'file_path': 'ContactForm.tsx',
            'content': '<input type="tel" name="phone" />'
        }
    })
    if code == 2:
        print("   ✅ TCPA compliance working (blocks with exit code 2)")
    else:
        print(f"   ❌ TCPA compliance FAILED (exit code: {code})")
    
    # Test Security Validator
    print("\n3. Testing 22-security-validator.py...")
    code, stderr = test_hook('22-security-validator.py', {
        'tool_name': 'Write',
        'tool_input': {
            'file_path': '/api/test.ts',
            'content': 'const data = await req.json();'
        }
    })
    if code == 1:  # This one warns, doesn't block
        print("   ✅ Security validator working (warns with exit code 1)")
    else:
        print(f"   ❌ Security validator FAILED (exit code: {code})")
    
    # Test Design Check
    print("\n4. Testing 02-design-check.py...")
    code, stderr = test_hook('02-design-check.py', {
        'tool_name': 'Write',
        'tool_input': {
            'file_path': 'Button.tsx',
            'content': '<button className="text-sm font-bold">Test</button>'
        }
    })
    if code == 2:
        print("   ✅ Design check working (blocks with exit code 2)")
    else:
        print(f"   ❌ Design check FAILED (exit code: {code})")
    
    print("\n" + "=" * 60)
    print("Critical hooks test complete!")
    print("Restart Claude Code to load the updated hooks.")
    print("=" * 60)

if __name__ == '__main__':
    import os
    os.chdir('/Users/shawnsmith/dev/bfc/boilerplate')
    main()
