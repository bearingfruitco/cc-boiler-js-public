---
name: prp-gameplan-execute
description: Execute the PRP gameplan by creating PRPs one by one with full context
aliases: [execute-prps, create-prps, prp-execute]
---

# Execute PRP Gameplan

Create PRPs one by one based on the gameplan, with full context and safety checks.

## Usage

```bash
/prp-gameplan-execute
/execute-prps  # alias
```

## Prerequisites

Must run `/analyze-for-prps` first to create the gameplan.

## Process

### Phase 1: Load Gameplan

```bash
# Check for gameplan
if [ ! -f "PRPs/gameplan/prp-gameplan.md" ]; then
  echo "❌ No gameplan found. Run /analyze-for-prps first"
  exit 1
fi

# Load the gameplan
GAMEPLAN=$(cat PRPs/gameplan/prp-gameplan.md)
PRP_LIST=$(extract_prp_list "$GAMEPLAN")
```

### Phase 2: Create PRPs One by One

For each PRP in the gameplan, I'll:

#### Step 1: Gather Context
```javascript
function gatherPRPContext(prpName) {
  // From gameplan
  const contextFiles = gameplan.getContextFiles(prpName);
  const warnings = gameplan.getWarnings(prpName);
  const dependencies = gameplan.getDependencies(prpName);
  
  // Fresh discovery
  const currentState = discoverCurrentImplementation(prpName);
  const workingSystems = findWorkingFeatures(prpName);
  const schemaInfo = analyzeDatabase(prpName);
  
  return {
    files: contextFiles,
    warnings: warnings,
    deps: dependencies,
    current: currentState,
    working: workingSystems,
    schema: schemaInfo
  };
}
```

#### Step 2: Create PRP with Full Context

```markdown
# Creating: ${prpName}

## 🔍 Context Discovery
Reading ${contextFiles.length} files...
Checking working systems...
Analyzing database schema...

## 📝 Generating PRP Structure

### Required Sections:
1. Context (with file references)
2. Current State vs Target State
3. DO NOT MODIFY list
4. Implementation Steps
5. Validation Loops
6. Success Criteria
7. Risk Mitigation

## ✅ Validation
Checking PRP structure...
Ensuring all sections present...
Verifying context completeness...
```

#### Step 3: Save with Progress

```bash
# Save PRP
echo "Creating PRP ${index}/${total}: ${prpName}"
save_prp "PRPs/active/${prpName}.md"

# Update progress
echo "✅ Created: ${prpName}"
echo "   Context files: ${contextFileCount}"
echo "   Warnings: ${warningCount}"
echo "   Priority: ${priority}"

# Pause between PRPs to avoid timeouts
sleep 2
```

### Phase 3: Progressive Creation

The command will create PRPs in batches to avoid timeouts:

```javascript
async function createPRPsProgressively(prpList) {
  const batches = [
    prpList.filter(p => p.priority === 'P0'), // Critical first
    prpList.filter(p => p.priority === 'P1'), // Important next
    prpList.filter(p => p.priority === 'P2')  // Enhancements last
  ];
  
  for (const batch of batches) {
    console.log(`Creating ${batch.length} PRPs (Priority: ${batch[0].priority})`);
    
    for (const prp of batch) {
      // Create with full context
      await createSinglePRP(prp);
      
      // Show progress
      showProgress(prp);
      
      // Pause to avoid timeout
      await sleep(2000);
    }
    
    // Confirm batch before continuing
    if (!confirmContinue()) break;
  }
}
```

### Phase 4: Creation Report

After each PRP:

```markdown
## PRP Creation Progress

✅ Created Successfully:
1. debt-form-refactor-prp.md
   - 15 context files included
   - 3 warnings noted
   - 5 working systems preserved

2. test-infrastructure-prp.md
   - 8 context files included
   - 1 warning noted
   - Package.json deps preserved

⏳ Remaining:
3. supabase-integration-prp.md (next)
4. rudderstack-bigquery-prp.md
5. sentry-enhancement-prp.md

Continue? (y/n)
```

## Safety Features

### Context Preservation
Each PRP will include:
- List of files that must not break
- Working features to preserve
- Revenue-critical code warnings
- Database schema constraints

### Timeout Prevention
- Creates one PRP at a time
- 2-second pause between PRPs
- Progress saved after each
- Can resume if interrupted

### Validation
- Checks PRP structure
- Ensures required sections
- Verifies context completeness
- Validates against templates

## Output

After completion:

```markdown
# PRP Creation Complete

## 📊 Summary
Created: 7 PRPs
Time taken: 12 minutes
Total context files: 76
Warnings preserved: 15

## ✅ Created PRPs
PRPs/active/
├── debt-form-refactor-prp.md (P0)
├── test-infrastructure-prp.md (P0)
├── supabase-integration-prp.md (P1)
├── rudderstack-bigquery-prp.md (P1)
├── sentry-enhancement-prp.md (P2)
├── performance-optimization-prp.md (P2)
└── monitoring-setup-prp.md (P2)

## 🎯 Next Steps
1. Review each PRP for accuracy
2. Run: /prp-to-issues
3. Start with: /fw start [first-issue]

## ⚠️ Critical Reminders
- DebtForm contains revenue logic
- Preserve ALL RudderStack tracking
- Database changes must be additive
- Test in staging first
```

## Interruption Handling

If interrupted, resume with:

```bash
/prp-gameplan-execute --resume

# Will skip already created PRPs
# Continues from where it left off
```

## Usage Example

```bash
# Step 1: Analyze and create gameplan
/analyze-for-prps

# Step 2: Review gameplan
cat PRPs/gameplan/prp-gameplan.md

# Step 3: Execute one by one
/prp-gameplan-execute

# Step 4: Convert to issues
/prp-to-issues
```

This ensures each PRP is created with full context without timeouts!
