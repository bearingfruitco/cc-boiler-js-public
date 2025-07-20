#!/usr/bin/env python3
"""
PRP Validator Hook - Ensures PRPs follow the methodology
Validates structure, content quality, and dependencies
NOTE: Only runs when editing PRP files to avoid conflicts with design validator
"""

import json
import sys
import re
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def hook(action):
    """Main hook function - only validate PRP files"""
    
    # Only validate when editing PRP files
    file_path = action.get('path', '')
    if not any(marker in file_path for marker in ['PRPs/', '.prp', 'prp.md', 'prp_']):
        return  # Not a PRP file, skip validation
    
    # Only validate on write operations
    if action.get('tool') not in ['EditTool', 'CreateTool', 'WriteFileTool']:
        return

def get_config():
    """Load hook configuration"""
    config_path = Path(__file__).parent.parent / 'config.json'
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {}

def validate_prp_structure(content):
    """Validate PRP has all required sections"""
    required_sections = [
        (r'##?\s*(?:🎯\s*)?Goal', 'Goal section with clear objectives'),
        (r'##?\s*(?:📚\s*)?Required Context', 'Context section with references'),
        (r'##?\s*(?:🏗️\s*)?Implementation', 'Implementation blueprint'),
        (r'##?\s*(?:🧪\s*)?Validation', 'Validation loops specification')
    ]
    
    missing = []
    for pattern, description in required_sections:
        if not re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
            missing.append(description)
    
    return missing

def validate_prp_content(content, file_path):
    """Validate PRP content quality"""
    issues = []
    
    # Check for vague language
    vague_terms = {
        'should': 'Use "must" or "will" for requirements',
        'might': 'Be specific about behavior',
        'maybe': 'Remove uncertainty - be definitive',
        'possibly': 'Clarify as definite requirement or remove',
        'could': 'Use "will" or "must" instead',
        'probably': 'Remove uncertainty from specifications'
    }
    
    content_lower = content.lower()
    for term, suggestion in vague_terms.items():
        if term in content_lower:
            # Count occurrences
            count = content_lower.count(term)
            if count > 0:
                issues.append(f"Found '{term}' {count}x - {suggestion}")
    
    # Check for design system compliance in examples
    if 'className=' in content or 'class=' in content:
        forbidden_classes = [
            'text-sm', 'text-lg', 'text-xl', 'text-2xl',
            'font-bold', 'font-medium', 'font-light',
            'p-5', 'p-7', 'm-5', 'gap-5'
        ]
        for cls in forbidden_classes:
            if cls in content:
                issues.append(f"Example uses forbidden class '{cls}' - check design system")
    
    # Check for validation loops
    if not re.search(r'##?\s*(?:🧪\s*)?Validation', content, re.IGNORECASE):
        issues.append("Missing validation loops section - all PRPs need validation")
    
    # Check for success criteria
    if not re.search(r'(?:Success Criteria|✅|Acceptance Criteria)', content, re.IGNORECASE):
        issues.append("Missing success criteria - how do we know when it's done?")
    
    # Check for metrics in completed PRPs
    if '/completed/' in str(file_path):
        if 'metrics:' not in content.lower():
            issues.append("Completed PRPs must include success metrics")
    
    # Check for AI docs references
    if 'ai_docs/' not in content and 'Required Context' in content:
        issues.append("Consider referencing AI docs for patterns and gotchas")
    
    return issues

def check_prp_dependencies(content):
    """Check if PRP dependencies are valid"""
    errors = []
    
    # Look for dependency declarations
    dep_patterns = [
        r'(?:Requires|Dependencies|Depends on):\s*([^\n]+)',
        r'depends:\s*\[(.*?)\]',
        r'requires:\s*\[(.*?)\]'
    ]
    
    for pattern in dep_patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE | re.DOTALL)
        for match in matches:
            dep_text = match.group(1)
            # Extract PRP names (ending in .md or -prp)
            prp_names = re.findall(r'([a-zA-Z0-9-_]+(?:-prp|\.md))', dep_text)
            
            for prp_name in prp_names:
                # Normalize name
                if not prp_name.endswith('.md'):
                    prp_name = f"{prp_name}.md"
                
                # Check if dependency exists
                dep_paths = [
                    Path(f"PRPs/active/{prp_name}"),
                    Path(f"PRPs/completed/{prp_name}"),
                    Path(f"PRPs/{prp_name}")
                ]
                
                if not any(p.exists() for p in dep_paths):
                    errors.append(f"Dependency '{prp_name}' not found")
    
    return errors

def extract_prp_info(content):
    """Extract key information from PRP for validation"""
    info = {
        'has_code_examples': bool(re.search(r'```(?:typescript|javascript|tsx|jsx|python)', content)),
        'has_file_paths': bool(re.search(r'(?:path|file):\s*[\'"`]?([/\w.-]+)', content)),
        'has_success_criteria': bool(re.search(r'(?:Success Criteria|✅|Acceptance Criteria)', content, re.IGNORECASE)),
        'has_time_estimate': bool(re.search(r'(?:time|duration|estimate):\s*\d+[hm]', content, re.IGNORECASE)),
        'references_patterns': bool(re.search(r'(?:pattern|example):\s*[/\w.-]+', content, re.IGNORECASE))
    }
    return info

def main():
    try:
        """Main hook logic"""
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
    
        # Only process file write/edit operations

        # Extract tool name - handle multiple formats

        tool_name = input_data.get('tool_name', '')

        if not tool_name and 'tool_use' in input_data:

            tool_name = input_data['tool_use'].get('name', '')

        if not tool_name:

            tool_name = input_data.get('tool', '')

    

        # Extract parameters

        tool_input = input_data.get('tool_input', {})

        if not tool_input and 'tool_use' in input_data:

            tool_input = input_data['tool_use'].get('parameters', {})

    

        if tool_name not in ['Write', 'Edit', 'str_replace']:
                    return
    
        file_path = tool_input.get('file_path', tool_input.get('path', '')
    
        # Only validate PRP files
        if not file_path.endswith('.md') or 'PRPs/' not in file_path:
            # sys.exit(0)
    except Exception as e:
other non-PRP markdown files
    if file_path.endswith('README.md') or '/templates/' in file_path:
        # sys.exit(0)
        return
    
    content = input_dafig()
    
    # Extract PRP info
    prp_info = extract_prp_info(content)
    
    # Validate structure
    missing_sections = validate_prp_structure(content)
    if missing_sections:
        message = "🚨 PRP STRUCTURE INCOMPLETE\n\n"
        message += "Every PRP must have these sections:\n"
        for section in missing_sections:
            message += f"  ❌ {section}\n"
        message += "\n📚 Use PRP templates in PRPs/templates/ as a guide"
        
        # print(message,
            "missing_sections": missing_sections
        , file=sys.stderr)
            sys.exit(2)
        return
    
    # Validate content quality
    issues = validate_prp_content(content, file_path)
    
    # Check dependencies
    dep_errors = check_prp_dependencies(content)
    if dep_errors:
        issues.extend(dep_errors)
    
    # Determine severity
    if issues:
        # Critical issues that should block
        critical_keywords = ['Missing validation', 'Missing success criteria', 'not found']
        has_critical = any(any(keyword in issue for keyword in critical_keywords) for issue in issues)
        
        if has_critical:
            message = "🚨 PRP VALIDATION FAILED\n\n"
            message += "Critical issues found:\n"
            for issue in issues:
                if any(keyword in issue for keyword in critical_keywords):
                    message += f"  ❌ {issue}\n"
            
            message += "\nOther issues:\n"
            for issue in issues:
                if not any(keyword in issue for keyword in critical_keywords):
                    message += f"  ⚠️  {issue}\n"
            
            message += "\n💡 Fix critical issues before proceeding"
            
            # print(message,
                "issues": issues
            , file=sys.stderr)
            sys.exit(2)
            return
        else:
            # Non-critical issues - warn but allow
            message = "⚠️ PRP QUALITY SUGGESTIONS\n\n"
            message += "Consider addressing these points:\n"
            for issue in issues:
                message += f"  • {issue}\n"
            
            # Add helpful suggestions based on what's missing
            if not prp_info['has_code_examples']:
                message += "\n💡 Tip: Include code examples for clarity"
            if not prp_info['has_time_estimate']:
                message += "\n💡 Tip: Add time estimates for planning"
            if not prp_info['references_patterns']:
                message += "\n💡 Tip: Reference existing patterns to follow"
            
            # print(message,
                "issues": issues,
                "prp_info": prp_info
            , file=sys.stderr)
            sys.exit(1)
            return
    
    # All good - provide positive feedback
    strengths = []
    if prp_info['has_code_examples']:
        strengths.append("includes code examples")
    if prp_info['has_success_criteria']:
        strengths.append("has clear success criteria")
    if prp_info['references_patterns']:
        strengths.append("references patterns")
    
    if strengths:
        message = f"✅ PRP looks good! Strengths: {', '.join(strengths)}"
        # print(message,
            "prp_info": prp_info
        )  # Info message
            sys.exit(0)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
