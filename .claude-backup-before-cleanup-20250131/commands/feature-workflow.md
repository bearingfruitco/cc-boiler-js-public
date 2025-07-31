# Feature Workflow Command (TDD Enhanced)

Orchestrates issue-based development with MANDATORY test-first development, design validation, and GitHub integration.

🔴 **TDD IS NOW MANDATORY**: All features start with test generation based on issue requirements.

## Arguments:
- $ACTION: start|validate|complete
- $ISSUE_NUMBER: GitHub issue number
- $OPTIONS: --no-tdd (skip TDD - requires confirmation)

## Why This Command:
GitHub MCP handles Git operations, but doesn't:
- Enforce test-first development
- Auto-generate test suites from requirements
- Enforce design system rules
- Manage worktrees
- Create issue-based workflows
- Auto-generate compliant code

## Steps:

### Action: START
1. **Use MCP to Get Issue**
   ```typescript
   // MCP handles this
   const issue = await github.getIssue(ISSUE_NUMBER);
   ```

2. **Generate Test Suite from Requirements** (NEW - MANDATORY)
   ```bash
   # Extract requirements from issue
   REQUIREMENTS=$(extract_requirements "$issue.body")
   
   # Auto-spawn TDD engineer
   echo "🤖 Spawning TDD engineer to generate tests..."
   
   # Generate comprehensive test suite
   /spawn tdd-engineer <<EOF
   Generate test suite for issue #${ISSUE_NUMBER}:
   ${issue.title}
   
   Requirements:
   ${REQUIREMENTS}
   
   Create tests for:
   - All acceptance criteria
   - Edge cases
   - Error scenarios
   - Design system compliance
   - Accessibility
   EOF
   
   # Wait for test generation
   echo "⏳ Generating tests... (typically 2-3 minutes)"
   ```

3. **Create Worktree** (Not in MCP)
   ```bash
   # Extract requirements from issue
   BRANCH_NAME="feature/${ISSUE_NUMBER}-${SLUG}"
   WORKTREE_PATH="../$(basename $(pwd))-worktrees/$BRANCH_NAME"
   
   # Create isolated workspace
   git worktree add -b $BRANCH_NAME $WORKTREE_PATH origin/main
   ```

4. **Generate Implementation Plan (Now Test-Driven)**
   ```markdown
   # Feature Plan: ${issue.title}
   
   ## Test Coverage Generated:
   ${listGeneratedTests()}
   
   ## TDD Implementation Order:
   1. Run tests (RED phase)
   2. Implement minimal code to pass
   3. Refactor while keeping tests green
   ```

5. **Original Implementation Plan**
   ```markdown
   # Feature Plan: ${issue.title}
   
   ## Requirements from Issue:
   ${parseRequirements(issue.body)}
   
   ## Components to Create:
   ${identifyComponents(issue.body)}
   
   ## Design System Checklist:
   - [ ] Typography: 4 sizes, 2 weights
   - [ ] Spacing: 4px grid
   - [ ] Touch targets: 44px+
   - [ ] Mobile-first
   ```

6. **Scaffold Initial Files (Tests First)**
   Based on issue requirements, create:
   - ✅ Test files (ALREADY GENERATED)
   - Component stubs with design system
   - Documentation updates
   
   ```bash
   # Verify tests exist before any implementation
   if [ ! -f "*test*" ]; then
     echo "❌ ERROR: No tests found!"
     echo "TDD requires tests before implementation."
     exit 1
   fi
   ```

### Action: VALIDATE
1. **TDD Compliance Check** (NEW)
   ```bash
   # Ensure all code has tests
   echo "🧪 Checking TDD compliance..."
   
   # Find components without tests
   UNTESTED=$(find_components_without_tests)
   
   if [ ! -z "$UNTESTED" ]; then
     echo "❌ Components without tests:"
     echo "$UNTESTED"
     echo ""
     echo "Run: /chain atdd [component] to generate tests"
     exit 1
   fi
   
   # Check coverage
   COVERAGE=$(npm run test:coverage --silent | grep "All files" | awk '{print $10}')
   if [ "${COVERAGE%\%}" -lt 80 ]; then
     echo "❌ Coverage below 80%: $COVERAGE"
     exit 1
   fi
   ```

2. **Pre-Commit Validation**
   ```bash
   # Run design system check
   npm run validate:design || {
     echo "❌ Fix violations before committing"
     exit 1
   }
   ```

2. **Generate Commit Message**
   ```typescript
   // Smart commit with issue linking
   const files = await git.status();
   const message = generateCommitMessage(files, ISSUE_NUMBER);
   // e.g., "feat: add auth components (#23)"
   ```

3. **Use MCP for Commit**
   ```typescript
   // Let MCP handle the actual commit
   await github.commit(message);
   ```

### Action: COMPLETE
1. **Final Validation**
   ```bash
   # Comprehensive checks
   npm run validate:design
   npm test
   npm run build
   ```

2. **Generate PR Body**
   ```markdown
   Closes #${ISSUE_NUMBER}
   
   ## Design System Compliance ✅
   - Typography: 4 sizes, 2 weights only
   - Spacing: 4px grid (validated)
   - Colors: 60/30/10 distribution
   - Touch targets: 44px+ confirmed
   
   ## Changes
   ${generateChangeLog()}
   ```

3. **Use MCP for PR**
   ```typescript
   // MCP creates the PR
   await github.createPullRequest({
     title: `feat: ${issue.title} (#${ISSUE_NUMBER})`,
     body: prBody,
     base: 'main'
   });
   ```

4. **Cleanup Worktree**
   ```bash
   # After merge (not in MCP)
   git worktree remove $WORKTREE_PATH
   ```

## What This Command Adds Beyond MCP:

1. **Test-First Development** - Tests generated from issue requirements
2. **TDD Enforcement** - No code without tests
3. **Design Validation** - Enforced at every step
4. **Worktree Management** - Isolated feature development
5. **Smart Scaffolding** - Generate compliant components
6. **Issue Parsing** - Extract requirements automatically
7. **Workflow Automation** - Orchestrate MCP commands

## Integration Example:

```bash
# Start feature (our command + MCP)
/feature-workflow start 23
# - Gets issue from GitHub
# - GENERATES TESTS FIRST (automatic)
# - Creates worktree
# - Generates TDD plan
# - Uses MCP to update issue

# During development
/create-component ui AuthForm  # Tests already exist!
/test                          # Run tests (should fail)
# ... implement until tests pass ...
/test                          # All green!
/validate-design               # Ensure compliance

# Complete feature (our command + MCP)
/feature-workflow complete 23
# - Validates TDD compliance
# - Checks test coverage (>80%)
# - Validates design system
# - Uses MCP to create PR
# - Cleans up worktree
```

## TDD Workflow Visualization

```
GitHub Issue #23
       ↓
/fw start 23
       ↓
[AUTO] Extract requirements
       ↓
[AUTO] Generate test suite
       ↓
[AUTO] Create worktree
       ↓
[USER] See failing tests (RED)
       ↓
[USER] Implement features
       ↓
[AUTO] Tests pass (GREEN)
       ↓
[USER] Refactor if needed
       ↓
/fw complete 23
       ↓
PR with 100% tested code
```

## Skipping TDD (Emergency Only)

```bash
/fw start 23 --no-tdd

# ⚠️  WARNING: Skipping TDD violates best practices!
# 
# This will:
# - Create technical debt
# - Risk bugs and regressions
# - Make refactoring harder
# 
# Are you SURE? (y/N): _
```
