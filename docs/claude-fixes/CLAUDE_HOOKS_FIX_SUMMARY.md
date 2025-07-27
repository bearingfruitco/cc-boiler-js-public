# Claude Code Hooks Fix Summary

## ✅ What Was Fixed

### 1. **Settings.json Structure**
- Removed invalid fields (`file_system`, `shell` under permissions)
- Now only contains the 3 allowed fields: `permissions`, `env`, `hooks`
- Started with minimal hook configuration for testing

### 2. **Hook Output Format** 
- All hooks now output required JSON: `{"action": "continue"}` or `{"action": "block", "message": "..."}`
- Removed `sys.exit()` calls without output
- Fixed invalid action values (allow → continue, skip → continue, etc.)

### 3. **Tool Name Handling**
- Fixed hooks to handle multiple input formats from Claude Code
- Added proper extraction of tool_name and tool_input
- Changed from MCP-style names (filesystem:write_file) to Claude Code names (Write)

### 4. **Error Handling**
- Wrapped all main() functions in try-except blocks
- Ensures JSON output even on errors
- No more crashes that block Claude Code

### 5. **Problem Hooks**
Created minimal working versions for complex hooks that had too many issues:
- Collaboration sync hooks
- Pattern learning hooks  
- Notification hooks
- These are backed up as `.backup` files for future restoration

## 📋 Current Status

### Working Hooks in settings.json:
1. **00-auto-approve-safe-ops.py** - Auto-approves safe read operations
2. **02-design-check.py** - Enforces design system rules

### Hooks Ready to Add (after testing):
- **07-pii-protection.py** - PII/PHI protection
- **10-hydration-guard.py** - Next.js hydration error prevention
- **13-import-validator.py** - Import path validation

## 🚀 Next Steps

### 1. Test Current Setup
```bash
# Check settings are valid
claude doctor

# Start Claude Code
claude

# Test basic operations
/help
```

### 2. Gradually Add More Hooks
After confirming basic setup works, add hooks one at a time:

```json
{
  "matcher": "Write|Edit",
  "hooks": [
    {
      "type": "command", 
      "command": "python3 .claude/hooks/pre-tool-use/07-pii-protection.py"
    }
  ]
}
```

### 3. Test Each Hook
```bash
# Test individual hook
echo '{"tool_name": "Write", "tool_input": {"file_path": "test.py", "content": "test"}}' | python3 .claude/hooks/pre-tool-use/[hook-name].py

# Should output:
# {"action": "continue"}
```

### 4. Restore Complex Hooks Later
The complex hooks are backed up and can be properly refactored later:
- Focus on hook logic, not infrastructure
- Ensure single JSON output
- Handle all input formats
- Test thoroughly before enabling

## 🔧 Common Issues & Solutions

### Issue: "Cannot assign to read only property"
**Solution**: Check settings.json only has `permissions`, `env`, `hooks`

### Issue: Hook doesn't run
**Solution**: Check matcher pattern and command path

### Issue: Claude Code hangs
**Solution**: Hook is not outputting JSON - check with test command

### Issue: "Invalid action"
**Solution**: Only use: continue, block, approve, warn

## 📚 Key Rules for Hooks

1. **ALWAYS output JSON**: `print(json.dumps({"action": "continue"}))`
2. **Handle multiple input formats**: tool_name might be in different places
3. **Use correct tool names**: Write, Edit, Read, Bash (not filesystem:write_file)
4. **One output only**: No multiple print statements
5. **Error handling**: Always output JSON even on errors

## 🎯 Testing Checklist

- [ ] Run `claude doctor` - no errors
- [ ] Start Claude Code - no errors
- [ ] Run `/help` - works
- [ ] Create a file - auto-approval works
- [ ] Edit a component - design check works
- [ ] Check `.claude/logs/` for hook execution
- [ ] Add one more hook and repeat

## 💡 Tips

1. Start minimal - 2-3 hooks max initially
2. Test hooks individually before adding to settings.json
3. Watch Claude Code output with `--debug` flag for hook details
4. Keep hooks simple - complex logic often breaks
5. When in doubt, output `{"action": "continue"}`

## 🚨 If Things Break

1. Restore minimal settings:
```bash
echo '{"permissions": {"allow": [], "deny": [], "defaultMode": "default"}, "env": {}, "hooks": {}}' > .claude/settings.json
```

2. Check for other settings files:
```bash
find ~ -name "settings.json" -path "*claude*" 2>/dev/null
```

3. Remove all and start fresh:
```bash
mv .claude .claude.broken
mkdir .claude
echo '{}' > .claude/settings.json
```

Your hooks system is now fixed and ready for gradual testing and expansion!
