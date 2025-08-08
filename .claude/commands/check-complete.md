---
name: check-complete
description: Verify all requirements are met before marking as done
aliases: [check, complete-check, verify-complete, completeness]
---

# Completeness Checker Command

Ensures AI agents complete 100% of requirements, not just 80%. Catches missing error states, loading states, tests, and documentation.

## Usage

```bash
/check-complete [issue-number]    # Check specific issue
/check-complete --current         # Check current branch issue
/check                          # Short alias
/check-complete --block-pr      # Block PR if incomplete
```

## What It Checks

### UI Components
- ✅ Loading states
- ✅ Error states  
- ✅ Empty states
- ✅ Mobile responsiveness
- ✅ Accessibility (aria labels, keyboard nav)
- ✅ Touch targets (44px minimum)

### API Endpoints
- ✅ Input validation
- ✅ Error handling
- ✅ Auth checks
- ✅ Rate limiting
- ✅ TypeScript types
- ✅ API documentation

### Testing
- ✅ Test files exist
- ✅ Coverage >80%
- ✅ Happy path tests
- ✅ Error case tests
- ✅ Edge case tests

### Documentation
- ✅ README updated
- ✅ API docs updated
- ✅ Component docs
- ✅ Environment variables documented

## Process

### Phase 1: Requirement Extraction

```javascript
async function extractRequirements(issueNumber) {
  const requirements = {
    explicit: [],    // From checkboxes
    implicit: [],    // Detected from context
    standard: []     // Based on issue type
  };
  
  // Get issue content
  const issue = await getIssue(issueNumber);
  
  // Extract explicit checkboxes
  const checkboxRegex = /- \[([ x])\] (.+)/g;
  const matches = issue.body.matchAll(checkboxRegex);
  
  for (const match of matches) {
    requirements.explicit.push({
      text: match[2],
      completed: match[1] === 'x',
      type: 'explicit'
    });
  }
  
  // Detect implicit requirements
  if (issue.labels.includes('frontend')) {
    requirements.implicit.push(
      { text: 'Loading state implemented', type: 'implicit' },
      { text: 'Error state implemented', type: 'implicit' },
      { text: 'Empty state implemented', type: 'implicit' },
      { text: 'Mobile responsive', type: 'implicit' },
      { text: 'Accessibility compliant', type: 'implicit' }
    );
  }
  
  if (issue.labels.includes('backend')) {
    requirements.implicit.push(
      { text: 'Input validation', type: 'implicit' },
      { text: 'Error handling', type: 'implicit' },
      { text: 'Auth checks', type: 'implicit' },
      { text: 'TypeScript types', type: 'implicit' }
    );
  }
  
  // Add standard requirements
  requirements.standard.push(
    { text: 'Tests written', type: 'standard' },
    { text: 'Documentation updated', type: 'standard' },
    { text: 'No console errors', type: 'standard' },
    { text: 'Design system compliant', type: 'standard' }
  );
  
  return requirements;
}
```

### Phase 2: Completeness Verification

```javascript
class CompletenessChecker {
  async checkRequirement(req) {
    switch (req.text) {
      case 'Loading state implemented':
        return this.hasLoadingState();
      case 'Error state implemented':
        return this.hasErrorState();
      case 'Empty state implemented':
        return this.hasEmptyState();
      case 'Mobile responsive':
        return this.isMobileResponsive();
      case 'Tests written':
        return this.hasTests();
      case 'Documentation updated':
        return this.hasDocumentation();
      default:
        return this.genericCheck(req);
    }
  }
  
  hasLoadingState() {
    const patterns = [
      'isLoading',
      'loading &&',
      'setLoading',
      '<Skeleton',
      '<Spinner',
      'LoadingState'
    ];
    
    const files = this.getRelevantFiles();
    return this.searchPatterns(files, patterns);
  }
  
  hasErrorState() {
    const patterns = [
      'error &&',
      'isError',
      'ErrorBoundary',
      'catch (error)',
      'onError',
      'ErrorMessage'
    ];
    
    const files = this.getRelevantFiles();
    return this.searchPatterns(files, patterns);
  }
  
  hasEmptyState() {
    const patterns = [
      'length === 0',
      'isEmpty',
      'NoResults',
      'EmptyState',
      'No data',
      'empty &&'
    ];
    
    const files = this.getRelevantFiles();
    return this.searchPatterns(files, patterns);
  }
  
  async hasTests() {
    // Check for test files
    const testFiles = glob.sync('**/*.{test,spec}.{ts,tsx,js,jsx}');
    if (testFiles.length === 0) return false;
    
    // Check coverage
    try {
      const coverage = await this.getCoverage();
      return coverage >= 80;
    } catch {
      return false;
    }
  }
}
```

### Phase 3: Report Generation

```javascript
function generateReport(requirements) {
  const allReqs = [
    ...requirements.explicit,
    ...requirements.implicit,
    ...requirements.standard
  ];
  
  const completed = allReqs.filter(r => r.completed);
  const missing = allReqs.filter(r => !r.completed);
  const percentage = (completed.length / allReqs.length) * 100;
  
  const report = [];
  
  // Header
  report.push('# 📋 Completeness Check Report\n');
  
  // Summary with visual indicator
  const emoji = percentage === 100 ? '✅' : percentage >= 80 ? '🟡' : '❌';
  report.push(`## ${emoji} ${percentage.toFixed(1)}% Complete\n`);
  
  // Stats
  report.push('### Summary');
  report.push(`- ✅ Completed: ${completed.length}/${allReqs.length}`);
  report.push(`- ❌ Missing: ${missing.length}/${allReqs.length}\n`);
  
  // Missing items (if any)
  if (missing.length > 0) {
    report.push('## ❌ Missing Requirements\n');
    
    // Group by type
    const byType = groupBy(missing, 'type');
    
    if (byType.explicit) {
      report.push('### Explicit (from issue):');
      byType.explicit.forEach(req => {
        report.push(`- [ ] ${req.text}`);
        report.push(`  💡 ${getSuggestion(req)}`);
      });
      report.push('');
    }
    
    if (byType.implicit) {
      report.push('### Implicit (standard requirements):');
      byType.implicit.forEach(req => {
        report.push(`- [ ] ${req.text}`);
        report.push(`  💡 ${getSuggestion(req)}`);
      });
      report.push('');
    }
  }
  
  // Completed items
  report.push('## ✅ Completed Requirements\n');
  completed.forEach(req => {
    report.push(`- [x] ${req.text}`);
  });
  
  // Recommendations
  if (missing.length > 0) {
    report.push('\n## 🔧 How to Fix\n');
    report.push(generateFixInstructions(missing));
  }
  
  return report.join('\n');
}

function getSuggestion(req) {
  const suggestions = {
    'loading state': 'Add useState for isLoading and show spinner/skeleton',
    'error state': 'Add try-catch and error UI component',
    'empty state': 'Check data.length === 0 and show empty message',
    'mobile': 'Add responsive Tailwind classes (sm:, md:, lg:)',
    'tests': 'Create *.test.tsx file with describe/it blocks',
    'documentation': 'Update README.md with usage info'
  };
  
  const key = Object.keys(suggestions).find(k => 
    req.text.toLowerCase().includes(k)
  );
  
  return suggestions[key] || 'Review and implement this requirement';
}
```

## Integration

### With /fw workflow
```javascript
// Block incomplete work
function enhancedFwComplete(issueNumber) {
  console.log('📋 Checking completeness...');
  
  const report = await checkComplete(issueNumber);
  const match = report.match(/(\d+\.?\d*)% Complete/);
  const percentage = parseFloat(match[1]);
  
  if (percentage < 100) {
    console.error('❌ Cannot complete - requirements missing!');
    console.log(report);
    console.log('\n🔧 Fix the missing items and try again');
    process.exit(1);
  }
  
  console.log('✅ All requirements met!');
  await originalFwComplete(issueNumber);
}
```

### As Git Hook
```bash
#!/bin/bash
# .git/hooks/pre-push

BRANCH=$(git branch --show-current)
ISSUE=$(echo $BRANCH | grep -oE '[0-9]+')

if [ -n "$ISSUE" ]; then
  echo "Checking completeness for issue #$ISSUE..."
  /check-complete $ISSUE || exit 1
fi
```

## Output Example

```bash
/check-complete 23

📋 Checking Issue #23: Refactor DebtForm Component

🔍 Extracting requirements...
  Explicit: 5 requirements
  Implicit: 8 requirements  
  Standard: 4 requirements

🔎 Verifying completion...
  ✓ Component extraction
  ✓ State management
  ✓ Tests written
  ✗ Loading state
  ✗ Error state
  ✗ Documentation

# 📋 Completeness Check Report

## 🟡 76.5% Complete

### Summary
- ✅ Completed: 13/17
- ❌ Missing: 4/17

## ❌ Missing Requirements

### Implicit (standard requirements):
- [ ] Loading state implemented
  💡 Add useState for isLoading and show spinner/skeleton
- [ ] Error state implemented
  💡 Add try-catch and error UI component
- [ ] Empty state implemented
  💡 Check data.length === 0 and show empty message
- [ ] Documentation updated
  💡 Update README.md with usage info

## 🔧 How to Fix

1. Add loading state:
   const [isLoading, setIsLoading] = useState(false);
   if (isLoading) return <Spinner />;

2. Add error handling:
   try { ... } catch (error) { setError(error); }
   if (error) return <ErrorMessage error={error} />;

3. Add empty state:
   if (data.length === 0) return <EmptyState />;

4. Update docs:
   Add usage examples to README.md
```

## Features

- **Comprehensive** - Checks explicit and implicit requirements
- **Smart** - Detects common missing patterns
- **Actionable** - Provides specific fix instructions
- **Integrated** - Works with /fw workflow
- **Blocking** - Prevents incomplete PRs

This ensures AI agents deliver 100% complete features!
