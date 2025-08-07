---
name: fw
description: Feature workflow - Enhanced with PRP awareness and smart agent selection
aliases: [feature-workflow, feature, workflow]
---

# Feature Workflow Command (PRP & Agent-Aware)

Orchestrates issue-based development with PRP context, smart agent selection, MANDATORY test-first development, and GitHub integration.

🔴 **TDD IS MANDATORY**: All features start with test generation
🎯 **PRP-AWARE**: Automatically loads context from related PRPs
🤖 **SMART AGENTS**: Selects appropriate agent based on issue type

## Arguments:
- $ACTION: start|validate|complete
- $ISSUE_NUMBER: GitHub issue number
- $OPTIONS: --no-tdd (skip TDD - requires confirmation)

## Enhanced Workflow

### Action: START

#### Step 1: Get Issue & Load Context
```typescript
// Get issue from GitHub
const issue = await github.getIssue(ISSUE_NUMBER);

// Check for related PRP
const prpName = extractPRPReference(issue.body);
if (prpName) {
  const prp = await loadPRP(`PRPs/active/${prpName}.md`);
  console.log("📋 Loaded PRP context: " + prpName);
}

// Load architectural context
const archContext = await loadArchitecturalContext(issue);
```

#### Step 2: Smart Agent Selection

Based on issue type and labels, select the appropriate agent:

```javascript
function selectAgentForIssue(issue, prp) {
  const labels = issue.labels.map(l => l.name);
  const title = issue.title.toLowerCase();
  
  // Refactoring tasks
  if (labels.includes('refactoring') || title.includes('refactor')) {
    return {
      primary: 'refactoring-expert',
      support: ['qa', 'performance'],
      reason: 'Major refactoring detected'
    };
  }
  
  // Test infrastructure
  if (labels.includes('testing') || title.includes('test')) {
    return {
      primary: 'qa',
      support: ['tdd-specialist', 'backend'],
      reason: 'Test infrastructure setup'
    };
  }
  
  // Frontend features
  if (labels.includes('frontend') || title.includes('ui') || title.includes('component')) {
    return {
      primary: 'frontend',
      support: ['ui-systems', 'form-builder-specialist'],
      reason: 'Frontend development'
    };
  }
  
  // Backend/API
  if (labels.includes('backend') || title.includes('api')) {
    return {
      primary: 'backend',
      support: ['database-architect', 'api-designer'],
      reason: 'Backend implementation'
    };
  }
  
  // Performance
  if (labels.includes('performance') || title.includes('optimize')) {
    return {
      primary: 'performance',
      support: ['refactoring-expert'],
      reason: 'Performance optimization'
    };
  }
  
  // Database
  if (labels.includes('database') || title.includes('schema')) {
    return {
      primary: 'database-architect',
      support: ['orm-specialist', 'backend'],
      reason: 'Database work'
    };
  }
  
  // Default: senior engineer
  return {
    primary: 'senior-engineer',
    support: ['frontend', 'backend'],
    reason: 'General development'
  };
}
```

#### Step 3: Agent-Driven Test Generation

```bash
# Select appropriate agent
AGENT_CONFIG=$(selectAgentForIssue "$issue" "$prp")
PRIMARY_AGENT=${AGENT_CONFIG.primary}
SUPPORT_AGENTS=${AGENT_CONFIG.support}

echo "🤖 Selected Agent: $PRIMARY_AGENT"
echo "   Reason: ${AGENT_CONFIG.reason}"
echo "   Support: ${SUPPORT_AGENTS[@]}"

# Different test generation based on agent/issue type
case "$PRIMARY_AGENT" in
  "refactoring-expert")
    echo "♻️ Generating refactoring test suite with $PRIMARY_AGENT"
    cat <<EOF
Using the refactoring-expert agent to:
1. Analyze current component structure (${archContext.lines} lines)
2. Generate regression tests for existing behavior
3. Create tests for new component structure
4. Add performance benchmarks
5. Ensure no functionality is lost

Current: ${archContext.current}
Target: ${archContext.target}
EOF
    ;;
    
  "qa")
    echo "🧪 Generating test infrastructure with qa agent"
    cat <<EOF
Using the qa agent to:
1. Set up testing framework (Vitest/Jest)
2. Configure coverage reporting
3. Create test utilities and helpers
4. Generate initial test suites
5. Set up CI/CD test pipeline
EOF
    ;;
    
  "frontend")
    echo "🎨 Generating component tests with frontend agent"
    cat <<EOF
Using the frontend agent to:
1. Create component unit tests
2. Add accessibility tests
3. Generate visual regression tests
4. Test user interactions
5. Validate design system compliance
EOF
    ;;
    
  "backend")
    echo "⚙️ Generating API tests with backend agent"
    cat <<EOF
Using the backend agent to:
1. Create API endpoint tests
2. Add integration tests
3. Generate load tests
4. Test error handling
5. Validate data contracts
EOF
    ;;
    
  *)
    echo "📝 Generating standard test suite with $PRIMARY_AGENT"
    ;;
esac

# Note: In Claude Code, the agent will actually generate the tests
echo "💡 To generate tests, the $PRIMARY_AGENT agent will create:"
echo "   - Test files in __tests__/ or *.test.ts"
echo "   - Coverage configuration"
echo "   - Test utilities"
```

#### Step 4: Create Contextual Branch

```bash
# Determine branch type from primary agent and issue
BRANCH_TYPE=$(determineBranchType "$PRIMARY_AGENT" "$issue")
BRANCH_NAME="${BRANCH_TYPE}/${ISSUE_NUMBER}-${SLUG}"

# Create worktree with context
git worktree add -b $BRANCH_NAME "../worktrees/$BRANCH_NAME" origin/main
cd "../worktrees/$BRANCH_NAME"

# Copy relevant context
cp "PRPs/active/${prpName}.md" ".current-prp.md"
echo "$AGENT_CONFIG" > ".agent-selection.json"

echo "📋 Context available:"
echo "   - PRP: .current-prp.md"
echo "   - Agent: .agent-selection.json"
echo "   - Primary: $PRIMARY_AGENT"
```

#### Step 5: Implementation Guidance

```markdown
# Implementation Plan: ${issue.title}

## 🤖 Agent Assignment
- **Primary**: ${PRIMARY_AGENT}
- **Support**: ${SUPPORT_AGENTS}
- **Reason**: ${AGENT_CONFIG.reason}

## 📋 PRP Context
${prp ? `Following: ${prpName}` : 'No PRP linked'}

## 🏗️ Current State
${archContext.hasDebt ? `
- Component: ${archContext.component} (${archContext.lines} lines)
- Coverage: ${archContext.coverage}%
- Performance: ${archContext.performance}ms
` : 'Clean slate'}

## 🎯 Target State
${prp.targetState || 'As defined in issue'}

## 📝 Implementation Steps
Based on ${PRIMARY_AGENT} expertise:
${generateAgentSpecificSteps(PRIMARY_AGENT, issue, prp)}

## 🧪 Test-Driven Approach
1. Run tests (RED - ${testCount} failing)
2. Implement minimal solution
3. Refactor with confidence (GREEN)
4. Optimize if needed

## ✅ Success Criteria
${extractSuccessCriteria(prp, issue)}
```

### Action: VALIDATE

```bash
# Run agent-specific validations
case "$PRIMARY_AGENT" in
  "refactoring-expert")
    echo "♻️ Running refactoring validations..."
    # Check component sizes
    # Verify no regression
    # Check performance
    ;;
    
  "frontend")
    echo "🎨 Running frontend validations..."
    # Design system compliance
    # Accessibility checks
    # Component tests
    ;;
    
  "backend")
    echo "⚙️ Running backend validations..."
    # API tests
    # Integration tests
    # Performance benchmarks
    ;;
esac

# Standard validations
npm test
npm run validate:design
npm run test:coverage
```

### Action: COMPLETE

```bash
# Generate PR with agent context
generate_pr_body() {
  cat <<EOF
Closes #${ISSUE_NUMBER}

## 🤖 Development Team
- **Lead**: ${PRIMARY_AGENT}
- **Support**: ${SUPPORT_AGENTS}
- **Reason**: ${AGENT_CONFIG.reason}

## 📋 PRP Implementation
${prpName ? "Implements: \`PRPs/active/${prpName}.md\`" : "No PRP"}

## ✅ Acceptance Criteria
${checkCriteria()}

## 🧪 Testing
- Coverage: ${COVERAGE}
- Tests: ${testsPassing}/${totalTests} passing

## 📊 Metrics
${generateMetrics()}

## 📚 Documentation
- [ ] Updated by ${PRIMARY_AGENT}
- [ ] Reviewed by support agents
EOF
}
```

## Agent Selection Matrix

| Issue Type | Primary Agent | Support Agents | Focus |
|------------|--------------|----------------|-------|
| Refactoring | refactoring-expert | qa, performance | Break down monoliths |
| Testing | qa | tdd-specialist, backend | Test infrastructure |
| Frontend | frontend | ui-systems, form-builder | Components & UX |
| Backend | backend | database-architect, api | APIs & logic |
| Database | database-architect | orm-specialist | Schema & queries |
| Performance | performance | refactoring-expert | Optimization |
| Security | security | backend, database | Hardening |
| Infrastructure | platform-deployment | backend, qa | CI/CD & deployment |

## Usage Examples

### Refactoring Task
```bash
/fw start 23
# Output:
🤖 Selected Agent: refactoring-expert
   Reason: Major refactoring detected (3,053 lines)
   Support: [qa, performance]
♻️ Generating refactoring test suite...
```

### Test Infrastructure
```bash
/fw start 24
# Output:
🤖 Selected Agent: qa
   Reason: Test infrastructure setup
   Support: [tdd-specialist, backend]
🧪 Generating test framework setup...
```

### Frontend Feature
```bash
/fw start 25
# Output:
🤖 Selected Agent: frontend
   Reason: Frontend development
   Support: [ui-systems, form-builder-specialist]
🎨 Generating component tests...
```

## Key Improvements

1. **Smart Agent Selection** - Uses the right expert for each task
2. **PRP Context Loading** - Guides implementation
3. **Agent-Specific Tests** - Different test strategies per agent
4. **Contextual Validation** - Agent-appropriate checks
5. **Team Simulation** - Primary + support agents

This ensures the right expertise is applied to each issue!
