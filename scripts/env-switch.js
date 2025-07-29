#!/usr/bin/env node
/**
 * Environment switcher utility
 * Helps switch between development, staging, and production environments
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const environments = ['development', 'staging', 'production'];
const currentEnv = process.env.NODE_ENV || 'development';

console.log(`\n🌍 Environment Switcher`);
console.log(`Current environment: ${currentEnv}\n`);

// Check which env files exist
console.log('Available environment files:');
environments.forEach(env => {
  const envFile = `.env.${env}`;
  const exists = fs.existsSync(envFile);
  console.log(`${exists ? '✅' : '❌'} ${envFile}`);
});

// Get target environment from args or prompt
const targetEnv = process.argv[2];

if (targetEnv && environments.includes(targetEnv)) {
  switchEnvironment(targetEnv);
} else {
  console.log('\nSelect environment:');
  environments.forEach((env, i) => {
    console.log(`${i + 1}. ${env}`);
  });
  
  rl.question('\nChoice (1-3): ', (answer) => {
    const choice = parseInt(answer);
    if (choice >= 1 && choice <= 3) {
      switchEnvironment(environments[choice - 1]);
    } else {
      console.log('❌ Invalid choice');
      process.exit(1);
    }
    rl.close();
  });
}

function switchEnvironment(env) {
  console.log(`\n🔄 Switching to ${env}...`);
  
  const envFile = `.env.${env}`;
  if (!fs.existsSync(envFile)) {
    console.log(`❌ ${envFile} not found! Run 'npm run setup:env' first.`);
    process.exit(1);
  }
  
  // Production safety check
  if (env === 'production') {
    console.log('\n⚠️  WARNING: Switching to PRODUCTION environment!');
    console.log('This will use production database and services.\n');
    
    rl.question('Type "production" to confirm: ', (answer) => {
      if (answer === 'production') {
        performSwitch(env, envFile);
      } else {
        console.log('❌ Cancelled');
        process.exit(0);
      }
      rl.close();
    });
  } else {
    performSwitch(env, envFile);
    rl.close();
  }
}

function performSwitch(env, envFile) {
  // Update .env.local to point to selected environment
  try {
    const content = fs.readFileSync(envFile, 'utf8');
    fs.writeFileSync('.env.local', content);
    
    console.log(`\n✅ Switched to ${env} environment!`);
    console.log('\n📝 Next steps:');
    console.log('1. Restart your development server');
    console.log('2. Run "npm run env:validate" to verify');
    
    if (env === 'production') {
      console.log('\n🔒 Production checklist:');
      console.log('- [ ] All tests passing');
      console.log('- [ ] Security scan complete');
      console.log('- [ ] Database backup created');
      console.log('- [ ] Team notified');
    }
  } catch (error) {
    console.error('❌ Error switching environment:', error.message);
    process.exit(1);
  }
}
