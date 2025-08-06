#!/usr/bin/env python3
"""
TDD Enforcer Hook - Ensures tests exist before implementation
Follows official Claude Code hooks documentation
"""

import json
import sys
import re
from pathlib import Path

def main():
    try:
        # Read input from stdin as per official docs
        input_data = json.loads(sys.stdin.read())
        
        # Extract fields according to PreToolUse schema
        session_id = input_data.get('session_id')
        tool_name = input_data.get('tool_name')
        tool_input = input_data.get('tool_input', {})
        
        # Only check Write/Edit operations
        if tool_name not in ['Write', 'Edit']:
            sys.exit(0)
        
        file_path = tool_input.get('file_path', '')
        content = tool_input.get('content', '')
        
        # Skip test files themselves
        if any(x in file_path for x in ['.test.', '.spec.', '__tests__', '/tests/']):
            sys.exit(0)
        
        # Skip non-implementation files
        if not any(ext in file_path for ext in ['.tsx', '.ts', '.jsx', '.js']):
            sys.exit(0)
        
        # Skip configuration and setup files
        if any(x in file_path for x in ['config', 'setup', 'types', '.d.ts', 'index.ts']):
            sys.exit(0)
        
        # Check if this is a component or feature implementation
        is_implementation = False
        feature_name = None
        
        # Check for component files
        if 'components/' in file_path and any(x in content for x in ['export function', 'export const', 'export default']):
            is_implementation = True
            # Extract component name
            path_parts = Path(file_path).parts
            if 'components' in path_parts:
                idx = path_parts.index('components')
                if idx + 1 < len(path_parts):
                    feature_name = Path(path_parts[-1]).stem
        
        # Check for lib/feature files
        elif 'lib/' in file_path and 'export' in content:
            is_implementation = True
            feature_name = Path(file_path).stem
        
        # Check for app route handlers
        elif 'app/' in file_path and 'route.ts' in file_path:
            is_implementation = True
            feature_name = Path(file_path).parent.name
        
        if not is_implementation or not feature_name:
            sys.exit(0)
        
        # Look for existing tests
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
        
        # Check for related PRP
        prp_files = []
        prp_dir = Path("PRPs/active")
        if prp_dir.exists():
            # Look for PRPs that might be related
            for prp_file in prp_dir.glob("*.md"):
                with open(prp_file) as f:
                    prp_content = f.read().lower()
                    if feature_name.lower() in prp_content:
                        prp_files.append(prp_file)
        
        # If no tests exist, provide guidance
        if not test_files:
            message = "🧪 TDD Workflow: Tests Required First\n\n"
            message += f"Implementing: {feature_name}\n"
            message += f"File: {file_path}\n\n"
            
            if prp_files:
                message += f"Found PRP: {prp_files[0].name}\n\n"
            
            message += "No tests found. Follow TDD workflow:\n\n"
            message += "1. Create test file first:\n"
            message += f"   Path: {Path(file_path).parent}/__tests__/{feature_name}.test.tsx\n\n"
            
            message += "2. Write tests for:\n"
            message += "   - Component renders without errors\n"
            message += "   - Props are handled correctly\n"
            message += "   - User interactions work\n"
            message += "   - Edge cases are covered\n"
            message += "   - Error states display properly\n\n"
            
            message += "3. Run tests (they should fail):\n"
            message += f"   npm test {feature_name}.test\n\n"
            
            message += "4. Then implement to make tests pass\n\n"
            
            message += "Or use: /tdd-workflow " + feature_name
            
            # Output decision as per official docs
            print(json.dumps({
                "decision": "block",
                "reason": message
            }))
            sys.exit(0)
        
        # Tests exist - allow with info
        test_list = "\n".join(f"   - {t.relative_to('.')}" for t in test_files[:3])
        
        print(json.dumps({
            "decision": "approve",
            "reason": f"✅ TDD: Found tests for {feature_name}\n{test_list}"
        }))
        sys.exit(0)
        
    except Exception as e:
        # Non-blocking error as per docs
        print(f"TDD enforcer error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
