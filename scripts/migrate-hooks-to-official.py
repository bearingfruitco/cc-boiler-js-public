#!/usr/bin/env python3
"""
Hook Migration Script - Update all hooks to official Claude Code format
Based on https://docs.anthropic.com/en/docs/claude-code/hooks
"""

import os
import sys
import shutil
import re
from pathlib import Path
from datetime import datetime

# Hook directory
HOOKS_DIR = Path('.claude/hooks')

def backup_hook(hook_path):
    """Create a backup of the hook before modifying"""
    backup_path = hook_path.with_suffix(hook_path.suffix + '.backup-' + datetime.now().strftime('%Y%m%d-%H%M%S'))
    shutil.copy2(hook_path, backup_path)
    return backup_path

def fix_hook_format(content):
    """Fix hook to use official format"""
    modified = False
    original_content = content
    
    # 1. Fix tool names
    tool_replacements = [
        ('write_file', 'Write'),
        ('edit_file', 'Edit'),
        ('multi_edit', 'MultiEdit'),
        ('read_file', 'Read'),
        ('bash', 'Bash'),
        ('web_search', 'WebSearch'),
        ('web_fetch', 'WebFetch'),
    ]
    
    for old_name, new_name in tool_replacements:
        if f"'{old_name}'" in content or f'"{old_name}"' in content:
            content = content.replace(f"'{old_name}'", f"'{new_name}'")
            content = content.replace(f'"{old_name}"', f'"{new_name}"')
            modified = True
    
    # 2. Fix decision block pattern
    # Pattern 1: print(json.dumps({"decision": "block", ...}))
    pattern1 = r'print\(json\.dumps\(\s*\{\s*["\']decision["\']\s*:\s*["\']block["\'][^}]*\}\s*\)\)'
    
    # Pattern 2: Simple {"decision": "block"} output
    pattern2 = r'{\s*["\']decision["\']\s*:\s*["\']block["\'][^}]*}'
    
    # Find and replace pattern 1
    matches = list(re.finditer(pattern1, content))
    for match in reversed(matches):  # Reverse to maintain positions
        # Extract the message if present
        msg_match = re.search(r'["\'](?:message|reason)["\']:\s*([^,}]+)', match.group())
        
        if msg_match:
            message_var = msg_match.group(1).strip()
            # Replace with stderr + exit(2)
            replacement = f'print({message_var}, file=sys.stderr)\n            sys.exit(2)  # Block operation'
        else:
            replacement = 'sys.exit(2)  # Block operation'
        
        # Find the sys.exit(0) that typically follows
        following_text = content[match.end():match.end()+100]
        if 'sys.exit(0)' in following_text:
            # Remove the sys.exit(0) as we're replacing it
            content = content[:match.start()] + replacement + content[match.end():].replace('sys.exit(0)', '', 1)
        else:
            content = content[:match.start()] + replacement + content[match.end():]
        
        modified = True
    
    # 3. Fix tool_input access
    if 'params = input_data.get(' in content:
        content = content.replace(
            "params = input_data.get('params', {})",
            "tool_input = input_data.get('tool_input', {})"
        )
        content = content.replace('params.get(', 'tool_input.get(')
        content = content.replace('params[', 'tool_input[')
        modified = True
    
    return content, modified

def archive_duplicates():
    """Archive all duplicate hook files"""
    archive_dir = HOOKS_DIR / '_archive' / datetime.now().strftime('%Y%m%d_%H%M%S')
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    duplicates_moved = 0
    
    for hook_dir in HOOKS_DIR.iterdir():
        if not hook_dir.is_dir() or hook_dir.name.startswith('_'):
            continue
        
        for file in hook_dir.iterdir():
            if file.is_file() and any(ext in file.name for ext in ['.original', '.broken', '.backup', '.old', '.prefixbatch']):
                dest = archive_dir / hook_dir.name / file.name
                dest.parent.mkdir(exist_ok=True)
                shutil.move(str(file), str(dest))
                duplicates_moved += 1
                print(f"Archived: {file.name}")
    
    return duplicates_moved

def install_critical_hooks():
    """Install the three critical hooks that are missing"""
    pre_tool_dir = HOOKS_DIR / 'pre-tool-use'
    
    critical_hooks = {
        '07-pii-protection.py': '07-pii-protection-FIXED-OFFICIAL.py',
        '16-tcpa-compliance.py': '16-tcpa-compliance-FIXED-OFFICIAL.py',
        '22-security-validator.py': '22-security-validator-FIXED-OFFICIAL.py',
    }
    
    installed = []
    
    for target, source in critical_hooks.items():
        source_path = pre_tool_dir / source
        target_path = pre_tool_dir / target
        
        if source_path.exists():
            # Backup existing if present
            if target_path.exists():
                backup_hook(target_path)
            
            shutil.copy2(source_path, target_path)
            installed.append(target)
            print(f"✅ Installed: {target}")
    
    return installed

def validate_hook(hook_path):
    """Validate a hook follows official format"""
    issues = []
    
    with open(hook_path, 'r') as f:
        content = f.read()
    
    # Check for old patterns
    if '"decision"' in content and '"block"' in content:
        issues.append("Uses old decision:block format")
    
    if 'write_file' in content or 'edit_file' in content:
        issues.append("Uses old tool names")
    
    if "params = input_data.get('params" in content:
        issues.append("Uses params instead of tool_input")
    
    # Check for proper exit codes
    if 'sys.exit(2)' not in content and 'PreToolUse' in str(hook_path):
        if '"block"' in content:
            issues.append("Missing sys.exit(2) for blocking")
    
    return issues

def main():
    """Main migration process"""
    print("=" * 60)
    print("Claude Code Hooks Migration Tool")
    print("Based on official docs: https://docs.anthropic.com/en/docs/claude-code/hooks")
    print("=" * 60)
    print()
    
    # Step 1: Archive duplicates
    print("Step 1: Archiving duplicate files...")
    duplicates = archive_duplicates()
    print(f"Archived {duplicates} duplicate files\n")
    
    # Step 2: Install critical hooks
    print("Step 2: Installing critical hooks...")
    installed = install_critical_hooks()
    print(f"Installed {len(installed)} critical hooks\n")
    
    # Step 3: Fix existing hooks
    print("Step 3: Updating hooks to official format...")
    
    fixed_count = 0
    error_count = 0
    
    for hook_dir in HOOKS_DIR.iterdir():
        if not hook_dir.is_dir() or hook_dir.name.startswith('_'):
            continue
        
        print(f"\nProcessing {hook_dir.name}/...")
        
        for hook_file in hook_dir.glob('*.py'):
            # Skip our fixed versions
            if 'FIXED' in hook_file.name or 'OFFICIAL' in hook_file.name:
                continue
            
            try:
                with open(hook_file, 'r') as f:
                    content = f.read()
                
                fixed_content, was_modified = fix_hook_format(content)
                
                if was_modified:
                    # Backup original
                    backup_path = backup_hook(hook_file)
                    
                    # Write fixed version
                    with open(hook_file, 'w') as f:
                        f.write(fixed_content)
                    
                    print(f"  ✅ Fixed: {hook_file.name} (backup: {backup_path.name})")
                    fixed_count += 1
                else:
                    # Validate even if not modified
                    issues = validate_hook(hook_file)
                    if issues:
                        print(f"  ⚠️  {hook_file.name}: {', '.join(issues)}")
                    else:
                        print(f"  ✓ {hook_file.name}: Already compliant")
                        
            except Exception as e:
                print(f"  ❌ Error processing {hook_file.name}: {e}")
                error_count += 1
    
    # Step 4: Summary
    print("\n" + "=" * 60)
    print("Migration Summary:")
    print(f"  • Duplicates archived: {duplicates}")
    print(f"  • Critical hooks installed: {len(installed)}")
    print(f"  • Hooks fixed: {fixed_count}")
    print(f"  • Errors: {error_count}")
    print("=" * 60)
    
    # Step 5: Validation report
    print("\nValidation Report:")
    print("-" * 40)
    
    all_valid = True
    for hook_dir in HOOKS_DIR.iterdir():
        if not hook_dir.is_dir() or hook_dir.name.startswith('_'):
            continue
        
        for hook_file in hook_dir.glob('*.py'):
            if 'FIXED' in hook_file.name or 'OFFICIAL' in hook_file.name:
                continue
            
            issues = validate_hook(hook_file)
            if issues:
                all_valid = False
                print(f"❌ {hook_file.relative_to(HOOKS_DIR)}")
                for issue in issues:
                    print(f"   - {issue}")
    
    if all_valid:
        print("✅ All hooks are compliant with official format!")
    
    print("\n" + "=" * 60)
    print("Migration complete!")
    print("\nNext steps:")
    print("1. Restart Claude Code to load updated hooks")
    print("2. Test file operations to ensure hooks work correctly")
    print("3. Remove -FIXED-OFFICIAL versions once confirmed working")
    print("=" * 60)

if __name__ == '__main__':
    os.chdir('/Users/shawnsmith/dev/bfc/boilerplate')
    main()
