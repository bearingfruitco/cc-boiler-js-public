/**
 * React hooks for the event system
 */

import { useCallback, useEffect, useRef } from 'react';
import { eventQueue, EventOptions } from '@/lib/events/event-queue';
import { EventHandler } from '@/lib/events/event-types';

/**
 * Hook to emit events with automatic cleanup
 */
export function useEventEmitter() {
  const isMountedRef = useRef(true);

  useEffect(() => {
    return () => {
      isMountedRef.current = false;
    };
  }, []);

  const emit = useCallback(
    async <T = any>(event: string, data: T, options?: EventOptions) => {
      if (!isMountedRef.current) return;
      await eventQueue.emit(event, data, options);
    },
    []
  );

  const emitAsync = useCallback(
    <T = any>(event: string, data: T, options?: EventOptions) => {
      if (!isMountedRef.current) return;
      eventQueue.emit(event, data, { ...options, async: true });
    },
    []
  );

  const emitCritical = useCallback(
    async <T = any>(event: string, data: T, options?: EventOptions) => {
      if (!isMountedRef.current) return;
      await eventQueue.emit(event, data, { ...options, async: false });
    },
    []
  );

  return { emit, emitAsync, emitCritical };
}

/**
 * Hook to listen to events with automatic cleanup
 */
export function useEventListener<T = any>(
  event: string,
  handler: EventHandler<T>,
  deps: React.DependencyList = []
) {
  const savedHandler = useRef(handler);

  // Update handler ref when it changes
  useEffect(() => {
    savedHandler.current = handler;
  }, [handler]);

  useEffect(() => {
    // Create stable handler that calls current ref
    const stableHandler: EventHandler<T> = (data) => {
      if (savedHandler.current) {
        savedHandler.current(data);
      }
    };

    eventQueue.on(event, stableHandler);

    return () => {
      eventQueue.off(event, stableHandler);
    };
  }, [event, ...deps]);
}

/**
 * Hook to track event metrics
 */
export function useEventMetrics(eventPattern?: string) {
  const [metrics, setMetrics] = useState({
    totalEvents: 0,
    eventCounts: {} as Record<string, number>,
  });

  useEventListener(
    eventPattern || '*',
    useCallback((data: any) => {
      setMetrics((prev) => ({
        totalEvents: prev.totalEvents + 1,
        eventCounts: {
          ...prev.eventCounts,
          [data.source]: (prev.eventCounts[data.source] || 0) + 1,
        },
      }));
    }, [])
  );

  return metrics;
}

/**
 * Hook for lead form events
 */
export function useLeadFormEvents(formId: string) {
  const { emit, emitAsync } = useEventEmitter();
  const [sessionId] = useState(() => 
    `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  );

  const trackFormView = useCallback(() => {
    emitAsync('lead.form.view', {
      formId,
      sessionId,
      timestamp: new Date().toISOString(),
      source: 'lead-form',
    });
  }, [formId, sessionId, emitAsync]);

  const trackFormStart = useCallback(() => {
    emitAsync('lead.form.start', {
      formId,
      sessionId,
      timestamp: new Date().toISOString(),
      source: 'lead-form',
    });
  }, [formId, sessionId, emitAsync]);

  const trackFieldChange = useCallback(
    (fieldName: string, oldValue: any, newValue: any, isValid: boolean) => {
      emitAsync('lead.field.change', {
        formId,
        sessionId,
        fieldName,
        oldValue,
        newValue,
        isValid,
        timestamp: new Date().toISOString(),
        source: 'lead-form',
      });
    },
    [formId, sessionId, emitAsync]
  );

  const trackFormSubmit = useCallback(
    async (data: Record<string, any>) => {
      const startTime = Date.now();
      
      await emit('lead.form.submit', {
        formId,
        sessionId,
        data,
        timestamp: new Date().toISOString(),
        source: 'lead-form',
      });

      return startTime;
    },
    [formId, sessionId, emit]
  );

  const trackSubmissionResult = useCallback(
    (success: boolean, startTime: number, errors?: Record<string, string>) => {
      const event = success ? 'lead.submission.success' : 'lead.submission.error';
      
      emitAsync(event, {
        formId,
        sessionId,
        success,
        errors,
        duration: Date.now() - startTime,
        timestamp: new Date().toISOString(),
        source: 'lead-form',
      });
    },
    [formId, sessionId, emitAsync]
  );

  // Track form view on mount
  useEffect(() => {
    trackFormView();
  }, [trackFormView]);

  return {
    sessionId,
    trackFormStart,
    trackFieldChange,
    trackFormSubmit,
    trackSubmissionResult,
  };
}

/**
 * Hook to wait for events
 */
export function useEventWaiter() {
  const waitForEvent = useCallback(
    <T = any>(event: string, timeout = 5000): Promise<T> => {
      return new Promise((resolve, reject) => {
        const timer = setTimeout(() => {
          eventQueue.off(event, handler);
          reject(new Error(`Timeout waiting for event: ${event}`));
        }, timeout);

        const handler: EventHandler<T> = (data) => {
          clearTimeout(timer);
          resolve(data);
        };

        eventQueue.once(event, handler);
      });
    },
    []
  );

  return { waitForEvent };
}

import { useState } from 'react';
