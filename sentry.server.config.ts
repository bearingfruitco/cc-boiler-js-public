import * as Sentry from '@sentry/nextjs';

const SENTRY_DSN = process.env.SENTRY_DSN || process.env.NEXT_PUBLIC_SENTRY_DSN;

if (SENTRY_DSN) {
  Sentry.init({
    dsn: SENTRY_DSN,
    
    // Performance Monitoring
    tracesSampleRate: process.env.NODE_ENV === 'production' ? 0.1 : 1.0,
    
    // Release tracking
    release: process.env.NEXT_PUBLIC_APP_VERSION,
    
    // Environment
    environment: process.env.NODE_ENV,
    
    // Server-specific settings
    
    // Filtering
    beforeSend(event, hint) {
      // Filter out non-error events in development
      if (process.env.NODE_ENV === 'development' && event.level !== 'error') {
        return null;
      }
      
      // Don't send events for specific errors
      const error = hint.originalException;
      if (error && error instanceof Error) {
        // Skip expected errors
        if (error.message?.includes('NEXT_NOT_FOUND')) {
          return null;
        }
      }
      
      return event;
    },
  });
}
