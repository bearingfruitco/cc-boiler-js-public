# Hook System Repair - Issues and Tasks

## 🚨 Critical Issues Found

After detailed analysis, here's what we discovered:

### Problem Summary
1. **3 critical hooks missing** - blocking all file operations
2. **2 hooks have corrupted syntax** - both versions broken
3. **1 hook has valid backup** - can be restored
4. **70 duplicate hook files** - causing confusion
5. **Mixed file versions** - .original, .broken, .backup, .old, .prefixbatch

### Root Cause
The hooks appear to have been corrupted during an automated update or merge process. The presence of `.prefixbatch` files suggests a batch processing tool was used but didn't complete properly.

---

## 📋 GitHub Issues to Create

### Issue #1: 🚨 P0 - Critical Hooks Blocking All Operations
**Title:** Fix missing/broken hooks blocking Claude Code operations  
**Labels:** `bug`, `critical`, `hooks`, `blocking`  
**Assignee:** @shawnsmith  
**Priority:** P0 - URGENT  

**Description:**
Three critical hooks are missing from the pre-tool-use directory, causing all file operations to fail with hook errors.

**Affected Hooks:**
- `07-pii-protection.py` - BOTH versions have syntax errors
- `16-tcpa-compliance.py` - .original has syntax error  
- `22-security-validator.py` - .original is valid

**Tasks:**
- [x] Create backup of current hooks directory
- [x] Create fixed version of 07-pii-protection.py
- [x] Create fixed version of 16-tcpa-compliance.py
- [ ] Restore 22-security-validator.py from .original
- [ ] Test all three hooks for syntax validity
- [ ] Verify file operations work without errors
- [ ] Update settings.json if needed

**Implementation:**
```bash
# Run the repair script
./scripts/repair-critical-hooks.sh

# Test the repairs
python3 .claude/hooks/pre-tool-use/07-pii-protection.py
python3 .claude/hooks/pre-tool-use/16-tcpa-compliance.py
python3 .claude/hooks/pre-tool-use/22-security-validator.py
```

---

### Issue #2: ⚠️ P1 - Clean Up Duplicate Hook Versions
**Title:** Remove duplicate hook versions and establish single source of truth  
**Labels:** `cleanup`, `technical-debt`, `hooks`  
**Assignee:** @shawnsmith  
**Priority:** P1 - High  

**Description:**
70 hooks have multiple versions (.original, .broken, .backup, .old, .prefixbatch) making it unclear which version is active.

**Affected Directories:**
- `pre-tool-use/` - 35 duplicates
- `post-tool-use/` - 18 duplicates
- `pre-compact/` - 2 duplicates
- `user-prompt-submit/` - 2 duplicates
- `stop/` - 5 duplicates
- `sub-agent-stop/` - 3 duplicates
- `notification/` - 5 duplicates

**Tasks:**
- [ ] Run detailed analysis: `python3 scripts/analyze-hooks-detailed.py`
- [ ] Review each duplicate group
- [ ] Compare file sizes and modification dates
- [ ] Test syntax validity of each version
- [ ] Select best version for each hook
- [ ] Archive old versions to `.claude/hooks/_archive/`
- [ ] Update documentation

**Decision Criteria:**
1. Valid Python syntax (no SyntaxError)
2. Has `__main__` block
3. Larger file size (usually more complete)
4. More recent modification date
5. Not marked as .broken

---

### Issue #3: 🔧 P2 - Fix Hook Syntax Errors
**Title:** Repair hooks with syntax errors  
**Labels:** `bug`, `hooks`, `syntax-error`  
**Priority:** P2 - Medium  

**Description:**
Multiple hooks have syntax errors in their .original versions, suggesting corruption during updates.

**Hooks with Syntax Errors:**
- `01-collab-sync.py.original` - SYNTAX_ERR
- `02-design-check.py.original` - SYNTAX_ERR
- `03-conflict-check.py.original` - SYNTAX_ERR
- `04-actually-works.py.original` - SYNTAX_ERR
- `05-code-quality.py.original` - SYNTAX_ERR
- `05a-auto-context-inclusion.py.original` - SYNTAX_ERR
- `06-requirement-drift-detector.py.original` - SYNTAX_ERR
- `06a-biome-lint.py.original` - SYNTAX_ERR
- `07-pii-protection.py.original` - SYNTAX_ERR (line 243)
- `07-pii-protection.py.broken` - SYNTAX_ERR (line 208)
- `16-tcpa-compliance.py.original` - SYNTAX_ERR (line 32)

**Tasks:**
- [ ] Identify all hooks with syntax errors
- [ ] Determine if current versions are working
- [ ] Fix or recreate broken hooks
- [ ] Test each repaired hook
- [ ] Document changes made

---

### Issue #4: 📚 P3 - Document Hook System
**Title:** Create comprehensive hook system documentation  
**Labels:** `documentation`, `hooks`  
**Priority:** P3 - Low  

**Description:**
Document the hook system architecture, each hook's purpose, and maintenance procedures.

**Tasks:**
- [ ] Document each hook's purpose and functionality
- [ ] Create troubleshooting guide
- [ ] Document hook development best practices
- [ ] Create testing framework for hooks
- [ ] Document version management strategy
- [ ] Create hook health monitoring dashboard

**Deliverables:**
- `.claude/hooks/README.md` - Overview and architecture
- `.claude/hooks/HOOKS_CATALOG.md` - List of all hooks with descriptions
- `.claude/hooks/TROUBLESHOOTING.md` - Common issues and fixes
- `.claude/hooks/DEVELOPMENT.md` - How to create new hooks

---

### Issue #5: 🛡️ P2 - Create Hook Validation System
**Title:** Implement automated hook validation and testing  
**Labels:** `enhancement`, `testing`, `hooks`  
**Priority:** P2 - Medium  

**Description:**
Create automated validation to prevent hook corruption and ensure all hooks remain functional.

**Tasks:**
- [ ] Create `validate-hooks.py` script
- [ ] Add pre-commit hook for validation
- [ ] Create CI/CD pipeline check
- [ ] Implement hook health monitoring
- [ ] Create automated backup system
- [ ] Add version control for hooks

**Validation Checks:**
- Python syntax validity
- Required functions exist
- Proper JSON input/output
- Performance benchmarks
- Error handling

---

## 🎯 Immediate Action Plan

### Step 1: Fix Critical Hooks (NOW)
```bash
# 1. Run the repair script
chmod +x scripts/repair-critical-hooks.sh
./scripts/repair-critical-hooks.sh

# 2. Test the repairs
python3 -c "import sys; sys.path.insert(0, '.claude/hooks/pre-tool-use'); import importlib; importlib.import_module('07-pii-protection')"
```

### Step 2: Clean Up Duplicates (Next 30 min)
```bash
# 1. Run detailed analysis
python3 scripts/analyze-hooks-detailed.py > hook-analysis.txt

# 2. Review recommendations
less hook-analysis.txt

# 3. Archive old versions
mkdir -p .claude/hooks/_archive/20250805
find .claude/hooks -type f \( -name "*.original" -o -name "*.broken" -o -name "*.backup" -o -name "*.old" \) -exec mv {} .claude/hooks/_archive/20250805/ \;
```

### Step 3: Validate All Hooks (Next hour)
```bash
# Create and run validation script
python3 scripts/validate-all-hooks.py
```

---

## 📊 Success Metrics

The hook system will be considered repaired when:

1. **No Hook Errors** - File operations complete without hook failures
2. **Single Versions** - Each hook has only one active version
3. **Valid Syntax** - All hooks pass Python syntax validation
4. **Documented** - Each hook's purpose is documented
5. **Tested** - All hooks have been manually tested
6. **Archived** - Old versions moved to _archive directory

---

## 🔍 Lessons Learned

1. **Always test hooks after updates** - Syntax errors can block all operations
2. **Maintain single source of truth** - Multiple versions cause confusion
3. **Use version control** - Track changes to hooks over time
4. **Implement validation** - Catch errors before they reach production
5. **Document everything** - Hook purposes and dependencies

---

## 📅 Timeline

- **NOW**: Fix 3 critical hooks (15 min)
- **Today**: Clean up all duplicates (2 hours)
- **This Week**: Complete documentation (4 hours)
- **Next Week**: Implement validation system (8 hours)

---

**Created:** 2025-08-05  
**Author:** Claude + @shawnsmith  
**Status:** In Progress
