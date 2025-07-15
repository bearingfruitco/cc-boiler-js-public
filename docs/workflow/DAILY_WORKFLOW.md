# Daily Development Workflow

This guide explains the day-to-day workflow for building features with Claude Code, GitHub issues, and the PRD-driven development system.

## 🎯 Core Concept: Everything Flows Through GitHub Issues

```
GitHub Issue → Feature PRD → Tasks → Implementation → PR (closes issue)
      ↓                                    ↓
   Gist stores state              State auto-saved every 60 seconds
```

## 🚦 Decision Tree: What to Do When Claude Gives You a Plan

```mermaid
graph TD
    A[Claude provides a plan/suggestion] --> B{Is it more than 30 min work?}
    B -->|No| C[Quick Fix Mode]
    B -->|Yes| D{Does it change core functionality?}
    
    C --> C1[Create quick issue]
    C1 --> C2[/fw quick ##]
    
    D -->|No| E[Standard Issue]
    D -->|Yes| F[Feature with PRD]
    
    E --> E1[gh issue create]
    E1 --> E2[/fw start ##]
    E2 --> E3[Work through tasks]
    
    F --> F1[gh issue create]
    F1 --> F2[/fw start ##]
    F2 --> F3[/prd feature-name]
    F3 --> F4[/gt feature-name]
    F4 --> F5[/pt feature-name]
```

## 📋 Quick Reference: When to Use What

| Scenario | GitHub Issue? | PRD? | Why |
|----------|--------------|------|-----|
| Bug fix (<30 min) | ✅ Quick issue | ❌ | Just track it |
| Validation/testing | ✅ Standard | ❌ | Plan is clear |
| New UI component | ✅ Standard | ❌ | Scope is limited |
| New feature | ✅ Full issue | ✅ | Needs full spec |
| Architecture change | ✅ Full issue | ✅ | Impacts system |
| Claude gives complex plan | ✅ Always | ✅ If >2hr | Don't lose context |

## 🎯 The "Accept Claude's Plan" Workflow

When Claude gives you a plan (like a validation plan), here's the exact workflow:

```bash
# 1. DON'T just say "yes, let's do it"
# INSTEAD, capture it immediately:

# Option A: Quick capture (for any plan)
/research-docs save "validation-plan-2024-01-15"
# This saves to .claude/research/

# Option B: Direct to issue (recommended)
gh issue create --title "Core Functionality Validation" \
  --body "[paste Claude's entire plan]" \
  --label "validation"
# Note the issue number!

# 2. Decide complexity:
# - Under 2 hours? Start directly
/fw start 27

# - Over 2 hours or multiple phases? Create PRD
/fw start 27
/prd core-validation
# Paste Claude's plan into the PRD structure

# 3. NOW tell Claude:
"I've created issue #27 for this. Let's start with Phase 1"
```

## 📅 Daily Workflow

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
# - Where you stopped
```

### Working on a Feature

#### Step 1: Pick or Create an Issue

**Option A: Continue existing work**
```bash
# See your open issues
gh issue list --assignee @me

# Resume specific issue
/fw resume 23  # Loads issue #23 context
```

**Option B: Start new feature**
```bash
# Create GitHub issue FIRST
gh issue create --title "Feature: Quiz Creation" \
  --body "Users should be able to create custom quizzes with multiple choice questions"

# Note the issue number (e.g., #24)
```

**Option C: Claude just gave you a plan**
```bash
# Capture it immediately!
gh issue create --title "Implement: [Plan Summary]" \
  --body "$(pbpaste)" \  # Mac: paste from clipboard
  --label "from-claude"

# Or save to research first
/research-docs save "claude-plan-$(date +%Y%m%d)"
```

#### Step 2: Start Feature Workflow

```bash
# Start working on issue #24
/fw start 24

# This automatically:
# ✓ Creates branch: feature/24-quiz-creation
# ✓ Sets up isolated worktree
# ✓ Links to issue #24
# ✓ Prepares context
```

#### Step 3: Create Feature PRD (When Needed)

```bash
# Use PRD for complex features or multi-phase work
/prd quiz-creation

# This creates:
# docs/project/features/quiz-creation-PRD.md
# With:
# - User stories
# - Acceptance criteria
# - Technical requirements
# - UI/UX specifications
# - Stage gates
# - Async requirements
```

#### Step 4: Generate and Process Tasks

```bash
# Break PRD into tasks
/gt quiz-creation

# This creates:
# docs/project/features/quiz-creation-tasks.md
# With ~15-20 tasks like:
# 1.1 Create quiz database schema
# 1.2 Design quiz creation form
# 1.3 Implement question components
# etc.

# Work through tasks one by one
/pt quiz-creation

# Claude will:
# 1. Show you task 1.1
# 2. Implement it
# 3. Test it works
# 4. Ask for approval
# 5. Move to next task
```

#### Step 5: During Development

```bash
# Add quick TODOs as you work
/todo add "Refactor this validation logic"

# Check design compliance
/vd

# Run browser tests
/btf quiz-creation

# Your work is auto-saved to GitHub gist every 60 seconds!
# Gist name: work-state-issue-24.json
```

#### Step 6: Complete Feature

```bash
# When all tasks done
/fw complete 24

# This:
# ✓ Validates everything
# ✓ Creates PR linked to issue #24
# ✓ PR description includes "Closes #24"
# ✓ Cleans up worktree
```

### End of Day

```bash
# Create checkpoint (optional)
/checkpoint create "end of day"

# Just close terminal - state already saved!
# Tomorrow: /sr will restore everything
```

## 🚨 Common Mistakes & Fixes

### Mistake 1: "Just accepting plans"
```bash
# ❌ Wrong:
Claude: "Here's a plan for validation..."
You: "Yes, let's do it"

# ✅ Right:
Claude: "Here's a plan for validation..."
You: "Let me capture this first"
gh issue create --title "..." --body "[plan]"
/fw start ##
"Now let's start with step 1"
```

### Mistake 2: "Not sure if I need a PRD"
```bash
# Use this command to help decide:
/think-through "Do I need a PRD for [feature]?"

# Or use this rule:
# - Changes multiple files/systems? → PRD
# - Adds new user-facing feature? → PRD  
# - Just fixing/validating? → No PRD
# - Over 2 hours of work? → PRD
```

### Mistake 3: "Lost track of what we decided"
```bash
# Always available:
/research-docs list  # See all saved plans
/fw status          # Current issue status
/checkpoint list    # Recent save points
gh issue list --assignee @me  # All your work
```

## 💡 New Habits to Build

1. **The Pause Habit**
   ```
   Claude gives plan → PAUSE → Create issue → THEN proceed
   ```

2. **The Context Check**
   ```bash
   # Before accepting any plan:
   /fw status  # Am I already working on something?
   /todo list  # Do I have pending tasks?
   ```

3. **The Handoff Mindset**
   ```
   "Would future me (or a teammate) understand what to do?"
   If no → Create issue with full context
   ```

## 🔄 Integrated Workflow for Complex Plans

When Claude gives you a multi-phase plan:

```bash
# 1. Claude just gave you a validation plan
# DON'T just proceed!

# 2. Quick capture
gh issue create \
  --title "Critical: Core Functionality Validation" \
  --body "$(pbpaste)" \
  --label critical,validation \
  --milestone "MVP"

# 3. Since it's multi-phase, create PRD
/fw start 28  # Use the issue number
/prd core-validation

# 4. The PRD will structure it properly with:
# - Stage gates between phases
# - Clear exit criteria
# - Testable outcomes

# 5. Generate tasks from phases
/gt core-validation

# 6. Now tell Claude:
"I've created issue #28 and PRD. Starting with Phase 1 now."
/pt core-validation  # Work through systematically
```

## 🔄 Switching Between Features

```bash
# Save current state
/checkpoint create "switching to bug fix"

# List your issues
gh issue list --assignee @me

# Switch to different issue
/fw switch 25

# Later, switch back
/fw switch 24
# All your context restored from gist!
```

## 👥 Team Handoffs

```bash
# Before handoff
/fw handoff 24 "Completed tasks 1-8, working on API integration"

# Team member picks up
/fw resume 24
# They see:
# - Your progress
# - Current state
# - Where to continue
```

## 📊 Progress Tracking

### See Overall Progress
```bash
# View all open issues
gh issue list

# See specific issue status
/fw status 24
```

### Task-Level Progress
```bash
# See task completion
/ts quiz-creation

# Visual task board
/tb
```

## 🚨 Common Scenarios

### "I forgot what I was working on"
```bash
/sr  # Shows current context
/fw status  # Shows current issue
```

### "I need to fix a bug quickly"
```bash
# Stash current work
/checkpoint create "before bug fix"

# Create bug issue
gh issue create --title "Bug: Form validation error" --label bug

# Quick fix without full workflow
/fw quick 25
```

### "Multiple features in progress"
```bash
# See all your active branches
/worktree list

# Switch between them
/fw switch 23  # User auth
/fw switch 24  # Quiz creation
```

### "I messed something up"
```bash
# Restore from checkpoint
/checkpoint restore latest

# Or restore from gist
/fw restore 24
```

### "Claude gave me a complex plan"
```bash
# 1. Save it immediately
/research-docs save "claude-plan-validation"

# 2. Create issue with the plan
gh issue create --title "Implement: Validation Plan" \
  --body "$(cat .claude/research/claude-plan-validation.md)"

# 3. Decide if it needs PRD
/think-through "Does this validation plan need a PRD?"
# If yes: /prd validation-plan
# If no: just /fw start ##
```

## 🎯 Key Points to Remember

1. **Always start with a GitHub issue** - It's your anchor point
2. **Issues track features, not individual tasks** - One issue = one feature
3. **State saves automatically** - Via GitHub gists every 60 seconds
4. **PRDs provide detailed specs** - Generated from issue description
5. **Tasks are granular** - 5-15 minute chunks from PRD
6. **Everything links back to the issue** - Branches, PRs, gists
7. **Capture Claude's plans immediately** - Don't lose context

## 📈 Example: Full Feature Flow

```bash
# Monday: Start new feature
gh issue create --title "Feature: User Profile" --body "Users need profiles"
# Created issue #26

/fw start 26
/prd user-profile
/gt user-profile
/pt user-profile
# Complete tasks 1.1 through 1.5

# Tuesday: Continue
/sr  # Shows you're on issue #26, task 1.6
/pt user-profile  # Continue from task 1.6

# Wednesday: Finish up
/pt user-profile  # Complete remaining tasks
/fw complete 26  # Create PR, closes issue #26
```

## 📈 Example: Handling Claude's Plans

```bash
# Claude provides validation plan
Claude: "Here's a 4-phase validation plan..."

# Your response:
"Great plan! Let me capture this properly."

# Create issue
gh issue create \
  --title "Core Functionality Validation" \
  --body "[paste plan]" \
  --label "validation,critical"
# Created issue #29

# Start work
/fw start 29

# Since it's 4 phases (>2hr), create PRD
/prd core-validation
# Paste Claude's plan when prompted

# Generate tasks
/gt core-validation

# Now work through it
/pt core-validation
"Starting with Phase 1: Make It Accessible"
```

## 🔗 How It All Connects

```
Issue #26 "User Profile"
    ├── Branch: feature/26-user-profile
    ├── PRD: docs/project/features/user-profile-PRD.md
    ├── Tasks: docs/project/features/user-profile-tasks.md
    ├── State: work-state-issue-26.json (GitHub gist)
    └── PR: "feat: add user profile (#26)" → Closes #26
```

## 🎓 Learning the System

### Quick Commands When Unsure
```bash
/help workflow      # Today's workflow reminders
/best-practice      # Shows example of perfect workflow
/mistakes-check     # Analyzes your recent workflow
```

### The Golden Rule
**Every piece of work should have a GitHub issue as its "home"** - even if it's just a 30-minute task. This prevents the "accepting plans and losing track" problem.

This is your daily development cycle. Issues organize work, PRDs define it, tasks break it down, and GitHub tracks it all!
