---
name: prp-to-issues
description: Convert PRPs to GitHub issues with duplicate detection and update support
aliases: [pti, issues-from-prps]
---

# PRP to GitHub Issues - Smart Converter

Converts PRPs to GitHub issues with duplicate detection, update support, and tracking.

## Usage

```bash
/prp-to-issues              # Convert all new PRPs
/prp-to-issues --force      # Re-create even if exists
/prp-to-issues --update     # Update existing issues
/prp-to-issues [prp-name]   # Convert specific PRP
```

## Process

### Phase 1: Duplicate Detection

```javascript
async function checkExistingIssues() {
  const tracking = loadTrackingFile('.agent-os/prp-issue-tracking.json');
  const githubIssues = await gh.api('GET /repos/{owner}/{repo}/issues');
  
  const status = {
    prps: [],
    alreadyCreated: [],
    needsCreation: [],
    needsUpdate: []
  };
  
  // Check each PRP
  for (const prpFile of getPRPFiles()) {
    const prpName = extractPRPName(prpFile);
    
    // Check tracking file
    if (tracking[prpName]) {
      const issueNumber = tracking[prpName].issueNumber;
      const lastModified = tracking[prpName].lastModified;
      
      // Check if PRP was updated after issue creation
      if (prpFile.mtime > lastModified) {
        status.needsUpdate.push({
          prp: prpName,
          issue: issueNumber,
          reason: 'PRP modified after issue creation'
        });
      } else {
        status.alreadyCreated.push({
          prp: prpName,
          issue: issueNumber
        });
      }
    } else {
      // Check GitHub for issues mentioning this PRP
      const existingIssue = githubIssues.find(i => 
        i.body.includes(`PRP: ${prpName}`) ||
        i.title.includes(prpName)
      );
      
      if (existingIssue) {
        // Found issue but not tracked locally
        tracking[prpName] = {
          issueNumber: existingIssue.number,
          lastModified: new Date().toISOString()
        };
        status.alreadyCreated.push({
          prp: prpName,
          issue: existingIssue.number
        });
      } else {
        status.needsCreation.push(prpName);
      }
    }
  }
  
  return status;
}
```

### Phase 2: Issue Tracking System

```json
// .agent-os/prp-issue-tracking.json
{
  "debt-form-refactor": {
    "issueNumber": 23,
    "subIssues": [24, 25, 26, 27, 28],
    "createdAt": "2024-02-07T10:00:00Z",
    "lastModified": "2024-02-07T10:00:00Z",
    "prpChecksum": "abc123...",
    "status": "created"
  },
  "rudderstack-bigquery": {
    "issueNumber": 29,
    "subIssues": [],
    "createdAt": "2024-02-07T11:00:00Z",
    "lastModified": "2024-02-07T11:00:00Z",
    "prpChecksum": "def456...",
    "status": "created"
  }
}
```

### Phase 3: Smart Issue Creation

```javascript
async function createIssuesSmartly(status) {
  console.log(`
📊 PRP to Issues Analysis:
  ✅ Already created: ${status.alreadyCreated.length}
  📝 Need creation: ${status.needsCreation.length}
  🔄 Need update: ${status.needsUpdate.length}
  `);
  
  // Show what's already done
  if (status.alreadyCreated.length > 0) {
    console.log('\n✅ Already Created (Skipping):');
    for (const item of status.alreadyCreated) {
      console.log(`  - ${item.prp} → Issue #${item.issue}`);
    }
  }
  
  // Show what needs updating
  if (status.needsUpdate.length > 0) {
    console.log('\n🔄 PRPs Modified (Need Update):');
    for (const item of status.needsUpdate) {
      console.log(`  - ${item.prp} → Issue #${item.issue}`);
      console.log(`    Reason: ${item.reason}`);
    }
    
    const answer = await prompt('Update existing issues? (y/n/skip): ');
    if (answer === 'y') {
      await updateExistingIssues(status.needsUpdate);
    }
  }
  
  // Create new issues
  if (status.needsCreation.length > 0) {
    console.log('\n📝 Creating New Issues:');
    for (const prpName of status.needsCreation) {
      const issue = await createIssueFromPRP(prpName);
      
      // Track it
      updateTracking(prpName, issue.number);
      
      console.log(`✅ Created: ${prpName} → Issue #${issue.number}`);
    }
  }
}
```

### Phase 4: Update Existing Issues

```javascript
async function updateExistingIssues(updates) {
  for (const update of updates) {
    const prp = loadPRP(`PRPs/active/${update.prp}.md`);
    const issue = await gh.api(`GET /repos/{owner}/{repo}/issues/${update.issue}`);
    
    // Compare and update
    const changes = [];
    
    // Check if acceptance criteria changed
    const newCriteria = extractAcceptanceCriteria(prp);
    const oldCriteria = extractAcceptanceCriteria(issue.body);
    
    if (newCriteria !== oldCriteria) {
      changes.push('Acceptance criteria updated');
    }
    
    // Check if implementation tasks changed
    const newTasks = extractTasks(prp);
    const oldTasks = extractTasks(issue.body);
    
    if (newTasks !== oldTasks) {
      changes.push('Implementation tasks updated');
    }
    
    if (changes.length > 0) {
      // Update issue body
      const updatedBody = generateIssueBody(prp) + `
      
---
📝 **Updated from PRP**: ${new Date().toISOString()}
Changes: ${changes.join(', ')}
      `;
      
      await gh.api(`PATCH /repos/{owner}/{repo}/issues/${update.issue}`, {
        body: updatedBody
      });
      
      // Add comment about update
      await gh.api(`POST /repos/{owner}/{repo}/issues/${update.issue}/comments`, {
        body: `🔄 Issue updated from PRP changes:\n- ${changes.join('\n- ')}`
      });
      
      console.log(`✅ Updated Issue #${update.issue}`);
    }
  }
}
```

### Phase 5: Tracking File Management

```javascript
function updateTracking(prpName, issueNumber, subIssues = []) {
  const trackingFile = '.agent-os/prp-issue-tracking.json';
  
  // Load existing or create new
  let tracking = {};
  if (fs.existsSync(trackingFile)) {
    tracking = JSON.parse(fs.readFileSync(trackingFile));
  }
  
  // Calculate checksum of PRP
  const prpContent = fs.readFileSync(`PRPs/active/${prpName}.md`);
  const checksum = crypto.createHash('md5').update(prpContent).digest('hex');
  
  // Update tracking
  tracking[prpName] = {
    issueNumber: issueNumber,
    subIssues: subIssues,
    createdAt: tracking[prpName]?.createdAt || new Date().toISOString(),
    lastModified: new Date().toISOString(),
    prpChecksum: checksum,
    status: 'created'
  };
  
  // Save
  fs.writeFileSync(trackingFile, JSON.stringify(tracking, null, 2));
}
```

## Workflow Examples

### First Time Creation
```bash
/prp-to-issues

📊 PRP to Issues Analysis:
  ✅ Already created: 0
  📝 Need creation: 5
  🔄 Need update: 0

📝 Creating New Issues:
✅ Created: debt-form-refactor → Issue #23
✅ Created: test-infrastructure → Issue #24
✅ Created: rudderstack-bigquery → Issue #25

✅ Tracking saved to .agent-os/prp-issue-tracking.json
```

### Running Again (Duplicate Detection)
```bash
/prp-to-issues

📊 PRP to Issues Analysis:
  ✅ Already created: 3
  📝 Need creation: 2
  🔄 Need update: 0

✅ Already Created (Skipping):
  - debt-form-refactor → Issue #23
  - test-infrastructure → Issue #24
  - rudderstack-bigquery → Issue #25

📝 Creating New Issues:
✅ Created: supabase-integration → Issue #26
✅ Created: performance-optimization → Issue #27
```

### After Modifying a PRP
```bash
# Edit PRPs/active/rudderstack-bigquery.md
vim PRPs/active/rudderstack-bigquery.md

/prp-to-issues

📊 PRP to Issues Analysis:
  ✅ Already created: 4
  📝 Need creation: 0
  🔄 Need update: 1

🔄 PRPs Modified (Need Update):
  - rudderstack-bigquery → Issue #25
    Reason: PRP modified after issue creation

Update existing issues? (y/n/skip): y

✅ Updated Issue #25
  - Acceptance criteria updated
  - Implementation tasks updated
  - Comment added to issue
```

### Force Recreation
```bash
/prp-to-issues --force debt-form-refactor

⚠️ Force mode: Will recreate even if exists

Found existing Issue #23 for debt-form-refactor
Close existing issue and create new? (y/n): y

✅ Closed Issue #23 with comment
✅ Created new Issue #28 for debt-form-refactor
✅ Tracking updated
```

## Update Workflow

### When to Update PRPs and Issues

1. **Small Changes** → Update PRP, then update issue:
```bash
# Edit PRP
vim PRPs/active/[name].md

# Update issue
/prp-to-issues --update [name]
```

2. **Major Changes** → Close old, create new:
```bash
# Edit PRP significantly
vim PRPs/active/[name].md

# Force recreation
/prp-to-issues --force [name]
```

3. **Check Status Anytime**:
```bash
/prp-to-issues --status

📊 PRP Issue Status:
✅ Synced:
  - debt-form-refactor → #23 (in sync)
  - test-infrastructure → #24 (in sync)

🔄 Out of Sync:
  - rudderstack-bigquery → #25 (PRP newer)

❌ Not Created:
  - new-feature-prp (no issue yet)
```

## Features

✅ **Duplicate Detection** - Never creates duplicate issues
✅ **Update Support** - Updates existing issues when PRPs change
✅ **Tracking File** - Maintains PRP-to-issue mapping
✅ **GitHub Integration** - Creates real GitHub issues
✅ **Smart Diffing** - Only updates what changed
✅ **Force Mode** - Can recreate if needed
✅ **Status Checking** - See sync status anytime

This ensures your PRPs and issues stay in sync!
