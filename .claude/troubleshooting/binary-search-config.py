#!/usr/bin/env python3
"""Binary search to find exactly which configuration causes the error"""

import json
import subprocess
import time
import sys

def test_settings(settings_content):
    """Test if given settings cause an error"""
    # Write settings
    with open("/Users/shawnsmith/dev/bfc/boilerplate/.claude/settings.json", "w") as f:
        json.dump(settings_content, f, indent=2)
    
    # Kill any running claude-code
    subprocess.run(["pkill", "-f", "claude-code"], capture_output=True)
    time.sleep(0.5)
    
    # Test
    result = subprocess.run(
        ["claude-code", "--version"],
        cwd="/Users/shawnsmith/dev/bfc/boilerplate",
        capture_output=True,
        text=True,
        timeout=3
    )
    
    has_error = "Cannot assign to read only property" in result.stderr
    return not has_error  # Return True if NO error

# Test configurations
print("Testing different settings configurations...")
print("=" * 50)

configs = [
    ("No hooks", {
        "permissions": {
            "file_system": {"read": True, "write": True},
            "shell": {"execute": True}
        }
    }),
    ("Empty hooks object", {
        "permissions": {
            "file_system": {"read": True, "write": True},
            "shell": {"execute": True}
        },
        "hooks": {}
    }),
    ("Empty preToolUse array", {
        "permissions": {
            "file_system": {"read": True, "write": True},
            "shell": {"execute": True}
        },
        "hooks": {
            "preToolUse": []
        }
    }),
    ("Single echo command", {
        "permissions": {
            "file_system": {"read": True, "write": True},
            "shell": {"execute": True}
        },
        "hooks": {
            "preToolUse": [
                {"command": "echo 'test'"}
            ]
        }
    }),
    ("Single Python hook", {
        "permissions": {
            "file_system": {"read": True, "write": True},
            "shell": {"execute": True}
        },
        "hooks": {
            "preToolUse": [
                {"command": "python3 .claude/hooks/pre-tool-use/00-auto-approve-safe-ops.py"}
            ]
        }
    }),
    ("Two Python hooks", {
        "permissions": {
            "file_system": {"read": True, "write": True},
            "shell": {"execute": True}
        },
        "hooks": {
            "preToolUse": [
                {"command": "python3 .claude/hooks/pre-tool-use/00-auto-approve-safe-ops.py"},
                {"command": "python3 .claude/hooks/pre-tool-use/01-collab-sync.py"}
            ]
        }
    }),
    ("Mixed hook types", {
        "permissions": {
            "file_system": {"read": True, "write": True},
            "shell": {"execute": True}
        },
        "hooks": {
            "preToolUse": [
                {"command": "python3 .claude/hooks/pre-tool-use/00-auto-approve-safe-ops.py"}
            ],
            "postToolUse": [
                {"command": "python3 .claude/hooks/post-tool-use/02-metrics.py"}
            ]
        }
    })
]

working_configs = []
failing_configs = []

for name, config in configs:
    print(f"\nTesting: {name}...", end=" ")
    sys.stdout.flush()
    
    try:
        if test_settings(config):
            print("✅ WORKS")
            working_configs.append(name)
        else:
            print("❌ FAILS")
            failing_configs.append(name)
            # Show the exact config that fails
            print(f"Failed config: {json.dumps(config, indent=2)}")
            break  # Stop at first failure
    except Exception as e:
        print(f"⚠️  ERROR: {e}")
        failing_configs.append(name)

print("\n" + "=" * 50)
print(f"Working: {', '.join(working_configs)}")
print(f"Failing: {', '.join(failing_configs)}")

# Restore a working configuration
if working_configs:
    # Find the last working config
    for name, config in reversed(configs):
        if name in working_configs:
            print(f"\nRestoring last working config: {name}")
            with open("/Users/shawnsmith/dev/bfc/boilerplate/.claude/settings.json", "w") as f:
                json.dump(config, f, indent=2)
            break
