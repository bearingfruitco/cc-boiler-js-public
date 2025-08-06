#!/usr/bin/env python3
"""
TDD Context Loader - Loads project context for better test generation
Enhances TDD automation by providing rich context to the tdd-engineer agent
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def load_project_patterns():
    """Load existing test patterns from the project"""
    patterns = {
        "component_tests": [],
        "api_tests": [],
        "utility_tests": [],
        "e2e_tests": []
    }
    
    # Find example test files
    test_files = list(Path(".").glob("**/*.test.*")) + list(Path(".").glob("**/*.spec.*"))
    
    for test_file in test_files[:10]:  # Sample first 10
        try:
            with open(test_file) as f:
                content = f.read()
                
            # Categorize test patterns
            if 'render' in content and 'screen' in content:
                patterns["component_tests"].append({
                    "file": str(test_file),
                    "imports": extract_imports(content),
                    "patterns": extract_test_patterns(content)
                })
            elif 'request' in content or 'api' in content.lower():
                patterns["api_tests"].append({
                    "file": str(test_file),
                    "patterns": extract_test_patterns(content)
                })
            elif 'describe' in content and 'function' in content:
                patterns["utility_tests"].append({
                    "file": str(test_file),
                    "patterns": extract_test_patterns(content)
                })
                
        except Exception:
            continue
    
    return patterns

def extract_imports(content):
    """Extract testing library imports"""
    imports = []
    lines = content.split('\n')
    
    for line in lines:
        if 'import' in line and any(lib in line for lib in ['@testing-library', 'vitest', '@playwright']):
            imports.append(line.strip())
    
    return imports

def extract_test_patterns(content):
    """Extract common test patterns"""
    patterns = []
    
    # Look for describe blocks
    if 'describe(' in content:
        patterns.append("describe-it pattern")
    
    # Look for test blocks
    if 'test(' in content or 'it(' in content:
        patterns.append("test blocks")
    
    # Look for hooks
    if 'beforeEach' in content:
        patterns.append("beforeEach hooks")
    
    # Look for assertions
    if 'expect(' in content:
        patterns.append("expect assertions")
    
    return patterns

def load_design_system_rules():
    """Load design system rules for UI testing"""
    rules = {
        "font_sizes": ["text-size-1", "text-size-2", "text-size-3", "text-size-4"],
        "font_weights": ["font-regular", "font-semibold"],
        "spacing": ["p-1", "p-2", "p-3", "p-4", "p-6", "p-8"],
        "touch_targets": ["h-11", "h-12"],
        "colors": {
            "primary": "blue-600",
            "error": "red-600",
            "success": "green-600"
        }
    }
    
    # Check if design system doc exists
    design_doc = Path(".claude/docs/design-system.md")
    if design_doc.exists():
        rules["doc_path"] = str(design_doc)
    
    return rules

def load_prp_requirements(feature_name):
    """Load requirements from PRP if available"""
    prp_dir = Path("PRPs/active")
    requirements = []
    
    if prp_dir.exists():
        for prp_file in prp_dir.glob("*.md"):
            try:
                with open(prp_file) as f:
                    content = f.read()
                    
                if feature_name.lower() in content.lower():
                    # Extract requirements
                    lines = content.split('\n')
                    in_criteria = False
                    
                    for line in lines:
                        if any(marker in line for marker in ['Success Criteria', '✅', 'Requirements']):
                            in_criteria = True
                            continue
                        elif in_criteria and line.startswith('#'):
                            break
                        elif in_criteria and line.strip().startswith('-'):
                            requirements.append(line.strip()[1:].strip())
                    
                    if requirements:
                        return {
                            "source": str(prp_file),
                            "requirements": requirements
                        }
            except Exception:
                continue
    
    return None

def determine_test_scope(file_path, content):
    """Determine what types of tests to generate"""
    scope = {
        "unit": True,
        "integration": False,
        "e2e": False,
        "performance": False,
        "accessibility": False
    }
    
    # Component files need UI tests
    if 'components/' in file_path:
        scope["accessibility"] = True
        scope["integration"] = True
    
    # API routes need integration tests
    if 'api/' in file_path or 'route' in file_path:
        scope["integration"] = True
        scope["e2e"] = True
    
    # Critical paths need performance tests
    if any(critical in file_path for critical in ['auth', 'payment', 'checkout']):
        scope["performance"] = True
        scope["e2e"] = True
    
    return scope

def create_tdd_context(feature_name, file_path, content):
    """Create comprehensive context for TDD"""
    context = {
        "feature_name": feature_name,
        "file_path": file_path,
        "timestamp": datetime.now().isoformat(),
        "project_patterns": load_project_patterns(),
        "design_system": load_design_system_rules(),
        "test_scope": determine_test_scope(file_path, content),
        "stack_info": {
            "framework": "Next.js 15",
            "testing": "Vitest + React Testing Library",
            "e2e": "Playwright",
            "styling": "Tailwind CSS 4"
        }
    }
    
    # Add PRP requirements if available
    prp_data = load_prp_requirements(feature_name)
    if prp_data:
        context["requirements"] = prp_data
    
    # Add performance requirements
    if context["test_scope"]["performance"]:
        context["performance_targets"] = {
            "render_time": "< 100ms",
            "interaction_delay": "< 50ms",
            "bundle_size": "< 50KB"
        }
    
    return context

def save_context(context):
    """Save context for TDD engineer"""
    context_dir = Path(".claude/context/tdd")
    context_dir.mkdir(parents=True, exist_ok=True)
    
    context_file = context_dir / f"{context['feature_name']}-context.json"
    
    with open(context_file, 'w') as f:
        json.dump(context, f, indent=2)
    
    return context_file

def main():
    try:
        # Read input from Claude Code
        try:
            input_data = json.loads(sys.stdin.read())
        except (json.JSONDecodeError, ValueError):
            # No valid JSON on stdin (e.g., when run directly for testing)
            sys.exit(0)
        
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Only process Write/Edit operations
        if tool_name not in ['Write', 'Edit']:
            sys.exit(0)  # Exit success for non-relevant tools
        
        file_path = tool_input.get('file_path', '')
        content = tool_input.get('content', '')
        
        # Skip if not implementation
        if not any(indicator in content for indicator in ['export', 'function', 'class', 'const']):
            sys.exit(0)
        
        # Extract feature name
        feature_name = Path(file_path).stem
        
        # Create comprehensive context
        context = create_tdd_context(feature_name, file_path, content)
        
        # Save context for TDD engineer
        context_file = save_context(context)
        
        # Log context creation
        log_dir = Path(".claude/logs/progress")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        with open(log_dir / f"tdd-context-{datetime.now().strftime('%Y-%m-%d')}.log", 'a') as f:
            f.write(f"\n[{datetime.now().isoformat()}] Created TDD context for {feature_name}\n")
            f.write(f"  Context file: {context_file}\n")
            f.write(f"  Test scope: {json.dumps(context['test_scope'])}\n")
            if 'requirements' in context:
                f.write(f"  Requirements found: {len(context['requirements']['requirements'])}\n")
        
        # PreToolUse hooks exit normally
        sys.exit(0)
        
    except Exception as e:
        # Non-blocking error - show to user but continue
        print(f"TDD context loader error: {str(e)}", file=sys.stderr)
        sys.exit(1)  # Non-blocking error

if __name__ == "__main__":
    main()
