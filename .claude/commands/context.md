---
name: context
description: Aggregate all context for an issue into one place
aliases: [ctx, gather-context, context-gather]
---

# Context Aggregator Command

Gathers ALL relevant information for an issue into a `.context/` folder, ensuring AI agents have complete context.

## Usage

```bash
/context [issue-number]       # Gather context for specific issue
/ctx 23                      # Short alias
/context --current           # Use current branch issue number
```

## Process

### Phase 1: Issue Analysis

```javascript
async function analyzeIssue(issueNumber) {
  // Get issue from GitHub
  const cmd = `gh issue view ${issueNumber} --json title,body,labels,assignees,projectItems`;
  const issue = JSON.parse(execSync(cmd).toString());
  
  // Extract key information
  const context = {
    number: issueNumber,
    title: issue.title,
    labels: issue.labels.map(l => l.name),
    type: detectIssueType(issue),
    prp: extractPRPReference(issue.body),
    requirements: extractRequirements(issue.body)
  };
  
  return context;
}
```

### Phase 2: Context Gathering

```javascript
async function gatherAllContext(issueNumber) {
  const contextDir = `.context/issue-${issueNumber}`;
  fs.mkdirSync(contextDir, { recursive: true });
  
  const sources = {
    // 1. Issue details
    issue: await getIssueDetails(issueNumber),
    
    // 2. Related PRP
    prp: await getRelatedPRP(issueNumber),
    
    // 3. Architecture docs
    architecture: await getRelevantArchitecture(issueNumber),
    
    // 4. Similar code patterns
    patterns: await findSimilarPatterns(issueNumber),
    
    // 5. Test examples
    tests: await findTestExamples(issueNumber),
    
    // 6. Design system rules
    design: await getDesignRules(),
    
    // 7. Database schema
    schema: await getDatabaseSchema(issueNumber),
    
    // 8. Environment variables
    env: await getRequiredEnvVars(issueNumber)
  };
  
  return sources;
}
```

### Phase 3: Context File Generation

```javascript
function generateContextFiles(contextDir, sources) {
  // 1. README with overview
  const readme = `# Context for Issue #${sources.issue.number}

## ${sources.issue.title}

### Quick Links
- [Requirements](./requirements.md)
- [Architecture](./architecture.md)
- [Code Patterns](./patterns.md)
- [Test Examples](./test-examples.md)
- [Design Rules](./design-rules.md)

### Type: ${sources.issue.type}
### Priority: ${sources.issue.priority}
### PRP: ${sources.prp?.name || 'None'}
`;
  fs.writeFileSync(`${contextDir}/README.md`, readme);
  
  // 2. Requirements from issue + PRP
  const requirements = combineRequirements(sources.issue, sources.prp);
  fs.writeFileSync(`${contextDir}/requirements.md`, requirements);
  
  // 3. Relevant architecture sections
  if (sources.architecture) {
    fs.writeFileSync(`${contextDir}/architecture.md`, sources.architecture);
  }
  
  // 4. Code patterns to follow
  if (sources.patterns.length > 0) {
    const patterns = formatPatterns(sources.patterns);
    fs.writeFileSync(`${contextDir}/patterns.md`, patterns);
  }
  
  // 5. Test examples
  if (sources.tests.length > 0) {
    const tests = formatTests(sources.tests);
    fs.writeFileSync(`${contextDir}/test-examples.md`, tests);
  }
  
  // 6. Warnings and gotchas
  const warnings = extractWarnings(sources);
  fs.writeFileSync(`${contextDir}/warnings.md`, warnings);
  
  // 7. Validation checklist
  const checklist = generateChecklist(sources);
  fs.writeFileSync(`${contextDir}/checklist.md`, checklist);
}
```

### Phase 4: Smart Pattern Finding

```javascript
function findSimilarPatterns(issue) {
  const patterns = [];
  const keywords = extractKeywords(issue);
  
  // Search for similar components
  if (issue.labels.includes('frontend')) {
    const components = glob.sync('src/components/**/*.tsx');
    for (const component of components) {
      if (matchesKeywords(component, keywords)) {
        patterns.push({
          file: component,
          type: 'component',
          relevance: calculateRelevance(component, keywords)
        });
      }
    }
  }
  
  // Search for similar API endpoints
  if (issue.labels.includes('backend')) {
    const apis = glob.sync('src/app/api/**/*.ts');
    for (const api of apis) {
      if (matchesKeywords(api, keywords)) {
        patterns.push({
          file: api,
          type: 'api',
          relevance: calculateRelevance(api, keywords)
        });
      }
    }
  }
  
  // Sort by relevance and return top 5
  return patterns
    .sort((a, b) => b.relevance - a.relevance)
    .slice(0, 5);
}
```

## Integration with /fw

```javascript
// Auto-load context when starting work
function enhancedFwStart(issueNumber) {
  console.log('📚 Gathering context...');
  
  // Gather context first
  await gatherContext(issueNumber);
  
  console.log('✅ Context ready in .context/');
  console.log('📁 Files created:');
  const files = fs.readdirSync(`.context/issue-${issueNumber}`);
  files.forEach(f => console.log(`   - ${f}`));
  
  // Continue with normal fw start
  await originalFwStart(issueNumber);
}
```

## Output Example

```bash
/context 23

📚 Gathering context for Issue #23...

🔍 Analyzing issue...
  Type: refactor
  Priority: P0
  PRP: debt-form-refactor

📂 Collecting sources...
  ✓ Issue details
  ✓ Related PRP found
  ✓ Architecture docs (3 sections)
  ✓ Similar patterns (5 files)
  ✓ Test examples (3 files)
  ✓ Design rules loaded
  ✓ Schema relevant
  ✓ Env vars identified

📝 Generating context files...
  Created: .context/issue-23/README.md
  Created: .context/issue-23/requirements.md
  Created: .context/issue-23/architecture.md
  Created: .context/issue-23/patterns.md
  Created: .context/issue-23/test-examples.md
  Created: .context/issue-23/design-rules.md
  Created: .context/issue-23/warnings.md
  Created: .context/issue-23/checklist.md
  Created: .context/issue-23/schema.sql
  Created: .context/issue-23/env-vars.md

✅ Context ready! Total size: 145KB

💡 Tips:
- Review README.md first for overview
- Check warnings.md for gotchas
- Use checklist.md to track progress
```

## Features

- **Complete Context** - All relevant info in one place
- **Smart Pattern Matching** - Finds similar code automatically
- **PRP Integration** - Loads related PRPs
- **Architecture Awareness** - Includes relevant docs
- **Test Examples** - Shows how to test
- **Design Rules** - Prevents violations
- **Validation Checklist** - Track completion

This ensures AI agents have everything they need!
