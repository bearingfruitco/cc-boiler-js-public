#!/usr/bin/env python3
"""
Test Runner Hook - Automatically runs tests after implementation changes
Ensures code changes don't break existing tests
"""

import json
import sys
import subprocess
from pathlib import Path

def find_related_tests(file_path):
    """Find test files related to changed file"""
    # Convert component path to test path
    if 'components/' in file_path:
        component_name = Path(file_path).stem
        test_patterns = [
            f"**/{component_name}.test.tsx",
            f"**/{component_name}.test.ts",
            f"**/{component_name}.spec.tsx",
            f"**/{component_name}.spec.ts"
        ]
        
        tests = []
        for pattern in test_patterns:
            tests.extend(Path(".").glob(pattern))
        
        return tests
    
    return []

def main():
    try:
        # Read input
        input_data = json.loads(sys.stdin.read())
        
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        tool_response = input_data.get('tool_response', {})
        
        # Only process successful writes/edits
        if tool_name not in ['Write', 'Edit'] or not tool_response.get('success'):
            sys.exit(0)
        
        file_path = tool_input.get('file_path', '')
        
        # Skip test files themselves
        if any(x in file_path for x in ['.test.', '.spec.', '__tests__']):
            sys.exit(0)
        
        # Find related tests
        test_files = find_related_tests(file_path)
        
        if test_files:
            print(f"\n🧪 Running related tests for {Path(file_path).name}...")
            
            for test_file in test_files:
                result = subprocess.run(
                    ["npm", "test", str(test_file), "--", "--run"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode != 0:
                    # Tests failing - provide feedback
                    print(json.dumps({
                        "decision": "block",
                        "reason": f"❌ Tests failing after change!\n\nFile: {file_path}\nTest: {test_file}\n\nRun: npm test {test_file}\n\nFix tests or revert changes."
                    }))
                    sys.exit(0)
                else:
                    print(f"  ✅ {test_file.name} passing")
        
        sys.exit(0)
        
    except Exception as e:
        # Don't block on errors
        print(f"Test runner hook error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
