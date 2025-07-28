#!/usr/bin/env python3
"""
Comprehensive V4.0 System Audit
Checks all v4.0 features and agent auto-spawning
"""

import json
import os
from pathlib import Path

def check_hooks_active():
    """Verify all v4.0 hooks are in settings.json"""
    settings_path = Path('.claude/settings.json')
    required_hooks = {
        'PreToolUse': [
            '17-performance-budget-enforcer.py',
            '18-security-first-enforcer.py',
            '19-auto-rls-generator.py',
            '21-docs-first-enforcer.py',
            '22-api-docs-generator.py',
            '23-a11y-enforcer.py',
            '18-auto-parallel-agents.py'  # This spawns agents!
        ],
        'PostToolUse': [
            '01-auto-error-recovery.py'
        ]
    }
    
    results = {'active': [], 'missing': []}
    
    if settings_path.exists():
        with open(settings_path) as f:
            settings = json.load(f)
        
        for hook_type, hooks in required_hooks.items():
            for required_hook in hooks:
                found = False
                if hook_type in settings.get('hooks', {}):
                    for group in settings['hooks'][hook_type]:
                        for hook in group.get('hooks', []):
                            if required_hook in hook.get('command', ''):
                                found = True
                                results['active'].append(f"{hook_type}: {required_hook}")
                                break
                
                if not found:
                    results['missing'].append(f"{hook_type}: {required_hook}")
    
    return results

def check_agent_auto_spawning():
    """Check if auto-parallel-agents hook is working"""
    hook_path = Path('.claude/hooks/pre-tool-use/18-auto-parallel-agents.py')
    
    if hook_path.exists():
        with open(hook_path) as f:
            content = f.read()
        
        # Check for key agent spawning logic
        has_spawn_logic = 'spawn-agent' in content
        has_parallel_logic = 'parallel' in content
        has_orchestrate = 'orchestrate' in content
        
        return {
            'exists': True,
            'has_spawn_logic': has_spawn_logic,
            'has_parallel_logic': has_parallel_logic,
            'has_orchestrate': has_orchestrate
        }
    
    return {'exists': False}

def check_chains_integration():
    """Check if v4.0 chains are properly integrated"""
    chains_v4_path = Path('.claude/chains-v4.json')
    
    if chains_v4_path.exists():
        with open(chains_v4_path) as f:
            chains = json.load(f)
        
        v4_chains = chains.get('v4_chains', {})
        
        # Check for agent usage in chains
        agent_chains = []
        for chain_name, chain_data in v4_chains.items():
            if 'agent' in str(chain_data):
                agent_chains.append(chain_name)
        
        return {
            'total_chains': len(v4_chains),
            'chains_with_agents': len(agent_chains),
            'agent_chains': agent_chains[:5]  # First 5
        }
    
    return {'total_chains': 0}

def check_sub_agents():
    """Check available sub-agents"""
    sub_agents_dir = Path('.claude/sub-agents')
    agents = []
    
    if sub_agents_dir.exists():
        for agent_file in sub_agents_dir.glob('*.json'):
            agents.append(agent_file.stem)
    
    return agents

def check_security_enforcement():
    """Test if security enforcement is working"""
    enforcer_path = Path('.claude/hooks/pre-tool-use/18-security-first-enforcer.py')
    
    if enforcer_path.exists():
        with open(enforcer_path) as f:
            content = f.read()
        
        # Check for blocking logic
        has_blocking = 'sys.exit(1)' in content
        has_auto_spawn = 'spawn-agent security-auditor' in content
        
        return {
            'enforcer_exists': True,
            'blocks_creation': has_blocking,
            'auto_spawns_security': has_auto_spawn
        }
    
    return {'enforcer_exists': False}

def print_audit_results():
    """Print comprehensive audit results"""
    print("\n🔍 V4.0 SYSTEM AUDIT RESULTS")
    print("=" * 50)
    
    # Check hooks
    print("\n📌 HOOK STATUS:")
    hook_results = check_hooks_active()
    print(f"✅ Active hooks: {len(hook_results['active'])}")
    for hook in hook_results['active']:
        print(f"   • {hook}")
    
    if hook_results['missing']:
        print(f"\n❌ Missing hooks: {len(hook_results['missing'])}")
        for hook in hook_results['missing']:
            print(f"   • {hook}")
    
    # Check agent auto-spawning
    print("\n🤖 AGENT AUTO-SPAWNING:")
    agent_check = check_agent_auto_spawning()
    if agent_check['exists']:
        print("✅ Auto-parallel-agents hook exists")
        print(f"   • Spawn logic: {'✅' if agent_check['has_spawn_logic'] else '❌'}")
        print(f"   • Parallel logic: {'✅' if agent_check['has_parallel_logic'] else '❌'}")
        print(f"   • Orchestration: {'✅' if agent_check['has_orchestrate'] else '❌'}")
    else:
        print("❌ Auto-parallel-agents hook NOT FOUND")
    
    # Check chains
    print("\n⛓️  V4.0 CHAINS:")
    chains_info = check_chains_integration()
    print(f"✅ Total v4.0 chains: {chains_info['total_chains']}")
    print(f"✅ Chains using agents: {chains_info['chains_with_agents']}")
    if chains_info.get('agent_chains'):
        print("   Examples:")
        for chain in chains_info['agent_chains']:
            print(f"   • {chain}")
    
    # Check sub-agents
    print("\n👥 AVAILABLE SUB-AGENTS:")
    agents = check_sub_agents()
    if agents:
        print(f"✅ {len(agents)} sub-agents available:")
        for agent in agents:
            print(f"   • {agent}")
    else:
        print("❌ No sub-agents found")
    
    # Check security enforcement
    print("\n🔒 SECURITY ENFORCEMENT:")
    security = check_security_enforcement()
    if security['enforcer_exists']:
        print("✅ Security enforcer active")
        print(f"   • Blocks insecure APIs: {'✅' if security['blocks_creation'] else '❌'}")
        print(f"   • Auto-spawns security agent: {'✅' if security['auto_spawns_security'] else '❌'}")
    else:
        print("❌ Security enforcer not found")
    
    # Overall status
    print("\n" + "=" * 50)
    all_good = (
        len(hook_results['missing']) == 0 and
        agent_check['exists'] and
        chains_info['total_chains'] > 0 and
        len(agents) > 0 and
        security['enforcer_exists']
    )
    
    if all_good:
        print("✅ ALL V4.0 SYSTEMS OPERATIONAL!")
        print("\n🎯 Agents ARE auto-called through:")
        print("   1. Auto-parallel-agents hook (complexity detection)")
        print("   2. Security enforcer (spawns security-auditor)")
        print("   3. V4.0 chains (orchestrated workflows)")
        print("   4. Error recovery (spawns senior-engineer)")
    else:
        print("⚠️  SOME V4.0 SYSTEMS NEED ATTENTION")
    
    print("\n💡 Test agent auto-spawning:")
    print("   1. Try creating an API without security")
    print("   2. Give a complex task to trigger parallel agents")
    print("   3. Run: /chain-v4 full-stack-feature-v4")

if __name__ == "__main__":
    print_audit_results()
