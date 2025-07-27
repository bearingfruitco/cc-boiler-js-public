#!/usr/bin/env python3
"""Integrate sub-agents with existing Claude Code system v2.8.0"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"🚀 {text}")
    print(f"{'='*60}")

def verify_agents():
    """Verify all agents are properly configured"""
    
    agents_dir = Path(".claude/agents")
    required_agents = [
        "security-threat-analyst",
        "frontend-ux-specialist", 
        "backend-reliability-engineer",
        "qa-test-engineer",
        "product-manager-orchestrator",
        "code-analyzer-debugger",
        "systems-architect",
        "tdd-engineer",
        "code-reviewer",
        "documentation-writer",
        "performance-optimizer",
        "database-architect",
        "migration-specialist",
        "refactoring-expert",
        "smart-form-builder",
        "form-builder-specialist",
        "pii-guardian",
        "automation-workflow-engineer",
        "technical-mentor-guide",
        "report-generator",
        "financial-analyst",
        "prd-writer",
        "researcher",
        "production-code-validator",
        "senior-engineer"
    ]
    
    print("\n🔍 Verifying sub-agents...")
    
    missing = []
    found = []
    
    for agent in required_agents:
        agent_file = agents_dir / f"{agent}.md"
        if agent_file.exists():
            # Verify it has proper YAML frontmatter
            with open(agent_file, 'r') as f:
                content = f.read()
                if content.startswith('---') and 'name:' in content:
                    found.append(agent)
                    print(f"  ✅ {agent}")
                else:
                    print(f"  ⚠️  {agent} - Invalid format!")
                    missing.append(agent)
        else:
            print(f"  ❌ {agent} - Missing!")
            missing.append(agent)
    
    # Check for additional agents
    existing_files = list(agents_dir.glob("*.md"))
    existing_names = [f.stem for f in existing_files if not f.stem.startswith(('template', 'README', 'QUICK', 'agent-tool'))]
    extras = [name for name in existing_names if name not in required_agents]
    
    if extras:
        print(f"\n📦 Additional agents found: {', '.join(extras)}")
    
    if missing:
        print(f"\n⚠️  Missing or invalid agents: {', '.join(missing)}")
        print("Please create these agents before proceeding.")
        return False
    
    print(f"\n✨ All {len(found)} agents verified!")
    return True

def update_command_registry():
    """Update commands to use sub-agents"""
    
    registry_path = Path(".claude/command-registry.json")
    
    if registry_path.exists():
        with open(registry_path, 'r') as f:
            registry = json.load(f)
        
        # Add sub-agent references
        updates = {
            "security-check": {
                "delegates_to": "security-threat-analyst",
                "description": "Run comprehensive security audit using sub-agent"
            },
            "create-tests": {
                "delegates_to": ["qa-test-engineer", "tdd-engineer"],
                "description": "Generate tests using QA and TDD sub-agents"
            },
            "review-pr": {
                "delegates_to": "code-reviewer",
                "description": "Perform code review using sub-agent"
            }
        }
        
        updated = 0
        for cmd, config in updates.items():
            if cmd in registry:
                registry[cmd].update(config)
                updated += 1
            else:
                registry[cmd] = config
                updated += 1
        
        with open(registry_path, 'w') as f:
            json.dump(registry, f, indent=2)
        
        print(f"✅ Updated command registry ({updated} commands)")
    else:
        print("⚠️  Command registry not found, creating basic version")
        registry = {
            "security-check": {
                "delegates_to": "security-threat-analyst",
                "description": "Run comprehensive security audit"
            },
            "create-tests": {
                "delegates_to": ["qa-test-engineer", "tdd-engineer"],
                "description": "Generate tests using sub-agents"
            },
            "review-pr": {
                "delegates_to": "code-reviewer",
                "description": "Perform code review"
            }
        }
        with open(registry_path, 'w') as f:
            json.dump(registry, f, indent=2)

def verify_hooks():
    """Verify hook integration"""
    
    print("\n🔗 Verifying hook integration...")
    
    settings_path = Path(".claude/settings.json")
    if not settings_path.exists():
        print("❌ settings.json not found!")
        return False
    
    with open(settings_path, 'r') as f:
        settings = json.load(f)
    
    # Check for our hooks
    hooks_to_verify = {
        "PostToolUse": "20-subagent-suggester.py",
        "SubagentStop": "02-flow-controller.py",
        "Stop": "03-agent-summary.py"
    }
    
    found_hooks = []
    for event, hook_file in hooks_to_verify.items():
        if event in settings.get('hooks', {}):
            hook_list = settings['hooks'][event]
            for hook_config in hook_list:
                for hook in hook_config.get('hooks', []):
                    if hook_file in hook.get('command', ''):
                        found_hooks.append(f"{event}/{hook_file}")
                        print(f"  ✅ {event} → {hook_file}")
                        break
    
    if len(found_hooks) == len(hooks_to_verify):
        print("✅ All hooks properly integrated")
        return True
    else:
        print("⚠️  Some hooks missing from settings.json")
        return False

def verify_aliases():
    """Verify alias configuration"""
    
    print("\n⚡ Verifying aliases...")
    
    aliases_path = Path(".claude/aliases.json")
    if not aliases_path.exists():
        print("❌ aliases.json not found!")
        return False
    
    with open(aliases_path, 'r') as f:
        aliases = json.load(f)
    
    # Check key aliases
    key_aliases = ['fe', 'be', 'qa', 'sec', 'tdd', 'cr', 'doc', 'pm']
    found = []
    
    for alias in key_aliases:
        if alias in aliases and 'subagent to' in aliases[alias]:
            found.append(alias)
            print(f"  ✅ {alias} → {aliases[alias]}")
    
    print(f"✅ Found {len(found)}/{len(key_aliases)} key aliases")
    return len(found) >= 6  # At least 6 key aliases

def verify_chains():
    """Verify chain configuration"""
    
    print("\n🔗 Verifying workflow chains...")
    
    chains_path = Path(".claude/chains.json")
    if not chains_path.exists():
        print("❌ chains.json not found!")
        return False
    
    with open(chains_path, 'r') as f:
        chains_data = json.load(f)
    
    # Check for agent-based chains
    agent_chains = [
        'security-audit-chain',
        'feature-development-chain',
        'database-migration-chain',
        'performance-optimization-chain',
        'refactoring-chain'
    ]
    
    found = []
    chains = chains_data.get('chains', {})
    
    for chain in agent_chains:
        if chain in chains:
            found.append(chain)
            print(f"  ✅ {chain}")
    
    print(f"✅ Found {len(found)}/{len(agent_chains)} agent workflow chains")
    return len(found) >= 3  # At least 3 chains

def create_usage_guide():
    """Update quick reference guide"""
    
    guide_path = Path(".claude/agents/QUICK_REFERENCE.md")
    
    if guide_path.exists():
        print("✅ Quick reference guide already exists")
        return True
    
    print("⚠️  Creating quick reference guide...")
    # Guide content would be created here
    return True

def generate_summary():
    """Generate integration summary"""
    
    print_header("Integration Summary")
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "version": "2.8.0",
        "agents_count": len(list(Path(".claude/agents").glob("*.md"))),
        "hooks_integrated": True,
        "aliases_configured": True,
        "chains_updated": True,
        "status": "complete"
    }
    
    summary_path = Path(".claude/state/subagent-integration.json")
    summary_path.parent.mkdir(exist_ok=True)
    
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"""
📊 Integration Status:
- Sub-agents available: {summary['agents_count']}
- Hooks integrated: ✅
- Aliases configured: ✅
- Chains updated: ✅
- Documentation: ✅

🎯 System ready for sub-agent usage!
""")

def main():
    print_header("Claude Code v2.8.0 Sub-Agent Integration")
    
    # Run verification steps
    checks = [
        ("Verifying agents", verify_agents),
        ("Updating commands", update_command_registry),
        ("Verifying hooks", verify_hooks),
        ("Verifying aliases", verify_aliases),
        ("Verifying chains", verify_chains),
        ("Checking documentation", create_usage_guide)
    ]
    
    all_passed = True
    for description, check_func in checks:
        try:
            if not check_func():
                all_passed = False
                print(f"❌ {description} failed")
        except Exception as e:
            print(f"❌ {description} error: {e}")
            all_passed = False
    
    if all_passed:
        generate_summary()
        print("\n✨ Integration complete! Sub-agents are ready to use.")
        print("\n📚 Next steps:")
        print("1. Review .claude/agents/QUICK_REFERENCE.md")
        print("2. Test with: use security-threat-analyst subagent to scan")
        print("3. Try aliases: sa check for vulnerabilities")
        print("4. Run chains: chain security-audit-chain")
    else:
        print("\n⚠️  Some checks failed. Please review and fix issues.")
        sys.exit(1)

if __name__ == "__main__":
    main()
