# 🚀 Master Workflow Guide - Claude Code Boilerplate v2.7.0

> **One Document to Rule Them All** - Your complete reference for maximizing the Claude Code Boilerplate system with Agent OS integration.

## Table of Contents
1. [Quick Command Reference](#quick-command-reference)
2. [First Time Setup](#first-time-setup)
3. [Existing Project Setup](#existing-project-setup) **(NEW!)**
4. [Daily Workflow](#daily-workflow)
5. [Feature Development Workflows](#feature-development-workflows)
6. [Testing & Validation](#testing--validation)
7. [Context Management](#context-management)
8. [Common Scenarios](#common-scenarios)
9. [Pro Tips & Best Practices](#pro-tips--best-practices)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Quick Command Reference

> **💡 NEW: Intelligent Next Command Suggestions!**  
> After every command, the system now suggests the most logical next steps.  
> No more wondering "what should I do next?" - just follow the guided workflow!

### Essential Daily Commands
```bash
/sr                    # Smart Resume - start every session with this
/ae                    # Analyze Existing - for existing projects (NEW!)
/cp load frontend      # Load context profile (frontend/backend/debug)
/bt list              # Check open bugs
/checkpoint           # Manual save current state
/help                 # Context-aware help
```

### Starting Work
```bash
# New Projects
/init-project         # Initialize new project
/fw start 123         # Start from GitHub issue #123

# Existing Projects (NEW!)
/ae                   # Analyze existing codebase
/mds analyze          # Check design compliance
/chain onboard-existing # Complete onboarding

# Feature Development
/create-prp feature   # Generate PRP for clear features
/prd feature          # Generate PRD for exploratory work
/gt feature           # Generate tasks from PRD
/pt feature           # Process tasks one by one
```

### Development Commands
```bash
/cc ComponentName     # Create component with design validation
/ctf FormName         # Create secure tracked form
/vd                   # Validate design system compliance
/mds migrate          # Migrate to strict design (NEW!)
/deps check Button    # Check component dependencies
/exists Button        # Check if component exists (auto-runs on create)
```

### Testing Commands
```bash
/tdd-workflow feature # Start TDD workflow
/prd-tests feature    # Generate tests from PRD
/tr current           # Run tests for current file
/btf                  # Browser test flow with Playwright
/verify               # Verify completion claims
/verify --full        # Full verification with coverage
```

### Validation & Quality
```bash
/prp-execute feature  # Run PRP validation loops
/sv check 2           # Check stage 2 completion
/grade                # Grade implementation against PRD
/sc                   # Security check
/validate-async       # Check async patterns
```

### Collaboration
```bash
/cti "Title"          # Capture Claude response to GitHub issue
/fw complete          # Create PR with full context
/orch feature         # Orchestrate multi-agent work
/specs extract        # Save successful patterns
```

### Advanced Features
```bash
/ut complex problem   # UltraThink - 32k+ token deep analysis
/vp feature           # Visual planning with screenshots
/research topic       # Create/update research document
/dmoff               # Disable design mode temporarily
/chain [name]         # Run command chains
```

---

## 🚀 First Time Setup

### 1. Clone and Initialize YOUR Project
```bash
# Clone boilerplate to YOUR project
git clone https://github.com/bearingfruitco/claude-code-boilerplate.git my-awesome-app
cd my-awesome-app

# Remove boilerplate git history
rm -rf .git
git init

# Create YOUR GitHub repo
gh repo create my-awesome-app --private --source=.

# Run quick setup
chmod +x scripts/quick-setup.sh
./scripts/quick-setup.sh

# Setup PRP system
chmod +x setup-prp.sh
./setup-prp.sh
```

### 2. Configure Agent OS Standards (NEW!)
```bash
# Customize your global standards
edit ~/.agent-os/standards/design-system.md    # Your design rules
edit ~/.agent-os/standards/tech-stack.md       # Your tech preferences
edit ~/.agent-os/standards/best-practices.md   # Your dev philosophy

# These will be used across ALL projects
```

### 3. Install GitHub Apps
1. **CodeRabbit**: [github.com/marketplace/coderabbit](https://github.com/marketplace/coderabbit)
   - Install on YOUR repo (not boilerplate)
   - Configure with `.coderabbit.yaml`

2. **Claude Code Bot**: [github.com/apps/claude](https://github.com/apps/claude)
   - Install on YOUR repo
   - Grant code, issues, PRs permissions

### 4. Update Configuration
```bash
# Edit .claude/project-config.json
{
  "repository": {
    "owner": "YOUR_USERNAME",
    "name": "my-awesome-app",
    "branch": "main"
  }
}
```

### 5. Start Claude Code
```bash
# Open in Claude Code
claude .

# Initialize system
/init

# Initialize YOUR project (not boilerplate!)
/init-project

# Generate GitHub issues for your project
/gi PROJECT
```

### 6. Verify Setup
```bash
# Create test PR with design violation
git checkout -b test/setup
echo '<div className="text-sm">Test</div>' > test.tsx
git add . && git commit -m "Test setup"
git push origin test/setup

# Create PR - CodeRabbit should review within 2-3 minutes
```

---

## 🏢 Existing Project Setup (NEW!)

### 1. Add Claude Code to Existing Project
```bash
cd your-existing-project

# Add Claude Code system
curl -sSL https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/scripts/add-to-existing.sh | bash -s full

# Open in Claude Code
claude .
```

### 2. Analyze Your Codebase
```bash
# Run the analyze command
/ae

# This will:
# - Detect your tech stack
# - Find existing features
# - Create mission/roadmap docs
# - Set up .agent-os structure
# - Generate migration report
```

### 3. Check Design Compliance
```bash
# Analyze design violations
/mds analyze

# Review report
cat .agent-os/DESIGN_MIGRATION_REPORT.md

# If you want to migrate:
/mds migrate
```

### 4. Complete Onboarding
```bash
# Run full onboarding chain
/chain onboard-existing

# Or step by step:
/analyze-existing      # If not done yet
/mds analyze          # Check design
/create-prd-from-existing main-features
/task-ledger sync     # Import tasks
/sr                   # Load everything
```

### 5. Verify Integration
```bash
# Test standards loading
/sr

# Should show:
# ✓ Loaded: design-system.md
# ✓ Loaded: tech-stack.md
# ✓ Loaded: best-practices.md

# Test design validation
/vd
```

---

## 📅 Daily Workflow

### Morning Startup Sequence
```bash
# 1. Open project in Claude Code
claude .

# 2. Smart resume (ALWAYS start with this)
/sr

# This shows:
# - Current branch and issue
# - Modified files
# - Active TODOs
# - Open bugs
# - Active PRPs
# - Loaded standards (NEW!)
# - Last checkpoint

# 3. Check active work
ls PRPs/active/           # Active PRPs
/bt list --open          # Open bugs
/todo                    # Current TODOs
ls .agent-os/product/    # Product docs (NEW!)

# 4. Load appropriate context
/cp load frontend        # Or backend, debug, etc.
```

### Choosing Your Workflow

```mermaid
graph TD
    A[New Work Item] --> B{Existing Project?}
    B -->|Yes| C[/ae first]
    B -->|No| D{Have clear specs?}
    
    D -->|Yes| E{Have code examples?}
    D -->|No| F[Use PRD Workflow]
    
    E -->|Yes| G[Use PRP Workflow]
    E -->|No| H{Is it exploratory?}
    
    H -->|Yes| F
    H -->|No| I[Create simple PRP]
    
    C --> J[/mds analyze]
    J --> D
```

### PRP Workflow (Recommended for Clear Features)
```bash
# 1. Start from issue
/fw start 123

# 2. Create PRP
/create-prp user-authentication

# 3. Review and validate
/prp-validate user-authentication

# 4. Execute with validation
/prp-execute user-authentication --level 1

# 5. Process tasks
/pt user-authentication

# 6. Verify and complete
/verify --full
/fw complete
```

### PRD Workflow (For Exploratory Work)
```bash
# 1. Create PRD
/prd new-feature

# 2. Add async requirements
/prd-async new-feature

# 3. Generate tests from PRD
/prd-tests new-feature

# 4. Generate tasks
/gt new-feature

# 5. Process with TDD
/tdd-workflow new-feature
```

---

## 🧪 Testing & Validation

### Multi-Level Validation System
```bash
# Level 1: Code Quality (instant)
/vd                    # Design validation
/lint:fix             # Auto-fix issues
/typecheck            # TypeScript check

# Level 2: Component Testing
/tr current           # Test current file
/tr:components        # All component tests
/tr:hooks            # Hook tests

# Level 3: Integration Testing
/btf                  # Browser test flow
/test:e2e            # E2E tests
/test:api            # API tests

# Level 4: Production Readiness
/lighthouse          # Performance audit
/sc all              # Security check
/grade               # Implementation grading
```

### TDD Workflow
```bash
# 1. Start TDD mode
/tdd-workflow feature-name

# 2. Write failing test
# Claude writes test first

# 3. Implement minimum code
# Claude implements to pass

# 4. Refactor
# Claude improves code

# 5. Verify
/verify --tdd
```

---

## 🧠 Context Management

### Standards Management (NEW!)
```bash
# View standards
cat .agent-os/standards/design-system.md
cat .agent-os/standards/tech-stack.md
cat .agent-os/standards/best-practices.md

# Standards are automatically loaded on:
/sr                    # Smart resume
/init-project         # New projects
/ae                   # Existing projects
```

### Context Profiles
```bash
# Load focused context
/cp load frontend      # Frontend work
/cp load backend       # Backend work
/cp load debug         # Debugging mode
/cp load testing       # Test writing

# Create custom profile
/cp create mobile-ui   # Custom profile

# List profiles
/cp list
```

### Research Documents
```bash
# Create research
/research auth-strategy

# Update existing
/research update auth-strategy

# Search research
/research search authentication

# Include in context
/research context auth-strategy
```

### Checkpoints
```bash
# Manual checkpoint
/checkpoint "Before refactor"

# List checkpoints
/checkpoint list

# Restore checkpoint
/checkpoint restore 3
```

---

## 🎯 Common Scenarios

### Scenario: Onboarding Existing React Project
```bash
# 1. Add system
cd my-react-app
curl -sSL https://raw.githubusercontent.com/bearingfruitco/claude-code-boilerplate/main/scripts/add-to-existing.sh | bash -s full

# 2. Open and analyze
claude .
/ae

# 3. Check design
/mds analyze

# 4. Migrate if needed
/mds migrate

# 5. Start working
/fw start 456
```

### Scenario: Creating Secure Form
```bash
# 1. Create tracked form
/ctf ContactForm

# This generates:
# - Form component with validation
# - Event tracking hooks
# - TCPA compliance
# - Loading states
# - Error handling

# 2. Validate
/vd
/sc form

# 3. Test
/tr ContactForm
```

### Scenario: Debugging Production Issue
```bash
# 1. Load debug context
/cp load debug

# 2. Analyze with UltraThink
/ut "Users report form submissions failing intermittently"

# 3. Check async patterns
/validate-async

# 4. Review event logs
/query-logs --errors --last-hour

# 5. Create fix
/mt "Add retry logic to form submission"
```

### Scenario: Multi-Agent Feature
```bash
# 1. Large feature needing parallel work
/gt authentication-system

# 2. Check if orchestration helps
# System suggests: "Save ~45 minutes with parallel execution"

# 3. Orchestrate
/orch authentication-system --agents=3

# 4. Monitor progress
/sas
/ov
```

---

## 💡 Pro Tips & Best Practices

### 1. Always Start with /sr
```bash
# BAD: Jumping straight into work
/pt

# GOOD: Load context first
/sr
/pt
```

### 2. Use Standards Effectively
```bash
# Customize for your team
edit ~/.agent-os/standards/best-practices.md

# Override for specific project
mkdir .agent-os/standards
echo "# Project-specific rules" > .agent-os/standards/overrides.md
```

### 3. Chain Commands for Efficiency
```bash
# Morning routine
/chain daily-startup

# Pre-PR validation
/chain pre-pr

# Feature completion
/chain safe-feature-complete
```

### 4. Trust the Validation
```bash
# Don't skip levels
/prp-execute --level 1  # Do this
/prp-execute --level 2  # Then this
/prp-execute --level 3  # Then this
/prp-execute --level 4  # Finally this
```

### 5. Use Visual Planning for UI
```bash
# Screenshot current state
# Paste with Ctrl+V
/vp dashboard-redesign

# Claude analyzes and suggests improvements
```

### 6. Let Hooks Work for You
```bash
# Safe operations auto-approve
# No more "Can I read this file?" interruptions

# Design violations block immediately
# No more fixing later

# Standards load automatically
# No more copy-pasting rules
```

---

## 🔧 Troubleshooting

### Issue: Design Violations Keep Appearing
```bash
# Solution 1: Check if design mode is on
/dmon

# Solution 2: Run migration
/mds analyze
/mds migrate

# Solution 3: Update standards
edit .agent-os/standards/design-system.md
```

### Issue: Context Lost After Compaction
```bash
# Solution: Smart resume restores everything
/sr

# Prevention: Regular checkpoints
/checkpoint "Before big feature"
```

### Issue: Tests Failing Mysteriously
```bash
# Solution 1: Check async patterns
/validate-async

# Solution 2: Review recent changes
/deps scan

# Solution 3: Full verification
/verify --full --debug
```

### Issue: Can't Find Command
```bash
# Solution 1: Use help
/help [partial-command]

# Solution 2: Check aliases
/help aliases | grep [what-you-want]

# Solution 3: Browse all commands
ls .claude/commands/
```

### Issue: Existing Project Won't Analyze
```bash
# Solution 1: Check you're in root
pwd  # Should show project root

# Solution 2: Try manual setup
mkdir -p .agent-os/product
/init-project  # Then manually edit

# Solution 3: Check permissions
ls -la .claude/
```

---

## 🎉 You're Ready!

With this guide, you have everything needed to maximize the Claude Code Boilerplate system. Remember:

1. **Start every session with `/sr`**
2. **Use `/ae` for existing projects**
3. **Trust the automated validations**
4. **Let next command suggestions guide you**
5. **Customize standards for your team**

The system handles the HOW so you can focus on the WHAT. Happy building! 🚀
