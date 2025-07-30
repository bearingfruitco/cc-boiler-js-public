#!/usr/bin/env python3
"""
Next Command Suggester - Enhanced with Agent OS and Playwright Integration
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
        'has_playwright': Path('playwright.config.ts').exists() or Path('tests/e2e').exists(),
        'recent_command': None,
        'recent_files': [],
        'has_components': False,
        'has_forms': False,
        'has_api_routes': False
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
                # Analyze file types
                for file in context['recent_files']:
                    if 'components/' in file and '.tsx' in file:
                        context['has_components'] = True
                    if 'form' in file.lower() or 'Form' in file:
                        context['has_forms'] = True
                    if 'app/api/' in file or 'pages/api/' in file:
                        context['has_api_routes'] = True
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
    
    # PLAYWRIGHT SUGGESTIONS - NEW!
    # After component modifications
    if tool_name in ['Write', 'Edit', 'MultiEdit'] and context['has_components']:
        suggestions.append({
            'command': 'pw-verify',
            'reason': 'Verify component renders correctly in browser',
            'priority': 'high'
        })
        
        suggestions.append({
            'command': 'pw-console',
            'reason': 'Check for JavaScript console errors',
            'priority': 'medium'
        })
    
    # After form modifications
    if context['has_forms'] and tool_name in ['Write', 'Edit', 'MultiEdit']:
        suggestions.append({
            'command': 'pw-form',
            'reason': 'Test form submission and validation',
            'priority': 'high'
        })
        
        suggestions.append({
            'command': 'pw-a11y',
            'reason': 'Check form accessibility',
            'priority': 'medium'
        })
    
    # After API route changes
    if context['has_api_routes'] and tool_name in ['Write', 'Edit']:
        suggestions.append({
            'command': 'pw-api-test',
            'reason': 'Test API integration in browser',
            'priority': 'high'
        })
    
    # After any UI file modifications
    if tool_name in ['Write', 'Edit', 'MultiEdit']:
        # Check if it's a UI file
        ui_modified = any(
            file.endswith(('.tsx', '.jsx', '.css')) 
            for file in context['recent_files']
        )
        
        if ui_modified:
            suggestions.append({
                'command': 'validate-design',
                'reason': 'Ensure design system compliance',
                'priority': 'medium'
            })
            
            suggestions.append({
                'command': 'pw-screenshot',
                'reason': 'Capture component screenshot for review',
                'priority': 'low'
            })
        
        # Test suggestions
        if any('.test.' in f or '.spec.' in f for f in context['recent_files']):
            suggestions.append({
                'command': 'test',
                'reason': 'Run tests for recent changes',
                'priority': 'high'
            })
            
            suggestions.append({
                'command': 'pw-test',
                'reason': 'Run browser-based tests',
                'priority': 'medium'
            })
    
    # Error recovery suggestions
    if tool_result and 'error' in str(tool_result).lower():
        suggestions.append({
            'command': 'pw-debug',
            'reason': 'Debug error in browser context',
            'priority': 'high'
        })
        
        suggestions.append({
            'command': 'er',
            'reason': 'Run error recovery workflow',
            'priority': 'high'
        })
    
    # Time-based suggestions
    current_hour = datetime.now().hour
    if current_hour >= 17:  # After 5 PM
        suggestions.append({
            'command': 'pw-visual-test',
            'reason': 'Run visual regression tests before EOD',
            'priority': 'medium'
        })
    
    # General suggestions
    suggestions.append({
        'command': 'work-status',
        'reason': 'Get overview of current work',
        'priority': 'low'
    })
    
    # If many UI changes detected, suggest orchestration
    if len([f for f in context['recent_files'] if f.endswith(('.tsx', '.jsx'))]) > 3:
        suggestions.append({
            'command': 'orchestrate browser-test-suite',
            'reason': 'Multiple UI changes - orchestrate comprehensive testing',
            'priority': 'high'
        })
    
    return suggestions

def format_suggestions(suggestions):
    """Format suggestions for output"""
    if not suggestions:
        return None
    
    # Remove duplicates while preserving order
    seen = set()
    unique_suggestions = []
    for sugg in suggestions:
        if sugg['command'] not in seen:
            seen.add(sugg['command'])
            unique_suggestions.append(sugg)
    
    # Sort by priority
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    unique_suggestions.sort(key=lambda x: priority_order.get(x['priority'], 3))
    
    # Format message
    msg = "\n💡 Suggested next commands:\n"
    
    # Show top 4 suggestions (increased from 3 to include Playwright)
    for i, sugg in enumerate(unique_suggestions[:4], 1):
        emoji = "🔴" if sugg['priority'] == 'high' else "🟡" if sugg['priority'] == 'medium' else "⚪"
        msg += f"{emoji} {i}. /{sugg['command']} - {sugg['reason']}\n"
    
    # Add contextual hint
    if any('pw-' in s['command'] for s in unique_suggestions[:4]):
        msg += "\n🔍 Browser testing available - catch issues before users do!"
    
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
