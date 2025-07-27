#!/usr/bin/env python3
"""
Gradually restore hooks to find any problematic ones
"""

import json
import subprocess
import time
import sys
from pathlib import Path

# Define hooks in the order they should be added
HOOK_GROUPS = {
    "Critical PreToolUse": [
        "00-auto-approve-safe-ops.py",
        "00a-snapshot-manager.py",
        "01-collab-sync.py",
        "04-actually-works.py"
    ],
    "Context PreToolUse": [
        "05a-auto-context-inclusion.py",
        "05b-prp-context-loader.py"
    ],
    "Quality PreToolUse": [
        "06a-biome-lint.py",
        "07-pii-protection-simple.py",
        "08-evidence-language.py",
        "08a-async-patterns.py"
    ],
    "Guard PreToolUse": [
        "09-auto-persona.py",
        "10-hydration-guard.py",
        "11-truth-enforcer.py",
        "12-deletion-guard.py",
        "13-import-validator.py"
    ],
    "Advanced PreToolUse": [
        "14a-creation-guard.py",
        "15-implementation-guide.py",
        "15a-dependency-tracker.py",
        "16-tcpa-compliance.py",
        "16a-prp-validator.py",
        "17-ai-docs-check.py"
    ],
    "PostToolUse": [
        "01-track-completion.py",
        "02-metrics.py",
        "03-pattern-learning.py"
    ]
}

def load_current_settings():
    """Load current settings.json"""
    settings_path = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude/settings.json")
    with open(settings_path, 'r') as f:
        return json.load(f)

def save_settings(settings):
    """Save settings.json"""
    settings_path = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude/settings.json")
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)

def test_claude_code():
    """Test if Claude Code starts without errors"""
    try:
        # Kill existing process
        subprocess.run(["pkill", "-f", "claude-code"], capture_output=True)
        time.sleep(1)
        
        # Start claude-code
        process = subprocess.Popen(
            ["claude-code", "--version"],
            cwd="/Users/shawnsmith/dev/bfc/boilerplate",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for output
        stdout, stderr = process.communicate(timeout=3)
        
        # Check for the error
        if "Cannot assign to read only property" in stderr:
            return False, "String assignment error"
        
        return True, "OK"
        
    except subprocess.TimeoutExpired:
        process.kill()
        return True, "OK (no immediate errors)"
    except Exception as e:
        return False, str(e)

def add_hook(hook_type, hook_name):
    """Add a single hook to settings"""
    settings = load_current_settings()
    
    # Initialize hooks if not present
    if "hooks" not in settings:
        settings["hooks"] = {}
    
    # Initialize hook type if not present
    if hook_type not in settings["hooks"]:
        settings["hooks"][hook_type] = []
    
    # Determine path
    if hook_type == "preToolUse":
        path = "pre-tool-use"
    elif hook_type == "postToolUse":
        path = "post-tool-use"
    else:
        path = hook_type.lower()
    
    # Add hook
    hook_command = f"python3 .claude/hooks/{path}/{hook_name}"
    hook_entry = {"command": hook_command}
    
    # Check if already exists
    existing_commands = [h.get("command") for h in settings["hooks"][hook_type]]
    if hook_command not in existing_commands:
        settings["hooks"][hook_type].append(hook_entry)
    
    save_settings(settings)
    return settings

def main():
    print("🔄 Gradually Restoring Hooks")
    print("=" * 60)
    
    # Test current state
    print("\n📊 Testing current configuration...")
    success, msg = test_claude_code()
    if not success:
        print(f"❌ Current configuration has errors: {msg}")
        print("Please fix before proceeding.")
        return
    print("✅ Current configuration is working")
    
    # Process each group
    total_added = 0
    failed_hooks = []
    
    for group_name, hooks in HOOK_GROUPS.items():
        print(f"\n📦 Adding {group_name}...")
        print("-" * 40)
        
        # Determine hook type from group name
        if "PreToolUse" in group_name:
            hook_type = "preToolUse"
        elif "PostToolUse" in group_name:
            hook_type = "postToolUse"
        else:
            continue
        
        for hook in hooks:
            # Check if hook file exists
            if hook_type == "preToolUse":
                hook_path = f"/Users/shawnsmith/dev/bfc/boilerplate/.claude/hooks/pre-tool-use/{hook}"
            else:
                hook_path = f"/Users/shawnsmith/dev/bfc/boilerplate/.claude/hooks/post-tool-use/{hook}"
            
            if not Path(hook_path).exists():
                print(f"  ⚠️  {hook} - File not found, skipping")
                continue
            
            # Add hook
            print(f"  Adding {hook}...", end=" ")
            add_hook(hook_type, hook)
            
            # Test
            success, msg = test_claude_code()
            if success:
                print("✅")
                total_added += 1
            else:
                print(f"❌ {msg}")
                failed_hooks.append((hook_type, hook, msg))
                
                # Remove the problematic hook
                settings = load_current_settings()
                hook_command = f"python3 .claude/hooks/{hook_type.replace('ToolUse', '-tool-use')}/{hook}"
                settings["hooks"][hook_type] = [
                    h for h in settings["hooks"][hook_type] 
                    if h.get("command") != hook_command
                ]
                save_settings(settings)
                print(f"     Removed {hook} from configuration")
        
        # Add a small delay between groups
        time.sleep(1)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print(f"✅ Successfully added: {total_added} hooks")
    print(f"❌ Failed hooks: {len(failed_hooks)}")
    
    if failed_hooks:
        print("\n❌ Problematic hooks:")
        for hook_type, hook, error in failed_hooks:
            print(f"  - {hook_type}/{hook}: {error}")
        
        print("\n💡 Next steps:")
        print("1. Check the failed hook files for syntax errors")
        print("2. Ensure hooks follow the official documentation format")
        print("3. Test each failed hook individually")
    
    # Save a backup of the working configuration
    settings = load_current_settings()
    backup_path = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude/settings-working.json")
    with open(backup_path, 'w') as f:
        json.dump(settings, f, indent=2)
    print(f"\n💾 Saved working configuration to: {backup_path}")

if __name__ == "__main__":
    main()
