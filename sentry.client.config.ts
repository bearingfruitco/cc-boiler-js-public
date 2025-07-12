import * as Sentry from '@sentry/nextjs';

const SENTRY_DSN = process.env.NEXT_PUBLIC_SENTRY_DSN;

if (SENTRY_DSN) {
  Sentry.init({
    dsn: SENTRY_DSN,
    
    // Performance Monitoring
    tracesSampleRate: process.env.NODE_ENV === 'production' ? 0.1 : 1.0,
    
    // Session Replay
    replaysSessionSampleRate: 0.1, // 10% of sessions
    replaysOnErrorSampleRate: 1.0, // 100% of sessions with errors
    
    // Release tracking
    release: process.env.NEXT_PUBLIC_APP_VERSION,
    
    // Environment
    environment: process.env.NODE_ENV,
    
    // Integrations
    integrations: [
      Sentry.replayIntegration({
        // Mask sensitive content
        maskAllText: true,
        maskAllInputs: true,
        blockAllMedia: false,
        
        // Custom masking
        mask: ['.sensitive', '[data-pii="true"]'],
        block: ['.no-capture'],
      }),
    ],
    
    // Filtering
    beforeSend(event, hint) {
      // Filter out non-error events in development
      if (process.env.NODE_ENV === 'development' && event.level !== 'error') {
        return null;
      }
      
      // Remove PII from error messages
      if (event.message) {
        event.message = event.message.replace(/\b[\w._%+-]+@[\w.-]+\.[A-Z|a-z]{2,}\b/g, '[email]');
      }
      
      return event;
    },
  });
}
