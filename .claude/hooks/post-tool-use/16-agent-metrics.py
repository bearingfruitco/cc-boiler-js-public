#!/usr/bin/env python3
"""
Agent Performance Metrics Tracking Hook

Tracks performance metrics for all persona-based agents including:
- Success rates
- Token usage
- Duration
- Common failure patterns
- Task type effectiveness
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Get Claude environment
CLAUDE_PROJECT_DIR = os.getenv('CLAUDE_PROJECT_DIR', '.')
METRICS_DIR = Path(CLAUDE_PROJECT_DIR) / '.claude' / 'metrics'
AGENT_METRICS_DIR = METRICS_DIR / 'agents'
SESSION_METRICS_DIR = METRICS_DIR / 'sessions'

# Ensure directories exist
AGENT_METRICS_DIR.mkdir(parents=True, exist_ok=True)
SESSION_METRICS_DIR.mkdir(parents=True, exist_ok=True)

def load_tool_data():
    """Load tool data from stdin"""
    try:
        return json.load(sys.stdin)
    except:
        return {}

def extract_agent_info(data):
    """Extract agent/persona information from tool data"""
    tool_name = data.get('tool_name', '')
    tool_input = data.get('tool_input', {})
    
    # Check if this is a sub-agent task
    if tool_name == 'Task':
        task_prompt = tool_input.get('prompt', '')
        # Extract persona mentions
        personas = [
            'frontend', 'backend', 'security', 'qa', 'architect',
            'performance', 'integrator', 'data', 'mentor', 'database',
            'supabase', 'orm', 'analytics', 'ui-systems', 'privacy',
            'event-schema', 'platform', 'documentation', 'tdd'
        ]
        
        for persona in personas:
            if persona in task_prompt.lower():
                return persona, task_prompt
                
    return None, None

def update_agent_metrics(agent_name, task_prompt, tool_data):
    """Update metrics for a specific agent"""
    metrics_file = AGENT_METRICS_DIR / f"{agent_name}.json"
    
    # Load existing metrics
    if metrics_file.exists():
        with open(metrics_file, 'r') as f:
            metrics = json.load(f)
    else:
        metrics = {
            'agent': agent_name,
            'total_tasks': 0,
            'successful_tasks': 0,
            'failed_tasks': 0,
            'total_tokens': 0,
            'total_duration_seconds': 0,
            'task_types': {},
            'common_patterns': {},
            'last_updated': None,
            'performance_history': []
        }
    
    # Update basic counts
    metrics['total_tasks'] += 1
    
    # Detect task type from prompt
    task_type = 'general'
    if 'component' in task_prompt.lower():
        task_type = 'component_creation'
    elif 'api' in task_prompt.lower() or 'endpoint' in task_prompt.lower():
        task_type = 'api_development'
    elif 'test' in task_prompt.lower():
        task_type = 'testing'
    elif 'debug' in task_prompt.lower() or 'fix' in task_prompt.lower():
        task_type = 'debugging'
    elif 'refactor' in task_prompt.lower():
        task_type = 'refactoring'
    elif 'security' in task_prompt.lower() or 'audit' in task_prompt.lower():
        task_type = 'security_audit'
    
    # Update task type metrics
    if task_type not in metrics['task_types']:
        metrics['task_types'][task_type] = {
            'count': 0,
            'success_rate': 0.0,
            'avg_duration': 0.0
        }
    
    metrics['task_types'][task_type]['count'] += 1
    
    # Add to performance history (keep last 100)
    performance_entry = {
        'timestamp': datetime.now().isoformat(),
        'task_type': task_type,
        'prompt_preview': task_prompt[:100] + '...' if len(task_prompt) > 100 else task_prompt
    }
    
    metrics['performance_history'].append(performance_entry)
    if len(metrics['performance_history']) > 100:
        metrics['performance_history'] = metrics['performance_history'][-100:]
    
    metrics['last_updated'] = datetime.now().isoformat()
    
    # Save updated metrics
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    return task_type

def update_session_metrics(agent_name, task_type):
    """Update current session metrics"""
    session_file = SESSION_METRICS_DIR / 'current_session.json'
    
    if session_file.exists():
        with open(session_file, 'r') as f:
            session = json.load(f)
    else:
        session = {
            'session_id': datetime.now().strftime('%Y%m%d_%H%M%S'),
            'started_at': datetime.now().isoformat(),
            'agent_usage': {},
            'task_flow': []
        }
    
    # Update agent usage
    if agent_name not in session['agent_usage']:
        session['agent_usage'][agent_name] = {
            'invocations': 0,
            'task_types': {}
        }
    
    session['agent_usage'][agent_name]['invocations'] += 1
    
    if task_type not in session['agent_usage'][agent_name]['task_types']:
        session['agent_usage'][agent_name]['task_types'][task_type] = 0
    session['agent_usage'][agent_name]['task_types'][task_type] += 1
    
    # Add to task flow
    session['task_flow'].append({
        'timestamp': datetime.now().isoformat(),
        'agent': agent_name,
        'task_type': task_type
    })
    
    # Save session
    with open(session_file, 'w') as f:
        json.dump(session, f, indent=2)

def main():
    # Load tool data
    data = load_tool_data()
    
    # Extract agent information
    agent_name, task_prompt = extract_agent_info(data)
    
    if agent_name and task_prompt:
        # Update agent metrics
        task_type = update_agent_metrics(agent_name, task_prompt, data)
        
        # Update session metrics
        update_session_metrics(agent_name, task_type)
        
        # Log for debugging (will be captured by post-tool-use system)
        print(f"📊 Metrics updated for {agent_name} agent ({task_type} task)")
    
    # Always exit successfully
    sys.exit(0)

if __name__ == "__main__":
    main()
