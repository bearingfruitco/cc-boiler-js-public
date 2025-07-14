// Global type declarations for window object

interface Window {
  // Analytics
  rudderanalytics?: any;
  analytics?: any;
  gtag?: (...args: any[]) => void;
  fbq?: (...args: any[]) => void;
  dataLayer?: any[];
  
  // Event queue (from our async system)
  __eventQueue?: {
    getStats: () => any;
    eventNames: () => string[];
    listenerCount: (event: string) => number;
    _queue?: any[];
  };
  
  // File system (for Claude Code)
  fs?: {
    readFile: (path: string, options?: { encoding?: string }) => Promise<any>;
  };
  
  // Claude completion
  claude?: {
    complete: (prompt: string) => Promise<string>;
  };
}

// Extend NodeJS ProcessEnv
declare namespace NodeJS {
  interface ProcessEnv {
    NODE_ENV: 'development' | 'production' | 'test';
    NEXT_PUBLIC_SUPABASE_URL: string;
    NEXT_PUBLIC_SUPABASE_ANON_KEY: string;
    SUPABASE_SERVICE_ROLE_KEY?: string;
    DATABASE_URL?: string;
    ENCRYPTION_KEY?: string;
    NEXT_PUBLIC_RUDDERSTACK_KEY?: string;
    NEXT_PUBLIC_RUDDERSTACK_URL?: string;
    NEXT_PUBLIC_GA_ID?: string;
    NEXT_PUBLIC_APP_VERSION?: string;
    SENTRY_DSN?: string;
    SENTRY_ORG?: string;
    SENTRY_PROJECT?: string;
  }
}

// Global test helpers
declare global {
  var testHelpers: {
    mockFetch: jest.Mock;
    resetMocks: () => void;
  };
  
  // Vitest matchers
  namespace Vi {
    interface Matchers<R> {
      toBeWithinRange(floor: number, ceiling: number): R;
    }
  }
}

export {};
