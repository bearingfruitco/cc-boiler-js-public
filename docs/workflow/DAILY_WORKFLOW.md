# Daily Development Workflow

> 🚀 **For the complete unified guide, see: [MASTER_WORKFLOW_GUIDE.md](../../MASTER_WORKFLOW_GUIDE.md)**

This guide explains the day-to-day workflow for building features with Claude Code, GitHub issues, and both PRD and PRP-driven development systems.

## 🎯 Core Concept: Everything Flows Through GitHub Issues

```
GitHub Issue → PRD/PRP → Tasks/Validation → Implementation → PR (closes issue)
      ↓                                              ↓
   Gist stores state                    State auto-saved every 60 seconds
```

## 🚦 Decision Tree: PRD vs PRP

```mermaid
graph TD
    A[New Feature Request] --> B{Clear implementation path?}
    B -->|No| C[Use PRD]
    B -->|Yes| D{Have code examples?}
    
    C --> C1[Define what & why]
    C1 --> C2[/prd feature-name]
    C2 --> C3[Generate tasks]
    
    D -->|No| E[Use PRD]
    D -->|Yes| F[Use PRP]
    
    E --> C
    F --> F1[One-pass implementation]
    F1 --> F2[/create-prp feature-name]
    F2 --> F3[Validation loops]
```

## 📋 Quick Reference: When to Use What

| Scenario | GitHub Issue? | PRD? | PRP? | Why |
|----------|--------------|------|------|-----|
| Bug fix (<30 min) | ✅ Quick issue | ❌ | ❌ | Just track it |
| Clear component | ✅ Standard | ❌ | ✅ | Have patterns to follow |
| New feature (exploratory) | ✅ Full issue | ✅ | ❌ | Need to define specs |
| New feature (clear specs) | ✅ Full issue | Optional | ✅ | Can implement directly |
| Architecture change | ✅ Full issue | ✅ | ❌ | Needs planning |
| Refactoring | ✅ Standard | ❌ | ✅ | Clear before/after |

## 🎯 The "Accept Claude's Plan" Workflow

When Claude gives you a plan, capture it and decide the approach:

```bash
# 1. DON'T just say "yes, let's do it"
# INSTEAD, capture it immediately:

# Quick capture
gh issue create --title "Implement: [Plan Summary]" \
  --body "[paste Claude's entire plan]" \
  --label "from-claude"
# Note the issue number!

# 2. Decide approach:
# - Exploratory/Complex? → PRD
/fw start 27
/prd feature-name

# - Clear implementation? → PRP (NEW)
/fw start 27
/create-prp feature-name

# 3. NOW tell Claude:
"I've created issue #27 and a PRP. Let's validate and implement."
```

## 📅 Daily Workflow Options

### Morning: Resume Where You Left Off

```bash
# Start Claude Code
claude-code .

# Smart resume - shows everything
/sr

# This shows:
# - Current branch/issue
# - Modified files
# - Active TODOs
# - Active PRPs
# - Where you stopped
```

### Option A: PRP Workflow (Recommended for Clear Features)

Perfect when you know what to build and have examples to follow.

#### Step 1: Start from Issue
```bash
# Start working on issue
/fw start 45  # "Add user avatar upload"

# Create comprehensive PRP
/create-prp user avatar upload with crop and preview
# or shorter:
/prp avatar upload
```

#### Step 2: Validate Environment
```bash
# Check if ready to implement
/prp-execute user-avatar --level 1

# Fix any issues
/prp-execute user-avatar --level 1 --fix
```

#### Step 3: Implement Following Blueprint
The PRP provides exact implementation steps. Follow them phase by phase.

#### Step 4: Validate Each Phase
```bash
# After backend work
/prp-execute user-avatar --level 2

# After frontend work  
/prp-execute user-avatar --level 3

# Before PR
/prp-execute user-avatar --level 4
```

#### Step 5: Complete Feature
```bash
# Final validation
/prp-execute user-avatar

# Create PR
/fw complete
```

### Option B: Traditional PRD Workflow

Perfect for exploratory development or when requirements aren't fully clear.

#### Step 1: Create Issue & PRD
```bash
# Create GitHub issue
gh issue create --title "Feature: User Dashboard" \
  --body "Users need a dashboard to view their data"

# Start work
/fw start 23

# Create PRD
/prd user-dashboard
```

#### Step 2: Break Down & Implement
```bash
# Generate micro-tasks
/gt user-dashboard

# Process tasks
/pt user-dashboard

# Check progress
/ts user-dashboard
```

#### Step 3: Validate & Complete
```bash
# Check stage completion
/sv check 2

# Grade implementation
/grade

# Create PR
/fw complete
```

## 🔄 Switching Between Workflows

You can use both approaches on the same project:

```bash
# Complex feature? Start with PRD
/prd complex-feature
# ... after defining specs ...
# Create PRP for implementation
/prp complex-feature-phase-1

# Clear component? Jump to PRP
/prp data-table-component
```

## 📊 Real Example: Contact Form

### Using PRP (Clear Requirements)
```bash
# 1. Create issue
gh issue create --title "Add contact form with email notifications"

# 2. Start work
/fw start 89

# 3. Create PRP with all context
/prp contact form with validation and email

# 4. Validate readiness
/prp-execute contact-form --level 1

# 5. Implement (following PRP blueprint)
# ... coding ...

# 6. Validate implementation
/prp-execute contact-form

# 7. Ship it
/fw complete
```

### Using PRD (Exploratory)
```bash
# 1. Create issue
gh issue create --title "Add customer communication feature"

# 2. Start work
/fw start 90

# 3. Define requirements
/prd customer-communication

# 4. Break down
/gt customer-communication

# 5. Process tasks
/pt customer-communication

# 6. Grade alignment
/grade

# 7. Ship it
/fw complete
```

## 🎯 Pro Tips

### 1. Choose the Right Tool
- **Use PRP when**: You know exactly what to build
- **Use PRD when**: You need to explore and define

### 2. Validation is Key
```bash
# PRP: Run continuously
/prp-execute feature --level 1  # While coding

# PRD: Check stages
/sv check                       # After phases
```

### 3. Combine Approaches
```bash
# Start with PRD for planning
/prd big-feature

# Create PRPs for implementation
/prp big-feature-api
/prp big-feature-ui
/prp big-feature-integration
```

### 4. Use Auto-Fix
```bash
# Save time with PRP auto-fix
/prp-execute feature --fix

# This fixes:
# - Linting issues
# - Import problems
# - Simple type errors
```

## 📋 Daily Checklist

### Morning
- [ ] `/sr` - Resume context
- [ ] Check active PRPs: `ls PRPs/active/`
- [ ] `/bt list` - Check bugs
- [ ] Pick approach (PRD vs PRP)

### During Development
- [ ] PRP: Run Level 1 validation continuously
- [ ] PRD: Check stage gates
- [ ] Commit frequently (state auto-saves)
- [ ] Track bugs with `/bt add`

### Before PR
- [ ] PRP: Full validation `/prp-execute feature`
- [ ] PRD: Grade alignment `/grade`
- [ ] Security check `/sc`
- [ ] `/fw complete` - Create PR

### End of Day
- [ ] `/checkpoint` - Manual save
- [ ] Update PRPs/PRDs if needed
- [ ] Note stopping point

## 🚀 Advanced Workflows

### Parallel Development with PRPs
```bash
# Create multiple PRPs
/prp user-profile-view
/prp user-profile-edit
/prp user-profile-api

# Validate all at once
/prp-execute user-profile-* --level 1

# Work in parallel with team
```

### CI/CD with PRPs
```yaml
# .github/workflows/prp-check.yml
- name: Validate PRPs
  run: |
    for prp in PRPs/active/*.md; do
      bun run PRPs/scripts/prp-runner.ts \
        --prp $(basename $prp .md) \
        --output-format json
    done
```

### Pattern Extraction
```bash
# After successful implementation
/specs extract user-avatar

# Creates reusable pattern from PRP
# Future PRPs reference this pattern
```

## 🎓 Remember

- **PRPs** = One-pass implementation with validation
- **PRDs** = Requirements definition and exploration
- **Both** = Complete development system
- **GitHub Issues** = Single source of truth

The best developers use the right tool for the job. Sometimes that's a PRD for planning, sometimes it's a PRP for implementation, and often it's both!
