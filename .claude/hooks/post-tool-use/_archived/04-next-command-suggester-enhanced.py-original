#!/usr/bin/env python3
"""
Enhanced Next Command Suggestion System with Agent OS Integration
Provides comprehensive workflow guidance including new analyze-existing and migrate commands
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
    """Intelligent decision engine for command suggestions with Agent OS integration."""
    
    def __init__(self):
        self.context = self._load_comprehensive_context()
        self.command_executed = None
        self.execution_result = None
        
    def _load_comprehensive_context(self) -> Dict[str, Any]:
        """Load context from all available sources."""
        context = {
            # Project state
            'is_new_project': self._check_new_project(),
            'is_existing_project': self._check_existing_project(),
            'has_agent_os': self._check_has_agent_os(),
            'has_prd': self._check_has_prd(),
            'has_prp': self._check_has_prp(),
            'has_issues': self._check_has_issues(),
            'has_tasks': self._check_has_tasks(),
            'needs_design_migration': self._check_needs_design_migration(),
            
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
            Path('.') / '.claude' / 'project-config.json',
            Path('.') / '.agent-os' / 'product' / 'mission.md'
        ]
        return not any(p.exists() for p in project_indicators)
    
    def _check_existing_project(self) -> bool:
        """Check if this is an existing project without boilerplate setup."""
        has_code = any(Path('.').glob('**/*.tsx')) or any(Path('.').glob('**/*.jsx'))
        has_package = Path('package.json').exists()
        has_boilerplate = Path('.claude').exists()
        
        return (has_code or has_package) and not has_boilerplate
    
    def _check_has_agent_os(self) -> bool:
        """Check if Agent OS is set up."""
        return Path('.agent-os').exists() and Path('.agent-os/standards').exists()
    
    def _check_needs_design_migration(self) -> bool:
        """Check if project needs design system migration."""
        # Simple heuristic: if using Tailwind but not our strict system
        if Path('tailwind.config.js').exists():
            # Check a few component files for old patterns
            for comp in Path('.').glob('**/*.tsx'):
                try:
                    content = comp.read_text()
                    if 'text-sm' in content or 'font-bold' in content:
                        return True
                except:
                    pass
        return False
    
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
        """Check for tasks in various locations."""
        task_indicators = [
            Path('.') / '.task-ledger.md',
            Path('.') / 'docs' / 'tasks',
            Path('.') / '.claude' / 'state' / 'current-task.json'
        ]
        return any(p.exists() for p in task_indicators)
    
    def _load_state_files(self, context: Dict[str, Any]) -> None:
        """Load state from various state files."""
        # Implementation details omitted for brevity
        pass
    
    def _load_project_structure(self, context: Dict[str, Any]) -> None:
        """Analyze project structure."""
        # Implementation details omitted for brevity
        pass
    
    def _analyze_user_state(self, context: Dict[str, Any]) -> None:
        """Analyze user behavior patterns."""
        # Implementation details omitted for brevity
        pass
    
    def get_suggestions(self, command: str, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get intelligent suggestions based on command and context."""
        self.command_executed = command
        self.execution_result = result
        
        # Special handling for existing project scenarios
        if self.context['is_existing_project'] and not self.context['has_agent_os']:
            return self._suggest_existing_project_setup()
        
        # Check for design migration needs
        if self.context['has_agent_os'] and self.context['needs_design_migration']:
            return self._suggest_design_migration()
        
        # Route to specific suggestion handlers
        suggestion_handlers = {
            'init-project': self._suggest_after_init,
            'analyze-existing': self._suggest_after_analyze,
            'migrate-to-strict-design': self._suggest_after_migrate,
            'create-prd': self._suggest_after_prd,
            'create-prp': self._suggest_after_prp,
            'capture-to-issue': self._suggest_after_cti,
            'generate-tasks': self._suggest_after_gt,
            'generate-issues': self._suggest_after_gi,
            'process-tasks': self._suggest_after_pt,
            'smart-resume': self._suggest_after_resume,
            'feature-workflow': self._suggest_after_fw,
            'validate-design': self._suggest_after_vd,
            'test-runner': self._suggest_after_test,
            'branch-status': self._suggest_after_branch_status
        }
        
        # Find handler for command (handles aliases)
        handler = None
        for cmd_pattern, suggest_func in suggestion_handlers.items():
            if cmd_pattern in command or command.startswith(cmd_pattern):
                handler = suggest_func
                break
        
        if handler:
            return handler()
        else:
            return self._suggest_general()
    
    def _suggest_existing_project_setup(self) -> List[Dict[str, Any]]:
        """Suggest setup for existing projects."""
        return [
            {
                'command': '/analyze-existing',
                'aliases': ['/ae', '/drop-in'],
                'description': 'Analyze your existing codebase and set up full system',
                'reason': 'Detected existing project without boilerplate setup'
            },
            {
                'command': '/help existing',
                'description': 'Learn about integrating with existing projects',
                'reason': 'Get guidance on the integration process'
            }
        ]
    
    def _suggest_design_migration(self) -> List[Dict[str, Any]]:
        """Suggest design system migration."""
        return [
            {
                'command': '/migrate-to-strict-design analyze',
                'aliases': ['/mds analyze'],
                'description': 'Analyze design system violations',
                'reason': 'Detected non-compliant design patterns'
            },
            {
                'command': '/vd',
                'description': 'Quick design validation check',
                'reason': 'See current violations'
            }
        ]
    
    def _suggest_after_analyze(self) -> List[Dict[str, Any]]:
        """Suggestions after analyzing existing project."""
        suggestions = [
            {
                'command': '/migrate-to-strict-design analyze',
                'aliases': ['/mds analyze'],
                'description': 'Check for design system violations',
                'reason': 'Ensure code follows strict design standards'
            },
            {
                'command': '/sr',
                'description': 'Load full context with new documentation',
                'reason': 'Start working with complete project understanding'
            }
        ]
        
        if self.context['has_prd']:
            suggestions.append({
                'command': '/create-prp main-feature',
                'description': 'Create PRP for main feature',
                'reason': 'Enhance PRD with implementation details'
            })
        
        return suggestions
    
    def _suggest_after_migrate(self) -> List[Dict[str, Any]]:
        """Suggestions after design migration."""
        return [
            {
                'command': '/vd',
                'description': 'Validate design compliance',
                'reason': 'Ensure migration was successful'
            },
            {
                'command': '/tr changed',
                'description': 'Run tests on changed files',
                'reason': 'Ensure nothing broke during migration'
            },
            {
                'command': '/checkpoint post-migration',
                'description': 'Save state after migration',
                'reason': 'Create restore point'
            }
        ]
    
    def _suggest_after_init(self) -> List[Dict[str, Any]]:
        """Suggestions after project initialization."""
        suggestions = []
        
        if not self.context['has_issues']:
            suggestions.append({
                'command': '/gi PROJECT',
                'aliases': ['/gen-issues PROJECT'],
                'description': 'Generate GitHub issues from PRD',
                'reason': 'Create trackable work items'
            })
        
        if not self.context['has_prp']:
            suggestions.append({
                'command': '/create-prp core-feature',
                'description': 'Create PRP for first feature',
                'reason': 'Add implementation details to PRD'
            })
        
        suggestions.append({
            'command': '/fw start',
            'description': 'Start working on first feature',
            'reason': 'Begin implementation'
        })
        
        return suggestions
    
    def _suggest_after_prd(self) -> List[Dict[str, Any]]:
        """Suggestions after creating PRD."""
        # Original implementation
        pass
    
    def _suggest_after_prp(self) -> List[Dict[str, Any]]:
        """Suggestions after creating PRP."""
        # Original implementation
        pass
    
    def _suggest_after_cti(self) -> List[Dict[str, Any]]:
        """Suggestions after capturing to issue."""
        # Original implementation
        pass
    
    def _suggest_after_gt(self) -> List[Dict[str, Any]]:
        """Suggestions after generating tasks."""
        # Original implementation
        pass
    
    def _suggest_after_gi(self) -> List[Dict[str, Any]]:
        """Suggestions after generating issues."""
        # Original implementation
        pass
    
    def _suggest_after_pt(self) -> List[Dict[str, Any]]:
        """Suggestions after processing tasks."""
        # Original implementation
        pass
    
    def _suggest_after_resume(self) -> List[Dict[str, Any]]:
        """Suggestions after smart resume."""
        suggestions = []
        
        # Check if this is first time setup
        if self.context['is_existing_project'] and not self.context['has_agent_os']:
            suggestions.append({
                'command': '/analyze-existing',
                'aliases': ['/ae'],
                'description': 'Set up boilerplate for existing project',
                'reason': 'Complete system integration'
            })
        
        # Original resume suggestions
        if self.context['has_tasks'] and self.context['total_tasks'] > self.context['completed_tasks']:
            suggestions.append({
                'command': '/pt',
                'description': 'Continue processing tasks',
                'reason': f"{self.context['total_tasks'] - self.context['completed_tasks']} tasks remaining"
            })
        
        return suggestions
    
    def _suggest_after_fw(self) -> List[Dict[str, Any]]:
        """Suggestions after feature workflow."""
        # Original implementation
        pass
    
    def _suggest_after_vd(self) -> List[Dict[str, Any]]:
        """Suggestions after design validation."""
        # Original implementation
        pass
    
    def _suggest_after_test(self) -> List[Dict[str, Any]]:
        """Suggestions after running tests."""
        # Original implementation
        pass
    
    def _suggest_after_branch_status(self) -> List[Dict[str, Any]]:
        """Suggestions after checking branch status."""
        # Original implementation
        pass
    
    def _suggest_general(self) -> List[Dict[str, Any]]:
        """General suggestions when no specific handler matches."""
        suggestions = []
        
        # Always useful commands
        suggestions.extend([
            {
                'command': '/help',
                'description': 'See all available commands',
                'reason': 'Explore capabilities'
            },
            {
                'command': '/chain',
                'description': 'Run command chains',
                'reason': 'Automate workflows'
            }
        ])
        
        return suggestions


def format_suggestions(suggestions: List[Dict[str, Any]]) -> str:
    """Format suggestions for display."""
    if not suggestions:
        return ""
    
    output = "\n💡 Next steps:\n"
    
    for i, suggestion in enumerate(suggestions[:3]):  # Show max 3 primary suggestions
        cmd = suggestion['command']
        desc = suggestion['description']
        
        # Add aliases if present
        if 'aliases' in suggestion and suggestion['aliases']:
            alias_str = f" ({', '.join(suggestion['aliases'])})"
        else:
            alias_str = ""
        
        # Add reason if present
        if 'reason' in suggestion:
            reason = f" - {suggestion['reason']}"
        else:
            reason = ""
        
        output += f"  → {cmd}{alias_str} - {desc}{reason}\n"
    
    if len(suggestions) > 3:
        output += f"  → /help - {len(suggestions) - 3} more options available\n"
    
    output += "\n📚 Need help?\n"
    output += "  • /help - See all available commands\n"
    output += "  • /think-through \"what should I do next?\" - Get AI guidance\n"
    
    return output


def main():
    """Main entry point for next command suggester."""
    try:
        # Read tool use data from stdin
        tool_data = json.load(sys.stdin)
        
        # Extract command and result
        command = tool_data.get('tool_name', '')
        result = tool_data.get('result', {})
        
        # Initialize decision engine
        engine = WorkflowDecisionEngine()
        
        # Get suggestions
        suggestions = engine.get_suggestions(command, result)
        
        # Format and display
        if suggestions:
            output = format_suggestions(suggestions)
            print(output, file=sys.stderr)
        
    except Exception as e:
        # Log errors but don't break the flow
        print(f"Next command suggester error: {str(e)}", file=sys.stderr)
    
    # Always exit successfully
    print(json.dumps({"action": "continue"}))
        return


if __name__ == "__main__":
    main()
