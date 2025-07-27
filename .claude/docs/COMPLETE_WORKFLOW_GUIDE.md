# 🚀 Claude Code v2.8.0 Complete Workflow Guide

## Table of Contents
1. [Starting Fresh vs Existing Projects](#starting-fresh-vs-existing-projects)
2. [Core Workflow: Plan → Execute → Validate → Ship](#core-workflow)
3. [Task & Issue Management](#task--issue-management)
4. [Recovery & Rollback](#recovery--rollback)
5. [Command Reference](#quick-command-reference)
6. [Real Project Walkthrough](#real-project-walkthrough)

---

## Starting Fresh vs Existing Projects

### 🆕 Starting a New Project

```bash
# 1. Initialize project structure
/init-project my-app
# Creates: Next.js setup, folder structure, configs

# 2. Set up your project vision
/create-prd main
# Interactive PRD creation with AI assistance

# 3. Generate initial tasks
/generate-tasks
# Creates task breakdown from PRD

# 4. Check your roadmap
/task-status
# Shows all tasks, priorities, dependencies
```

### 📦 Dropping into Existing Project

```bash
# 1. Full system analysis
/analyze-existing full
# Scans: structure, dependencies, patterns, tech stack

# 2. Smart resume (understands context)
/smart-resume
# Loads: previous state, active branch, current tasks

# 3. Migrate to design system (if needed)
/migrate-to-strict-design analyze
# Checks: design compliance, suggests fixes

# 4. Create PRD from existing code
/create-prd-from-existing main-features
# Reverse-engineers PRD from codebase
```

---

## Core Workflow

### 📋 Phase 1: Planning & Capture

```bash
# Create your vision
/create-prd authentication-system

# Or capture ideas on the fly
"I need a user auth system with email/password, OAuth, and 2FA"
/capture-to-issue
# → Creates: issues/AUTH-001-user-authentication.md

# Generate structured tasks
/generate-tasks
# → Creates: .claude/tasks/*.md files
# → Updates: .claude/task-ledger.json

# View your roadmap
/task-board
```

**Where tasks live:**
- `.claude/tasks/` - Individual task files
- `.claude/task-ledger.json` - Master task registry
- `.claude/issues/` - Captured ideas/issues

### 🔨 Phase 2: Execution

```bash
# Start working on tasks
/process-tasks
# Shows next task, context, and suggested approach

# Or pick specific task
/task-status
# Pick task ID, then:
/pt TASK-001

# Claude automatically suggests agents
"Working on login form..."
System: "💡 Use frontend-ux-specialist for UI"
fe create login form with email/password fields
```

**Task Execution Flow:**
1. Claude shows task requirements
2. System suggests relevant agents
3. You work (with agent help)
4. System tracks progress
5. Auto-validates against requirements

### ✅ Phase 3: Validation

```bash
# After implementing a task
/verify-task TASK-001
# Checks: requirements met, tests pass, design compliance

# Validate entire stage
/stage-validate check
# Multi-agent validation:
# - Design compliance (frontend-ux-specialist)
# - Code quality (code-reviewer)
# - Security (security-threat-analyst)
# - Test coverage (qa-test-engineer)

# Fix any issues
/stage-validate fix
# Auto-fixes what it can, guides you through rest
```

### 🚢 Phase 4: Ship

```bash
# Complete current feature
/feature-complete
# - Runs all validations
# - Updates documentation
# - Marks tasks complete
# - Prepares for merge

# Create PR
/review-pr
# code-reviewer agent analyzes changes

# Merge and clean up
/branch-clean
/sync-main
```

---

## Task & Issue Management

### 📍 Where Everything Lives

```
.claude/
├── tasks/                 # Individual task files (TASK-XXX.md)
├── task-ledger.json      # Master task tracking
├── issues/               # Captured issues (ISSUE-XXX.md)
├── PRDs/                 # Product requirement docs
├── checkpoints/          # Saved states
└── state/                # Current working state
```

### 📝 Task Commands

```bash
# View all tasks
/task-status
/task-board           # Visual board view
/todo                # Simple todo list

# Work on tasks
/process-tasks       # Next task automatically
/pt TASK-001        # Specific task

# Task management
/assign-task TASK-001 @frontend
/task-checkpoint    # Save progress
/verify-task TASK-001
```

### 💡 Capture & Issues

```bash
# Quick capture during conversation
"We need to add password strength indicator"
/capture-to-issue
# → Creates: issues/ISSUE-XXX-password-strength.md

# Convert issue to task
/issue-to-task ISSUE-001

# Bulk issue generation from PRD
/generate-issues
```

---

## Recovery & Rollback

### 🔄 Checkpoint System

```bash
# Before risky changes
/checkpoint create before-refactor
# → Saves: current state, git state, task progress

# List checkpoints
/checkpoint list

# Restore if needed
/checkpoint restore before-refactor
```

### 🚨 Error Recovery

```bash
# Something broke?
/error-recovery diagnose
# Analyzes: recent changes, errors, suggests fixes

# Quick fixes
/error-recovery deps      # Fix dependencies
/error-recovery build     # Fix build issues
/error-recovery types     # Fix TypeScript

# Nuclear option - full rollback
/checkpoint restore last-working
```

### 🎯 Git-Aware Recovery

```bash
# Oops, bad commit?
git reset --soft HEAD~1
/smart-resume           # Re-syncs Claude with git state

# Need to switch context?
/checkpoint create current-work
git stash
git checkout other-branch
/smart-resume           # Loads other branch context
```

---

## Claude Interaction Patterns

### 🗣️ Starting Work Sessions

```bash
# Morning startup
chain morning-setup
# Runs: smart-resume, security-check, test-runner

# Or just
/smart-resume
"What was I working on?"
```

### 🛑 Stopping & Handoff

```bash
# End of session
"I need to stop for today"
/checkpoint create end-of-day
/work-status save

# Prepare handoff
"Create handoff notes for tomorrow"
doc create session summary and next steps
```

### 🧠 Planning & Thinking

```bash
# Need to think through approach?
/think-through "How should I implement real-time notifications?"

# Ultra-deep analysis
/ultra-think "Design a scalable architecture for 1M users"

# Get unstuck
/help-decide "Should I use WebSockets or Server-Sent Events?"
```

---

## Quick Command Reference

### 🎯 Essential Flows

```bash
# Project Setup
/init-project            # New project
/analyze-existing        # Existing project
/smart-resume           # Continue work

# Planning
/create-prd             # Define features
/generate-tasks         # Break down work
/task-board            # View roadmap

# Execution
/process-tasks          # Work on tasks
fe/be/qa/sec [task]     # Use agents
/verify                 # Check work

# Validation
/stage-validate         # Full validation
/test-runner           # Run tests
/security-check        # Security audit

# Shipping
/feature-complete       # Finalize feature
/review-pr             # Code review
/branch-clean          # Cleanup
```

### 🚀 Power Workflows

```bash
# Full feature development
chain feature-development-chain

# Security audit
chain security-audit-chain

# Morning routine
chain morning-setup

# Pre-PR validation
chain pre-pr
```

---

## Real Project Walkthrough

Let's build a user authentication system from scratch:

### Day 1: Planning

```bash
# 1. Initialize project
/init-project auth-app

# 2. Create vision
/create-prd authentication-system
"I need login, register, password reset, and 2FA"

# 3. Generate tasks
/generate-tasks
# Output: 12 tasks generated

# 4. Review plan
/task-board
```

### Day 2: Core Implementation

```bash
# 1. Morning startup
/smart-resume
"Continue with auth system"

# 2. Start first task
/process-tasks
# Shows: "TASK-001: Create user model"

# 3. Use agents
db design user schema with auth fields
migrate create user table migration

# 4. Verify task
/verify-task TASK-001
# ✅ Task complete

# 5. Continue
/pt  # Next task automatically
```

### Day 3: UI Development

```bash
# 1. Resume
chain morning-setup

# 2. Frontend tasks
/pt
# Shows: "TASK-005: Create login form"

# 3. TDD approach
tdd create login form tests
fe implement login form with tests passing

# 4. Quick fix needed
"The button is too small on mobile"
fe fix button touch target for mobile

# 5. Checkpoint progress
/checkpoint create ui-complete
```

### Day 4: Security & Testing

```bash
# 1. Security audit
chain security-audit-chain
# Runs full security analysis

# 2. Fix issues
be implement rate limiting for auth endpoints
sec verify security fixes

# 3. Full test suite
qa create comprehensive auth test suite
/test-runner all
```

### Day 5: Ship It!

```bash
# 1. Final validation
/stage-validate check --strict

# 2. Documentation
doc create auth system documentation

# 3. Complete feature
/feature-complete

# 4. PR review
/review-pr
cr review all auth system changes

# 5. Merge
/sync-main
git merge feature/auth-system
```

---

## 💡 Pro Tips

1. **Always checkpoint before big changes**
   ```bash
   /checkpoint create before-[what-youre-doing]
   ```

2. **Let agents guide you**
   - Don't force specific agents
   - Let context suggestions help

3. **Capture everything**
   ```bash
   "Idea: We should add social login"
   /capture-to-issue
   ```

4. **Trust the workflow**
   - PRD → Tasks → Execute → Validate → Ship
   - Don't skip validation!

5. **Use chains for common workflows**
   ```bash
   chain morning-setup
   chain pre-pr
   chain feature-complete
   ```

## 🆘 When Things Go Wrong

```bash
# Can't remember where you were?
/smart-resume
/work-status

# Tests failing?
/error-recovery diagnose
tdd fix failing tests

# Design broken?
/validate-design --fix

# Need to start over?
/checkpoint restore last-working

# Completely lost?
/help
pm orchestrate getting back on track
```

---

Remember: The system is designed to guide you. Trust the workflow, use the agents, and let the automation handle the repetitive parts while you focus on creating great software!
