import { expect } from "vitest";
/**
 * Test utilities for async operations and event-driven code
 */

import { eventQueue } from '@/lib/events/event-queue';
import { vi } from 'vitest';

/**
 * Wait for a specific event to be emitted
 * @param eventName Name of the event to wait for
 * @param timeout Maximum time to wait in milliseconds
 * @returns Promise that resolves with event data or rejects on timeout
 */
export async function waitForEvent<T = any>(
  eventName: string,
  timeout = 5000
): Promise<T> {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      eventQueue.off(eventName, handler);
      reject(new Error(`Timeout waiting for event: ${eventName}`));
    }, timeout);

    const handler = (data: T) => {
      clearTimeout(timer);
      resolve(data);
    };

    eventQueue.once(eventName, handler);
  });
}

/**
 * Expect a sequence of events to be emitted in order
 * @param events Array of event names expected in order
 * @param action Async function that should trigger the events
 * @param timeout Maximum time to wait for all events
 */
export async function expectEventSequence(
  events: string[],
  action: () => Promise<void>,
  timeout = 5000
): Promise<void> {
  const received: string[] = [];
  const startTime = Date.now();

  // Set up listeners for all expected events
  const handlers = events.map(event => {
    const handler = () => {
      received.push(event);
    };
    eventQueue.once(event, handler);
    return { event, handler };
  });

  try {
    // Execute the action
    await action();

    // Wait for all events or timeout
    while (received.length < events.length && Date.now() - startTime < timeout) {
      await new Promise(resolve => setTimeout(resolve, 50));
    }

    // Clean up any remaining handlers
    handlers.forEach(({ event, handler }) => {
      eventQueue.off(event, handler);
    });

    // Check if we received all events in order
    if (received.length !== events.length) {
      throw new Error(
        `Expected ${events.length} events but received ${received.length}. ` +
        `Expected: ${events.join(', ')}. Received: ${received.join(', ')}`
      );
    }

    if (JSON.stringify(received) !== JSON.stringify(events)) {
      throw new Error(
        `Events received in wrong order. ` +
        `Expected: ${events.join(', ')}. Received: ${received.join(', ')}`
      );
    }
  } catch (error) {
    // Clean up handlers on error
    handlers.forEach(({ event, handler }) => {
      eventQueue.off(event, handler);
    });
    throw error;
  }
}

/**
 * Mock event handler for testing
 * @param eventName Event to mock
 * @returns Object with handler spy and cleanup function
 */
export function mockEventHandler(eventName: string) {
  const handler = vi.fn();
  eventQueue.on(eventName, handler);

  return {
    handler,
    cleanup: () => eventQueue.off(eventName, handler),
    expectCalled: (times = 1) => expect(handler).toHaveBeenCalledTimes(times),
    expectCalledWith: (data: any) => expect(handler).toHaveBeenCalledWith(data),
    reset: () => handler.mockReset(),
  };
}

/**
 * Create a test harness for async operations
 * @param setup Setup function
 * @param teardown Teardown function
 * @returns Test harness functions
 */
export function createAsyncTestHarness<T = any>(
  setup: () => Promise<T>,
  teardown: (context: T) => Promise<void>
) {
  let context: T | null = null;

  return {
    beforeEach: async () => {
      context = await setup();
      return context;
    },
    afterEach: async () => {
      if (context) {
        await teardown(context);
        context = null;
      }
    },
    getContext: () => {
      if (!context) {
        throw new Error('Test harness not initialized. Call beforeEach first.');
      }
      return context;
    },
  };
}

/**
 * Test helper for API mocking with timeout simulation
 */
export function mockApiWithDelay<T>(
  response: T,
  delay = 100,
  shouldFail = false
) {
  return vi.fn().mockImplementation(() => {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        if (shouldFail) {
          reject(new Error('API Error'));
        } else {
          resolve(response);
        }
      }, delay);
    });
  });
}

/**
 * Test helper for simulating network conditions
 */
export class NetworkSimulator {
  private delays = new Map<string, number>();
  private failures = new Map<string, boolean>();

  setDelay(url: string, delay: number) {
    this.delays.set(url, delay);
    return this;
  }

  setFailure(url: string, shouldFail = true) {
    this.failures.set(url, shouldFail);
    return this;
  }

  async simulateFetch(url: string, response: any) {
    const delay = this.delays.get(url) || 0;
    const shouldFail = this.failures.get(url) || false;

    await new Promise(resolve => setTimeout(resolve, delay));

    if (shouldFail) {
      throw new Error(`Network error for ${url}`);
    }

    return response;
  }

  reset() {
    this.delays.clear();
    this.failures.clear();
  }
}

/**
 * Assert that an async function throws with specific error
 */
export async function expectAsyncError(
  fn: () => Promise<any>,
  errorMessage?: string | RegExp
): Promise<void> {
  try {
    await fn();
    throw new Error('Expected function to throw');
  } catch (error) {
    if (errorMessage) {
      if (typeof errorMessage === 'string') {
        expect(error).toHaveProperty('message', errorMessage);
      } else {
        expect(error).toHaveProperty('message');
        expect((error as Error).message).toMatch(errorMessage);
      }
    }
  }
}

/**
 * Measure async operation performance
 */
export async function measurePerformance<T>(
  operation: () => Promise<T>,
  name = 'Operation'
): Promise<{ result: T; duration: number }> {
  const startTime = performance.now();
  const result = await operation();
  const duration = performance.now() - startTime;

  console.log(`${name} took ${duration.toFixed(2)}ms`);

  return { result, duration };
}

/**
 * Create a controllable promise for testing
 */
export function createControllablePromise<T>() {
  let resolve: (value: T) => void;
  let reject: (error: Error) => void;

  const promise = new Promise<T>((res, rej) => {
    resolve = res;
    reject = rej;
  });

  return {
    promise,
    resolve: (value: T) => resolve(value),
    reject: (error: Error) => reject(error),
  };
}

/**
 * Test multiple async operations in parallel
 */
export async function testParallelOperations<T>(
  operations: Array<() => Promise<T>>,
  expectations: {
    maxDuration?: number;
    minDuration?: number;
    successCount?: number;
    failureCount?: number;
  } = {}
): Promise<void> {
  const startTime = Date.now();
  const results = await Promise.allSettled(operations.map(op => op()));
  const duration = Date.now() - startTime;

  const successCount = results.filter(r => r.status === 'fulfilled').length;
  const failureCount = results.filter(r => r.status === 'rejected').length;

  if (expectations.maxDuration !== undefined) {
    expect(duration).toBeLessThanOrEqual(expectations.maxDuration);
  }

  if (expectations.minDuration !== undefined) {
    expect(duration).toBeGreaterThanOrEqual(expectations.minDuration);
  }

  if (expectations.successCount !== undefined) {
    expect(successCount).toBe(expectations.successCount);
  }

  if (expectations.failureCount !== undefined) {
    expect(failureCount).toBe(expectations.failureCount);
  }
}
