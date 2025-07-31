#!/usr/bin/env python3
"""
Systematically test different hook configurations to find the working format
"""

import json
import os
import subprocess
import time
from pathlib import Path

CLAUDE_DIR = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude")
SETTINGS_FILE = CLAUDE_DIR / "settings.json"
BACKUP_FILE = CLAUDE_DIR / "settings-safe-backup.json"

# Base configuration without hooks
BASE_CONFIG = {
    "permissions": {
        "file_system": {
            "read": True,
            "write": True
        },
        "shell": {
            "execute": True
        }
    }
}

# Different hook configurations to test
TEST_CONFIGS = [
    {
        "name": "Empty hooks object",
        "config": {
            **BASE_CONFIG,
            "hooks": {}
        }
    },
    {
        "name": "Single hook - lowercase preToolUse",
        "config": {
            **BASE_CONFIG,
            "hooks": {
                "preToolUse": [
                    {
                        "command": "python3 .claude/hooks/pre-tool-use/00-auto-approve-safe-ops.py"
                    }
                ]
            }
        }
    },
    {
        "name": "Single hook - uppercase PreToolUse",
        "config": {
            **BASE_CONFIG,
            "hooks": {
                "PreToolUse": [
                    {
                        "command": "python3 .claude/hooks/pre-tool-use/00-auto-approve-safe-ops.py"
                    }
                ]
            }
        }
    },
    {
        "name": "Single hook with matcher",
        "config": {
            **BASE_CONFIG,
            "hooks": {
                "preToolUse": [
                    {
                        "matcher": "",
                        "command": "python3 .claude/hooks/pre-tool-use/00-auto-approve-safe-ops.py"
                    }
                ]
            }
        }
    },
    {
        "name": "Multiple hooks - simple format",
        "config": {
            **BASE_CONFIG,
            "hooks": {
                "preToolUse": [
                    {
                        "command": "python3 .claude/hooks/pre-tool-use/00-auto-approve-safe-ops.py"
                    },
                    {
                        "command": "python3 .claude/hooks/pre-tool-use/02-design-check.py"
                    }
                ]
            }
        }
    },
    {
        "name": "Hook as string instead of object",
        "config": {
            **BASE_CONFIG,
            "hooks": {
                "preToolUse": [
                    "python3 .claude/hooks/pre-tool-use/00-auto-approve-safe-ops.py"
                ]
            }
        }
    },
    {
        "name": "Multiple event types - simple format",
        "config": {
            **BASE_CONFIG,
            "hooks": {
                "preToolUse": [
                    {
                        "command": "python3 .claude/hooks/pre-tool-use/00-auto-approve-safe-ops.py"
                    }
                ],
                "postToolUse": [
                    {
                        "command": "python3 .claude/hooks/post-tool-use/01-state-save.py"
                    }
                ]
            }
        }
    }
]

def test_configuration(config_data, name):
    """Test a single configuration"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")
    
    # Write the test configuration
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(config_data, f, indent=2)
    
    print("Configuration written:")
    print(json.dumps(config_data, indent=2))
    
    # Run doctor command to check for errors
    try:
        result = subprocess.run(
            ["claude", "doctor"],
            cwd=CLAUDE_DIR.parent,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        print(f"\nReturn code: {result.returncode}")
        print(f"STDOUT:\n{result.stdout}")
        print(f"STDERR:\n{result.stderr}")
        
        # Check for the specific error
        if "Cannot assign to read only property" in result.stderr:
            print("❌ FAILED: Got the 'read only property' error")
            return False
        elif "Found invalid settings files" in result.stderr:
            print("❌ FAILED: Invalid settings file")
            return False
        else:
            print("✅ SUCCESS: No configuration errors detected")
            return True
            
    except subprocess.TimeoutExpired:
        print("❌ FAILED: Command timed out")
        return False
    except Exception as e:
        print(f"❌ FAILED: Exception occurred: {e}")
        return False

def main():
    """Run all tests"""
    print("Starting systematic hook configuration tests...")
    
    # Save current configuration
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, 'r') as f:
            original_config = json.load(f)
        print("Original configuration saved")
    else:
        original_config = BASE_CONFIG
    
    successful_configs = []
    
    # Test each configuration
    for test in TEST_CONFIGS:
        success = test_configuration(test["config"], test["name"])
        if success:
            successful_configs.append(test["name"])
        
        # Small delay between tests
        time.sleep(2)
    
    # Restore original configuration
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(original_config, f, indent=2)
    print("\n\nOriginal configuration restored")
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total tests: {len(TEST_CONFIGS)}")
    print(f"Successful: {len(successful_configs)}")
    
    if successful_configs:
        print("\nSuccessful configurations:")
        for config in successful_configs:
            print(f"  ✅ {config}")
    else:
        print("\n❌ No configurations succeeded")
    
    # Save results
    results_file = CLAUDE_DIR / "hook-test-results.json"
    with open(results_file, 'w') as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "successful_configs": successful_configs,
            "total_tests": len(TEST_CONFIGS)
        }, f, indent=2)
    print(f"\nResults saved to: {results_file}")

if __name__ == "__main__":
    main()
