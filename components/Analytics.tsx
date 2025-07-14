/**
 * Analytics Component
 * Handles analytics initialization and tracking
 */

'use client';

import { useEffect } from 'react';
import { useAnalyticsStore } from '@/stores';

export function Analytics() {
  useEffect(() => {
    // Initialize analytics session
    const analytics = useAnalyticsStore.getState();
    analytics.initialize({
      writeKey: process.env.NEXT_PUBLIC_RUDDERSTACK_KEY || '',
      dataPlaneUrl: process.env.NEXT_PUBLIC_RUDDERSTACK_URL || '',
    });

    // Track page view
    analytics.trackPageView();

    // Set up page view tracking on route changes
    const handleRouteChange = () => {
      analytics.trackPageView();
    };

    // Listen for route changes (Next.js App Router)
    window.addEventListener('popstate', handleRouteChange);

    return () => {
      window.removeEventListener('popstate', handleRouteChange);
    };
  }, []);

  // This component doesn't render anything
  return null;
}
