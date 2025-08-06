#!/usr/bin/env python3
"""
User Prompt Submit Hook - Inject browser context when user mentions UI issues
"""

import json
import sys
import os
from pathlib import Path

# Keywords that suggest browser/UI issues
UI_KEYWORDS = [
    'not working',
    'broken',
    'error',
    'console',
    'click',
    'button',
    'form',
    'submit',
    'render',
    'display',
    'style',
    'css',
    'javascript',
    'browser',
    'chrome',
    'safari',
    'firefox',
    'mobile',
    'responsive',
    'viewport'
]

def contains_ui_issue(prompt):
    """Check if prompt mentions UI/browser issues"""
    prompt_lower = prompt.lower()
    return any(keyword in prompt_lower for keyword in UI_KEYWORDS)

def get_browser_context():
    """Get relevant browser context to inject"""
    context_parts = []
    
    # Check for recent console errors
    console_log = Path('.claude/metrics/console-errors.json')
    if console_log.exists():
        with open(console_log, 'r') as f:
            data = json.load(f)
            if data.get('recent_errors'):
                context_parts.append(f"Recent browser errors: {data['recent_errors'][:3]}")
    
    # Check browser test status
    test_status = Path('.claude/metrics/browser-test-results.json')
    if test_status.exists():
        with open(test_status, 'r') as f:
            data = json.load(f)
            last_run = data.get('last_run', {})
            if last_run.get('failed', 0) > 0:
                context_parts.append(f"Browser tests failing: {last_run['failed']} tests")
    
    # Get viewport info
    context_parts.append("Browser testing available with /pw commands")
    
    return "\n".join(context_parts) if context_parts else None

def main():
    """Main hook logic"""
    try:
        # Read input
        input_data = json.loads(sys.stdin.read())
        prompt = input_data.get('prompt', '')
        
        # Check if browser context might be helpful
        if contains_ui_issue(prompt):
            browser_context = get_browser_context()
            
            if browser_context:
                # Inject context
                enhanced_prompt = f"{prompt}\n\n[Browser Context]\n{browser_context}"
                
                # Also suggest browser commands
                print("\n💡 Browser testing commands available:")
                print("   • /pw-debug - Debug the issue")
                print("   • /pw-console - Check console errors")
                print("   • /pw-verify - Verify component rendering")
                
                # Output enhanced prompt
                output = {
                    "prompt": enhanced_prompt,
                    "continue": True
                }
                print(json.dumps(output))
                sys.exit(0)
        
        # Continue normally
        sys.exit(0)
        
    except Exception as e:
        print(f"Browser context injection error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
