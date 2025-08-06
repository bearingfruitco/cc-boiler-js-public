#!/usr/bin/env python3
"""
Test Claude Code Hooks - Validate they follow official specification
"""

import json
import subprocess
import sys
from pathlib import Path

def test_hook(hook_path, test_input, expected_exit_code, description):
    """Test a single hook with given input"""
    try:
        result = subprocess.run(
            ['python3', str(hook_path)],
            input=json.dumps(test_input),
            capture_output=True,
            text=True,
            timeout=5
        )
        
        success = result.returncode == expected_exit_code
        
        if success:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            print(f"     Expected exit code: {expected_exit_code}, Got: {result.returncode}")
            if result.stderr:
                print(f"     Stderr: {result.stderr[:100]}...")
        
        return success
        
    except subprocess.TimeoutExpired:
        print(f"  ❌ {description} - TIMEOUT")
        return False
    except Exception as e:
        print(f"  ❌ {description} - ERROR: {e}")
        return False

def main():
    """Test all critical hooks"""
    print("=" * 60)
    print("Testing Claude Code Hooks")
    print("=" * 60)
    
    hooks_dir = Path('.claude/hooks/pre-tool-use')
    
    # Test cases for each hook type
    test_suites = {
        '07-pii-protection.py': [
            {
                'input': {
                    'tool_name': 'Write',
                    'tool_input': {
                        'file_path': 'test.ts',
                        'content': 'const email = "user@example.com"; console.log(email);'
                    }
                },
                'expected': 2,  # Should block
                'description': 'Block PII (email) in code'
            },
            {
                'input': {
                    'tool_name': 'Write',
                    'tool_input': {
                        'file_path': 'test.ts',
                        'content': 'const data = getUserData();'
                    }
                },
                'expected': 0,  # Should pass
                'description': 'Allow code without PII'
            },
            {
                'input': {
                    'tool_name': 'Read',
                    'tool_input': {
                        'file_path': 'test.ts'
                    }
                },
                'expected': 0,  # Should pass (not a write)
                'description': 'Ignore non-write operations'
            }
        ],
        
        '16-tcpa-compliance.py': [
            {
                'input': {
                    'tool_name': 'Write',
                    'tool_input': {
                        'file_path': 'ContactForm.tsx',
                        'content': '<input type="tel" name="phone" />'
                    }
                },
                'expected': 2,  # Should block
                'description': 'Block phone field without consent'
            },
            {
                'input': {
                    'tool_name': 'Write',
                    'tool_input': {
                        'file_path': 'ContactForm.tsx',
                        'content': '<input type="tel" name="phone" />\n<p>By providing your phone number, you consent to receive text messages. Message and data rates may apply. Reply STOP to cancel.</p>'
                    }
                },
                'expected': 0,  # Should pass
                'description': 'Allow phone field with consent language'
            }
        ],
        
        '22-security-validator.py': [
            {
                'input': {
                    'tool_name': 'Write',
                    'tool_input': {
                        'file_path': '/api/test.ts',
                        'content': 'const data = await req.json(); // Use data directly'
                    }
                },
                'expected': 1,  # Should warn (non-blocking)
                'description': 'Warn about unvalidated input'
            },
            {
                'input': {
                    'tool_name': 'Write',
                    'tool_input': {
                        'file_path': '/api/test.ts',
                        'content': 'const data = schema.parse(await req.json());'
                    }
                },
                'expected': 0,  # Should pass
                'description': 'Allow validated input'
            }
        ],
        
        '02-design-check.py': [
            {
                'input': {
                    'tool_name': 'Write',
                    'tool_input': {
                        'file_path': 'Button.tsx',
                        'content': '<button className="text-sm font-bold">Click</button>'
                    }
                },
                'expected': 2,  # Should block
                'description': 'Block forbidden text size and weight'
            },
            {
                'input': {
                    'tool_name': 'Write',
                    'tool_input': {
                        'file_path': 'Button.tsx',
                        'content': '<button className="text-size-3 font-semibold h-12">Click</button>'
                    }
                },
                'expected': 0,  # Should pass
                'description': 'Allow compliant design tokens'
            }
        ]
    }
    
    # Run tests
    total_tests = 0
    passed_tests = 0
    
    for hook_name, tests in test_suites.items():
        hook_path = hooks_dir / hook_name
        
        # Try the fixed version first
        fixed_path = hooks_dir / hook_name.replace('.py', '-FIXED-OFFICIAL.py')
        if fixed_path.exists():
            hook_path = fixed_path
        
        if not hook_path.exists():
            print(f"\n❌ {hook_name}: NOT FOUND")
            continue
        
        print(f"\nTesting {hook_name}:")
        
        for test in tests:
            total_tests += 1
            if test_hook(hook_path, test['input'], test['expected'], test['description']):
                passed_tests += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Test Results: {passed_tests}/{total_tests} passed")
    
    if passed_tests == total_tests:
        print("✅ All tests passed!")
    else:
        print(f"❌ {total_tests - passed_tests} tests failed")
    
    print("=" * 60)
    
    # Additional validation: Check for old patterns
    print("\nChecking for old patterns in hooks...")
    
    issues_found = False
    for hook_file in hooks_dir.glob('*.py'):
        if 'FIXED' in hook_file.name or 'OFFICIAL' in hook_file.name:
            continue
        
        with open(hook_file, 'r') as f:
            content = f.read()
        
        issues = []
        if '"decision"' in content and '"block"' in content:
            issues.append("old decision:block format")
        if 'write_file' in content or 'edit_file' in content:
            issues.append("old tool names")
        
        if issues:
            issues_found = True
            print(f"  ⚠️ {hook_file.name}: {', '.join(issues)}")
    
    if not issues_found:
        print("  ✅ No old patterns found!")
    
    return 0 if passed_tests == total_tests else 1

if __name__ == '__main__':
    import os
    os.chdir('/Users/shawnsmith/dev/bfc/boilerplate')
    sys.exit(main())
