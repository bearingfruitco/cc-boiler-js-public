---
name: prp-gameplan-execute
description: Execute the PRP gameplan creating PRPs with correct validator structure
aliases: [execute-prps, create-prps-from-plan]
---

# Execute PRP Gameplan with Validator-Compliant Structure

Create PRPs one by one following the required template structure.

## Required PRP Structure (From Validator)

Every PRP MUST have these sections:
1. **🎯 Goal** - Clear objective
2. **📚 Required Context** - References and documentation
3. **🏗️ Implementation Blueprint** - How to build
4. **🧪 Validation** - Testing and verification loops

## Process

### Phase 1: Load or Create Gameplan

```javascript
// Check for gameplan or analyze
const gameplan = loadGameplan('.agent-os/prp-gameplan.json') || analyzeProject();
```

### Phase 2: Generate Validator-Compliant PRPs

For each PRP, use this structure:

```markdown
# PRP: ${prpName} - One-Pass Implementation Guide

> **PRP = PRD + Curated Codebase Intelligence + Validation Loops**
> This document provides everything needed for production-ready implementation on the first pass.

## 🎯 Goal
${goal}

## 🔑 Why This Matters
- **User Value**: ${userValue}
- **Business Value**: ${businessValue}
- **Technical Value**: ${technicalValue}

## ✅ Success Criteria (Measurable)
${successCriteria.map(c => `- [ ] ${c}`).join('\n')}

## 📚 Required Context

### Documentation & References
\`\`\`yaml
${contextFiles.map(file => `
- file: ${file.path}
  why: ${file.reason}
  pattern: ${file.pattern}
  gotcha: ${file.gotcha || 'None'}
`).join('\n')}
\`\`\`

### Known Gotchas & Critical Warnings
\`\`\`markdown
${warnings.map(w => `# ${w.level}: ${w.message}`).join('\n')}
\`\`\`

### Required Patterns From Codebase
\`\`\`typescript
${codePatterns}
\`\`\`

## 🏗️ Implementation Blueprint

### Phase 1: ${phase1.name} (${phase1.time})
\`\`\`typescript
${phase1.code}
\`\`\`

**Validation**: \`${phase1.validation}\`

### Phase 2: ${phase2.name} (${phase2.time})
\`\`\`typescript
${phase2.code}
\`\`\`

**Validation**: \`${phase2.validation}\`

## 🧪 Validation Loops

### Loop 1: Unit Testing
- [ ] All functions have tests
- [ ] Coverage > 80%
- [ ] Tests pass: \`bun test\`

### Loop 2: Integration Testing
- [ ] API endpoints tested
- [ ] Database operations verified
- [ ] Error cases handled

### Loop 3: Design Validation
- [ ] Run \`/vd\` - no violations
- [ ] Touch targets >= 44px
- [ ] Mobile responsive

### Loop 4: Production Readiness
- [ ] No console errors
- [ ] Performance metrics met
- [ ] Analytics tracking verified

## 🚫 Common Mistakes to Avoid
${mistakes.map(m => `- ${m}`).join('\n')}

## 📊 Success Metrics
- **Performance**: ${performanceTarget}
- **Quality**: ${qualityTarget}
- **Business**: ${businessTarget}
```

### Phase 3: Create PRPs with Context

```javascript
function createValidatorCompliantPRP(prpSpec) {
  const prp = {
    name: prpSpec.name,
    goal: determineGoal(prpSpec),
    context: gatherRequiredContext(prpSpec),
    implementation: generateImplementationPlan(prpSpec),
    validation: createValidationLoops(prpSpec)
  };
  
  // Ensure all required sections exist
  validatePRPStructure(prp);
  
  return formatPRPContent(prp);
}

function gatherRequiredContext(prpSpec) {
  const context = {
    files: [],
    warnings: [],
    patterns: []
  };
  
  // Find relevant files with explanations
  if (prpSpec.name === 'debt-form-refactor') {
    context.files.push({
      path: 'src/app/[domain]/optin/[funnel]/components/debt/DebtForm.tsx',
      why: 'Current monolithic component to refactor',
      pattern: 'Extract validation logic (lines 500-800)',
      gotcha: 'Preserve all tracking events'
    });
    
    context.files.push({
      path: 'src/lib/analytics/rudderstack.ts',
      why: 'Tracking patterns to preserve',
      pattern: 'eventQueue.emit() for non-blocking',
      gotcha: 'Never await analytics calls'
    });
    
    context.warnings.push({
      level: 'CRITICAL',
      message: 'This form generates revenue - test thoroughly'
    });
    
    context.warnings.push({
      level: 'CRITICAL',
      message: 'Preserve ALL rudderAnalytics.track() calls'
    });
  }
  
  if (prpSpec.name === 'test-infrastructure') {
    context.files.push({
      path: 'package.json',
      why: 'Check existing test dependencies',
      pattern: 'vitest already in devDependencies',
      gotcha: 'May need configuration only'
    });
    
    context.warnings.push({
      level: 'WARNING',
      message: 'Set up CI/CD to run tests automatically'
    });
  }
  
  if (prpSpec.name === 'supabase-integration') {
    context.files.push({
      path: '.env.example',
      why: 'Environment variables already configured',
      pattern: 'SUPABASE_URL and keys present',
      gotcha: 'Do not rename existing variables'
    });
    
    context.files.push({
      path: 'src/lib/supabase/client.ts',
      why: 'May already exist - extend, don\'t replace',
      pattern: 'createClient pattern if exists',
      gotcha: 'Check for existing implementation first'
    });
    
    context.warnings.push({
      level: 'CRITICAL',
      message: 'Enable RLS on all Supabase tables'
    });
  }
  
  return context;
}

function createValidationLoops(prpSpec) {
  const loops = [];
  
  // Common validation loops
  loops.push({
    name: 'Unit Testing',
    checks: [
      'All functions have tests',
      'Coverage > 80%',
      'Tests pass: bun test'
    ]
  });
  
  // Specific validation based on PRP type
  if (prpSpec.name.includes('refactor')) {
    loops.push({
      name: 'Regression Testing',
      checks: [
        'All existing features still work',
        'Form submission succeeds',
        'Tracking events fire correctly',
        'No performance degradation'
      ]
    });
  }
  
  if (prpSpec.name.includes('integration')) {
    loops.push({
      name: 'Integration Testing',
      checks: [
        'Connection established',
        'Authentication works',
        'Data operations succeed',
        'Error handling works'
      ]
    });
  }
  
  loops.push({
    name: 'Production Readiness',
    checks: [
      'No console errors',
      'Performance targets met',
      'Monitoring configured',
      'Documentation updated'
    ]
  });
  
  return loops;
}
```

### Phase 4: Safe File Operations

```javascript
// Ensure we're writing files, not directories
function writePRPSafely(prpPath, content) {
  const dir = path.dirname(prpPath);
  
  // Create directory if needed
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  // Ensure we're writing to a file
  if (fs.existsSync(prpPath) && fs.statSync(prpPath).isDirectory()) {
    throw new Error(`Cannot write PRP: ${prpPath} is a directory`);
  }
  
  // Write the PRP
  fs.writeFileSync(prpPath, content, 'utf8');
  
  // Verify it passes validation
  const validationResult = validatePRPStructure(content);
  if (!validationResult.valid) {
    console.warn(`⚠️ PRP may not pass validator: ${validationResult.issues}`);
  }
  
  return true;
}
```

## Example Output

When creating a PRP, it will now have the required structure:

```
🔨 Creating PRP: debt-form-refactor

✅ Section added: 🎯 Goal
✅ Section added: 📚 Required Context (5 files, 3 warnings)
✅ Section added: 🏗️ Implementation Blueprint
✅ Section added: 🧪 Validation Loops (4 loops)

✓ PRP structure validated
✓ Written to: PRPs/active/debt-form-refactor-prp.md
```

This ensures all PRPs pass the validator!
