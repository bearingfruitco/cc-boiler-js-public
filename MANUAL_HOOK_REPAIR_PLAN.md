# Manual Hook Repair Plan - One by One

## 🚨 Current Situation

After reviewing ALL hooks against the official documentation:
- **Only 26 out of 46 pre-tool-use hooks are compliant**
- **Most hooks use OLD format**: `{"decision": "block"}` instead of exit codes
- **Wrong tool names**: Using `write_file` instead of `Write`
- **Missing critical hooks**: 07-pii-protection, 16-tcpa-compliance, 22-security-validator

## 📋 Manual Actions Required - One Hook at a Time

### Group 1: Critical Missing Hooks (MUST FIX FIRST)

#### Hook: `07-pii-protection.py`
**Current State:** 
- ❌ Main file missing
- ❌ `.original` has syntax error (line 243)
- ❌ `.broken` has syntax error (line 208)

**ACTION:**
```bash
# Use the official-compliant version we created
cp .claude/hooks/pre-tool-use/07-pii-protection-OFFICIAL.py .claude/hooks/pre-tool-use/07-pii-protection.py

# Archive broken versions
mkdir -p .claude/hooks/_archive/20250805
mv .claude/hooks/pre-tool-use/07-pii-protection.py.original .claude/hooks/_archive/20250805/
mv .claude/hooks/pre-tool-use/07-pii-protection.py.broken .claude/hooks/_archive/20250805/

# Test it
echo '{"tool_name":"Write","tool_input":{"file_path":"test.ts","content":"console.log(email);"}}' | python3 .claude/hooks/pre-tool-use/07-pii-protection.py
echo "Exit code: $?"  # Should be 2 (blocking)
```

---

#### Hook: `16-tcpa-compliance.py`
**Current State:**
- ❌ Main file missing  
- ❌ `.original` has syntax error (line 32)

**ACTION:**
```bash
# Use the official-compliant version we created
cp .claude/hooks/pre-tool-use/16-tcpa-compliance-OFFICIAL.py .claude/hooks/pre-tool-use/16-tcpa-compliance.py

# Archive broken version
mv .claude/hooks/pre-tool-use/16-tcpa-compliance.py.original .claude/hooks/_archive/20250805/

# Test it
echo '{"tool_name":"Write","tool_input":{"file_path":"ContactForm.tsx","content":"<input name=\"phone\" />"}}' | python3 .claude/hooks/pre-tool-use/16-tcpa-compliance.py
echo "Exit code: $?"  # Should be 2 (blocking due to missing consent)
```

---

#### Hook: `22-security-validator.py`
**Current State:**
- ❌ Main file missing
- ⚠️ `.original` has valid syntax but uses old format

**ACTION:**
```bash
# Use the official-compliant version we created
cp .claude/hooks/pre-tool-use/22-security-validator-OFFICIAL.py .claude/hooks/pre-tool-use/22-security-validator.py

# Archive old version
mv .claude/hooks/pre-tool-use/22-security-validator.py.original .claude/hooks/_archive/20250805/

# Test it
echo '{"tool_name":"Write","tool_input":{"file_path":"/api/test.ts","content":"await req.json()"}}' | python3 .claude/hooks/pre-tool-use/22-security-validator.py
echo "Exit code: $?"  # Should be 1 or 2 depending on severity
```

---

### Group 2: Hooks Using OLD Format (Need Update)

These hooks work but use `{"decision": "block"}` instead of exit codes:

#### Hook: `02-design-check.py`
**Current State:**
- ✅ Main file exists and has valid syntax
- ❌ Uses old format: `{"decision": "block"}`
- ❌ Has `.original` backup (10609 bytes)

**DECISION:** Keep current but needs update to use exit codes

**ACTION:**
```bash
# Backup current working version
cp .claude/hooks/pre-tool-use/02-design-check.py .claude/hooks/pre-tool-use/02-design-check.py.working

# Archive the .original
mv .claude/hooks/pre-tool-use/02-design-check.py.original .claude/hooks/_archive/20250805/

# TODO: Update the hook to replace:
# print(json.dumps({"decision": "block", "message": error_msg}))
# WITH:
# print(error_msg, file=sys.stderr)
# sys.exit(2)
```

---

#### Hook: `00a-dangerous-commands.py`
**Current State:**
- ✅ Main file exists (1913 bytes)
- ❌ Uses old format
- Has `.original` (622 bytes - much smaller)

**DECISION:** Keep current, archive .original

**ACTION:**
```bash
# Archive the smaller .original
mv .claude/hooks/pre-tool-use/00a-dangerous-commands.py.original .claude/hooks/_archive/20250805/

# TODO: Update to use exit code 2 instead of {"decision": "block"}
```

---

### Group 3: Duplicate Files to Clean

These have multiple versions that need consolidation:

#### Hook: `11-truth-enforcer.py`
**Files:**
- Main: 11-truth-enforcer.py (6625 bytes)
- .old: 11-truth-enforcer.py.old (6800 bytes)
- .original: 11-truth-enforcer.py.original (6488 bytes)

**ACTION:**
```bash
# Keep main, archive others
mv .claude/hooks/pre-tool-use/11-truth-enforcer.py.old .claude/hooks/_archive/20250805/
mv .claude/hooks/pre-tool-use/11-truth-enforcer.py.original .claude/hooks/_archive/20250805/
```

---

#### Hook: `19-tdd-enforcer.py`
**Files:**
- Main: 19-tdd-enforcer.py (5735 bytes)
- .backup: 19-tdd-enforcer.py.backup (5274 bytes)
- .original: 19-tdd-enforcer.py.original (5224 bytes)

**ACTION:**
```bash
# Keep main, archive others
mv .claude/hooks/pre-tool-use/19-tdd-enforcer.py.backup .claude/hooks/_archive/20250805/
mv .claude/hooks/pre-tool-use/19-tdd-enforcer.py.original .claude/hooks/_archive/20250805/
```

---

### Group 4: Post-Tool-Use Hooks

Most are compliant (20/30), but some need fixes:

#### Hook: `post-tool-use/04-next-command-suggester.py`
**Issue:** Missing 'tool_input' field
**Files:**
- Main: 9231 bytes
- .original: 31344 bytes (much larger!)

**DECISION:** Check if .original is better

```bash
# Compare the files
diff .claude/hooks/post-tool-use/04-next-command-suggester.py .claude/hooks/post-tool-use/04-next-command-suggester.py.original | head -50

# If .original is outdated, archive it:
mv .claude/hooks/post-tool-use/04-next-command-suggester.py.original .claude/hooks/_archive/20250805/
```

---

## 🔧 Hooks That Need Format Updates

These hooks work but need to be updated to official format:

### High Priority (Blocking hooks):
1. `02-design-check.py` - Change to exit code 2
2. `00a-dangerous-commands.py` - Change to exit code 2
3. `03-conflict-check.py` - Change to exit code 2
4. `06-requirement-drift-detector.py` - Change to exit code 2
5. `11-truth-enforcer.py` - Change to exit code 2
6. `14-prd-clarity.py` - Change to exit code 2
7. `16a-prp-validator.py` - Change to exit code 2

### Tool Name Updates Needed:
These check for `write_file` instead of `Write`:
1. `15-implementation-guide.py`
2. `05-multi-review-suggester.py`

---

## ✅ Success Criteria

After manual repair:
1. All 3 critical hooks installed and working
2. No syntax errors in any active hooks
3. All blocking hooks use exit code 2 (not {"decision": "block"})
4. All hooks check for "Write" not "write_file"
5. All backup/old versions archived
6. Each hook tested with official JSON format

---

## 📝 Testing Each Hook

After each fix, test with:

```bash
# Test blocking (should exit 2)
echo '{"tool_name":"Write","tool_input":{"file_path":"test.tsx","content":"bad content"}}' | python3 .claude/hooks/pre-tool-use/HOOKNAME.py
echo "Exit code: $?"

# Test non-blocking (should exit 0)
echo '{"tool_name":"Read","tool_input":{"file_path":"test.tsx"}}' | python3 .claude/hooks/pre-tool-use/HOOKNAME.py
echo "Exit code: $?"
```

---

**IMPORTANT:** Do NOT run any automated scripts. Go through each hook manually to ensure we keep the right version and update it properly.
