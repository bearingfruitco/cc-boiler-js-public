#!/usr/bin/env python3
"""
Analyzes task complexity and suggests appropriate agents or workflows.
"""

import os
import sys
import json
import re
from typing import Dict, List, Tuple, Optional

# Add the parent directory to the path so we can import from utils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from utils.command_utils import CommandBase, CommandResult
except ImportError:
    # Fallback implementation
    class CommandBase:
        def __init__(self):
            pass
        
        def success(self, message: str, data: dict = None):
            result = {"status": "success", "message": message}
            if data:
                result["data"] = data
            print(json.dumps(result, indent=2))
            return CommandResult(True, message, data)
        
        def error(self, message: str, data: dict = None):
            result = {"status": "error", "message": message}
            if data:
                result["data"] = data
            print(json.dumps(result, indent=2))
            return CommandResult(False, message, data)
    
    class CommandResult:
        def __init__(self, success: bool, message: str, data: dict = None):
            self.success = success
            self.message = message
            self.data = data


class TaskAnalyzer(CommandBase):
    def __init__(self):
        super().__init__()
        
        # Technology indicators
        self.tech_indicators = {
            'supabase': {
                'keywords': ['supabase', 'rls', 'row level', 'auth', 'realtime', 'edge function'],
                'agent': 'supabase-specialist',
                'description': 'Supabase database, auth, and real-time features'
            },
            'orm': {
                'keywords': ['drizzle', 'prisma', 'schema', 'migration', 'relation', 'database model'],
                'agent': 'orm-specialist',
                'description': 'Database ORM operations with Drizzle or Prisma'
            },
            'analytics': {
                'keywords': ['track', 'event', 'analytics', 'dbt', 'bigquery', 'rudderstack', 'metrics'],
                'agent': 'analytics-engineer',
                'description': 'Analytics tracking and data pipelines'
            },
            'ui': {
                'keywords': ['component', 'ui', 'design', 'animation', 'shadcn', 'tailwind', 'framer'],
                'agent': 'ui-systems',
                'description': 'UI components and design system'
            },
            'privacy': {
                'keywords': ['gdpr', 'ccpa', 'consent', 'cookie', 'tracking', 'pii', 'privacy'],
                'agent': 'privacy-compliance',
                'description': 'Privacy compliance and data protection'
            },
            'deployment': {
                'keywords': ['deploy', 'vercel', 'edge', 'cicd', 'gcp', 'cloud run', 'performance'],
                'agent': 'platform-deployment',
                'description': 'Deployment and infrastructure optimization'
            },
            'event_schema': {
                'keywords': ['event schema', 'event taxonomy', 'event design', 'tracking schema'],
                'agent': 'event-schema',
                'description': 'Event architecture and schema design'
            }
        }
        
        # Complexity indicators
        self.complexity_indicators = {
            'simple': {
                'keywords': ['fix', 'update', 'change', 'modify', 'adjust', 'tweak', 'rename'],
                'max_agents': 1,
                'description': 'Single-agent tasks'
            },
            'medium': {
                'keywords': ['create', 'implement', 'build', 'add', 'setup', 'configure'],
                'max_agents': 3,
                'description': 'Multi-agent coordination'
            },
            'complex': {
                'keywords': ['architect', 'design', 'optimize', 'refactor', 'integrate', 'migrate'],
                'max_agents': 5,
                'description': 'Full orchestration needed'
            }
        }
        
        # Common workflows
        self.workflows = {
            'full_stack_feature': {
                'triggers': ['full stack', 'complete feature', 'end to end', 'entire flow'],
                'agents': ['event-schema', 'orm-specialist', 'supabase-specialist', 'backend-reliability-engineer', 'ui-systems', 'qa-test-engineer'],
                'description': 'Complete feature across all layers'
            },
            'auth_implementation': {
                'triggers': ['authentication', 'login', 'signup', 'auth flow'],
                'agents': ['supabase-specialist', 'privacy-compliance', 'ui-systems', 'qa-test-engineer'],
                'description': 'Authentication system implementation'
            },
            'analytics_setup': {
                'triggers': ['analytics', 'tracking', 'metrics', 'data pipeline'],
                'agents': ['event-schema', 'analytics-engineer', 'privacy-compliance'],
                'description': 'Analytics and tracking implementation'
            },
            'performance_optimization': {
                'triggers': ['performance', 'optimize', 'speed up', 'faster'],
                'agents': ['performance-optimizer', 'platform-deployment', 'ui-systems'],
                'description': 'Performance optimization across stack'
            },
            'database_design': {
                'triggers': ['database schema', 'data model', 'migrations'],
                'agents': ['database-architect', 'orm-specialist', 'supabase-specialist'],
                'description': 'Database design and implementation'
            }
        }
    
    def analyze_task(self, task_description: str) -> Dict:
        """Analyze task and suggest agents/workflows"""
        task_lower = task_description.lower()
        
        # Detect technologies
        detected_techs = []
        for tech, config in self.tech_indicators.items():
            if any(keyword in task_lower for keyword in config['keywords']):
                detected_techs.append({
                    'technology': tech,
                    'agent': config['agent'],
                    'description': config['description']
                })
        
        # Detect complexity
        complexity = self._detect_complexity(task_lower)
        
        # Detect workflows
        suggested_workflow = self._detect_workflow(task_lower)
        
        # Get suggested agents
        suggested_agents = self._get_suggested_agents(detected_techs, complexity, suggested_workflow)
        
        # Build recommendation
        recommendation = self._build_recommendation(
            task_description,
            detected_techs,
            complexity,
            suggested_workflow,
            suggested_agents
        )
        
        return recommendation
    
    def _detect_complexity(self, task_lower: str) -> Dict:
        """Detect task complexity"""
        for level, config in self.complexity_indicators.items():
            if any(keyword in task_lower for keyword in config['keywords']):
                return {
                    'level': level,
                    'max_agents': config['max_agents'],
                    'description': config['description']
                }
        
        # Default to medium complexity
        return {
            'level': 'medium',
            'max_agents': 3,
            'description': 'Multi-agent coordination'
        }
    
    def _detect_workflow(self, task_lower: str) -> Optional[Dict]:
        """Detect if task matches a known workflow"""
        for workflow_name, config in self.workflows.items():
            if any(trigger in task_lower for trigger in config['triggers']):
                return {
                    'name': workflow_name,
                    'agents': config['agents'],
                    'description': config['description']
                }
        return None
    
    def _get_suggested_agents(self, detected_techs: List, complexity: Dict, workflow: Optional[Dict]) -> List[str]:
        """Get list of suggested agents"""
        agents = []
        
        # Add workflow agents if detected
        if workflow:
            agents.extend(workflow['agents'])
        
        # Add technology-specific agents
        for tech in detected_techs:
            if tech['agent'] not in agents:
                agents.append(tech['agent'])
        
        # Add orchestrator for complex tasks
        if complexity['level'] == 'complex' and 'product-manager-orchestrator' not in agents:
            agents.insert(0, 'product-manager-orchestrator')
        
        # Limit based on complexity
        if len(agents) > complexity['max_agents']:
            agents = agents[:complexity['max_agents']]
        
        return agents
    
    def _build_recommendation(self, task: str, techs: List, complexity: Dict, 
                            workflow: Optional[Dict], agents: List[str]) -> Dict:
        """Build final recommendation"""
        recommendation = {
            'task': task,
            'analysis': {
                'technologies': techs,
                'complexity': complexity,
                'workflow': workflow,
                'suggested_agents': agents
            },
            'execution_plan': self._generate_execution_plan(agents, workflow, complexity)
        }
        
        return recommendation
    
    def _generate_execution_plan(self, agents: List[str], workflow: Optional[Dict], 
                                complexity: Dict) -> Dict:
        """Generate execution plan based on analysis"""
        if workflow:
            return {
                'type': 'workflow',
                'name': workflow['name'],
                'description': workflow['description'],
                'steps': [
                    f"Execute workflow: {workflow['name']}",
                    f"Agents involved: {', '.join(agents)}",
                    "Monitor progress and coordinate between agents"
                ]
            }
        elif len(agents) > 1:
            return {
                'type': 'multi-agent',
                'description': f"{complexity['description']} required",
                'steps': [
                    f"Primary agent: {agents[0]}",
                    f"Supporting agents: {', '.join(agents[1:])}",
                    "Coordinate outputs between agents"
                ]
            }
        elif agents:
            return {
                'type': 'single-agent',
                'description': 'Single agent can handle this task',
                'steps': [
                    f"Use {agents[0]} agent",
                    "Execute task directly"
                ]
            }
        else:
            return {
                'type': 'direct',
                'description': 'No specialized agent needed',
                'steps': [
                    "Execute task directly with Claude",
                    "Use standard commands if applicable"
                ]
            }
    
    def run(self, args: List[str]) -> CommandResult:
        """Run the task analyzer"""
        if not args:
            return self.error("Please provide a task description to analyze")
        
        task_description = ' '.join(args)
        
        try:
            analysis = self.analyze_task(task_description)
            
            # Format output
            output = [
                f"\n📋 Task Analysis",
                f"{'=' * 50}",
                f"Task: {analysis['task']}\n",
                f"🔍 Detected Technologies:"
            ]
            
            if analysis['analysis']['technologies']:
                for tech in analysis['analysis']['technologies']:
                    output.append(f"  • {tech['technology']}: {tech['description']}")
            else:
                output.append("  • None specific detected")
            
            output.extend([
                f"\n📊 Complexity: {analysis['analysis']['complexity']['level'].upper()}",
                f"   {analysis['analysis']['complexity']['description']}",
                f"\n🔄 Workflow Match:"
            ])
            
            if analysis['analysis']['workflow']:
                output.append(f"  • {analysis['analysis']['workflow']['name']}: {analysis['analysis']['workflow']['description']}")
            else:
                output.append("  • No specific workflow detected")
            
            output.extend([
                f"\n🤖 Suggested Agents:"
            ])
            
            if analysis['analysis']['suggested_agents']:
                for agent in analysis['analysis']['suggested_agents']:
                    output.append(f"  • {agent}")
            else:
                output.append("  • Claude can handle this directly")
            
            output.extend([
                f"\n📝 Execution Plan:",
                f"Type: {analysis['execution_plan']['type']}",
                f"Description: {analysis['execution_plan']['description']}"
            ])
            
            for i, step in enumerate(analysis['execution_plan']['steps'], 1):
                output.append(f"  {i}. {step}")
            
            output.extend([
                f"\n💡 Quick Commands:"
            ])
            
            # Generate quick commands
            if analysis['analysis']['suggested_agents']:
                primary_agent = analysis['analysis']['suggested_agents'][0]
                # Find alias for agent
                alias = self._get_agent_alias(primary_agent)
                if alias:
                    output.append(f"  • {alias} {task_description}")
                else:
                    output.append(f"  • use {primary_agent} subagent to {task_description}")
                
                if len(analysis['analysis']['suggested_agents']) > 1:
                    output.append(f"  • pm orchestrate {task_description}")
            
            print('\n'.join(output))
            
            return self.success("Task analysis complete", analysis)
            
        except Exception as e:
            return self.error(f"Error analyzing task: {str(e)}")
    
    def _get_agent_alias(self, agent_name: str) -> Optional[str]:
        """Get alias for agent if available"""
        # Map of agent names to common aliases
        alias_map = {
            'supabase-specialist': 'sup',
            'orm-specialist': 'orm',
            'analytics-engineer': 'analytics',
            'ui-systems': 'ui',
            'privacy-compliance': 'privacy',
            'event-schema': 'schema',
            'platform-deployment': 'deploy',
            'product-manager-orchestrator': 'pm',
            'frontend-ux-specialist': 'fe',
            'backend-reliability-engineer': 'be',
            'qa-test-engineer': 'qa',
            'security-threat-analyst': 'sec',
            'database-architect': 'db'
        }
        
        return alias_map.get(agent_name)


if __name__ == "__main__":
    analyzer = TaskAnalyzer()
    analyzer.run(sys.argv[1:])
