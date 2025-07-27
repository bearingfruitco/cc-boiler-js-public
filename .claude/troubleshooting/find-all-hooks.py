#!/usr/bin/env python3
"""Find all unique hooks and create a complete configuration"""

import json
from pathlib import Path
import re

CLAUDE_DIR = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude")
HOOKS_DIR = CLAUDE_DIR / "hooks"

def find_all_hooks():
    """Find all unique hook files (excluding backups)"""
    hook_map = {
        "PreToolUse": [],
        "PostToolUse": [],
        "Stop": [],
        "SubagentStop": [],
        "Notification": [],
        "PreCompact": [],
        "UserPromptSubmit": []
    }
    
    # Map directory names to event types
    dir_mapping = {
        "pre-tool-use": "PreToolUse",
        "post-tool-use": "PostToolUse",
        "stop": "Stop",
        "sub-agent-stop": "SubagentStop",
        "notification": "Notification",
        "pre-compact": "PreCompact",
        "user-prompt-submit": "UserPromptSubmit"
    }
    
    for dir_name, event_type in dir_mapping.items():
        hook_dir = HOOKS_DIR / dir_name
        if not hook_dir.exists():
            continue
            
        # Find all .py files that aren't backups
        py_files = []
        for f in hook_dir.iterdir():
            if f.suffix == '.py' and not any(x in f.name for x in ['.original', '.old', '.broken', '.prefixbatch', '-simple']):
                # Skip duplicates like 07-pii-protection-simple.py if 07-pii-protection.py exists
                if '-simple.py' in f.name:
                    base_name = f.name.replace('-simple.py', '.py')
                    if (hook_dir / base_name).exists():
                        continue
                py_files.append(f)
        
        # Sort by number prefix
        py_files.sort(key=lambda x: (
            int(re.match(r'^(\d+)', x.name).group(1)) if re.match(r'^(\d+)', x.name) else 999,
            x.name
        ))
        
        for py_file in py_files:
            hook_map[event_type].append(f"python3 .claude/hooks/{dir_name}/{py_file.name}")
    
    return hook_map

def create_complete_config():
    """Create a configuration with ALL hooks"""
    # Load current settings for permissions
    with open(CLAUDE_DIR / "settings.json") as f:
        current = json.load(f)
    
    # Find all hooks
    all_hooks = find_all_hooks()
    
    # Build new config
    config = {
        "permissions": current.get("permissions", {
            "file_system": {"read": True, "write": True},
            "shell": {"execute": True}
        }),
        "hooks": {}
    }
    
    # Add hooks to config
    total_count = 0
    for event_type, hook_commands in all_hooks.items():
        if hook_commands:
            config["hooks"][event_type] = [{
                "matcher": "",
                "hooks": [{"type": "command", "command": cmd} for cmd in hook_commands]
            }]
            total_count += len(hook_commands)
    
    return config, all_hooks, total_count

def main():
    print("🔍 Finding ALL hooks in your system...")
    print("=" * 60)
    
    config, hooks_by_type, total = create_complete_config()
    
    print("\n📊 COMPLETE HOOK INVENTORY:")
    for event_type, hooks in hooks_by_type.items():
        if hooks:
            print(f"\n{event_type}: {len(hooks)} hooks")
            for hook in hooks[:5]:  # Show first 5
                hook_name = Path(hook).name
                print(f"  • {hook_name}")
            if len(hooks) > 5:
                print(f"  ... and {len(hooks) - 5} more")
    
    print(f"\n🎯 TOTAL UNIQUE HOOKS FOUND: {total}")
    
    # Compare with current
    with open(CLAUDE_DIR / "settings.json") as f:
        current = json.load(f)
    
    current_count = 0
    if "hooks" in current:
        for event_type, matchers in current["hooks"].items():
            for matcher in matchers:
                current_count += len(matcher.get("hooks", []))
    
    print(f"\n📈 Currently active: {current_count} hooks")
    print(f"📈 Available to enable: {total} hooks")
    print(f"📈 Missing: {total - current_count} hooks")
    
    # Save complete config
    output_path = CLAUDE_DIR / "settings-all-hooks-complete.json"
    with open(output_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Complete configuration saved to: {output_path}")
    print(f"   This config has ALL {total} hooks enabled!")
    
    print("\n🚀 To enable ALL hooks:")
    print(f"   cp {output_path} .claude/settings.json")
    print("   claude doctor")

if __name__ == "__main__":
    main()
