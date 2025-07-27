#!/usr/bin/env python3
"""Complete system audit including orphaned references"""

import json
from pathlib import Path

CLAUDE_DIR = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude")

def audit_system():
    """Complete audit of hooks, chains, commands, and aliases"""
    
    # Load configurations
    with open(CLAUDE_DIR / "settings.json") as f:
        settings = json.load(f)
    
    with open(CLAUDE_DIR / "chains.json") as f:
        chains_data = json.load(f)
    
    with open(CLAUDE_DIR / "aliases.json") as f:
        aliases = json.load(f)
    
    print("🔍 CLAUDE CODE SYSTEM AUDIT")
    print("=" * 60)
    
    # Count hooks
    print("\n📌 HOOKS AUDIT:")
    total_hooks = 0
    for event_type, matchers in settings.get("hooks", {}).items():
        count = sum(len(m.get("hooks", [])) for m in matchers)
        total_hooks += count
        print(f"  • {event_type}: {count} hooks")
    print(f"  🎯 Total: {total_hooks} hooks active")
    
    # Check hook files exist
    print("\n🔍 Verifying hook files exist...")
    missing_hooks = []
    for event_type, matchers in settings.get("hooks", {}).items():
        for matcher in matchers:
            for hook in matcher.get("hooks", []):
                cmd = hook.get("command", "")
                if cmd.startswith("python3 "):
                    hook_path = Path(cmd.replace("python3 ", "").strip())
                    if not (Path("/Users/shawnsmith/dev/bfc/boilerplate") / hook_path).exists():
                        missing_hooks.append(hook_path)
    
    if missing_hooks:
        print(f"  ❌ Missing hook files: {len(missing_hooks)}")
        for h in missing_hooks[:5]:
            print(f"    - {h}")
    else:
        print("  ✅ All hook files exist!")
    
    # Audit chains
    print("\n⛓️  CHAINS AUDIT:")
    chains = chains_data.get("chains", {})
    print(f"  • Total chains: {len(chains)}")
    
    # Check commands in chains
    commands_dir = CLAUDE_DIR / "commands"
    all_chain_commands = set()
    for chain_name, chain_data in chains.items():
        for cmd in chain_data.get("commands", []):
            # Extract base command (remove arguments)
            base_cmd = cmd.split()[0]
            all_chain_commands.add(base_cmd)
    
    print(f"  • Unique commands referenced: {len(all_chain_commands)}")
    
    # Check which commands exist
    missing_commands = []
    for cmd in all_chain_commands:
        found = False
        # Check various extensions
        for ext in ['.md', '.py', '.js', '.sh', '']:
            if (commands_dir / f"{cmd}{ext}").exists():
                found = True
                break
        # Check if it's a special command
        if not found and cmd in ['test', 'lint:fix', 'bash']:
            found = True  # Built-in or special commands
        if not found:
            missing_commands.append(cmd)
    
    if missing_commands:
        print(f"  ⚠️  Commands not found: {len(missing_commands)}")
        for cmd in sorted(missing_commands)[:10]:
            print(f"    - {cmd}")
    else:
        print("  ✅ All chain commands found!")
    
    # Audit aliases
    print("\n🔗 ALIASES AUDIT:")
    print(f"  • Total aliases: {len(aliases)}")
    
    # Check alias targets
    missing_alias_targets = []
    for alias, target in aliases.items():
        # Extract base command from target
        base_target = target.split()[0]
        if base_target.startswith("chain"):
            continue  # Chain commands are special
        
        found = False
        for ext in ['.md', '.py', '.js', '.sh', '']:
            if (commands_dir / f"{base_target}{ext}").exists():
                found = True
                break
        if not found and base_target not in ['bash']:
            missing_alias_targets.append((alias, target))
    
    if missing_alias_targets:
        print(f"  ⚠️  Aliases with missing targets: {len(missing_alias_targets)}")
        for alias, target in missing_alias_targets[:5]:
            print(f"    - {alias} → {target}")
    else:
        print("  ✅ All alias targets exist!")
    
    # Command inventory
    print("\n🛠️  COMMANDS INVENTORY:")
    command_files = list(commands_dir.glob("*.md")) + \
                   list(commands_dir.glob("*.py")) + \
                   list(commands_dir.glob("*.js")) + \
                   list(commands_dir.glob("*.sh"))
    
    print(f"  • Total command files: {len(command_files)}")
    print(f"  • By type:")
    print(f"    - Markdown (.md): {len(list(commands_dir.glob('*.md')))}")
    print(f"    - Python (.py): {len(list(commands_dir.glob('*.py')))}")
    print(f"    - JavaScript (.js): {len(list(commands_dir.glob('*.js')))}")
    print(f"    - Shell (.sh): {len(list(commands_dir.glob('*.sh')))}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SYSTEM SUMMARY:")
    print(f"  ✅ Hooks: {total_hooks} active")
    print(f"  ✅ Chains: {len(chains)} workflows")
    print(f"  ✅ Commands: {len(command_files)} files")
    print(f"  ✅ Aliases: {len(aliases)} shortcuts")
    
    if missing_hooks or missing_commands or missing_alias_targets:
        print("\n⚠️  ISSUES FOUND:")
        if missing_hooks:
            print(f"  - {len(missing_hooks)} missing hook files")
        if missing_commands:
            print(f"  - {len(missing_commands)} missing chain commands")
        if missing_alias_targets:
            print(f"  - {len(missing_alias_targets)} broken aliases")
    else:
        print("\n🎉 SYSTEM FULLY OPERATIONAL - NO ORPHANED REFERENCES!")

if __name__ == "__main__":
    audit_system()
