---
name: fw
description: Feature workflow with automatic branch management and priority awareness
aliases: [feature-workflow, feature, workflow]
---

# Feature Workflow Command - Enhanced

Complete issue-based development with automatic branching, PRP context, and smart prioritization.

🌿 **AUTO-BRANCHING**: Creates/checks out appropriate branches
🎯 **PRP-AWARE**: Loads context from related PRPs
🚦 **PRIORITY-AWARE**: Warns if starting lower priority with P0s pending

## Usage

```bash
/fw start [issue]      # Start work (creates branch)
/fw validate [issue]   # Run validations
/fw complete [issue]   # Complete and create PR
/fw status            # Show current work status
```

## Enhanced START Action

### Step 1: Priority Check

```javascript
async function checkPriority(issueNumber) {
  // Get all open issues
  const issues = await getOpenIssues();
  const targetIssue = issues.find(i => i.number === issueNumber);
  
  // Find P0 issues
  const p0Issues = issues.filter(i => i.labels.includes('P0'));
  
  if (!targetIssue.labels.includes('P0') && p0Issues.length > 0) {
    console.warn(`
⚠️ WARNING: There are ${p0Issues.length} P0 (Critical) issues:
${p0Issues.map(i => `  - #${i.number}: ${i.title}`).join('\n')}

You're starting: #${issueNumber} (${targetIssue.priority})

Continue anyway? (y/n): `);
    
    const answer = await prompt();
    if (answer !== 'y') {
      console.log('Suggesting: /next-issue');
      return false;
    }
  }
  
  return true;
}
```

### Step 2: Automatic Branch Management

```javascript
async function setupBranch(issue) {
  const issueNumber = issue.number;
  const issueTitle = issue.title;
  
  // Determine branch type from issue
  let branchType = 'feature';
  if (issue.labels.includes('bug')) branchType = 'fix';
  if (issue.labels.includes('refactor')) branchType = 'refactor';
  if (issue.labels.includes('test')) branchType = 'test';
  if (issue.labels.includes('docs')) branchType = 'docs';
  
  // Create branch name
  const slug = issueTitle
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .substring(0, 50);
  const branchName = `${branchType}/${issueNumber}-${slug}`;
  
  // Check if branch exists
  const branches = execSync('git branch -a').toString();
  const branchExists = branches.includes(branchName);
  
  if (branchExists) {
    console.log(`🌿 Branch exists: ${branchName}`);
    console.log(`📍 Checking out...`);
    execSync(`git checkout ${branchName}`);
    
    // Check if behind main
    const behind = execSync('git rev-list --count HEAD..main').toString().trim();
    if (parseInt(behind) > 0) {
      console.log(`⚠️ Branch is ${behind} commits behind main`);
      console.log(`🔄 Updating branch...`);
      execSync('git merge main');
    }
  } else {
    console.log(`🌿 Creating new branch: ${branchName}`);
    
    // Ensure we're on main and up to date
    console.log(`📍 Updating main branch...`);
    execSync('git checkout main');
    execSync('git pull origin main');
    
    // Create and checkout new branch
    execSync(`git checkout -b ${branchName}`);
    console.log(`✅ Branch created and checked out`);
    
    // Push branch to remote
    console.log(`🚀 Pushing branch to remote...`);
    execSync(`git push -u origin ${branchName}`);
  }
  
  return branchName;
}
```

### Step 3: Complete Workflow

```javascript
async function startFeatureWorkflow(issueNumber) {
  console.log(`
════════════════════════════════════════════════════
🚀 Starting Feature Workflow for Issue #${issueNumber}
════════════════════════════════════════════════════
`);
  
  // Step 1: Priority check
  const shouldContinue = await checkPriority(issueNumber);
  if (!shouldContinue) return;
  
  // Step 2: Get issue details
  const issue = await getIssue(issueNumber);
  console.log(`📋 Issue: ${issue.title}`);
  console.log(`🏷️ Labels: ${issue.labels.join(', ')}`);
  
  // Step 3: Setup branch
  const branchName = await setupBranch(issue);
  
  // Step 4: Load PRP context
  const prpName = extractPRPFromIssue(issue);
  if (prpName) {
    console.log(`📚 Loading PRP: ${prpName}`);
    const prp = loadPRP(`PRPs/active/${prpName}.md`);
    
    // Copy PRP to current branch for reference
    fs.copyFileSync(
      `PRPs/active/${prpName}.md`,
      `.current-context.md`
    );
    console.log(`📋 PRP context saved to .current-context.md`);
  }
  
  // Step 5: Select appropriate agent
  const agent = selectAgentForIssue(issue);
  console.log(`🤖 Selected Agent: ${agent.primary}`);
  console.log(`   Support: ${agent.support.join(', ')}`);
  
  // Step 6: Generate implementation plan
  console.log(`
📝 Implementation Plan
════════════════════════════════════════════════════

Branch: ${branchName}
Issue: #${issueNumber}
PRP: ${prpName || 'None'}
Agent: ${agent.primary}

Next Steps:
1. Review the issue requirements
2. Check .current-context.md for PRP details
3. Run tests to see current state
4. Implement feature/fix
5. Run /fw validate ${issueNumber}
6. Run /fw complete ${issueNumber}

Commands:
- View issue: gh issue view ${issueNumber}
- Run tests: npm test
- Validate: /fw validate ${issueNumber}
- Complete: /fw complete ${issueNumber}
════════════════════════════════════════════════════
`);
}
```

### Step 4: Status Command

```javascript
async function showStatus() {
  // Get current branch
  const currentBranch = execSync('git branch --show-current').toString().trim();
  
  // Parse issue number from branch
  const issueMatch = currentBranch.match(/(\d+)/);
  const issueNumber = issueMatch ? issueMatch[1] : null;
  
  // Get uncommitted changes
  const changes = execSync('git status --porcelain').toString();
  const hasChanges = changes.length > 0;
  
  console.log(`
📊 Current Work Status
════════════════════════════════════════════════════

🌿 Branch: ${currentBranch}
📋 Issue: ${issueNumber ? `#${issueNumber}` : 'None detected'}
💾 Changes: ${hasChanges ? 'Yes (uncommitted)' : 'None'}

${issueNumber ? `
Actions Available:
- /fw validate ${issueNumber} - Run validation
- /fw complete ${issueNumber} - Create PR
- gh issue view ${issueNumber} - View issue
` : `
No issue detected from branch name.
Use: /fw start [issue-number]
`}
════════════════════════════════════════════════════
`);
}
```

## Complete Example Flow

```bash
# 1. Check what to work on
/next-issue

Recommends: Issue #23 (P0)

# 2. Start work (automatic branching)
/fw start 23

🚀 Starting Feature Workflow for Issue #23
📋 Issue: Refactor DebtForm Component
🏷️ Labels: P0, refactor, tech-debt

🌿 Creating new branch: refactor/23-debt-form
✅ Branch created and checked out
🚀 Branch pushed to remote

📚 Loading PRP: debt-form-refactor
📋 PRP context saved to .current-context.md

🤖 Selected Agent: refactoring-expert
   Support: qa, performance

# 3. Do the work...

# 4. Validate
/fw validate 23

✅ Tests passing
✅ Coverage: 82%
✅ No linting errors
✅ Design system compliant

# 5. Complete
/fw complete 23

Creating PR from refactor/23-debt-form to main
✅ PR #145 created
🔗 https://github.com/user/repo/pull/145
```

## Key Features

### Automatic Branching
- Creates appropriate branch type (feature/fix/refactor)
- Checks for existing branches
- Keeps branches up to date with main
- Pushes to remote automatically

### Priority Awareness
- Warns if starting non-critical work with P0s pending
- Suggests higher priority issues
- Allows override with confirmation

### Context Loading
- Loads PRP into `.current-context.md`
- Preserves issue context
- Links to documentation

### Smart Workflow
- Detects current branch and issue
- Shows available actions
- Guides through complete flow

This ensures proper branch management and priority focus!
