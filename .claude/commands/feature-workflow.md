---
name: fw
description: Feature workflow - Enhanced with PRP awareness
aliases: [feature-workflow, feature, workflow]
---

# Feature Workflow Command (PRP & TDD Enhanced)

Orchestrates issue-based development with PRP context, MANDATORY test-first development, design validation, and GitHub integration.

🔴 **TDD IS MANDATORY**: All features start with test generation based on issue requirements.
🎯 **PRP-AWARE**: Automatically loads context from related PRPs.

## Arguments:
- $ACTION: start|validate|complete
- $ISSUE_NUMBER: GitHub issue number
- $OPTIONS: --no-tdd (skip TDD - requires confirmation)

## Enhanced Workflow

### Action: START

#### Step 1: Get Issue & Load PRP Context
```typescript
// Get issue from GitHub
const issue = await github.getIssue(ISSUE_NUMBER);

// NEW: Check for related PRP
const prpName = extractPRPReference(issue.body);
if (prpName) {
  const prp = await loadPRP(`PRPs/active/${prpName}.md`);
  console.log("📋 Loaded PRP context: " + prpName);
}

// NEW: Load architectural context
const archContext = await loadArchitecturalContext(issue);
if (archContext.hasDebt) {
  console.log("🏗️ Architectural debt context loaded");
  console.log(`  Current: ${archContext.current}`);
  console.log(`  Target: ${archContext.target}`);
}
```

#### Step 2: Generate Contextual Tests
```bash
# Extract requirements from issue AND PRP
REQUIREMENTS=$(extract_requirements "$issue.body" "$prp.content")

# Check if this is a refactoring task
if [[ "$issue.labels" == *"refactoring"* ]]; then
  echo "♻️ Refactoring detected - generating refactoring test suite"
  /spawn tdd-engineer <<EOF
  Generate refactoring test suite for issue #${ISSUE_NUMBER}:
  
  Current State: ${archContext.current}
  Target State: ${archContext.target}
  
  Create tests that:
  1. Verify current behavior (regression tests)
  2. Test new component structure
  3. Ensure no functionality lost
  4. Check performance improvements
EOF
else
  # Standard feature tests
  /spawn tdd-engineer <<EOF
  Generate test suite for issue #${ISSUE_NUMBER}:
  ${issue.title}
  
  PRP Context: ${prp.summary}
  Requirements: ${REQUIREMENTS}
  
  Create tests for:
  - All acceptance criteria
  - Edge cases
  - Error scenarios
  - Design system compliance
  - Accessibility
EOF
fi

echo "⏳ Generating contextual tests... (2-3 minutes)"
```

#### Step 3: Create Smart Worktree
```bash
# Determine branch type from issue
if [[ "$issue.labels" == *"refactor"* ]]; then
  BRANCH_TYPE="refactor"
elif [[ "$issue.labels" == *"fix"* ]]; then
  BRANCH_TYPE="fix"
elif [[ "$issue.labels" == *"test"* ]]; then
  BRANCH_TYPE="test"
else
  BRANCH_TYPE="feature"
fi

BRANCH_NAME="${BRANCH_TYPE}/${ISSUE_NUMBER}-${SLUG}"
WORKTREE_PATH="../$(basename $(pwd))-worktrees/$BRANCH_NAME"

# Create isolated workspace
git worktree add -b $BRANCH_NAME $WORKTREE_PATH origin/main
cd $WORKTREE_PATH

# Copy PRP context to worktree
if [ -n "$prpName" ]; then
  cp "PRPs/active/${prpName}.md" ".current-prp.md"
  echo "📋 PRP context available in .current-prp.md"
fi
```

#### Step 4: Generate Implementation Plan
```markdown
# Implementation Plan: ${issue.title}

## PRP Context
${prp ? `Following PRP: ${prpName}` : 'No PRP linked'}

## Architectural Context
${archContext.hasDebt ? `
### Current Issues:
- Component: ${archContext.component} (${archContext.lines} lines)
- Coverage: ${archContext.coverage}%
- Performance: ${archContext.performance}ms

### Target State:
- Break into ${archContext.targetComponents} components
- Achieve ${archContext.targetCoverage}% coverage
- Optimize to ${archContext.targetPerformance}ms
` : 'No architectural debt'}

## Test-Driven Development Order:
1. ❌ Run tests (RED phase - ${testCount} tests failing)
2. ✅ Implement minimal code to pass
3. ♻️ Refactor while keeping tests green
4. 📊 Check coverage (target: ${targetCoverage}%)

## Implementation Phases:
${generatePhasesFromPRP(prp, issue)}
```

### Action: VALIDATE

#### Enhanced Validation with Context
```bash
# Check if following PRP guidelines
if [ -f ".current-prp.md" ]; then
  echo "📋 Validating against PRP requirements..."
  
  # Extract success criteria from PRP
  CRITERIA=$(grep -A 10 "Success Criteria" .current-prp.md)
  
  # Validate each criterion
  while IFS= read -r criterion; do
    if validate_criterion "$criterion"; then
      echo "✅ $criterion"
    else
      echo "❌ $criterion - NOT MET"
      VALIDATION_FAILED=true
    fi
  done <<< "$CRITERIA"
fi

# Standard validations
echo "🧪 Running test suite..."
npm test || exit 1

echo "📊 Checking coverage..."
COVERAGE=$(npm run test:coverage --silent | grep "All files" | awk '{print $10}')
TARGET_COVERAGE=$(grep "targetCoverage" .current-prp.md | grep -o '[0-9]+' || echo "80")

if [ "${COVERAGE%\%}" -lt "$TARGET_COVERAGE" ]; then
  echo "❌ Coverage ${COVERAGE} below target ${TARGET_COVERAGE}%"
  exit 1
fi

echo "🎨 Validating design system..."
npm run validate:design || exit 1

# Architecture validation for refactoring
if [[ "$BRANCH_NAME" == refactor/* ]]; then
  echo "🏗️ Validating refactoring..."
  
  # Check component size
  MAX_LINES=500
  for file in src/**/*.tsx; do
    LINES=$(wc -l < "$file")
    if [ "$LINES" -gt "$MAX_LINES" ]; then
      echo "❌ $file still has $LINES lines (max: $MAX_LINES)"
      exit 1
    fi
  done
  
  echo "✅ All components under $MAX_LINES lines"
fi
```

### Action: COMPLETE

#### Smart PR Generation with Context
```bash
# Generate comprehensive PR body
generate_pr_body() {
  cat <<EOF
Closes #${ISSUE_NUMBER}

## 📋 PRP Implementation
${prpName ? "Implements PRP: \`PRPs/active/${prpName}.md\`" : "No PRP linked"}

## 🏗️ Architectural Improvements
${archContext.hasDebt ? "
### Before:
- Component size: ${archContext.lines} lines
- Test coverage: ${archContext.coverage}%
- Performance: ${archContext.performance}ms

### After:
- Component size: ${newComponentStats}
- Test coverage: ${newCoverage}%
- Performance: ${newPerformance}ms
" : "N/A"}

## ✅ Acceptance Criteria
$(extract_and_check_criteria)

## 🧪 Testing
- Test coverage: ${COVERAGE}
- Tests added: ${testsAdded}
- Tests passing: ${testsPassing}/${totalTests}

## 🎨 Design System Compliance
- Typography: ✅ 4 sizes, 2 weights only
- Spacing: ✅ 4px grid validated
- Colors: ✅ 60/30/10 distribution
- Touch targets: ✅ 44px+ confirmed

## 📊 Performance Impact
$(generate_performance_comparison)

## 📚 Documentation
- [ ] Component docs updated
- [ ] API docs updated
- [ ] Architecture diagrams updated

## 🔄 Migration Notes
${migrationNotes || "None"}
EOF
}

# Create PR with comprehensive context
PR_BODY=$(generate_pr_body)
gh pr create \
  --title "${BRANCH_TYPE}: ${issue.title} (#${ISSUE_NUMBER})" \
  --body "$PR_BODY" \
  --base main
```

## PRP Integration Features

### Automatic PRP Detection
- Scans issue body for PRP references
- Loads PRP content for context
- Uses PRP success criteria for validation

### Architectural Debt Awareness
- Detects refactoring issues
- Loads current component metrics
- Validates improvements

### Smart Test Generation
- Different test strategies for features vs refactoring
- Uses PRP requirements for test cases
- Includes regression tests for refactoring

### Context-Aware Validation
- Validates against PRP success criteria
- Checks architectural improvements
- Ensures coverage targets from PRP

## Usage Examples

### Starting a Refactoring Task
```bash
/fw start 23
# Detects: Issue #23 is refactoring DebtForm
# Loads: debt-form-refactor-prp.md
# Generates: Refactoring test suite
# Creates: refactor/23-debt-form branch
```

### Starting a Feature
```bash
/fw start 24
# Detects: Issue #24 is test infrastructure
# Loads: test-infrastructure-prp.md
# Generates: Infrastructure test suite
# Creates: feature/24-test-infrastructure branch
```

### Completing with Full Context
```bash
/fw complete 23
# Validates: Against PRP criteria
# Checks: Component size reduced
# Verifies: Coverage increased
# Creates: PR with full context
```

## Workflow Visualization

```
GitHub Issue #23 (with PRP reference)
       ↓
/fw start 23
       ↓
[AUTO] Load PRP context
       ↓
[AUTO] Detect issue type (refactor/feature/fix)
       ↓
[AUTO] Generate contextual test suite
       ↓
[AUTO] Create appropriate branch type
       ↓
[USER] See failing tests with context (RED)
       ↓
[USER] Implement with PRP guidance
       ↓
[AUTO] Validate against PRP criteria (GREEN)
       ↓
[USER] Refactor if needed
       ↓
/fw complete 23
       ↓
PR with full PRP + architecture context
```

This enhanced workflow ensures every feature:
- Follows PRP guidelines
- Addresses architectural debt
- Has comprehensive tests
- Includes full context in PRs
