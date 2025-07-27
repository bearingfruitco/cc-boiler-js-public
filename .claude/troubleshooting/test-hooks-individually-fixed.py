#!/usr/bin/env python3
"""Test hooks one by one to identify any problematic ones"""

import json
import subprocess
import time
from pathlib import Path

CLAUDE_DIR = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude")
FIXED_CONFIG = CLAUDE_DIR / "settings-fixed.json"

def load_fixed_config():
    with open(FIXED_CONFIG) as f:
        return json.load(f)

def test_individual_hooks():
    """Test each hook individually to find problematic ones"""
    config = load_fixed_config()
    base_config = {
        "permissions": config["permissions"]
    }
    
    failed_hooks = []
    passed_hooks = []
    
    for event_type, matchers in config.get("hooks", {}).items():
        print(f"\n🔍 Testing {event_type} hooks...")
        
        for matcher_config in matchers:
            hooks = matcher_config.get("hooks", [])
            
            for hook in hooks:
                cmd = hook["command"]
                hook_name = Path(cmd).name
                
                # Create test config with just this hook
                test_config = base_config.copy()
                test_config["hooks"] = {
                    event_type: [{
                        "matcher": "",
                        "hooks": [hook]
                    }]
                }
                
                # Save and test
                settings_path = CLAUDE_DIR / "settings.json"
                settings_path.write_text(json.dumps(test_config, indent=2))
                
                print(f"  Testing: {hook_name}... ", end="", flush=True)
                
                result = subprocess.run(["claude", "doctor"], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=10)
                
                if result.returncode == 0 and "Found invalid settings files" not in result.stdout:
                    print("✅")
                    passed_hooks.append((event_type, cmd))
                else:
                    print("❌")
                    failed_hooks.append((event_type, cmd, result.stdout, result.stderr))
                
                time.sleep(0.5)  # Small delay between tests
    
    # Report results
    print("\n📊 Test Results:")
    print(f"✅ Passed: {len(passed_hooks)} hooks")
    print(f"❌ Failed: {len(failed_hooks)} hooks")
    
    if failed_hooks:
        print("\n❌ Failed hooks:")
        for event_type, cmd, stdout, stderr in failed_hooks:
            print(f"  - {event_type}: {Path(cmd).name}")
            if stderr:
                print(f"    Error: {stderr[:100]}...")
    
    # Create config with only working hooks
    if passed_hooks:
        working_config = base_config.copy()
        working_config["hooks"] = {}
        
        # Group by event type
        for event_type, cmd in passed_hooks:
            if event_type not in working_config["hooks"]:
                working_config["hooks"][event_type] = [{
                    "matcher": "",
                    "hooks": []
                }]
            
            working_config["hooks"][event_type][0]["hooks"].append({
                "type": "command",
                "command": cmd
            })
        
        # Save working config
        working_path = CLAUDE_DIR / "settings-only-working-hooks.json"
        with open(working_path, 'w') as f:
            json.dump(working_config, f, indent=2)
        
        print(f"\n✅ Created config with only working hooks: {working_path}")
        print("To use it: cp .claude/settings-only-working-hooks.json .claude/settings.json")

if __name__ == "__main__":
    test_individual_hooks()
