---
name: prp-gameplan-execute
description: Execute the PRP gameplan by creating PRPs one by one with full context
aliases: [execute-prps, create-prps-from-plan]
---

# Execute PRP Gameplan

Create PRPs one by one based on the gameplan from `/analyze-for-prps`.

## Usage

```bash
/prp-gameplan-execute          # Create all PRPs from gameplan
/prp-gameplan-execute P0       # Create only P0 priority
/prp-gameplan-execute debt-form-refactor  # Create specific PRP
```

## Process

### Phase 1: Load or Create Gameplan

First, check if we have a gameplan or need to analyze:

```bash
# Check if gameplan exists
if [ -f ".agent-os/prp-gameplan.json" ]; then
  echo "📋 Loading existing gameplan..."
  cat .agent-os/prp-gameplan.json
else
  echo "No gameplan found. Analyzing project..."
  # Run analysis to determine what PRPs are needed
fi
```

If no gameplan exists, I'll analyze:
- `.agent-os/` directory contents (check each file, not directory)
- `docs/architecture/` markdown files
- Large components in `src/`
- Test coverage
- Integration status

### Phase 2: Create PRPs Sequentially

For each PRP needed, I'll create it one by one:

```javascript
// IMPORTANT: File operation safety
function safeReadFile(path) {
  // Check if path exists and is a file (not directory)
  if (!fs.existsSync(path)) {
    return null;
  }
  
  const stats = fs.statSync(path);
  if (stats.isDirectory()) {
    // If it's a directory, list its contents instead
    return fs.readdirSync(path);
  }
  
  // Only read if it's actually a file
  if (stats.isFile()) {
    return fs.readFileSync(path, 'utf8');
  }
  
  return null;
}

// SAFE: Check file type before operations
function gatherContextFiles(prpName) {
  const contexts = [];
  
  // Define search patterns
  const patterns = {
    'debt-form-refactor': [
      'src/**/DebtForm.tsx',  // Specific file
      'src/**/debt/*.tsx'     // Files in directory
    ],
    'test-infrastructure': [
      'jest.config.*',
      'vitest.config.*',
      '**/*.test.ts'
    ],
    'supabase-integration': [
      'src/lib/supabase/client.ts',
      'supabase/migrations/*.sql',
      '.env.example'
    ]
  };
  
  // Safely find and read files
  for (const pattern of patterns[prpName] || []) {
    const files = glob.sync(pattern);
    for (const file of files) {
      // Check if it's a file before reading
      if (fs.statSync(file).isFile()) {
        contexts.push({
          path: file,
          exists: true,
          size: fs.statSync(file).size
        });
      }
    }
  }
  
  return contexts;
}
```

### Phase 3: Safe PRP Creation

Create each PRP with proper file handling:

```javascript
async function createPRPSafely(prpSpec) {
  console.log(`\n🔨 Creating PRP: ${prpSpec.name}`);
  
  // Step 1: Safely gather context
  const contextFiles = [];
  
  // Check specific files (not directories)
  const filesToCheck = {
    'debt-form-refactor': [
      'src/app/[domain]/optin/[funnel]/components/debt/DebtForm.tsx'
    ],
    'test-infrastructure': [
      'package.json',
      'tsconfig.json'
    ],
    'supabase-integration': [
      '.env.example',
      'src/lib/supabase/client.ts'
    ],
    'rudderstack-bigquery': [
      'src/lib/analytics/rudderstack.ts',
      'docs/RUDDERSTACK_BIGQUERY_CONFIG.md'
    ]
  };
  
  // Check each file safely
  for (const file of filesToCheck[prpSpec.name] || []) {
    try {
      const stats = fs.statSync(file);
      if (stats.isFile()) {
        contextFiles.push({
          path: file,
          size: stats.size,
          exists: true
        });
      }
    } catch (e) {
      // File doesn't exist
      contextFiles.push({
        path: file,
        exists: false
      });
    }
  }
  
  // Step 2: Create PRP directory if needed
  const prpDir = 'PRPs/active';
  if (!fs.existsSync(prpDir)) {
    fs.mkdirSync(prpDir, { recursive: true });
  }
  
  // Step 3: Generate PRP content
  const prpContent = generatePRPContent(prpSpec, contextFiles);
  
  // Step 4: Write PRP file (ensure we're writing to a file, not directory)
  const prpPath = `${prpDir}/${prpSpec.name}-prp.md`;
  
  // Make sure we're not trying to write to a directory
  if (fs.existsSync(prpPath) && fs.statSync(prpPath).isDirectory()) {
    console.error(`Error: ${prpPath} is a directory, not a file!`);
    return false;
  }
  
  // Write the file
  fs.writeFileSync(prpPath, prpContent);
  console.log(`✅ Created: ${prpPath}`);
  
  return true;
}
```

### Phase 4: Directory-Safe Analysis

When analyzing the project:

```javascript
function analyzeProjectSafely() {
  const analysis = {
    largeComponents: [],
    testCoverage: 0,
    integrations: {},
    architectureIssues: []
  };
  
  // Find large TypeScript/TSX files (not directories)
  const files = glob.sync('src/**/*.{ts,tsx}');
  
  for (const file of files) {
    try {
      const stats = fs.statSync(file);
      // Only process files, not directories
      if (stats.isFile()) {
        const content = fs.readFileSync(file, 'utf8');
        const lines = content.split('\n').length;
        
        if (lines > 1000) {
          analysis.largeComponents.push({
            file: file,
            lines: lines
          });
        }
      }
    } catch (e) {
      // Skip files we can't read
      continue;
    }
  }
  
  // Check test files (count only actual files)
  const testFiles = glob.sync('**/*.{test,spec}.{ts,tsx,js,jsx}');
  const actualTestFiles = testFiles.filter(f => {
    try {
      return fs.statSync(f).isFile();
    } catch {
      return false;
    }
  });
  
  analysis.testCoverage = actualTestFiles.length;
  
  return analysis;
}
```

### Phase 5: Example Gameplan Structure

The gameplan will be structured like:

```json
{
  "timestamp": "2024-02-07T10:00:00Z",
  "project": "debt-funnel",
  "prps": [
    {
      "name": "debt-form-refactor",
      "priority": "P0",
      "reason": "Component is 3,053 lines",
      "effort": "5-7 days",
      "contextFiles": [
        "src/app/[domain]/optin/[funnel]/components/debt/DebtForm.tsx"
      ]
    },
    {
      "name": "test-infrastructure",
      "priority": "P0",
      "reason": "0% test coverage",
      "effort": "3-4 days",
      "contextFiles": [
        "package.json",
        "vitest.config.ts"
      ]
    }
  ]
}
```

## Error Prevention

The command now:
1. **Checks file vs directory** before any read operation
2. **Uses `fs.statSync().isFile()`** to verify
3. **Handles missing files** gracefully
4. **Creates directories** with `recursive: true`
5. **Lists directory contents** instead of trying to read them

## Example Execution

```bash
/prp-gameplan-execute

📋 Analyzing project for PRPs...
✓ Found large component: DebtForm.tsx (3,053 lines)
✓ Test coverage: 0 test files found
✓ Supabase configured but not implemented

Creating PRPs sequentially...

🔨 Creating PRP 1/4: debt-form-refactor
   ✓ Found context file: DebtForm.tsx (3,053 lines)
   ✓ Writing to: PRPs/active/debt-form-refactor-prp.md
✅ Created successfully

🔨 Creating PRP 2/4: test-infrastructure
   ✓ Found context file: package.json
   ✗ vitest.config.ts not found (will create)
   ✓ Writing to: PRPs/active/test-infrastructure-prp.md
✅ Created successfully

[continues...]

✅ All PRPs created without errors!
```

This version handles directories and files correctly!
