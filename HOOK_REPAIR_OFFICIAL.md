# Hook System Repair Plan - Official Claude Code Compliant

## 🚨 Critical Issue: Hooks Not Following Official Format

After reviewing the [official Claude Code hooks documentation](https://docs.anthropic.com/en/docs/claude-code/hooks), I've identified that your hooks are using an outdated or incorrect format.

### Official Hook Requirements

According to Anthropic's documentation:

1. **Input Format**: Hooks receive JSON via stdin with this schema:
   ```json
   {
     "tool_name": "Write",
     "tool_input": {
       "file_path": "/path/to/file",
       "content": "file content"
     }
   }
   ```

2. **Exit Codes**:
   - `0` = Success (continue execution)
   - `2` = Blocking error (stderr fed to Claude)
   - Other = Non-blocking error (stderr shown to user)

3. **Output**:
   - stdout: Shown in transcript mode (Ctrl-R)
   - stderr: Fed back to Claude (exit code 2) or shown to user (other codes)
   - Optional JSON output for advanced control

4. **Configuration**: In `settings.json`:
   ```json
   {
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "Write|Edit",
           "hooks": [
             {
               "type": "command",
               "command": "python3 .claude/hooks/pre-tool-use/hook.py"
             }
           ]
         }
       ]
     }
   }
   ```

### Your Current Issues

1. **Wrong Input Format**: Many hooks expect different JSON structure
2. **Wrong Exit Codes**: Not using exit code 2 for blocking
3. **Multiple Versions**: 70+ duplicate files with various formats
4. **Syntax Errors**: Critical hooks have Python errors

---

## 📋 GitHub Issues to Create

### Issue #1: 🚨 P0 - Fix Critical Hooks to Match Official Format
**Title:** Update 3 critical hooks to official Claude Code format  
**Labels:** `bug`, `critical`, `hooks`, `blocking`  
**Priority:** P0 - URGENT  

**Problem:**
Three critical hooks are missing/broken and not following the official Claude Code hook specification.

**Tasks:**
- [x] Create officially compliant 07-pii-protection.py
- [x] Create officially compliant 16-tcpa-compliance.py  
- [x] Create officially compliant 22-security-validator.py
- [ ] Install the official versions
- [ ] Test with proper JSON input
- [ ] Verify exit codes work correctly
- [ ] Update settings.json matcher patterns

**Implementation:**
```bash
# Run the official repair script
chmod +x scripts/repair-hooks-official.sh
./scripts/repair-hooks-official.sh

# Test with official format
echo '{"tool_name":"Write","tool_input":{"file_path":"test.ts","content":"test"}}' | python3 .claude/hooks/pre-tool-use/07-pii-protection.py
```

---

### Issue #2: ⚠️ P1 - Audit All Hooks for Official Compliance
**Title:** Update all hooks to match official Claude Code specification  
**Labels:** `refactor`, `hooks`, `compliance`  
**Priority:** P1 - High  

**Problem:**
Most hooks are using outdated formats and need updating to match official specification.

**Tasks:**
- [ ] Create validation script for official format
- [ ] Test each hook with proper JSON input
- [ ] Update hooks to use correct exit codes
- [ ] Fix tool_name matching (should be "Write" not "write_file")
- [ ] Update all matcher patterns in settings.json
- [ ] Test blocking vs non-blocking behavior

**Affected Hook Types:**
- PreToolUse: Before tool calls (can block)
- PostToolUse: After tool completion  
- UserPromptSubmit: When user submits prompt
- SessionStart: New/resumed session
- Notification: When awaiting input
- Stop: When Claude finishes
- SubAgentStop: When subagent finishes
- PreCompact: Before compaction

---

### Issue #3: 🧹 P2 - Clean Up Duplicate Hook Versions
**Title:** Remove 70+ duplicate hook files after compliance update  
**Labels:** `cleanup`, `technical-debt`  
**Priority:** P2 - Medium  

**Problem:**
Multiple versions exist (.original, .broken, .backup, .old, .prefixbatch).

**Tasks:**
- [ ] Identify which hooks are actually being used
- [ ] Test current vs backup versions
- [ ] Archive all non-compliant versions
- [ ] Document which version was kept
- [ ] Update version control

**Archive Strategy:**
```bash
# Create archive with timestamp
mkdir -p .claude/hooks/_archive/$(date +%Y%m%d)

# Move all old versions
find .claude/hooks -type f \( \
  -name "*.original" -o \
  -name "*.broken" -o \
  -name "*.backup" -o \
  -name "*.old" -o \
  -name "*.prefixbatch" \
\) -exec mv {} .claude/hooks/_archive/$(date +%Y%m%d)/ \;
```

---

### Issue #4: 📚 P3 - Create Official Hooks Documentation
**Title:** Document hooks following Anthropic's specification  
**Labels:** `documentation`, `hooks`  
**Priority:** P3 - Low  

**Tasks:**
- [ ] Document each hook's purpose
- [ ] Provide JSON input/output examples
- [ ] Document exit code behavior
- [ ] Create testing guide
- [ ] Add troubleshooting section

**Documentation Structure:**
```markdown
# Hook Name
## Purpose
## Input Schema
## Exit Codes
## Example Usage
## Testing
```

---

### Issue #5: 🔧 P2 - Create Hook Validation Framework
**Title:** Build testing framework for official hook compliance  
**Labels:** `testing`, `automation`, `hooks`  
**Priority:** P2 - Medium  

**Tasks:**
- [ ] Create test harness with sample JSON inputs
- [ ] Test all exit code scenarios
- [ ] Validate JSON parsing
- [ ] Check stderr/stdout handling
- [ ] Create CI/CD integration

**Test Cases:**
```python
# Test success case (exit 0)
test_input = {"tool_name": "Read", "tool_input": {"file_path": "test.py"}}

# Test blocking case (exit 2)  
test_input = {"tool_name": "Write", "tool_input": {"content": "console.log(ssn)"}}

# Test warning case (exit 1)
test_input = {"tool_name": "Write", "tool_input": {"content": "// TODO: fix"}}
```

---

## 🚀 Immediate Action Plan

### Step 1: Install Official Hooks (NOW)
```bash
# Run the official compliant repair script
chmod +x scripts/repair-hooks-official.sh
./scripts/repair-hooks-official.sh
```

### Step 2: Verify Official Format (5 min)
```bash
# Test each critical hook
for hook in 07-pii-protection 16-tcpa-compliance 22-security-validator; do
  echo "Testing $hook..."
  echo '{"tool_name":"Write","tool_input":{"file_path":"test.ts","content":"test"}}' | \
    python3 .claude/hooks/pre-tool-use/${hook}.py
  echo "Exit code: $?"
done
```

### Step 3: Update settings.json (10 min)
Ensure matcher patterns use official tool names:
- `Write` (not write_file)
- `Edit` (not edit_file)
- `Bash` (not bash_command)
- `Read` (not read_file)

### Step 4: Clean Up (15 min)
```bash
# Archive all old versions
mkdir -p .claude/hooks/_archive/20250805
find .claude/hooks -name "*.original" -o -name "*.broken" | xargs -I {} mv {} .claude/hooks/_archive/20250805/
```

---

## 📊 Success Criteria

The hook system is compliant when:

1. ✅ All hooks accept official JSON input format
2. ✅ Exit codes follow specification (0, 2, other)
3. ✅ Matcher patterns use official tool names
4. ✅ No duplicate versions remain
5. ✅ All hooks pass validation tests
6. ✅ Documentation matches official spec

---

## 🔍 Key Differences from Previous Approach

| Aspect | Your Current | Official Spec |
|--------|--------------|---------------|
| Input | Various formats | JSON via stdin |
| Tool Names | write_file, edit_file | Write, Edit |
| Blocking | Different mechanisms | Exit code 2 |
| Non-blocking | Various | Exit code 1 |
| Success | Various | Exit code 0 |
| Feedback | print() statements | stderr for Claude |

---

## 📚 Resources

- [Official Hooks Reference](https://docs.anthropic.com/en/docs/claude-code/hooks)
- [Hooks Quickstart Guide](https://docs.anthropic.com/en/docs/claude-code/hooks-guide)
- [Security Considerations](https://docs.anthropic.com/en/docs/claude-code/hooks#security-considerations)

---

**Created:** 2025-08-05  
**Updated:** After reviewing official documentation  
**Status:** Ready for implementation
