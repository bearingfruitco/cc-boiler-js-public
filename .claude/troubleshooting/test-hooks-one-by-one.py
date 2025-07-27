#!/usr/bin/env python3
"""
Test hooks one by one with the correct format from official documentation
"""

import json
import subprocess
import time
from pathlib import Path

CLAUDE_DIR = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude")
BACKUP_DIR = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude.full_backup_20250727_102756")

# Base configuration
BASE_CONFIG = {
    "permissions": {
        "file_system": {"read": True, "write": True},
        "shell": {"execute": True}
    }
}

def run_claude_doctor():
    """Run claude doctor and check for errors"""
    try:
        result = subprocess.run(
            ["claude", "doctor"],
            cwd=CLAUDE_DIR.parent,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if "Cannot assign to read only property" in result.stderr:
            return False, "Read-only property error"
        elif "Found invalid settings files" in result.stderr:
            return False, "Invalid settings"
        elif result.returncode != 0:
            return False, f"Exit code {result.returncode}"
        else:
            return True, "Success"
    except Exception as e:
        return False, str(e)

def test_hook(event_type, hook_file, description):
    """Test a single hook"""
    print(f"\n{'='*60}")
    print(f"Testing: {hook_file}")
    print(f"Description: {description}")
    print(f"{'='*60}")
    
    # Create configuration with single hook
    config = {
        **BASE_CONFIG,
        "hooks": {
            event_type: [
                {
                    "matcher": "",  # Empty string to match all tools
                    "hooks": [
                        {
                            "type": "command",
                            "command": f"python3 .claude/hooks/{event_type.lower().replace('tooluse', '-tool-use')}/{hook_file}"
                        }
                    ]
                }
            ]
        }
    }
    
    # Save configuration
    settings_path = CLAUDE_DIR / "settings.json"
    settings_path.write_text(json.dumps(config, indent=2))
    
    # Test with claude doctor
    success, message = run_claude_doctor()
    
    if success:
        print(f"✅ SUCCESS: {message}")
        return True
    else:
        print(f"❌ FAILED: {message}")
        return False

def main():
    """Test hooks one by one"""
    # Read hooks configuration from backup
    hooks_config_path = BACKUP_DIR / "hooks/config.json"
    if not hooks_config_path.exists():
        print("❌ hooks/config.json not found")
        return
    
    hooks_config = json.loads(hooks_config_path.read_text())
    
    # Save current settings as backup
    settings_path = CLAUDE_DIR / "settings.json"
    if settings_path.exists():
        backup_path = CLAUDE_DIR / "settings-before-testing.json"
        backup_path.write_text(settings_path.read_text())
        print(f"💾 Backed up current settings to {backup_path}")
    
    # Map directory names to event types
    event_map = {
        "pre-tool-use": "PreToolUse",
        "post-tool-use": "PostToolUse",
        "notification": "Notification",
        "pre-compact": "PreCompact",
        "stop": "Stop",
        "sub-agent-stop": "SubagentStop",
        "user-prompt-submit": "UserPromptSubmit"
    }
    
    # Test each hook
    successful_hooks = []
    failed_hooks = []
    
    for dir_name, event_type in event_map.items():
        if dir_name in hooks_config["hooks"]:
            print(f"\n🔍 Testing {event_type} hooks...")
            
            for hook_info in hooks_config["hooks"][dir_name]:
                if hook_info.get("enabled", True):
                    hook_file = hook_info["script"]
                    description = hook_info.get("description", "No description")
                    
                    success = test_hook(event_type, hook_file, description)
                    
                    if success:
                        successful_hooks.append(f"{event_type}/{hook_file}")
                    else:
                        failed_hooks.append(f"{event_type}/{hook_file}")
                    
                    # Ask to continue
                    response = input("\nPress Enter to test next hook, or 'q' to quit: ")
                    if response.lower() == 'q':
                        break
    
    # Summary
    print("\n" + "="*60)
    print("TESTING SUMMARY")
    print("="*60)
    print(f"✅ Successful: {len(successful_hooks)}")
    print(f"❌ Failed: {len(failed_hooks)}")
    
    if failed_hooks:
        print("\nFailed hooks:")
        for hook in failed_hooks[:10]:  # Show first 10
            print(f"  - {hook}")
    
    # Restore original settings
    if (CLAUDE_DIR / "settings-before-testing.json").exists():
        settings_path.write_text((CLAUDE_DIR / "settings-before-testing.json").read_text())
        print("\n✅ Restored original settings")

if __name__ == "__main__":
    main()
