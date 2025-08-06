#!/usr/bin/env python3
"""
Multi-Perspective Review Integration Hook
Suggests multi-perspective reviews at appropriate times
"""

import json
import sys
import os
from pathlib import Path
import re

def should_suggest_multi_review(tool_name: str, args: dict, context: dict) -> bool:
    """Determine if multi-perspective review would be beneficial."""
    
    # Skip if already in a review command
    if 'review' in tool_name.lower():
        return False
        
    # Good times to suggest multi-perspective review:
    
    # 1. After completing a feature
    if tool_name in ['feature_workflow_complete', 'fw_complete']:
        return True
        
    # 2. Before creating a PR (if we detect PR creation intent)
    if tool_name == 'Bash' and args.get('command', '').startswith('gh pr create'):
        return True
        
    # 3. After all tests pass
    if tool_name == 'test_runner':
        result = context.get('result', {})
        if isinstance(result, dict) and result.get('all_passed', False):
            return True
            
    # 4. When explicitly grading or validating
    if tool_name in ['grade', 'stage_validate_grade']:
        return True
        
    # 5. After significant file changes (using official tool names)
    if tool_name in ['Write', 'Edit', 'MultiEdit']:
        # Check if this is a significant component or API change
        path = str(args.get('file_path', args.get('path', '')))
        significant_patterns = [
            r'components/.*\.tsx?$',
            r'app/api/.*\.ts$',
            r'lib/(auth|security|db)/.*\.ts$',
            r'middleware\.ts$'
        ]
        return any(re.match(pattern, path) for pattern in significant_patterns)
        
    return False

def get_review_context(tool_name: str, args: dict) -> dict:
    """Get context for the review suggestion."""
    context = {
        'target': 'current changes',
        'reason': 'comprehensive quality check'
    }
    
    if tool_name in ['feature_workflow_complete', 'fw_complete']:
        context['target'] = 'completed feature'
        context['reason'] = 'before creating PR'
        
    elif tool_name == 'test_runner':
        context['target'] = 'implementation'
        context['reason'] = 'tests are passing'
        
    elif tool_name in ['Write', 'Edit', 'MultiEdit']:
        path = Path(args.get('file_path', args.get('path', '')))
        context['target'] = path.name
        context['reason'] = 'significant changes detected'
        
    return context

def main():
    """Main hook execution."""
    try:
        # Read input from stdin (official format)
        input_data = json.loads(sys.stdin.read())
        
        tool_name = input_data.get('tool_name', '')
        # Use tool_input not arguments (official format)
        tool_input = input_data.get('tool_input', {})
        tool_result = input_data.get('tool_result', {})
        
        # Skip if another review suggestion exists
        if 'review' in str(tool_result).lower() and 'perspective' in str(tool_result).lower():
            sys.exit(0)
            
        # Check if we should suggest multi-perspective review
        if not should_suggest_multi_review(tool_name, tool_input, {'result': tool_result}):
            sys.exit(0)
            
        # Get context
        review_context = get_review_context(tool_name, tool_input)
        
        # Build suggestion
        suggestion = f"\n🔍 **Consider Multi-Perspective Review**\n"
        suggestion += f"Review {review_context['target']} from multiple expert angles "
        suggestion += f"({review_context['reason']}):\n"
        suggestion += f"  → `/mpr` - Security, performance, UX, and architecture review\n"
        suggestion += f"  → `/chain multi-perspective-review` - Run as workflow\n"
        
        # Only suggest if we're at a good stopping point
        if tool_name in ['feature_workflow_complete', 'test_runner', 'grade']:
            suggestion += f"\n✨ This ensures quality before moving forward.\n"
            
            # PostToolUse hooks output to stdout for transcript mode
            print(suggestion)
                
        sys.exit(0)
        
    except Exception as e:
        # Non-blocking error - log to stderr but continue
        print(f"Multi-review suggester error: {str(e)}", file=sys.stderr)
        sys.exit(1)  # Non-blocking error

if __name__ == "__main__":
    main()
