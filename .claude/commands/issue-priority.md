---
name: issue-priority
description: Analyze and suggest which issues to work on based on priority and dependencies
aliases: [next-issue, what-next, priority]
---

# Issue Priority Analyzer

Suggests which issue to work on next based on priority, dependencies, and current state.

## Usage

```bash
/issue-priority          # Show prioritized issue list
/next-issue             # Suggest single next issue
/what-next              # Alias for next-issue
```

## Process

### Phase 1: Gather Issue Data

```javascript
async function analyzeIssuePriority() {
  // Get all open issues
  const issues = await gh.api('GET /repos/{owner}/{repo}/issues', {
    state: 'open',
    labels: 'from-prp'
  });
  
  // Load PRP tracking to get priorities
  const tracking = loadJSON('.agent-os/prp-issue-tracking.json');
  
  // Analyze each issue
  const analyzed = issues.map(issue => {
    const prpName = extractPRPName(issue.body);
    const priority = determinePriority(issue, tracking[prpName]);
    
    return {
      number: issue.number,
      title: issue.title,
      priority: priority.level, // P0, P1, P2
      score: priority.score,     // Numeric for sorting
      blockers: findBlockers(issue),
      blocked: isBlocked(issue),
      effort: estimateEffort(issue),
      type: getIssueType(issue),
      branch: checkBranchStatus(issue)
    };
  });
  
  return analyzed.sort((a, b) => b.score - a.score);
}
```

### Phase 2: Priority Scoring System

```javascript
function calculatePriorityScore(issue) {
  let score = 0;
  
  // Priority level (P0=100, P1=50, P2=25)
  if (issue.labels.includes('P0')) score += 100;
  else if (issue.labels.includes('P1')) score += 50;
  else if (issue.labels.includes('P2')) score += 25;
  
  // Issue type bonuses
  if (issue.labels.includes('bug')) score += 30;
  if (issue.labels.includes('security')) score += 50;
  if (issue.labels.includes('performance')) score += 20;
  if (issue.labels.includes('tech-debt')) score += 15;
  
  // Blocking other issues
  if (issue.blockingCount > 0) score += (issue.blockingCount * 10);
  
  // Revenue impact
  if (issue.body.includes('revenue') || issue.body.includes('conversion')) score += 25;
  
  // Already started (in-progress branch exists)
  if (issue.hasBranch) score += 10;
  
  // Effort consideration (prefer quick wins for ties)
  if (score < 50 && issue.effort === 'small') score += 5;
  
  return score;
}
```

### Phase 3: Dependency Analysis

```javascript
function analyzeDependencies(issues) {
  const dependencies = {};
  
  for (const issue of issues) {
    dependencies[issue.number] = {
      blocks: [],    // Issues this blocks
      blockedBy: [], // Issues blocking this
      canStart: true // Can start immediately?
    };
    
    // Check for dependency mentions
    const depMatches = issue.body.matchAll(/(?:blocks?|depends on|requires?)\s+#(\d+)/gi);
    for (const match of depMatches) {
      const depNumber = parseInt(match[1]);
      dependencies[issue.number].blockedBy.push(depNumber);
      dependencies[depNumber]?.blocks.push(issue.number);
    }
    
    // Check if can start
    dependencies[issue.number].canStart = dependencies[issue.number].blockedBy.every(
      dep => isIssueClosed(dep)
    );
  }
  
  return dependencies;
}
```

### Phase 4: Branch Management

```javascript
function checkAndSuggestBranch(issue) {
  // Check if branch exists
  const branches = execSync('git branch -a').toString();
  const branchPatterns = [
    `feature/${issue.number}`,
    `fix/${issue.number}`,
    `refactor/${issue.number}`
  ];
  
  const existingBranch = branchPatterns.find(pattern => 
    branches.includes(pattern)
  );
  
  if (existingBranch) {
    return {
      exists: true,
      name: existingBranch,
      action: 'checkout'
    };
  }
  
  // Suggest branch name based on issue type
  const branchType = determineBranchType(issue);
  const branchName = `${branchType}/${issue.number}-${slugify(issue.title)}`;
  
  return {
    exists: false,
    name: branchName,
    action: 'create',
    command: `git checkout -b ${branchName}`
  };
}
```

## Output Format

### Priority List View

```
🎯 Issue Priority Analysis
══════════════════════════════════════════════════

🔴 CRITICAL (P0) - Start Immediately
─────────────────────────────────────
#23 📊 Refactor DebtForm Component
  Score: 135 | Effort: Large (5-7 days)
  ⚡ Blocks: 3 other issues
  🌿 Branch: feature/23-debt-form (exists)
  
  ➜ Recommended: Start this first
  Command: git checkout feature/23-debt-form

#24 🧪 Test Infrastructure Setup
  Score: 120 | Effort: Medium (3-4 days)
  ⚡ Blocks: All testing work
  🌿 Branch: Not created
  
  ➜ Create branch: git checkout -b feature/24-test-infrastructure

🟡 IMPORTANT (P1) - Next Sprint
─────────────────────────────────────
#25 🔗 RudderStack BigQuery Integration
  Score: 75 | Effort: Medium (3-5 days)
  ⛔ Blocked by: #24 (test setup)
  🌿 Branch: Not created
  
  ➜ Wait for #24 completion

#26 🗄️ Supabase Integration
  Score: 70 | Effort: Large (5-7 days)
  ✅ No blockers
  🌿 Branch: Not created

🟢 ENHANCEMENT (P2) - When Available
─────────────────────────────────────
#27 ⚡ Performance Optimization
  Score: 45 | Effort: Small (1-2 days)
  ⛔ Blocked by: #23 (refactoring)
  
══════════════════════════════════════════════════

📍 RECOMMENDATION: Start with Issue #23
══════════════════════════════════════════════════
Reasons:
• Highest priority (P0)
• Blocks 3 other issues
• Branch already exists
• Revenue-critical component

Next steps:
1. git checkout feature/23-debt-form
2. /fw start 23
```

### Single Recommendation View

```bash
/next-issue

🎯 Next Issue Recommendation: #23

📊 Refactor DebtForm Component
Priority: P0 (Critical)
Effort: 5-7 days
Status: Not started

Why this issue:
✓ Highest priority score (135)
✓ Blocks 3 other issues
✓ Revenue-critical component
✓ No dependencies

🌿 Branch Setup:
git checkout -b feature/23-debt-form

🚀 Start Development:
/fw start 23

Alternative if blocked:
Issue #24 - Test Infrastructure (P0, no blockers)
```

## Integration with Workflow

### Automatic Branch Creation

```javascript
function startIssueWithBranch(issueNumber) {
  const issue = getIssue(issueNumber);
  const branch = checkAndSuggestBranch(issue);
  
  if (!branch.exists) {
    console.log(`🌿 Creating branch: ${branch.name}`);
    execSync(`git checkout -b ${branch.name}`);
    console.log(`✅ Branch created and checked out`);
  } else {
    console.log(`🌿 Checking out existing branch: ${branch.name}`);
    execSync(`git checkout ${branch.name}`);
    console.log(`✅ Switched to branch`);
  }
  
  // Now start the feature workflow
  console.log(`🚀 Starting development on Issue #${issueNumber}`);
  execSync(`/fw start ${issueNumber}`);
}
```

## Smart Features

### 1. Dependency Awareness
- Won't suggest blocked issues
- Prioritizes blocking issues
- Shows dependency chains

### 2. Branch Management
- Checks for existing branches
- Suggests appropriate branch names
- Handles checkout/creation

### 3. Priority Scoring
- P0 > P1 > P2
- Revenue impact bonus
- Quick wins for ties
- Blocker consideration

### 4. Context Awareness
- Checks current branch
- Identifies work in progress
- Suggests resuming vs starting new

## Usage Examples

### Get Priority List
```bash
/issue-priority

Shows all issues ranked by:
- Priority level
- Dependencies
- Effort
- Revenue impact
```

### Get Single Recommendation
```bash
/next-issue

Recommends: Issue #23
Reason: Highest priority, blocks others
Command: git checkout -b feature/23-debt-form
```

### Start Recommended Issue
```bash
/next-issue --start

Automatically:
1. Identifies Issue #23
2. Creates branch feature/23-debt-form
3. Runs /fw start 23
```

This gives you intelligent issue prioritization!
