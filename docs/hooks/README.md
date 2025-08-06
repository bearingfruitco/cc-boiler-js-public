# Hooks System Documentation

> Extending Claude Code's official hooks system with production-ready automation

## ⚠️ SECURITY WARNING

**USE AT YOUR OWN RISK**: Claude Code hooks execute arbitrary shell commands on your system automatically. By using hooks, you acknowledge that:

- You are solely responsible for the commands you configure
- Hooks can modify, delete, or access any files your user account can access
- Malicious or poorly written hooks can cause data loss or system damage
- Anthropic provides no warranty and assumes no liability for any damages resulting from hook usage
- You should thoroughly test hooks in a safe environment before production use

Always review and understand any hook commands before adding them to your configuration.

## Overview

This project provides 25+ pre-built hooks that extend the official Claude Code hooks system while maintaining 100% compatibility.

### Official Hooks Documentation
- Full Reference: https://docs.anthropic.com/en/docs/claude-code/hooks
- Security Guide: https://docs.anthropic.com/en/docs/claude-code/hooks#security-considerations

## Hook Events (Official)

Our hooks use all four official event types:

| Event | When It Runs | Our Usage |
|-------|--------------|-----------|
| **PreToolUse** | Before tool execution | Design validation, security checks, auto-approval |
| **PostToolUse** | After tool success | Auto-save, metrics, documentation updates |
| **Notification** | On notifications | Team awareness, smart suggestions |
| **Stop** | When Claude stops | State saving, knowledge extraction |

## Our Pre-Built Hooks

### PreToolUse Hooks (Prevent Issues)

1. **Design System Enforcement** (`02-design-check.py`)
   - Blocks non-compliant CSS before writing
   - Auto-fixes simple violations
   - Enforces 4-size, 2-weight system

2. **Security Validation** (`07-pii-protection.py`)
   - Prevents PII in logs, URLs, storage
   - Blocks sensitive data exposure
   - Enforces encryption requirements

3. **Auto-Approval** (`00-auto-approve-safe-ops.py`)
   - Skips confirmation for safe operations
   - Maintains security for dangerous ops
   - Improves workflow speed

4. **TDD Enforcement** (`19-tdd-enforcer.py`)
   - Ensures tests exist before implementation
   - Auto-spawns test generation
   - Maintains code quality

### PostToolUse Hooks (Automation)

1. **Auto-Save to GitHub** (`01-state-save.py`)
   - Saves work state every 60 seconds
   - Creates GitHub gists for backup
   - Enables perfect handoffs

2. **Documentation Updates** (`update-docs-on-change.py`)
   - Updates docs when code changes
   - Maintains sync automatically
   - Zero manual documentation

3. **Test Runner** (`06-test-auto-runner.py`)
   - Runs relevant tests after changes
   - Provides immediate feedback
   - Catches breaks early

### Notification Hooks (Intelligence)

1. **Smart Suggestions** (`smart-suggest.py`)
   - Context-aware command suggestions
   - Workflow recommendations
   - Reduces decision fatigue

2. **Team Awareness** (`team-aware.py`)
   - Shows team activity
   - Prevents conflicts
   - Enables collaboration

## Hook Configuration

### Using Official `/hooks` Command

```bash
/hooks              # Opens interactive configurator
```

### Our Configuration Structure

```json
{
  "hooks": {
    "pre-tool-use": [
      {
        "script": "02-design-check.py",
        "enabled": true,
        "critical": false,
        "auto_fix": true,
        "description": "Enforce design system rules"
      }
    ],
    "post-tool-use": [
      {
        "script": "01-state-save.py",
        "throttle": 60,
        "batch": true,
        "description": "Save work state to GitHub"
      }
    ]
  }
}
```

## Hook Input/Output (Official Schema)

### Input (All Hooks Receive)
```json
{
  "session_id": "unique-session-id",
  "timestamp": "2024-01-31T10:30:00Z",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "components/Button.tsx",
    "content": "..."
  }
}
```

### Output Options

#### Simple: Exit Codes
- `0` - Success, continue normally
- `2` - Block with error (PreToolUse blocks tool)
- Other - Non-blocking error

#### Advanced: JSON Output
```json
{
  "decision": "block",      // or "approve"
  "message": "Error details for Claude",
  "continue": true,         // or false to stop
  "metadata": {}           // Optional custom data
}
```

## Security Best Practices

### Input Validation
```python
# Always validate input
if '../' in file_path:
    return block("Path traversal detected")

# Quote shell variables
subprocess.run(['ls', file_path])  # Good
subprocess.run(f'ls {file_path}')  # Bad - injection risk
```

### Safe File Operations
```python
# Check allowed paths
ALLOWED_DIRS = ['src/', 'components/', 'lib/']
if not any(file_path.startswith(d) for d in ALLOWED_DIRS):
    return block("File outside allowed directories")

# Skip sensitive files
SENSITIVE = ['.env', 'secrets', 'credentials']
if any(s in file_path for s in SENSITIVE):
    return block("Cannot modify sensitive files")
```

## Creating Custom Hooks

### Template for PreToolUse Hook
```python
#!/usr/bin/env python3
"""
Hook description and purpose
Security: Explain what this hook can access/modify
"""

import json
import sys

def main():
    try:
        # Read input per official schema
        input_data = json.loads(sys.stdin.read())
        
        # Extract fields
        tool_name = input_data.get('tool_name')
        tool_input = input_data.get('tool_input', {})
        
        # Your logic here
        if should_block():
            # Block with feedback
            print(json.dumps({
                "decision": "block",
                "message": "Explanation for Claude"
            }))
            sys.exit(0)
        
        # Approve to skip confirmation
        print(json.dumps({
            "decision": "approve"
        }))
        sys.exit(0)
        
    except Exception as e:
        # Errors are non-blocking
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## Testing Hooks

### Manual Testing
```bash
# Test hook with sample input
echo '{"tool_name":"Write","tool_input":{"file_path":"test.ts"}}' | python hook.py
```

### Integration Testing
```bash
# Enable hook and test in Claude Code
/hooks
# Select hook and enable
# Try the operation it should affect
```

## Troubleshooting

### Hook Not Running?
1. Check `/hooks` menu shows your hook
2. Verify JSON syntax in settings
3. Check file permissions (must be executable)
4. Look for errors in debug mode: `claude --debug`

### Hook Blocking Incorrectly?
1. Test with sample data
2. Check decision logic
3. Verify JSON output format
4. Add logging for debugging

## Performance Considerations

- **Timeout**: Hooks have 60-second limit
- **Parallel**: Multiple hooks run simultaneously  
- **Throttling**: Use for expensive operations
- **Caching**: Cache results when possible

## Best Practices

1. **Fast Execution** - Keep hooks under 1 second
2. **Clear Messages** - Help Claude understand blocks
3. **Safe Defaults** - Fail open, not closed
4. **Test Coverage** - Test all code paths
5. **Error Handling** - Never crash Claude Code

## Summary

Our hooks system provides:
- ✅ 25+ production-ready hooks
- ✅ Full official compatibility
- ✅ Security-first design
- ✅ Extensive automation
- ✅ Easy customization

Use official `/hooks` command to manage, and our pre-built hooks for instant productivity.

---

*Remember: With great power comes great responsibility. Hooks run with your full permissions.*
