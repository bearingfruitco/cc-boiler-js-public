/**
 * Initialize analytics and event system
 * This should be called once in your app's root layout or _app.tsx
 */

import { initAnalytics } from '@/lib/analytics/rudderstack';
import { initAnalyticsBridge } from '@/lib/analytics/analytics-bridge';

let initialized = false;

export function initializeApp() {
  if (initialized || typeof window === 'undefined') {
    return;
  }

  initialized = true;

  // Initialize Rudderstack
  initAnalytics();

  // Initialize the event queue -> Rudderstack bridge
  initAnalyticsBridge();

  // Log initialization in development
  if (process.env.NODE_ENV === 'development') {
    console.log('[App] Analytics and event system initialized');
  }
}
