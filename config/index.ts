import { env, isDevelopment, isStaging, isProduction } from '@/lib/env';

/**
 * Centralized configuration for the application
 * All configuration should be accessed through this module
 */

export const config = {
  app: {
    name: env.NEXT_PUBLIC_APP_NAME,
    url: env.NEXT_PUBLIC_APP_URL,
    env: env.NODE_ENV,
  },
  
  api: {
    url: env.NEXT_PUBLIC_API_URL,
    timeout: env.API_TIMEOUT,
  },
  
  database: {
    url: env.DATABASE_URL,
    logging: env.ENABLE_SQL_LOGS,
  },
  
  supabase: {
    url: env.NEXT_PUBLIC_SUPABASE_URL,
    anonKey: env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
    serviceRoleKey: env.SUPABASE_SERVICE_ROLE_KEY,
  },
  
  auth: {
    url: env.NEXTAUTH_URL,
    secret: env.NEXTAUTH_SECRET,
  },
  
  features: {
    newCheckout: env.ENABLE_NEW_CHECKOUT,
    aiAssistant: env.ENABLE_AI_ASSISTANT,
    analytics: env.ENABLE_ANALYTICS,
  },
  
  logging: {
    debug: env.ENABLE_DEBUG_LOGS,
    sql: env.ENABLE_SQL_LOGS,
    performance: env.ENABLE_PERFORMANCE_LOGS,
  },
  
  // Environment-specific configurations
  ...(isDevelopment && {
    dev: {
      hotReload: true,
      sourceMaps: true,
      verboseErrors: true,
    },
  }),
  
  ...(isStaging && {
    staging: {
      enablePreviews: true,
      collectMetrics: true,
    },
  }),
  
  ...(isProduction && {
    production: {
      enableCaching: true,
      minifyAssets: true,
      securityHeaders: true,
    },
  }),
} as const;

// Performance budgets by environment
export const performanceBudgets = {
  development: {
    bundleSize: Infinity, // No limit in dev
    pageLoad: 5000, // 5s
    apiResponse: 3000, // 3s
  },
  staging: {
    bundleSize: 1000 * 1024, // 1MB
    pageLoad: 3000, // 3s
    apiResponse: 1000, // 1s
  },
  production: {
    bundleSize: 500 * 1024, // 500KB
    pageLoad: 2000, // 2s
    apiResponse: 500, // 500ms
  },
}[env.NODE_ENV];

// Security settings by environment
export const securitySettings = {
  development: {
    enforceHTTPS: false,
    csrfProtection: true,
    rateLimiting: false,
  },
  staging: {
    enforceHTTPS: true,
    csrfProtection: true,
    rateLimiting: true,
  },
  production: {
    enforceHTTPS: true,
    csrfProtection: true,
    rateLimiting: true,
    ddosProtection: true,
  },
}[env.NODE_ENV];

// Helper to check if a feature is enabled
export function isFeatureEnabled(feature: keyof typeof config.features): boolean {
  return config.features[feature] ?? false;
}

// Helper to get environment-specific values
export function getEnvValue<T>(values: {
  development: T;
  staging: T;
  production: T;
}): T {
  return values[env.NODE_ENV as keyof typeof values];
}

export default config;
