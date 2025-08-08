#!/usr/bin/env python3
"""
Handoff Prep Hook - Prepares handoff package when session ends
Creates a summary for the next developer or session
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def create_handoff_summary():
    """Create a handoff summary for the next session"""
    handoff_data = {
        "timestamp": datetime.now().isoformat(),
        "session_id": os.getenv('CLAUDE_SESSION_ID', 'unknown'),
        "work_summary": [],
        "next_steps": [],
        "warnings": []
    }
    
    # Check recent files modified
    recent_files = Path(".claude/state/recent-files.txt")
    if recent_files.exists():
        try:
            with open(recent_files, 'r') as f:
                files = [line.strip() for line in f.readlines()[-10:]]
                handoff_data["recent_files"] = files
        except:
            pass
    
    # Check for active tasks
    task_ledger = Path(".task-ledger.md")
    if task_ledger.exists():
        try:
            with open(task_ledger, 'r') as f:
                content = f.read()
                # Find in-progress tasks
                in_progress = []
                lines = content.split('\n')
                for line in lines:
                    if '[ ]' in line and 'In Progress' in line:
                        in_progress.append(line.strip())
                if in_progress:
                    handoff_data["active_tasks"] = in_progress[:5]
        except:
            pass
    
    # Check for uncommitted changes
    try:
        import subprocess
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            uncommitted_count = len(result.stdout.strip().split('\n'))
            handoff_data["warnings"].append(f"{uncommitted_count} uncommitted files")
    except:
        pass
    
    return handoff_data

def save_handoff_data(handoff_data):
    """Save handoff data to file"""
    handoff_dir = Path(".claude/handoff")
    handoff_dir.mkdir(parents=True, exist_ok=True)
    
    # Save to timestamped file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    handoff_file = handoff_dir / f"handoff_{timestamp}.json"
    
    with open(handoff_file, 'w') as f:
        json.dump(handoff_data, f, indent=2)
    
    # Also save as latest
    latest_file = handoff_dir / "latest.json"
    with open(latest_file, 'w') as f:
        json.dump(handoff_data, f, indent=2)
    
    return handoff_file

def main():
    """Main hook logic"""
    try:
        # Read input if provided
        input_data = {}
        if not sys.stdin.isatty():
            try:
                input_data = json.loads(sys.stdin.read())
            except:
                pass
        
        # Create handoff summary
        handoff_data = create_handoff_summary()
        
        # Save handoff data
        handoff_file = save_handoff_data(handoff_data)
        
        # Log handoff creation
        message = f"📋 Handoff package created: {handoff_file.name}\n"
        if handoff_data.get("active_tasks"):
            message += f"📌 {len(handoff_data['active_tasks'])} active tasks preserved\n"
        if handoff_data.get("warnings"):
            message += f"⚠️ Warnings: {', '.join(handoff_data['warnings'])}\n"
        
        print(message, file=sys.stderr)
        
        # Allow Claude to stop normally - exit with code 0
        sys.exit(0)
        
    except Exception as e:
        # Log error but still allow stop
        print(f"Handoff prep error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
