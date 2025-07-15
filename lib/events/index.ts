/**
 * Main exports for the event system
 */

export { eventQueue, emitAsync, emitCritical } from './event-queue';
export type { EventHandler, EventOptions } from './event-queue';
export * from './event-types';
export * from './lead-events';
export * from './analytics-events';

// Re-export commonly used items
export { LEAD_EVENTS } from './lead-events';
export { ANALYTICS_EVENTS } from './analytics-events';
