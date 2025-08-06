# GitHub Issues for Hook System Repair

Based on the official [Claude Code hooks documentation](https://docs.anthropic.com/en/docs/claude-code/hooks), here are the issues to create:

---

## Issue #1: 🚨 [P0 CRITICAL] Fix 3 missing hooks blocking all file operations

**Title:** Fix missing PII, TCPA, and Security hooks that block all operations  
**Labels:** `bug`, `critical`, `blocking`, `hooks`  
**Assignee:** @shawnsmith  
**Priority:** P0 - CRITICAL  
**Milestone:** Hook System Recovery  

### Description

Three critical pre-tool-use hooks are missing/broken, causing all file operations to fail. These hooks need to follow the official Claude Code hook specification.

### Official Hook Requirements (from Anthropic docs)

```json
// Input format (via stdin):
{
  "tool_name": "Write",  // Official tool names: Write, Edit, Read, Bash, etc.
  "tool_input": {
    "file_path": "/path/to/file",
    "content": "file content"
  }
}
```

**Exit codes:**
- `0` = Success, continue
- `2` = Block operation (stderr sent to Claude)  
- `1` or other = Non-blocking error (stderr shown to user)

### Current State

| Hook | Main File | Backup Files | Status |
|------|-----------|--------------|--------|
| 07-pii-protection.py | Missing | .original (syntax error line 243), .broken (syntax error line 208) | ❌ All versions broken |
| 16-tcpa-compliance.py | Missing | .original (syntax error line 32) | ❌ Backup broken |
| 22-security-validator.py | Missing | .original (valid syntax, wrong format) | ⚠️ Needs format update |

### Tasks

- [ ] **Task 1.1:** Install 07-pii-protection.py
  ```bash
  # Copy the official-compliant version
  cp .claude/hooks/pre-tool-use/07-pii-protection-OFFICIAL.py .claude/hooks/pre-tool-use/07-pii-protection.py
  
  # Test with PII content (should block with exit code 2)
  echo '{"tool_name":"Write","tool_input":{"file_path":"test.ts","content":"console.log(email);"}}' | python3 .claude/hooks/pre-tool-use/07-pii-protection.py
  echo "Exit code: $?"  # Should be 2
  
  # Test without PII (should pass with exit code 0)
  echo '{"tool_name":"Write","tool_input":{"file_path":"test.ts","content":"console.log(data);"}}' | python3 .claude/hooks/pre-tool-use/07-pii-protection.py
  echo "Exit code: $?"  # Should be 0
  ```

- [ ] **Task 1.2:** Install 16-tcpa-compliance.py
  ```bash
  # Copy the official-compliant version
  cp .claude/hooks/pre-tool-use/16-tcpa-compliance-OFFICIAL.py .claude/hooks/pre-tool-use/16-tcpa-compliance.py
  
  # Test with phone field without consent (should block)
  echo '{"tool_name":"Write","tool_input":{"file_path":"ContactForm.tsx","content":"<input name=\"phone\" />"}}' | python3 .claude/hooks/pre-tool-use/16-tcpa-compliance.py
  echo "Exit code: $?"  # Should be 2
  
  # Test with consent language (should pass)
  echo '{"tool_name":"Write","tool_input":{"file_path":"ContactForm.tsx","content":"<input name=\"phone\" />\\n<p>By providing your phone, you consent to receive messages</p>"}}' | python3 .claude/hooks/pre-tool-use/16-tcpa-compliance.py
  echo "Exit code: $?"  # Should be 0
  ```

- [ ] **Task 1.3:** Install 22-security-validator.py
  ```bash
  # Copy the official-compliant version
  cp .claude/hooks/pre-tool-use/22-security-validator-OFFICIAL.py .claude/hooks/pre-tool-use/22-security-validator.py
  
  # Test with unvalidated input (should warn/block)
  echo '{"tool_name":"Write","tool_input":{"file_path":"/api/test.ts","content":"const data = await req.json();"}}' | python3 .claude/hooks/pre-tool-use/22-security-validator.py
  echo "Exit code: $?"  # Should be 1 or 2
  
  # Test with validated input (should pass)
  echo '{"tool_name":"Write","tool_input":{"file_path":"/api/test.ts","content":"const data = schema.parse(await req.json());"}}' | python3 .claude/hooks/pre-tool-use/22-security-validator.py
  echo "Exit code: $?"  # Should be 0
  ```

- [ ] **Task 1.4:** Archive broken versions
  ```bash
  mkdir -p .claude/hooks/_archive/20250805
  mv .claude/hooks/pre-tool-use/07-pii-protection.py.original .claude/hooks/_archive/20250805/
  mv .claude/hooks/pre-tool-use/07-pii-protection.py.broken .claude/hooks/_archive/20250805/
  mv .claude/hooks/pre-tool-use/16-tcpa-compliance.py.original .claude/hooks/_archive/20250805/
  mv .claude/hooks/pre-tool-use/22-security-validator.py.original .claude/hooks/_archive/20250805/
  ```

- [ ] **Task 1.5:** Verify in Claude Code
  - Restart Claude Code
  - Try to write a file
  - Confirm no hook errors appear

### Acceptance Criteria

- [ ] All 3 hooks installed and pass syntax check
- [ ] Each hook correctly uses exit code 2 for blocking
- [ ] Each hook correctly uses exit code 0 for success
- [ ] Hooks parse official JSON format from stdin
- [ ] No hook errors when performing file operations in Claude Code
- [ ] All broken versions archived

---

## Issue #2: [P1 HIGH] Update 20 hooks from old format to official format

**Title:** Update hooks using {"decision":"block"} to use exit codes  
**Labels:** `refactor`, `hooks`, `compliance`  
**Assignee:** @shawnsmith  
**Priority:** P1 - HIGH  
**Milestone:** Hook System Recovery  

### Description

20 hooks use the old `{"decision": "block"}` format instead of the official exit code system. These need to be updated to comply with the official specification.

### Hooks Requiring Format Update

| Hook | Current Format | Required Change |
|------|---------------|-----------------|
| 02-design-check.py | `print(json.dumps({"decision": "block"}))` | Use `sys.exit(2)` with stderr |
| 00a-dangerous-commands.py | `{"decision": "block"}` | Use `sys.exit(2)` |
| 03-conflict-check.py | `{"decision": "block"}` | Use `sys.exit(2)` |
| 05-code-quality.py | `{"decision": "block"}` | Use `sys.exit(2)` |
| 06-requirement-drift-detector.py | `{"decision": "block"}` | Use `sys.exit(2)` |
| 11-truth-enforcer.py | `{"decision": "block"}` | Use `sys.exit(2)` |
| 14-prd-clarity.py | `{"decision": "block"}` | Use `sys.exit(2)` |
| 15-implementation-guide.py | `{"decision": "block"}` + uses `write_file` | Use `sys.exit(2)` + check for `Write` |
| 16a-prp-validator.py | `{"decision": "block"}` | Use `sys.exit(2)` |
| 17-performance-budget-enforcer.py | `{"decision": "block"}` | Use `sys.exit(2)` |
| 17-test-generation-enforcer.py | `{"decision": "block"}` | Use `sys.exit(2)` |
| 18-security-first-enforcer.py | `{"decision": "block"}` | Use `sys.exit(2)` |
| 19-tdd-enforcer.py | `{"decision": "block"}` | Use `sys.exit(2)` |
| 19a-auto-test-spawner.py | `{"decision": "block"}` | Use `sys.exit(2)` |
| 20-feature-state-guardian.py | `{"decision": "block"}` | Use `sys.exit(2)` |
| 21-branch-controller.py | `{"decision": "block"}` | Use `sys.exit(2)` |
| 21-docs-first-enforcer.py | `{"decision": "block"}` | Use `sys.exit(2)` |
| 23-a11y-enforcer.py | `{"decision": "block"}` | Use `sys.exit(2)` |

### Tasks

- [ ] **Task 2.1:** Update 02-design-check.py
  ```python
  # CHANGE FROM:
  print(json.dumps({"decision": "block", "message": error_msg}))
  sys.exit(0)
  
  # CHANGE TO:
  print(error_msg, file=sys.stderr)
  sys.exit(2)  # Block with exit code 2
  ```

- [ ] **Task 2.2:** Update tool name checks
  ```python
  # CHANGE FROM:
  if tool_name not in ['write_file', 'edit_file']:
  
  # CHANGE TO:
  if tool_name not in ['Write', 'Edit', 'MultiEdit']:
  ```

- [ ] **Task 2.3:** Test each updated hook
  ```bash
  # For each hook, test blocking scenario
  echo '{"tool_name":"Write","tool_input":{"file_path":"test.tsx","content":"BAD_CONTENT"}}' | python3 .claude/hooks/pre-tool-use/HOOKNAME.py
  echo "Exit code: $?"  # Should be 2 for blocking
  ```

- [ ] **Task 2.4:** Create test script for all hooks
  ```bash
  # Create a test that validates all hooks use proper exit codes
  for hook in .claude/hooks/pre-tool-use/*.py; do
    if grep -q '"decision".*"block"' "$hook"; then
      echo "❌ $hook still uses old format"
    fi
  done
  ```

### Acceptance Criteria

- [ ] No hooks contain `{"decision": "block"}` pattern
- [ ] All blocking hooks use `sys.exit(2)`
- [ ] All success cases use `sys.exit(0)`
- [ ] All hooks check for official tool names (Write, Edit, not write_file)
- [ ] Each hook tested with official JSON input format

---

## Issue #3: [P2 MEDIUM] Clean up 70+ duplicate hook files

**Title:** Archive duplicate hook versions (.original, .broken, .backup, .old)  
**Labels:** `cleanup`, `technical-debt`, `hooks`  
**Assignee:** @shawnsmith  
**Priority:** P2 - MEDIUM  
**Milestone:** Hook System Recovery  

### Description

70+ duplicate files exist across all hook directories. These need to be reviewed and archived.

### Duplicate Files by Directory

| Directory | Duplicate Count | File Extensions |
|-----------|----------------|-----------------|
| pre-tool-use | 35 | .original, .broken, .backup, .old |
| post-tool-use | 18 | .original, .backup |
| pre-compact | 2 | .original, .prefixbatch |
| user-prompt-submit | 2 | .original, .prefixbatch |
| stop | 5 | .original, .prefixbatch |
| sub-agent-stop | 3 | .original, .prefixbatch |
| notification | 5 | .original, .prefixbatch |

### Tasks

- [ ] **Task 3.1:** Review each duplicate group
  ```bash
  # For each hook with duplicates, compare sizes and dates
  ls -la .claude/hooks/pre-tool-use/11-truth-enforcer.py*
  # Keep: 11-truth-enforcer.py
  # Archive: .old, .original
  ```

- [ ] **Task 3.2:** Create archive directory with timestamp
  ```bash
  ARCHIVE_DIR=".claude/hooks/_archive/$(date +%Y%m%d_%H%M%S)"
  mkdir -p "$ARCHIVE_DIR"
  ```

- [ ] **Task 3.3:** Move duplicates to archive
  ```bash
  # Move all backup versions
  find .claude/hooks -type f \( \
    -name "*.original" -o \
    -name "*.broken" -o \
    -name "*.backup" -o \
    -name "*.old" -o \
    -name "*.prefixbatch" \
  \) -exec mv {} "$ARCHIVE_DIR/" \;
  ```

- [ ] **Task 3.4:** Document what was kept
  ```bash
  # Create manifest of decisions
  echo "# Hook Version Decisions - $(date)" > "$ARCHIVE_DIR/DECISIONS.md"
  echo "Kept main versions, archived all backups" >> "$ARCHIVE_DIR/DECISIONS.md"
  ```

- [ ] **Task 3.5:** Verify no duplicates remain
  ```bash
  find .claude/hooks -name "*.original" -o -name "*.broken" -o -name "*.backup" | wc -l
  # Should output: 0
  ```

### Acceptance Criteria

- [ ] No .original, .broken, .backup, .old, .prefixbatch files in hook directories
- [ ] All duplicates archived with timestamp
- [ ] Decision log created in archive
- [ ] Each hook directory has only one version per hook

---

## Issue #4: [P2 MEDIUM] Fix hooks with missing tool_input field

**Title:** Update hooks missing required tool_input field  
**Labels:** `bug`, `hooks`, `compliance`  
**Assignee:** @shawnsmith  
**Priority:** P2 - MEDIUM  
**Milestone:** Hook System Recovery  

### Description

Several hooks are missing the `tool_input` field or not parsing it correctly from the official JSON format.

### Affected Hooks

**Pre-tool-use:**
- 17-architecture-enforcer.py

**Post-tool-use:**
- 01-auto-error-recovery.py
- 03b-command-logger.py
- 04-next-command-suggester.py
- 04a-architecture-suggester.py
- 05-multi-review-suggester.py

**User-prompt-submit:**
- All 3 hooks (different input format for this event)

### Tasks

- [ ] **Task 4.1:** Update to use tool_input field
  ```python
  # CHANGE FROM:
  params = input_data.get('params', {})
  
  # CHANGE TO:
  tool_input = input_data.get('tool_input', {})
  file_path = tool_input.get('file_path', '')
  content = tool_input.get('content', '')
  ```

- [ ] **Task 4.2:** Handle UserPromptSubmit differently
  ```python
  # UserPromptSubmit has different schema:
  # { "prompt": "user's prompt text", "session_id": "...", ... }
  # Not tool_name/tool_input
  ```

- [ ] **Task 4.3:** Test with correct JSON structure
  ```bash
  echo '{"tool_name":"Write","tool_input":{"file_path":"test.ts","content":"test"}}' | python3 [hook]
  ```

### Acceptance Criteria

- [ ] All PreToolUse/PostToolUse hooks check tool_input field
- [ ] UserPromptSubmit hooks handle their different schema
- [ ] No hooks reference old field names (params, etc.)

---

## Issue #5: [P3 LOW] Create hook validation and testing framework

**Title:** Build automated testing for hook compliance  
**Labels:** `testing`, `automation`, `hooks`  
**Assignee:** @shawnsmith  
**Priority:** P3 - LOW  
**Milestone:** Hook System Improvements  

### Description

Create automated testing to ensure all hooks remain compliant with the official specification.

### Tasks

- [ ] **Task 5.1:** Create test harness
  ```python
  # test_hooks.py
  def test_hook_compliance(hook_path):
      # Test with various inputs
      # Verify exit codes
      # Check stderr output
      pass
  ```

- [ ] **Task 5.2:** Create CI/CD integration
  ```yaml
  # .github/workflows/test-hooks.yml
  - name: Test all hooks
    run: python3 scripts/test_hooks.py
  ```

- [ ] **Task 5.3:** Create hook template
  ```python
  # templates/hook_template.py
  # Official format template for new hooks
  ```

- [ ] **Task 5.4:** Documentation
  - Hook development guide
  - Testing procedures
  - Troubleshooting guide

### Acceptance Criteria

- [ ] Automated test suite for all hooks
- [ ] CI/CD runs tests on commit
- [ ] Template for creating new hooks
- [ ] Complete documentation

---

## 🎯 Execution Order

1. **Start with Issue #1** - Fix the 3 critical hooks (blocks all operations)
2. **Then Issue #2** - Update format for existing hooks  
3. **Then Issue #3** - Clean up duplicates
4. **Then Issue #4** - Fix missing fields
5. **Finally Issue #5** - Build testing framework

---

## 📊 Success Metrics

- **Immediate:** File operations work without hook errors
- **Day 1:** All critical hooks installed and tested
- **Week 1:** All hooks using official format
- **Week 2:** No duplicate files, full compliance

---

**Created:** 2025-08-05  
**Updated:** Based on official Anthropic documentation review  
**Status:** Ready to create in GitHub
