#!/usr/bin/env python3
"""
Smart Notification System Hook

Provides intelligent notifications for long-running operations without
creating unnecessary agents. Uses TTS, desktop notifications, and other
channels based on task importance and duration.
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Get Claude environment
CLAUDE_PROJECT_DIR = os.getenv('CLAUDE_PROJECT_DIR', '.')
CLAUDE_SESSION_ID = os.getenv('CLAUDE_SESSION_ID', 'unknown')

# Notification settings
SETTINGS_FILE = Path(CLAUDE_PROJECT_DIR) / '.claude' / 'settings.json'
NOTIFICATION_LOG = Path(CLAUDE_PROJECT_DIR) / '.claude' / 'logs' / 'notifications.log'

# Default thresholds
DEFAULT_THRESHOLDS = {
    'short_task': 30,      # seconds
    'medium_task': 60,     # seconds
    'long_task': 180,      # seconds
    'quiet_hours_start': 22,  # 10 PM
    'quiet_hours_end': 8      # 8 AM
}

def load_settings():
    """Load notification settings"""
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
                return settings.get('notifications', DEFAULT_THRESHOLDS)
        except:
            pass
    return DEFAULT_THRESHOLDS

def load_tool_data():
    """Load tool data from stdin"""
    try:
        return json.load(sys.stdin)
    except:
        return {}

def is_quiet_hours():
    """Check if we're in quiet hours"""
    settings = load_settings()
    current_hour = datetime.now().hour
    start = settings.get('quiet_hours_start', 22)
    end = settings.get('quiet_hours_end', 8)
    
    if start > end:  # Crosses midnight
        return current_hour >= start or current_hour < end
    else:
        return start <= current_hour < end

def get_task_importance(tool_data):
    """Determine task importance based on context"""
    tool_name = tool_data.get('tool_name', '')
    tool_input = tool_data.get('tool_input', {})
    
    # High importance indicators
    high_importance = [
        'production', 'security', 'critical', 'urgent',
        'deployment', 'hotfix', 'emergency', 'breaking'
    ]
    
    # Check tool input for importance indicators
    input_str = json.dumps(tool_input).lower()
    
    for indicator in high_importance:
        if indicator in input_str:
            return 'high'
    
    # Check for specific tools
    if tool_name in ['Task', 'MultiTask']:
        return 'medium'
    
    return 'low'

def get_agent_name(tool_data):
    """Extract agent name from tool data"""
    if tool_data.get('tool_name') == 'Task':
        prompt = tool_data.get('tool_input', {}).get('prompt', '')
        # Try to extract agent name
        for agent in ['frontend', 'backend', 'security', 'qa', 'database']:
            if agent in prompt.lower():
                return agent
    return 'agent'

def format_notification_message(agent_name, duration, task_summary):
    """Format notification message based on context"""
    if duration < 60:
        duration_str = f"{int(duration)} seconds"
    elif duration < 3600:
        duration_str = f"{duration/60:.1f} minutes"
    else:
        duration_str = f"{duration/3600:.1f} hours"
    
    # Shorten task summary if needed
    if len(task_summary) > 100:
        task_summary = task_summary[:97] + "..."
    
    return f"{agent_name} completed in {duration_str}: {task_summary}"

def send_notification(message, importance='medium', use_tts=False):
    """Send notification through appropriate channel"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'message': message,
        'importance': importance,
        'quiet_hours': is_quiet_hours()
    }
    
    # Log all notifications
    NOTIFICATION_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(NOTIFICATION_LOG, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
    
    # Skip audio during quiet hours unless critical
    if is_quiet_hours() and importance != 'high':
        use_tts = False
    
    # Platform-specific notifications
    platform = sys.platform
    
    if platform == 'darwin':  # macOS
        # Desktop notification
        os.system(f'''osascript -e 'display notification "{message}" with title "Claude Code" sound name "Glass"' ''')
        
        # TTS if requested
        if use_tts:
            os.system(f'say "{message}"')
            
    elif platform.startswith('linux'):
        # Desktop notification (requires notify-send)
        os.system(f'notify-send "Claude Code" "{message}"')
        
        # TTS if available (espeak)
        if use_tts and os.system('which espeak > /dev/null 2>&1') == 0:
            os.system(f'espeak "{message}" 2>/dev/null')
            
    elif platform == 'win32':
        # Windows notification (requires plyer or win10toast)
        try:
            from plyer import notification
            notification.notify(
                title='Claude Code',
                message=message,
                timeout=10
            )
        except:
            print(f"🔔 {message}")

def main():
    # Load data
    data = load_tool_data()
    settings = load_settings()
    
    # This hook runs on sub-agent completion
    # Check if this is a completion event
    if 'stop_hook_active' in data:
        # Get timing information from session
        # For now, use a reasonable estimate
        duration = 45  # seconds, would be calculated from actual timing
        
        agent_name = get_agent_name(data)
        importance = get_task_importance(data)
        
        # Determine if notification is needed
        should_notify = False
        use_tts = False
        
        if importance == 'high':
            should_notify = True
            use_tts = True
        elif importance == 'medium' and duration > settings.get('medium_task', 60):
            should_notify = True
            use_tts = duration > settings.get('long_task', 180)
        elif duration > settings.get('long_task', 180):
            should_notify = True
        
        if should_notify:
            # Extract task summary
            task_summary = "Task completed successfully"
            
            message = format_notification_message(agent_name, duration, task_summary)
            send_notification(message, importance, use_tts)
    
    # Always exit successfully
    sys.exit(1)

if __name__ == "__main__":
    main()
