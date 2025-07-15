/**
 * Analytics Component
 * Handles analytics initialization and tracking
 */

'use client';

import { useEffect } from 'react';
import { usePathname } from 'next/navigation';
import { useAnalyticsStore } from '@/stores/analytics-store';

export function Analytics() {
  const pathname = usePathname();
  const { initialize, trackPageView } = useAnalyticsStore();

  useEffect(() => {
    // Initialize analytics on mount
    initialize();
  }, [initialize]);

  useEffect(() => {
    // Track page view on route change
    trackPageView(pathname, {
      url: window.location.href,
      path: pathname,
      referrer: document.referrer,
      title: document.title,
    });
  }, [pathname, trackPageView]);

  // This component doesn't render anything
  return null;
}
