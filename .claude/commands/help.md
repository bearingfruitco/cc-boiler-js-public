# Help - Enhanced Command Reference

Show context-aware help for all commands and workflows.

## Usage

```bash
/help [topic]
/h [topic]     # short alias
/? [topic]     # shorter alias

# Topics: all, new, commands, workflows, aliases, prd, testing, security
```

## 🆕 NEW FEATURES (Latest Additions)

### Truth & Existence Commands
- `/facts [category]` - Show established project values that cannot be changed
- `/exists [name]` - Check if component/function/route already exists
- `/truth` - Alias for /facts (see what's established)
- `/check` - Alias for /exists

### Field Registry Generation
- `/field-generate schemas` - Generate Zod validation from registry
- `/field-generate factories` - Generate test data factories
- `/field-generate masking` - Generate PII masking functions
- `/fg [type]` - Short alias for field-generate

### New Safety Chains
- `/chain safe-commit` - Validate before committing (facts → design → lint → test)
- `/chain field-sync` - Regenerate all field-based code
- `/chain pre-component` - Check before creating components

### New Hook Protections (Automatic)
- **Hydration Guard** - Prevents Next.js SSR errors
- **Truth Enforcer** - Blocks changes to established values
- **Deletion Guard** - Warns before significant deletions
- **Import Validator** - Fixes import path issues

## 📚 Command Categories

### 1. Context & State Management
```bash
/smart-resume (sr)         # Restore full context
/checkpoint (cp)           # Save current state
/context-grab (cg)         # Capture working context
/compress-context          # Reduce token usage
/compact-prepare          # Prepare for session end
```

### 2. PRD & Task Workflow
```bash
/create-prd (prd)         # Generate Product Requirements
/generate-tasks (gt)      # Break PRD into tasks
/process-tasks (pt)       # Work through tasks
/task-status (ts)         # View progress
/task-board (tb)          # Visual task view
/verify-task (vt)         # Confirm completion
```

### 3. Development Commands
```bash
/create-component (cc)    # Create validated component
/validate-design (vd)     # Check design compliance
/create-tracked-form (ctf) # Secure form with tracking
/exists [name]            # Check before creating
/facts [category]         # Show established values
```

### 4. Testing & Quality
```bash
/browser-test-flow (btf)  # Browser automation tests
/test-runner (tr)         # Run unit tests
/lint-check (lc)          # Biome linting
/audit-form-security (afs) # Security audit
```

### 5. Team & Collaboration
```bash
/feature-workflow (fw)    # GitHub issue workflow
/work-status (ws)         # Team activity
/todo (td)                # Task management
/change-log               # Recent changes
```

### 6. Security & Compliance
```bash
/security-check (sc)      # Security audit
/audit-form-security      # Form security check
/field-generate           # Generate from registry
/facts env                # Show environment vars
```

### 7. Multi-Agent Orchestration
```bash
/orchestrate-agents (orch) # Start multi-agent work
/spawn-agent (spawn)      # Create specialized agent
/persona (p)              # Switch persona mode
/sub-agent-status (sas)   # Check agent progress
```

## 🔄 Workflow Examples

### Starting New Feature (Complete Flow)
```bash
# 1. Create issue
gh issue create --title "User Dashboard"

# 2. Start feature
/fw start 23

# 3. Check what exists
/facts                    # See constraints
/exists Dashboard         # Check if exists

# 4. Create PRD
/prd user-dashboard

# 5. Generate and process tasks
/gt user-dashboard
/pt user-dashboard

# 6. Safe development
/chain pre-component      # Before creating
/cc feature Dashboard     # Create component
/chain safe-commit       # Before committing

# 7. Complete
/btf dashboard
/fw complete 23
```

### Daily Development
```bash
# Morning
/sr                      # Resume context
/facts                   # See constraints
/ts                      # Check tasks

# Before creating
/exists LoginForm        # Check first
/pc LoginForm           # Full pre-check

# Safe commits
/chain safe-commit      # Validate everything
```

### Form Development
```bash
/exists ContactForm
/ctf ContactForm --vertical=debt
/fg schemas             # Generate validation
/fg factories           # Generate test data
/afs components/forms/ContactForm.tsx
```

## 💡 Command Aliases

### Most Used
- `sr` → smart-resume
- `cc` → create-component
- `vd` → validate-design
- `fw` → feature-workflow
- `prd` → create-prd
- `gt` → generate-tasks
- `pt` → process-tasks

### New Aliases
- `truth` → facts
- `check` → exists
- `fg` → field-generate
- `sc` → safe-commit (chain)
- `fs` → field-sync (chain)
- `pc` → pre-component (chain)

## 🛡️ Automatic Protections

### What Hooks Prevent (No Action Needed)
1. **Design violations** - Wrong CSS classes blocked
2. **PII exposure** - No sensitive data in logs
3. **Hydration errors** - SSR issues caught
4. **Import mistakes** - Path errors fixed
5. **Truth violations** - Can't change established values
6. **Accidental deletions** - Warnings before removal

## 📊 Quick Reference Card

```
DAILY ESSENTIALS        BEFORE CREATING        SAFE DEVELOPMENT
/sr    - resume         /exists  - check       /chain safe-commit
/facts - constraints    /pc      - pre-check   /vd - validate
/ts    - tasks         /facts   - values      /btf - test

PRD WORKFLOW           TESTING                 FIELD REGISTRY
/prd   - create PRD    /btf - browser test    /fg schemas
/gt    - gen tasks     /tr  - unit test       /fg factories  
/pt    - process       /afs - security        /fg masking
```

## 🚀 Getting More Help

```bash
/help workflows          # Detailed workflow guides
/help aliases           # All command shortcuts
/help new               # Latest features
/help [command]         # Specific command help
```

The system prevents common mistakes automatically - focus on building!