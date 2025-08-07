#!/usr/bin/env python3
"""
Next Command Suggester - Enhanced with full workflow awareness
Suggests next commands based on current context and documentation state
"""

import os
import json
from pathlib import Path
from datetime import datetime

def check_project_state():
    """Determine current state of the project"""
    state = {
        'has_prd': Path('docs/project/PROJECT_PRD.md').exists(),
        'has_agent_os': Path('.agent-os').exists(),
        'has_architecture': Path('docs/architecture').exists(),
        'has_prps': len(list(Path('PRPs/active').glob('*.md'))) if Path('PRPs/active').exists() else 0,
        'has_improvements': any(Path('.').glob('*IMPROVEMENTS.md')),
        'has_roadmap': Path('.agent-os/product/roadmap.md').exists(),
        'has_git_changes': False,
        'last_command': None
    }
    
    # Check for uncommitted changes
    try:
        import subprocess
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        state['has_git_changes'] = bool(result.stdout.strip())
    except:
        pass
    
    return state

def suggest_next_commands(state, last_command=None):
    """Generate intelligent command suggestions based on state"""
    suggestions = []
    
    # Workflow for existing projects with boilerplate
    if not state['has_agent_os']:
        suggestions.append({
            'command': '/analyze-existing full',
            'reason': 'Generate comprehensive analysis in .agent-os/',
            'priority': 'P0',
            'time': '2-3 minutes'
        })
        return suggestions
    
    if not state['has_prd']:
        suggestions.append({
            'command': '/prd-from-existing',
            'reason': 'Document what you\'ve built (uses .agent-os/ analysis)',
            'priority': 'P0',
            'time': '5 minutes'
        })
        return suggestions
    
    if not state['has_architecture']:
        suggestions.append({
            'command': '/architecture',
            'reason': 'Generate architecture documentation',
            'priority': 'P0',
            'time': '5 minutes'
        })
        return suggestions
    
    if state['has_prps'] == 0:
        suggestions.append({
            'command': '/prd-to-prp',
            'reason': 'Convert PRD + Architecture → Implementation PRPs',
            'priority': 'P0',
            'time': '3 minutes',
            'note': 'Will use roadmap phases and architectural debt findings'
        })
        return suggestions
    
    # If we have PRPs, suggest working with them
    if state['has_prps'] > 0:
        suggestions.append({
            'command': '/prp list',
            'reason': f'Review {state["has_prps"]} generated PRPs',
            'priority': 'P1',
            'time': '1 minute'
        })
        
        suggestions.append({
            'command': '/prp-to-issues',
            'reason': 'Create GitHub issues from PRPs',
            'priority': 'P1',
            'time': '5 minutes'
        })
        
        suggestions.append({
            'command': '/fw start [issue-number]',
            'reason': 'Start TDD implementation of an issue',
            'priority': 'P1',
            'time': 'Varies'
        })
    
    # Git-related suggestions
    if state['has_git_changes']:
        suggestions.append({
            'command': '/commit-message',
            'reason': 'Generate commit message for changes',
            'priority': 'P2',
            'time': '30 seconds'
        })
    
    # Testing suggestions
    suggestions.append({
        'command': '/test',
        'reason': 'Run test suite',
        'priority': 'P2',
        'time': '1 minute'
    })
    
    return suggestions

def format_suggestions(suggestions, state):
    """Format suggestions for display"""
    output = []
    
    # Workflow status header
    output.append("\n📊 **Workflow Status**")
    output.append("```")
    output.append(f"✓ Analysis:     {'✅' if state['has_agent_os'] else '❌'} .agent-os/")
    output.append(f"✓ PRD:          {'✅' if state['has_prd'] else '❌'} PROJECT_PRD.md")
    output.append(f"✓ Architecture: {'✅' if state['has_architecture'] else '❌'} docs/architecture/")
    output.append(f"✓ PRPs:         {'✅ ' + str(state['has_prps']) if state['has_prps'] else '❌ None'}")
    output.append(f"✓ Roadmap:      {'✅' if state['has_roadmap'] else '❌'} Phase planning")
    output.append("```")
    
    # Next steps
    output.append("\n🎯 **Suggested Next Commands**")
    
    for i, suggestion in enumerate(suggestions[:3], 1):  # Top 3
        output.append(f"\n**{i}. `{suggestion['command']}`**")
        output.append(f"   {suggestion['reason']}")
        output.append(f"   ⏱️ {suggestion['time']} | Priority: {suggestion['priority']}")
        if 'note' in suggestion:
            output.append(f"   💡 {suggestion['note']}")
    
    # Workflow reminder
    if not state['has_prps']:
        output.append("\n📋 **Complete Workflow**")
        output.append("```mermaid")
        output.append("graph LR")
        output.append("    A[analyze-existing] --> B[prd-from-existing]")
        output.append("    B --> C[architecture]")
        output.append("    C --> D[prd-to-prp]")
        output.append("    D --> E[prp-to-issues]")
        output.append("    E --> F[fw start]")
        output.append("```")
    
    return "\n".join(output)

def main(response=None):
    """Main execution"""
    # Check current state
    state = check_project_state()
    
    # Get last command from response if available
    last_command = None
    if response:
        # Extract command pattern
        import re
        cmd_match = re.search(r'/[\w-]+', response)
        if cmd_match:
            last_command = cmd_match.group()
            state['last_command'] = last_command
    
    # Generate suggestions
    suggestions = suggest_next_commands(state, last_command)
    
    if suggestions:
        output = format_suggestions(suggestions, state)
        print(output)
        
        # Log suggestion event
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'state': state,
            'suggestions': [s['command'] for s in suggestions],
            'last_command': last_command
        }
        
        log_file = Path('.claude/logs/command-suggestions.jsonl')
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

if __name__ == "__main__":
    import sys
    response = sys.stdin.read() if not sys.stdin.isatty() else None
    main(response)
