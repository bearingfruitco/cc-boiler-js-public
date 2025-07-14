/**
 * Type definitions for the event system
 */

import { z } from 'zod';

// Base event structure
export const BaseEventSchema = z.object({
  id: z.string().optional(),
  timestamp: z.string().datetime(),
  source: z.string(),
  version: z.string().default('1.0'),
  metadata: z.record(z.any()).optional(),
});

export type BaseEvent = z.infer<typeof BaseEventSchema>;

// Event handler types
export type EventHandler<T = any> = (data: T) => void | Promise<void>;
export type EventUnsubscribe = () => void;

// Event options
export interface EventOptions {
  priority?: 'critical' | 'high' | 'normal' | 'low';
  timeout?: number;
  retries?: number;
  async?: boolean;
}

// Event result for tracking
export interface EventResult {
  event: string;
  success: boolean;
  duration: number;
  error?: Error;
  retries?: number;
}

// Event metrics
export interface EventMetrics {
  totalEvents: number;
  successfulEvents: number;
  failedEvents: number;
  averageDuration: number;
  eventCounts: Record<string, number>;
  errorCounts: Record<string, number>;
}
