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
            # Exit with code 0 and no output to continue with normal permission flow
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
        
        # If no tests exist, trigger auto-test-spawner
        if not test_files:
            # Check if test generation is already in progress
            task_file = Path(f".claude/tasks/tdd-generation.json")
            if task_file.exists():
                with open(task_file) as f:
                    task = json.load(f)
                    if task.get('context', {}).get('feature_name') == feature_name:
                        # Already generating tests
                        print(json.dumps({
                            "decision": "block",
                            "message": f"⏳ Test generation in progress for {feature_name}. Please wait..."
                        }))
                        sys.exit(0)
            
            # Delegate to auto-test-spawner hook
            # The auto-test-spawner will handle agent invocation
            message = "🧪 TDD Enforcer: Tests Required First\n\n"
            message += f"Feature: {feature_name}\n"
            message += f"File: {file_path}\n\n"
            
            if prp_files:
                message += f"Found PRP: {prp_files[0].name}\n\n"
            
            message += "The auto-test-spawner will now:\n"
            message += "1. Invoke the tdd-engineer agent\n"
            message += "2. Generate comprehensive tests\n"
            message += "3. Ensure TDD compliance\n\n"
            
            message += "This is now handled automatically by the TDD automation system."
            
            # Output decision - the auto-test-spawner will take over
            print(json.dumps({
                "decision": "block",
                "message": message,
                "metadata": {
                    "trigger_auto_spawner": True,
                    "feature_name": feature_name,
                    "prp_found": bool(prp_files)
                }
            }))
            sys.exit(0)
        
        # Tests exist - allow with info  
        test_list = "\n".join(f"   - {t.relative_to('.')}" for t in test_files[:3])
        
        # Auto-approve since tests exist
        print(json.dumps({
            "decision": "approve"
        }))
        sys.exit(0)
        
    except Exception as e:
        # Non-blocking error as per docs
        print(f"TDD enforcer error: {str(e)}", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
