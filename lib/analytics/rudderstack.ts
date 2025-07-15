// Rudderstack Analytics Integration
import type { RudderAnalytics, RudderAnalyticsPreloader } from '@/types/rudderstack';

declare global {
  interface Window {
    rudderanalytics?: RudderAnalytics | RudderAnalyticsPreloader;
  }
}

export function initializeRudderstack(): void {
  if (typeof window === 'undefined') return;
  
  // Create the analytics queue if it doesn't exist
  if (!window.rudderanalytics) {
    window.rudderanalytics = [] as any;
  }
  
  const analytics = window.rudderanalytics;
  
  // Setup the analytics queue
  if (Array.isArray(analytics)) {
    const methods = [
      'load', 'page', 'track', 'identify', 'alias', 'group',
      'ready', 'reset', 'getAnonymousId', 'setAnonymousId'
    ];
    
    methods.forEach((method) => {
      (analytics as any)[method] = function(...args: any[]) {
        (analytics as any).push([method, ...args]);
      };
    });
  }
  
  // Load the SDK if we have keys
  const writeKey = process.env.NEXT_PUBLIC_RUDDERSTACK_KEY;
  const dataPlaneUrl = process.env.NEXT_PUBLIC_RUDDERSTACK_URL;
  
  if (writeKey && dataPlaneUrl && !Array.isArray(analytics)) {
    analytics.load(writeKey, dataPlaneUrl);
  }
}

export function track(event: string, properties?: any): void {
  if (typeof window !== 'undefined' && window.rudderanalytics && !Array.isArray(window.rudderanalytics)) {
    window.rudderanalytics.track(event, properties);
  }
}

export function page(name?: string, properties?: any): void {
  if (typeof window !== 'undefined' && window.rudderanalytics && !Array.isArray(window.rudderanalytics)) {
    window.rudderanalytics.page(name || undefined, properties);
  }
}

export function identify(userId?: string, traits?: any): void {
  if (typeof window !== 'undefined' && window.rudderanalytics && !Array.isArray(window.rudderanalytics)) {
    if (userId) {
      window.rudderanalytics.identify(userId, traits);
    }
  }
}

export const rudderstack = {
  initialize: initializeRudderstack,
  track,
  page,
  identify,
};
