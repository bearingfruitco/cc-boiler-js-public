# PRP: Completeness Checker - One-Pass Implementation Guide

> **PRP = PRD + Curated Codebase Intelligence + Validation Loops**
> This tool ensures AI agents complete 100% of requirements, not just 80%.

## 🎯 Goal
Create a `/check-complete [issue]` command that verifies ALL requirements are met, preventing incomplete implementations from AI agents.

## 🔑 Why This Matters
- **User Value**: Features actually work completely
- **Business Value**: No half-finished features in production
- **Technical Value**: Comprehensive test coverage and documentation

## ✅ Success Criteria (Measurable)
- [ ] Catches 100% of missing requirements
- [ ] Clear actionable output for what's missing
- [ ] Integrated with /fw workflow
- [ ] Blocks PRs if incomplete
- [ ] Runs in <10 seconds

## 📚 Required Context

### Documentation & References
```yaml
- file: .claude/commands/feature-workflow.md
  why: Integration point for validation
  pattern: How fw validate works
  gotcha: Must enhance, not duplicate

- file: .claude/commands/prp-to-issues.md
  why: Understanding acceptance criteria format
  pattern: How criteria are structured
  gotcha: Various checkbox formats

- file: .claude/hooks/pre-tool-use/16a-prp-validator.py
  why: Validation patterns
  pattern: How to check completeness
  gotcha: Don't duplicate validation

- pattern: **/*.test.ts
  why: Test coverage requirements
  usage: Check test existence
```

### Known Gotchas & Critical Warnings
```markdown
# CRITICAL: Must check implicit requirements (not just checkboxes)
# CRITICAL: Don't pass incomplete work as done
# WARNING: AI often skips error states and edge cases
# WARNING: Documentation frequently forgotten
# NOTE: Loading states almost always missing
```

### Required Patterns From Codebase
```typescript
// 1. Completeness checks needed
const COMPLETENESS_RULES = {
  components: {
    required: [
      'loading state',
      'error state', 
      'empty state',
      'mobile responsive',
      'accessibility'
    ]
  },
  api: {
    required: [
      'input validation',
      'error handling',
      'auth check',
      'rate limiting',
      'typed responses'
    ]
  },
  tests: {
    required: [
      'unit tests exist',
      'coverage >80%',
      'error cases',
      'edge cases',
      'happy path'
    ]
  }
};

// 2. Common missing items from AI
const AI_COMMONLY_FORGETS = [
  'Loading states',
  'Error boundaries',
  'Empty states',
  'Mobile views',
  'Aria labels',
  'Test files',
  'Documentation updates',
  'Environment variables'
];
```

## 🏗️ Implementation Blueprint

### Phase 1: Requirement Parser (2 hours)
```typescript
// .claude/commands/check-complete.md
---
name: check-complete
description: Verify all requirements are met
aliases: [check, complete-check, verify-complete]
---

interface Requirement {
  text: string;
  type: 'explicit' | 'implicit';
  completed: boolean;
  location?: string;
  evidence?: string;
}

async function parseRequirements(issueNumber: number): Promise<Requirement[]> {
  const requirements: Requirement[] = [];
  
  // Get issue content
  const issue = await getIssue(issueNumber);
  
  // Extract explicit requirements (checkboxes)
  const checkboxes = extractCheckboxes(issue.body);
  requirements.push(...checkboxes);
  
  // Extract implicit requirements
  const implicit = detectImplicitRequirements(issue);
  requirements.push(...implicit);
  
  // Add standard requirements based on type
  const standard = getStandardRequirements(issue.labels);
  requirements.push(...standard);
  
  return requirements;
}
```

### Phase 2: Completeness Verification (3 hours)
```typescript
// Verification engine
class CompletenessChecker {
  async checkRequirement(req: Requirement): Promise<boolean> {
    switch (req.type) {
      case 'explicit':
        return this.checkExplicit(req);
      case 'implicit':
        return this.checkImplicit(req);
      default:
        return false;
    }
  }
  
  // Check explicit requirements
  async checkExplicit(req: Requirement): Promise<boolean> {
    // Search for evidence in code
    const evidence = await this.findEvidence(req.text);
    req.evidence = evidence;
    req.completed = !!evidence;
    return req.completed;
  }
  
  // Check implicit requirements
  async checkImplicit(req: Requirement): Promise<boolean> {
    // Check for common patterns
    if (req.text.includes('loading state')) {
      return this.hasLoadingState();
    }
    if (req.text.includes('error handling')) {
      return this.hasErrorHandling();
    }
    if (req.text.includes('tests')) {
      return this.hasTests();
    }
    // ... more checks
  }
  
  // Specific checks
  hasLoadingState(): boolean {
    const patterns = [
      'isLoading',
      'loading &&',
      '<Skeleton',
      '<Spinner'
    ];
    return this.searchPatterns(patterns);
  }
  
  hasErrorHandling(): boolean {
    const patterns = [
      'catch (error)',
      'error &&',
      '<ErrorBoundary',
      'onError'
    ];
    return this.searchPatterns(patterns);
  }
}
```

### Phase 3: Report Generation (2 hours)
```typescript
// Generate completeness report
function generateReport(requirements: Requirement[]): string {
  const completed = requirements.filter(r => r.completed);
  const missing = requirements.filter(r => !r.completed);
  const percentage = (completed.length / requirements.length) * 100;
  
  const report = [];
  
  // Summary
  report.push('# Completeness Check Report\n');
  report.push(`## Summary: ${percentage.toFixed(1)}% Complete\n`);
  report.push(`✅ Completed: ${completed.length}`);
  report.push(`❌ Missing: ${missing.length}\n`);
  
  // Missing items (priority)
  if (missing.length > 0) {
    report.push('## ❌ Missing Requirements\n');
    for (const req of missing) {
      report.push(`### ${req.text}`);
      report.push(`Type: ${req.type}`);
      report.push(`Action: ${getSuggestion(req)}\n`);
    }
  }
  
  // Completed items
  report.push('## ✅ Completed Requirements\n');
  for (const req of completed) {
    report.push(`- ${req.text}`);
    if (req.evidence) {
      report.push(`  Evidence: ${req.evidence}`);
    }
  }
  
  // Recommendations
  report.push('\n## Recommendations\n');
  report.push(generateRecommendations(missing));
  
  return report.join('\n');
}

// Generate fix suggestions
function getSuggestion(req: Requirement): string {
  const suggestions = {
    'loading state': 'Add isLoading state and show spinner/skeleton',
    'error state': 'Add error handling with try-catch and error UI',
    'empty state': 'Add check for empty data and show appropriate message',
    'tests': 'Create test file with describe/it blocks',
    'mobile': 'Add responsive classes and test on mobile viewport'
  };
  
  for (const [key, suggestion] of Object.entries(suggestions)) {
    if (req.text.toLowerCase().includes(key)) {
      return suggestion;
    }
  }
  
  return 'Review requirement and implement';
}
```

### Phase 4: Workflow Integration (1 hour)
```typescript
// Integrate with /fw workflow
function enhancedComplete(issueNumber: number) {
  // First check completeness
  console.log('📋 Checking completeness...');
  const report = await checkComplete(issueNumber);
  
  const match = report.match(/(\d+\.?\d*)% Complete/);
  const percentage = parseFloat(match[1]);
  
  if (percentage < 100) {
    console.error('❌ Implementation incomplete!');
    console.log(report);
    console.log('\n🔧 Fix missing items and try again');
    process.exit(1);
  }
  
  console.log('✅ All requirements met!');
  
  // Continue with PR creation
  await originalComplete(issueNumber);
}

// Add as git hook
// .git/hooks/pre-push
#!/bin/bash
ISSUE=$(git branch --show-current | grep -oE '[0-9]+')
if [ -n "$ISSUE" ]; then
  /check-complete $ISSUE || exit 1
fi
```

## 🧪 Validation Loops

### Loop 1: Requirement Detection
- [ ] Finds all explicit requirements
- [ ] Detects implicit requirements
- [ ] Includes standard requirements
- [ ] No false requirements

### Loop 2: Verification Accuracy
- [ ] Correctly identifies completed
- [ ] Correctly identifies missing
- [ ] Provides evidence
- [ ] No false positives

### Loop 3: Actionability
- [ ] Clear what's missing
- [ ] Specific fix suggestions
- [ ] Helpful recommendations
- [ ] Easy to understand

### Loop 4: Integration
- [ ] Works with /fw workflow
- [ ] Blocks incomplete PRs
- [ ] Git hook compatible
- [ ] Fast execution

## 🚫 Common Mistakes to Avoid
- Only checking explicit checkboxes
- Missing implicit requirements
- Not checking test coverage
- Ignoring documentation
- Passing partial completion

## 📊 Success Metrics
- **Coverage**: 100% of requirements checked
- **Accuracy**: Zero false positives
- **Speed**: <10 seconds execution
- **Prevention**: Zero incomplete PRs merged
