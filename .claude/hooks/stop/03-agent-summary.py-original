#!/usr/bin/env python3
"""
Agent Summary Hook - Shows available sub-agents when stopping
"""

import sys
import json
import os

def get_hook_input():
    """Get and parse hook input from stdin"""
    try:
        return json.loads(sys.stdin.read())
    except:
        return {}

def get_agent_list():
    """Get list of available agents"""
    agents_dir = ".claude/agents"
    agents = []
    
    if os.path.exists(agents_dir):
        for file in os.listdir(agents_dir):
            if file.endswith('.md') and not file.startswith(('template', 'README', 'QUICK', 'agent-tool')):
                agent_name = file.replace('.md', '')
                agents.append(agent_name)
    
    return sorted(agents)

def get_agent_categories():
    """Categorize agents by function"""
    categories = {
        'Development': [
            'frontend-ux-specialist',
            'backend-reliability-engineer',
            'systems-architect',
            'senior-engineer',
            'tdd-engineer'
        ],
        'Quality & Testing': [
            'qa-test-engineer',
            'code-reviewer',
            'production-code-validator'
        ],
        'Analysis & Security': [
            'security-threat-analyst',
            'analyzer',
            'performance-optimizer',
            'researcher'
        ],
        'Data & Infrastructure': [
            'database-architect',
            'migration-specialist',
            'automation-workflow-engineer'
        ],
        'Documentation & Planning': [
            'documentation-writer',
            'prd-writer',
            'report-generator',
            'pm-orchestrator'
        ],
        'Specialized': [
            'form-builder-specialist',
            'refactoring-expert',
            'financial-analyst',
            'pii-guardian',
            'mentor'
        ]
    }
    
    return categories

def main():
    # Get available agents
    agents = get_agent_list()
    categories = get_agent_categories()
    
    if agents:
        print("\n🤖 **Available Sub-Agents**")
        print(f"You have {len(agents)} specialized agents ready to help:\n")
        
        # Show by category
        for category, agent_list in categories.items():
            available = [a for a in agent_list if a in agents]
            if available:
                print(f"**{category}:**")
                for agent in available:
                    print(f"  • {agent}")
                print()
        
        # Show quick usage
        print("💡 **Quick Usage:**")
        print("```")
        print("use [agent-name] subagent to [task description]")
        print("```")
        
        print("\n⚡ **Aliases:**")
        print("• `fe` → frontend-ux-specialist")
        print("• `be` → backend-reliability-engineer") 
        print("• `qa` → qa-test-engineer")
        print("• `sec` → security-threat-analyst")
        print("• `tdd` → tdd-engineer")
        print("• `cr` → code-reviewer")
        print("• `doc` → documentation-writer")
        print("• `pm` → pm-orchestrator")
        
        print("\n📚 For detailed agent descriptions, check `.claude/agents/`")

if __name__ == "__main__":
    main()
