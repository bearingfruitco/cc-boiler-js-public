# Claude Code Hooks Fix Guide

## 🚨 Critical Changes Needed

Based on the official Claude Code documentation and common errors, your hooks need these fixes:

### 1. **EVERY Hook Must Output Valid JSON**

❌ **WRONG** (your current pattern):
```python
sys.exit(0)  # No output
```

✅ **CORRECT**:
```python
print(json.dumps({"action": "continue"}))
```

### 2. **Valid Hook Actions**

For `PreToolUse` hooks:
- `{"action": "continue"}` - Continue with normal flow
- `{"action": "approve"}` - Auto-approve (bypass permissions)
- `{"action": "block", "message": "reason"}` - Block the operation
- `{"action": "warn", "message": "warning", "continue": true}` - Warn but continue

For `PostToolUse` hooks:
- `{"action": "continue"}` - Continue normally
- `{"action": "block", "message": "reason"}` - Show error to Claude

### 3. **Handle Multiple Input Formats**

Claude Code may send different formats:

```python
def get_tool_info(input_data):
    """Extract tool information from various input formats"""
    # Format 1: Direct tool info
    if 'tool_name' in input_data:
        return input_data['tool_name'], input_data.get('tool_input', {})
    
    # Format 2: Tool use wrapper
    tool_use = input_data.get('tool_use', {})
    if tool_use:
        return tool_use.get('name', ''), tool_use.get('parameters', {})
    
    # Format 3: Legacy format
    return input_data.get('tool', ''), input_data
```

### 4. **Fix Common Patterns**

#### Pattern 1: Exit without output
```python
# ❌ WRONG
if should_block:
    sys.exit(1)

# ✅ CORRECT
if should_block:
    print(json.dumps({
        "action": "block",
        "message": "Reason for blocking"
    }))
    return
```

#### Pattern 2: Multiple outputs
```python
# ❌ WRONG
print("Checking design...")
print(json.dumps({"action": "continue"}))

# ✅ CORRECT - only ONE output
result = {"action": "continue"}
if violations:
    result = {
        "action": "block",
        "message": f"Design violations: {violations}"
    }
print(json.dumps(result))
```

#### Pattern 3: Wrong tool names
```python
# ❌ WRONG - MCP style names
if tool_name == 'filesystem:write_file':

# ✅ CORRECT - Claude Code names
if tool_name == 'Write':
```

### 5. **Tool Name Reference**

Claude Code uses these tool names:
- `Task` - Agent tasks
- `Bash` - Shell commands
- `Read` - File reading
- `Write` - File writing
- `Edit`, `MultiEdit` - File editing
- `Glob` - File pattern matching
- `Grep` - Content search
- `WebFetch`, `WebSearch` - Web operations

### 6. **Quick Fix Script**

Run this to fix all hooks at once:

```bash
#!/bin/bash
# fix-all-hooks.sh

# Find all Python hooks
find .claude/hooks -name "*.py" -type f | while read hook; do
    echo "Fixing: $hook"
    
    # Check if hook has any print(json.dumps output
    if ! grep -q 'print(json.dumps' "$hook"; then
        # Add required output before the last line
        sed -i '' -e '$i\
\    # Ensure we always output valid JSON\
\    print(json.dumps({"action": "continue"}))' "$hook"
    fi
    
    # Fix sys.exit(0) to include output
    sed -i '' 's/sys.exit(0)/print(json.dumps({"action": "continue"}))\
        return/g' "$hook"
    
    # Fix sys.exit(1) to use block action
    sed -i '' 's/sys.exit(1)/print(json.dumps({"action": "block", "message": "Operation blocked"}))\
        return/g' "$hook"
done
```

### 7. **Testing Your Fixes**

1. Test individual hook:
```bash
echo '{"tool_name": "Write", "tool_input": {"file_path": "test.py"}}' | python3 .claude/hooks/pre-tool-use/02-design-check.py
```

2. Run the test script:
```bash
python3 test-claude-hooks.py
```

3. Validate with Claude doctor:
```bash
claude doctor
```

### 8. **Minimal Working Configuration**

Start with this minimal settings.json:

```json
{
  "permissions": {
    "allow": [],
    "deny": [],
    "defaultMode": "default"
  },
  "env": {},
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/pre-tool-use/00-auto-approve-safe-ops.py"
          }
        ]
      }
    ]
  }
}
```

Then add hooks one at a time after testing each one.

## 🔧 Hook Template

Use this template for all new hooks:

```python
#!/usr/bin/env python3
"""Hook description"""

import json
import sys

def main():
    try:
        # Read input
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool info (handle multiple formats)
        tool_name = input_data.get('tool_name', '')
        if not tool_name and 'tool_use' in input_data:
            tool_name = input_data['tool_use'].get('name', '')
        
        tool_input = input_data.get('tool_input', {})
        if not tool_input and 'tool_use' in input_data:
            tool_input = input_data['tool_use'].get('parameters', {})
        
        # Your hook logic here
        
        # ALWAYS output valid JSON
        print(json.dumps({"action": "continue"}))
        
    except Exception as e:
        # Always output valid JSON even on error
        print(json.dumps({
            "action": "continue",
            "message": f"Hook error: {str(e)}"
        }))

if __name__ == '__main__':
    main()
```

## 📋 Checklist

Before using hooks, ensure:

- [ ] `settings.json` only contains `permissions`, `env`, `hooks` fields
- [ ] All hooks output `{"action": "..."}` JSON
- [ ] No `sys.exit()` without JSON output
- [ ] Tool names match Claude Code names (not MCP names)
- [ ] Each hook tested with `test-claude-hooks.py`
- [ ] `claude doctor` shows no errors
- [ ] Start with minimal hooks, add gradually

Remember: The most common issue is invalid JSON output from hooks!
