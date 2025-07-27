#!/usr/bin/env python3
"""
Auto-Parallel Agent Detection & Think Enhancement Hook

Automatically:
1. Spawns parallel agents for complex tasks
2. Injects "think harder" instructions when needed
3. Adds UltraThink to commands that would benefit
"""

import sys
import json
import os
import re
from pathlib import Path
from datetime import datetime

def get_task_complexity(command_info):
    """Analyze task complexity on a scale of 1-10"""
    command = command_info.get('command', '').lower()
    selected_files = command_info.get('selected_files', [])
    
    complexity = 1
    
    # File count increases complexity
    complexity += min(len(selected_files), 3)
    
    # Keywords that indicate complexity
    complex_keywords = {
        'refactor': 3,
        'architecture': 4,
        'migrate': 3,
        'optimize': 2,
        'performance': 2,
        'security': 3,
        'redesign': 3,
        'implement': 2,
        'analyze': 2,
        'debug': 2,
        'complex': 3,
        'system': 2,
        'integration': 2,
        'async': 2,
        'parallel': 2,
        'distributed': 3
    }
    
    for keyword, weight in complex_keywords.items():
        if keyword in command:
            complexity += weight
    
    # Commands that benefit from deep thinking
    if any(cmd in command for cmd in ['/prd', '/prp', '/generate-tasks', '/analyze']):
        complexity += 2
    
    return min(complexity, 10)

def should_enhance_thinking(command_info, complexity):
    """Determine if we should add thinking instructions"""
    command = command_info.get('command', '').lower()
    
    # Already has thinking instructions
    if any(term in command for term in ['think', 'ultrathink', 'deep', 'careful']):
        return False
    
    # Commands that always benefit from enhanced thinking
    thinking_commands = [
        '/prd',
        '/prp', 
        '/create-prd',
        '/create-prp',
        '/generate-tasks',
        '/gt',
        '/analyze',
        '/architect',
        '/debug',
        '/optimize',
        '/refactor'
    ]
    
    for cmd in thinking_commands:
        if command.startswith(cmd):
            return True
    
    # Complexity threshold
    return complexity >= 5

def should_spawn_parallel_agents(command_info, complexity):
    """Determine if parallel agents should be spawned"""
    
    # Check for explicit triggers
    command = command_info.get('command', '').lower()
    explicit_triggers = [
        'ultrathink',
        'ultra-think',
        '/ut ',
        'parallel agents',
        'sub-agents',
        'multiple agents'
    ]
    
    if any(trigger in command for trigger in explicit_triggers):
        return True
    
    # High complexity tasks
    return complexity >= 7

def get_thinking_instruction(complexity):
    """Get appropriate thinking instruction based on complexity"""
    if complexity >= 8:
        return "UltraThink deeply about this"
    elif complexity >= 6:
        return "Think step by step"
    elif complexity >= 4:
        return "Think carefully"
    else:
        return "Consider"

def determine_agent_types(command_info):
    """Determine which types of agents to spawn based on task"""
    
    command = command_info.get('command', '').lower()
    agents = []
    
    # PRD/PRP related
    if any(word in command for word in ['prd', 'prp', 'requirement', 'specification']):
        agents.extend([
            {
                'type': 'requirements-analyst',
                'focus': 'Analyze requirements completeness and clarity',
                'context': 'PRD templates, acceptance criteria patterns'
            },
            {
                'type': 'technical-feasibility',
                'focus': 'Assess technical implementation challenges',
                'context': 'codebase constraints, technical debt'
            },
            {
                'type': 'task-decomposer',
                'focus': 'Break down into implementable tasks',
                'context': 'task patterns, estimation guidelines'
            }
        ])
    
    # UI/UX related
    elif any(word in command for word in ['ui', 'ux', 'layout', 'design', 'component', 'responsive']):
        agents.extend([
            {
                'type': 'ui-analyst',
                'focus': 'Analyze UI/UX patterns and usability',
                'context': 'design system rules, component library'
            },
            {
                'type': 'pattern-researcher', 
                'focus': 'Research best practices and patterns',
                'context': 'similar implementations, design patterns'
            },
            {
                'type': 'accessibility-reviewer',
                'focus': 'Ensure WCAG compliance and a11y',
                'context': 'accessibility guidelines, aria patterns'
            }
        ])
    
    # Architecture related
    elif any(word in command for word in ['architecture', 'system', 'infrastructure', 'scale']):
        agents.extend([
            {
                'type': 'system-analyst',
                'focus': 'Analyze system architecture and dependencies',
                'context': 'current architecture, dependency graph'
            },
            {
                'type': 'performance-optimizer',
                'focus': 'Identify performance bottlenecks and optimizations',
                'context': 'performance metrics, benchmarks'
            },
            {
                'type': 'security-reviewer',
                'focus': 'Review security implications',
                'context': 'security rules, OWASP guidelines'
            }
        ])
    
    # Bug fixing related  
    elif any(word in command for word in ['bug', 'fix', 'issue', 'error', 'problem']):
        agents.extend([
            {
                'type': 'root-cause-analyst',
                'focus': 'Identify root cause of the issue',
                'context': 'error logs, stack traces, related code'
            },
            {
                'type': 'pattern-reviewer',
                'focus': 'Review code patterns and anti-patterns',
                'context': 'similar fixes, known issues'
            },
            {
                'type': 'solution-researcher',
                'focus': 'Research and propose solutions',
                'context': 'documentation, similar problems'
            }
        ])
    
    # Refactoring related
    elif any(word in command for word in ['refactor', 'restructure', 'reorganize', 'optimize']):
        agents.extend([
            {
                'type': 'dependency-mapper',
                'focus': 'Map dependencies and impact',
                'context': 'import graph, component usage'
            },
            {
                'type': 'impact-analyzer',
                'focus': 'Analyze change impact and risks',
                'context': 'test coverage, critical paths'
            },
            {
                'type': 'migration-planner',
                'focus': 'Plan safe migration strategy',
                'context': 'rollback plans, feature flags'
            }
        ])
    
    # Default agents if none matched
    if not agents:
        agents = [
            {
                'type': 'technical-analyst',
                'focus': 'Analyze technical requirements',
                'context': 'codebase patterns, constraints'
            },
            {
                'type': 'solution-designer',
                'focus': 'Design optimal solution',
                'context': 'best practices, patterns'
            },
            {
                'type': 'implementation-planner',
                'focus': 'Plan implementation approach',
                'context': 'tasks, dependencies, risks'
            }
        ]
    
    return agents

def create_agent_prompt(agent, original_command, command_info):
    """Create specialized prompt for each agent"""
    
    return f"""
You are a specialized {agent['type']} agent working as part of a parallel analysis team.

Your focus: {agent['focus']}
Context to consider: {agent['context']}

Original task: {original_command}

Please analyze this task from your specialized perspective and provide:
1. Key findings and insights
2. Specific recommendations
3. Potential concerns or risks
4. Required resources or dependencies

Work independently but consider how your analysis will integrate with other agents' findings.
"""

def enhance_command_with_thinking(command, complexity):
    """Add thinking instructions to command"""
    thinking = get_thinking_instruction(complexity)
    
    # For specific commands, inject thinking differently
    if command.startswith('/prd'):
        return command.replace('/prd', f'/prd [{thinking}]')
    elif command.startswith('/generate-tasks') or command.startswith('/gt'):
        return f"{thinking} about task decomposition. {command}"
    elif command.startswith('/create-prp') or command.startswith('/prp'):
        return command.replace('create', f'create [{thinking}]')
    else:
        # Generic enhancement
        return f"{thinking}: {command}"

def main():
    """Main hook logic"""
    try:
        # Read hook input
        hook_input = json.loads(sys.stdin.read())
        
        # Extract tool name - handle multiple formats
        tool_name = hook_input.get('tool_name', '')
        if not tool_name and 'tool_use' in hook_input:
            tool_name = hook_input['tool_use'].get('name', '')
        
        # This hook only processes custom commands or complex file operations
        command = hook_input.get('command', '')
        if tool_name not in ['Bash', 'Write', 'Edit'] or not command:
            sys.exit(0)
        
        # Extract tool input
        tool_input = hook_input.get('tool_input', {})
        if not tool_input and 'tool_use' in hook_input:
            tool_input = hook_input['tool_use'].get('parameters', {})
        
        # Build command info
        command_info = {
            'command': command,
            'selected_files': tool_input.get('selected_files', [])
        }
        
        # Analyze complexity
        complexity = get_task_complexity(command_info)
        
        # Original command
        original_command = command
        enhanced_command = original_command
        
        # Should we enhance thinking?
        if should_enhance_thinking(command_info, complexity):
            enhanced_command = enhance_command_with_thinking(original_command, complexity)
        
        # Should we spawn parallel agents?
        spawn_agents = should_spawn_parallel_agents(command_info, complexity)
        
        if spawn_agents:
            # Determine agent types
            agents = determine_agent_types(command_info)
            
            # Add parallel agent instructions
            enhanced_command = f"""[ULTRATHINK MODE AUTO-ACTIVATED - Complexity: {complexity}/10]

Enhanced request: {enhanced_command}

Spawning {len(agents)} specialized agents:
{chr(10).join(f"- {agent['type']}: {agent['focus']}" for agent in agents)}

Each agent will analyze independently with extended thinking.
Results will be synthesized into a comprehensive solution.
"""
            
            # Create agent prompts
            prompts_file = Path('.claude/context/agent-prompts.json')
            prompts_file.parent.mkdir(parents=True, exist_ok=True)
            
            agent_prompts = {
                f"agent_{i}": create_agent_prompt(agent, original_command, command_info)
                for i, agent in enumerate(agents)
            }
            
            with open(prompts_file, 'w') as f:
                json.dump(agent_prompts, f, indent=2)
        
        # Log thinking enhancement
        log_file = Path('.claude/logs/thinking-enhancement.log')
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_file, 'a') as f:
            f.write(f"\n--- Thinking Enhancement ---\n")
            f.write(f"Time: {datetime.now().isoformat()}\n")
            f.write(f"Original: {original_command}\n")
            f.write(f"Complexity: {complexity}/10\n")
            f.write(f"Enhanced: {enhanced_command != original_command}\n")
            f.write(f"Parallel Agents: {spawn_agents}\n")
        
        # Return result
        if enhanced_command != original_command or spawn_agents:
            # Show enhancement info
            message = f"🤖 AUTO-ENHANCEMENT APPLIED\n"
            message += f"Complexity: {complexity}/10\n"
            if spawn_agents:
                message += f"Parallel agents: {len(agents)}\n"
            
            print(message, file=sys.stderr)
            sys.exit(0)
        else:
            # No enhancement needed
            sys.exit(0)
            
    except Exception as e:
        # On error, exit with non-zero code and error in stderr
        print(f"Auto parallel agents hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
