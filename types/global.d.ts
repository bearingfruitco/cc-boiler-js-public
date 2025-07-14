// Global type definitions

import { AsyncEventQueue } from '@/lib/events/event-queue';

declare global {
  interface Window {
    // Analytics
    rudderanalytics?: any;
    gtag?: (command: string, ...args: any[]) => void;
    
    // Event system
    eventQueue?: AsyncEventQueue;
    
    // Debug helpers
    debugStores?: () => void;
    resetAllStores?: () => void;
    
    // File system (for analysis tool)
    fs?: {
      readFile: (path: string, options?: { encoding?: string }) => Promise<Uint8Array | string>;
    };
    
    // Claude completions (for artifacts)
    claude?: {
      complete: (prompt: string) => Promise<string>;
    };
  }

  namespace NodeJS {
    interface ProcessEnv {
      // Database
      DATABASE_URL: string;
      DATABASE_DIRECT_URL?: string;
      
      // Supabase
      NEXT_PUBLIC_SUPABASE_URL: string;
      NEXT_PUBLIC_SUPABASE_ANON_KEY: string;
      SUPABASE_SERVICE_ROLE_KEY: string;
      
      // Analytics
      NEXT_PUBLIC_RUDDERSTACK_KEY?: string;
      NEXT_PUBLIC_RUDDERSTACK_DATA_PLANE_URL?: string;
      NEXT_PUBLIC_VERCEL_ANALYTICS_ID?: string;
      
      // Sentry
      NEXT_PUBLIC_SENTRY_DSN?: string;
      SENTRY_DSN?: string;
      SENTRY_AUTH_TOKEN?: string;
      SENTRY_ORG?: string;
      SENTRY_PROJECT?: string;
      
      // App
      NODE_ENV: 'development' | 'production' | 'test';
      NEXT_PUBLIC_APP_URL: string;
      NEXT_PUBLIC_APP_VERSION?: string;
      
      // Feature flags
      NEXT_PUBLIC_ENABLE_ANALYTICS?: string;
      NEXT_PUBLIC_ENABLE_SENTRY?: string;
    }
  }
}

export {};
