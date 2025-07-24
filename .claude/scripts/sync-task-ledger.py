#!/usr/bin/env python3
"""
Task Ledger Sync Script
Scans existing task files and creates/updates the task ledger
"""

import re
from pathlib import Path
from datetime import datetime
import subprocess
import json

def get_current_branch():
    """Get current git branch."""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except:
        return 'main'

def extract_issue_from_branch(branch):
    """Extract issue number from branch name."""
    match = re.search(r'(\d+)', branch)
    if match:
        return f"#{match.group(1)}"
    return "#pending"

def count_tasks_in_file(filepath):
    """Count total tasks in a task file."""
    try:
        content = filepath.read_text()
        total = len(re.findall(r'^\s*- \[[ x]\]', content, re.MULTILINE))
        return total
    except:
        return 0

def count_completed_tasks(filepath):
    """Count completed tasks in a task file."""
    try:
        content = filepath.read_text()
        completed = len(re.findall(r'^\s*- \[x\]', content, re.MULTILINE))
        return completed
    except:
        return 0

def scan_task_files():
    """Scan for all task files in the project."""
    task_files = []
    
    # Look in standard locations
    paths = [
        Path('docs/project/features'),
        Path('docs/features'),
        Path('tasks')
    ]
    
    for path in paths:
        if path.exists():
            task_files.extend(path.glob('*-tasks.md'))
    
    return task_files

def create_ledger_entry(task_file):
    """Create a ledger entry for a task file."""
    # Extract feature name
    feature = task_file.stem.replace('-tasks', '')
    
    # Count tasks
    total = count_tasks_in_file(task_file)
    completed = count_completed_tasks(task_file)
    
    # Determine status
    if completed == 0:
        status = "📋 Generated"
    elif completed == total and total > 0:
        status = "✅ Completed"
    else:
        status = "🔄 In Progress"
    
    # Try to find associated PRD
    prd_path = task_file.parent / f"{feature}-PRD.md"
    
    # Get file modification time
    mtime = datetime.fromtimestamp(task_file.stat().st_mtime)
    
    entry = f"""### {feature}

**Created**: {mtime.strftime("%Y-%m-%d %H:%M:%S")}
**Issue**: #pending
**Branch**: `unknown`
**Status**: {status}
**Progress**: {completed}/{total} tasks

**Files**:
- Tasks: `{task_file}`"""
    
    if prd_path.exists():
        entry += f"\n- PRD: `{prd_path}`"
    
    entry += f"""

**Quick Actions**:
- Process tasks: `/pt {feature}`
- View board: `/tb`
- Check status: `/ts`

---

"""
    
    return entry, total, completed

def sync_task_ledger():
    """Main sync function."""
    print("🔄 Syncing task ledger...")
    
    # Check if ledger exists
    ledger_path = Path('.task-ledger.md')
    
    if not ledger_path.exists():
        # Create new ledger
        project_name = Path.cwd().name
        content = f"""# Task Ledger - {project_name}

> Single source of truth for all project tasks. Auto-updated by Claude Code hooks.

**Last Updated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary
- **Total Features**: 0
- **Active Tasks**: 0
- **Completed**: 0
- **In Progress**: 0

---

## Features

"""
        ledger_path.write_text(content)
        print("✅ Created new task ledger")
    
    # Scan for task files
    task_files = scan_task_files()
    
    if not task_files:
        print("❌ No task files found")
        return
    
    print(f"📁 Found {len(task_files)} task files")
    
    # Process each task file
    entries = []
    total_tasks = 0
    completed_tasks = 0
    in_progress = 0
    
    for task_file in sorted(task_files):
        entry, total, completed = create_ledger_entry(task_file)
        entries.append(entry)
        total_tasks += total
        completed_tasks += completed
        
        if 0 < completed < total:
            in_progress += 1
        
        print(f"  ✅ {task_file.stem}: {completed}/{total} tasks")
    
    # Update ledger
    content = ledger_path.read_text()
    
    # Update summary
    summary = f"""## Summary
- **Total Features**: {len(task_files)}
- **Active Tasks**: {total_tasks}
- **Completed**: {completed_tasks}
- **In Progress**: {in_progress}"""
    
    # Replace summary
    pattern = r'## Summary.*?(?=\n---)'
    content = re.sub(pattern, summary, content, flags=re.DOTALL)
    
    # Update timestamp
    pattern = r'(\*\*Last Updated\*\*: ).*?(\n)'
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = re.sub(pattern, rf"\g<1>{timestamp}\g<2>", content)
    
    # Add features if not already present
    for entry in entries:
        feature_match = re.search(r'### ([^\n]+)', entry)
        if feature_match:
            feature = feature_match.group(1)
            if f"### {feature}" not in content:
                # Add to features section
                features_end = content.find("## Features") + len("## Features\n\n")
                content = content[:features_end] + entry + content[features_end:]
    
    ledger_path.write_text(content)
    
    print(f"\n✅ Task ledger synced!")
    print(f"   Total features: {len(task_files)}")
    print(f"   Total tasks: {total_tasks}")
    print(f"   Completed: {completed_tasks} ({(completed_tasks/total_tasks*100):.1f}%)")

if __name__ == "__main__":
    sync_task_ledger()
