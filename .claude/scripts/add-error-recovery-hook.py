#!/usr/bin/env python3
"""
Add error recovery hook to PostToolUse
"""

import json
from pathlib import Path

def update_settings():
    settings_path = Path('.claude/settings.json')
    
    # Read current settings
    with open(settings_path) as f:
        settings = json.load(f)
    
    # New hook to add
    new_hook = {
        "type": "command",
        "command": "python3 .claude/hooks/post-tool-use/01-auto-error-recovery.py"
    }
    
    # Find PostToolUse hooks
    for hook_group in settings['hooks']['PostToolUse']:
        if hook_group['matcher'] == "":
            existing_commands = [h['command'] for h in hook_group['hooks']]
            
            # Add at the beginning for early error detection
            if new_hook['command'] not in existing_commands:
                hook_group['hooks'].insert(0, new_hook)
                print(f"✅ Added: {new_hook['command'].split('/')[-1]}")
    
    # Write updated settings
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)
    
    print(f"✅ Updated settings.json with error recovery hook")
    
    # Make hook executable
    hook_path = Path('.claude/hooks/post-tool-use/01-auto-error-recovery.py')
    if hook_path.exists():
        hook_path.chmod(0o755)
        print(f"✅ Made executable: 01-auto-error-recovery.py")

if __name__ == "__main__":
    update_settings()
