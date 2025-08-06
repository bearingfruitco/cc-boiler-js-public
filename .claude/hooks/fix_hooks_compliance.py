#!/usr/bin/env python3
"""
Hook Auto-Fixer
Automatically fixes common compliance issues in hooks
"""

import os
import re
from pathlib import Path
import shutil
from datetime import datetime

# Wrong tool names mapping
TOOL_NAME_FIXES = {
    "'write_file'": "'Write'",
    '"write_file"': '"Write"',
    "'edit_file'": "'Edit'",
    '"edit_file"': '"Edit"',
    "'str_replace'": "'MultiEdit'",
    '"str_replace"': '"MultiEdit"',
    "'multi_edit'": "'MultiEdit'",
    '"multi_edit"': '"MultiEdit"',
    "'read_file'": "'Read'",
    '"read_file"': '"Read"',
    "'bash'": "'Bash'",
    '"bash"': '"Bash"',
    "'list_directory'": "'ListDirectory'",
    '"list_directory"': '"ListDirectory"',
    "'search_files'": "'SearchFiles'",
    '"search_files"': '"SearchFiles"',
    "'create_directory'": "'CreateDirectory'",
    '"create_directory"': '"CreateDirectory"',
    "'delete_file'": "'DeleteFile'",
    '"delete_file"': '"DeleteFile"',
    "'create_task'": "'Task'",
    '"create_task"': '"Task"',
    "'web_fetch'": "'WebFetch'",
    '"web_fetch"': '"WebFetch"',
    "'web_search'": "'WebSearch'",
    '"web_search"': '"WebSearch"',
}

def fix_hook(file_path, dry_run=False):
    """Fix a single hook file"""
    changes_made = []
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        original_content = content
    except:
        return None
    
    # Fix 1: Wrong tool names
    for wrong, correct in TOOL_NAME_FIXES.items():
        if wrong in content:
            content = content.replace(wrong, correct)
            changes_made.append(f"Fixed tool name: {wrong} → {correct}")
    
    # Fix 2: sys.exit(0) in exception handlers → sys.exit(1)
    # Match patterns like: except Exception as e:\n    ...sys.exit(0)
    pattern = r'(except[^:]*:(?:[^\n]*\n)*?\s*)sys\.exit\(0\)'
    matches = list(re.finditer(pattern, content))
    for match in reversed(matches):  # Process in reverse to maintain positions
        if 'except' in match.group(0):
            content = content[:match.start()] + match.group(1) + 'sys.exit(1)' + content[match.end():]
            changes_made.append("Fixed exception handler exit code: sys.exit(0) → sys.exit(1)")
    
    # Fix 3: Remove JSON decision format
    if 'json.dumps' in content and '"decision"' in content:
        # This is complex - mark for manual review
        changes_made.append("NEEDS MANUAL FIX: JSON decision format detected")
    
    # Fix 4: tool_response → tool_result in PostToolUse hooks
    if 'post-tool-use' in str(file_path) and 'tool_response' in content:
        content = content.replace("'tool_response'", "'tool_result'")
        content = content.replace('"tool_response"', '"tool_result"')
        content = content.replace(".get('tool_response'", ".get('tool_result'")
        content = content.replace('.get("tool_response"', '.get("tool_result"')
        changes_made.append("Fixed field name: tool_response → tool_result")
    
    # Fix 5: params → tool_input
    if "'params'" in content or '"params"' in content:
        content = content.replace("'params'", "'tool_input'")
        content = content.replace('"params"', '"tool_input"')
        content = content.replace(".get('params'", ".get('tool_input'")
        content = content.replace('.get("params"', '.get("tool_input"')
        changes_made.append("Fixed field name: params → tool_input")
    
    # Fix 6: parameters → tool_input (only if not in fallback logic)
    if "'parameters'" in content or '"parameters"' in content:
        if 'tool_use' not in content:  # Only fix if not fallback logic
            content = content.replace("'parameters'", "'tool_input'")
            content = content.replace('"parameters"', '"tool_input"')
            content = content.replace(".get('parameters'", ".get('tool_input'")
            content = content.replace('.get("parameters"', '.get("tool_input"')
            changes_made.append("Fixed field name: parameters → tool_input")
    
    # Fix 7: Remove unnecessary fallback logic for tool names
    if "tool_use" in content and "get('name'" in content:
        changes_made.append("NEEDS MANUAL FIX: Has unnecessary fallback logic for tool names")
    
    if changes_made and content != original_content:
        if not dry_run:
            # Backup original
            backup_path = file_path.with_suffix('.py.backup')
            shutil.copy2(file_path, backup_path)
            
            # Write fixed content
            with open(file_path, 'w') as f:
                f.write(content)
        
        return changes_made
    
    return None

def main():
    hooks_dir = Path("/Users/shawnsmith/dev/bfc/boilerplate/.claude/hooks")
    
    # Get all Python files in hooks directories
    hook_files = []
    for subdir in hooks_dir.iterdir():
        if subdir.is_dir() and not subdir.name.startswith('_'):
            hook_files.extend(subdir.glob('*.py'))
    
    print("# Hook Auto-Fix Report\n")
    print(f"Processing {len(hook_files)} hook files...\n")
    
    fixed_count = 0
    manual_fix_needed = []
    
    for hook_file in sorted(hook_files):
        changes = fix_hook(hook_file, dry_run=False)
        if changes:
            fixed_count += 1
            rel_path = hook_file.relative_to(hooks_dir)
            print(f"\n## Fixed: {rel_path}")
            for change in changes:
                if "NEEDS MANUAL" in change:
                    manual_fix_needed.append((rel_path, change))
                    print(f"  ⚠️  {change}")
                else:
                    print(f"  ✅ {change}")
    
    print(f"\n# Summary")
    print(f"- Total hooks processed: {len(hook_files)}")
    print(f"- Hooks fixed: {fixed_count}")
    print(f"- Hooks needing manual fix: {len(manual_fix_needed)}")
    
    if manual_fix_needed:
        print(f"\n# Manual Fixes Required\n")
        for path, issue in manual_fix_needed:
            print(f"- {path}: {issue.replace('NEEDS MANUAL FIX: ', '')}")

if __name__ == "__main__":
    main()
