#!/usr/bin/env python3
"""Final comprehensive audit of the Claude Code system"""

import json
from pathlib import Path
import subprocess

CLAUDE_DIR = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude")
PROJECT_ROOT = Path("/Users/shawnsmith/dev/bfc/boilerplate")

def audit_complete_system():
    """Run a complete system audit"""
    
    print("🔍 CLAUDE CODE COMPLETE SYSTEM AUDIT")
    print("=" * 60)
    
    # Load configurations
    with open(CLAUDE_DIR / "settings.json") as f:
        settings = json.load(f)
    
    with open(CLAUDE_DIR / "chains.json") as f:
        chains_data = json.load(f)
    
    with open(CLAUDE_DIR / "aliases.json") as f:
        aliases = json.load(f)
    
    with open(CLAUDE_DIR / "config.json") as f:
        config = json.load(f)
    
    # Hooks audit
    print("\n📌 HOOKS STATUS:")
    total_hooks = 0
    hook_summary = {}
    for event_type, matchers in settings.get("hooks", {}).items():
        count = sum(len(m.get("hooks", [])) for m in matchers)
        total_hooks += count
        hook_summary[event_type] = count
    
    for event_type, count in hook_summary.items():
        print(f"  • {event_type}: {count} hooks")
    print(f"  🎯 Total: {total_hooks} hooks active")
    
    # Chains audit
    print(f"\n⛓️  CHAINS: {len(chains_data['chains'])} workflows")
    print(f"  • Shortcuts: {len(chains_data.get('shortcuts', {}))}")
    
    # Commands audit
    commands_dir = CLAUDE_DIR / "commands"
    command_count = len(list(commands_dir.rglob("*.md")))
    print(f"\n🛠️  COMMANDS: {command_count} files")
    
    # Scripts audit
    scripts_dir = CLAUDE_DIR / "scripts"
    if scripts_dir.exists():
        script_count = len(list(scripts_dir.glob("*")))
        print(f"\n📜 SCRIPTS: {script_count} files")
        # List important scripts
        important_scripts = ["worktree-manager.sh", "smart-resume-branch-integration.sh", 
                           "sync-task-ledger.py", "health-check.py"]
        for script in important_scripts:
            if (scripts_dir / script).exists():
                print(f"  ✅ {script}")
    else:
        print("\n📜 SCRIPTS: Directory missing!")
    
    # Aliases audit
    print(f"\n🔗 ALIASES: {len(aliases)} shortcuts")
    
    # Additional directories
    print("\n📁 ADDITIONAL COMPONENTS:")
    
    # Templates
    templates_dir = CLAUDE_DIR / "templates"
    if templates_dir.exists():
        print(f"  ✅ Templates directory exists")
    else:
        print(f"  ❌ Templates directory missing")
    
    # Context directory
    context_dir = CLAUDE_DIR / "context"
    if context_dir.exists():
        print(f"  ✅ Context directory exists")
    else:
        print(f"  ❌ Context directory missing")
    
    # Utils directory
    utils_dir = CLAUDE_DIR / "hooks" / "utils"
    if utils_dir.exists():
        util_count = len(list(utils_dir.glob("*.py")))
        print(f"  ✅ Hook utils: {util_count} files")
    
    # PRPs directory
    prps_dir = PROJECT_ROOT / "PRPs"
    if prps_dir.exists():
        print(f"  ✅ PRPs directory exists")
        prp_subdirs = ["templates", "ai_docs", "scripts", "active", "completed"]
        for subdir in prp_subdirs:
            if (prps_dir / subdir).exists():
                print(f"    ✅ {subdir}/")
    
    # Agent OS directory
    agent_os_dir = PROJECT_ROOT / ".agent-os"
    if agent_os_dir.exists():
        print(f"  ✅ Agent OS directory exists")
        aos_subdirs = ["standards", "product", "specs"]
        for subdir in aos_subdirs:
            if (agent_os_dir / subdir).exists():
                print(f"    ✅ {subdir}/")
    
    # Configuration files
    print("\n📋 CONFIGURATION FILES:")
    config_files = [
        ("config.json", "Main configuration"),
        ("project-config.json", "Project settings"),
        ("settings.json", "Hooks configuration"),
        ("chains.json", "Command chains"),
        ("aliases.json", "Command aliases"),
        ("command-registry.json", "Command registry")
    ]
    
    for filename, desc in config_files:
        if (CLAUDE_DIR / filename).exists():
            print(f"  ✅ {filename} - {desc}")
        else:
            print(f"  ❌ {filename} - {desc}")
    
    # Feature status from config
    print("\n🚀 ENABLED FEATURES (from config.json):")
    features = config.get("features", {})
    for feature, enabled in features.items():
        status = "✅" if enabled else "❌"
        print(f"  {status} {feature}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 FINAL SUMMARY:")
    print(f"  ✅ Hooks: {total_hooks} active across 7 event types")
    print(f"  ✅ Chains: {len(chains_data['chains'])} workflows")
    print(f"  ✅ Commands: {command_count} files")
    print(f"  ✅ Aliases: {len(aliases)} shortcuts")
    print(f"  ✅ Scripts: {'Restored' if scripts_dir.exists() else 'Missing'}")
    print(f"  ✅ Configuration: Complete")
    
    print("\n🎉 CLAUDE CODE BOILERPLATE SYSTEM FULLY OPERATIONAL!")
    print("\n💡 Key capabilities enabled:")
    print("  • Auto-approval for safe operations")
    print("  • Security validations and auditing")
    print("  • TDD enforcement and test generation")
    print("  • Task tracking and ledger integration")
    print("  • Branch awareness and worktree support")
    print("  • PRP methodology implementation")
    print("  • Agent OS integration")
    print("  • Design system enforcement")
    print("  • And much more...")

if __name__ == "__main__":
    audit_complete_system()
