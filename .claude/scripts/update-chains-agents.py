#!/usr/bin/env python3
"""
Update chains.json to use correct native agent names instead of persona names
"""

import json
import re

# Agent name mappings from personas to native agents
AGENT_MAPPINGS = {
    # Direct mappings
    "frontend": "frontend-ux-specialist",
    "backend": "backend",
    "security": "security-threat-analyst",
    "qa": "qa",
    "architect": "system-architect",
    "performance": "performance",
    "integrator": "integration-specialist",  # Will need to create this
    "data": "database-architect",
    
    # Additional mappings found in chains
    "performance-optimizer": "performance",
    "qa-test-engineer": "qa",
    "backend-reliability-engineer": "backend",
    "privacy-compliance": "privacy-compliance",
    "product-manager-orchestrator": "pm-orchestrator",
    "platform-deployment": "platform-deployment",
    "documentation-writer": "documentation-writer",
    "documentation-specialist": "documentation-writer",
    "systems-architect": "system-architect",  # Fix duplicate
    "code-analyzer-debugger": "analyzer",
    "security-auditor": "security-threat-analyst",
    "threat-modeler": "security-threat-analyst",
    "accessibility-specialist": "frontend-ux-specialist",  # Frontend handles a11y
    "prediction-engine": "analyzer",
    "git-workflow-automation": "automation-workflow-engineer",
    "debug-specialist": "analyzer",
    "mobile-specialist": "frontend-ux-specialist",
    "security-engineer": "security-threat-analyst",
    "devops-engineer": "platform-deployment",
}

def update_agent_name(agent_name):
    """Update agent name to use native agent"""
    return AGENT_MAPPINGS.get(agent_name, agent_name)

def process_chains(chains_data):
    """Process chains data and update agent names"""
    updated_count = 0
    
    for chain_name, chain_data in chains_data.get("chains", {}).items():
        # Handle steps that are agent-based
        if "steps" in chain_data and isinstance(chain_data["steps"], list):
            for step in chain_data["steps"]:
                if isinstance(step, dict):
                    # Single agent in step
                    if "agent" in step:
                        old_name = step["agent"]
                        new_name = update_agent_name(old_name)
                        if old_name != new_name:
                            step["agent"] = new_name
                            updated_count += 1
                            print(f"  Updated: {old_name} → {new_name}")
                    
                    # Multiple agents in step
                    if "agents" in step and isinstance(step["agents"], list):
                        for agent_item in step["agents"]:
                            if isinstance(agent_item, dict) and "agent" in agent_item:
                                old_name = agent_item["agent"]
                                new_name = update_agent_name(old_name)
                                if old_name != new_name:
                                    agent_item["agent"] = new_name
                                    updated_count += 1
                                    print(f"  Updated: {old_name} → {new_name}")
        
        # Handle phases (for complex chains)
        if "phases" in chain_data and isinstance(chain_data["phases"], list):
            for phase in chain_data["phases"]:
                if "agents" in phase and isinstance(phase["agents"], list):
                    for agent_item in phase["agents"]:
                        if isinstance(agent_item, dict) and "agent" in agent_item:
                            old_name = agent_item["agent"]
                            new_name = update_agent_name(old_name)
                            if old_name != new_name:
                                agent_item["agent"] = new_name
                                updated_count += 1
                                print(f"  Updated: {old_name} → {new_name}")
    
    return chains_data, updated_count

def main():
    chains_file = "/Users/shawnsmith/dev/bfc/boilerplate/.claude/chains.json"
    
    print("Updating chains.json to use native agent names...")
    
    # Read current chains
    with open(chains_file, 'r') as f:
        chains_data = json.load(f)
    
    # Backup original
    with open(chains_file + '.backup', 'w') as f:
        json.dump(chains_data, f, indent=2)
    
    # Update agent names
    updated_data, count = process_chains(chains_data)
    
    # Write updated chains
    with open(chains_file, 'w') as f:
        json.dump(updated_data, f, indent=2)
    
    print(f"\n✅ Updated {count} agent references")
    print(f"📋 Backup saved to: {chains_file}.backup")
    
    # Check for agents that need to be created
    missing_agents = {
        "integration-specialist": "External API integration, webhooks, third-party services"
    }
    
    if missing_agents:
        print("\n⚠️  Missing agents that need to be created:")
        for agent, desc in missing_agents.items():
            print(f"  - {agent}: {desc}")

if __name__ == "__main__":
    main()
