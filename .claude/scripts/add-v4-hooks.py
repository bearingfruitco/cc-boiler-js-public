#!/usr/bin/env python3
"""
Add v4.0 hooks to Claude settings
"""

import json
from pathlib import Path

def update_settings():
    settings_path = Path('.claude/settings.json')
    
    # Read current settings
    with open(settings_path) as f:
        settings = json.load(f)
    
    # New v4.0 hooks to add
    new_hooks = [
        {
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/17-performance-budget-enforcer.py"
        },
        {
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/18-security-first-enforcer.py"
        },
        {
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/19-auto-rls-generator.py"
        }
    ]
    
    # Find PreToolUse hooks
    for hook_group in settings['hooks']['PreToolUse']:
        if hook_group['matcher'] == "":
            existing_commands = [h['command'] for h in hook_group['hooks']]
            
            # Add new hooks if not already present
            for new_hook in new_hooks:
                if new_hook['command'] not in existing_commands:
                    # Insert after security validator (position 22)
                    insert_pos = min(22, len(hook_group['hooks']))
                    hook_group['hooks'].insert(insert_pos, new_hook)
                    print(f"✅ Added: {new_hook['command'].split('/')[-1]}")
    
    # Backup current settings
    backup_path = settings_path.with_suffix('.json.backup-v3')
    with open(backup_path, 'w') as f:
        json.dump(settings, f, indent=2)
    print(f"\n📦 Backup created: {backup_path}")
    
    # Write updated settings
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)
    
    print(f"✅ Updated settings.json with v4.0 hooks")
    
    # Make hooks executable
    hooks_dir = Path('.claude/hooks/pre-tool-use')
    for hook_file in ['17-performance-budget-enforcer.py', 
                      '18-security-first-enforcer.py', 
                      '19-auto-rls-generator.py']:
        hook_path = hooks_dir / hook_file
        if hook_path.exists():
            hook_path.chmod(0o755)
            print(f"✅ Made executable: {hook_file}")

if __name__ == "__main__":
    update_settings()
