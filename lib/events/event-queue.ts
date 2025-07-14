/**
 * Browser-compatible async event queue for non-blocking operations
 * Enables fire-and-forget patterns for analytics, tracking, and notifications
 */

export interface EventOptions {
  priority?: 'critical' | 'high' | 'normal' | 'low';
  timeout?: number;
  retries?: number;
  async?: boolean;
}

export interface EventHandler<T = any> {
  (data: T): void | Promise<void>;
}

export class AsyncEventQueue {
  private handlers = new Map<string, Set<EventHandler>>();
  private queue = new Map<string, Array<() => Promise<void>>>();
  private processing = false;

  /**
   * Emit an event with optional async handling
   * @param event Event name (e.g., 'lead.form.submit')
   * @param data Event data payload
   * @param options Event handling options
   */
  async emit<T = any>(event: string, data: T, options: EventOptions = {}): Promise<void> {
    const { priority = 'normal', timeout = 5000, async = true } = options;

    // Get all handlers for this event and wildcard handlers
    const exactHandlers = this.handlers.get(event) || new Set();
    const wildcardHandlers = this.getWildcardHandlers(event);
    const allHandlers = [...exactHandlers, ...wildcardHandlers];

    if (allHandlers.length === 0) {
      console.warn(`No handlers registered for event: ${event}`);
      return;
    }

    if (!async) {
      // Critical path - must complete before continuing
      await this.executeHandlers(allHandlers, data, timeout);
      return;
    }

    // Non-blocking queue for normal operations
    this.queueHandlers(event, allHandlers, data, options);
    
    // Process queue in next tick
    if (!this.processing) {
      setImmediate(() => this.processQueue());
    }
  }

  /**
   * Register an event handler
   */
  on<T = any>(event: string, handler: EventHandler<T>): void {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, new Set());
    }
    this.handlers.get(event)!.add(handler);
  }

  /**
   * Register a one-time event handler
   */
  once<T = any>(event: string, handler: EventHandler<T>): void {
    const wrappedHandler: EventHandler<T> = async (data) => {
      this.off(event, wrappedHandler);
      await handler(data);
    };
    this.on(event, wrappedHandler);
  }

  /**
   * Remove an event handler
   */
  off(event: string, handler: EventHandler): void {
    const handlers = this.handlers.get(event);
    if (handlers) {
      handlers.delete(handler);
      if (handlers.size === 0) {
        this.handlers.delete(event);
      }
    }
  }

  /**
   * Remove all handlers for an event
   */
  removeAllListeners(event?: string): void {
    if (event) {
      this.handlers.delete(event);
    } else {
      this.handlers.clear();
    }
  }

  /**
   * Get count of listeners for an event
   */
  listenerCount(event: string): number {
    const handlers = this.handlers.get(event);
    return handlers ? handlers.size : 0;
  }

  /**
   * Get all registered events
   */
  eventNames(): string[] {
    return Array.from(this.handlers.keys());
  }

  /**
   * Execute handlers with timeout protection
   */
  private async executeHandlers(
    handlers: EventHandler[],
    data: any,
    timeout: number
  ): Promise<void> {
    await Promise.allSettled(
      handlers.map(handler => this.executeWithTimeout(handler, data, timeout))
    );
  }

  /**
   * Execute a single handler with timeout
   */
  private async executeWithTimeout(
    handler: EventHandler,
    data: any,
    timeout: number
  ): Promise<void> {
    const timeoutPromise = new Promise<never>((_, reject) => {
      setTimeout(() => reject(new Error(`Handler timeout after ${timeout}ms`)), timeout);
    });

    try {
      await Promise.race([handler(data), timeoutPromise]);
    } catch (error) {
      console.error('Event handler error:', error);
      // Log to monitoring but don't throw - other handlers should still execute
    }
  }

  /**
   * Queue handlers for async processing
   */
  private queueHandlers(
    event: string,
    handlers: EventHandler[],
    data: any,
    options: EventOptions
  ): void {
    const { priority = 'normal', timeout = 5000 } = options;
    
    const tasks = handlers.map(handler => 
      () => this.executeWithTimeout(handler, data, timeout)
    );

    // Priority-based queue insertion
    const queueKey = `${priority}:${event}`;
    const existing = this.queue.get(queueKey) || [];
    this.queue.set(queueKey, [...existing, ...tasks]);
  }

  /**
   * Process queued events by priority
   */
  private async processQueue(): Promise<void> {
    if (this.processing) return;
    this.processing = true;

    try {
      // Process by priority
      const priorities = ['critical', 'high', 'normal', 'low'];
      
      for (const priority of priorities) {
        const keys = Array.from(this.queue.keys())
          .filter(key => key.startsWith(`${priority}:`));
        
        for (const key of keys) {
          const tasks = this.queue.get(key) || [];
          this.queue.delete(key);
          
          // Execute all tasks for this priority level
          await Promise.allSettled(tasks.map(task => task()));
        }
      }
    } finally {
      this.processing = false;
      
      // Check if more items were queued while processing
      if (this.queue.size > 0) {
        setImmediate(() => this.processQueue());
      }
    }
  }

  /**
   * Get wildcard handlers that match the event
   */
  private getWildcardHandlers(event: string): EventHandler[] {
    const handlers: EventHandler[] = [];
    
    // Support wildcard patterns like 'lead.*' matching 'lead.form.submit'
    for (const [pattern, patternHandlers] of this.handlers) {
      if (pattern.includes('*')) {
        const regex = new RegExp('^' + pattern.replace(/\*/g, '.*') + '$');
        if (regex.test(event)) {
          handlers.push(...patternHandlers);
        }
      }
    }
    
    return handlers;
  }
}

// Global event queue instance
export const eventQueue = new AsyncEventQueue();

// Convenience function for critical events
export async function emitCritical<T = any>(event: string, data: T): Promise<void> {
  return eventQueue.emit(event, data, { async: false });
}

// Convenience function for fire-and-forget
export function emitAsync<T = any>(event: string, data: T, options?: EventOptions): void {
  eventQueue.emit(event, data, { ...options, async: true });
}
