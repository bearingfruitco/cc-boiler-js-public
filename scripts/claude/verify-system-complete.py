#!/usr/bin/env python3
"""Comprehensive verification of Claude Code hooks and chains"""

import json
import os
from pathlib import Path

CLAUDE_DIR = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude")

def verify_hooks():
    """Verify hooks are active"""
    settings_path = CLAUDE_DIR / "settings.json"
    if not settings_path.exists():
        return False, "No settings.json found"
    
    with open(settings_path) as f:
        config = json.load(f)
    
    if "hooks" not in config:
        return False, "No hooks section in settings"
    
    hook_counts = {}
    total = 0
    
    for event_type, matchers in config["hooks"].items():
        count = 0
        for matcher_config in matchers:
            hooks = matcher_config.get("hooks", [])
            count += len(hooks)
        hook_counts[event_type] = count
        total += count
    
    return True, {"counts": hook_counts, "total": total}

def verify_chains():
    """Verify chains are available"""
    chains_path = CLAUDE_DIR / "chains.json"
    if not chains_path.exists():
        return False, "No chains.json found"
    
    with open(chains_path) as f:
        data = json.load(f)
    
    chains = data.get("chains", {})
    return True, {"count": len(chains), "names": list(chains.keys())[:5]}

def verify_commands():
    """Verify custom commands exist"""
    commands_dir = CLAUDE_DIR / "commands"
    if not commands_dir.exists():
        return False, "No commands directory"
    
    py_files = list(commands_dir.glob("*.py"))
    js_files = list(commands_dir.glob("*.js"))
    sh_files = list(commands_dir.glob("*.sh"))
    
    return True, {
        "python": len(py_files),
        "javascript": len(js_files),
        "shell": len(sh_files),
        "total": len(py_files) + len(js_files) + len(sh_files)
    }

def main():
    print("🔍 Claude Code System Verification")
    print("=" * 60)
    
    # Verify hooks
    print("\n📌 HOOKS STATUS:")
    hooks_ok, hooks_data = verify_hooks()
    if hooks_ok:
        print("✅ Hooks are configured and active!")
        for event_type, count in hooks_data["counts"].items():
            print(f"   • {event_type}: {count} hooks")
        print(f"   🎯 Total: {hooks_data['total']} hooks")
    else:
        print(f"❌ Hooks issue: {hooks_data}")
    
    # Verify chains
    print("\n⛓️  CHAINS STATUS:")
    chains_ok, chains_data = verify_chains()
    if chains_ok:
        print(f"✅ Chains are available: {chains_data['count']} chains")
        print(f"   First 5: {', '.join(chains_data['names'])}")
    else:
        print(f"❌ Chains issue: {chains_data}")
    
    # Verify commands
    print("\n🛠️  COMMANDS STATUS:")
    commands_ok, commands_data = verify_commands()
    if commands_ok:
        print(f"✅ Commands available: {commands_data['total']} total")
        print(f"   • Python: {commands_data['python']}")
        print(f"   • JavaScript: {commands_data['javascript']}")
        print(f"   • Shell: {commands_data['shell']}")
    else:
        print(f"❌ Commands issue: {commands_data}")
    
    # Summary
    print("\n" + "=" * 60)
    if hooks_ok and chains_ok and commands_ok:
        print("🎉 SYSTEM FULLY OPERATIONAL!")
        print("\n💡 To test hooks in action:")
        print("1. Start Claude Code: claude")
        print("2. Press Ctrl+R for transcript mode")
        print("3. Try: 'read README.md' or 'list files'")
        print("\n⛓️  To use chains:")
        print("Type /chain followed by chain name, e.g.:")
        print("  /chain morning-setup")
        print("  /chain pre-pr")
    else:
        print("⚠️  Some components need attention")

if __name__ == "__main__":
    main()
