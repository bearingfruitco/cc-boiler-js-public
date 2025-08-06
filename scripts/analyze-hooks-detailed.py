#!/usr/bin/env python3
"""
Detailed hook analysis tool - examines each hook group to determine the best version.
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def get_file_info(file_path):
    """Get detailed info about a file."""
    try:
        stat = os.stat(file_path)
        with open(file_path, 'r') as f:
            content = f.read()
            lines = content.split('\n')
            
        # Check for common issues
        has_syntax_error = False
        try:
            compile(content, file_path, 'exec')
        except SyntaxError:
            has_syntax_error = True
            
        # Look for key indicators
        has_main_block = '__main__' in content
        has_functions = 'def ' in content
        has_imports = 'import ' in content
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        
        return {
            'path': file_path,
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'lines': len(lines),
            'has_syntax_error': has_syntax_error,
            'has_main_block': has_main_block,
            'has_functions': has_functions,
            'has_imports': has_imports,
            'comment_lines': comment_lines,
            'md5': hashlib.md5(content.encode()).hexdigest()[:8]
        }
    except Exception as e:
        return {
            'path': file_path,
            'error': str(e)
        }

def analyze_hook_group(base_name, files, dir_path):
    """Analyze a group of hook files to determine the best version."""
    
    print(f"\n{'=' * 80}")
    print(f"Analyzing: {base_name}")
    print(f"{'=' * 80}")
    
    file_infos = []
    for file in files:
        info = get_file_info(dir_path / file)
        file_infos.append(info)
        
    # Sort by various criteria
    valid_files = [f for f in file_infos if not f.get('error') and not f.get('has_syntax_error')]
    
    if not valid_files:
        print("❌ No valid Python files in this group!")
        for f in file_infos:
            if f.get('error'):
                print(f"  - {Path(f['path']).name}: ERROR - {f['error']}")
            elif f.get('has_syntax_error'):
                print(f"  - {Path(f['path']).name}: SYNTAX ERROR")
        return None
    
    # Display analysis
    print("\nFile Comparison:")
    print(f"{'File':<40} {'Size':<8} {'Lines':<7} {'Modified':<20} {'Status':<15}")
    print("-" * 100)
    
    for info in sorted(file_infos, key=lambda x: x.get('modified', datetime.min), reverse=True):
        name = Path(info['path']).name
        if 'error' in info:
            print(f"{name:<40} ERROR: {info['error']}")
        else:
            status = []
            if info['has_syntax_error']:
                status.append("SYNTAX_ERR")
            if not info['has_main_block']:
                status.append("NO_MAIN")
            if not info['has_functions']:
                status.append("NO_FUNCS")
            
            status_str = ','.join(status) if status else "OK"
            
            # Highlight likely best version
            marker = ""
            if not any(ext in name for ext in ['.original', '.broken', '.backup', '.old']):
                marker = " ← CURRENT"
            
            print(f"{name:<40} {info['size']:<8} {info['lines']:<7} "
                  f"{info['modified'].strftime('%Y-%m-%d %H:%M'):<20} {status_str:<15}{marker}")
    
    # Recommendation logic
    print("\n📊 Analysis:")
    
    # Find the main version (without extensions)
    main_version = None
    for info in valid_files:
        name = Path(info['path']).name
        if not any(ext in name for ext in ['.original', '.broken', '.backup', '.old', '.prefixbatch']):
            main_version = info
            break
    
    # Find the newest valid version
    newest = max(valid_files, key=lambda x: x['modified'])
    
    # Find the largest valid version (often most complete)
    largest = max(valid_files, key=lambda x: x['size'])
    
    recommendation = None
    
    if main_version:
        # Check if main version is healthy
        if main_version == newest and main_version == largest:
            print(f"✅ Current version is newest and largest - KEEP CURRENT")
            recommendation = Path(main_version['path']).name
        elif main_version['size'] < largest['size'] * 0.5:
            print(f"⚠️  Current version is much smaller than {Path(largest['path']).name}")
            print(f"    Current: {main_version['size']} bytes vs Largest: {largest['size']} bytes")
            recommendation = Path(largest['path']).name
        else:
            print(f"✅ Current version appears healthy - KEEP CURRENT")
            recommendation = Path(main_version['path']).name
    else:
        # No main version exists
        if newest == largest:
            print(f"💡 No main version exists. Recommend using {Path(newest['path']).name} (newest & largest)")
            recommendation = Path(newest['path']).name
        else:
            print(f"💡 No main version exists.")
            print(f"   Newest: {Path(newest['path']).name} ({newest['modified'].strftime('%Y-%m-%d')})")
            print(f"   Largest: {Path(largest['path']).name} ({largest['size']} bytes)")
            recommendation = Path(largest['path']).name
    
    # Check for special cases
    for info in file_infos:
        name = Path(info['path']).name
        if '.prefixbatch' in name and info in valid_files:
            print(f"📌 Note: {name} might be from automated update")
    
    print(f"\n🎯 RECOMMENDATION: Use {recommendation}")
    
    return {
        'base_name': base_name,
        'recommendation': recommendation,
        'all_files': [Path(f['path']).name for f in file_infos],
        'main_exists': main_version is not None
    }

def main():
    """Analyze all hooks and generate detailed recommendations."""
    
    base_dir = Path(".claude/hooks")
    
    hook_dirs = [
        "pre-tool-use",
        "post-tool-use",
        "pre-compact",
        "user-prompt-submit",
        "stop",
        "sub-agent-stop",
        "notification"
    ]
    
    all_recommendations = []
    
    print("=" * 80)
    print("DETAILED HOOK ANALYSIS")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    for hook_dir in hook_dirs:
        dir_path = base_dir / hook_dir
        if not dir_path.exists():
            continue
            
        print(f"\n\n{'#' * 80}")
        print(f"# {hook_dir.upper()}")
        print(f"{'#' * 80}")
        
        # Group files
        files = list(dir_path.glob("*.py*"))
        file_groups = defaultdict(list)
        
        for file in files:
            name = file.name
            # Extract base name
            base = name.replace('.original', '').replace('.broken', '').replace('.backup', '').replace('.old', '').replace('.prefixbatch', '')
            if base.endswith('.py'):
                file_groups[base].append(name)
        
        # Analyze each group
        for base_name, group_files in sorted(file_groups.items()):
            if len(group_files) > 1:
                rec = analyze_hook_group(base_name, group_files, dir_path)
                if rec:
                    rec['directory'] = hook_dir
                    all_recommendations.append(rec)
            elif len(group_files) == 1 and any(ext in group_files[0] for ext in ['.original', '.broken', '.backup', '.old']):
                # Single orphaned backup file
                print(f"\n⚠️  Orphaned backup: {base_name}")
                print(f"    Only file: {group_files[0]}")
                all_recommendations.append({
                    'directory': hook_dir,
                    'base_name': base_name,
                    'recommendation': 'CREATE_FROM_BACKUP',
                    'all_files': group_files,
                    'main_exists': False
                })
    
    # Generate action script
    print("\n\n" + "=" * 80)
    print("GENERATING ACTION PLAN")
    print("=" * 80)
    
    script_lines = [
        "#!/bin/bash",
        "# Manual hook repair script",
        f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "# This script shows what needs to be done - review each action!",
        "",
        "# Create backup first",
        "cp -r .claude/hooks .claude/hooks.backup.$(date +%Y%m%d_%H%M%S)",
        "",
        "# Actions to take:",
        ""
    ]
    
    for rec in all_recommendations:
        dir_name = rec['directory']
        base_name = rec['base_name']
        
        script_lines.append(f"# {dir_name}/{base_name}")
        
        if rec['recommendation'] == 'CREATE_FROM_BACKUP':
            backup_file = rec['all_files'][0]
            target_file = base_name
            script_lines.append(f"# CREATE: No main version exists, create from backup")
            script_lines.append(f"cp .claude/hooks/{dir_name}/{backup_file} .claude/hooks/{dir_name}/{target_file}")
        elif not rec['main_exists']:
            # Need to rename recommended file
            script_lines.append(f"# RESTORE: No main version, use {rec['recommendation']}")
            script_lines.append(f"cp .claude/hooks/{dir_name}/{rec['recommendation']} .claude/hooks/{dir_name}/{base_name}")
        elif rec['recommendation'] != base_name:
            # Replace current with recommended
            script_lines.append(f"# REPLACE: Current may be outdated, check {rec['recommendation']}")
            script_lines.append(f"# diff .claude/hooks/{dir_name}/{base_name} .claude/hooks/{dir_name}/{rec['recommendation']}")
            script_lines.append(f"# If better, then:")
            script_lines.append(f"# cp .claude/hooks/{dir_name}/{rec['recommendation']} .claude/hooks/{dir_name}/{base_name}")
        else:
            script_lines.append(f"# KEEP: Current version is best")
        
        # Archive others
        for file in rec['all_files']:
            if file != base_name and file != rec['recommendation']:
                script_lines.append(f"# mv .claude/hooks/{dir_name}/{file} .claude/hooks/_archive/")
        
        script_lines.append("")
    
    # Save action script
    script_path = Path("scripts/hook-repair-manual.sh")
    with open(script_path, 'w') as f:
        f.write('\n'.join(script_lines))
    os.chmod(script_path, 0o755)
    
    print(f"\n✅ Manual action script generated: {script_path}")
    print("\n⚠️  IMPORTANT: Review the script before running!")
    print("    Some recommendations need manual verification with 'diff' command")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total hook groups analyzed: {len(all_recommendations)}")
    print(f"Groups needing action: {sum(1 for r in all_recommendations if not r['main_exists'] or r['recommendation'] != r['base_name'])}")
    print(f"Groups with missing main: {sum(1 for r in all_recommendations if not r['main_exists'])}")

if __name__ == "__main__":
    main()
