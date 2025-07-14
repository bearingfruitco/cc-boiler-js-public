/**
 * Analytics event handlers using the event queue
 */

import { eventQueue } from './event-queue';
import { BaseEvent } from './event-types';

// Analytics event types
export const ANALYTICS_EVENTS = {
  PAGE_VIEW: 'analytics.page.view',
  USER_ACTION: 'analytics.user.action',
  ERROR_TRACK: 'analytics.error.track',
  PERFORMANCE_MARK: 'analytics.performance.mark',
  CONVERSION: 'analytics.conversion',
  EXPERIMENT: 'analytics.experiment',
} as const;

export type AnalyticsEventType = typeof ANALYTICS_EVENTS[keyof typeof ANALYTICS_EVENTS];

// Page view event
export interface PageViewEvent extends BaseEvent {
  url: string;
  referrer: string;
  title: string;
  path: string;
  query: Record<string, string>;
}

// User action event
export interface UserActionEvent extends BaseEvent {
  category: string;
  action: string;
  label?: string;
  value?: number;
}

// Error tracking event
export interface ErrorEvent extends BaseEvent {
  error: {
    message: string;
    stack?: string;
    type?: string;
  };
  context: Record<string, any>;
}

// Performance event
export interface PerformanceEvent extends BaseEvent {
  metric: string;
  value: number;
  unit: 'ms' | 's' | 'bytes' | 'count';
  tags?: Record<string, string>;
}

/**
 * Track page view
 */
export function trackPageView(data: Partial<PageViewEvent>): void {
  const event: PageViewEvent = {
    timestamp: new Date().toISOString(),
    source: 'analytics',
    version: '1.0',
    url: window.location.href,
    referrer: document.referrer,
    title: document.title,
    path: window.location.pathname,
    query: Object.fromEntries(new URLSearchParams(window.location.search)),
    ...data,
  };

  eventQueue.emit(ANALYTICS_EVENTS.PAGE_VIEW, event);
}

/**
 * Track user action
 */
export function trackAction(
  category: string,
  action: string,
  label?: string,
  value?: number
): void {
  const event: UserActionEvent = {
    timestamp: new Date().toISOString(),
    source: 'analytics',
    version: '1.0',
    category,
    action,
    label,
    value,
  };

  eventQueue.emit(ANALYTICS_EVENTS.USER_ACTION, event);
}

/**
 * Track error
 */
export function trackError(error: Error, context?: Record<string, any>): void {
  const event: ErrorEvent = {
    timestamp: new Date().toISOString(),
    source: 'analytics',
    version: '1.0',
    error: {
      message: error.message,
      stack: error.stack,
      type: error.name,
    },
    context: context || {},
  };

  eventQueue.emit(ANALYTICS_EVENTS.ERROR_TRACK, event, { priority: 'high' });
}

/**
 * Track performance metric
 */
export function trackPerformance(
  metric: string,
  value: number,
  unit: PerformanceEvent['unit'] = 'ms',
  tags?: Record<string, string>
): void {
  const event: PerformanceEvent = {
    timestamp: new Date().toISOString(),
    source: 'analytics',
    version: '1.0',
    metric,
    value,
    unit,
    tags,
  };

  eventQueue.emit(ANALYTICS_EVENTS.PERFORMANCE_MARK, event);
}

/**
 * Track conversion
 */
export function trackConversion(
  conversionType: string,
  value?: number,
  metadata?: Record<string, any>
): void {
  const event: BaseEvent = {
    timestamp: new Date().toISOString(),
    source: 'analytics',
    version: '1.0',
    metadata: {
      type: conversionType,
      value,
      ...metadata,
    },
  };

  eventQueue.emit(ANALYTICS_EVENTS.CONVERSION, event, { priority: 'high' });
}

// Bridge to existing analytics providers
if (typeof window !== 'undefined') {
  // Google Analytics bridge
  eventQueue.on('analytics.*', async (event: BaseEvent) => {
    if ((window as any).gtag) {
      const eventType = event.source.split('.').pop();
      (window as any).gtag('event', eventType, {
        event_category: 'app_analytics',
        ...event.metadata,
      });
    }
  });

  // Performance monitoring
  eventQueue.on(ANALYTICS_EVENTS.PERFORMANCE_MARK, async (event: PerformanceEvent) => {
    // Log to console in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`[Performance] ${event.metric}: ${event.value}${event.unit}`);
    }
    
    // Send to monitoring service
    if ((window as any).performance && (window as any).performance.mark) {
      (window as any).performance.mark(`${event.metric}_${event.value}`);
    }
  });
}
