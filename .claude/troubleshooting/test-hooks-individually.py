#!/usr/bin/env python3
"""Test each hook individually to find the problematic one"""

import json
import subprocess
import time

HOOKS_TO_TEST = [
    ("preToolUse", "01-collab-sync.py"),
    ("preToolUse", "04-actually-works.py"),
    ("postToolUse", "02-metrics.py")
]

def test_claude():
    """Quick test if Claude Code starts without error"""
    result = subprocess.run(
        ["claude-code", "--version"],
        cwd="/Users/shawnsmith/dev/bfc/boilerplate",
        capture_output=True,
        text=True
    )
    return "Cannot assign to read only property" not in result.stderr

def test_hook(hook_type, hook_name):
    """Test adding a specific hook"""
    # Load current settings
    with open("/Users/shawnsmith/dev/bfc/boilerplate/.claude/settings.json", "r") as f:
        settings = json.load(f)
    
    # Backup current settings
    with open("/Users/shawnsmith/dev/bfc/boilerplate/.claude/settings-backup.json", "w") as f:
        json.dump(settings, f, indent=2)
    
    # Add the hook
    path = "pre-tool-use" if hook_type == "preToolUse" else "post-tool-use"
    new_hook = {"command": f"python3 .claude/hooks/{path}/{hook_name}"}
    
    if hook_type not in settings["hooks"]:
        settings["hooks"][hook_type] = []
    
    settings["hooks"][hook_type].append(new_hook)
    
    # Save and test
    with open("/Users/shawnsmith/dev/bfc/boilerplate/.claude/settings.json", "w") as f:
        json.dump(settings, f, indent=2)
    
    time.sleep(0.5)
    success = test_claude()
    
    if not success:
        # Restore backup
        with open("/Users/shawnsmith/dev/bfc/boilerplate/.claude/settings-backup.json", "r") as f:
            settings = json.load(f)
        with open("/Users/shawnsmith/dev/bfc/boilerplate/.claude/settings.json", "w") as f:
            json.dump(settings, f, indent=2)
    
    return success

# Test current state
print("Testing current state...")
if test_claude():
    print("✅ Current configuration works")
else:
    print("❌ Current configuration has errors")
    exit(1)

# Test each hook
for hook_type, hook_name in HOOKS_TO_TEST:
    print(f"\nTesting {hook_type}/{hook_name}...", end=" ")
    if test_hook(hook_type, hook_name):
        print("✅ OK")
    else:
        print("❌ CAUSES ERROR")
        print(f"\n🚨 Found problematic hook: {hook_type}/{hook_name}")
        break

print("\nFinal settings.json contains only working hooks.")
