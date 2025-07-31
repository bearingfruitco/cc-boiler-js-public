/**
 * Architecture Change Tracker
 * 
 * A system for tracking and managing changes to software architecture over time.
 */

export * from './types';
export * from './tracker';

// Re-export main class for convenience
export { ArchitectureChangeTracker as default } from './tracker';
