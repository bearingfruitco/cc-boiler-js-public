#!/usr/bin/env node

/**
 * Quick design system check for staged files only
 * Complements full MCP hook validation
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Get staged files
const stagedFiles = execSync('git diff --cached --name-only --diff-filter=ACM')
  .toString()
  .trim()
  .split('\n')
  .filter(file => file.match(/\.(tsx?|jsx?)$/));

if (stagedFiles.length === 0) {
  console.log('No staged component files to check');
  process.exit(0);
}

// Design system rules (matching your config)
const violationPatterns = {
  forbiddenSizes: /\b(text-(?:xs|sm|base|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl))\b/g,
  forbiddenWeights: /\b(font-(?:thin|extralight|light|normal|medium|bold|extrabold|black))\b/g,
  invalidSpacing: /\b(?:p|m|gap|space-[xy])-(5|7|9|11|13|15|17|18|19)\b/g,
};

let hasViolations = false;

stagedFiles.forEach(file => {
  try {
    const content = fs.readFileSync(file, 'utf8');
    const violations = [];
    
    // Check font sizes
    const sizeMatches = content.match(violationPatterns.forbiddenSizes);
    if (sizeMatches) {
      violations.push(`Font sizes: ${sizeMatches.join(', ')}`);
    }
    
    // Check font weights
    const weightMatches = content.match(violationPatterns.forbiddenWeights);
    if (weightMatches) {
      violations.push(`Font weights: ${weightMatches.join(', ')}`);
    }
    
    // Check spacing
    const spacingMatches = content.match(violationPatterns.invalidSpacing);
    if (spacingMatches) {
      violations.push(`Invalid spacing: ${spacingMatches.join(', ')}`);
    }
    
    if (violations.length > 0) {
      console.error(`\n❌ ${file}:`);
      violations.forEach(v => console.error(`   ${v}`));
      hasViolations = true;
    }
  } catch (e) {
    // Skip files that can't be read
  }
});

if (hasViolations) {
  console.error('\n📚 Allowed values:');
  console.error('   Font sizes: text-size-[1-4]');
  console.error('   Font weights: font-regular, font-semibold');
  console.error('   Spacing: multiples of 4 (p-1, p-2, p-3, p-4, p-6, p-8...)');
  process.exit(1);
}

console.log('✅ Design system check passed');
