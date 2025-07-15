import { create } from 'zustand';
import { eventQueue } from '@/lib/events';

interface AnalyticsStore {
  isInitialized: boolean;
  initialize: () => void;
  track: (event: string, properties?: any) => void;
  trackPageView: (page: string, properties?: any) => void;
  trackConversion: (type: string, value?: number) => void;
}

export const useAnalyticsStore = create<AnalyticsStore>((set, get) => ({
  isInitialized: false,
  
  initialize: () => {
    if (!get().isInitialized) {
      if (typeof window !== 'undefined') {
        // Initialize RudderStack or your analytics
        const rudderanalytics = (window as any).rudderanalytics;
        if (rudderanalytics && process.env.NEXT_PUBLIC_RUDDERSTACK_KEY) {
          rudderanalytics.load(
            process.env.NEXT_PUBLIC_RUDDERSTACK_KEY,
            process.env.NEXT_PUBLIC_RUDDERSTACK_URL
          );
        }
      }
      set({ isInitialized: true });
    }
  },
  
  track: (event, properties) => {
    // Use event queue for non-blocking
    eventQueue.emit('analytics.track', {
      event,
      properties,
      timestamp: new Date().toISOString(),
      source: 'analytics-store',
    });
    
    // Also track directly if analytics is available
    if (typeof window !== 'undefined' && (window as any).analytics) {
      (window as any).analytics.track(event, properties);
    }
  },
  
  trackPageView: (page, properties) => {
    eventQueue.emit('analytics.page_view', {
      page,
      properties,
      timestamp: new Date().toISOString(),
      source: 'analytics-store',
    });
    
    if (typeof window !== 'undefined' && (window as any).analytics) {
      (window as any).analytics.page(page, properties);
    }
  },
  
  trackConversion: (type, value) => {
    eventQueue.emit('analytics.conversion', {
      type,
      value,
      timestamp: new Date().toISOString(),
      source: 'analytics-store',
    });
    
    if (typeof window !== 'undefined' && (window as any).analytics) {
      (window as any).analytics.track('Conversion', { type, value });
    }
  }
}));

export const useAnalyticsSession = () => ({});
export const useAnalyticsConfig = () => ({});
export const useAnalyticsActions = () => useAnalyticsStore();

export type { AnalyticsStore };

// Export missing types
export interface AnalyticsEvent {
  event: string;
  properties?: any;
  timestamp: string;
}

export interface PageView {
  page: string;
  properties?: any;
  timestamp: string;
}

export interface FormInteraction {
  fieldName: string;
  eventType: string;
  timestamp: string;
}

export interface ConversionEvent {
  type: string;
  value?: number;
  timestamp: string;
}

export interface Session {
  sessionId: string;
  startedAt: string;
  lastActiveAt: string;
}

export type AnalyticsState = AnalyticsStore;
