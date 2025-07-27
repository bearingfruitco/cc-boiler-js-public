#!/usr/bin/env python3
"""
Test Auto-Runner Hook - Runs tests after code changes
Follows official Claude Code PostToolUse hook format
"""

import json
import sys
import subprocess
from pathlib import Path

def main():
    try:
        # Read input from stdin as per official docs
        input_data = json.loads(sys.stdin.read())
        
        # Extract fields for PostToolUse
        session_id = input_data.get('session_id')
        tool_name = input_data.get('tool_name')
        tool_input = input_data.get('tool_input', {})
        tool_response = input_data.get('tool_response', {})
        
        # Only process successful Write/Edit operations
        if tool_name not in ['Write', 'Edit']:
            sys.exit(0)
            
        # Check if the tool succeeded
        if not tool_response.get('success', False):
            sys.exit(0)
        
        file_path = tool_input.get('file_path', '')
        
        # Skip test files
        if any(x in file_path for x in ['.test.', '.spec.', '__tests__']):
            sys.exit(0)
        
        # Skip non-code files
        if not any(ext in file_path for ext in ['.tsx', '.ts', '.jsx', '.js']):
            sys.exit(0)
        
        # Extract component/feature name
        feature_name = Path(file_path).stem
        
        # Find related test files
        test_patterns = [
            f"**/{feature_name}.test.tsx",
            f"**/{feature_name}.test.ts",
            f"**/{feature_name}.spec.tsx",
            f"**/{feature_name}.spec.ts",
            f"**/__tests__/{feature_name}.tsx",
            f"**/__tests__/{feature_name}.ts"
        ]
        
        test_files = []
        for pattern in test_patterns:
            test_files.extend(Path(".").glob(pattern))
        
        if not test_files:
            # No tests to run
            sys.exit(0)
        
        # Run tests for the changed file
        failed_tests = []
        passed_tests = []
        
        for test_file in test_files[:3]:  # Limit to first 3 to avoid timeout
            try:
                result = subprocess.run(
                    ["npm", "test", str(test_file), "--", "--run", "--silent"],
                    capture_output=True,
                    text=True,
                    timeout=15
                )
                
                if result.returncode == 0:
                    passed_tests.append(test_file)
                else:
                    failed_tests.append((test_file, result.stdout + result.stderr))
                    
            except subprocess.TimeoutExpired:
                failed_tests.append((test_file, "Test timed out"))
            except Exception as e:
                failed_tests.append((test_file, str(e)))
        
        # Report results
        if failed_tests and not passed_tests:
            # All tests failing - this is concerning
            message = f"❌ Tests Failing After Changes!\n\n"
            message += f"Modified: {file_path}\n\n"
            message += "Failed tests:\n"
            
            for test_file, error in failed_tests:
                message += f"\n{test_file.name}:\n"
                # Show first few lines of error
                error_lines = error.strip().split('\n')[:5]
                for line in error_lines:
                    message += f"  {line}\n"
            
            message += f"\nRun manually: npm test {feature_name}.test"
            
            # PostToolUse hooks output to stdout for visibility
            print(message)
            sys.exit(0)
            
        elif failed_tests and passed_tests:
            # Some tests failing - warn but don't block
            message = f"⚠️  Some tests failing for {feature_name}\n"
            message += f"Passed: {len(passed_tests)}, Failed: {len(failed_tests)}"
            
            # Output warning to stdout
            print(message)
            sys.exit(0)
            
        elif passed_tests:
            # All tests passing - great!
            # PostToolUse hooks can output to stdout for transcript mode
            message = f"✅ TDD: All tests passing for {feature_name} ({len(passed_tests)} tests)"
            print(message)
            sys.exit(0)
        
        # No tests were run
        sys.exit(0)
        
    except Exception as e:
        # Non-blocking error
        print(f"Test runner error: {str(e)}", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
