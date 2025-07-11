`/create-component <type> <name> [options]`

### Parameters
- `type`: Component category
  - `ui`: Base UI components (Button, Card, Input)
  - `form`: Form-specific (FormField, ValidationMessage)
  - `layout`: Layout components (Container, Section)
  - `feature`: Feature-specific components

- `name`: Component name (PascalCase)

- `options`:
  - `--with-tests`: Include test file
  - `--with-story`: Include Storybook story
  - `--with-docs`: Include documentation

### Design Rules Enforced
✅ Typography: Only text-size-[1-4], font-[regular|semibold]
✅ Spacing: Only 4px grid values
✅ Colors: 60/30/10 distribution
✅ Mobile: 44px+ touch targets

### Examples
```bash
# Basic UI component
/create-component ui Button

# Form component with tests
/create-component form ContactForm --with-tests

# Full feature component
/create-component feature QuizWizard --with-tests --with-docs
```

### Generated Structure
```
components/
  ui/
    Button.tsx         # Component
    Button.test.tsx    # Tests (if --with-tests)
    Button.stories.tsx # Storybook (if --with-story)
    Button.md          # Docs (if --with-docs)
```

### Common Issues
❌ "Component exists" - Check the file first
❌ "Invalid type" - Use: ui, form, layout, or feature
❌ "Design violation" - Component template has issues

### Related Commands
- `/validate-design` - Check after creation
- `/test-runner generate` - Add tests later
- `/performance-monitor` - Check render performance
```

### PRD Workflow Example
```bash
/help prd-workflow

## 🚀 Complete PRD to Production Workflow

### Step 1: Create GitHub Issue
```bash
gh issue create --title "Feature: Payment Integration"
# Note issue number (e.g., #42)
```

### Step 2: Start Feature
```bash
/fw start 42
# Creates branch and worktree
```

### Step 3: Generate PRD
```bash
/prd payment-integration
# or /create-prd payment-integration
# Creates: docs/project/features/payment-integration-PRD.md
# Edit PRD with specific requirements
```

### Step 4: Generate Tasks
```bash
/gt payment-integration
# or /generate-tasks payment-integration
# Creates: docs/project/features/payment-integration-tasks.md
# Review and adjust task list if needed
```

### Step 5: Process Tasks
```bash
/pt payment-integration
# or /process-tasks payment-integration
# Work through each task with approval
```

### Step 6: Test Implementation
```bash
/btf payment-checkout
# or /browser-test-flow payment-checkout
# Creates automated browser tests
```

### Step 7: Complete Feature
```bash
/fw complete 42
# Runs all checks and creates PR
```

### Monitoring Progress
- `/ts` - Check task status
- `/tb` - Visual task board
- `/tc` - Create checkpoint
```

### Command Aliases
```bash
/help aliases

## ⚡ Command Shortcuts

### Essential Aliases
- `/?` → `/help`
- `/sr` → `/smart-resume`
- `/cc` → `/create-component`
- `/vd` → `/validate-design`
- `/fw` → `/feature-workflow`

### PRD & Task Aliases
- `/prd` → `/create-prd`
- `/gt` → `/generate-tasks`
- `/pt` → `/process-tasks`
- `/ts` → `/task-status`
- `/tb` → `/task-board`
- `/tc` → `/task-checkpoint`
- `/vt` → `/verify-task`

### Testing Aliases
- `/tr` → `/test-runner`
- `/btf` → `/browser-test-flow`
- `/spm` → `/setup-playwright-mcp`

### Workflow Aliases
- `/ws` → `/work-status`
- `/cp` → `/checkpoint`
- `/cg` → `/context-grab`
- `/td` → `/todo`

### Utility Aliases
- `/pm` → `/performance-monitor`
- `/sc` → `/security-check`
- `/er` → `/error-recovery`
- `/auc` → `/auto-update-context`
```

### Interactive Mode
```bash
/help interactive

## 🤝 Interactive Command Helper

What would you like to do?

1. Start a new feature (PRD → Tasks → Code)
2. Resume previous work
3. Create a component
4. Run tests
5. Check design compliance
6. Fix an error
7. Create documentation
8. View project status
9. Set up browser testing
10. Update project context

Enter number or search: _
```

## Smart Help Features:

1. **Context Awareness**
   - Shows relevant commands based on current state
   - Suggests next logical actions
   - Warns about missing steps

2. **Search Capability**
   - Find commands by keyword
   - Show related commands
   - Provide examples

3. **Learning Mode**
   - Detailed explanations
   - Common patterns
   - Troubleshooting tips

4. **Quick Reference**
   - Cheat sheet format
   - Copy-paste examples
   - Common workflows

5. **PRD & Task Integration**
   - Complete workflow guidance
   - Step-by-step instructions
   - Progress tracking

This ensures developers can always find the right command without memorizing everything!