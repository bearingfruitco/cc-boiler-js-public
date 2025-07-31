#!/usr/bin/env python3
"""
Test different command formats for Claude Code hooks
"""

import json
import subprocess
import time
from pathlib import Path

CLAUDE_DIR = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude")

def test_command_format(name, hooks_config):
    """Test a specific command format"""
    print(f"\n{'='*50}")
    print(f"Testing: {name}")
    
    settings = {
        "permissions": {
            "file_system": {"read": True, "write": True},
            "shell": {"execute": True}
        },
        "hooks": hooks_config
    }
    
    # Write settings
    settings_path = CLAUDE_DIR / "settings.json"
    settings_path.write_text(json.dumps(settings, indent=2))
    
    # Run doctor
    result = subprocess.run(
        ["claude", "doctor"],
        cwd=CLAUDE_DIR.parent,
        capture_output=True,
        text=True
    )
    
    if "Cannot assign to read only property" in result.stderr:
        print("❌ Read-only property error")
        return False
    elif "invalid settings" in result.stderr.lower():
        print("❌ Invalid settings")
        return False
    else:
        print("✅ Success - no errors!")
        return True

# Test different formats
tests = [
    # Test 1: Object with command string
    ("Object with command string", {
        "preToolUse": [{
            "command": "python3 .claude/hooks/pre-tool-use/00-auto-approve-safe-ops.py"
        }]
    }),
    
    # Test 2: Direct string array
    ("Direct string array", {
        "preToolUse": [
            "python3 .claude/hooks/pre-tool-use/00-auto-approve-safe-ops.py"
        ]
    }),
    
    # Test 3: Object with type field
    ("Object with type field", {
        "preToolUse": [{
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/00-auto-approve-safe-ops.py"
        }]
    }),
    
    # Test 4: Object with matcher
    ("Object with matcher", {
        "preToolUse": [{
            "matcher": "",
            "command": "python3 .claude/hooks/pre-tool-use/00-auto-approve-safe-ops.py"
        }]
    }),
    
    # Test 5: Shell command array
    ("Command as array", {
        "preToolUse": [{
            "command": ["python3", ".claude/hooks/pre-tool-use/00-auto-approve-safe-ops.py"]
        }]
    })
]

# Save current settings
backup_path = CLAUDE_DIR / "settings-test-backup.json"
settings_path = CLAUDE_DIR / "settings.json"
if settings_path.exists():
    backup_path.write_text(settings_path.read_text())

# Run tests
successful = []
for name, config in tests:
    if test_command_format(name, config):
        successful.append(name)
    time.sleep(1)

# Restore backup
if backup_path.exists():
    settings_path.write_text(backup_path.read_text())
    backup_path.unlink()

print("\n" + "="*50)
print("SUMMARY")
print("="*50)
print(f"Successful formats: {len(successful)}/{len(tests)}")
for fmt in successful:
    print(f"  ✅ {fmt}")
