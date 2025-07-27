#!/usr/bin/env python3
"""
Fix Claude Code hooks configuration:
1. Replace old hooks with v2 versions where available
2. Convert settings.json to official format
3. Add orphaned hooks to configuration
"""

import json
import os
import shutil
from pathlib import Path

def backup_file(file_path):
    """Create a backup of a file"""
    backup_path = str(file_path) + '.backup'
    shutil.copy2(file_path, backup_path)
    print(f"✅ Backed up: {file_path} -> {backup_path}")
    return backup_path

def replace_with_v2_hooks():
    """Replace old hooks with v2 versions where they exist"""
    hooks_dir = Path('.claude/hooks/pre-tool-use')
    v2_hooks = [
        ('11-truth-enforcer.py', '11-truth-enforcer-v2.py'),
        ('13-import-validator.py', '13-import-validator-v2.py'),
        ('15a-dependency-tracker.py', '15a-dependency-tracker-v2.py'),
    ]
    
    for old_name, v2_name in v2_hooks:
        old_path = hooks_dir / old_name
        v2_path = hooks_dir / v2_name
        
        if v2_path.exists():
            # Backup old version
            backup_path = str(old_path) + '.old'
            if old_path.exists():
                shutil.move(str(old_path), backup_path)
                print(f"✅ Backed up: {old_name} -> {old_name}.old")
            
            # Replace with v2
            shutil.copy2(str(v2_path), str(old_path))
            print(f"✅ Replaced {old_name} with {v2_name}")
            
            # Remove v2 file to avoid confusion
            os.remove(str(v2_path))
            print(f"✅ Removed duplicate: {v2_name}")

def convert_settings_format():
    """Convert settings.json to official Claude Code format"""
    settings_path = Path('.claude/settings.json')
    
    # Read current settings
    with open(settings_path, 'r') as f:
        settings = json.load(f)
    
    # Convert hooks format
    new_hooks = {}
    
    # Mapping of old names to new names
    name_mapping = {
        'PreToolUse': 'pre_tool_use',
        'PostToolUse': 'post_tool_use',
        'Stop': 'stop',
        'Notification': 'notification',
        'SubagentStop': 'subagent_stop',
        'PreCompact': 'pre_compact',
        'UserPromptSubmit': 'user_prompt_submit'
    }
    
    for old_name, hook_configs in settings.get('hooks', {}).items():
        new_name = name_mapping.get(old_name, old_name.lower())
        new_hooks[new_name] = []
        
        for config in hook_configs:
            new_config = {}
            
            # Handle matcher
            if 'matcher' in config and config['matcher']:
                if config['matcher'] == 'Bash':
                    new_config['matcher'] = {'tool_name': 'Bash'}
                elif config['matcher'] in ['Write|Edit', 'Write|Edit|MultiEdit']:
                    new_config['matcher'] = {'tool_name': ['Write', 'Edit', 'MultiEdit']}
                elif '|' in config['matcher']:
                    # Handle multiple matchers
                    tools = config['matcher'].split('|')
                    new_config['matcher'] = {'tool_name': tools}
                else:
                    new_config['matcher'] = {'path_pattern': config['matcher']}
            
            # Extract commands
            commands = []
            if 'hooks' in config:
                for hook in config['hooks']:
                    if hook.get('type') == 'command' and 'command' in hook:
                        commands.append(hook['command'])
            
            new_config['commands'] = commands
            
            # Only add if there are commands
            if commands:
                new_hooks[new_name].append(new_config)
    
    # Add orphaned hooks that should be included
    orphaned_hooks_to_add = {
        'pre_tool_use': [
            {
                'matcher': {'tool_name': ['Write', 'Edit', 'MultiEdit']},
                'commands': [
                    'python3 .claude/hooks/pre-tool-use/15-implementation-guide.py',
                    'python3 .claude/hooks/pre-tool-use/17-test-generation-enforcer.py',
                    'python3 .claude/hooks/pre-tool-use/20-feature-state-guardian.py',
                    'python3 .claude/hooks/pre-tool-use/21-branch-controller.py'
                ]
            }
        ]
    }
    
    # Merge orphaned hooks
    for hook_type, configs in orphaned_hooks_to_add.items():
        if hook_type in new_hooks:
            # Find the Write|Edit matcher config
            for i, existing_config in enumerate(new_hooks[hook_type]):
                if existing_config.get('matcher', {}).get('tool_name') == ['Write', 'Edit', 'MultiEdit']:
                    # Add to existing commands
                    for cmd in configs[0]['commands']:
                        if cmd not in existing_config['commands']:
                            existing_config['commands'].append(cmd)
                    break
        
    # Update settings
    settings['hooks'] = new_hooks
    
    # Write updated settings
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)
    
    print(f"✅ Updated {settings_path} to official format")
    
    return settings

def clean_up_duplicates():
    """Remove old backup files and duplicates"""
    hooks_dir = Path('.claude/hooks/pre-tool-use')
    
    # Files to remove
    files_to_remove = [
        '00-auto-approve-safe-ops.py.fixed',
        '02-design-check-simple.py',
        '02-design-check-standards.py',
        '20-feature-state-guardian-v2.py'  # Keep the original, not v2
    ]
    
    for filename in files_to_remove:
        file_path = hooks_dir / filename
        if file_path.exists():
            # Create archive directory
            archive_dir = hooks_dir / '_archived'
            archive_dir.mkdir(exist_ok=True)
            
            # Move to archive instead of deleting
            archive_path = archive_dir / filename
            shutil.move(str(file_path), str(archive_path))
            print(f"📁 Archived: {filename}")

def main():
    """Main execution"""
    print("🔧 Fixing Claude Code Hooks Configuration\n")
    
    # Change to project root
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)
    
    # Step 1: Backup settings.json
    settings_path = Path('.claude/settings.json')
    if settings_path.exists():
        backup_file(settings_path)
    
    # Step 2: Replace old hooks with v2 versions
    print("\n📝 Updating hooks to v2 versions...")
    replace_with_v2_hooks()
    
    # Step 3: Convert settings format
    print("\n🔄 Converting settings.json format...")
    convert_settings_format()
    
    # Step 4: Clean up duplicates
    print("\n🧹 Cleaning up duplicates...")
    clean_up_duplicates()
    
    print("\n✅ Configuration fixed successfully!")
    print("\n⚠️  Important:")
    print("1. Restart Claude Code for changes to take effect")
    print("2. Test a few hooks to ensure they're working")
    print("3. Original files are backed up with .backup or .old extensions")
    
    # Show summary
    with open('.claude/settings.json', 'r') as f:
        settings = json.load(f)
    
    print("\n📊 Hook Summary:")
    for hook_type, configs in settings['hooks'].items():
        total_hooks = sum(len(config['commands']) for config in configs)
        print(f"  {hook_type}: {total_hooks} hooks")

if __name__ == '__main__':
    main()
