#!/usr/bin/env python3
"""
TDD Workflow Suggester - Suggests TDD when user is starting implementation
UserPromptSubmit hook following official documentation
"""

import json
import sys
import re

def main():
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read())
        
        # Extract prompt from UserPromptSubmit event
        prompt = input_data.get('prompt', '').lower()
        
        # Patterns that indicate starting implementation
        implementation_patterns = [
            r'create.*component',
            r'implement.*feature',
            r'build.*form',
            r'add.*functionality',
            r'make.*work',
            r'code.*for',
            r'write.*code',
            r'start.*coding',
            r'begin.*implementation'
        ]
        
        # Check if prompt suggests implementation
        is_implementation = any(re.search(pattern, prompt) for pattern in implementation_patterns)
        
        if not is_implementation:
            # Not about implementation, continue normally
            sys.exit(0)
        
        # Check if tests are mentioned
        has_test_mention = any(word in prompt for word in ['test', 'tdd', 'spec'])
        
        if has_test_mention:
            # User already thinking about tests
            sys.exit(0)
        
        # Extract potential feature name
        feature_match = re.search(r'(?:create|implement|build|add)\s+(?:a\s+)?(\w+)', prompt)
        feature_name = feature_match.group(1) if feature_match else "the feature"
        
        # Output TDD suggestion to stderr (will show in conversation)
        tdd_context = f"\n💡 TDD Suggestion: Consider writing tests first for {feature_name}.\n"
        tdd_context += "Use: /tdd-workflow " + feature_name + "\n"
        tdd_context += "This will:\n"
        tdd_context += "1. Generate test templates from requirements\n"
        tdd_context += "2. Run tests (RED phase)\n"
        tdd_context += "3. Guide implementation (GREEN phase)\n"
        tdd_context += "4. Enable safe refactoring\n"
        
        print(tdd_context, file=sys.stderr)
        
        # UserPromptSubmit hooks just exit
        sys.exit(0)
        
    except Exception as e:
        # Don't block on errors - log to stderr
        print(f"TDD suggester error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
