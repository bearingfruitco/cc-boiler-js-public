#!/usr/bin/env python3
"""
Suggestion System Utilities
Shared utilities for command suggestion and decision logic
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

class ContextLoader:
    """Centralized context loading for all suggestion systems."""
    
    @staticmethod
    def load_full_context() -> Dict[str, Any]:
        """Load comprehensive context from all sources."""
        context = {
            # Project state
            'is_new_project': False,
            'has_prd': False,
            'has_prp': False,
            'has_issues': False,
            'has_tasks': False,
            
            # Current work
            'current_branch': None,
            'current_issue': None,
            'current_feature': None,
            'current_prp': None,
            'active_prps': [],
            
            # Work metrics
            'open_bugs': 0,
            'completed_tasks': 0,
            'total_tasks': 0,
            'tasks_by_domain': {},
            
            # User state
            'work_duration': 0,
            'last_command_time': None,
            'appears_stuck': False,
            'command_history': [],
            
            # Time context
            'is_morning': datetime.now().hour < 10,
            'is_evening': datetime.now().hour >= 17,
            'is_weekend': datetime.now().weekday() >= 5
        }
        
        # Load from various sources
        ContextLoader._load_project_state(context)
        ContextLoader._load_work_state(context)
        ContextLoader._load_task_state(context)
        ContextLoader._load_bug_state(context)
        ContextLoader._load_user_state(context)
        
        print(json.dumps({"action": "continue"}))
        
        return context
    
    @staticmethod
    def _load_project_state(context: Dict):
        """Check project initialization state."""
        # Check for project markers
        project_markers = [
            Path('.') / 'docs' / 'project' / 'PROJECT_PRD.md',
            Path('.') / '.claude' / 'project-config.json',
            Path('.') / 'package.json'
        ]
        
        context['is_new_project'] = not any(p.exists() for p in project_markers)
        
        # Check for PRDs
        prd_dirs = [
            Path('.') / 'docs' / 'prds',
            Path('.') / 'PRDs',
            Path('.') / 'docs' / 'project'
        ]
        for prd_dir in prd_dirs:
            if prd_dir.exists() and list(prd_dir.glob('*.md')):
                context['has_prd'] = True
                break
        
        # Check for PRPs
        prp_active = Path('.') / 'PRPs' / 'active'
        if prp_active.exists():
            prps = list(prp_active.glob('*.md'))
            context['has_prp'] = len(prps) > 0
            context['active_prps'] = [p.stem for p in prps]
            if prps:
                context['current_prp'] = prps[0].stem
    
    @staticmethod
    def _load_work_state(context: Dict):
        """Load current work state."""
        state_dir = Path.home() / '.claude-code-state'
        
        # Current work
        work_file = state_dir / 'current_work.json'
        if work_file.exists():
            try:
                with open(work_file) as f:
                    work = json.load(f)
                    context['current_issue'] = work.get('issue_number')
                    context['current_branch'] = work.get('branch_name')
                    context['current_feature'] = work.get('feature_name')
            except:
                pass
        
        # GitHub issues
        issues_file = state_dir / 'github_issues.json'
        context['has_issues'] = issues_file.exists()
    
    @staticmethod
    def _load_task_state(context: Dict):
        """Load task information."""
        state_dir = Path.home() / '.claude-code-state'
        tasks_file = state_dir / 'tasks.json'
        
        if tasks_file.exists():
            try:
                with open(tasks_file) as f:
                    data = json.load(f)
                    tasks = data.get('tasks', [])
                    
                    context['has_tasks'] = len(tasks) > 0
                    context['total_tasks'] = len(tasks)
                    context['completed_tasks'] = len([t for t in tasks 
                                                    if t.get('status') == 'completed'])
                    
                    # Group by domain
                    domains = {}
                    for task in tasks:
                        domain = task.get('domain', 'general')
                        domains[domain] = domains.get(domain, 0) + 1
                    context['tasks_by_domain'] = domains
            except:
                pass
    
    @staticmethod
    def _load_bug_state(context: Dict):
        """Load bug tracking state."""
        bugs_file = Path('.') / '.claude' / 'bugs' / 'bugs.json'
        if bugs_file.exists():
            try:
                with open(bugs_file) as f:
                    data = json.load(f)
                    bugs = data.get('bugs', [])
                    context['open_bugs'] = len([b for b in bugs 
                                              if b.get('status') == 'open'])
            except:
                pass
    
    @staticmethod
    def _load_user_state(context: Dict):
        """Analyze user state and patterns."""
        state_dir = Path.home() / '.claude-code-state'
        
        # Command history
        cmd_log = state_dir / 'command_log.json'
        if cmd_log.exists():
            try:
                with open(cmd_log) as f:
                    log = json.load(f)
                    commands = log.get('commands', [])
                    
                    if commands:
                        # Last command time
                        last_cmd = commands[-1]
                        context['last_command_time'] = last_cmd.get('timestamp')
                        
                        # Check if stuck
                        if context['last_command_time']:
                            last_time = datetime.fromisoformat(context['last_command_time'])
                            elapsed = (datetime.now() - last_time).seconds
                            context['appears_stuck'] = elapsed > 300  # 5 minutes
                        
                        # Recent command history
                        context['command_history'] = [c['command'] for c in commands[-10:]]
            except:
                pass


class ComplexityAnalyzer:
    """Analyze task/feature complexity."""
    
    @staticmethod
    def analyze(text: str) -> str:
        """Return complexity level: simple, medium, complex."""
        if not text:
            print(json.dumps({"action": "continue"}))
            return 'simple'
        
        text_lower = text.lower()
        
        # Complexity indicators
        indicators = {
            'complex': [
                'research', 'figure out', 'investigate', 'explore',
                'architecture', 'design', 'integration', 'ml', 'ai',
                'real-time', 'distributed', 'scale', 'optimize',
                'multiple options', 'approaches', 'complex', 'unclear'
            ],
            'medium': [
                'implement', 'enhance', 'refactor', 'migrate',
                'api', 'database', 'authentication', 'workflow',
                'form', 'ui component', 'validation', 'testing'
            ],
            'simple': [
                'fix', 'typo', 'rename', 'update', 'add button',
                'change color', 'text', 'label', 'minor', 'quick'
            ]
        }
        
        # Score each level
        scores = {}
        for level, keywords in indicators.items():
            scores[level] = sum(1 for kw in keywords if kw in text_lower)
        
        # Length factor
        if len(text) > 300:
            scores['complex'] += 1
        elif len(text) < 50:
            scores['simple'] += 1
        
        # Return highest scoring level
        print(json.dumps({"action": "continue"}))
        return max(scores.keys(), key=lambda k: scores[k])


class OrchestrationCalculator:
    """Calculate orchestration benefits."""
    
    @staticmethod
    def should_suggest_orchestration(tasks: List[Dict]) -> bool:
        """Determine if orchestration would help."""
        if len(tasks) < 5:
            print(json.dumps({"action": "continue"}))
            return False
        
        domains = set(task.get('domain', 'general') for task in tasks)
        print(json.dumps({"action": "continue"}))
        return len(domains) >= 2
    
    @staticmethod
    def calculate_optimal_agents(tasks: List[Dict]) -> int:
        """Calculate optimal number of agents."""
        domains = set(task.get('domain', 'general') for task in tasks)
        print(json.dumps({"action": "continue"}))
        return min(len(domains), 5)
    
    @staticmethod
    def calculate_time_saved(tasks: List[Dict]) -> int:
        """Estimate time saved in minutes."""
        total_time = sum(task.get('estimated_time', 30) for task in tasks)
        # Assume 30% savings with parallel execution
        print(json.dumps({"action": "continue"}))
        return int(total_time * 0.3)


class SuggestionConflictChecker:
    """Check for conflicts with other hooks."""
    
    @staticmethod
    def has_existing_suggestions(result: Any) -> bool:
        """Check if suggestions already provided."""
        if not result:
            print(json.dumps({"action": "continue"}))
            return False
        
        result_str = str(result)
        
        # Check for existing suggestions
        suggestion_indicators = [
            'orchestration_suggestion',
            'suggested_persona',
            'Next steps:',
            'next steps:',
            'Recommended:',
            'Suggestion:'
        ]
        
        print(json.dumps({"action": "continue"}))
        
        return any(indicator in result_str for indicator in suggestion_indicators)


class CommandMappings:
    """Centralized command mappings."""
    
    # Tool name to command mapping
    TOOL_TO_COMMAND = {
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
        'feature_workflow_complete': 'fw complete',
        'checkpoint': 'checkpoint',
        'smart_resume': 'sr',
        'work_status': 'ws',
        'validate_design': 'vd',
        'help_decide': 'help-decide'
    }
    
    # Command workflow chains
    WORKFLOW_CHAINS = {
        'init-project': ['gi PROJECT', 'fw start 1'],
        'py-prd': ['gi', 'gt', 'fw start'],
        'cti': ['gt', 'fw start', 'prp'],
        'prp': ['prp-execute', 'prp-status', 'prp-complete'],
        'prp-complete': ['cti', 'py-prd', 'gt'],
        'gi': ['fw start', 'tb', 'issue-kanban'],
        'gt': ['orch', 'fw start', 'pt'],
        'fw start': ['gt', 'pt', 'generate-tests'],
        'pt': ['test', 'checkpoint', 'vd'],
        'test': ['fw complete', 'bt add', 'grade'],
        'mt': ['test', 'commit-review', 'pt'],
        'bt add': ['generate-tests', 'mt', 'fw start'],
        'fw complete': ['checkpoint', 'fw start', 'ws']
    }
    
    # Situational suggestions
    SITUATIONAL = {
        'morning': [
            {'command': '/sr', 'reason': 'Resume with full context'},
            {'command': '/bt list --open', 'reason': 'Check overnight issues'},
            {'command': '/ws', 'reason': 'Review work status'}
        ],
        'evening': [
            {'command': '/checkpoint "EOD"', 'reason': 'Save progress'},
            {'command': '/todo add "Continue tomorrow"', 'reason': 'Note for tomorrow'},
            {'command': '/fw complete', 'reason': 'Create WIP PR if needed'}
        ],
        'stuck': [
            {'command': '/help-decide', 'reason': 'Interactive decision guide'},
            {'command': '/think-through "next steps"', 'reason': 'Get AI analysis'},
            {'command': '/ws', 'reason': 'Review overall status'}
        ],
        'many_bugs': [
            {'command': '/bt list --priority=high', 'reason': 'Focus on critical bugs'},
            {'command': '/bt assign --auto', 'reason': 'Distribute bug work'}
        ]
    }
