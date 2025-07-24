#!/usr/bin/env python3
"""
Smart Resume Enhancement Script
Adds task ledger integration to smart resume output
"""

import json
import sys
from pathlib import Path
import re
from datetime import datetime

def get_task_ledger_summary():
    """Extract summary from task ledger."""
    ledger_path = Path('.task-ledger.md')
    if not ledger_path.exists():
        return None
    
    try:
        content = ledger_path.read_text()
        
        # Extract summary stats
        features_match = re.search(r'\*\*Total Features\*\*: (\d+)', content)
        tasks_match = re.search(r'\*\*Active Tasks\*\*: (\d+)', content)
        completed_match = re.search(r'\*\*Completed\*\*: (\d+)', content)
        in_progress_match = re.search(r'\*\*In Progress\*\*: (\d+)', content)
        
        features = int(features_match.group(1)) if features_match else 0
        tasks = int(tasks_match.group(1)) if tasks_match else 0
        completed = int(completed_match.group(1)) if completed_match else 0
        in_progress = int(in_progress_match.group(1)) if in_progress_match else 0
        
        # Get current feature if on feature branch
        current_branch = get_current_branch()
        current_feature = None
        
        # Find feature matching branch
        feature_matches = re.findall(r'### ([^\n]+).*?**Branch**: `([^`]+)`', content, re.DOTALL)
        for feature, branch in feature_matches:
            if branch == current_branch:
                current_feature = feature
                break
        
        # Get progress for current feature
        current_progress = None
        if current_feature:
            pattern = rf'### {re.escape(current_feature)}.*?**Progress**: (\d+)/(\d+) tasks'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                current_progress = {
                    'completed': int(match.group(1)),
                    'total': int(match.group(2))
                }
        
        return {
            'features': features,
            'tasks': tasks,
            'completed': completed,
            'in_progress': in_progress,
            'current_feature': current_feature,
            'current_progress': current_progress,
            'percentage': round((completed / tasks * 100) if tasks > 0 else 0, 1)
        }
    except Exception as e:
        return None

def get_current_branch():
    """Get current git branch."""
    try:
        import subprocess
        result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                              capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return 'main'

def format_task_ledger_section(summary):
    """Format task ledger section for smart resume."""
    if not summary:
        return ""
    
    output = "\n## 📋 Task Ledger Status\n"
    
    # Overall stats
    output += f"**Total Progress**: {summary['completed']}/{summary['tasks']} tasks ({summary['percentage']}%)\n"
    output += f"**Active Features**: {summary['in_progress']} of {summary['features']}\n"
    
    # Current feature
    if summary['current_feature'] and summary['current_progress']:
        progress = summary['current_progress']
        pct = round((progress['completed'] / progress['total'] * 100) if progress['total'] > 0 else 0)
        output += f"\n**Current Feature**: {summary['current_feature']}\n"
        output += f"Progress: {progress['completed']}/{progress['total']} tasks ({pct}%)\n"
        
        # Visual progress bar
        filled = int(pct / 10)
        empty = 10 - filled
        bar = "█" * filled + "░" * empty
        output += f"[{bar}] {pct}%\n"
    
    output += "\n**Quick Actions**:\n"
    output += "- View full ledger: `/tl`\n"
    if summary['current_feature']:
        output += f"- Continue tasks: `/pt {summary['current_feature']}`\n"
    output += "- See task board: `/tb`\n"
    
    return output

def main():
    """Enhance smart resume with task ledger info."""
    # Get task ledger summary
    summary = get_task_ledger_summary()
    
    if summary:
        # Output the task ledger section
        section = format_task_ledger_section(summary)
        if section:
            print(section)

if __name__ == "__main__":
    main()
