#!/usr/bin/env python3
"""
Team Aware - Monitors team collaboration and provides relevant notifications
Tracks who's working on what and suggests coordination
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

def get_team_activity():
    """Get recent team activity from various sources"""
    activity = {
        'active_users': [],
        'recent_changes': [],
        'potential_conflicts': [],
        'handoffs': []
    }
    
    # Check team directory
    team_dir = Path('.claude/team')
    if team_dir.exists():
        # Look for user activity markers
        for user_file in team_dir.glob('*.json'):
            if user_file.stem.startswith('user-'):
                try:
                    with open(user_file, 'r') as f:
                        user_data = json.load(f)
                        last_active = datetime.fromisoformat(user_data.get('last_active', ''))
                        if (datetime.now() - last_active) < timedelta(hours=8):
                            activity['active_users'].append({
                                'name': user_data.get('name', 'Unknown'),
                                'working_on': user_data.get('current_file', 'Unknown'),
                                'last_active': last_active.isoformat()
                            })
                except:
                    pass
        
        # Check for handoff notes
        handoff_file = team_dir / 'handoff.md'
        if handoff_file.exists():
            try:
                if (datetime.now() - datetime.fromtimestamp(handoff_file.stat().st_mtime)) < timedelta(hours=24):
                    activity['handoffs'].append({
                        'file': str(handoff_file),
                        'age': (datetime.now() - datetime.fromtimestamp(handoff_file.stat().st_mtime)).seconds // 3600
                    })
            except:
                pass
    
    # Check for potential conflicts via git
    try:
        import subprocess
        
        # Get files modified by others
        result = subprocess.run(
            ['git', 'log', '--since=8.hours.ago', '--name-only', '--pretty=format:', '--author-invert-grep'],
            capture_output=True,
            text=True,
            stderr=subprocess.DEVNULL
        )
        
        if result.stdout:
            other_changes = [f for f in result.stdout.strip().split('\n') if f]
            
            # Check if we're also working on these files
            recent_files_path = Path('.claude/state/recent-files.txt')
            if recent_files_path.exists():
                try:
                    with open(recent_files_path, 'r') as f:
                        our_files = set(line.strip() for line in f.readlines())
                        
                        conflicts = set(other_changes) & our_files
                        if conflicts:
                            activity['potential_conflicts'] = list(conflicts)[:5]  # Max 5
                except:
                    pass
    except:
        pass
    
    return activity

def check_collaboration_needs():
    """Check if collaboration or coordination is needed"""
    needs = []
    
    # Check if working on shared components
    shared_components = ['Header', 'Footer', 'Navigation', 'Layout', 'Auth']
    recent_files_path = Path('.claude/state/recent-files.txt')
    
    if recent_files_path.exists():
        try:
            with open(recent_files_path, 'r') as f:
                recent_files = [line.strip() for line in f.readlines()[-20:]]
                
                for shared in shared_components:
                    if any(shared in f for f in recent_files):
                        needs.append(f"working-on-shared: {shared}")
        except:
            pass
    
    # Check if PR is open
    try:
        import subprocess
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True,
            stderr=subprocess.DEVNULL
        )
        
        if result.stdout.strip() != 'main':
            # Check for PR
            pr_result = subprocess.run(
                ['gh', 'pr', 'status', '--json', 'number'],
                capture_output=True,
                text=True,
                stderr=subprocess.DEVNULL
            )
            
            if pr_result.stdout:
                needs.append("has-open-pr")
    except:
        pass
    
    return needs

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
        
        # Check if we should show team notifications (throttled)
        team_marker = Path('.claude/state/last-team-notification.json')
        should_notify = True
        
        if team_marker.exists():
            try:
                with open(team_marker, 'r') as f:
                    last_notify = json.load(f)
                    last_time = datetime.fromisoformat(last_notify.get('timestamp'))
                    # Notify every 2 hours max
                    if (datetime.now() - last_time).seconds < 7200:
                        should_notify = False
            except:
                pass
        
        if should_notify:
            # Get team activity
            activity = get_team_activity()
            needs = check_collaboration_needs()
            
            notifications = []
            
            # Check for handoffs
            if activity['handoffs']:
                notifications.append({
                    'type': 'handoff',
                    'message': f"Handoff note available ({activity['handoffs'][0]['age']}h old)"
                })
            
            # Check for conflicts
            if activity['potential_conflicts']:
                notifications.append({
                    'type': 'conflict',
                    'message': f"Potential conflicts in {len(activity['potential_conflicts'])} files"
                })
            
            # Check for active team members
            if len(activity['active_users']) > 1:
                notifications.append({
                    'type': 'collaboration',
                    'message': f"{len(activity['active_users'])} team members active"
                })
            
            # Check for shared component work
            shared_work = [n for n in needs if n.startswith('working-on-shared')]
            if shared_work:
                component = shared_work[0].split(': ')[1]
                notifications.append({
                    'type': 'shared',
                    'message': f"Working on shared component: {component}"
                })
            
            if notifications:
                # Pick most important notification
                priority = {'conflict': 0, 'handoff': 1, 'shared': 2, 'collaboration': 3}
                notifications.sort(key=lambda n: priority.get(n['type'], 4))
                
                notification = notifications[0]
                
                # Create message
                emoji_map = {
                    'handoff': '📋',
                    'conflict': '⚠️',
                    'collaboration': '👥',
                    'shared': '🔗'
                }
                
                message = f"{emoji_map.get(notification['type'], '💬')} Team Activity\n"
                message += f"{notification['message']}\n"
                
                if notification['type'] == 'handoff':
                    message += "Run /handoff to view notes"
                elif notification['type'] == 'conflict':
                    message += "Run /team-status to coordinate"
                elif notification['type'] == 'shared':
                    message += "Consider syncing with team"
                
                # Update marker
                team_marker.parent.mkdir(parents=True, exist_ok=True)
                with open(team_marker, 'w') as f:
                    json.dump({'timestamp': datetime.now().isoformat()}, f)
                
                # Output notification to stderr
                print(message, file=sys.stderr)
        
        # Notification hooks just exit normally
        sys.exit(0)
        
    except Exception as e:
        # On error, log to stderr and exit with error code
        print(f"Team aware error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
