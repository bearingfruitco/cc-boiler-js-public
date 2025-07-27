#!/usr/bin/env python3
"""
Task Ledger Updater Hook - Persistent Task Tracking
Maintains .task-ledger.md as a single source of truth for all tasks

Complements existing systems:
- Enhances /ts and /tb with persistent state
- Links tasks to GitHub issues automatically
- Tracks progress across sessions
- Integrates with existing state saves
"""

import json
import sys
import re
from datetime import datetime
from pathlib import Path
import subprocess

def main():
    """Main hook entry point following Claude Code specification."""
    try:
        # Read hook payload from stdin
        payload = json.loads(sys.stdin.read())
        
        # Extract command information
        tool_name = payload.get('tool_name', '')
        tool_input = payload.get('tool_input', {})
        tool_output = payload.get('tool_output', {})
        
        # Only process specific tools that generate or modify tasks
        task_tools = ['Write', 'Edit', 'MultiEdit']
        if tool_name not in task_tools:
            sys.exit(0)
        
        # Check if this is a task-related file operation
        file_path = tool_input.get('path', tool_input.get('file_path', ''))
        if not is_task_related_file(file_path):
            sys.exit(0)
        
        # Update task ledger based on the operation
        update_task_ledger(file_path, tool_name, tool_input, tool_output)
        
        # PostToolUse hooks just exit normally
        sys.exit(0)
        
    except Exception as e:
        # Non-blocking - log error but don't fail
        print(f"Task ledger update error: {str(e)}", file=sys.stderr)
        sys.exit(0)

def is_task_related_file(file_path):
    """Check if the file path is task-related."""
    if not file_path:
        return False
    
    # Task file patterns
    task_patterns = [
        r'docs/project/features/.*-tasks\.md$',
        r'docs/project/features/.*-PRD\.md$',
        r'PRPs/active/.*\.md$'
    ]
    
    return any(re.search(pattern, file_path) for pattern in task_patterns)

def update_task_ledger(file_path, tool_name, tool_input, tool_output):
    """Update the task ledger based on file operations."""
    ledger_path = Path('.task-ledger.md')
    
    # Initialize ledger if it doesn't exist
    if not ledger_path.exists():
        initialize_ledger(ledger_path)
    
    # Determine the type of update needed
    if '-tasks.md' in file_path:
        # Task file was created or modified
        feature = extract_feature_name(file_path)
        if feature:
            if tool_name == 'Write' and not Path(file_path).exists():
                # New task file created
                add_feature_to_ledger(ledger_path, feature, file_path)
            else:
                # Task file updated
                update_task_progress(ledger_path, feature, file_path)
    
    elif '-PRD.md' in file_path and tool_name == 'Write':
        # PRD created - prepare ledger entry
        feature = extract_feature_name(file_path)
        if feature:
            prepare_feature_entry(ledger_path, feature)

def initialize_ledger(ledger_path):
    """Create initial task ledger file."""
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

def extract_feature_name(file_path):
    """Extract feature name from file path."""
    match = re.search(r'features/([^/]+?)(?:-tasks|-PRD)?\.md$', file_path)
    if match:
        return match.group(1)
    
    # Try PRP pattern
    match = re.search(r'PRPs/active/([^/]+?)\.md$', file_path)
    if match:
        return match.group(1)
    
    return None

def add_feature_to_ledger(ledger_path, feature, task_file):
    """Add a new feature to the task ledger."""
    content = ledger_path.read_text()
    
    # Check if feature already exists
    if f"### {feature}" in content:
        # Update existing entry
        update_task_progress(ledger_path, feature, task_file)
        return
    
    # Get current branch and issue info
    branch = get_current_branch()
    issue_info = extract_issue_from_branch(branch)
    
    # Count tasks in the file
    task_count = count_tasks_in_file(task_file)
    
    # Create new feature entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = f"""### {feature}

**Created**: {timestamp}
**Issue**: {issue_info}
**Branch**: `{branch}`
**Status**: 📋 Generated
**Progress**: 0/{task_count} tasks

**Files**:
- Tasks: `{task_file}`
- PRD: `docs/project/features/{feature}-PRD.md`
- Tests: `tests/{feature}/`

**Quick Actions**:
- Process tasks: `/pt {feature}`
- View board: `/tb`
- Check status: `/ts`

---

"""
    
    # Insert before the first feature or at the end
    features_section = content.find("## Features")
    if features_section >= 0:
        # Find the end of the Features section header
        insert_pos = content.find("\n", features_section) + 1
        # Find if there are any existing features
        next_feature = content.find("###", insert_pos)
        if next_feature >= 0:
            # Insert before the first feature
            content = content[:next_feature] + new_entry + content[next_feature:]
        else:
            # Append at the end
            content = content + new_entry
    else:
        # Append at the end
        content = content + new_entry
    
    # Update summary
    content = update_ledger_summary(content)
    
    ledger_path.write_text(content)
    
    # Log update for visibility
    print(f"📋 Added '{feature}' to task ledger ({task_count} tasks)", file=sys.stderr)

def update_task_progress(ledger_path, feature, task_file):
    """Update task progress for a feature."""
    content = ledger_path.read_text()
    
    # Count completed tasks
    completed = count_completed_tasks(task_file)
    total = count_tasks_in_file(task_file)
    
    # Calculate status
    if completed == 0:
        status = "📋 Generated"
    elif completed == total:
        status = "✅ Completed"
    else:
        status = "🔄 In Progress"
        
    # Update the feature section
    pattern = rf"(### {feature}.*?**Progress**: )\d+/\d+( tasks)"
    replacement = rf"\g<1>{completed}/{total}\g<2>"
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Update status
    pattern = rf"(### {feature}.*?**Status**: ).*?(\n)"
    replacement = rf"\g<1>{status}\g<2>"
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Update timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pattern = r"(\*\*Last Updated\*\*: ).*?(\n)"
    replacement = rf"\g<1>{timestamp}\g<2>"
    content = re.sub(pattern, replacement, content)
    
    # Update summary
    content = update_ledger_summary(content)
    
    ledger_path.write_text(content)

def prepare_feature_entry(ledger_path, feature):
    """Prepare a feature entry when PRD is created."""
    content = ledger_path.read_text()
    
    # Check if feature already exists
    if f"### {feature}" in content:
        return
    
    # Add placeholder entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    branch = get_current_branch()
    issue_info = extract_issue_from_branch(branch)
    
    placeholder = f"""### {feature}

**Created**: {timestamp}
**Issue**: {issue_info}
**Branch**: `{branch}`
**Status**: 📝 PRD Created
**Progress**: Awaiting task generation

**Files**:
- PRD: `docs/project/features/{feature}-PRD.md`

**Next Step**: Generate tasks with `/gt {feature}`

---

"""
    
    # Insert the placeholder
    features_section = content.find("## Features")
    if features_section >= 0:
        insert_pos = content.find("\n", features_section) + 1
        next_feature = content.find("###", insert_pos)
        if next_feature >= 0:
            content = content[:next_feature] + placeholder + content[next_feature:]
        else:
            content = content + placeholder
    else:
        content = content + placeholder
    
    ledger_path.write_text(content)

def update_ledger_summary(content):
    """Update the summary section of the ledger."""
    # Count features and tasks
    features = len(re.findall(r'^### ', content, re.MULTILINE))
    
    # Count task states
    total_tasks = 0
    completed_tasks = 0
    
    # Parse progress from each feature
    progress_matches = re.findall(r'\*\*Progress\*\*: (\d+)/(\d+) tasks', content)
    for completed, total in progress_matches:
        completed_tasks += int(completed)
        total_tasks += int(total)
    
    in_progress = len(re.findall(r'\*\*Status\*\*: 🔄 In Progress', content))
    
    # Update summary section
    summary = f"""## Summary
- **Total Features**: {features}
- **Active Tasks**: {total_tasks}
- **Completed**: {completed_tasks}
- **In Progress**: {in_progress}"""
    
    # Replace old summary
    pattern = r'## Summary.*?(?=\n---)'
    content = re.sub(pattern, summary, content, flags=re.DOTALL)
    
    return content

def count_tasks_in_file(filepath):
    """Count total tasks in a task file."""
    try:
        path = Path(filepath)
        if not path.exists():
            return 0
        
        content = path.read_text()
        # Count task checkboxes
        total = len(re.findall(r'^\s*- \[[ x]\]', content, re.MULTILINE))
        return total
    except:
        return 0

def count_completed_tasks(filepath):
    """Count completed tasks in a task file."""
    try:
        path = Path(filepath)
        if not path.exists():
            return 0
        
        content = path.read_text()
        # Count completed checkboxes
        completed = len(re.findall(r'^\s*- \[x\]', content, re.MULTILINE))
        return completed
    except:
        return 0

def get_current_branch():
    """Get current git branch name."""
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

if __name__ == "__main__":
    main()
