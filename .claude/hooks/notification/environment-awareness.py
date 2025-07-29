#!/usr/bin/env python3
"""
Environment Awareness Hook - Shows current environment in notifications
Reminds users of their current environment to prevent mistakes
"""

import json
import sys
import os

def main():
    """Show environment awareness in notifications"""
    try:
        # Get current environment
        current_env = os.environ.get('NODE_ENV', 'development')
        
        # Only show warnings for non-development environments
        if current_env != 'development':
            env_emoji = '🟧' if current_env == 'staging' else '🔴'
            
            notification = {
                "type": "info",
                "message": f"{env_emoji} Current Environment: {current_env.upper()}\n"
                          f"Be careful with operations in {current_env}!"
            }
            
            # Extra warning for production
            if current_env == 'production':
                notification["message"] += "\n⚠️  Production mode active - destructive operations blocked"
            
            print(json.dumps(notification))
        
    except Exception as e:
        # Silent fail - don't disrupt workflow
        pass

if __name__ == '__main__':
    main()
