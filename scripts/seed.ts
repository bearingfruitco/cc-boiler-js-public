#!/usr/bin/env node
/**
 * Database seeding script with environment protection
 * Prevents seeding production database
 */

import { execSync } from 'child_process';
import { env, isProduction, isStaging } from '../lib/env';

async function seedDatabase() {
  console.log(`🌱 Seeding database in ${env.NODE_ENV} environment...`);
  
  // Block production seeding
  if (isProduction) {
    console.error('❌ Cannot seed production database!');
    console.error('Production data should only be created through the application.');
    process.exit(1);
  }
  
  // Warn for staging
  if (isStaging) {
    console.warn('⚠️  Seeding staging database...');
    console.warn('This will reset staging data. Continue? (Ctrl+C to cancel)');
    
    // Give 5 seconds to cancel
    await new Promise(resolve => setTimeout(resolve, 5000));
  }
  
  try {
    console.log('\n🔄 Clearing existing data...');
    // Add your database clearing logic here
    
    console.log('🌱 Inserting seed data...');
    // Add your seeding logic here
    
    console.log('\n✅ Database seeded successfully!');
    
    if (isStaging) {
      console.log('\n📝 Staging database seeded with:');
      console.log('  - Test users');
      console.log('  - Sample data');
      console.log('  - Demo content');
    }
  } catch (error) {
    console.error('❌ Seeding failed:', error);
    process.exit(1);
  }
}

// Environment check
if (!env.DATABASE_URL) {
  console.error('❌ DATABASE_URL not set');
  process.exit(1);
}

// Run seeding
seedDatabase().catch(console.error);
