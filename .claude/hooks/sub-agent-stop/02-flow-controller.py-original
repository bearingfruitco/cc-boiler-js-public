#!/usr/bin/env python3
"""
Subagent Flow Controller - Manages transitions and suggests next agents
"""

import sys
import json
import os
from datetime import datetime

def get_hook_input():
    """Get and parse hook input from stdin"""
    try:
        return json.loads(sys.stdin.read())
    except:
        return {}

def load_agent_history():
    """Load history of agent usage"""
    history_file = ".claude/state/agent-history.json"
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_agent_history(history):
    """Save agent history"""
    history_file = ".claude/state/agent-history.json"
    os.makedirs(os.path.dirname(history_file), exist_ok=True)
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2)

def get_next_agent_suggestions(current_agent, task_context):
    """Suggest next agents based on workflow patterns"""
    
    workflows = {
        'qa-test-engineer': [
            {'agent': 'tdd-engineer', 'reason': 'Implement tests using TDD approach'},
            {'agent': 'code-reviewer', 'reason': 'Review test implementation'},
            {'agent': 'documentation-writer', 'reason': 'Document test strategies'}
        ],
        'tdd-engineer': [
            {'agent': 'frontend-ux-specialist', 'reason': 'Implement UI with tests in place'},
            {'agent': 'backend-reliability-engineer', 'reason': 'Build reliable APIs'},
            {'agent': 'code-reviewer', 'reason': 'Review implementation'}
        ],
        'frontend-ux-specialist': [
            {'agent': 'qa-test-engineer', 'reason': 'Create UI tests'},
            {'agent': 'performance-optimizer', 'reason': 'Optimize UI performance'},
            {'agent': 'security-threat-analyst', 'reason': 'Check for XSS vulnerabilities'}
        ],
        'backend-reliability-engineer': [
            {'agent': 'database-architect', 'reason': 'Design efficient schemas'},
            {'agent': 'security-threat-analyst', 'reason': 'Audit API security'},
            {'agent': 'qa-test-engineer', 'reason': 'Create API tests'}
        ],
        'security-threat-analyst': [
            {'agent': 'code-reviewer', 'reason': 'Review security fixes'},
            {'agent': 'documentation-writer', 'reason': 'Document security measures'},
            {'agent': 'backend-reliability-engineer', 'reason': 'Implement security fixes'}
        ],
        'code-reviewer': [
            {'agent': 'refactoring-expert', 'reason': 'Refactor based on review'},
            {'agent': 'documentation-writer', 'reason': 'Update docs based on changes'},
            {'agent': 'qa-test-engineer', 'reason': 'Add tests for review findings'}
        ],
        'database-architect': [
            {'agent': 'migration-specialist', 'reason': 'Create migration scripts'},
            {'agent': 'backend-reliability-engineer', 'reason': 'Update APIs for schema'},
            {'agent': 'documentation-writer', 'reason': 'Document schema changes'}
        ],
        'performance-optimizer': [
            {'agent': 'code-reviewer', 'reason': 'Review optimizations'},
            {'agent': 'qa-test-engineer', 'reason': 'Create performance tests'},
            {'agent': 'documentation-writer', 'reason': 'Document performance gains'}
        ],
        'documentation-writer': [
            {'agent': 'code-reviewer', 'reason': 'Review documentation accuracy'},
            {'agent': 'pm-orchestrator', 'reason': 'Update project status'}
        ],
        'pm-orchestrator': [
            {'agent': 'systems-architect', 'reason': 'Define technical approach'},
            {'agent': 'qa-test-engineer', 'reason': 'Create test plan'},
            {'agent': 'prd-writer', 'reason': 'Refine requirements'}
        ]
    }
    
    return workflows.get(current_agent, [])

def main():
    # Get hook input
    hook_data = get_hook_input()
    
    # Extract agent information
    agent_name = hook_data.get('agent_name', '')
    task_completed = hook_data.get('task', '')
    
    if not agent_name:
        return
    
    # Load and update history
    history = load_agent_history()
    history.append({
        'agent': agent_name,
        'task': task_completed,
        'timestamp': datetime.now().isoformat()
    })
    save_agent_history(history)
    
    # Get workflow suggestions
    suggestions = get_next_agent_suggestions(agent_name, task_completed)
    
    if suggestions:
        print("\n✅ **Sub-Agent Task Complete**")
        print(f"The {agent_name} has finished its task.\n")
        print("🔄 **Suggested Next Steps:**\n")
        
        for i, suggestion in enumerate(suggestions[:3], 1):
            print(f"{i}. **{suggestion['agent']}** - {suggestion['reason']}")
            print(f"   ```")
            print(f"   use {suggestion['agent']} subagent to continue workflow")
            print(f"   ```")
        
        # Check for workflow chains
        if len(history) >= 2:
            last_two = [h['agent'] for h in history[-2:]]
            if last_two == ['qa-test-engineer', 'tdd-engineer']:
                print("\n🎯 **TDD Workflow Active**: Consider implementing the feature now that tests are in place.")
            elif last_two == ['security-threat-analyst', 'code-reviewer']:
                print("\n🔒 **Security Review Complete**: Ensure all findings are addressed.")
    
    # Summary of session
    print(f"\n📊 **Session Summary**")
    print(f"Agents used in this session: {len(set(h['agent'] for h in history))}")
    print(f"Total agent invocations: {len(history)}")
    
    # Offer to generate report
    if len(history) > 5:
        print("\n📝 Consider using `report-generator` subagent to create a comprehensive session report.")

if __name__ == "__main__":
    main()
