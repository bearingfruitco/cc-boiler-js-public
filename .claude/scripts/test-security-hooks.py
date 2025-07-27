#!/usr/bin/env python3
"""
Test Security Hooks
Verifies that security hooks are properly configured and working
"""

import json
import subprocess
import sys
import os

def test_hook(hook_path, test_input):
    """Test a hook with sample input"""
    try:
        # Run the hook
        process = subprocess.Popen(
            ['python3', hook_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(input=json.dumps(test_input))
        
        if process.returncode != 0:
            print(f"❌ Hook failed: {hook_path}")
            print(f"   Error: {stderr}")
            return False
        
        # Parse output
        if stdout.strip():
            result = json.loads(stdout)
            print(f"✅ Hook passed: {os.path.basename(hook_path)}")
            if 'message' in result:
                print(f"   Message: {result['message'][:50]}...")
            return True
        else:
            print(f"✅ Hook passed (no output): {os.path.basename(hook_path)}")
            return True
            
    except Exception as e:
        print(f"❌ Hook error: {hook_path}")
        print(f"   Exception: {str(e)}")
        return False

def main():
    print("🔍 Testing Security Hooks...\n")
    
    # Test cases
    test_cases = [
        {
            'hook': '.claude/hooks/pre-tool-use/22-security-validator.py',
            'input': {
                'toolUse': {
                    'toolName': 'write_file',
                    'params': {
                        'path': 'app/api/test/route.ts',
                        'content': 'export async function POST(req) { const data = await req.json(); return Response.json(data); }'
                    }
                }
            }
        },
        {
            'hook': '.claude/hooks/post-tool-use/16-security-analyzer.py',
            'input': {
                'toolUse': {
                    'toolName': 'write_file',
                    'params': {
                        'path': 'app/api/users/route.ts'
                    }
                },
                'toolResult': {
                    'output': 'File created successfully'
                }
            }
        },
        {
            'hook': '.claude/hooks/notification/security-alerts.py',
            'input': {
                'metadata': {
                    'last_security_alert': 0
                }
            }
        }
    ]
    
    passed = 0
    failed = 0
    
    for test in test_cases:
        if os.path.exists(test['hook']):
            if test_hook(test['hook'], test['input']):
                passed += 1
            else:
                failed += 1
        else:
            print(f"⚠️  Hook not found: {test['hook']}")
            failed += 1
    
    print(f"\n📊 Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("✅ All security hooks are working correctly!")
        return 0
    else:
        print("❌ Some hooks have issues. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
