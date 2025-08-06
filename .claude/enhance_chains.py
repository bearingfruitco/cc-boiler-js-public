#!/usr/bin/env python3
"""
Create enhanced chains with parallel execution support
"""

import json
from pathlib import Path

def enhance_chains():
    chains_file = Path('/Users/shawnsmith/dev/bfc/boilerplate/.claude/config/chains.json')
    
    # Read existing chains
    with open(chains_file, 'r') as f:
        chains = json.load(f)
    
    # Add parallel execution example
    enhanced_chain = {
        "feature-development-parallel": {
            "description": "Feature development with parallel analysis phase",
            "phases": [
                {
                    "name": "analysis",
                    "parallel": True,
                    "steps": [
                        {"agent": "system-architect", "task": "Design system architecture"},
                        {"agent": "security", "task": "Perform threat analysis"},
                        {"agent": "performance", "task": "Analyze performance requirements"}
                    ]
                },
                {
                    "name": "implementation",
                    "parallel": False,
                    "steps": [
                        {"command": "/create-prp database-schema"},
                        {"command": "/create-prp api-endpoints"},
                        {"command": "/create-prp frontend-components"}
                    ]
                },
                {
                    "name": "validation",
                    "parallel": True,
                    "steps": [
                        {"command": "/prp-execute database-schema --level 1"},
                        {"command": "/prp-execute api-endpoints --level 1"},
                        {"command": "/prp-execute frontend-components --level 1"}
                    ]
                }
            ]
        }
    }
    
    # Add to chains
    if 'chains' not in chains:
        chains['chains'] = {}
    
    chains['chains']['feature-development-parallel'] = enhanced_chain['feature-development-parallel']
    
    # Save enhanced version
    backup_file = chains_file.with_suffix('.json.backup')
    chains_file.rename(backup_file)
    
    with open(chains_file, 'w') as f:
        json.dump(chains, f, indent=2)
    
    print(f"✅ Enhanced chains.json with parallel support")
    print(f"✅ Backup saved to {backup_file}")
    print("\nNew parallel chain added: feature-development-parallel")
    print("  - Phase 1: Parallel analysis (3 agents simultaneously)")
    print("  - Phase 2: Sequential implementation")
    print("  - Phase 3: Parallel validation")
    
    return True

if __name__ == '__main__':
    success = enhance_chains()
    exit(0 if success else 1)
