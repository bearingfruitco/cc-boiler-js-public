#!/usr/bin/env python3
"""
Test Generation Enforcer Hook
Ensures tests are generated and passing before allowing implementation
Part of TDD workflow: PRD → PRP → Tests → Code
"""

import json
import sys
import subprocess
from pathlib import Path

def check_for_feature_context(tool_input):
    """Check if we're about to implement a feature"""
    file_path = tool_input.get('file_path', '')
    content = tool_input.get('content', '')
    
    # Indicators we're implementing a feature
    implementation_indicators = [
        'components/',
        'app/',
        'lib/',
        '.tsx',
        '.ts',
        'export function',
        'export const',
        'export class'
    ]
    
    # Exclude test files
    if any(x in file_path for x in ['.test.', '.spec.', '__tests__']):
        return None
    
    # Check if this looks like feature implementation
    if any(indicator in file_path or indicator in content for indicator in implementation_indicators):
        # Try to extract feature name from path or content
        if 'components/' in file_path:
            parts = file_path.split('/')
            if len(parts) > 2:
                return parts[2]  # e.g., components/forms/ContactForm.tsx -> ContactForm
        return "current-feature"
    
    return None

def find_related_prp(feature_name):
    """Find PRP for this feature"""
    prp_paths = [
        Path(f"PRPs/active/{feature_name}.md"),
        Path(f"PRPs/active/{feature_name.lower()}.md"),
        Path(f"PRPs/active/{feature_name.replace('Form', '-form')}.md")
    ]
    
    for path in prp_paths:
        if path.exists():
            return path
    
    # Search for any PRP mentioning this feature
    active_prps = Path("PRPs/active")
    if active_prps.exists():
        for prp_file in active_prps.glob("*.md"):
            with open(prp_file) as f:
                content = f.read()
                if feature_name.lower() in content.lower():
                    return prp_file
    
    return None

def check_for_tests(feature_name):
    """Check if tests exist for this feature"""
    test_patterns = [
        f"**/*{feature_name}.test.tsx",
        f"**/*{feature_name}.test.ts",
        f"**/*{feature_name}.spec.tsx",
        f"**/*{feature_name}.spec.ts"
    ]
    
    for pattern in test_patterns:
        test_files = list(Path(".").glob(pattern))
        if test_files:
            return test_files
    
    return []

def generate_test_requirements(prp_path):
    """Extract test requirements from PRP"""
    with open(prp_path) as f:
        content = f.read()
    
    test_requirements = []
    
    # Extract success criteria
    if "Success Criteria" in content or "✅" in content:
        lines = content.split('\n')
        in_criteria = False
        for line in lines:
            if "Success Criteria" in line or "## ✅" in line:
                in_criteria = True
                continue
            if in_criteria and line.strip().startswith('- '):
                test_requirements.append(line.strip()[2:])
            elif in_criteria and line.startswith('#'):
                break
    
    return test_requirements

def main():
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Only check Write/Edit operations
        if tool_name not in ['Write', 'Edit']:
            sys.exit(0)
        
        # Check if this is feature implementation
        feature_name = check_for_feature_context(tool_input)
        if not feature_name:
            sys.exit(0)  # Not a feature implementation
        
        # Find related PRP
        prp_path = find_related_prp(feature_name)
        if not prp_path:
            sys.exit(0)  # No PRP, so not enforcing TDD
        
        # Check for existing tests
        test_files = check_for_tests(feature_name)
        
        if not test_files:
            # No tests found - block and provide guidance
            requirements = generate_test_requirements(prp_path)
            
            message = f"🚨 TDD ENFORCEMENT: Tests Required First!\n\n"
            message += f"Feature: {feature_name}\n"
            message += f"PRP: {prp_path}\n\n"
            
            message += "No tests found. Please create tests first:\n\n"
            message += "1. Run: /prd-generate-tests " + str(prp_path) + "\n"
            message += "2. Or create manually with these requirements:\n"
            
            for req in requirements[:5]:  # Show first 5
                message += f"   - {req}\n"
            
            message += "\nTests should cover:\n"
            message += "- Component rendering\n"
            message += "- User interactions\n"
            message += "- Edge cases\n"
            message += "- Error states\n"
            
            message += "\nTDD Flow: PRD → PRP → Tests → Implementation"
            
            # Block the operation
            print(json.dumps({
                "decision": "block",
                "message": message
            }))
            sys.exit(0)
        else:
            # Tests exist - check if they're passing
            test_file = test_files[0]
            
            # Try to run the tests
            result = subprocess.run(
                ["npm", "test", str(test_file), "--", "--run"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                # Tests failing - warn but don't block
                message = f"⚠️ TDD Warning: Tests are failing!\n\n"
                message += f"Feature: {feature_name}\n"
                message += f"Test file: {test_file}\n\n"
                message += "Consider fixing tests before implementing.\n"
                message += "Run: npm test " + str(test_file)
                
                print(message, file=sys.stderr)
                sys.exit(0)  # Non-blocking warning
            else:
                # Tests passing - good to go
                print(json.dumps({
                    "decision": "approve"
                }))
                sys.exit(0)
        
    except Exception as e:
        # Don't block on errors
        print(f"TDD hook error: {e}", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
