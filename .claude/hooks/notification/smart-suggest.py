#!/usr/bin/env python3
"""
Smart Suggest - Provides intelligent suggestions based on current context
Analyzes work patterns and suggests helpful commands or actions
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

def analyze_current_context():
    """Analyze current work context for smart suggestions"""
    context = {
        'recent_files': [],
        'current_task': None,
        'work_duration': 0,
        'last_test': None,
        'last_commit': None,
        'errors_seen': False
    }
    
    # Get recent files
    recent_files_path = Path('.claude/state/recent-files.txt')
    if recent_files_path.exists():
        try:
            with open(recent_files_path, 'r') as f:
                context['recent_files'] = [line.strip() for line in f.readlines()[-10:]]
        except:
            pass
    
    # Check current task
    current_task_path = Path('.claude/team/current-task.md')
    if current_task_path.exists():
        try:
            context['current_task'] = current_task_path.read_text().strip()[:100]
        except:
            pass
    
    # Check work duration
    session_start = Path('.claude/state/session-start.json')
    if session_start.exists():
        try:
            with open(session_start, 'r') as f:
                start_data = json.load(f)
                start_time = datetime.fromisoformat(start_data.get('timestamp'))
                context['work_duration'] = (datetime.now() - start_time).seconds // 60  # minutes
        except:
            pass
    
    # Check last test run
    test_marker = Path('.claude/state/last-test-run.json')
    if test_marker.exists():
        try:
            with open(test_marker, 'r') as f:
                test_data = json.load(f)
                last_test = datetime.fromisoformat(test_data.get('timestamp'))
                context['last_test'] = (datetime.now() - last_test).seconds // 60  # minutes ago
        except:
            pass
    
    # Check for recent errors
    error_log = Path('.claude/logs/errors.log')
    if error_log.exists():
        try:
            # Check if errors in last 10 minutes
            ten_min_ago = datetime.now() - timedelta(minutes=10)
            if error_log.stat().st_mtime > ten_min_ago.timestamp():
                context['errors_seen'] = True
        except:
            pass
    
    return context

def generate_smart_suggestions(context):
    """Generate suggestions based on context"""
    suggestions = []
    
    # Suggest break if working for long time
    if context['work_duration'] > 90:
        suggestions.append({
            'type': 'wellness',
            'message': "You've been working for over 90 minutes",
            'action': "Consider taking a break 🧘"
        })
    
    # Suggest testing if haven't tested recently
    if context['last_test'] is None or context['last_test'] > 30:
        if any('.tsx' in f or '.ts' in f for f in context['recent_files']):
            suggestions.append({
                'type': 'quality',
                'message': "Haven't run tests in a while",
                'action': "Run /test to verify your changes"
            })
    
    # Suggest commit if many files changed
    if len(context['recent_files']) > 5:
        suggestions.append({
            'type': 'workflow',
            'message': f"Modified {len(context['recent_files'])} files",
            'action': "Consider committing with /safe-commit"
        })
    
    # Suggest error help if errors seen
    if context['errors_seen']:
        suggestions.append({
            'type': 'help',
            'message': "Recent errors detected",
            'action': "Run /error-recovery for assistance"
        })
    
    # Suggest validation for component files
    component_files = [f for f in context['recent_files'] if any(ext in f for ext in ['.tsx', '.jsx'])]
    if component_files:
        suggestions.append({
            'type': 'validation',
            'message': "Component changes detected",
            'action': "Run /validate-design to check compliance"
        })
    
    return suggestions

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
        
        # Check if we should show suggestions (throttled)
        suggest_marker = Path('.claude/state/last-smart-suggest.json')
        should_suggest = True
        
        if suggest_marker.exists():
            try:
                with open(suggest_marker, 'r') as f:
                    last_suggest = json.load(f)
                    last_time = datetime.fromisoformat(last_suggest.get('timestamp'))
                    # Suggest every 20 minutes max
                    if (datetime.now() - last_time).seconds < 1200:
                        should_suggest = False
            except:
                pass
        
        if should_suggest:
            # Analyze context
            context = analyze_current_context()
            
            # Generate suggestions
            suggestions = generate_smart_suggestions(context)
            
            if suggestions:
                # Pick the most relevant suggestion
                # Prioritize: errors > quality > workflow > wellness
                priority_order = {'help': 0, 'quality': 1, 'validation': 2, 'workflow': 3, 'wellness': 4}
                suggestions.sort(key=lambda s: priority_order.get(s['type'], 5))
                
                suggestion = suggestions[0]
                
                # Create notification
                emoji_map = {
                    'wellness': '🧘',
                    'quality': '🧪',
                    'workflow': '📝',
                    'help': '🆘',
                    'validation': '✅'
                }
                
                message = f"{emoji_map.get(suggestion['type'], '💡')} Smart Suggestion\n"
                message += f"{suggestion['message']}\n"
                message += f"→ {suggestion['action']}"
                
                # Update marker
                suggest_marker.parent.mkdir(parents=True, exist_ok=True)
                with open(suggest_marker, 'w') as f:
                    json.dump({'timestamp': datetime.now().isoformat()}, f)
                
                # Output notification to stderr
                print(message, file=sys.stderr)
        
        # Notification hooks just exit normally
        sys.exit(0)
        
    except Exception as e:
        # On error, log to stderr and exit with error code
        print(f"Smart suggest error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
