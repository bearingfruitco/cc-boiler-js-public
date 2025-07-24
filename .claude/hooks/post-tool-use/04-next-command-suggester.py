#!/usr/bin/env python3
"""
Intelligent Next Command Suggestion System
Provides comprehensive workflow guidance based on command-decision-guide.md
Covers ALL scenarios: init, prd, prp, cti, gt, gi, pt, and intelligent decision trees
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
import re
from typing import Dict, List, Optional, Any, Tuple

# Add the utils directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))

class WorkflowDecisionEngine:
    """Intelligent decision engine for command suggestions."""
    
    def __init__(self):
        self.context = self._load_comprehensive_context()
        self.command_executed = None
        self.execution_result = None
        
    def _load_comprehensive_context(self) -> Dict[str, Any]:
        """Load context from all available sources."""
        context = {
            # Project state
            'is_new_project': self._check_new_project(),
            'has_prd': self._check_has_prd(),
            'has_prp': self._check_has_prp(),
            'has_issues': self._check_has_issues(),
            'has_tasks': self._check_has_tasks(),
            
            # Current work
            'current_branch': None,
            'current_issue': None,
            'current_feature': None,
            'current_prp': None,
            'active_prps': [],
            
            # Work state
            'open_bugs': 0,
            'completed_tasks': 0,
            'total_tasks': 0,
            'work_duration': 0,
            'last_command_time': None,
            
            # User state
            'appears_stuck': False,
            'is_morning': datetime.now().hour < 10,
            'is_evening': datetime.now().hour >= 17,
            
            # Feature complexity
            'complexity_level': 'unknown'
        }
        
        # Load from state files
        self._load_state_files(context)
        
        # Load from project structure
        self._load_project_structure(context)
        
        # Analyze user state
        self._analyze_user_state(context)
        
        return context
    
    def _check_new_project(self) -> bool:
        """Check if this is a new project."""
        project_indicators = [
            Path('.') / 'docs' / 'project' / 'PROJECT_PRD.md',
            Path('.') / '.claude' / 'project-config.json'
        ]
        return not any(p.exists() for p in project_indicators)
    
    def _check_has_prd(self) -> bool:
        """Check if PRDs exist."""
        prd_locations = [
            Path('.') / 'docs' / 'prds',
            Path('.') / 'PRDs',
            Path('.') / 'docs' / 'project'
        ]
        return any(p.exists() and list(p.glob('*.md')) for p in prd_locations)
    
    def _check_has_prp(self) -> bool:
        """Check if PRPs exist."""
        prp_dir = Path('.') / 'PRPs' / 'active'
        return prp_dir.exists() and len(list(prp_dir.glob('*.md'))) > 0
    
    def _check_has_issues(self) -> bool:
        """Check if GitHub issues have been created."""
        # Check for issue tracking in state
        state_dir = Path.home() / '.claude-code-state'
        issues_file = state_dir / 'github_issues.json'
        return issues_file.exists()
    
    def _check_has_tasks(self) -> bool:
        """Check if tasks have been generated."""
        state_dir = Path.home() / '.claude-code-state'
        tasks_file = state_dir / 'tasks.json'
        if tasks_file.exists():
            try:
                with open(tasks_file) as f:
                    tasks = json.load(f)
                    return len(tasks.get('tasks', [])) > 0
            except:
                pass
        return False
    
    def _load_state_files(self, context: Dict):
        """Load from Claude Code state files."""
        state_dir = Path.home() / '.claude-code-state'
        
        # Current work state
        work_state_file = state_dir / 'current_work.json'
        if work_state_file.exists():
            try:
                with open(work_state_file) as f:
                    work = json.load(f)
                    context['current_issue'] = work.get('issue_number')
                    context['current_branch'] = work.get('branch_name')
                    context['current_feature'] = work.get('feature_name')
            except:
                pass
        
        # Bug tracking
        bugs_file = Path('.') / '.claude' / 'bugs' / 'bugs.json'
        if bugs_file.exists():
            try:
                with open(bugs_file) as f:
                    bugs = json.load(f)
                    context['open_bugs'] = len([b for b in bugs.get('bugs', []) 
                                               if b.get('status') == 'open'])
            except:
                pass
        
        # Command history for stuck detection
        cmd_log = state_dir / 'command_log.json'
        if cmd_log.exists():
            try:
                with open(cmd_log) as f:
                    log = json.load(f)
                    if log.get('commands'):
                        last_cmd = log['commands'][-1]
                        context['last_command_time'] = last_cmd.get('timestamp')
            except:
                pass
    
    def _load_project_structure(self, context: Dict):
        """Load from project structure."""
        # Active PRPs
        prp_dir = Path('.') / 'PRPs' / 'active'
        if prp_dir.exists():
            context['active_prps'] = [p.stem for p in prp_dir.glob('*.md')]
            if context['active_prps']:
                context['current_prp'] = context['active_prps'][0]
        
        # Task completion status
        state_dir = Path.home() / '.claude-code-state'
        tasks_file = state_dir / 'tasks.json'
        if tasks_file.exists():
            try:
                with open(tasks_file) as f:
                    tasks = json.load(f)
                    all_tasks = tasks.get('tasks', [])
                    context['total_tasks'] = len(all_tasks)
                    context['completed_tasks'] = len([t for t in all_tasks 
                                                    if t.get('status') == 'completed'])
            except:
                pass
    
    def _analyze_user_state(self, context: Dict):
        """Analyze if user appears stuck or needs help."""
        # Check time since last command
        if context['last_command_time']:
            try:
                last_time = datetime.fromisoformat(context['last_command_time'])
                elapsed = (datetime.now() - last_time).seconds
                context['appears_stuck'] = elapsed > 300  # 5 minutes
            except:
                pass
        
        # Check for repeated help commands or confusion indicators
        # This would look at command history patterns
    
    def analyze_complexity(self, text: str) -> str:
        """Analyze feature complexity from description."""
        if not text:
            return 'simple'
        
        text_lower = text.lower()
        
        # High complexity indicators
        high_complexity = [
            'research', 'figure out', 'investigate', 'explore',
            'architecture', 'design', 'integration', 'ml', 'ai',
            'real-time', 'distributed', 'scale', 'optimize',
            'multiple options', 'approaches', 'complex'
        ]
        
        # Medium complexity indicators
        medium_complexity = [
            'implement', 'enhance', 'refactor', 'migrate',
            'api', 'database', 'authentication', 'workflow'
        ]
        
        # Simple indicators
        simple_indicators = [
            'fix', 'typo', 'rename', 'update', 'add button',
            'change color', 'text', 'label', 'minor'
        ]
        
        # Score complexity
        high_score = sum(1 for ind in high_complexity if ind in text_lower)
        medium_score = sum(1 for ind in medium_complexity if ind in text_lower)
        simple_score = sum(1 for ind in simple_indicators if ind in text_lower)
        
        if high_score >= 2 or 'research' in text_lower:
            return 'complex'
        elif medium_score >= 2 or len(text) > 200:
            return 'medium'
        else:
            return 'simple'
    
    def get_decision_tree_suggestions(self) -> List[Dict[str, str]]:
        """Get suggestions based on decision tree logic."""
        suggestions = []
        
        # New project flow
        if self.context['is_new_project']:
            suggestions.extend([
                {'command': '/init-project', 'reason': 'Initialize new project structure'},
                {'command': '/py-prd PROJECT', 'reason': 'Define project requirements'}
            ])
            return suggestions
        
        # Check what stage we're at
        if not self.context['has_prd'] and not self.context['has_issues']:
            # Need to define what to build
            suggestions.append({
                'command': '/py-prd [feature]',
                'reason': 'Create product requirements document'
            })
            suggestions.append({
                'command': '/cti "[clear task]"',
                'reason': 'Capture specific enhancement (if path is clear)'
            })
            
        elif self.context['has_prd'] and not self.context['has_issues']:
            # Have PRD, need issues
            suggestions.append({
                'command': '/gi [feature]',
                'reason': 'Generate GitHub issues from PRD'
            })
            
        elif self.context['has_issues'] and not self.context['has_tasks']:
            # Have issues, need tasks
            if self.context['current_issue']:
                suggestions.append({
                    'command': f'/gt {self.context["current_feature"] or "feature"}',
                    'reason': 'Generate task breakdown'
                })
            else:
                suggestions.append({
                    'command': '/fw start [issue#]',
                    'reason': 'Start working on an issue'
                })
                
        elif self.context['has_tasks']:
            # Ready to work
            if self.context['completed_tasks'] < self.context['total_tasks']:
                suggestions.append({
                    'command': f'/pt {self.context["current_feature"] or "feature"}',
                    'reason': f'Continue processing tasks ({self.context["completed_tasks"]}/{self.context["total_tasks"]} done)'
                })
            else:
                suggestions.append({
                    'command': '/test',
                    'reason': 'All tasks complete - run tests'
                })
                suggestions.append({
                    'command': '/fw complete',
                    'reason': 'Create PR for completed work'
                })
        
        # Always helpful options
        if self.context['appears_stuck']:
            suggestions.extend([
                {'command': '/ws', 'reason': 'Check overall work status'},
                {'command': '/think-through "next steps"', 'reason': 'Get AI guidance'},
                {'command': '/help workflow', 'reason': 'See workflow documentation'}
            ])
        
        return suggestions
    
    def get_command_specific_suggestions(self, command: str, args: Dict, result: Any) -> List[Dict[str, str]]:
        """Get suggestions specific to the command that was just executed."""
        suggestions = []
        
        # Comprehensive command mappings
        if command in ['init-project', 'init']:
            suggestions.extend([
                {'command': '/gi PROJECT', 'reason': 'Create initial GitHub issues'},
                {'command': '/py-prd PROJECT', 'reason': 'Define overall project requirements'}
            ])
            
        elif command in ['py-prd', 'prd', 'create-prd']:
            feature = self._extract_feature_name(args) or 'feature'
            suggestions.extend([
                {'command': f'/gi {feature}', 'reason': 'Generate GitHub issues from PRD'},
                {'command': f'/think-through "{feature} architecture"', 'reason': 'Explore technical approach'},
                {'command': f'/gt {feature}', 'reason': 'Generate task breakdown directly'}
            ])
            
        elif command in ['cti', 'capture-to-issue']:
            issue_num = self._extract_issue_number(result)
            feature = self._extract_feature_name(args)
            complexity = self.analyze_complexity(args.get('body', ''))
            
            if complexity == 'complex':
                suggestions.append({
                    'command': f'/prp {feature}',
                    'reason': 'Complex feature - needs research and exploration'
                })
            
            suggestions.extend([
                {'command': f'/gt {feature}', 'reason': 'Break down into manageable tasks'},
                {'command': f'/fw start {issue_num}' if issue_num else '/fw start [issue]', 
                 'reason': 'Start implementation immediately'}
            ])
            
        elif command in ['prp', 'create-prp']:
            name = args.get('name', 'research')
            suggestions.extend([
                {'command': f'/prp-execute {name}', 'reason': 'Begin research phase'},
                {'command': f'/think-through "{name} approach"', 'reason': 'Brainstorm solutions'},
                {'command': '/prp-status', 'reason': 'Check PRP progress'}
            ])
            
        elif command == 'prp-execute':
            suggestions.extend([
                {'command': '/prp-status', 'reason': 'Monitor research progress'},
                {'command': '/checkpoint "research findings"', 'reason': 'Save important discoveries'}
            ])
            
        elif command == 'prp-complete':
            suggestions.extend([
                {'command': '/cti "Implement [solution from PRP]"', 'reason': 'Capture solution as actionable issue'},
                {'command': '/py-prd [feature]', 'reason': 'Create formal requirements from research'},
                {'command': '/gt [feature]', 'reason': 'Generate implementation tasks'}
            ])
            
        elif command in ['gi', 'generate-issues']:
            suggestions.extend([
                {'command': '/fw start 1', 'reason': 'Start with the first issue'},
                {'command': '/tb', 'reason': 'View task board overview'},
                {'command': '/issue-kanban', 'reason': 'See issues in kanban view'}
            ])
            
        elif command in ['gt', 'generate-tasks']:
            feature = self._extract_feature_name(args)
            
            # Check for orchestration benefit
            if self._should_suggest_orchestration(result):
                agents = self._calculate_optimal_agents(result)
                time_saved = self._calculate_time_saved(result)
                suggestions.append({
                    'command': f'/orch {feature} --agents={agents}',
                    'reason': f'Save ~{time_saved} min with parallel agents'
                })
            
            suggestions.extend([
                {'command': '/tl', 'reason': 'View task ledger for all features'},
                {'command': f'/fw start {self.context["current_issue"] or "[issue]"}', 
                 'reason': 'Begin feature workflow'},
                {'command': f'/pt {feature}', 'reason': 'Process tasks systematically'}
            ])
            
        elif command in ['fw start', 'feature-workflow-start']:
            feature = self._extract_feature_name(args)
            
            if not self.context['has_tasks']:
                suggestions.append({
                    'command': f'/gt {feature}',
                    'reason': 'No tasks found - generate them first'
                })
            
            suggestions.extend([
                {'command': f'/pt {feature}', 'reason': 'Process tasks one by one'},
                {'command': '/generate-tests', 'reason': 'Create test suite (TDD approach)'},
                {'command': f'/create-prp {feature}', 'reason': 'Need implementation blueprint'}
            ])
            
        elif command in ['pt', 'process-tasks']:
            suggestions.extend([
                {'command': '/test', 'reason': 'Verify implementation'},
                {'command': '/checkpoint', 'reason': 'Save progress'},
                {'command': '/vd', 'reason': 'Validate design compliance'}
            ])
            
            if self.context['appears_stuck']:
                suggestions.append({
                    'command': '/mt "[specific blocker]"',
                    'reason': 'Handle specific blocker'
                })
                
        elif command in ['mt', 'micro-task']:
            suggestions.extend([
                {'command': '/test', 'reason': 'Quick test of your fix'},
                {'command': '/commit-review', 'reason': 'Review changes before commit'},
                {'command': f'/pt {self.context["current_feature"]}', 
                 'reason': 'Return to main task flow'}
            ])
            
        elif command in ['test', 'test-runner', 'tr']:
            if self._tests_passed(result):
                suggestions.extend([
                    {'command': '/fw complete', 'reason': '✅ Tests passing - create PR'},
                    {'command': '/grade', 'reason': 'Check implementation quality'},
                    {'command': f'/pt {self.context["current_feature"]}', 
                     'reason': 'Continue with next task'}
                ])
            else:
                suggestions.extend([
                    {'command': '/bt add "[test failure description]"', 
                     'reason': '❌ Track test failure'},
                    {'command': '/think-through "test failure"', 
                     'reason': 'Debug with AI help'},
                    {'command': '/vd', 'reason': 'Check for design violations'}
                ])
                
        elif command in ['bt add', 'bug-track']:
            bug_id = self._extract_bug_id(result)
            suggestions.extend([
                {'command': f'/generate-tests bug-{bug_id}', 
                 'reason': 'Create failing test first (TDD)'},
                {'command': f'/mt "fix bug {bug_id}"', 
                 'reason': 'Quick fix if simple'},
                {'command': '/bt list --open', 'reason': 'See all open bugs'}
            ])
            
        elif command in ['fw complete', 'feature-workflow-complete']:
            next_issue = self._get_next_issue_number()
            suggestions.extend([
                {'command': '/checkpoint "feature complete"', 
                 'reason': 'Save completion state'},
                {'command': f'/fw start {next_issue}' if next_issue else '/ws',
                 'reason': 'Continue with next issue' if next_issue else 'Check for more work'},
                {'command': '/tb', 'reason': 'View overall progress'}
            ])
            
        elif command in ['orch', 'orchestrate']:
            suggestions.extend([
                {'command': '/sas', 'reason': 'Monitor agent status'},
                {'command': '/orchestration-view', 'reason': 'Visualize agent work'},
                {'command': '/checkpoint', 'reason': 'Save orchestration state'}
            ])
            
        elif command in ['think-through', 'ut', 'ultra-think']:
            suggestions.extend([
                {'command': '/cti "[conclusion from analysis]"', 
                 'reason': 'Capture insights as actionable issue'},
                {'command': '/prp [topic]', 'reason': 'Start formal research'},
                {'command': '/research [topic]', 'reason': 'Document findings'}
            ])
        
        return suggestions
    
    def get_situational_suggestions(self) -> List[Dict[str, str]]:
        """Get time and context-based suggestions."""
        suggestions = []
        
        # Morning suggestions
        if self.context['is_morning']:
            suggestions.extend([
                {'command': '/sr', 'reason': '☀️ Start your day with smart resume'},
                {'command': '/bt list --open', 'reason': 'Check overnight bug reports'},
                {'command': '/ws', 'reason': 'Review work status'}
            ])
            
        # Evening suggestions
        elif self.context['is_evening']:
            suggestions.extend([
                {'command': '/checkpoint "EOD"', 'reason': '🌙 Save end-of-day progress'},
                {'command': '/todo add "Continue [task] tomorrow"', 
                 'reason': 'Note for tomorrow'},
                {'command': '/fw complete', 'reason': 'Create WIP PR if applicable'}
            ])
            
        # Bug context
        if self.context['open_bugs'] > 2:
            suggestions.append({
                'command': '/bt list --priority=high',
                'reason': f'🐛 {self.context["open_bugs"]} bugs need attention'
            })
            
        # Stuck context
        if self.context['appears_stuck']:
            suggestions.extend([
                {'command': '/help-decide', 'reason': '🤔 Interactive decision guide'},
                {'command': '/ws', 'reason': 'Review current status'},
                {'command': '/think-through "what should I do next?"', 
                 'reason': 'Get unstuck with AI'}
            ])
        
        return suggestions
    
    def _extract_feature_name(self, args: Dict) -> Optional[str]:
        """Extract feature name from various argument formats."""
        # Try multiple common argument names
        for key in ['name', 'feature', 'title', 'description', 'feature_name']:
            if key in args and args[key]:
                # Convert to slug format
                feature = str(args[key]).lower()
                feature = re.sub(r'[^a-z0-9]+', '-', feature)
                return feature.strip('-')
        return None
    
    def _extract_issue_number(self, result: Any) -> Optional[str]:
        """Extract issue number from result."""
        if isinstance(result, (str, dict)):
            result_str = str(result)
            match = re.search(r'#(\d+)', result_str)
            if match:
                return match.group(1)
        return None
    
    def _extract_bug_id(self, result: Any) -> str:
        """Extract bug ID from result."""
        if isinstance(result, dict) and 'id' in result:
            return str(result['id'])
        return '1'
    
    def _should_suggest_orchestration(self, result: Any) -> bool:
        """Determine if orchestration would be beneficial."""
        if not isinstance(result, dict) or 'tasks' not in result:
            return False
        
        tasks = result.get('tasks', [])
        if len(tasks) < 5:
            return False
        
        # Count domains
        domains = set()
        for task in tasks:
            domain = task.get('domain', 'general')
            domains.add(domain)
        
        # Orchestration beneficial with 2+ domains and 5+ tasks
        return len(domains) >= 2
    
    def _calculate_optimal_agents(self, result: Any) -> int:
        """Calculate optimal number of agents."""
        if not isinstance(result, dict) or 'tasks' not in result:
            return 2
        
        tasks = result.get('tasks', [])
        domains = set(task.get('domain', 'general') for task in tasks)
        
        # 1 agent per domain, max 5
        return min(len(domains), 5)
    
    def _calculate_time_saved(self, result: Any) -> int:
        """Calculate estimated time saved with orchestration."""
        if not isinstance(result, dict) or 'tasks' not in result:
            return 0
        
        tasks = result.get('tasks', [])
        total_time = sum(task.get('estimated_time', 30) for task in tasks)
        
        # Assume 30% time savings with parallel execution
        return int(total_time * 0.3)
    
    def _tests_passed(self, result: Any) -> bool:
        """Check if tests passed from result."""
        if isinstance(result, dict):
            return result.get('all_passed', False) or result.get('success', False)
        elif isinstance(result, str):
            result_lower = result.lower()
            return 'passed' in result_lower and 'failed' not in result_lower
        return False
    
    def _get_next_issue_number(self) -> Optional[str]:
        """Get next issue number if available."""
        if self.context['current_issue']:
            try:
                return str(int(self.context['current_issue']) + 1)
            except:
                pass
        return None
    
    def format_suggestions(self, all_suggestions: List[Dict[str, str]]) -> str:
        """Format suggestions for display."""
        if not all_suggestions:
            return ""
        
        # De-duplicate suggestions
        seen = set()
        unique_suggestions = []
        for s in all_suggestions:
            key = s['command'].split()[0]  # Use base command as key
            if key not in seen:
                seen.add(key)
                unique_suggestions.append(s)
        
        # Limit to top 3 primary suggestions
        primary = unique_suggestions[:3]
        
        output = "\n💡 **Next steps:**\n"
        for i, suggestion in enumerate(primary, 1):
            output += f"  → `{suggestion['command']}` - {suggestion['reason']}\n"
        
        # Add situational help if relevant
        if self.context['appears_stuck']:
            output += "\n🤔 **Feeling stuck?**\n"
            output += "  • `/help-decide` - Interactive workflow guide\n"
            output += "  • `/think-through \"what next?\"` - Get AI assistance\n"
            output += "  • `/ws` - See overall status\n"
        
        # Time-based additions
        if self.context['is_evening']:
            output += "\n⏰ **End of day:**\n"
            output += "  • `/checkpoint` - Save your progress\n"
        elif self.context['is_morning'] and not any('sr' in s['command'] for s in primary):
            output += "\n☀️ **Starting fresh?**\n"
            output += "  • `/sr` - Resume with full context\n"
        
        return output


def extract_command_from_tool(tool_name: str, args: Dict) -> Optional[str]:
    """Extract the command name from tool execution."""
    # Direct command mappings
    tool_to_command = {
        'create_issue': 'cti',
        'capture_to_issue': 'cti',
        'generate_tasks': 'gt',
        'feature_workflow_start': 'fw start',
        'process_tasks': 'pt',
        'bug_track_add': 'bt add',
        'create_prd': 'prd',
        'create_prp': 'prp',
        'test_runner': 'test',
        'generate_issues': 'gi',
        'micro_task': 'mt',
        'init_project': 'init-project',
        'orchestrate_agents': 'orch',
        'think_through': 'think-through',
        'prp_execute': 'prp-execute',
        'prp_complete': 'prp-complete',
        'feature_workflow_complete': 'fw complete'
    }
    
    # Check direct mapping
    if tool_name in tool_to_command:
        return tool_to_command[tool_name]
    
    # Check file creation for commands
    if tool_name == 'create_file' and 'commands/' in str(args.get('path', '')):
        path = Path(args['path'])
        return path.stem
    
    # Check run_command
    if tool_name == 'run_command':
        cmd = args.get('command', '')
        if cmd.startswith('/'):
            return cmd.split()[0][1:]
    
    return None


def check_for_conflicts(tool_name: str, result: Any) -> bool:
    """Check if other hooks have already provided suggestions."""
    # Skip if orchestration suggestion already made
    if 'orchestration_suggestion' in str(result):
        return True
    
    # Skip if persona suggestion already made  
    if 'suggested_persona' in str(result):
        return True
    
    # Skip if next steps already included
    if 'Next steps:' in str(result) or 'next steps:' in str(result):
        return True
    
    return False


def main():
    """Main execution following Anthropic hooks specification."""
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool information
        tool_name = input_data.get('tool_name', '')
        args = input_data.get('arguments', {})
        result = input_data.get('result', {})
        
        # Skip certain tools
        skip_tools = [
            'read_file', 'write_file', 'list_directory',
            'get_file_info', 'search_files', 'str_replace',
            'str_replace_editor', 'view_file'
        ]
        
        if tool_name in skip_tools:
            sys.exit(0)
        
        # Check for conflicts with other hooks
        if check_for_conflicts(tool_name, result):
            sys.exit(0)
        
        # Extract command
        command = extract_command_from_tool(tool_name, args)
        if not command:
            sys.exit(0)
        
        # Initialize decision engine
        engine = WorkflowDecisionEngine()
        engine.command_executed = command
        engine.execution_result = result
        
        # Generate suggestions from multiple sources
        suggestions = []
        
        # 1. Command-specific suggestions
        cmd_suggestions = engine.get_command_specific_suggestions(command, args, result)
        suggestions.extend(cmd_suggestions)
        
        # 2. Decision tree suggestions (if no command-specific)
        if len(suggestions) < 2:
            tree_suggestions = engine.get_decision_tree_suggestions()
            suggestions.extend(tree_suggestions)
        
        # 3. Situational suggestions
        situational = engine.get_situational_suggestions()
        suggestions.extend(situational)
        
        # Format and display
        if suggestions:
            output = engine.format_suggestions(suggestions)
            if output:
                print(output, file=sys.stderr)
        
        # Always exit successfully
        sys.exit(0)
        
    except Exception as e:
        # Log error but don't fail
        print(f"\n⚠️ Next command suggester error: {str(e)}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
