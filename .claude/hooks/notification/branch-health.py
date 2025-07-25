#!/usr/bin/env python3
"""
Branch Health Notification - Shows branch status in daily workflow
Integrates with existing notification system
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

def get_notification():
    """Generate branch health notification for display."""
    try:
        # Only show periodically (not every command)
        if not should_show_notification():
            return None
            
        # Gather branch info
        branch_info = gather_branch_info()
        if not branch_info:
            return None
            
        # Format notification
        return format_branch_notification(branch_info)
        
    except:
        # Never break workflow
        return None

def should_show_notification():
    """Check if we should show notification (throttled)."""
    try:
        # Check last shown time
        marker_file = Path('.claude/state/last-branch-notification.json')
        if marker_file.exists():
            data = json.loads(marker_file.read_text())
            last_shown = datetime.fromisoformat(data.get('timestamp'))
            
            # Only show every 2 hours
            if datetime.now() - last_shown < timedelta(hours=2):
                return False
        
        # Update marker
        marker_file.parent.mkdir(parents=True, exist_ok=True)
        marker_file.write_text(json.dumps({
            'timestamp': datetime.now().isoformat()
        }))
        
        return True
        
    except:
        return False

def gather_branch_info():
    """Gather current branch information."""
    info = {}
    
    try:
        # Current branch
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True
        )
        info['current_branch'] = result.stdout.strip()
        
        # Branch count
        result = subprocess.run(
            ['git', 'branch', '-r'],
            capture_output=True,
            text=True
        )
        info['total_branches'] = len(result.stdout.strip().split('\n'))
        
        # Check if main is stale
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%ar', 'origin/main'],
            capture_output=True,
            text=True
        )
        info['main_age'] = result.stdout.strip()
        
        # Modified files
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True
        )
        info['modified_count'] = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        
        return info
        
    except:
        return None

def format_branch_notification(info):
    """Format branch info as friendly notification."""
    lines = []
    
    # Only show if there's something noteworthy
    notifications = []
    
    # Check for stale main
    if 'day' in info.get('main_age', '') or 'week' in info.get('main_age', ''):
        notifications.append(f"📍 Main branch: {info['main_age']} (consider syncing)")
    
    # Check for uncommitted changes
    if info.get('modified_count', 0) > 5:
        notifications.append(f"📝 {info['modified_count']} files modified (consider committing)")
    
    # Check for many branches
    if info.get('total_branches', 0) > 10:
        notifications.append(f"🌿 {info['total_branches']} remote branches (consider cleanup)")
    
    if notifications:
        lines.append("\n💡 Branch Health Tips:")
        lines.extend([f"  {n}" for n in notifications])
        lines.append("  Run /branch-status for details")
        return '\n'.join(lines)
    
    return None

# Hook interface
def get_notification_message():
    """Called by notification system."""
    return get_notification()

if __name__ == "__main__":
    # Test mode
    notification = get_notification()
    if notification:
        print(notification)
