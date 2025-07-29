#!/usr/bin/env python3
"""
Architecture-Aware Next Command Suggester
Enhanced to suggest architecture design after PRD creation
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def check_architecture_exists():
    """Check if architecture documentation exists"""
    arch_dir = Path('docs/architecture')
    if not arch_dir.exists():
        return False
    
    required_files = [
        'SYSTEM_DESIGN.md',
        'DATABASE_SCHEMA.md',
        'API_SPECIFICATION.md',
        'FRONTEND_ARCHITECTURE.md',
        'SECURITY_DESIGN.md',
        'TECHNICAL_ROADMAP.md'
    ]
    
    existing_count = sum(1 for f in required_files if (arch_dir / f).exists())
    return existing_count >= 4  # At least 4 out of 6 files

def get_suggestions_after_command(command, output):
    """Get suggestions based on executed command and output"""
    suggestions = []
    
    # After PRD creation, suggest architecture
    if any(cmd in command for cmd in ['/create-prd', '/prd', 'create-prd']):
        if 'PRD created' in output or 'PROJECT_PRD.md' in output:
            has_arch = check_architecture_exists()
            
            if not has_arch:
                suggestions.append({
                    'command': '/create-architecture',
                    'aliases': ['/arch'],
                    'description': 'Design system architecture from PRD',
                    'reason': 'Essential step before generating issues',
                    'priority': 'high'
                })
                
                suggestions.append({
                    'command': '/chain architecture-design',
                    'aliases': ['/ad'],
                    'description': 'Run complete architecture design chain',
                    'reason': 'Automated architecture process with multiple agents',
                    'priority': 'high'
                })
            else:
                suggestions.append({
                    'command': '/gi PROJECT',
                    'description': 'Generate issues from PRD and architecture',
                    'reason': 'Architecture already exists',
                    'priority': 'high'
                })
    
    # After architecture creation, suggest issue generation
    elif any(cmd in command for cmd in ['/create-architecture', '/arch', 'architecture-design']):
        if 'Architecture' in output and 'Complete' in output:
            suggestions.append({
                'command': '/validate-architecture',
                'aliases': ['/va'],
                'description': 'Validate architecture completeness',
                'reason': 'Ensure all components are properly designed',
                'priority': 'medium'
            })
            
            suggestions.append({
                'command': '/gi PROJECT',
                'description': 'Generate implementation issues',
                'reason': 'Architecture is complete',
                'priority': 'high'
            })
    
    # After init-project
    elif any(cmd in command for cmd in ['/init-project', '/ip', 'init-project']):
        has_arch = check_architecture_exists()
        
        if not has_arch:
            suggestions.append({
                'command': '/create-architecture',
                'aliases': ['/arch'],
                'description': 'Design system architecture',
                'reason': 'Critical step after project initialization',
                'priority': 'high'
            })
        
        suggestions.append({
            'command': '/create-prp',
            'description': 'Create Product Requirement Prompt',
            'reason': 'Define implementation details',
            'priority': 'medium'
        })
    
    # After validate-architecture
    elif 'validate-architecture' in command:
        if 'Score: A' in output or 'Score: B' in output:
            suggestions.append({
                'command': '/gi PROJECT',
                'description': 'Generate implementation issues',
                'reason': 'Architecture validation passed',
                'priority': 'high'
            })
        else:
            suggestions.append({
                'command': '/create-architecture',
                'description': 'Fix architecture issues',
                'reason': 'Architecture needs improvements',
                'priority': 'high'
            })
    
    # General workflow suggestions
    if not suggestions:
        # Check project state
        has_prd = any(Path(p).exists() for p in [
            'docs/project/PROJECT_PRD.md',
            'PROJECT_PRD.md',
            'docs/PROJECT_PRD.md'
        ])
        has_arch = check_architecture_exists()
        has_issues = Path('.github/issues').exists() or Path('docs/issues').exists()
        
        if not has_prd:
            suggestions.append({
                'command': '/prd',
                'description': 'Create project PRD',
                'reason': 'Start with requirements',
                'priority': 'high'
            })
        elif not has_arch:
            suggestions.append({
                'command': '/arch',
                'description': 'Design architecture',
                'reason': 'PRD exists, need technical design',
                'priority': 'high'
            })
        elif not has_issues:
            suggestions.append({
                'command': '/gi PROJECT',
                'description': 'Generate issues',
                'reason': 'Ready for implementation',
                'priority': 'high'
            })
        else:
            suggestions.append({
                'command': '/fw start 1',
                'description': 'Start first feature',
                'reason': 'Everything is set up',
                'priority': 'high'
            })
    
    return suggestions

def format_suggestions(suggestions):
    """Format suggestions for display"""
    if not suggestions:
        return ""
    
    # Sort by priority
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    suggestions.sort(key=lambda x: priority_order.get(x.get('priority', 'low'), 3))
    
    output = "\n🏗️  Architecture-Aware Next Steps:\n\n"
    
    for i, sugg in enumerate(suggestions[:3], 1):
        emoji = "🔴" if sugg.get('priority') == 'high' else "🟡" if sugg.get('priority') == 'medium' else "⚪"
        
        cmd = sugg['command']
        if 'aliases' in sugg:
            cmd += f" ({', '.join(sugg['aliases'])})"
        
        output += f"{emoji} {i}. {cmd}\n"
        output += f"   {sugg['description']}\n"
        if 'reason' in sugg:
            output += f"   → {sugg['reason']}\n"
        output += "\n"
    
    # Add workflow reminder
    output += "📋 Proper workflow: PRD → Architecture → Issues → Implementation\n"
    output += "💡 Use /help for all commands\n"
    
    return output

def main():
    """Main hook logic"""
    try:
        # Read input
        input_data = json.loads(sys.stdin.read())
        
        # Extract command and output
        tool_name = input_data.get('tool_name', '')
        
        # For command execution, get the actual command
        if tool_name == 'execute_command':
            parameters = input_data.get('parameters', {})
            command = parameters.get('command', '')
            result = input_data.get('result', {})
            output = str(result.get('output', ''))
        else:
            # For other tools, use tool name as command
            command = tool_name
            output = str(input_data.get('result', ''))
        
        # Get suggestions
        suggestions = get_suggestions_after_command(command, output)
        
        # Format and output
        if suggestions:
            formatted = format_suggestions(suggestions)
            if formatted:
                print(formatted, file=sys.stderr)
        
    except Exception as e:
        # Log error but don't break
        print(f"Architecture suggester error: {str(e)}", file=sys.stderr)
    
    # Always exit successfully
    sys.exit(0)

if __name__ == "__main__":
    main()
