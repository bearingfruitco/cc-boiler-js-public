#!/usr/bin/env python3
"""
Test suite for Next Command Suggestion System
Tests all scenarios from command-decision-guide
"""

import pytest
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, mock_open

# Add hook directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / '.claude/hooks/post-tool-use'))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / '.claude/hooks/utils'))

from next_command_suggester import (
    WorkflowDecisionEngine,
    extract_command_from_tool,
    check_for_conflicts
)
from suggestion_utils import (
    ContextLoader,
    ComplexityAnalyzer,
    OrchestrationCalculator,
    CommandMappings
)


class TestWorkflowDecisionEngine:
    """Test the main decision engine."""
    
    def test_new_project_detection(self):
        """Test detection of new projects."""
        with patch('pathlib.Path.exists', return_value=False):
            engine = WorkflowDecisionEngine()
            assert engine.context['is_new_project'] is True
            
            suggestions = engine.get_decision_tree_suggestions()
            commands = [s['command'] for s in suggestions]
            assert '/init-project' in commands
            assert '/py-prd PROJECT' in commands
    
    def test_complexity_analysis(self):
        """Test feature complexity analysis."""
        engine = WorkflowDecisionEngine()
        
        # Simple
        assert engine.analyze_complexity("fix typo in readme") == 'simple'
        assert engine.analyze_complexity("update button color") == 'simple'
        
        # Medium
        assert engine.analyze_complexity("implement user authentication with JWT") == 'medium'
        assert engine.analyze_complexity("add API endpoint for data export") == 'medium'
        
        # Complex
        assert engine.analyze_complexity("research and implement ML-based lead scoring") == 'complex'
        assert engine.analyze_complexity("figure out real-time collaboration architecture") == 'complex'
    
    def test_command_specific_suggestions(self):
        """Test suggestions for each command type."""
        engine = WorkflowDecisionEngine()
        
        # Test CTI suggestions
        cti_result = {"issue_number": "42"}
        cti_args = {"title": "Add user avatar", "body": "Simple enhancement"}
        suggestions = engine.get_command_specific_suggestions('cti', cti_args, cti_result)
        
        commands = [s['command'] for s in suggestions]
        assert any('/gt' in cmd for cmd in commands)
        assert any('/fw start 42' in cmd for cmd in commands)
        
        # Test complex CTI (should suggest PRP)
        complex_args = {"title": "ML scoring", "body": "Research ML approaches for lead scoring"}
        suggestions = engine.get_command_specific_suggestions('cti', complex_args, {})
        commands = [s['command'] for s in suggestions]
        assert any('/prp' in cmd for cmd in commands)
    
    def test_prp_workflow_suggestions(self):
        """Test PRP workflow suggestions."""
        engine = WorkflowDecisionEngine()
        
        # Create PRP
        suggestions = engine.get_command_specific_suggestions('create-prp', {'name': 'ml-scoring'}, {})
        commands = [s['command'] for s in suggestions]
        assert '/prp-execute ml-scoring' in commands
        
        # Execute PRP
        suggestions = engine.get_command_specific_suggestions('prp-execute', {}, {})
        commands = [s['command'] for s in suggestions]
        assert '/prp-status' in commands
        
        # Complete PRP
        suggestions = engine.get_command_specific_suggestions('prp-complete', {}, {})
        commands = [s['command'] for s in suggestions]
        assert any('/cti' in cmd for cmd in commands)
        assert any('/py-prd' in cmd for cmd in commands)
    
    def test_orchestration_suggestions(self):
        """Test orchestration benefit calculation."""
        engine = WorkflowDecisionEngine()
        
        # Many tasks across domains
        gt_result = {
            'tasks': [
                {'domain': 'frontend', 'estimated_time': 60},
                {'domain': 'frontend', 'estimated_time': 45},
                {'domain': 'backend', 'estimated_time': 90},
                {'domain': 'backend', 'estimated_time': 60},
                {'domain': 'database', 'estimated_time': 30},
            ]
        }
        
        suggestions = engine.get_command_specific_suggestions('gt', {'feature': 'auth'}, gt_result)
        
        # Should suggest orchestration
        orch_suggestion = next((s for s in suggestions if '/orch' in s['command']), None)
        assert orch_suggestion is not None
        assert 'agents=3' in orch_suggestion['command']
        assert 'save' in orch_suggestion['reason'].lower()
    
    def test_situational_suggestions(self):
        """Test time-based and context-based suggestions."""
        engine = WorkflowDecisionEngine()
        
        # Morning context
        with patch('datetime.datetime') as mock_dt:
            mock_dt.now.return_value.hour = 9
            engine.context['is_morning'] = True
            suggestions = engine.get_situational_suggestions()
            
            commands = [s['command'] for s in suggestions]
            assert '/sr' in commands
        
        # Stuck context
        engine.context['appears_stuck'] = True
        suggestions = engine.get_situational_suggestions()
        commands = [s['command'] for s in suggestions]
        assert '/help-decide' in commands
        assert any('think-through' in cmd for cmd in commands)
    
    def test_bug_workflow_suggestions(self):
        """Test bug tracking workflow."""
        engine = WorkflowDecisionEngine()
        
        # Add bug
        suggestions = engine.get_command_specific_suggestions('bt add', {}, {'id': '5'})
        commands = [s['command'] for s in suggestions]
        assert any('generate-tests' in cmd for cmd in commands)
        assert any('/mt' in cmd for cmd in commands)
    
    def test_test_result_suggestions(self):
        """Test suggestions based on test results."""
        engine = WorkflowDecisionEngine()
        
        # Tests pass
        pass_result = {'all_passed': True}
        suggestions = engine.get_command_specific_suggestions('test', {}, pass_result)
        commands = [s['command'] for s in suggestions]
        assert '/fw complete' in commands
        
        # Tests fail
        fail_result = {'all_passed': False, 'failures': ['test_auth']}
        suggestions = engine.get_command_specific_suggestions('test', {}, fail_result)
        commands = [s['command'] for s in suggestions]
        assert any('/bt add' in cmd for cmd in commands)
        assert any('think-through' in cmd for cmd in commands)


class TestComplexityAnalyzer:
    """Test complexity analysis."""
    
    def test_keyword_detection(self):
        """Test keyword-based complexity detection."""
        analyzer = ComplexityAnalyzer()
        
        # Complex keywords
        assert analyzer.analyze("research the best approach") == 'complex'
        assert analyzer.analyze("figure out how to implement") == 'complex'
        assert analyzer.analyze("integrate ML pipeline") == 'complex'
        
        # Medium keywords
        assert analyzer.analyze("implement login form") == 'medium'
        assert analyzer.analyze("add database migration") == 'medium'
        
        # Simple keywords
        assert analyzer.analyze("fix typo") == 'simple'
        assert analyzer.analyze("update label text") == 'simple'
    
    def test_length_factor(self):
        """Test that text length affects complexity."""
        analyzer = ComplexityAnalyzer()
        
        short = "fix bug"
        long = "x" * 400  # Very long description
        
        assert analyzer.analyze(short) == 'simple'
        # Long descriptions tend toward complex
        assert analyzer.analyze(long) in ['medium', 'complex']


class TestOrchestrationCalculator:
    """Test orchestration benefit calculations."""
    
    def test_should_suggest_orchestration(self):
        """Test orchestration suggestion logic."""
        calc = OrchestrationCalculator()
        
        # Too few tasks
        few_tasks = [{'domain': 'frontend'} for _ in range(3)]
        assert not calc.should_suggest_orchestration(few_tasks)
        
        # Many tasks, one domain
        single_domain = [{'domain': 'frontend'} for _ in range(10)]
        assert not calc.should_suggest_orchestration(single_domain)
        
        # Many tasks, multiple domains
        multi_domain = [
            {'domain': 'frontend'},
            {'domain': 'frontend'},
            {'domain': 'backend'},
            {'domain': 'backend'},
            {'domain': 'database'},
        ]
        assert calc.should_suggest_orchestration(multi_domain)
    
    def test_calculate_optimal_agents(self):
        """Test agent count calculation."""
        calc = OrchestrationCalculator()
        
        tasks = [
            {'domain': 'frontend'},
            {'domain': 'backend'},
            {'domain': 'database'},
            {'domain': 'api'},
            {'domain': 'testing'},
            {'domain': 'docs'},
        ]
        
        # Should cap at 5
        assert calc.calculate_optimal_agents(tasks) == 5
    
    def test_time_saved_calculation(self):
        """Test time savings estimation."""
        calc = OrchestrationCalculator()
        
        tasks = [
            {'estimated_time': 60},
            {'estimated_time': 45},
            {'estimated_time': 30},
            {'estimated_time': 90},
        ]
        
        # Total: 225 min, 30% savings = 67.5 min
        assert calc.calculate_time_saved(tasks) == 67


class TestCommandExtraction:
    """Test command extraction from tool names."""
    
    def test_direct_tool_mapping(self):
        """Test direct tool name to command mapping."""
        assert extract_command_from_tool('create_issue', {}) == 'cti'
        assert extract_command_from_tool('generate_tasks', {}) == 'gt'
        assert extract_command_from_tool('feature_workflow_start', {}) == 'fw start'
        assert extract_command_from_tool('create_prp', {}) == 'prp'
    
    def test_file_creation_commands(self):
        """Test extracting command from file creation."""
        args = {'path': '.claude/commands/test-command.md'}
        assert extract_command_from_tool('create_file', args) == 'test-command'
    
    def test_run_command_extraction(self):
        """Test extracting from run_command tool."""
        args = {'command': '/gt user-auth'}
        assert extract_command_from_tool('run_command', args) == 'gt'


class TestConflictDetection:
    """Test conflict detection with other hooks."""
    
    def test_detects_existing_suggestions(self):
        """Test detection of existing suggestions."""
        assert check_for_conflicts('test', {'orchestration_suggestion': 'use /orch'})
        assert check_for_conflicts('test', {'suggested_persona': 'frontend'})
        assert check_for_conflicts('test', 'Next steps: do something')
        assert not check_for_conflicts('test', 'Regular output')


class TestContextLoader:
    """Test context loading utilities."""
    
    @patch('pathlib.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_full_context(self, mock_file, mock_exists):
        """Test comprehensive context loading."""
        mock_exists.return_value = True
        mock_file.return_value.read.return_value = json.dumps({
            'issue_number': '42',
            'feature_name': 'user-auth',
            'branch_name': 'feature/user-auth'
        })
        
        context = ContextLoader.load_full_context()
        
        assert isinstance(context, dict)
        assert 'is_new_project' in context
        assert 'has_prd' in context
        assert 'has_tasks' in context
        assert 'is_morning' in context
        assert 'is_evening' in context


class TestCommandMappings:
    """Test command mapping utilities."""
    
    def test_workflow_chains(self):
        """Test workflow chain mappings."""
        chains = CommandMappings.WORKFLOW_CHAINS
        
        # Init project chain
        assert 'gi PROJECT' in chains['init-project']
        assert 'fw start 1' in chains['init-project']
        
        # PRP chain
        assert 'prp-execute' in chains['prp']
        assert 'prp-status' in chains['prp']
        
        # CTI chain
        assert 'gt' in chains['cti']
        assert 'fw start' in chains['cti']
    
    def test_situational_mappings(self):
        """Test situational suggestion mappings."""
        situational = CommandMappings.SITUATIONAL
        
        # Morning suggestions
        morning_cmds = [s['command'] for s in situational['morning']]
        assert '/sr' in morning_cmds
        
        # Stuck suggestions
        stuck_cmds = [s['command'] for s in situational['stuck']]
        assert '/help-decide' in stuck_cmds


class TestEndToEndScenarios:
    """Test complete workflow scenarios."""
    
    def test_new_project_flow(self):
        """Test new project initialization flow."""
        engine = WorkflowDecisionEngine()
        engine.context['is_new_project'] = True
        
        # Should suggest init
        suggestions = engine.get_decision_tree_suggestions()
        assert any('init-project' in s['command'] for s in suggestions)
        
        # After init, should suggest issues
        init_suggestions = engine.get_command_specific_suggestions('init-project', {}, {})
        assert any('/gi PROJECT' in s['command'] for s in init_suggestions)
    
    def test_feature_development_flow(self):
        """Test complete feature development flow."""
        engine = WorkflowDecisionEngine()
        
        # 1. CTI creates issue
        cti_result = {'issue_number': '10'}
        suggestions = engine.get_command_specific_suggestions('cti', 
            {'title': 'Add auth'}, cti_result)
        assert any('/gt' in s['command'] for s in suggestions)
        
        # 2. GT generates tasks
        gt_result = {'tasks': [{'domain': 'frontend'}, {'domain': 'backend'}]}
        suggestions = engine.get_command_specific_suggestions('gt', 
            {'feature': 'auth'}, gt_result)
        assert any('/fw start' in s['command'] for s in suggestions)
        
        # 3. FW starts work
        suggestions = engine.get_command_specific_suggestions('fw start', 
            {'issue': '10'}, {})
        assert any('/pt' in s['command'] for s in suggestions)
        
        # 4. PT processes tasks
        suggestions = engine.get_command_specific_suggestions('pt', {}, {})
        assert any('/test' in s['command'] for s in suggestions)
        
        # 5. Tests pass
        suggestions = engine.get_command_specific_suggestions('test', 
            {}, {'all_passed': True})
        assert any('/fw complete' in s['command'] for s in suggestions)
    
    def test_research_flow(self):
        """Test research workflow."""
        engine = WorkflowDecisionEngine()
        
        # Complex feature needs research
        complex_args = {
            'title': 'ML scoring',
            'body': 'Figure out how to implement ML-based lead scoring'
        }
        suggestions = engine.get_command_specific_suggestions('cti', complex_args, {})
        assert any('/prp' in s['command'] for s in suggestions)
        
        # PRP flow
        prp_suggestions = engine.get_command_specific_suggestions('create-prp', 
            {'name': 'ml-scoring'}, {})
        assert any('prp-execute' in s['command'] for s in prp_suggestions)


# Run tests if executed directly
if __name__ == '__main__':
    pytest.main([__file__, '-v'])
