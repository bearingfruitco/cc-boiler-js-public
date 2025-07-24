// Branch awareness events for the async event system
// Integrates with existing lib/events/index.ts

export const BRANCH_EVENTS = {
  // Feature awareness events (non-blocking)
  FEATURE_AWARENESS_SHOWN: 'feature.awareness.shown',
  COMPLETED_FEATURE_MODIFIED: 'feature.completed.modified',
  
  // Branch health events
  MAIN_BRANCH_STALE: 'branch.main.stale',
  BRANCH_LIMIT_WARNING: 'branch.limit.warning',
  
  // Workflow events
  FEATURE_COMPLETED: 'feature.workflow.completed',
  BRANCH_CLEANUP_SUGGESTED: 'branch.cleanup.suggested'
} as const;

// Event handlers (non-blocking, fire-and-forget)
export const branchEventHandlers = {
  [BRANCH_EVENTS.FEATURE_AWARENESS_SHOWN]: async (data: any) => {
    // Log to analytics (non-blocking)
    console.log('Feature awareness:', data.feature, data.file);
  },
  
  [BRANCH_EVENTS.MAIN_BRANCH_STALE]: async (data: any) => {
    // Could trigger notification or suggestion
    console.log('Main branch is', data.hours, 'hours old');
  },
  
  [BRANCH_EVENTS.FEATURE_COMPLETED]: async (data: any) => {
    // Update feature tracking (async)
    try {
      // This would update your GitHub gist or state
      await updateFeatureState(data.feature, 'completed');
    } catch (error) {
      // Non-critical, don't block
      console.error('Failed to update feature state:', error);
    }
  }
};

// Integration with existing event queue
export function registerBranchEvents(eventQueue: EventQueue) {
  // Register handlers
  Object.entries(branchEventHandlers).forEach(([event, handler]) => {
    eventQueue.on(event, handler);
  });
  
  // Emit events from hooks/commands
  // Example: eventQueue.emit(BRANCH_EVENTS.FEATURE_AWARENESS_SHOWN, { feature, file });
}

// Helper to emit branch events from commands
export function emitBranchEvent(eventName: string, data: any) {
  // This integrates with your existing event queue
  if (typeof window !== 'undefined' && window.eventQueue) {
    window.eventQueue.emit(eventName, data);
  }
}
