# Hook System Repair Plan

## 🚨 CRITICAL ISSUES IDENTIFIED

### Summary
- **78 total issues** found in hook system
- **3 missing hooks** blocking all operations
- **70 duplicate hooks** causing confusion
- **1 broken hook** needing repair
- **4 orphaned files** without main versions

## 📋 IMMEDIATE ACTIONS REQUIRED

### Phase 1: Emergency Fix (Do Now)
Run the automated fix script to restore basic functionality:

```bash
# 1. Create backup first
cp -r .claude/hooks .claude/hooks.backup.$(date +%Y%m%d_%H%M%S)

# 2. Run the fix script
./scripts/fix-hooks.sh

# 3. Test basic operations
python3 .claude/hooks/pre-tool-use/02-design-check.py
```

### Phase 2: Manual Review (Next 30 minutes)

#### A. Fix the Broken PII Protection Hook
The `07-pii-protection.py` hook is marked as broken and needs manual repair:

```bash
# Review the broken file
cat .claude/hooks/pre-tool-use/07-pii-protection.py.broken

# Compare with original
diff .claude/hooks/pre-tool-use/07-pii-protection.py.broken \
     .claude/hooks/pre-tool-use/07-pii-protection.py.original

# Fix and test
# [Manual intervention needed to fix Python errors]
```

#### B. Handle Prefixbatch Files
Several hooks have `.prefixbatch` versions that might be newer:
- Check if these are improved versions
- Compare with current versions
- Decide which to keep

### Phase 3: Cleanup & Organization (Next Hour)

#### Task Breakdown:

##### Task 1: Archive Old Versions
```bash
# Create archive directory with timestamp
mkdir -p .claude/hooks/_archive/20250805

# Move all old versions
find .claude/hooks -type f \( \
  -name "*.original" -o \
  -name "*.broken" -o \
  -name "*.backup" -o \
  -name "*.old" -o \
  -name "*.prefixbatch" \
\) -exec mv {} .claude/hooks/_archive/20250805/ \;
```

##### Task 2: Validate All Hooks
```bash
# Create validation script
cat > scripts/validate-hooks.py << 'EOF'
#!/usr/bin/env python3
import os
import sys
import json
from pathlib import Path

def validate_hooks():
    settings_file = Path(".claude/settings.json")
    with open(settings_file) as f:
        settings = json.load(f)
    
    errors = []
    for hook_type, configs in settings.get("hooks", {}).items():
        if isinstance(configs, list):
            for config in configs:
                if "hooks" in config:
                    for hook in config["hooks"]:
                        if hook.get("type") == "command" and "python3" in hook.get("command", ""):
                            parts = hook["command"].split()
                            if len(parts) > 1:
                                file_path = parts[1]
                                if not Path(file_path).exists():
                                    errors.append(f"Missing: {file_path}")
                                else:
                                    # Try to import the file
                                    try:
                                        compile(open(file_path).read(), file_path, 'exec')
                                        print(f"✓ Valid: {file_path}")
                                    except SyntaxError as e:
                                        errors.append(f"Syntax error in {file_path}: {e}")
    
    if errors:
        print("\n❌ Errors found:")
        for error in errors:
            print(f"  - {error}")
        return 1
    else:
        print("\n✅ All hooks valid!")
        return 0

if __name__ == "__main__":
    sys.exit(validate_hooks())
EOF

chmod +x scripts/validate-hooks.py
python3 scripts/validate-hooks.py
```

##### Task 3: Update Settings.json
Remove references to non-existent hooks and ensure all paths are correct.

##### Task 4: Create Hook Documentation
```bash
# Generate hook documentation
cat > .claude/hooks/HOOKS_STATUS.md << 'EOF'
# Hook System Status

## Current State (as of 2025-08-05)

### Pre-Tool-Use Hooks (Active)
- ✅ 00-auto-approve-safe-ops.py - Auto-approves safe operations
- ✅ 00a-dangerous-commands.py - Blocks dangerous commands
- ✅ 00a-snapshot-manager.py - Manages snapshots
- ✅ 01-collab-sync.py - Team collaboration sync
- ✅ 02-design-check.py - Design system enforcement
- ✅ 03-conflict-check.py - Conflict detection
- ✅ 04-actually-works.py - "Actually Works" protocol
- ✅ 05-code-quality.py - Code quality checks
- ✅ 05a-auto-context-inclusion.py - Auto context loading
- ✅ 05b-prp-context-loader.py - PRP context loading
- ✅ 05c-tdd-context-loader.py - TDD context loading
- ✅ 06-requirement-drift-detector.py - Requirements tracking
- ✅ 06a-biome-lint.py - Biome linting
- ✅ 07-pii-protection.py - PII protection
- ✅ 08-evidence-language.py - Evidence language enforcement
- ✅ 08a-async-patterns.py - Async pattern validation
- ✅ 09-auto-persona.py - Auto persona selection
- ✅ 10-hydration-guard.py - Hydration error prevention
- ✅ 11-truth-enforcer.py - Truth enforcement
- ✅ 12-deletion-guard.py - Deletion protection
- ✅ 13-import-validator.py - Import validation
- ✅ 14-prd-clarity.py - PRD clarity checks
- ✅ 14a-creation-guard.py - Creation guard
- ✅ 15-implementation-guide.py - Implementation guidance
- ✅ 15a-dependency-tracker.py - Dependency tracking
- ✅ 16-tcpa-compliance.py - TCPA compliance
- ✅ 16a-prp-validator.py - PRP validation
- ✅ 17-ai-docs-check.py - AI docs verification
- ✅ 17-architecture-enforcer.py - Architecture enforcement
- ✅ 17-performance-budget-enforcer.py - Performance budgets
- ✅ 17-test-generation-enforcer.py - Test generation
- ✅ 18-auto-parallel-agents.py - Parallel agent orchestration
- ✅ 18-security-first-enforcer.py - Security-first development
- ✅ 19-auto-rls-generator.py - Auto RLS generation
- ✅ 19-tdd-enforcer.py - TDD enforcement
- ✅ 19a-auto-test-spawner.py - Auto test spawning
- ✅ 20-feature-awareness.py - Feature awareness
- ✅ 20-feature-state-guardian.py - Feature state protection
- ✅ 21-branch-controller.py - Branch control
- ✅ 21-docs-first-enforcer.py - Documentation-first
- ✅ 21-security-command-enhancer.py - Security enhancement
- ✅ 22-api-docs-generator.py - API docs generation
- ✅ 22-security-validator.py - Security validation
- ✅ 23-a11y-enforcer.py - Accessibility enforcement
- ✅ 24-environment-guard.py - Environment protection
- ✅ 25-deployment-validator.py - Deployment validation
- ✅ 26-database-environment-check.py - Database env check

### Post-Tool-Use Hooks (Active)
[List all active post-tool-use hooks]

### Issues Fixed
- Restored 07-pii-protection.py from .original
- Restored 16-tcpa-compliance.py from .original  
- Restored 22-security-validator.py from .original
- Archived 70 duplicate versions
- Fixed 1 broken hook

### Archive Location
All old versions moved to: `.claude/hooks/_archive/20250805/`
EOF
```

## 🎯 GITHUB ISSUES TO CREATE

### Issue 1: Critical Hook System Repair
**Title:** 🚨 Critical: Missing Claude Code hooks blocking operations  
**Priority:** P0 - Critical  
**Labels:** bug, critical, hooks  
**Assignee:** @shawnsmith  

**Tasks:**
- [ ] Run `./scripts/fix-hooks.sh`
- [ ] Fix 07-pii-protection.py.broken manually
- [ ] Test all hook operations
- [ ] Verify no blocking errors

### Issue 2: Hook System Cleanup
**Title:** ⚠️ High: Duplicate hook versions causing confusion  
**Priority:** P1 - High  
**Labels:** bug, high, hooks, cleanup  

**Tasks:**
- [ ] Archive all .original files
- [ ] Archive all .broken files  
- [ ] Archive all .backup files
- [ ] Archive all .old files
- [ ] Review .prefixbatch files
- [ ] Update hook documentation

### Issue 3: Hook Validation System
**Title:** 🔧 Medium: Create hook validation and monitoring  
**Priority:** P2 - Medium  
**Labels:** enhancement, hooks, monitoring  

**Tasks:**
- [ ] Create validation script
- [ ] Add pre-commit hook for validation
- [ ] Add CI/CD check for hooks
- [ ] Create hook health dashboard

### Issue 4: Hook System Documentation
**Title:** 📚 Low: Document hook system architecture  
**Priority:** P3 - Low  
**Labels:** documentation, hooks  

**Tasks:**
- [ ] Document each hook's purpose
- [ ] Create troubleshooting guide
- [ ] Add hook development guide
- [ ] Create hook testing framework

## 🚀 RECOMMENDED EXECUTION ORDER

1. **NOW (Emergency):**
   ```bash
   ./scripts/fix-hooks.sh
   ```

2. **Next 15 minutes:**
   - Fix 07-pii-protection.py manually
   - Test basic file operations

3. **Next 30 minutes:**
   - Run validation script
   - Archive old versions
   - Update documentation

4. **Next Hour:**
   - Complete cleanup
   - Create GitHub issues
   - Test all workflows

## ✅ SUCCESS CRITERIA

The hook system is considered fixed when:
1. No errors on file operations
2. All hooks in settings.json exist and are valid Python
3. No duplicate versions in main directories
4. All old versions archived
5. Documentation updated
6. Validation script passes

## 📊 METRICS TO TRACK

- Hook execution success rate
- Average hook execution time
- Number of hook errors per day
- Hook coverage (% of operations with hooks)

---

**Next Step:** Run `./scripts/fix-hooks.sh` immediately to restore basic functionality.
