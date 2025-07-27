#!/usr/bin/env python3
"""Simple script to fix the matcher format in the hooks configuration"""

import json
from pathlib import Path

BACKUP_CONFIG = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude.full_backup_20250727_102756/settings-backup/settings-with-hooks.json")
OUTPUT_CONFIG = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude/settings-fixed.json")

def main():
    print("🔧 Fixing Claude Code hooks configuration...")
    
    # Load the broken config
    with open(BACKUP_CONFIG) as f:
        config = json.load(f)
    
    # Fix all empty object matchers to empty strings
    if "hooks" in config:
        for event_type, matchers in config["hooks"].items():
            for matcher_config in matchers:
                # Change empty object {} to empty string ""
                if isinstance(matcher_config.get("matcher"), dict) and not matcher_config["matcher"]:
                    matcher_config["matcher"] = ""
                    print(f"✅ Fixed matcher in {event_type}")
    
    # Save the fixed config
    with open(OUTPUT_CONFIG, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Fixed configuration saved to: {OUTPUT_CONFIG}")
    print("\nTo test it:")
    print(f"1. cp {OUTPUT_CONFIG} .claude/settings.json")
    print("2. claude doctor")
    print("\nIf it works, your 70+ hooks should all be functional again!")

if __name__ == "__main__":
    main()
