#!/usr/bin/env python3
"""
Migrate Claude Code hooks from complex nested format to simple format
Based on official Claude Code documentation
"""

import json
from pathlib import Path

CLAUDE_DIR = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude")
BACKUP_DIR = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude.full_backup_20250727_102756")

def migrate_hooks():
    """Migrate hooks to correct format"""
    
    # Read the hooks configuration from backup
    hooks_config_path = BACKUP_DIR / "hooks/config.json"
    if not hooks_config_path.exists():
        print("❌ hooks/config.json not found in backup")
        return
    
    hooks_config = json.loads(hooks_config_path.read_text())
    
    # Create new settings with correct format
    new_settings = {
        "permissions": {
            "file_system": {
                "read": True,
                "write": True
            },
            "shell": {
                "execute": True
            }
        },
        "hooks": {}
    }
    
    # Map old directory names to new event names (lowercase camelCase)
    event_map = {
        "pre-tool-use": "preToolUse",
        "post-tool-use": "postToolUse",
        "notification": "notification",
        "pre-compact": "preCompact",
        "stop": "stop",
        "sub-agent-stop": "subagentStop", 
        "user-prompt-submit": "userPromptSubmit"
    }
    
    # Statistics
    total_hooks = 0
    enabled_hooks = 0
    
    # Convert hooks to correct format
    for event_dir, event_name in event_map.items():
        if event_dir in hooks_config["hooks"]:
            hooks = hooks_config["hooks"][event_dir]
            new_settings["hooks"][event_name] = []
            
            for hook in hooks:
                total_hooks += 1
                if hook.get("enabled", True):
                    enabled_hooks += 1
                    script = hook["script"]
                    path = f".claude/hooks/{event_dir}/{script}"
                    
                    # Simple format: just command string
                    new_settings["hooks"][event_name].append({
                        "command": f"python3 {path}"
                    })
                    
                    print(f"✅ Added {event_name}/{script}")
    
    # Save multiple versions for testing
    
    # 1. Full migration
    full_path = CLAUDE_DIR / "settings-migrated-full.json"
    full_path.write_text(json.dumps(new_settings, indent=2))
    print(f"\n📝 Full migration saved to: {full_path}")
    print(f"   Total hooks: {total_hooks}, Enabled: {enabled_hooks}")
    
    # 2. Minimal test (just one hook)
    minimal_settings = {
        "permissions": new_settings["permissions"].copy(),
        "hooks": {
            "preToolUse": [
                {
                    "command": "python3 .claude/hooks/pre-tool-use/00-auto-approve-safe-ops.py"
                }
            ]
        }
    }
    minimal_path = CLAUDE_DIR / "settings-migrated-minimal.json"
    minimal_path.write_text(json.dumps(minimal_settings, indent=2))
    print(f"\n📝 Minimal test saved to: {minimal_path}")
    
    # 3. Gradual migration (first 5 hooks of each type)
    gradual_settings = {
        "permissions": new_settings["permissions"].copy(),
        "hooks": {}
    }
    for event_name, hooks in new_settings["hooks"].items():
        if hooks:
            gradual_settings["hooks"][event_name] = hooks[:5]
    
    gradual_path = CLAUDE_DIR / "settings-migrated-gradual.json"
    gradual_path.write_text(json.dumps(gradual_settings, indent=2))
    print(f"\n📝 Gradual migration saved to: {gradual_path}")
    
    # Show next steps
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    print("1. Test minimal configuration:")
    print("   cp .claude/settings-migrated-minimal.json .claude/settings.json")
    print("   claude doctor")
    print("\n2. If successful, test gradual:")
    print("   cp .claude/settings-migrated-gradual.json .claude/settings.json")
    print("   claude doctor")
    print("\n3. If all good, use full migration:")
    print("   cp .claude/settings-migrated-full.json .claude/settings.json")
    print("   claude doctor")
    print("\n4. Always keep backup:")
    print("   cp .claude/settings-safe-backup.json .claude/settings-recovery.json")

if __name__ == "__main__":
    migrate_hooks()
