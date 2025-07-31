#!/usr/bin/env python3
"""Clean up project directory by organizing documentation and removing clutter"""

import os
import shutil
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path("/Users/shawnsmith/dev/bfc/boilerplate")
CLAUDE_DIR = PROJECT_ROOT / ".claude"

def create_directories():
    """Create organized directories for documentation"""
    dirs = [
        PROJECT_ROOT / "docs" / "claude-fixes",
        PROJECT_ROOT / "docs" / "implementation",
        PROJECT_ROOT / "docs" / "workflows",
        CLAUDE_DIR / "troubleshooting",
        CLAUDE_DIR / "backups" / "settings",
        CLAUDE_DIR / "backups" / "test-scripts",
    ]
    
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    return dirs

def organize_root_docs():
    """Move documentation files from root to organized directories"""
    
    # Files to keep in root
    keep_in_root = {
        "README.md",
        "README-PUBLIC.md", 
        "CONTRIBUTING.md",
        "CHANGELOG.md",
        "CLAUDE.md",  # Main Claude documentation
        ".gitignore",
        "package.json",
        "tsconfig.json",
        "next.config.js",
        "tailwind.config.js",
        "biome.json",
        "postcss.config.js",
        "middleware.ts",
        "next-env.d.ts",
        "drizzle.config.ts",
        "playwright.config.ts",
        "bunfig.toml",
        ".npmrc",
        ".coderabbit.yaml",
        "CODEOWNERS",
        "components.json",
        "pnpm-lock.yaml"
    }
    
    # Categorize documentation files
    file_moves = {
        "docs/claude-fixes": [
            "CLAUDE_CODE_HOOKS_FINAL_IMPLEMENTATION.md",
            "CLAUDE_CODE_HOOKS_FIX_GUIDE.md",
            "CLAUDE_CODE_HOOKS_VALIDATION_SUMMARY.md",
            "CLAUDE_HOOKS_FIX_COMPLETE.md",
            "CLAUDE_HOOKS_FIX_SUMMARY.md",
            "CLAUDE_HOOKS_TROUBLESHOOTING_GUIDE.md",
        ],
        "docs/implementation": [
            "KIERAN_ENHANCEMENTS_IMPLEMENTED.md",
            "KIERAN_FINAL_IMPLEMENTATION.md",
            "NEXT_COMMAND_SUGGESTIONS_IMPLEMENTATION.md",
            "MERGE_SUMMARY_NEXT_COMMAND_SUGGESTIONS.md",
            "SECURITY_INTEGRATION_PLAN.md",
            "SECURITY_INTEGRATION_SUMMARY.md",
        ],
        "docs/workflows": [
            "MASTER_WORKFLOW_GUIDE.md",
            "COMMAND_DECISION_GUIDE.md",
            "TDD_QUICK_REFERENCE.md",
            "GIT_COMMIT_GUIDE.md",
            "ACTIVATION_CHECKLIST.md",
            "SECURITY_ACTIVATION_CHECKLIST.md",
        ],
        "docs": [  # General docs
            "FINAL_PUSH_SUMMARY_v2.7.0.md",
            "GITHUB_PUSH_COMPLETE.md",
            "GITHUB_SYNC_SUMMARY.md",
            "GITHUB_UPDATE_SUMMARY.md",
            "PUBLIC_PUSH_COMPLETE.md",
            "PUBLIC_PUSH_STATUS.md",
            "PUSH_SUMMARY.md",
            "TASK_LEDGER_PUSH_SUMMARY.md",
            "UNCOMMITTED_FILES_SUMMARY.md",
        ]
    }
    
    moved_files = []
    
    for dest, files in file_moves.items():
        dest_path = PROJECT_ROOT / dest
        dest_path.mkdir(parents=True, exist_ok=True)
        
        for filename in files:
            src = PROJECT_ROOT / filename
            if src.exists():
                dst = dest_path / filename
                shutil.move(str(src), str(dst))
                moved_files.append((filename, dest))
                print(f"  ✓ Moved {filename} → {dest}/")
    
    return moved_files

def cleanup_shell_scripts():
    """Move diagnostic shell scripts to scripts directory"""
    shell_scripts = [
        "check-master-guide.sh",
        "debug-claude.sh",
        "demo-tdd-workflow.sh",
        "diagnose-claude-error.sh",
        "diagnose-claude-installation.sh",
        "final-diagnostic.sh",
        "find-all-claude-configs.sh",
        "find-json-issues.sh",
        "init-task-ledger.sh",
        "organized-push.sh",
        "quick-fix.sh",
        "run-doctor.sh",
        "setup-branch-awareness-integrated.sh",
        "setup-branch-management.sh",
        "test-minimal-claude.sh"
    ]
    
    scripts_dir = PROJECT_ROOT / "scripts" / "diagnostics"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    
    moved = []
    for script in shell_scripts:
        src = PROJECT_ROOT / script
        if src.exists():
            dst = scripts_dir / script
            shutil.move(str(src), str(dst))
            moved.append(script)
            print(f"  ✓ Moved {script} → scripts/diagnostics/")
    
    return moved

def cleanup_claude_dir():
    """Clean up .claude directory"""
    
    # Move settings backups
    settings_backups = [
        "settings-all-70-hooks.json",
        "settings-all-hooks-complete.json",
        "settings-all-hooks-final-complete.json",
        "settings-backup-2025_07_27_123929.json",
        "settings-diagnostic-backup.json",
        "settings-fixed-matchers.json",
        "settings-fixed.json",
        "settings-migrated-full.json",
        "settings-migrated-gradual.json",
        "settings-migrated-minimal.json",
        "settings-minimal-test.json",
        "settings-safe-backup.json",
        "settings-safe.json",
        "settings-simple-echo-test.json",
        "settings-test-minimal-hook.json",
        "settings-test-one-hook.json",
        "backup-current-settings.json",
        "chains.json.backup"
    ]
    
    backups_dir = CLAUDE_DIR / "backups" / "settings"
    backups_dir.mkdir(parents=True, exist_ok=True)
    
    for backup in settings_backups:
        src = CLAUDE_DIR / backup
        if src.exists():
            dst = backups_dir / backup
            shutil.move(str(src), str(dst))
            print(f"  ✓ Moved {backup} → .claude/backups/settings/")
    
    # Move test/diagnostic scripts
    test_scripts = [
        "binary-search-config.py",
        "diagnose-hook-error.py",
        "enable-all-70-hooks.py",
        "enable-all-hooks-complete-final.py",
        "enable-all-hooks-final.py",
        "find-all-hooks.py",
        "fix-hooks-systematically.py",
        "fix-matcher-fields.py",
        "fix-matcher-format.py",
        "fix-missing-commands.py",
        "fix-worktree-aliases.py",
        "migrate-hooks.py",
        "restore-hooks-gradually.py",
        "test-command-formats.py",
        "test-hook-config.sh",
        "test-hook-configurations.py",
        "test-hook-execution.py",
        "test-hook-formats.sh",
        "test-hooks-individually-fixed.py",
        "test-hooks-individually.py",
        "test-hooks-live.sh",
        "test-hooks-one-by-one.py",
        "verify-hooks-active.py",
        "verify-hooks.py",
        "verify-system-complete.py",
        "check-hook-syntax.sh",
        "check-hooks-status.sh"
    ]
    
    troubleshooting_dir = CLAUDE_DIR / "troubleshooting"
    
    for script in test_scripts:
        src = CLAUDE_DIR / script
        if src.exists():
            dst = troubleshooting_dir / script
            shutil.move(str(src), str(dst))
            print(f"  ✓ Moved {script} → .claude/troubleshooting/")
    
    # Keep essential troubleshooting scripts accessible
    essential_scripts = [
        "audit-system-complete.py",
        "final-system-audit.py"
    ]
    
    # Move temporary files
    temp_files = [
        "diagnostic-output.txt",
        "hook-format-test-results.txt",
        "hook-test-results.json"
    ]
    
    temp_dir = CLAUDE_DIR / "backups" / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    for temp_file in temp_files:
        src = CLAUDE_DIR / temp_file
        if src.exists():
            dst = temp_dir / temp_file
            shutil.move(str(src), str(dst))
            print(f"  ✓ Moved {temp_file} → .claude/backups/temp/")
    
    # Move BACKUP_LOG.md to backups
    if (CLAUDE_DIR / "BACKUP_LOG.md").exists():
        shutil.move(str(CLAUDE_DIR / "BACKUP_LOG.md"), 
                   str(CLAUDE_DIR / "backups" / "BACKUP_LOG.md"))
        print("  ✓ Moved BACKUP_LOG.md → .claude/backups/")

def create_cleanup_summary():
    """Create a summary of what was cleaned up"""
    
    summary = f"""# Project Cleanup Summary
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Organization Structure

### Documentation moved to /docs/
- **claude-fixes/** - All Claude Code hook fixes and troubleshooting guides
- **implementation/** - Implementation summaries and enhancements
- **workflows/** - Workflow guides and references

### Scripts moved to /scripts/diagnostics/
- All diagnostic shell scripts from root directory

### Claude directory organized:
- **troubleshooting/** - All test and fix scripts
- **backups/settings/** - All settings backup files
- **backups/temp/** - Temporary output files

## Key Files Kept Accessible

### In root directory:
- README.md, CLAUDE.md
- All configuration files (package.json, tsconfig.json, etc.)

### In .claude/:
- settings.json (active configuration)
- chains.json, aliases.json, config.json
- audit-system-complete.py, final-system-audit.py (for quick checks)
- command-registry.json

## Quick Access Commands

To check system status:
```bash
python3 .claude/audit-system-complete.py
```

To access troubleshooting scripts:
```bash
ls .claude/troubleshooting/
```

To find documentation:
```bash
ls docs/
```

## Backup Location
Full system backup remains at: .claude.full_backup_20250727_102756/
"""
    
    summary_path = PROJECT_ROOT / "docs" / "CLEANUP_SUMMARY.md"
    summary_path.write_text(summary)
    print(f"\n✅ Created cleanup summary at: docs/CLEANUP_SUMMARY.md")

def main():
    print("🧹 Cleaning up project directory...")
    print("=" * 60)
    
    # Create organized directories
    print("\n📁 Creating organized directories...")
    create_directories()
    
    # Organize root documentation
    print("\n📄 Moving documentation files...")
    organize_root_docs()
    
    # Clean up shell scripts
    print("\n🔧 Moving diagnostic scripts...")
    cleanup_shell_scripts()
    
    # Clean up .claude directory
    print("\n📦 Organizing .claude directory...")
    cleanup_claude_dir()
    
    # Create summary
    create_cleanup_summary()
    
    print("\n✨ Cleanup complete!")
    print("\nYour project is now organized with:")
    print("  • Documentation in /docs/")
    print("  • Scripts in /scripts/diagnostics/")
    print("  • Claude backups in /.claude/backups/")
    print("  • Troubleshooting tools in /.claude/troubleshooting/")
    print("\n🚀 Ready to move forward with a clean workspace!")

if __name__ == "__main__":
    main()
