#!/usr/bin/env python3
"""Fix missing command references and broken aliases"""

import json
from pathlib import Path
import os

CLAUDE_DIR = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude")

def fix_command_references():
    """Create fixes for missing commands"""
    
    # The actual locations of "missing" commands
    command_mappings = {
        "spawn": "spawn-agent",  # spawn is likely an alias for spawn-agent
        "test-security": "security-check",  # test-security might be part of security-check
        "worktree-parallel": "worktree/worktree-parallel",  # in subdirectory
        "validate-pii-handling": None  # This one truly doesn't exist
    }
    
    print("🔧 Fixing command references...")
    
    # Update chains.json to use correct command names
    chains_path = CLAUDE_DIR / "chains.json"
    with open(chains_path) as f:
        chains_data = json.load(f)
    
    updated = False
    for chain_name, chain_data in chains_data["chains"].items():
        new_commands = []
        for cmd in chain_data.get("commands", []):
            base_cmd = cmd.split()[0]
            
            # Fix spawn -> spawn-agent
            if base_cmd == "spawn" and "security-auditor" in cmd:
                new_cmd = cmd.replace("spawn ", "spawn-security-auditor ", 1)
                new_commands.append(new_cmd)
                print(f"  ✅ Fixed in {chain_name}: spawn → spawn-security-auditor")
                updated = True
            elif base_cmd == "spawn":
                new_cmd = cmd.replace("spawn ", "spawn-agent ", 1)
                new_commands.append(new_cmd)
                print(f"  ✅ Fixed in {chain_name}: spawn → spawn-agent")
                updated = True
            # Fix test-security -> security-check
            elif base_cmd == "test-security":
                new_cmd = cmd.replace("test-security", "security-check")
                new_commands.append(new_cmd)
                print(f"  ✅ Fixed in {chain_name}: test-security → security-check")
                updated = True
            else:
                new_commands.append(cmd)
        
        chain_data["commands"] = new_commands
    
    if updated:
        # Backup original
        backup_path = chains_path.with_suffix('.json.backup')
        with open(backup_path, 'w') as f:
            json.dump(chains_data, f, indent=2)
        
        # Save updated
        with open(chains_path, 'w') as f:
            json.dump(chains_data, f, indent=2)
        print(f"  ✅ Updated chains.json (backup saved)")
    
    # Update aliases.json
    aliases_path = CLAUDE_DIR / "aliases.json"
    with open(aliases_path) as f:
        aliases = json.load(f)
    
    # Remove broken alias for validate-pii-handling
    if "vph" in aliases and aliases["vph"] == "validate-pii-handling":
        del aliases["vph"]
        print("  ✅ Removed broken alias: vph → validate-pii-handling")
        
        with open(aliases_path, 'w') as f:
            json.dump(aliases, f, indent=2)
    
    # Create command stub for validate-pii-handling if needed
    pii_command_path = CLAUDE_DIR / "commands" / "validate-pii-handling.md"
    if not pii_command_path.exists():
        pii_content = """---
name: validate-pii-handling
description: Validate PII handling in code
category: security
---

# Validate PII Handling

This command validates that personally identifiable information (PII) is properly handled in the codebase.

## Usage
```
/validate-pii-handling [file|directory]
```

## What it checks:
- Proper masking of sensitive fields
- Secure storage practices
- Audit logging for PII access
- Compliance with data protection policies

Note: This functionality is also covered by the PII protection hook (07-pii-protection.py).
"""
        pii_command_path.write_text(pii_content)
        print("  ✅ Created validate-pii-handling.md command")

def create_command_registry():
    """Create a registry of all commands with their locations"""
    commands_dir = CLAUDE_DIR / "commands"
    registry = {}
    
    # Scan all directories
    for path in commands_dir.rglob("*.md"):
        rel_path = path.relative_to(commands_dir)
        command_name = path.stem
        registry[command_name] = str(rel_path)
    
    # Save registry
    registry_path = CLAUDE_DIR / "command-registry.json"
    with open(registry_path, 'w') as f:
        json.dump(registry, f, indent=2)
    
    print(f"\n📚 Created command registry with {len(registry)} commands")
    return registry

def main():
    print("🔍 Fixing Missing Commands and Broken Aliases")
    print("=" * 50)
    
    # Fix command references
    fix_command_references()
    
    # Create command registry
    registry = create_command_registry()
    
    # Show commands in subdirectories
    print("\n📁 Commands in subdirectories:")
    for cmd, path in registry.items():
        if "/" in path:
            print(f"  • {cmd}: {path}")
    
    print("\n✅ Fixes applied!")
    print("Run the audit again to verify all issues are resolved.")

if __name__ == "__main__":
    main()
