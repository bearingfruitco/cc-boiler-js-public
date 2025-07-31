#!/usr/bin/env python3
"""
Diagnose the Claude Code hook configuration error
Tests different data types and structures
"""

import json
import subprocess
import sys
import time
from pathlib import Path

def run_claude_doctor():
    """Run claude doctor and capture output"""
    try:
        result = subprocess.run(
            ["claude", "doctor"],
            cwd="/Users/shawnsmith/dev/bfc/boilerplate",
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

def test_config(name, config):
    """Test a specific configuration"""
    print(f"\n{'='*50}")
    print(f"Testing: {name}")
    print(f"{'='*50}")
    
    # Save current settings
    settings_path = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude/settings.json")
    backup_path = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude/settings-diagnostic-backup.json")
    
    # Backup current
    if settings_path.exists():
        backup_path.write_text(settings_path.read_text())
    
    # Write test config
    settings_path.write_text(json.dumps(config, indent=2))
    print("Config written:", json.dumps(config, indent=2))
    
    # Test
    code, stdout, stderr = run_claude_doctor()
    
    print(f"\nReturn code: {code}")
    if stderr and "Cannot assign to read only property" in stderr:
        print("❌ ERROR: Read-only property error detected!")
    elif stderr and "invalid settings" in stderr.lower():
        print("❌ ERROR: Invalid settings detected")
    else:
        print("✅ SUCCESS: No errors detected")
    
    if stderr:
        print(f"STDERR: {stderr}")
    
    # Restore backup
    if backup_path.exists():
        settings_path.write_text(backup_path.read_text())
    
    return not ("Cannot assign to read only property" in stderr)

# Test configurations
BASE = {
    "permissions": {
        "file_system": {"read": True, "write": True},
        "shell": {"execute": True}
    }
}

# Test 1: No hooks at all
test_config("No hooks", BASE)

# Test 2: Empty hooks object
test_config("Empty hooks object", {
    **BASE,
    "hooks": {}
})

# Test 3: Hook with string command (as shown in docs)
test_config("Hook with string command", {
    **BASE,
    "hooks": {
        "preToolUse": [
            {
                "command": "python3 .claude/hooks/pre-tool-use/00-auto-approve-safe-ops.py"
            }
        ]
    }
})

# Test 4: Hook with array command
test_config("Hook with array command", {
    **BASE,
    "hooks": {
        "preToolUse": [
            {
                "command": ["python3", ".claude/hooks/pre-tool-use/00-auto-approve-safe-ops.py"]
            }
        ]
    }
})

# Test 5: Direct string in array (no object wrapper)
test_config("Direct string in hook array", {
    **BASE,
    "hooks": {
        "preToolUse": [
            "python3 .claude/hooks/pre-tool-use/00-auto-approve-safe-ops.py"
        ]
    }
})

# Test 6: Using 'type' field
test_config("Hook with type field", {
    **BASE,
    "hooks": {
        "preToolUse": [
            {
                "type": "command",
                "command": "python3 .claude/hooks/pre-tool-use/00-auto-approve-safe-ops.py"
            }
        ]
    }
})

# Test 7: Using nested structure from backup
test_config("Nested structure with matcher", {
    **BASE,
    "hooks": {
        "PreToolUse": [
            {
                "matcher": {},
                "hooks": [
                    {
                        "type": "command",
                        "command": "python3 .claude/hooks/pre-tool-use/00-auto-approve-safe-ops.py"
                    }
                ]
            }
        ]
    }
})

print("\n" + "="*50)
print("DIAGNOSTIC COMPLETE")
print("="*50)
