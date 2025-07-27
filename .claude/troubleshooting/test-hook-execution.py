#!/usr/bin/env python3
"""Test that hooks are functioning correctly"""

import subprocess
import json
import time

def test_hook_execution():
    """Test if hooks are actually being executed"""
    print("🧪 Testing Hook Execution")
    print("=" * 40)
    
    # Create a test hook that writes to a file
    test_hook = '''#!/usr/bin/env python3
import sys
import json
import datetime

# Log that the hook was called
with open("/tmp/claude-hook-test.log", "a") as f:
    f.write(f"Hook executed at {datetime.datetime.now()}\\n")

# For PreToolUse, continue normally
sys.exit(0)
'''
    
    # Write test hook
    with open("/Users/shawnsmith/dev/bfc/boilerplate/.claude/hooks/pre-tool-use/99-test-hook.py", "w") as f:
        f.write(test_hook)
    
    subprocess.run(["chmod", "+x", "/Users/shawnsmith/dev/bfc/boilerplate/.claude/hooks/pre-tool-use/99-test-hook.py"])
    
    # Add to settings
    settings_path = "/Users/shawnsmith/dev/bfc/boilerplate/.claude/settings.json"
    with open(settings_path, "r") as f:
        settings = json.load(f)
    
    if "hooks" not in settings:
        settings["hooks"] = {}
    if "preToolUse" not in settings["hooks"]:
        settings["hooks"]["preToolUse"] = []
    
    settings["hooks"]["preToolUse"].append({
        "command": "python3 .claude/hooks/pre-tool-use/99-test-hook.py"
    })
    
    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=2)
    
    # Clear any existing log
    subprocess.run(["rm", "-f", "/tmp/claude-hook-test.log"], capture_output=True)
    
    print("✅ Test hook created")
    print("📝 To verify hooks are working:")
    print("   1. In Claude Code, run any command (like /help)")
    print("   2. Check if /tmp/claude-hook-test.log was created")
    print("   3. Run: cat /tmp/claude-hook-test.log")
    
    # Clean up test hook from settings after a moment
    time.sleep(2)
    settings["hooks"]["preToolUse"] = [
        h for h in settings["hooks"]["preToolUse"] 
        if "99-test-hook.py" not in h.get("command", "")
    ]
    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=2)

if __name__ == "__main__":
    test_hook_execution()
