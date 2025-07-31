#!/usr/bin/env python3
"""Verify that all hooks are loaded and count them"""

import json
from pathlib import Path

SETTINGS_PATH = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude/settings.json")

def count_hooks():
    """Count all hooks in the current settings"""
    with open(SETTINGS_PATH) as f:
        config = json.load(f)
    
    hook_counts = {}
    total = 0
    
    if "hooks" in config:
        for event_type, matchers in config["hooks"].items():
            count = 0
            for matcher_config in matchers:
                count += len(matcher_config.get("hooks", []))
            hook_counts[event_type] = count
            total += count
    
    return hook_counts, total

def list_hooks():
    """List all hooks with their names"""
    with open(SETTINGS_PATH) as f:
        config = json.load(f)
    
    print("🪝 ACTIVE HOOKS IN CLAUDE CODE")
    print("=" * 50)
    
    if "hooks" not in config:
        print("❌ No hooks found in settings!")
        return
    
    for event_type, matchers in config["hooks"].items():
        print(f"\n📁 {event_type}:")
        for matcher_config in matchers:
            matcher = matcher_config.get("matcher", "")
            matcher_display = '(all tools)' if matcher == "" else f'({matcher})'
            
            hooks = matcher_config.get("hooks", [])
            for hook in hooks:
                cmd = hook.get("command", "")
                hook_name = Path(cmd).name if cmd else "unknown"
                print(f"   ✓ {hook_name} {matcher_display}")

def main():
    """Main verification"""
    print("🔍 Claude Code Hooks Verification")
    print("=" * 50)
    
    # Count hooks
    hook_counts, total = count_hooks()
    
    print("\n📊 HOOK SUMMARY:")
    for event_type, count in hook_counts.items():
        print(f"  • {event_type}: {count} hooks")
    
    print(f"\n🎯 TOTAL: {total} hooks active")
    
    if total > 0:
        print("\n✅ Hooks are loaded and configured!")
        print("\n💡 To see hooks in action:")
        print("  1. Press Ctrl+R to enter transcript mode")
        print("  2. Ask Claude to read a file or run a command")
        print("  3. Watch the hooks execute in the transcript")
        
        # List all hooks
        print("\n" + "=" * 50)
        list_hooks()
    else:
        print("\n❌ No hooks found! Check your settings.json")

if __name__ == "__main__":
    main()
