# Claude Code Hook Compliance Audit - GitHub Issues

## 🎯 Objective
Audit and fix all hooks to comply with the official Claude Code hooks specification.

## 📋 Official Specification Reference

### ✅ Correct Format Requirements:

1. **Tool Names (MUST be exact):**
   - `Write` (NOT write_file)
   - `Edit` (NOT edit_file)
   - `MultiEdit` (NOT multi_edit)
   - `Read` (NOT read_file)
   - `Bash` (NOT bash - must be capital B)
   - `Task`
   - `Glob`
   - `Grep`
   - `WebFetch` (NOT web_fetch)
   - `WebSearch` (NOT web_search)

2. **Exit Codes:**
   - `sys.exit(0)` = Success, continue operation
   - `sys.exit(2)` = BLOCK operation (stderr message sent to Claude)
   - `sys.exit(1)` or other = Non-blocking error (stderr shown to user)

3. **Input Format:**
   ```python
   input_data = json.loads(sys.stdin.read())
   tool_name = input_data.get('tool_name', '')
   tool_input = input_data.get('tool_input', {})  # NOT 'params'
   ```

4. **Output Format:**
   - To block: Print to stderr + `sys.exit(2)`
   - To warn: Print to stderr + `sys.exit(1)`
   - Success: Just `sys.exit(0)`
   - NEVER use: `{"decision": "block"}` format

---

## 🔴 Issue #1: Pre-Tool-Use Hooks Compliance [CRITICAL]

### Files to Audit and Fix:

#### High Priority - Core Functionality
- [✅] `00-auto-approve-safe-ops.py` - FIXED: Removed JSON decision format
- [✅] `00a-dangerous-commands.py` - Already compliant!
- [✅] `00a-snapshot-manager.py` - Already compliant!
- [✅] `01-collab-sync.py` - FIXED: Updated error exit code
- [✅] `02-design-check.py` ⭐ CRITICAL - Already compliant!
- [✅] `03-conflict-check.py` - Already compliant!
- [✅] `04-actually-works.py` - FIXED: Updated error exit code
- [✅] `05-code-quality.py` - Already compliant!
- [✅] `05a-auto-context-inclusion.py` - FIXED: Removed 'str_replace' tool name
- [ ] `05b-prp-context-loader.py`
- [ ] `05c-tdd-context-loader.py`

#### Medium Priority - Feature Hooks
- [✅] `06-browser-state-check.py` - FIXED: Removed JSON output, fixed exit codes
- [ ] `06-requirement-drift-detector.py`
- [ ] `06a-biome-lint.py`
- [✅] `07-pii-protection.py` ⭐ SECURITY - Already compliant!
- [ ] `08-evidence-language.py`
- [ ] `08a-async-patterns.py`
- [ ] `09-auto-persona.py`
- [✅] `10-hydration-guard.py` - FIXED: Removed 'str_replace' tool name
- [✅] `11-truth-enforcer.py` ⭐ CRITICAL - Already compliant!
- [✅] `12-deletion-guard.py` - Already compliant!
- [✅] `13-import-validator.py` - Already compliant!
- [ ] `14-prd-clarity.py`
- [ ] `14a-creation-guard.py`
- [ ] `15-implementation-guide.py`
- [ ] `15a-dependency-tracker.py`

#### Low Priority - Additional Hooks
- [ ] `16-tcpa-compliance.py`
- [ ] `16a-prp-validator.py`
- [ ] `17-ai-docs-check.py`
- [ ] `17-architecture-enforcer.py`
- [ ] `17-performance-budget-enforcer.py`
- [ ] `17-test-generation-enforcer.py`
- [ ] `18-auto-parallel-agents.py`
- [ ] `18-security-first-enforcer.py`
- [ ] `19-auto-rls-generator.py`
- [✅] `19-tdd-enforcer.py` ⭐ CRITICAL - FIXED: Removed JSON decision format
- [ ] `19a-auto-test-spawner.py`
- [ ] `20-feature-awareness.py`
- [ ] `20-feature-state-guardian.py`
- [ ] `21-branch-controller.py`
- [✅] `21-docs-first-enforcer.py` - FIXED: Removed JSON decision format
- [ ] `21-security-command-enhancer.py`
- [ ] `22-api-docs-generator.py`
- [ ] `22-security-validator.py`
- [ ] `23-a11y-enforcer.py`
- [ ] `24-environment-guard.py`
- [ ] `25-deployment-validator.py`
- [ ] `26-database-environment-check.py`
- [ ] `security-comprehensive.py`

### Common Issues Found:
1. ❌ Using `'write_file'` instead of `'Write'`
2. ❌ Using `'edit_file'` instead of `'Edit'`
3. ❌ Using `get('params')` instead of `get('tool_input')`
4. ❌ Using `{"decision": "block"}` format
5. ❌ Using lowercase `'bash'` instead of `'Bash'`

---

## 🟡 Issue #2: Post-Tool-Use Hooks Compliance

### Files to Audit and Fix:

#### High Priority
- [✅] `01-auto-error-recovery.py` - FIXED: Updated error exit code
- [ ] `01-state-save.py`
- [ ] `01a-action-logger.py`
- [ ] `01b-tdd-progress-logger.py`
- [ ] `02-coverage-tracker.py`
- [✅] `02-metrics.py` - FIXED: Updated error exit code
- [ ] `03-pattern-learning.py`
- [ ] `03a-auto-orchestrate.py`
- [ ] `03b-command-logger.py`
- [ ] `03c-response-capture.py`
- [✅] `04-next-command-suggester.py` ⭐ CRITICAL - Already compliant!
- [ ] `04-research-capture.py`
- [ ] `04a-architecture-suggester.py`
- [ ] `04a-prp-metrics.py`

#### Medium Priority
- [ ] `05-browser-verify.py`
- [✅] `05-multi-review-suggester.py` - FIXED: Updated tool names and tool_input
- [ ] `05-test-runner.py`
- [ ] `06-console-monitor.py`
- [ ] `06-test-auto-runner.py`
- [ ] `10-auto-browser-verify.py`
- [ ] `10-prp-progress-tracker.py`
- [ ] `10-smart-browser-verify.py`
- [✅] `14-completion-verifier.py` ⭐ CRITICAL - FIXED: Removed 'Respond' tool, fixed exit codes
- [ ] `15b-task-ledger-updater.py`
- [ ] `16-agent-metrics.py`
- [ ] `16-security-analyzer.py`
- [ ] `20-subagent-suggester.py`
- [ ] `25-architecture-change-tracker.py`
- [ ] `25-doc-updater.py`
- [ ] `26-prp-regeneration.py`

---

## 🟢 Issue #3: Other Hook Directories

### Notification Hooks
- [ ] Check all files in `/notification`

### Stop Hooks
- [ ] Check all files in `/stop`

### Sub-Agent-Stop Hooks
- [ ] Check all files in `/sub-agent-stop`

### User-Prompt-Submit Hooks
- [ ] Check all files in `/user-prompt-submit`

### Pre-Compact Hooks
- [ ] Check all files in `/pre-compact`

---

## 📝 Tracking Format

For each file, document:
1. **File:** `filename.py`
2. **Status:** 🔴 Not Started | 🟡 In Progress | ✅ Complete
3. **Issues Found:**
   - Issue 1
   - Issue 2
4. **Changes Made:**
   - Fixed X
   - Updated Y
5. **Testing:** Verified with sample input

---

## 🔧 Fix Checklist for Each Hook

When fixing each hook, ensure:

- [ ] Replace all incorrect tool names:
  - `write_file` → `Write`
  - `edit_file` → `Edit`
  - `read_file` → `Read`
  - `multi_edit` → `MultiEdit`
  - `bash` → `Bash`
  - `web_fetch` → `WebFetch`
  - `web_search` → `WebSearch`

- [ ] Fix input handling:
  - Change `get('params')` to `get('tool_input')`
  - Access fields via `tool_input.get('file_path')` etc.

- [ ] Fix output format:
  - Remove `{"decision": "block"}` JSON format
  - Use `sys.exit(2)` with stderr for blocking
  - Use `sys.exit(1)` with stderr for warnings
  - Use `sys.exit(0)` for success

- [ ] Verify exit codes:
  - Only use 0, 1, or 2
  - No custom exit codes like 3, 4, etc.

---

## 📊 Progress Summary

**Total Hooks:** ~75 files
**Completed:** 26
**In Progress:** 0
**Not Started:** 49

**Last Updated:** 2024-01-30

---

## 🚀 Next Steps

1. Start with critical hooks marked with ⭐
2. Fix each hook manually (no bulk scripts)
3. Test each hook after fixing
4. Update this document as work progresses
5. Create PR when batch of related hooks complete
