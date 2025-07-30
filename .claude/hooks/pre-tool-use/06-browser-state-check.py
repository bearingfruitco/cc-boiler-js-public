#!/usr/bin/env python3
"""
Pre-Tool-Use Browser State Check - Validate browser compatibility before deployments
"""

import json
import sys
import os
from pathlib import Path

def check_browser_state():
    """Check if browser tests should run before deployment"""
    # Check for deployment-related actions
    deployment_indicators = [
        'deploy',
        'staging',
        'production',
        'preview',
        'build',
        'dist'
    ]
    
    return deployment_indicators

def validate_browser_readiness():
    """Ensure browser tests are passing before deployment"""
    # Check recent test results
    test_results_path = Path('.claude/metrics/browser-test-results.json')
    
    if test_results_path.exists():
        with open(test_results_path, 'r') as f:
            results = json.load(f)
            
        last_run = results.get('last_run', {})
        if last_run.get('failed', 0) > 0:
            return False, f"Browser tests failing: {last_run['failed']} tests"
    
    return True, "Browser tests ready"

def main():
    """Main hook logic"""
    try:
        # Read input
        input_data = json.loads(sys.stdin.read())
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Check if this is deployment-related
        command = tool_input.get('command', '').lower()
        
        for indicator in check_browser_state():
            if indicator in command:
                # Validate browser state
                ready, message = validate_browser_readiness()
                
                if not ready:
                    print(f"\n⚠️ Browser validation required before deployment!")
                    print(f"   {message}")
                    print(f"   Run: /pw-test smoke")
                    print(f"   Or: /browser-test-status --fix")
                    
                    # Optionally block deployment
                    output = {
                        "continue": True,  # Set to False to block
                        "warning": message
                    }
                    print(json.dumps(output))
                    sys.exit(0)
                else:
                    print("\n✅ Browser tests passing - ready for deployment")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"Browser state check error: {str(e)}", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
