#!/usr/bin/env python3
"""
Fix the matcher field in hook configuration
Changes "matcher": {} to "matcher": "" based on official docs
"""

import json
from pathlib import Path

def fix_matcher_in_config(config):
    """Fix matcher fields in hook configuration"""
    if "hooks" not in config:
        return config
    
    fixed_count = 0
    
    for event_type, matchers in config["hooks"].items():
        if isinstance(matchers, list):
            for matcher_config in matchers:
                # Check if matcher is an empty object
                if "matcher" in matcher_config and isinstance(matcher_config["matcher"], dict) and not matcher_config["matcher"]:
                    # Change empty object to empty string
                    matcher_config["matcher"] = ""
                    fixed_count += 1
                    print(f"✅ Fixed matcher in {event_type}")
    
    return config, fixed_count

def main():
    """Fix the hook configuration"""
    backup_settings = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude.full_backup_20250727_102756/settings-backup/settings-with-hooks.json")
    
    if not backup_settings.exists():
        print("❌ Backup settings file not found")
        return
    
    # Read the configuration
    config = json.loads(backup_settings.read_text())
    print("📖 Read backup configuration")
    
    # Fix matchers
    fixed_config, count = fix_matcher_in_config(config)
    print(f"\n🔧 Fixed {count} matcher fields")
    
    # Save fixed configuration
    output_path = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude/settings-fixed-matchers.json")
    output_path.write_text(json.dumps(fixed_config, indent=2))
    print(f"\n💾 Saved fixed configuration to: {output_path}")
    
    # Also create a minimal test version
    minimal_config = {
        "permissions": fixed_config["permissions"],
        "hooks": {
            "PreToolUse": [
                {
                    "matcher": "",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python3 .claude/hooks/pre-tool-use/00-auto-approve-safe-ops.py"
                        }
                    ]
                }
            ]
        }
    }
    
    minimal_path = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude/settings-minimal-test.json")
    minimal_path.write_text(json.dumps(minimal_config, indent=2))
    print(f"💾 Saved minimal test to: {minimal_path}")
    
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    print("1. Test the minimal configuration:")
    print("   cp .claude/settings-minimal-test.json .claude/settings.json")
    print("   claude doctor")
    print("\n2. If successful, test the full fixed configuration:")
    print("   cp .claude/settings-fixed-matchers.json .claude/settings.json")
    print("   claude doctor")

if __name__ == "__main__":
    main()
