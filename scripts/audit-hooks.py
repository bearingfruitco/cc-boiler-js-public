#!/usr/bin/env python3
"""
Audit and fix Claude Code hooks system.
Identifies missing hooks, duplicates, and generates fix report.
"""

import os
import json
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def find_hook_issues():
    """Analyze all hook directories for issues."""
    
    base_dir = Path(".claude/hooks")
    settings_file = Path(".claude/settings.json")
    
    # Load settings to see what hooks are configured
    with open(settings_file) as f:
        settings = json.load(f)
    
    issues = {
        "missing_hooks": [],
        "duplicate_hooks": defaultdict(list),
        "broken_hooks": [],
        "orphaned_files": [],
        "config_mismatches": []
    }
    
    hook_dirs = [
        "pre-tool-use",
        "post-tool-use", 
        "pre-compact",
        "user-prompt-submit",
        "stop",
        "sub-agent-stop",
        "notification"
    ]
    
    print("=" * 80)
    print("CLAUDE CODE HOOKS AUDIT REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()
    
    # Check each hook directory
    for hook_dir in hook_dirs:
        dir_path = base_dir / hook_dir
        if not dir_path.exists():
            print(f"⚠️  Directory missing: {hook_dir}")
            continue
            
        print(f"\n📁 Analyzing {hook_dir}/")
        print("-" * 40)
        
        # Get all files in directory
        files = list(dir_path.glob("*.py*"))
        
        # Group files by base name
        file_groups = defaultdict(list)
        for file in files:
            name = file.name
            # Extract base name (without extensions like .original, .broken, etc)
            if name.endswith('.py'):
                base_name = name
            elif '.py.' in name:
                base_name = name.split('.py')[0] + '.py'
            else:
                base_name = name
                
            file_groups[base_name.replace('.original', '').replace('.broken', '').replace('.backup', '').replace('.old', '')].append(name)
        
        # Analyze each group
        for base_name, variants in file_groups.items():
            if len(variants) > 1:
                print(f"  ⚠️  {base_name}: {len(variants)} versions found")
                for v in sorted(variants):
                    size = (dir_path / v).stat().st_size
                    print(f"      - {v} ({size} bytes)")
                issues["duplicate_hooks"][f"{hook_dir}/{base_name}"] = variants
                
            # Check if main file exists
            if base_name not in [v for v in variants if not any(ext in v for ext in ['.original', '.broken', '.backup', '.old'])]:
                if any('.broken' in v for v in variants):
                    print(f"  ❌ {base_name}: Only .broken version exists")
                    issues["broken_hooks"].append(f"{hook_dir}/{base_name}")
                elif any('.original' in v for v in variants):
                    print(f"  ⚠️  {base_name}: Only .original version exists")
                    issues["orphaned_files"].append(f"{hook_dir}/{base_name}")
    
    # Check configured hooks vs actual files
    print("\n📋 Checking configured hooks in settings.json")
    print("-" * 40)
    
    for hook_type, hook_configs in settings.get("hooks", {}).items():
        if isinstance(hook_configs, list):
            for config in hook_configs:
                if "hooks" in config:
                    for hook in config["hooks"]:
                        if hook.get("type") == "command":
                            cmd = hook.get("command", "")
                            if "python3" in cmd:
                                # Extract file path
                                parts = cmd.split()
                                if len(parts) > 1:
                                    file_path = parts[1]
                                    if not Path(file_path).exists():
                                        print(f"  ❌ Missing: {file_path}")
                                        issues["missing_hooks"].append(file_path)
    
    return issues

def generate_fix_script(issues):
    """Generate script to fix identified issues."""
    
    print("\n" + "=" * 80)
    print("RECOMMENDED FIXES")
    print("=" * 80)
    
    fix_commands = []
    
    # Fix missing hooks
    if issues["missing_hooks"]:
        print("\n🔧 Missing Hooks (need to be restored or created):")
        for hook in issues["missing_hooks"]:
            base_name = Path(hook).name
            dir_name = Path(hook).parent.name
            
            # Check if we have an original version
            original_path = hook + ".original"
            broken_path = hook + ".broken"
            
            if Path(original_path).exists():
                print(f"  ✓ Can restore {hook} from {original_path}")
                fix_commands.append(f"cp {original_path} {hook}")
            elif Path(broken_path).exists():
                print(f"  ⚠️  {hook} has .broken version - needs manual review")
                fix_commands.append(f"# Review and fix: {broken_path} -> {hook}")
            else:
                print(f"  ❌ {hook} - no backup found, needs creation")
                fix_commands.append(f"# CREATE: {hook}")
    
    # Handle duplicates
    if issues["duplicate_hooks"]:
        print("\n🔧 Duplicate Hooks (need consolidation):")
        for hook_path, variants in issues["duplicate_hooks"].items():
            print(f"  {hook_path}:")
            main_file = None
            for v in variants:
                if not any(ext in v for ext in ['.original', '.broken', '.backup', '.old']):
                    main_file = v
                    break
            
            if main_file:
                print(f"    ✓ Keep: {main_file}")
                for v in variants:
                    if v != main_file:
                        fix_commands.append(f"# Archive: .claude/hooks/{hook_path.split('/')[0]}/{v}")
            else:
                print(f"    ⚠️  No main version, needs manual selection from: {variants}")
    
    # Generate fix script
    script_path = Path("scripts/fix-hooks.sh")
    print(f"\n📝 Generating fix script: {script_path}")
    
    with open(script_path, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("# Auto-generated hook fix script\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("# Create backup\n")
        f.write("cp -r .claude/hooks .claude/hooks.backup.$(date +%Y%m%d_%H%M%S)\n\n")
        
        f.write("# Fix missing hooks\n")
        for cmd in fix_commands:
            f.write(f"{cmd}\n")
        
        f.write("\n# Archive old versions\n")
        f.write("mkdir -p .claude/hooks/_archive/$(date +%Y%m%d)\n")
        f.write("find .claude/hooks -name '*.original' -o -name '*.broken' -o -name '*.backup' -o -name '*.old' | while read f; do\n")
        f.write("  mv \"$f\" .claude/hooks/_archive/$(date +%Y%m%d)/\n")
        f.write("done\n")
        
        f.write("\necho 'Hook fixes applied!'\n")
    
    os.chmod(script_path, 0o755)
    print(f"  ✓ Script created and made executable")
    
    return script_path

def generate_issues_json(issues):
    """Generate GitHub issues JSON for tracking."""
    
    github_issues = []
    
    # Critical: Missing hooks
    if issues["missing_hooks"]:
        github_issues.append({
            "title": "🚨 Critical: Missing Claude Code hooks blocking operations",
            "labels": ["bug", "critical", "hooks"],
            "body": f"""## Problem
The following hooks are configured in settings.json but don't exist:

{chr(10).join('- `' + h + '`' for h in issues["missing_hooks"])}

## Impact
- All file operations are blocked
- V4.0 automation features unavailable
- Team collaboration broken

## Solution
1. Run the fix script: `./scripts/fix-hooks.sh`
2. Review any .broken hooks that need manual fixing
3. Test hook execution

## Acceptance Criteria
- [ ] All configured hooks exist
- [ ] No hook errors on file operations
- [ ] V4.0 features operational
"""
        })
    
    # High: Duplicate hooks
    if issues["duplicate_hooks"]:
        github_issues.append({
            "title": "⚠️ High: Duplicate hook versions causing confusion",
            "labels": ["bug", "high", "hooks", "cleanup"],
            "body": f"""## Problem
Multiple versions of hooks exist (.original, .broken, .backup, .old):

{chr(10).join(f'- `{k}`: {len(v)} versions' for k, v in issues["duplicate_hooks"].items())}

## Impact
- Unclear which version is active
- Maintenance confusion
- Potential for wrong hook execution

## Solution
1. Consolidate to single working version per hook
2. Archive old versions
3. Update version control

## Tasks
- [ ] Review each duplicate set
- [ ] Test consolidated versions
- [ ] Archive old versions to .claude/hooks/_archive/
- [ ] Update documentation
"""
        })
    
    # Medium: Broken hooks
    if issues["broken_hooks"]:
        github_issues.append({
            "title": "🔧 Medium: Broken hooks need repair",
            "labels": ["bug", "medium", "hooks"],
            "body": f"""## Problem
The following hooks only have .broken versions:

{chr(10).join('- `' + h + '`' for h in issues["broken_hooks"])}

## Solution
1. Review each .broken file
2. Fix the Python errors
3. Test execution
4. Rename to remove .broken suffix

## Tasks
{chr(10).join('- [ ] Fix `' + h + '`' for h in issues["broken_hooks"])}
"""
        })
    
    # Save issues
    issues_dir = Path("issues")
    issues_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    issues_file = issues_dir / f"hook-issues-{timestamp}.json"
    
    with open(issues_file, "w") as f:
        json.dump(github_issues, f, indent=2)
    
    print(f"\n📋 GitHub issues saved to: {issues_file}")
    
    return github_issues

def main():
    """Main audit function."""
    
    # Check we're in the right directory
    if not Path(".claude").exists():
        print("❌ Error: .claude directory not found. Run from project root.")
        sys.exit(1)
    
    # Run audit
    issues = find_hook_issues()
    
    # Generate fixes
    fix_script = generate_fix_script(issues)
    
    # Generate GitHub issues
    github_issues = generate_issues_json(issues)
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    total_issues = sum(len(v) if isinstance(v, list) else len(v.keys()) for v in issues.values())
    
    print(f"""
📊 Issues Found: {total_issues}
  - Missing hooks: {len(issues['missing_hooks'])}
  - Duplicate hooks: {len(issues['duplicate_hooks'])}
  - Broken hooks: {len(issues['broken_hooks'])}
  - Orphaned files: {len(issues['orphaned_files'])}

📝 Generated:
  - Fix script: ./scripts/fix-hooks.sh
  - GitHub issues: {len(github_issues)} issues created

🚀 Next Steps:
  1. Review the audit results above
  2. Run: ./scripts/fix-hooks.sh
  3. Test: python3 .claude/hooks/pre-tool-use/02-design-check.py
  4. Create GitHub issues for tracking
""")

if __name__ == "__main__":
    main()
