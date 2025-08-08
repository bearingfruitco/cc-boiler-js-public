# PRP: Context Aggregator - One-Pass Implementation Guide

> **PRP = PRD + Curated Codebase Intelligence + Validation Loops**
> This tool ensures AI agents have complete context for any issue.

## 🎯 Goal
Create a `/context [issue-number]` command that aggregates ALL relevant information for an issue into a single `.context/` folder, ensuring AI agents have 100% of needed context.

## 🔑 Why This Matters
- **User Value**: AI agents work correctly the first time
- **Business Value**: Reduces rework and failed attempts
- **Technical Value**: Eliminates context-switching and missing information

## ✅ Success Criteria (Measurable)
- [ ] Single command gathers all context in <10 seconds
- [ ] AI hallucination reduced by >50%
- [ ] Context folder contains 100% of needed files
- [ ] Auto-loads with `/fw start`
- [ ] Zero manual context searching needed

## 📚 Required Context

### Documentation & References
```yaml
- file: .claude/commands/feature-workflow.md
  why: Integration point - context loads with /fw start
  pattern: How fw loads PRP context currently
  gotcha: Must not duplicate existing context loading

- file: .claude/commands/prp-to-issues.md
  why: Understanding issue structure and tracking
  pattern: How issues link to PRPs
  gotcha: Issue tracking format varies

- file: .agent-os/prp-issue-tracking.json
  why: Maps PRPs to issues
  pattern: JSON structure for lookups
  gotcha: May not exist on new projects

- file: docs/architecture/*.md
  why: Architecture context needed for issues
  pattern: How to extract relevant sections
  gotcha: Not all sections relevant to all issues
```

### Known Gotchas & Critical Warnings
```markdown
# CRITICAL: Must handle missing files gracefully
# CRITICAL: Don't duplicate existing .current-context.md from /fw
# WARNING: GitHub API rate limits - cache when possible
# WARNING: Large contexts can overwhelm AI - smart filtering needed
# NOTE: Context should travel with branch
```

### Required Patterns From Codebase
```typescript
// 1. Issue fetching pattern (from prp-to-issues.md)
const issueCmd = `gh issue view ${issueNumber} --json title,body,labels`;
const issue = JSON.parse(execSync(issueCmd).toString());

// 2. PRP loading pattern (from feature-workflow.md)
const prpName = extractPRPFromIssue(issue);
const prpContent = fs.readFileSync(`PRPs/active/${prpName}.md`);

// 3. Safe file reading pattern
if (fs.existsSync(file) && fs.statSync(file).isFile()) {
  content = fs.readFileSync(file, 'utf8');
}
```

## 🏗️ Implementation Blueprint

### Phase 1: Command Structure (2 hours)
```typescript
// .claude/commands/context.md
---
name: context
description: Aggregate all context for an issue
aliases: [ctx, gather-context]
---

async function gatherContext(issueNumber) {
  // Create context directory
  const contextDir = `.context/issue-${issueNumber}`;
  fs.mkdirSync(contextDir, { recursive: true });
  
  // Gather all sources
  const issue = await fetchIssue(issueNumber);
  const prp = await fetchRelatedPRP(issue);
  const architecture = await fetchRelevantArchitecture(issue);
  const patterns = await findSimilarPatterns(issue);
  const tests = await findRelatedTests(issue);
  
  // Generate context files
  await generateContextFiles(contextDir, {
    issue, prp, architecture, patterns, tests
  });
}
```

### Phase 2: Context Gathering (3 hours)
```typescript
// Context sources to aggregate
const contextSources = {
  issue: {
    fetch: () => getGitHubIssue(issueNumber),
    output: 'issue.md'
  },
  prp: {
    fetch: () => getRelatedPRP(issue),
    output: 'requirements.md'
  },
  architecture: {
    fetch: () => getRelevantArchDocs(issue),
    output: 'architecture.md'
  },
  patterns: {
    fetch: () => findCodePatterns(issue),
    output: 'patterns.md'
  },
  tests: {
    fetch: () => findTestExamples(issue),
    output: 'test-examples.md'
  },
  design: {
    fetch: () => getDesignSystemRules(),
    output: 'design-rules.md'
  },
  schema: {
    fetch: () => getDatabaseSchema(issue),
    output: 'schema.sql'
  },
  env: {
    fetch: () => getRequiredEnvVars(issue),
    output: 'env-vars.md'
  }
};
```

### Phase 3: Context Structure (2 hours)
```markdown
# Generated .context/ structure
.context/issue-23/
├── README.md           # Overview and navigation
├── requirements.md     # From PRP + issue criteria
├── architecture.md     # Relevant arch docs
├── patterns.md        # Code examples to follow
├── test-examples.md   # How to test this
├── design-rules.md    # Design system constraints
├── warnings.md        # Gotchas and critical info
├── checklist.md       # Validation checklist
├── schema.sql         # If database related
└── env-vars.md        # Required environment
```

### Phase 4: Integration (1 hour)
```typescript
// Integrate with /fw start
function enhancedFwStart(issueNumber) {
  // First gather context
  console.log('📚 Gathering context...');
  await gatherContext(issueNumber);
  
  // Then normal fw start
  await originalFwStart(issueNumber);
  
  console.log('📁 Context available in .context/');
}
```

## 🧪 Validation Loops

### Loop 1: Context Completeness
- [ ] All required files present
- [ ] No broken references
- [ ] Issue details captured
- [ ] PRP linked correctly

### Loop 2: AI Testing
- [ ] Run with real issue
- [ ] Verify AI uses context
- [ ] Measure hallucination reduction
- [ ] Check for missing info

### Loop 3: Performance
- [ ] Completes in <10 seconds
- [ ] Handles missing files gracefully
- [ ] No API rate limit issues
- [ ] Context size reasonable (<1MB)

### Loop 4: Integration
- [ ] Works with /fw start
- [ ] Context travels with branch
- [ ] No conflicts with existing context
- [ ] Updates when issue changes

## 🚫 Common Mistakes to Avoid
- Duplicating existing context mechanisms
- Including irrelevant information
- Not handling missing files
- Creating huge context files
- Not caching API calls

## 📊 Success Metrics
- **Performance**: <10 seconds to gather
- **Completeness**: 100% of required files
- **AI Accuracy**: >50% reduction in errors
- **Size**: <1MB total context
