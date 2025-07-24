#!/usr/bin/env node

/**
 * Run tests only for staged files
 * Speeds up pre-commit by testing only what changed
 */

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// Get staged TypeScript/JavaScript files
const stagedFiles = execSync('git diff --cached --name-only --diff-filter=ACM')
  .toString()
  .trim()
  .split('\n')
  .filter(file => file.match(/\.(tsx?|jsx?)$/) && !file.includes('.test.') && !file.includes('.spec.'));

if (stagedFiles.length === 0) {
  console.log('No staged code files to test');
  process.exit(0);
}

// Find corresponding test files
const testFiles = new Set();

stagedFiles.forEach(file => {
  const basename = path.basename(file, path.extname(file));
  const dirname = path.dirname(file);
  
  // Possible test file patterns
  const patterns = [
    `${dirname}/${basename}.test.tsx`,
    `${dirname}/${basename}.test.ts`,
    `${dirname}/${basename}.spec.tsx`,
    `${dirname}/${basename}.spec.ts`,
    `${dirname}/__tests__/${basename}.tsx`,
    `${dirname}/__tests__/${basename}.ts`,
  ];
  
  patterns.forEach(pattern => {
    if (fs.existsSync(pattern)) {
      testFiles.add(pattern);
    }
  });
});

if (testFiles.size === 0) {
  console.log('⚠️  No tests found for staged files');
  console.log('💡 Consider adding tests (TDD approach)');
  process.exit(0); // Don't block if no tests exist
}

console.log(`Running ${testFiles.size} test file(s)...`);

// Run tests
try {
  const testFileArray = Array.from(testFiles);
  execSync(`npm test -- ${testFileArray.join(' ')} --run`, { 
    stdio: 'inherit',
    timeout: 30000 // 30 second timeout
  });
  console.log('✅ All tests passed!');
} catch (error) {
  console.error('❌ Tests failed');
  process.exit(1);
}
