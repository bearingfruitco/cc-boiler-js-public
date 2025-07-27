#!/usr/bin/env python3
"""
Smart Suggest Hook - Provides contextual command suggestions
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Context-based suggestions
CONTEXT_SUGGESTIONS = {
    "just_started": [
        "/sr - Resume previous work",
        "/help - Get help with commands",
        "/init-project - Start a new project"
    ],
    "editing_component": [
        "/vd - Validate design compliance",
        "/cc - Create a new component",
        "/test - Run component tests"
    ],
    "has_errors": [
        "/bt add - Track this bug",
        "/debug - Enter debug mode",
        "/help error - Get error help"
    ],
    "creating_feature": [
        "/prd - Create a PRD first",
        "/gt - Generate tasks",
        "/fw start - Start GitHub workflow"
    ],
    "idle_long": [
        "/checkpoint - Save your progress",
        "/status - Check current work",
        "/help - Need assistance?"
    ]
}

def get_context_from_message(message):
    """Determine context from the notification message"""
    message_lower = message.lower() if message else ""
    
    # Check various conditions
    if "permission" in message_lower:
        return "permission_needed"
    elif "error" in message_lower or "failed" in message_lower:
        return "has_errors"
    elif "idle" in message_lower or "waiting" in message_lower:
        return "idle_long"
    elif "started" in message_lower or "beginning" in message_lower:
        return "just_started"
    else:
        # Check recent activity if available
        try:
            session_file = Path(".claude/logs/session-summary.json")
            if session_file.exists():
                with open(session_file, "r") as f:
                    session_data = json.load(f)
                    
                # Analyze recent tools used
                tool_usage = session_data.get('tool_usage', {})
                if 'Write' in tool_usage or 'Edit' in tool_usage:
                    return "editing_component"
                elif 'Task' in tool_usage:
                    return "creating_feature"
        except:
            pass
        
        return "idle_long"  # Default

def format_suggestions(suggestions):
    """Format suggestions for display"""
    if not suggestions:
        return ""
    
    formatted = "\n💡 Suggested commands:\n"
    for suggestion in suggestions[:3]:  # Limit to 3 suggestions
        formatted += f"   • {suggestion}\n"
    
    return formatted

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract notification message
        message = input_data.get('message', '')
        
        # Determine context
        context = get_context_from_message(message)
        
        # Get relevant suggestions
        suggestions = CONTEXT_SUGGESTIONS.get(context, [])
        
        # Format suggestions
        suggestion_text = format_suggestions(suggestions)
        
        if suggestion_text:
            # Append suggestions to the notification
            sys.exit(0)
        else:
            # No suggestions - just continue
            sys.exit(0)
        
    except Exception as e:
        # Always output valid JSON even on error
        print(json.dumps({
            sys.exit(0)

if __name__ == '__main__':
    main()
    sys.exit(0)
