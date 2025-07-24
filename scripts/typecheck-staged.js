#!/usr/bin/env node

/**
 * Run TypeScript check only on staged files
 * Uses project tsconfig for proper settings
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Get staged TypeScript files
const stagedFiles = execSync('git diff --cached --name-only --diff-filter=ACM')
  .toString()
  .trim()
  .split('\n')
  .filter(file => file.match(/\.(tsx?|jsx?)$/) && !file.includes('.d.ts'));

if (stagedFiles.length === 0) {
  console.log('No staged TypeScript files to check');
  process.exit(0);
}

console.log(`Checking ${stagedFiles.length} file(s)...`);

// Create a temporary tsconfig that extends the main one but only includes staged files
const tempConfig = {
  extends: './tsconfig.json',
  include: stagedFiles,
  exclude: []
};

const tempConfigPath = '.tsconfig.staged.json';

try {
  // Write temporary config
  fs.writeFileSync(tempConfigPath, JSON.stringify(tempConfig, null, 2));
  
  // Run TypeScript with the temporary config
  execSync(`npx tsc --noEmit --project ${tempConfigPath}`, { 
    stdio: 'inherit'
  });
  
  console.log('✅ TypeScript check passed');
  process.exit(0);
} catch (error) {
  console.error('❌ TypeScript errors in staged files');
  process.exit(1);
} finally {
  // Clean up temp file
  try {
    fs.unlinkSync(tempConfigPath);
  } catch (e) {
    // Ignore cleanup errors
  }
}
