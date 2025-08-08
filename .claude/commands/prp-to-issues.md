---
name: prp-to-issues
description: Convert PRPs to GitHub issues with smart duplicate detection
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

### Phase 1: Check Repository

```bash
# Get the correct repository
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
echo "📍 Repository: $REPO"
```

### Phase 2: Duplicate Detection

```javascript
async function checkExistingIssues() {
  // Get repo info first
  const repoInfo = await execSync('gh repo view --json nameWithOwner -q .nameWithOwner').toString().trim();
  
  // Load tracking file
  const trackingFile = '.agent-os/prp-issue-tracking.json';
  let tracking = {};
  
  if (fs.existsSync(trackingFile)) {
    tracking = JSON.parse(fs.readFileSync(trackingFile, 'utf8'));
  } else {
    // Create tracking file
    fs.mkdirSync('.agent-os', { recursive: true });
    fs.writeFileSync(trackingFile, '{}', 'utf8');
  }
  
  // Get existing issues
  const issuesCmd = `gh issue list --repo ${repoInfo} --limit 100 --json number,title,body,state`;
  const issues = JSON.parse(execSync(issuesCmd).toString());
  
  // Check each PRP
  const prpFiles = fs.readdirSync('PRPs/active').filter(f => f.endsWith('.md'));
  
  const status = {
    needsCreation: [],
    alreadyCreated: [],
    needsUpdate: []
  };
  
  for (const prpFile of prpFiles) {
    const prpName = prpFile.replace('.md', '').replace('-prp', '');
    
    // Check if tracked
    if (tracking[prpName]) {
      status.alreadyCreated.push({
        prp: prpName,
        issue: tracking[prpName].issueNumber
      });
    } else {
      // Check if issue exists with this PRP name
      const existingIssue = issues.find(i => 
        i.title.toLowerCase().includes(prpName.toLowerCase()) ||
        i.body?.includes(`PRP: ${prpName}`)
      );
      
      if (existingIssue) {
        // Track it
        tracking[prpName] = {
          issueNumber: existingIssue.number,
          createdAt: new Date().toISOString()
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
  
  // Save tracking
  fs.writeFileSync(trackingFile, JSON.stringify(tracking, null, 2));
  
  return { status, tracking, repoInfo };
}
```

### Phase 3: Safe Issue Creation

```javascript
async function createIssueSafely(prpName, repoInfo) {
  const prpPath = `PRPs/active/${prpName}.md`;
  if (!prpPath.endsWith('-prp.md')) {
    prpPath = `PRPs/active/${prpName}-prp.md`;
  }
  
  // Read PRP content
  const prpContent = fs.readFileSync(prpPath, 'utf8');
  
  // Extract key information
  const title = extractTitle(prpContent, prpName);
  const goal = extractSection(prpContent, '🎯 Goal');
  const tasks = extractSection(prpContent, 'Implementation');
  const validation = extractSection(prpContent, 'Validation');
  
  // Create issue body
  const issueBody = `## 🎯 Feature: ${title}

### 📋 PRP Reference
- **PRP**: \`${prpPath}\`
- **Created**: ${new Date().toISOString()}

### 🎯 Goal
${goal || 'See PRP for details'}

### 📊 Context
${extractContext(prpContent)}

### ✅ Acceptance Criteria
${extractCriteria(prpContent)}

### 🔧 Implementation Tasks
${tasks || 'See PRP for implementation details'}

### 🧪 Validation
${validation || 'See PRP for validation loops'}

### 📚 Related Files
- PRP: \`${prpPath}\`
${extractRelatedFiles(prpContent)}
`;

  // Write to temp file (NOT in .agent-os)
  const tempFile = `/tmp/issue-${prpName}-${Date.now()}.md`;
  fs.writeFileSync(tempFile, issueBody);
  
  try {
    // Create issue using temp file
    const cmd = `gh issue create --repo ${repoInfo} --title "[PRP] ${title}" --body-file ${tempFile}`;
    const result = execSync(cmd).toString().trim();
    
    // Extract issue number from URL
    const issueNumber = result.match(/\/(\d+)$/)?.[1];
    
    // Clean up temp file
    fs.unlinkSync(tempFile);
    
    return {
      success: true,
      issueNumber: parseInt(issueNumber),
      url: result
    };
  } catch (error) {
    // Clean up temp file on error
    if (fs.existsSync(tempFile)) {
      fs.unlinkSync(tempFile);
    }
    
    // Try simpler approach without labels
    try {
      const simpleCmd = `gh issue create --repo ${repoInfo} --title "[PRP] ${title}" --body "${issueBody.substring(0, 1000)}..."`;
      const result = execSync(simpleCmd).toString().trim();
      const issueNumber = result.match(/\/(\d+)$/)?.[1];
      
      return {
        success: true,
        issueNumber: parseInt(issueNumber),
        url: result
      };
    } catch (e) {
      return {
        success: false,
        error: e.message
      };
    }
  }
}
```

### Phase 4: Helper Functions

```javascript
function extractTitle(prpContent, prpName) {
  // Try to extract from PRP header
  const match = prpContent.match(/^#\s+(?:PRP:\s+)?(.+?)(?:\s+-\s+|$)/m);
  if (match) return match[1].trim();
  
  // Clean up PRP name
  return prpName
    .replace(/-prp$/i, '')
    .replace(/[-_]/g, ' ')
    .replace(/\b\w/g, l => l.toUpperCase());
}

function extractSection(content, sectionName) {
  const regex = new RegExp(`##.*?${sectionName}.*?\\n([\\s\\S]*?)(?=\\n##|$)`, 'i');
  const match = content.match(regex);
  return match ? match[1].trim().substring(0, 500) : null;
}

function extractCriteria(content) {
  const section = extractSection(content, 'Success Criteria') || 
                  extractSection(content, 'Acceptance Criteria') || 
                  '';
  
  // Format as checkboxes
  return section
    .split('\n')
    .filter(line => line.trim())
    .map(line => line.startsWith('- [ ]') ? line : `- [ ] ${line.replace(/^[-*]\s*/, '')}`)
    .join('\n');
}
```

### Phase 5: Main Execution

```javascript
async function main() {
  console.log('🔍 Analyzing PRPs and existing issues...\n');
  
  const { status, tracking, repoInfo } = await checkExistingIssues();
  
  console.log(`📊 PRP to Issues Analysis:`);
  console.log(`  ✅ Already created: ${status.alreadyCreated.length}`);
  console.log(`  📝 Need creation: ${status.needsCreation.length}`);
  console.log(`  🔄 Need update: ${status.needsUpdate.length}\n`);
  
  // Show already created
  if (status.alreadyCreated.length > 0) {
    console.log('✅ Already Created (Skipping):');
    for (const item of status.alreadyCreated) {
      console.log(`  - ${item.prp} → Issue #${item.issue}`);
    }
    console.log('');
  }
  
  // Create new issues
  if (status.needsCreation.length > 0) {
    console.log('📝 Creating New Issues:\n');
    
    for (const prpName of status.needsCreation) {
      console.log(`🔨 Creating issue for: ${prpName}`);
      
      const result = await createIssueSafely(prpName, repoInfo);
      
      if (result.success) {
        console.log(`✅ Created: ${prpName} → Issue #${result.issueNumber}`);
        console.log(`   ${result.url}\n`);
        
        // Update tracking
        tracking[prpName] = {
          issueNumber: result.issueNumber,
          createdAt: new Date().toISOString(),
          url: result.url
        };
        
        // Save tracking after each success
        fs.writeFileSync('.agent-os/prp-issue-tracking.json', JSON.stringify(tracking, null, 2));
      } else {
        console.log(`❌ Failed to create issue for ${prpName}: ${result.error}\n`);
      }
      
      // Small delay between issues
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
  
  console.log('✅ Complete!');
  console.log(`📁 Tracking saved to: .agent-os/prp-issue-tracking.json`);
}

// Run if called directly
if (require.main === module) {
  main().catch(console.error);
}
```

## Features

✅ **Smart Repository Detection** - Uses gh repo view to get correct repo
✅ **Safe File Handling** - Uses /tmp for temporary files
✅ **Duplicate Detection** - Checks existing issues
✅ **Tracking File** - Maintains PRP-to-issue mapping
✅ **Error Recovery** - Falls back to simpler creation if needed
✅ **No Path Issues** - Uses relative paths correctly

## Example Output

```bash
/prp-to-issues

📍 Repository: bearingfruitco/debt-funnel

📊 PRP to Issues Analysis:
  ✅ Already created: 1
  📝 Need creation: 9

✅ Already Created (Skipping):
  - architecture-change-tracker → Issue #46

📝 Creating New Issues:

🔨 Creating issue for: debt-funnel-refactor
✅ Created: debt-funnel-refactor → Issue #47
   https://github.com/bearingfruitco/debt-funnel/issues/47

🔨 Creating issue for: test-infrastructure
✅ Created: test-infrastructure → Issue #48
   https://github.com/bearingfruitco/debt-funnel/issues/48

[continues...]
```

This version fixes all the issues!
