#!/usr/bin/env python3
"""
PRD Clarity Hook - Ensures PRDs are clear and actionable
Checks for vague language, missing requirements, and unclear specifications
"""

import json
import sys
import re

# Vague terms that should be avoided in PRDs
VAGUE_TERMS = {
    'maybe': 'Be definitive - use "will" or "will not"',
    'possibly': 'Remove uncertainty - state requirements clearly',
    'might': 'Use "must", "should", or "will" instead',
    'could': 'Specify exact behavior - use "will" or "must"',
    'somehow': 'Describe the exact implementation approach',
    'probably': 'Remove speculation - be certain',
    'various': 'List specific items instead of "various"',
    'etc': 'List all items explicitly, avoid "etc"',
    'and so on': 'Be exhaustive in specifications',
    'stuff': 'Use specific technical terms',
    'things': 'Name specific components or features',
    'nice to have': 'Clearly mark as "Required" or "Optional"',
    'if possible': 'Define clear conditions',
    'when needed': 'Specify exact trigger conditions',
    'as appropriate': 'Define what is appropriate',
    'user-friendly': 'Specify exact UX requirements',
    'modern': 'Define specific design standards',
    'fast': 'Specify performance metrics (e.g., <200ms)',
    'efficient': 'Define efficiency metrics',
    'scalable': 'Specify scale requirements (e.g., 10k users)'
}

def check_prd_clarity(content, file_path):
    """Check PRD for clarity issues"""
    issues = []
    
    # Only check PRD files
    if 'PRD' not in file_path and 'prd' not in file_path.lower():
        return issues
    
    lines = content.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        line_lower = line.lower()
        
        # Check for vague terms
        for term, suggestion in VAGUE_TERMS.items():
            if term in line_lower:
                # Skip if it's in a code block
                if line.strip().startswith('```') or line.strip().startswith('`'):
                    continue
                    
                issues.append({
                    'line': line_num,
                    'type': 'vague_language',
                    'term': term,
                    'suggestion': suggestion,
                    'context': line.strip()
                })
    
    # Check for missing sections
    required_sections = [
        ('objectives', 'Clear objectives/goals section'),
        ('requirements', 'Specific requirements section'),
        ('success', 'Success criteria section'),
        ('scope', 'Scope/boundaries section')
    ]
    
    content_lower = content.lower()
    for section, description in required_sections:
        if section not in content_lower:
            issues.append({
                'type': 'missing_section',
                'section': description,
                'suggestion': f'Add a "{description}" to clarify expectations'
            })
    
    # Check for measurable criteria
    if not re.search(r'\d+\s*(ms|seconds?|minutes?|hours?|days?|users?|%|percent)', content, re.IGNORECASE):
        issues.append({
            'type': 'no_metrics',
            'suggestion': 'Add measurable success criteria (response times, user counts, percentages)'
        })
    
    return issues

def format_clarity_message(issues):
    """Format issues into helpful guidance"""
    if not issues:
        return None
    
    message = "📝 PRD CLARITY CHECK\n\n"
    
    # Group by type
    vague_language = [i for i in issues if i.get('type') == 'vague_language']
    missing_sections = [i for i in issues if i.get('type') == 'missing_section']
    other_issues = [i for i in issues if i.get('type') not in ['vague_language', 'missing_section']]
    
    if vague_language:
        message += "🔍 Vague Language Found:\n"
        for issue in vague_language[:5]:  # Show first 5
            message += f"• Line {issue['line']}: '{issue['term']}' → {issue['suggestion']}\n"
            message += f"  Context: \"{issue['context'][:60]}...\"\n"
        
        if len(vague_language) > 5:
            message += f"\n... and {len(vague_language) - 5} more instances\n"
        message += "\n"
    
    if missing_sections:
        message += "📋 Missing Sections:\n"
        for issue in missing_sections:
            message += f"• {issue['section']}\n"
            message += f"  → {issue['suggestion']}\n"
        message += "\n"
    
    if other_issues:
        message += "⚠️ Other Issues:\n"
        for issue in other_issues:
            message += f"• {issue['suggestion']}\n"
        message += "\n"
    
    message += "✅ Good PRD practices:\n"
    message += "• Use specific, measurable requirements\n"
    message += "• Include acceptance criteria for each feature\n"
    message += "• Define exact behavior, not possibilities\n"
    message += "• Specify performance and scale requirements\n"
    
    return message

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool name - handle multiple formats
        tool_name = input_data.get('tool_name', '')
        if not tool_name and 'tool_use' in input_data:
            tool_name = input_data['tool_use'].get('name', '')
        
        # Only check write operations
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            sys.exit(0)
        
        # Extract parameters
        tool_input = input_data.get('tool_input', {})
        if not tool_input and 'tool_use' in input_data:
            tool_input = input_data['tool_use'].get('parameters', {})
        
        file_path = tool_input.get('file_path', tool_input.get('path', ''))
        content = tool_input.get('content', tool_input.get('new_str', ''))
        
        # Check PRD clarity
        issues = check_prd_clarity(content, file_path)
        
        if issues:
            message = format_clarity_message(issues)
            
            # For PRDs with many issues, consider blocking
            if len(issues) > 10:
                error_msg = message + "\n\n💡 Fix these clarity issues before proceeding"
                print(error_msg, file=sys.stderr)
                sys.exit(2)  # Block operation
            else:
                # Just warn for minor issues
                print(message, file=sys.stderr)
                sys.exit(0)
        else:
            sys.exit(0)
        
    except Exception as e:
        # On error, exit with non-zero code and error in stderr
        print(f"PRD clarity hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
