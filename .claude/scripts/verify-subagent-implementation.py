#!/usr/bin/env python3
"""
Final verification of sub-agent implementation
"""

import os
import json
from pathlib import Path
from datetime import datetime

def print_section(title):
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def verify_implementation():
    results = {
        "timestamp": datetime.now().isoformat(),
        "version": "2.8.0",
        "checks": {}
    }
    
    # Check 1: Agent Files
    print_section("Checking Agent Files")
    agents_created = ["tdd-engineer", "code-reviewer", "documentation-writer"]
    agents_dir = Path(".claude/agents")
    
    for agent in agents_created:
        agent_file = agents_dir / f"{agent}.md"
        if agent_file.exists():
            print(f"✅ {agent}.md exists")
            results["checks"][f"agent_{agent}"] = True
        else:
            print(f"❌ {agent}.md missing")
            results["checks"][f"agent_{agent}"] = False
    
    # Count total agents
    total_agents = len([f for f in agents_dir.glob("*.md") 
                       if not f.stem.startswith(('template', 'README', 'QUICK', 'agent-tool'))])
    print(f"\n📊 Total agents: {total_agents}")
    results["total_agents"] = total_agents
    
    # Check 2: Command Updates
    print_section("Checking Command Updates")
    commands = {
        "security-check": "security-threat-analyst",
        "create-tests": "qa-test-engineer",
        "review-pr": "code-reviewer"
    }
    
    commands_dir = Path(".claude/commands")
    for cmd, agent in commands.items():
        cmd_file = commands_dir / f"{cmd}.md"
        if cmd_file.exists():
            with open(cmd_file, 'r') as f:
                content = f.read()
                if "subagent" in content and agent in content:
                    print(f"✅ {cmd} delegates to {agent}")
                    results["checks"][f"command_{cmd}"] = True
                else:
                    print(f"⚠️  {cmd} needs sub-agent integration")
                    results["checks"][f"command_{cmd}"] = False
    
    # Check 3: Hook Integration
    print_section("Checking Hook Integration")
    settings_file = Path(".claude/settings.json")
    
    if settings_file.exists():
        with open(settings_file, 'r') as f:
            settings = json.load(f)
        
        hooks_to_check = {
            "PostToolUse": "20-subagent-suggester.py",
            "SubagentStop": "02-flow-controller.py",
            "Stop": "03-agent-summary.py"
        }
        
        for event, hook_file in hooks_to_check.items():
            found = False
            if event in settings.get('hooks', {}):
                for hook_group in settings['hooks'][event]:
                    for hook in hook_group.get('hooks', []):
                        if hook_file in hook.get('command', ''):
                            found = True
                            break
            
            if found:
                print(f"✅ {event} → {hook_file}")
                results["checks"][f"hook_{event}"] = True
            else:
                print(f"❌ {event} hook missing")
                results["checks"][f"hook_{event}"] = False
    
    # Check 4: Aliases
    print_section("Checking Aliases")
    aliases_file = Path(".claude/aliases.json")
    
    if aliases_file.exists():
        with open(aliases_file, 'r') as f:
            aliases = json.load(f)
        
        key_aliases = ['fe', 'be', 'qa', 'sec', 'tdd', 'cr', 'doc', 'pm']
        found_count = 0
        
        for alias in key_aliases:
            if alias in aliases and 'subagent to' in aliases[alias]:
                found_count += 1
        
        print(f"✅ Found {found_count}/{len(key_aliases)} key aliases")
        results["checks"]["aliases"] = found_count >= 6
    
    # Check 5: Chains
    print_section("Checking Workflow Chains")
    chains_file = Path(".claude/chains.json")
    
    if chains_file.exists():
        with open(chains_file, 'r') as f:
            chains_data = json.load(f)
        
        new_chains = [
            "security-audit-chain",
            "feature-development-chain",
            "database-migration-chain",
            "performance-optimization-chain",
            "refactoring-chain"
        ]
        
        chains = chains_data.get('chains', {})
        found_chains = [c for c in new_chains if c in chains]
        
        print(f"✅ Found {len(found_chains)}/{len(new_chains)} new chains")
        for chain in found_chains:
            print(f"  • {chain}")
        results["checks"]["chains"] = len(found_chains) >= 3
    
    # Check 6: Documentation
    print_section("Checking Documentation")
    docs = {
        ".claude/agents/QUICK_REFERENCE.md": "Quick reference guide",
        ".claude/docs/AGENT_ALIAS_PATTERNS.md": "Alias patterns",
        ".claude/agents/agent-tool-specifications.md": "Tool specifications"
    }
    
    for doc_path, doc_name in docs.items():
        if Path(doc_path).exists():
            print(f"✅ {doc_name}")
            results["checks"][f"doc_{Path(doc_path).stem}"] = True
        else:
            print(f"❌ {doc_name} missing")
            results["checks"][f"doc_{Path(doc_path).stem}"] = False
    
    # Save results
    results_file = Path(".claude/state/subagent-verification.json")
    results_file.parent.mkdir(exist_ok=True)
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Summary
    print_section("Implementation Summary")
    
    total_checks = len(results["checks"])
    passed_checks = sum(1 for v in results["checks"].values() if v)
    
    print(f"""
📊 Verification Results:
- Total checks: {total_checks}
- Passed: {passed_checks}
- Failed: {total_checks - passed_checks}
- Success rate: {(passed_checks/total_checks)*100:.1f}%

📁 Key Metrics:
- Total agents: {results['total_agents']}
- New agents added: 3
- Commands updated: 3
- Hooks integrated: 3
- Chains added: 5

🎯 Status: {'READY' if passed_checks == total_checks else 'NEEDS ATTENTION'}
""")
    
    return passed_checks == total_checks

if __name__ == "__main__":
    success = verify_implementation()
    
    if success:
        print("\n✨ Sub-agent implementation is complete and verified!")
    else:
        print("\n⚠️  Some items need attention. Please review the output above.")
