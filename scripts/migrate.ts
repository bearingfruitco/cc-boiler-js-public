#!/usr/bin/env node
/**
 * Safe database migration script with environment checks
 * Prevents accidental production migrations without confirmation
 */

import { execSync } from 'child_process';
import readline from 'readline';
import { env, isProduction } from '../lib/env';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

async function confirm(question: string): Promise<boolean> {
  return new Promise((resolve) => {
    rl.question(`${question} (yes/no): `, (answer) => {
      resolve(answer.toLowerCase() === 'yes');
    });
  });
}

async function backupDatabase() {
  console.log('📦 Creating database backup...');
  const timestamp = new Date().toISOString().replace(/:/g, '-');
  const backupFile = `backup-${env.NODE_ENV}-${timestamp}.sql`;
  
  try {
    execSync(`pg_dump ${env.DATABASE_URL} > ./backups/${backupFile}`);
    console.log(`✅ Backup created: ${backupFile}`);
    return backupFile;
  } catch (error) {
    console.error('❌ Backup failed:', error);
    return null;
  }
}

async function runMigration() {
  console.log(`🚀 Running migrations in ${env.NODE_ENV} environment...`);
  
  // Production safety checks
  if (isProduction) {
    console.log('\n⚠️  PRODUCTION MIGRATION WARNING!\n');
    console.log('You are about to run migrations in PRODUCTION.');
    console.log('This could potentially affect live users.\n');
    
    const checklistComplete = await confirm(
      'Have you completed the pre-migration checklist?\n' +
      '  ✓ Tested in staging\n' +
      '  ✓ Reviewed migration SQL\n' +
      '  ✓ Scheduled maintenance window\n' +
      '  ✓ Notified team\n' +
      'Confirm checklist complete'
    );
    
    if (!checklistComplete) {
      console.log('❌ Migration cancelled. Complete checklist first.');
      process.exit(1);
    }
    
    const backupConfirm = await confirm('Create backup before migration?');
    if (backupConfirm) {
      const backupFile = await backupDatabase();
      if (!backupFile) {
        const proceedWithoutBackup = await confirm('Backup failed. Proceed anyway?');
        if (!proceedWithoutBackup) {
          console.log('❌ Migration cancelled.');
          process.exit(1);
        }
      }
    }
    
    const finalConfirm = await confirm(
      `FINAL CONFIRMATION: Run migrations on ${env.DATABASE_URL}?`
    );
    
    if (!finalConfirm) {
      console.log('❌ Migration cancelled.');
      process.exit(1);
    }
  }
  
  try {
    // Run the actual migration
    console.log('\n🔄 Running migrations...');
    execSync('npm run db:migrate', { stdio: 'inherit' });
    console.log('\n✅ Migrations completed successfully!');
    
    // Log migration in production
    if (isProduction) {
      const logEntry = {
        timestamp: new Date().toISOString(),
        environment: env.NODE_ENV,
        user: process.env.USER,
        status: 'success'
      };
      
      execSync(
        `echo '${JSON.stringify(logEntry)}' >> .claude/logs/migrations.log`
      );
    }
  } catch (error) {
    console.error('\n❌ Migration failed:', error);
    
    if (isProduction) {
      console.log('\n🔄 To rollback, restore from backup:');
      console.log('  psql $DATABASE_URL < ./backups/[backup-file]');
    }
    
    process.exit(1);
  } finally {
    rl.close();
  }
}

// Run migration
runMigration().catch(console.error);
