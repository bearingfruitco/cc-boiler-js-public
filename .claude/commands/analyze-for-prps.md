---
name: analyze-for-prps
description: Analyze project and create a PRP gameplan without creating PRPs yet
aliases: [prp-analysis, prp-plan, analyze-prps]
---

# Analyze for PRPs - Create the Gameplan

Analyze the entire project to determine what PRPs are needed, without creating them yet.

## Usage

```bash
/analyze-for-prps
/prp-plan  # alias
```

## Process

### Phase 1: Safe Directory Analysis

```bash
echo "=== 📊 Analyzing Project for PRP Planning ==="

# SAFE: Check .agent-os directory contents (not reading directory as file)
echo "📚 Checking .agent-os/ analysis..."
if [ -d ".agent-os" ]; then
  # List files in directory, don't try to read the directory itself
  ls -la .agent-os/*.md 2>/dev/null | head -5
  
  # Read specific files if they exist
  [ -f ".agent-os/ANALYSIS_SUMMARY.md" ] && head -20 .agent-os/ANALYSIS_SUMMARY.md
  [ -f ".agent-os/product/roadmap.md" ] && grep "Phase 1" .agent-os/product/roadmap.md
fi

# SAFE: Check architecture directory
echo "🏗️ Checking architecture findings..."
if [ -d "docs/architecture" ]; then
  # List markdown files in directory
  ls -la docs/architecture/*.md 2>/dev/null
  
  # Read from specific files, not directory
  for file in docs/architecture/*.md; do
    [ -f "$file" ] && grep -h "debt\|missing\|needed" "$file" | head -2
  done
fi

# SAFE: Find large files (not directories)
echo "📏 Finding oversized components..."
find src -type f \( -name "*.tsx" -o -name "*.ts" \) -exec wc -l {} \; | sort -rn | head -5

# SAFE: Count test files
echo "🧪 Checking test coverage..."
find . -type f \( -name "*.test.*" -o -name "*.spec.*" \) | wc -l
```

### Phase 2: Safe File Discovery

```javascript
function discoverFilesSafely(pattern) {
  const fs = require('fs');
  const glob = require('glob');
  
  // Get matching paths
  const paths = glob.sync(pattern);
  
  // Filter to only files (not directories)
  const files = paths.filter(path => {
    try {
      const stats = fs.statSync(path);
      return stats.isFile();
    } catch (e) {
      return false;
    }
  });
  
  return files;
}

function analyzeComponentSizes() {
  const components = {};
  
  // Find all TypeScript/TSX files
  const files = discoverFilesSafely('src/**/*.{ts,tsx}');
  
  for (const file of files) {
    try {
      // Read the file content
      const content = fs.readFileSync(file, 'utf8');
      const lines = content.split('\n').length;
      
      if (lines > 1000) {
        components[file] = {
          lines: lines,
          needsRefactor: true,
          priority: lines > 2000 ? 'P0' : 'P1'
        };
      }
    } catch (e) {
      console.log(`Skipping ${file}: ${e.message}`);
    }
  }
  
  return components;
}
```

### Phase 3: Integration Status Check

```javascript
function checkIntegrationsSafely() {
  const integrations = {
    supabase: { configured: false, implemented: false },
    rudderstack: { configured: false, implemented: false },
    sentry: { configured: false, implemented: false },
    bigquery: { configured: false, implemented: false }
  };
  
  // Check .env.example for configuration
  if (fs.existsSync('.env.example') && fs.statSync('.env.example').isFile()) {
    const envContent = fs.readFileSync('.env.example', 'utf8');
    
    integrations.supabase.configured = envContent.includes('SUPABASE_URL');
    integrations.rudderstack.configured = envContent.includes('RUDDERSTACK');
    integrations.sentry.configured = envContent.includes('SENTRY_DSN');
    integrations.bigquery.configured = envContent.includes('BIGQUERY');
  }
  
  // Check for actual implementations (files, not directories)
  integrations.supabase.implemented = fs.existsSync('src/lib/supabase/client.ts') && 
                                     fs.statSync('src/lib/supabase/client.ts').isFile();
  
  integrations.rudderstack.implemented = fs.existsSync('src/lib/analytics/rudderstack.ts') && 
                                         fs.statSync('src/lib/analytics/rudderstack.ts').isFile();
  
  integrations.sentry.implemented = fs.existsSync('sentry.client.config.ts') && 
                                    fs.statSync('sentry.client.config.ts').isFile();
  
  return integrations;
}
```

### Phase 4: Generate Gameplan

Create a gameplan JSON that avoids directory read errors:

```javascript
function generateGameplan(analysis) {
  const gameplan = {
    timestamp: new Date().toISOString(),
    project: process.cwd().split('/').pop(),
    prps: [],
    contextFiles: {},
    summary: {
      total: 0,
      p0: 0,
      p1: 0,
      p2: 0
    }
  };
  
  // Add PRPs based on analysis
  if (analysis.largeComponents.length > 0) {
    for (const component of analysis.largeComponents) {
      gameplan.prps.push({
        name: `${component.name}-refactor`,
        priority: 'P0',
        reason: `Component is ${component.lines} lines`,
        effort: '5-7 days',
        contextFiles: [component.path],
        type: 'refactoring'
      });
      gameplan.summary.p0++;
    }
  }
  
  if (analysis.testCoverage === 0) {
    gameplan.prps.push({
      name: 'test-infrastructure',
      priority: 'P0',
      reason: 'No test coverage',
      effort: '3-4 days',
      contextFiles: ['package.json', 'tsconfig.json'],
      type: 'infrastructure'
    });
    gameplan.summary.p0++;
  }
  
  // Add integration PRPs
  for (const [service, status] of Object.entries(analysis.integrations)) {
    if (status.configured && !status.implemented) {
      gameplan.prps.push({
        name: `${service}-integration`,
        priority: 'P1',
        reason: `${service} configured but not implemented`,
        effort: '2-5 days',
        contextFiles: ['.env.example'],
        type: 'integration'
      });
      gameplan.summary.p1++;
    }
  }
  
  gameplan.summary.total = gameplan.prps.length;
  
  // Save gameplan
  const gameplanDir = '.agent-os';
  if (!fs.existsSync(gameplanDir)) {
    fs.mkdirSync(gameplanDir, { recursive: true });
  }
  
  const gameplanPath = `${gameplanDir}/prp-gameplan.json`;
  fs.writeFileSync(gameplanPath, JSON.stringify(gameplan, null, 2));
  
  return gameplan;
}
```

## Output Example

```
🎯 PRP Gameplan Analysis Complete

Found 6 PRPs needed across 4 categories:

📊 Summary:
- P0 (Critical): 2 PRPs
  ✗ debt-form-refactor: 3,053 lines (exceeds 1000 limit)
  ✗ test-infrastructure: 0% coverage

- P1 (Important): 3 PRPs
  ⚠️ supabase-integration: configured but not implemented
  ⚠️ rudderstack-bigquery: missing warehouse destination
  ⚠️ performance-optimization: needs improvements

- P2 (Enhancement): 1 PRP
  ○ sentry-enhancement: basic implementation exists

📁 Context Files Found:
- src/app/.../DebtForm.tsx (file, 3,053 lines)
- src/lib/analytics/rudderstack.ts (file, exists)
- .env.example (file, has configs)
- package.json (file, has test deps)

📋 Gameplan saved to: .agent-os/prp-gameplan.json

Next: Run /prp-gameplan-execute to create PRPs
```

## Error Prevention

This version:
1. **Never reads directories as files**
2. **Checks `isFile()` before reading**
3. **Uses `find -type f`** to only get files
4. **Lists directory contents** instead of reading them
5. **Handles missing files** gracefully

The EISDIR error should be completely eliminated!
