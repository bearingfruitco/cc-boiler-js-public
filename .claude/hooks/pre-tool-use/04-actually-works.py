#!/usr/bin/env python3
"""
Actually Works Protocol - Enforce testing before claiming fixes
Prevents the AI from saying "this should work" without verification
"""

import json
import sys
import re
from pathlib import Path

def check_for_untested_claims(content):
    """Check if AI is making untested claims about fixes"""
    
    # Red flag phrases that indicate untested code
    red_flags = [
        r"should\s+work\s+now",
        r"this\s+should\s+fix",
        r"i've\s+fixed\s+the\s+issue",
        r"try\s+it\s+now",
        r"the\s+logic\s+is\s+correct",
        r"i've\s+made\s+the\s+necessary\s+changes",
        r"that\s+ought\s+to\s+do\s+it",
        r"this\s+will\s+solve",
        r"should\s+be\s+working"
    ]
    
    violations = []
    for flag in red_flags:
        if re.search(flag, content, re.IGNORECASE):
            violations.append(flag.replace(r'\s+', ' '))
    
    return violations

def check_for_test_evidence(content):
    """Check if there's evidence of actual testing"""
    
    # Positive indicators of testing
    test_indicators = [
        r"i\s+tested",
        r"i\s+ran",
        r"i\s+verified",
        r"test\s+output",
        r"console\s+shows",
        r"result\s+was",
        r"confirmed\s+working"
    ]
    
    for indicator in test_indicators:
        if re.search(indicator, content, re.IGNORECASE):
            return True
    
    return False

def generate_testing_reminder():
    """Generate the Actually Works protocol reminder"""
    return """🛑 ACTUALLY WORKS PROTOCOL VIOLATION DETECTED

You appear to be claiming something works without testing it.

✅ The 30-Second Reality Check - Answer ALL with YES:
□ Did you run/build the code?
□ Did you trigger the exact feature you changed?
□ Did you see the expected result with your own observation?
□ Did you check for error messages?
□ Would you bet $100 this works?

💡 Required Actions:
1. Actually run the code
2. Test the specific feature
3. Verify the output
4. Only then claim it works

⏱️ Time Reality:
- Time saved skipping tests: 30 seconds
- Time wasted when it doesn't work: 30 minutes
- User trust lost: Immeasurable

Remember: "Should work" ≠ "Does work"
"""

def main():
    """Main hook logic"""
    try:
        # Read input from Claude Code
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool name
        tool_name = input_data.get('tool_name', '')
        
        # Only check on write operations that might contain claims
        if tool_name not in ['Write', 'Edit', 'MultiEdit']:
            # Not a write operation - continue normally
            sys.exit(0)
        
        # Extract content
        tool_input = input_data.get('tool_input', {})
        content = str(tool_input.get('content', '')) + str(tool_input.get('new_str', ''))
        
        # Skip if no content
        if not content:
            sys.exit(0)
        
        # Check for untested claims
        violations = check_for_untested_claims(content)
        
        if violations:
            # Check if there's test evidence
            has_test_evidence = check_for_test_evidence(content)
            
            if not has_test_evidence:
                # Log warning to stderr (will show in output)
                print(generate_testing_reminder(), file=sys.stderr)
        
        # This is a warning hook - always continue
        sys.exit(0)
        
    except Exception as e:
        # Non-blocking error - show to user but continue
        print(f"Actually works hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)  # Non-blocking error

if __name__ == "__main__":
    main()
