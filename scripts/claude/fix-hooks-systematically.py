#!/usr/bin/env python3
"""Fix Claude Code hooks by changing matcher from empty object to empty string"""

import json
import os
import sys
from pathlib import Path
import subprocess
import time

CLAUDE_DIR = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude")
BACKUP_DIR = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude.full_backup_20250727_102756")

# Base configuration
BASE_CONFIG = {
    "permissions": {
        "file_system": {"read": True, "write": True},
        "shell": {"execute": True}
    }
}

def load_broken_config():
    """Load the broken configuration with empty object matchers"""
    broken_path = BACKUP_DIR / "settings-backup" / "settings-with-hooks.json"
    with open(broken_path) as f:
        return json.load(f)

def fix_matchers_in_config(config):
    """Fix all empty object matchers to empty strings"""
    fixed_config = config.copy()
    
    if "hooks" in fixed_config:
        for event_type, matchers in fixed_config["hooks"].items():
            for matcher_config in matchers:
                # Change empty object to empty string
                if isinstance(matcher_config.get("matcher"), dict) and not matcher_config["matcher"]:
                    matcher_config["matcher"] = ""
    
    return fixed_config

def test_single_hook(event_type, hook_cmd):
    """Test a single hook with correct format"""
    config = {
        **BASE_CONFIG,
        "hooks": {
            event_type: [
                {
                    "matcher": "",  # Empty string to match all tools
                    "hooks": [
                        {
                            "type": "command",
                            "command": hook_cmd
                        }
                    ]
                }
            ]
        }
    }
    
    settings_path = CLAUDE_DIR / "settings.json"
    settings_path.write_text(json.dumps(config, indent=2))
    
    print(f"\n✅ Testing {event_type} hook: {Path(hook_cmd).name}")
    print("Running 'claude doctor' to verify...")
    
    result = subprocess.run(["claude", "doctor"], capture_output=True, text=True)
    
    if result.returncode == 0 and "Found invalid settings files" not in result.stdout:
        print("✅ Hook is valid!")
        return True
    else:
        print(f"❌ Hook failed validation")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        return False

def test_hook_batch(event_type, hook_cmds):
    """Test a batch of hooks together"""
    hooks_list = [{"type": "command", "command": cmd} for cmd in hook_cmds]
    
    config = {
        **BASE_CONFIG,
        "hooks": {
            event_type: [
                {
                    "matcher": "",  # Empty string to match all tools
                    "hooks": hooks_list
                }
            ]
        }
    }
    
    settings_path = CLAUDE_DIR / "settings.json"
    settings_path.write_text(json.dumps(config, indent=2))
    
    print(f"\n✅ Testing {len(hook_cmds)} {event_type} hooks together...")
    print("Running 'claude doctor' to verify...")
    
    result = subprocess.run(["claude", "doctor"], capture_output=True, text=True)
    
    if result.returncode == 0 and "Found invalid settings files" not in result.stdout:
        print(f"✅ All {len(hook_cmds)} hooks are valid!")
        return True
    else:
        print(f"❌ Batch failed validation")
        return False

def main():
    print("🔧 Claude Code Hook Fixer")
    print("=" * 50)
    
    # Step 1: Load and fix the broken config
    print("\n1️⃣ Loading broken configuration...")
    broken_config = load_broken_config()
    
    print("\n2️⃣ Fixing empty object matchers to empty strings...")
    fixed_config = fix_matchers_in_config(broken_config)
    
    # Save the fixed complete config
    fixed_path = CLAUDE_DIR / "settings-all-hooks-fixed.json"
    with open(fixed_path, 'w') as f:
        json.dump(fixed_config, f, indent=2)
    print(f"✅ Saved fixed configuration to: {fixed_path}")
    
    # Step 3: Test hooks incrementally
    print("\n3️⃣ Testing hooks one by one...")
    
    working_hooks = {
        "PreToolUse": [],
        "PostToolUse": [],
        "Stop": [],
        "SubagentStop": []
    }
    
    # Test each event type's hooks
    for event_type, matchers in fixed_config.get("hooks", {}).items():
        print(f"\n--- Testing {event_type} hooks ---")
        
        for matcher_config in matchers:
            hooks = matcher_config.get("hooks", [])
            
            # Test each hook individually first
            for hook in hooks:
                cmd = hook["command"]
                if test_single_hook(event_type, cmd):
                    working_hooks[event_type].append(cmd)
                    time.sleep(1)  # Small delay between tests
    
    # Step 4: Test all working hooks together
    print("\n4️⃣ Testing all working hooks together...")
    
    final_config = BASE_CONFIG.copy()
    final_config["hooks"] = {}
    
    for event_type, hook_cmds in working_hooks.items():
        if hook_cmds:
            print(f"\nAdding {len(hook_cmds)} {event_type} hooks...")
            final_config["hooks"][event_type] = [
                {
                    "matcher": "",
                    "hooks": [{"type": "command", "command": cmd} for cmd in hook_cmds]
                }
            ]
    
    # Save and test final config
    final_path = CLAUDE_DIR / "settings-all-working-hooks.json"
    with open(final_path, 'w') as f:
        json.dump(final_config, f, indent=2)
    
    settings_path = CLAUDE_DIR / "settings.json"
    settings_path.write_text(json.dumps(final_config, indent=2))
    
    print(f"\n✅ Testing final configuration with all working hooks...")
    result = subprocess.run(["claude", "doctor"], capture_output=True, text=True)
    
    if result.returncode == 0 and "Found invalid settings files" not in result.stdout:
        print("\n🎉 SUCCESS! All hooks are now working!")
        print(f"✅ Final configuration saved to: {final_path}")
        print(f"✅ Active in: {settings_path}")
        
        # Summary
        print("\n📊 Summary:")
        for event_type, hooks in working_hooks.items():
            print(f"  - {event_type}: {len(hooks)} hooks")
    else:
        print("\n❌ Final configuration still has issues")
        print("Try enabling hooks in smaller batches")

if __name__ == "__main__":
    main()
