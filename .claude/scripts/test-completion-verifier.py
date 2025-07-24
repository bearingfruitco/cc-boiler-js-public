#!/usr/bin/env python3
"""
Test script for completion verifier hook
"""

import json
import subprocess
import sys

# Test data that simulates Claude claiming completion
test_input = {
    "session_id": "test-session-123",
    "tool_name": "Respond",
    "tool_input": {},
    "tool_response": {
        "response": "I've successfully implemented the ContactForm component. The implementation is complete with all validation working properly. ✅ All done!"
    }
}

# Run the hook
process = subprocess.Popen(
    ['python3', '.claude/hooks/post-tool-use/14-completion-verifier.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

stdout, stderr = process.communicate(input=json.dumps(test_input))

print("=== HOOK TEST RESULTS ===")
print(f"Exit code: {process.returncode}")
print(f"\nStdout:\n{stdout}")
print(f"\nStderr:\n{stderr}")

# Test without completion claim
test_input_no_claim = {
    "session_id": "test-session-456",
    "tool_name": "Respond",
    "tool_input": {},
    "tool_response": {
        "response": "I'm working on the ContactForm component. Let me add the validation logic next."
    }
}

process2 = subprocess.Popen(
    ['python3', '.claude/hooks/post-tool-use/14-completion-verifier.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

stdout2, stderr2 = process2.communicate(input=json.dumps(test_input_no_claim))

print("\n=== TEST 2 (No completion claim) ===")
print(f"Exit code: {process2.returncode}")
print(f"Stdout: {stdout2}")
print(f"Stderr: {stderr2}")
