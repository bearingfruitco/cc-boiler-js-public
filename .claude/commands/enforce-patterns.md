---
name: enforce-patterns
description: Auto-fix common AI coding mistakes and design violations
aliases: [fix-patterns, enforce, fix-ai, pattern-fix]
---

# Pattern Enforcer Command

Automatically detects and fixes common AI agent mistakes, especially design system violations and missing error handling.

## Usage

```bash
/enforce-patterns              # Fix all files in current changes
/enforce-patterns [file]       # Fix specific file
/fix-ai                       # Short alias
/enforce-patterns --check     # Check only, don't fix
/enforce-patterns --report    # Generate detailed report
```

## Common AI Mistakes Fixed

### Design System Violations
```javascript
// AI writes:
<div className="text-sm font-bold p-5 m-7">

// Fixed to:
<div className="text-size-3 font-semibold p-4 m-6">
```

### Missing Error Handling
```javascript
// AI writes:
const data = await fetchData();

// Fixed to:
try {
  const data = await fetchData();
} catch (error) {
  console.error('Error fetching data:', error);
  throw error;
}
```

### Missing Loading States
```javascript
// AI writes:
function Component() {
  const data = useData();
  return <div>{data}</div>;
}

// Fixed to:
function Component() {
  const [isLoading, setIsLoading] = useState(true);
  const data = useData();
  
  if (isLoading) return <LoadingSpinner />;
  return <div>{data}</div>;
}
```

## Process

### Phase 1: Violation Detection

```javascript
const VIOLATIONS = {
  // Typography - STRICT
  'text-xs': 'text-size-4',
  'text-sm': 'text-size-3',
  'text-base': 'text-size-3',
  'text-lg': 'text-size-2',
  'text-xl': 'text-size-1',
  'text-2xl': 'text-size-1',
  'font-light': 'font-regular',
  'font-medium': 'font-regular',
  'font-bold': 'font-semibold',
  'font-black': 'font-semibold',
  
  // Spacing - Must be divisible by 4
  'p-1': 'p-1',  // 4px - OK
  'p-2': 'p-2',  // 8px - OK
  'p-3': 'p-3',  // 12px - OK
  'p-5': 'p-4',  // 20px → 16px
  'p-7': 'p-6',  // 28px → 24px
  'p-9': 'p-8',  // 36px → 32px
  'm-5': 'm-4',
  'm-7': 'm-6',
  'gap-5': 'gap-4',
  'gap-7': 'gap-6',
  'space-x-5': 'space-x-4',
  'space-y-5': 'space-y-4',
  
  // Touch targets - Min 44px
  'h-8': 'h-11',   // 32px → 44px
  'h-9': 'h-11',   // 36px → 44px
  'h-10': 'h-11',  // 40px → 44px
};

function detectViolations(content) {
  const violations = [];
  
  // Check each violation pattern
  for (const [wrong, right] of Object.entries(VIOLATIONS)) {
    const regex = new RegExp(`className="[^"]*\\b${wrong}\\b[^"]*"`, 'g');
    const matches = content.matchAll(regex);
    
    for (const match of matches) {
      violations.push({
        type: 'design',
        line: getLineNumber(content, match.index),
        original: wrong,
        fixed: right,
        context: match[0]
      });
    }
  }
  
  return violations;
}
```

### Phase 2: Auto-Fix Implementation

```javascript
class PatternFixer {
  fixFile(filePath) {
    let content = fs.readFileSync(filePath, 'utf8');
    const originalContent = content;
    
    // Fix design violations
    content = this.fixDesignViolations(content);
    
    // Fix error handling
    content = this.fixErrorHandling(content);
    
    // Fix import order
    content = this.fixImports(content);
    
    // Fix console logs
    content = this.removeConsoleLogs(content);
    
    // Add missing loading states
    content = this.addLoadingStates(content);
    
    // Only write if changed
    if (content !== originalContent) {
      fs.writeFileSync(filePath, content);
      return true;
    }
    
    return false;
  }
  
  fixDesignViolations(content) {
    let fixed = content;
    
    for (const [wrong, right] of Object.entries(VIOLATIONS)) {
      // Fix in className attributes
      const classRegex = new RegExp(
        `(className="[^"]*)\\b${wrong}\\b([^"]*")`,
        'g'
      );
      fixed = fixed.replace(classRegex, `$1${right}$2`);
      
      // Fix in clsx/cn functions
      const cnRegex = new RegExp(
        `(c[nx]\\([^)]*['"\`])${wrong}(['"\`])`,
        'g'
      );
      fixed = fixed.replace(cnRegex, `$1${right}$2`);
    }
    
    return fixed;
  }
  
  fixErrorHandling(content) {
    // Find await without try-catch
    const lines = content.split('\n');
    const fixedLines = [];
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      
      // Check for await without try
      if (line.includes('await') && !this.isInTryCatch(lines, i)) {
        const indent = line.match(/^\s*/)[0];
        fixedLines.push(`${indent}try {`);
        fixedLines.push(`  ${line}`);
        fixedLines.push(`${indent}} catch (error) {`);
        fixedLines.push(`${indent}  console.error('Error:', error);`);
        fixedLines.push(`${indent}  throw error;`);
        fixedLines.push(`${indent}}`);
      } else {
        fixedLines.push(line);
      }
    }
    
    return fixedLines.join('\n');
  }
}
```

### Phase 3: Report Generation

```javascript
function generateReport(violations, fixes) {
  const report = [];
  
  report.push('# Pattern Enforcement Report\n');
  report.push(`📊 Summary: ${violations.length} violations found, ${fixes.length} fixed\n`);
  
  // Group by type
  const byType = groupBy(violations, 'type');
  
  // Design violations
  if (byType.design) {
    report.push('## 🎨 Design System Violations\n');
    const byPattern = groupBy(byType.design, 'original');
    
    for (const [pattern, items] of Object.entries(byPattern)) {
      report.push(`### "${pattern}" → "${items[0].fixed}" (${items.length} instances)`);
      report.push('Files:');
      items.forEach(item => {
        report.push(`- ${item.file}:${item.line}`);
      });
      report.push('');
    }
  }
  
  // Error handling
  if (byType.errorHandling) {
    report.push('## 🚨 Missing Error Handling\n');
    byType.errorHandling.forEach(item => {
      report.push(`- ${item.file}:${item.line} - Added try-catch`);
    });
  }
  
  // Learning section
  report.push('\n## 📚 Remember for Next Time:\n');
  report.push('### Typography:');
  report.push('- ✅ Use: text-size-1, text-size-2, text-size-3, text-size-4');
  report.push('- ❌ Never: text-sm, text-lg, text-xl, text-2xl');
  report.push('');
  report.push('### Font Weight:');
  report.push('- ✅ Use: font-regular, font-semibold');
  report.push('- ❌ Never: font-bold, font-medium, font-light');
  report.push('');
  report.push('### Spacing:');
  report.push('- ✅ Must be divisible by 4: p-1(4px), p-2(8px), p-3(12px), p-4(16px)');
  report.push('- ❌ Never: p-5, p-7, p-9 (not divisible by 4)');
  report.push('');
  report.push('### Touch Targets:');
  report.push('- ✅ Minimum 44px: use h-11 or h-12 for buttons');
  report.push('- ❌ Never: h-8, h-9, h-10 for interactive elements');
  
  return report.join('\n');
}
```

## Integration

### With /fw validate
```javascript
// Auto-run before validation
function enhancedValidate() {
  console.log('🔧 Enforcing patterns...');
  const result = await enforcePatterns();
  
  if (result.fixed > 0) {
    console.log(`✅ Fixed ${result.fixed} violations`);
  }
  
  // Continue with normal validation
  await originalValidate();
}
```

### As Git Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run pattern enforcement
/enforce-patterns --quiet

# Check if files were modified
if [ -n "$(git diff --name-only)" ]; then
  echo "🔧 Patterns enforced, please review changes"
  git add -A
fi
```

## Output Example

```bash
/enforce-patterns

🔍 Scanning for violations...
  Checking: src/components/Form.tsx
  Checking: src/components/Button.tsx
  Checking: src/app/page.tsx

📊 Found 23 violations

🔧 Fixing violations...
  ✓ Fixed design violations: 18
  ✓ Added error handling: 3
  ✓ Fixed imports: 2

📝 Report generated: pattern-enforcement-report.md

✅ Complete! Changes applied to 3 files

💡 Run 'git diff' to review changes
```

## Features

- **Auto-Fix** - Corrects violations automatically
- **Safe** - Preserves functionality
- **Educational** - Explains why and how
- **Fast** - <5 seconds for most projects
- **Integrated** - Works with existing workflow

This ensures consistent, high-quality code from AI agents!
