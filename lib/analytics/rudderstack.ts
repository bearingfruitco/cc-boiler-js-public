import type { RudderAnalytics } from '@rudderstack/analytics-js';

declare global {
  interface Window {
    rudderanalytics?: RudderAnalytics;
  }
}

export function initAnalytics() {
  if (typeof window === 'undefined' || !process.env.NEXT_PUBLIC_RUDDERSTACK_KEY) {
    return;
  }

  // Load RudderStack
  (function() {
    const rudderanalytics = window.rudderanalytics = [];
    const methods = [
      'load', 'page', 'track', 'identify', 'alias', 'group',
      'ready', 'reset', 'getAnonymousId', 'setAnonymousId'
    ];
    
    for (let i = 0; i < methods.length; i++) {
      const method = methods[i];
      rudderanalytics[method] = function(...args) {
        rudderanalytics.push([method].concat(args));
      };
    }
    
    rudderanalytics.load(
      process.env.NEXT_PUBLIC_RUDDERSTACK_KEY,
      process.env.NEXT_PUBLIC_RUDDERSTACK_DATA_PLANE_URL
    );
    
    const script = document.createElement('script');
    script.src = 'https://cdn.rudderlabs.com/v1.1/rudder-analytics.min.js';
    script.async = true;
    document.head.appendChild(script);
  })();
}

export function trackEvent(event: string, properties?: Record<string, any>) {
  if (typeof window !== 'undefined' && window.rudderanalytics) {
    window.rudderanalytics.track(event, properties);
  }
}

export function identifyUser(userId: string, traits?: Record<string, any>) {
  if (typeof window !== 'undefined' && window.rudderanalytics) {
    window.rudderanalytics.identify(userId, traits);
  }
}

export function pageView(name?: string, properties?: Record<string, any>) {
  if (typeof window !== 'undefined' && window.rudderanalytics) {
    window.rudderanalytics.page(name, properties);
  }
}
