#!/usr/bin/env python3
"""
Auto Test Spawner Hook - Automatically spawns TDD engineer agent for test generation
Part of v3.1 TDD Automation Enhancement
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def find_prp_for_feature(feature_name):
    """Find PRP file related to the feature"""
    prp_dir = Path("PRPs/active")
    if not prp_dir.exists():
        return None
    
    # Direct match
    direct_match = prp_dir / f"{feature_name}.md"
    if direct_match.exists():
        return direct_match
    
    # Search for mentions
    for prp_file in prp_dir.glob("*.md"):
        with open(prp_file) as f:
            content = f.read().lower()
            if feature_name.lower() in content:
                return prp_file
    
    return None

def extract_requirements_from_prp(prp_path):
    """Extract testable requirements from PRP"""
    requirements = []
    
    with open(prp_path) as f:
        content = f.read()
    
    # Extract success criteria
    lines = content.split('\n')
    in_criteria = False
    
    for line in lines:
        if any(marker in line for marker in ['Success Criteria', '✅', '## Acceptance']):
            in_criteria = True
            continue
        elif in_criteria and line.startswith('#'):
            break
        elif in_criteria and line.strip().startswith('-'):
            requirements.append(line.strip()[1:].strip())
    
    return requirements

def create_test_generation_context(feature_name, file_path, prp_path=None):
    """Create context for TDD engineer agent"""
    context = {
        "feature_name": feature_name,
        "implementation_path": file_path,
        "test_path": str(Path(file_path).parent / "__tests__" / f"{feature_name}.test.tsx"),
        "timestamp": datetime.now().isoformat(),
        "requirements": []
    }
    
    if prp_path:
        context["prp_path"] = str(prp_path)
        context["requirements"] = extract_requirements_from_prp(prp_path)
    
    # Determine component type
    if 'components/' in file_path:
        context["type"] = "component"
        context["test_focus"] = ["rendering", "props", "interactions", "accessibility"]
    elif 'app/' in file_path and 'route' in file_path:
        context["type"] = "api"
        context["test_focus"] = ["endpoints", "validation", "errors", "auth"]
    elif 'lib/' in file_path:
        context["type"] = "utility"
        context["test_focus"] = ["functions", "edge cases", "errors", "types"]
    
    return context

def spawn_tdd_engineer(context):
    """Spawn TDD engineer agent to generate tests"""
    # Create task file for agent
    task_file = Path(".claude/tasks/tdd-generation.json")
    task_file.parent.mkdir(exist_ok=True)
    
    with open(task_file, 'w') as f:
        json.dump({
            "task": "generate-tests",
            "context": context,
            "status": "pending",
            "created": datetime.now().isoformat()
        }, f, indent=2)
    
    # Create agent invocation prompt
    prompt = f"""Generate comprehensive tests for {context['feature_name']}.

Implementation file: {context['implementation_path']}
Test file to create: {context['test_path']}

Requirements to test:
{chr(10).join(f"- {req}" for req in context['requirements'])}

Focus areas: {', '.join(context['test_focus'])}

Follow TDD principles:
1. Write failing tests first
2. Cover all requirements
3. Include edge cases
4. Test error scenarios
5. Ensure accessibility
6. Add performance tests if needed

Use the project's testing patterns and design system rules."""
    
    # Log the spawning
    log_dir = Path(".claude/logs/progress")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    with open(log_dir / f"tdd-{datetime.now().strftime('%Y-%m-%d')}.log", 'a') as f:
        f.write(f"\n[{datetime.now().isoformat()}] Spawning TDD engineer for {context['feature_name']}\n")
        f.write(f"  Context: {json.dumps(context, indent=2)}\n")
    
    return prompt, task_file

def check_test_generation_status(feature_name):
    """Check if tests are being generated"""
    task_file = Path(f".claude/tasks/tdd-generation.json")
    
    if task_file.exists():
        with open(task_file) as f:
            task = json.load(f)
            
        if task.get('context', {}).get('feature_name') == feature_name:
            return task.get('status', 'unknown')
    
    return None

def main():
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Only process Write/Edit operations
        if tool_name not in ['Write', 'Edit']:
            sys.exit(0)
        
        file_path = tool_input.get('file_path', '')
        content = tool_input.get('content', '')
        
        # Skip test files
        if any(x in file_path for x in ['.test.', '.spec.', '__tests__']):
            sys.exit(0)
        
        # Check if this is new feature implementation
        is_implementation = False
        feature_name = None
        
        # Detect feature implementation
        if 'components/' in file_path and any(x in content for x in ['export function', 'export const', 'export default']):
            is_implementation = True
            feature_name = Path(file_path).stem
        elif 'app/' in file_path and 'route' in file_path:
            is_implementation = True
            feature_name = Path(file_path).parent.name
        elif 'lib/' in file_path and 'export' in content:
            is_implementation = True
            feature_name = Path(file_path).stem
        
        if not is_implementation or not feature_name:
            sys.exit(0)
        
        # Check for existing tests
        test_patterns = [
            f"**/__tests__/{feature_name}.test.tsx",
            f"**/__tests__/{feature_name}.test.ts",
            f"**/{feature_name}.test.tsx",
            f"**/{feature_name}.test.ts"
        ]
        
        test_exists = any(Path(".").glob(pattern) for pattern in test_patterns)
        
        if test_exists:
            # Tests already exist, allow implementation
            sys.exit(0)
        
        # Check if test generation is already in progress
        status = check_test_generation_status(feature_name)
        
        if status == "pending":
            # Already generating tests
            print(json.dumps({
                "decision": "block",
                "message": f"⏳ Test generation in progress for {feature_name}. Please wait..."
            }))
            sys.exit(0)
        
        # Find related PRP
        prp_path = find_prp_for_feature(feature_name)
        
        # Create context for test generation
        context = create_test_generation_context(feature_name, file_path, prp_path)
        
        # Spawn TDD engineer
        prompt, task_file = spawn_tdd_engineer(context)
        
        # Create response message
        message = f"""🤖 Auto-spawning TDD Engineer for {feature_name}

The tdd-engineer agent will now:
1. Analyze requirements{' from ' + prp_path.name if prp_path else ''}
2. Generate comprehensive test suite
3. Ensure all scenarios are covered
4. Create {context['test_path']}

This ensures TDD compliance automatically!

Please wait while tests are generated...

To check status: /tdd-status {feature_name}
To see progress: /tdd-dashboard"""
        
        # Block implementation until tests are ready
        print(json.dumps({
            "decision": "block",
            "message": message,
            "metadata": {
                "spawn_tdd_engineer": True,
                "feature": feature_name,
                "context": context,
                "prompt": prompt
            }
        }))
        
        sys.exit(0)
        
    except Exception as e:
        # Log error but don't block
        print(f"Auto test spawner error: {str(e)}", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
