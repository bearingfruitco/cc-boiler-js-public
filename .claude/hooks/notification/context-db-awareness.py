#!/usr/bin/env python3
"""
Context DB Awareness - Monitors context database usage and suggests relevant context
Helps ensure AI agents have access to necessary context information
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def scan_context_database():
    """Scan for available context files"""
    context_files = []
    
    # Check standard context locations
    context_dirs = [
        Path('.claude/context'),
        Path('context'),
        Path('.context'),
        Path('docs/context')
    ]
    
    for context_dir in context_dirs:
        if context_dir.exists():
            # Find JSON context files
            for json_file in context_dir.rglob('*.json'):
                if not any(ignore in str(json_file) for ignore in ['.backup', '.tmp', 'node_modules']):
                    context_files.append({
                        'path': str(json_file),
                        'name': json_file.stem,
                        'size': json_file.stat().st_size,
                        'modified': datetime.fromtimestamp(json_file.stat().st_mtime).isoformat()
                    })
    
    return context_files

def check_if_context_needed():
    """Check if current work might need context database"""
    indicators = []
    
    # Check recent files for context indicators
    recent_files_path = Path('.claude/state/recent-files.txt')
    if recent_files_path.exists():
        try:
            with open(recent_files_path, 'r') as f:
                recent_files = [line.strip() for line in f.readlines()[-10:]]
                
                # Look for files that might need context
                for file_path in recent_files:
                    if 'brand' in file_path.lower():
                        indicators.append('brand-related')
                    if 'database' in file_path.lower() or 'schema' in file_path.lower():
                        indicators.append('database-related')
                    if 'config' in file_path.lower():
                        indicators.append('configuration-related')
        except:
            pass
    
    # Check current task
    current_task_path = Path('.claude/team/current-task.md')
    if current_task_path.exists():
        try:
            task_content = current_task_path.read_text().lower()
            if 'brand' in task_content:
                indicators.append('brand-task')
            if 'database' in task_content or 'schema' in task_content:
                indicators.append('database-task')
        except:
            pass
    
    return indicators

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = {}
        if not sys.stdin.isatty():
            try:
                input_data = json.loads(sys.stdin.read())
            except:
                pass
        
        # Check if context might be needed
        indicators = check_if_context_needed()
        
        if indicators:
            # Scan available context
            context_files = scan_context_database()
            
            if context_files:
                # Check when we last notified about context
                notification_file = Path('.claude/state/last-context-notification.json')
                should_notify = True
                
                if notification_file.exists():
                    try:
                        with open(notification_file, 'r') as f:
                            last_data = json.load(f)
                            last_time = datetime.fromisoformat(last_data.get('timestamp'))
                            # Only notify once per hour
                            if (datetime.now() - last_time).seconds < 3600:
                                should_notify = False
                    except:
                        pass
                
                if should_notify:
                    # Create notification
                    message = "💡 Context Database Available\n"
                    message += f"Found {len(context_files)} context files that might help:\n"
                    
                    # Show relevant files based on indicators
                    relevant_files = []
                    for file_info in context_files[:5]:  # Show max 5
                        name = file_info['name'].lower()
                        if any(ind in indicators for ind in ['brand-related', 'brand-task']) and 'brand' in name:
                            relevant_files.append(file_info)
                        elif any(ind in indicators for ind in ['database-related', 'database-task']) and ('database' in name or 'schema' in name):
                            relevant_files.append(file_info)
                        elif 'config' in name:
                            relevant_files.append(file_info)
                    
                    if relevant_files:
                        for file_info in relevant_files[:3]:
                            message += f"  • {file_info['name']}\n"
                        message += "\nUse /context-db list to see all available context"
                        
                        # Update notification timestamp
                        notification_file.parent.mkdir(parents=True, exist_ok=True)
                        with open(notification_file, 'w') as f:
                            json.dump({'timestamp': datetime.now().isoformat()}, f)
                        
                        # Output notification to stderr
                        print(message, file=sys.stderr)
        
        # Notification hooks just exit normally
        sys.exit(0)
        
    except Exception as e:
        # On error, log to stderr and exit with error code
        print(f"Context DB awareness error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
