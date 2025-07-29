import { z } from 'zod';

/**
 * Environment configuration with runtime validation
 * This ensures all required environment variables are present and correctly typed
 */

// Define the schema for our environment variables
const envSchema = z.object({
  // Application
  NODE_ENV: z.enum(['development', 'staging', 'production', 'test']),
  NEXT_PUBLIC_APP_NAME: z.string().min(1),
  NEXT_PUBLIC_APP_URL: z.string().url(),

  // Database
  DATABASE_URL: z.string().min(1),

  // Supabase
  NEXT_PUBLIC_SUPABASE_URL: z.string().url(),
  NEXT_PUBLIC_SUPABASE_ANON_KEY: z.string().min(1),
  SUPABASE_SERVICE_ROLE_KEY: z.string().min(1),

  // API Configuration
  NEXT_PUBLIC_API_URL: z.string().url(),
  API_TIMEOUT: z.string().transform(Number).default('30000'),

  // Feature Flags
  ENABLE_NEW_CHECKOUT: z.string().transform(val => val === 'true').default('false'),
  ENABLE_AI_ASSISTANT: z.string().transform(val => val === 'true').default('false'),
  ENABLE_ANALYTICS: z.string().transform(val => val === 'true').default('false'),

  // Security
  NEXTAUTH_SECRET: z.string().min(32).optional(),
  NEXTAUTH_URL: z.string().url().optional(),

  // External Services (Optional)
  STRIPE_SECRET_KEY: z.string().optional(),
  STRIPE_WEBHOOK_SECRET: z.string().optional(),
  SENDGRID_API_KEY: z.string().optional(),
  SENTRY_DSN: z.string().url().optional(),

  // Analytics (Optional)
  NEXT_PUBLIC_RUDDERSTACK_KEY: z.string().optional(),
  NEXT_PUBLIC_RUDDERSTACK_URL: z.string().url().optional(),
  NEXT_PUBLIC_GA_MEASUREMENT_ID: z.string().optional(),

  // Development Tools
  ENABLE_DEBUG_LOGS: z.string().transform(val => val === 'true').default('false'),
  ENABLE_SQL_LOGS: z.string().transform(val => val === 'true').default('false'),
  ENABLE_PERFORMANCE_LOGS: z.string().transform(val => val === 'true').default('false'),

  // Deployment
  VERCEL_URL: z.string().optional(),
  VERCEL_ENV: z.enum(['development', 'preview', 'production']).optional(),
});

// Parse and validate environment variables
const parseEnv = () => {
  try {
    return envSchema.parse(process.env);
  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error('❌ Invalid environment variables:');
      error.issues.forEach(issue => {
        console.error(`  ${issue.path.join('.')}: ${issue.message}`);
      });
      
      // In development, provide helpful error messages
      if (process.env.NODE_ENV === 'development') {
        console.error('\n💡 Tip: Check your .env.development file');
        console.error('   Copy .env.example and fill in the values\n');
      }
      
      throw new Error('Invalid environment configuration');
    }
    throw error;
  }
};

// Export validated environment
export const env = parseEnv();

// Type-safe environment helpers
export const isDevelopment = env.NODE_ENV === 'development';
export const isStaging = env.NODE_ENV === 'staging';
export const isProduction = env.NODE_ENV === 'production';
export const isTest = env.NODE_ENV === 'test';

// Feature flags helper
export const features = {
  newCheckout: env.ENABLE_NEW_CHECKOUT,
  aiAssistant: env.ENABLE_AI_ASSISTANT,
  analytics: env.ENABLE_ANALYTICS,
} as const;

// Logging helpers
export const logging = {
  debug: env.ENABLE_DEBUG_LOGS,
  sql: env.ENABLE_SQL_LOGS,
  performance: env.ENABLE_PERFORMANCE_LOGS,
} as const;

// Export the type for use in other files
export type Env = z.infer<typeof envSchema>;
