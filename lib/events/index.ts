/**
 * Main exports for the event system
 */

export { eventQueue, emitAsync, emitCritical } from './event-queue';
export type { EventHandler, EventOptions } from './event-queue';
export * from './event-types';
export * from './lead-events';
export * from './analytics-events';
export * from './security-events';

// Re-export commonly used items
export { LEAD_EVENTS } from './lead-events';
export { ANALYTICS_EVENTS } from './analytics-events';
export { SECURITY_EVENTS, emitSecurityEvent, registerSecurityHandlers } from './security-events';
