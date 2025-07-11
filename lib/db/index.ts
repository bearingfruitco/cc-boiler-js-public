import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';
import * as schema from './schema';

// Database URL validation
const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) {
  throw new Error('DATABASE_URL environment variable is not set');
}

// Create postgres clients
// For migrations - single connection
export const migrationClient = postgres(databaseUrl, { 
  max: 1,
  onnotice: () => {}, // Suppress notices during migrations
});

// For queries - connection pool
const queryClient = postgres(databaseUrl, {
  // Connection pool configuration
  max: 10, // Maximum number of connections
  idle_timeout: 20, // Close idle connections after 20 seconds
  connect_timeout: 10, // Connection timeout in seconds
  
  // SSL configuration for production
  ssl: process.env.NODE_ENV === 'production' ? 'require' : false,
  
  // Transform options
  transform: {
    undefined: null, // Transform undefined to null
  },
});

// Create Drizzle instance
export const db = drizzle(queryClient, { 
  schema,
  logger: process.env.NODE_ENV === 'development', // Enable logging in dev
});

// Export the schema for use in other files
export * from './schema';

// Type exports
export type Database = typeof db;
