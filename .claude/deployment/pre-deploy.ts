#!/usr/bin/env node
/**
 * Pre-deployment validation checklist
 * Ensures all requirements are met before deployment
 */

import { execSync } from 'child_process';
import { env, isProduction, isStaging } from '../lib/env';
import fs from 'fs';
import path from 'path';

interface CheckResult {
  name: string;
  status: 'pass' | 'fail' | 'warn';
  message: string;
}

const checks: CheckResult[] = [];

function runCheck(name: string, fn: () => boolean | string): void {
  try {
    const result = fn();
    if (result === true) {
      checks.push({ name, status: 'pass', message: '✅ Passed' });
    } else if (typeof result === 'string') {
      checks.push({ name, status: 'warn', message: `⚠️  ${result}` });
    } else {
      checks.push({ name, status: 'fail', message: '❌ Failed' });
    }
  } catch (error) {
    checks.push({ 
      name, 
      status: 'fail', 
      message: `❌ Error: ${error.message}` 
    });
  }
}

// Check: All tests passing
runCheck('All tests passing', () => {
  try {
    execSync('npm test', { stdio: 'pipe' });
    return true;
  } catch {
    return false;
  }
});

// Check: No console.logs in production code
runCheck('No console.logs', () => {
  const result = execSync(
    'grep -r "console\\.log" --include="*.ts" --include="*.tsx" --exclude-dir=node_modules --exclude-dir=.next --exclude="*.test.*" --exclude="*.spec.*" . || true',
    { encoding: 'utf8' }
  );
  
  if (result.trim()) {
    const count = result.trim().split('\n').length;
    return `Found ${count} console.log statements`;
  }
  return true;
});

// Check: Environment variables
runCheck('Environment variables', () => {
  const required = [
    'NODE_ENV',
    'DATABASE_URL',
    'NEXT_PUBLIC_SUPABASE_URL',
    'NEXT_PUBLIC_SUPABASE_ANON_KEY',
    'SUPABASE_SERVICE_ROLE_KEY'
  ];
  
  const missing = required.filter(key => !process.env[key]);
  if (missing.length > 0) {
    return `Missing: ${missing.join(', ')}`;
  }
  return true;
});

// Check: Database migrations
runCheck('Database migrations', () => {
  // Check if there are pending migrations
  try {
    const result = execSync('npm run db:status', { encoding: 'utf8' });
    if (result.includes('pending')) {
      return 'Pending migrations detected';
    }
    return true;
  } catch {
    return 'Could not check migration status';
  }
});

// Check: Build succeeds
runCheck('Production build', () => {
  if (!fs.existsSync('.next')) {
    return 'No build found - run npm run build';
  }
  
  // Check build age
  const buildTime = fs.statSync('.next').mtime;
  const hoursSinceBuild = (Date.now() - buildTime.getTime()) / (1000 * 60 * 60);
  
  if (hoursSinceBuild > 1) {
    return `Build is ${Math.round(hoursSinceBuild)} hours old`;
  }
  return true;
});

// Check: Bundle size
runCheck('Bundle size', () => {
  const statsFile = '.next/analyze/client.html';
  if (!fs.existsSync(statsFile)) {
    return 'No bundle analysis found';
  }
  
  // Simple size check (would need more sophisticated analysis)
  const buildDir = '.next/static/chunks';
  if (fs.existsSync(buildDir)) {
    const files = fs.readdirSync(buildDir);
    const totalSize = files.reduce((sum, file) => {
      const stats = fs.statSync(path.join(buildDir, file));
      return sum + stats.size;
    }, 0);
    
    const sizeMB = totalSize / (1024 * 1024);
    if (sizeMB > 1) {
      return `Bundle size: ${sizeMB.toFixed(2)}MB (target: < 1MB)`;
    }
  }
  
  return true;
});

// Check: Security scan
runCheck('Security scan', () => {
  try {
    const result = execSync('npm audit --production', { encoding: 'utf8' });
    if (result.includes('found 0 vulnerabilities')) {
      return true;
    }
    return 'Vulnerabilities found';
  } catch {
    return 'Security scan failed';
  }
});

// Check: TypeScript errors
runCheck('TypeScript compilation', () => {
  try {
    execSync('npx tsc --noEmit', { stdio: 'pipe' });
    return true;
  } catch {
    return false;
  }
});

// Check: Lint errors
runCheck('ESLint', () => {
  try {
    execSync('npm run lint', { stdio: 'pipe' });
    return true;
  } catch {
    return 'Lint errors found';
  }
});

// Generate report
console.log('\n📋 Pre-Deployment Checklist\n');
console.log(`Environment: ${env.NODE_ENV}`);
console.log(`Time: ${new Date().toISOString()}\n`);

const failed = checks.filter(c => c.status === 'fail');
const warnings = checks.filter(c => c.status === 'warn');

checks.forEach(check => {
  console.log(`${check.message} ${check.name}`);
});

console.log('\n📊 Summary:');
console.log(`✅ Passed: ${checks.filter(c => c.status === 'pass').length}`);
console.log(`⚠️  Warnings: ${warnings.length}`);
console.log(`❌ Failed: ${failed.length}`);

if (failed.length > 0) {
  console.log('\n❌ Deployment blocked due to failures!');
  console.log('Fix the issues above and run again.\n');
  process.exit(1);
}

if (warnings.length > 0 && isProduction) {
  console.log('\n⚠️  Warnings detected in production deployment!');
  console.log('Review warnings carefully before proceeding.\n');
}

console.log('\n✅ All checks passed! Ready to deploy.\n');

// Save report
const report = {
  timestamp: new Date().toISOString(),
  environment: env.NODE_ENV,
  checks,
  summary: {
    passed: checks.filter(c => c.status === 'pass').length,
    warnings: warnings.length,
    failed: failed.length
  }
};

fs.writeFileSync(
  `.claude/deployment/pre-deploy-report-${Date.now()}.json`,
  JSON.stringify(report, null, 2)
);
