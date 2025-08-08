# PRP: Pattern Enforcer - One-Pass Implementation Guide

> **PRP = PRD + Curated Codebase Intelligence + Validation Loops**
> This tool automatically fixes common AI coding mistakes to maintain consistency.

## 🎯 Goal
Create a `/enforce-patterns` command that automatically detects and fixes common AI agent mistakes, especially design system violations and missing error handling.

## 🔑 Why This Matters
- **User Value**: Consistent, high-quality code every time
- **Business Value**: Reduced review cycles and rework
- **Technical Value**: Maintains codebase standards automatically

## ✅ Success Criteria (Measurable)
- [ ] Catches >90% of design system violations
- [ ] Auto-fixes without breaking functionality
- [ ] Runs in <5 seconds on average component
- [ ] Zero false positives for valid patterns
- [ ] Educational output explains fixes

## 📚 Required Context

### Documentation & References
```yaml
- file: .claude/hooks/pre-tool-use/08-design-validator.py
  why: Existing design validation patterns
  pattern: How violations are detected
  gotcha: Must integrate, not duplicate

- file: docs/DESIGN_SYSTEM.md
  why: Source of truth for design rules
  pattern: Typography and spacing rules
  gotcha: Only 4 font sizes, 2 weights allowed

- file: .claude/commands/vd.md
  why: Existing validation command
  pattern: How validation currently works
  gotcha: Should enhance, not replace

- pattern: src/components/**/*.tsx
  why: Find correct patterns in use
  usage: Extract working examples
```

### Known Gotchas & Critical Warnings
```markdown
# CRITICAL: Only text-size-[1-4] and font-regular/semibold allowed
# CRITICAL: All spacing must be divisible by 4
# CRITICAL: Must preserve functionality when fixing
# WARNING: AI often uses text-sm, text-lg - always wrong
# WARNING: Don't break existing working code
# NOTE: Educational output helps AI learn
```

### Required Patterns From Codebase
```typescript
// 1. Design system violations AI makes
const COMMON_VIOLATIONS = {
  // Typography
  'text-sm': 'text-size-3',
  'text-lg': 'text-size-2',
  'text-xl': 'text-size-1',
  'font-bold': 'font-semibold',
  'font-medium': 'font-regular',
  
  // Spacing (not divisible by 4)
  'p-5': 'p-4',
  'p-7': 'p-6',
  'm-5': 'm-4',
  'gap-5': 'gap-4',
  
  // Touch targets
  'h-8': 'h-11', // Min 44px
  'h-10': 'h-11' // Min 44px
};

// 2. Missing error handling pattern
// AI writes:
const data = await fetchData();

// Should be:
try {
  setLoading(true);
  const data = await fetchData();
  // use data
} catch (error) {
  console.error('Error:', error);
  setError(error.message);
} finally {
  setLoading(false);
}
```

## 🏗️ Implementation Blueprint

### Phase 1: Detection System (3 hours)
```typescript
// .claude/commands/enforce-patterns.md
---
name: enforce-patterns
description: Auto-fix common AI coding mistakes
aliases: [fix-patterns, enforce, fix-ai]
---

interface Violation {
  file: string;
  line: number;
  type: 'design' | 'error-handling' | 'import' | 'console';
  original: string;
  fixed: string;
  explanation: string;
}

async function detectViolations(files: string[]): Promise<Violation[]> {
  const violations: Violation[] = [];
  
  for (const file of files) {
    // Check design system
    violations.push(...checkDesignViolations(file));
    
    // Check error handling
    violations.push(...checkErrorHandling(file));
    
    // Check imports
    violations.push(...checkImportOrder(file));
    
    // Check console logs
    violations.push(...checkConsoleLogs(file));
  }
  
  return violations;
}
```

### Phase 2: Auto-Fix System (4 hours)
```typescript
// Pattern fixing engine
class PatternFixer {
  // Fix design violations
  fixDesignViolations(content: string): string {
    let fixed = content;
    
    // Replace forbidden classes
    for (const [wrong, right] of Object.entries(COMMON_VIOLATIONS)) {
      const regex = new RegExp(`\\b${wrong}\\b`, 'g');
      fixed = fixed.replace(regex, right);
    }
    
    // Fix touch targets
    fixed = this.fixTouchTargets(fixed);
    
    // Fix spacing
    fixed = this.fixSpacing(fixed);
    
    return fixed;
  }
  
  // Add missing error handling
  fixErrorHandling(content: string): string {
    // Find await without try-catch
    const awaitRegex = /^(?!.*try).*await\s+(\w+)\([^)]*\)/gm;
    
    return content.replace(awaitRegex, (match) => {
      return `try {\n  ${match}\n} catch (error) {\n  console.error(error);\n}`;
    });
  }
  
  // Fix import order
  fixImportOrder(content: string): string {
    const imports = this.extractImports(content);
    const sorted = this.sortImports(imports);
    return this.replaceImports(content, sorted);
  }
}
```

### Phase 3: Educational Output (2 hours)
```typescript
// Generate educational report
function generateReport(violations: Violation[]): string {
  const report = [];
  
  report.push('# Pattern Enforcement Report\n');
  report.push(`Found and fixed ${violations.length} violations\n`);
  
  // Group by type
  const byType = groupBy(violations, 'type');
  
  for (const [type, items] of Object.entries(byType)) {
    report.push(`\n## ${type} (${items.length} violations)\n`);
    
    for (const violation of items) {
      report.push(`### ${violation.file}:${violation.line}`);
      report.push(`❌ Was: \`${violation.original}\``);
      report.push(`✅ Now: \`${violation.fixed}\``);
      report.push(`📚 Why: ${violation.explanation}\n`);
    }
  }
  
  // Add learning section
  report.push('\n## Remember for next time:');
  report.push('- Always use text-size-[1-4], never text-sm/lg/xl');
  report.push('- All spacing must be divisible by 4');
  report.push('- Minimum touch target is 44px (h-11)');
  report.push('- Always wrap await in try-catch');
  
  return report.join('\n');
}
```

### Phase 4: Integration (1 hour)
```typescript
// Integrate with /fw validate
function enhancedValidate() {
  // First run pattern enforcement
  console.log('🔧 Enforcing patterns...');
  const violations = await enforcePatterns();
  
  if (violations.length > 0) {
    console.log(`Fixed ${violations.length} violations`);
    console.log('Run git diff to see changes');
  }
  
  // Then normal validation
  await originalValidate();
}

// Add pre-commit hook option
// .git/hooks/pre-commit
#!/bin/bash
/enforce-patterns --quiet || exit 1
```

## 🧪 Validation Loops

### Loop 1: Detection Accuracy
- [ ] Catches all design violations
- [ ] Finds missing error handling
- [ ] Identifies wrong imports
- [ ] No false positives

### Loop 2: Fix Safety
- [ ] Fixes don't break code
- [ ] Preserves functionality
- [ ] Maintains formatting
- [ ] Handles edge cases

### Loop 3: Performance
- [ ] Runs in <5 seconds
- [ ] Handles large files
- [ ] Efficient regex patterns
- [ ] Minimal memory usage

### Loop 4: Education
- [ ] Clear explanations
- [ ] Actionable feedback
- [ ] Learning improvements
- [ ] Pattern documentation

## 🚫 Common Mistakes to Avoid
- Over-fixing valid variations
- Breaking working code
- Not preserving comments
- Missing context in fixes
- Not explaining why

## 📊 Success Metrics
- **Accuracy**: >90% violations caught
- **Safety**: Zero functionality breaks
- **Speed**: <5 seconds average
- **Learning**: AI violations decrease over time
