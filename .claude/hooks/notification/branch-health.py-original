#!/usr/bin/env python3
"""
Branch Health Notification - Shows branch status in daily workflow
Monitors git branch health and provides timely notifications
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

def should_show_notification():
    """Check if we should show notification (throttled)."""
    try:
        # Check last shown time
        marker_file = Path('.claude/state/last-branch-notification.json')
        if marker_file.exists():
            with open(marker_file, 'r') as f:
                data = json.load(f)
                last_shown = datetime.fromisoformat(data.get('timestamp'))
                
                # Only show every 2 hours
                if datetime.now() - last_shown < timedelta(hours=2):
                    return False
        
        # Update marker
        marker_file.parent.mkdir(parents=True, exist_ok=True)
        with open(marker_file, 'w') as f:
            json.dump({'timestamp': datetime.now().isoformat()}, f)
        
        return True
        
    except:
        return True  # Show if we can't determine

def gather_branch_info():
    """Gather current branch information."""
    info = {}
    
    try:
        # Current branch
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True,
            stderr=subprocess.DEVNULL
        )
        info['current_branch'] = result.stdout.strip()
        
        # Branch count
        result = subprocess.run(
            ['git', 'branch', '-r'],
            capture_output=True,
            text=True,
            stderr=subprocess.DEVNULL
        )
        branches = result.stdout.strip().split('\n') if result.stdout.strip() else []
        info['total_branches'] = len(branches)
        
        # Check if main is stale
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%ar', 'origin/main'],
            capture_output=True,
            text=True,
            stderr=subprocess.DEVNULL
        )
        info['main_age'] = result.stdout.strip()
        
        # Modified files
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            stderr=subprocess.DEVNULL
        )
        modified = result.stdout.strip().split('\n') if result.stdout.strip() else []
        info['modified_count'] = len(modified)
        
        return info
        
    except:
        return None

def format_branch_notification(info):
    """Format branch info as friendly notification."""
    if not info:
        return None
    
    # Only show if there's something noteworthy
    notifications = []
    
    # Check for stale main
    main_age = info.get('main_age', '')
    if any(period in main_age for period in ['day', 'week', 'month']):
        notifications.append(f"📍 Main branch: {main_age} (consider syncing)")
    
    # Check for uncommitted changes
    modified = info.get('modified_count', 0)
    if modified > 5:
        notifications.append(f"📝 {modified} files modified (consider committing)")
    
    # Check for many branches
    branches = info.get('total_branches', 0)
    if branches > 10:
        notifications.append(f"🌿 {branches} remote branches (consider cleanup)")
    
    if notifications:
        message = "💡 Branch Health Tips:\n"
        for n in notifications:
            message += f"  {n}\n"
        message += "  Run /branch-status for details"
        return message
    
    return None

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
        
        # Check if we should show notification (throttled)
        if should_show_notification():
            # Gather branch information
            branch_info = gather_branch_info()
            
            # Format notification if there's something to show
            message = format_branch_notification(branch_info)
            
            if message:
                # Output notification to stderr
                print(message, file=sys.stderr)
        
        # Notification hooks just exit normally
        sys.exit(1)
        
    except Exception as e:
        # On error, log to stderr and exit with error code
        print(f"Branch health error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
