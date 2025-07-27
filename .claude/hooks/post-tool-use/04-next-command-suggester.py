#!/usr/bin/env python3
"""
Next Command Suggester - Enhanced with Agent OS Integration
Provides intelligent workflow guidance based on current context
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def get_project_context():
    """Get current project context"""
    context = {
        'is_new_project': not Path('.git').exists(),
        'has_agent_os': Path('.agent-os').exists(),
        'has_prd': Path('PRD.md').exists() or Path('.claude/PRD.md').exists(),
        'has_tasks': Path('.task-ledger.md').exists(),
        'has_tests': Path('tests').exists() or Path('__tests__').exists(),
        'recent_command': None,
        'recent_files': []
    }
    
    # Check for recent command
    command_log = Path('.claude/state/command.log')
    if command_log.exists():
        try:
            with open(command_log, 'r') as f:
                lines = f.readlines()
                if lines:
                    context['recent_command'] = lines[-1].strip()
        except:
            pass
    
    # Check recent files
    recent_files = Path('.claude/state/recent-files.txt')
    if recent_files.exists():
        try:
            with open(recent_files, 'r') as f:
                context['recent_files'] = [line.strip() for line in f.readlines()[-5:]]
        except:
            pass
    
    return context

def suggest_next_commands(context, tool_name, tool_result):
    """Suggest next commands based on context"""
    suggestions = []
    
    # For new or existing projects without Agent OS
    if context['is_new_project'] or not context['has_agent_os']:
        suggestions.append({
            'command': 'analyze-existing full',
            'reason': 'Set up Agent OS and analyze project structure',
            'priority': 'high'
        })
    
    # If no PRD exists
    if not context['has_prd'] and context['has_agent_os']:
        suggestions.append({
            'command': 'create-prd',
            'reason': 'Create a PRD to define project requirements',
            'priority': 'high'
        })
    
    # If PRD exists but no tasks
    if context['has_prd'] and not context['has_tasks']:
        suggestions.append({
            'command': 'generate-tasks',
            'reason': 'Generate tasks from PRD',
            'priority': 'high'
        })
    
    # If working on tasks
    if context['has_tasks']:
        suggestions.append({
            'command': 'task-status',
            'reason': 'Check current task progress',
            'priority': 'medium'
        })
        
        suggestions.append({
            'command': 'process-tasks',
            'reason': 'Continue working on tasks',
            'priority': 'high'
        })
    
    # After file modifications
    if tool_name in ['Write', 'Edit', 'MultiEdit']:
        suggestions.append({
            'command': 'validate-design',
            'reason': 'Ensure design system compliance',
            'priority': 'medium'
        })
        
        if any('.test.' in f or '.spec.' in f for f in context['recent_files']):
            suggestions.append({
                'command': 'test',
                'reason': 'Run tests for recent changes',
                'priority': 'high'
            })
    
    # General suggestions
    suggestions.append({
        'command': 'work-status',
        'reason': 'Get overview of current work',
        'priority': 'low'
    })
    
    return suggestions

def format_suggestions(suggestions):
    """Format suggestions for output"""
    if not suggestions:
        return None
    
    # Sort by priority
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    suggestions.sort(key=lambda x: priority_order.get(x['priority'], 3))
    
    # Format message
    msg = "\n💡 Suggested next commands:\n"
    
    # Show top 3 suggestions
    for i, sugg in enumerate(suggestions[:3], 1):
        emoji = "🔴" if sugg['priority'] == 'high' else "🟡" if sugg['priority'] == 'medium' else "⚪"
        msg += f"{emoji} {i}. /{sugg['command']} - {sugg['reason']}\n"
    
    msg += "\nUse /help for more commands"
    
    return msg

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract information
        tool_name = input_data.get('tool_name', '')
        tool_result = input_data.get('tool_result', {})
        
        # Get context
        context = get_project_context()
        
        # Generate suggestions
        suggestions = suggest_next_commands(context, tool_name, tool_result)
        
        # Format suggestions
        message = format_suggestions(suggestions)
        
        if message:
            # PostToolUse hooks can output to stdout which is shown in transcript mode
            print(message)
        
        # Exit with code 0 for success
        sys.exit(0)
        
    except Exception as e:
        # On error, output to stderr and exit with non-zero code
        print(f"Command suggester error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
