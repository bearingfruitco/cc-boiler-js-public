/**
 * Async utility functions for parallel operations and timeout handling
 */

/**
 * Execute multiple operations in parallel with individual timeout and error handling
 * @param operations Record of named promises
 * @param options Configuration for timeouts and critical operations
 * @returns Array of results with success/error status for each operation
 */
export async function parallelSettle<T = any>(
  operations: Record<string, Promise<T>>,
  options?: {
    timeout?: number;
    critical?: string[];
    throwOnCriticalFailure?: boolean;
  }
): Promise<Array<{
  key: string;
  status: 'success' | 'error' | 'timeout';
  result?: T;
  error?: Error;
  duration: number;
}>> {
  const {
    timeout = 5000,
    critical = [],
    throwOnCriticalFailure = true
  } = options || {};

  const results = await Promise.allSettled(
    Object.entries(operations).map(async ([key, promise]) => {
      const startTime = Date.now();
      
      // Create timeout promise
      const timeoutPromise = new Promise<never>((_, reject) => 
        setTimeout(() => reject(new Error(`Operation '${key}' timed out after ${timeout}ms`)), timeout)
      );

      try {
        const result = await Promise.race([promise, timeoutPromise]);
        return {
          key,
          status: 'success' as const,
          result,
          duration: Date.now() - startTime,
        };
      } catch (error) {
        const duration = Date.now() - startTime;
        const isTimeout = duration >= timeout - 10; // Small buffer for timing
        const errorObj = error instanceof Error ? error : new Error(String(error));
        
        // If it's a critical operation and should throw
        if (critical.includes(key) && throwOnCriticalFailure) {
          throw errorObj;
        }
        
        return {
          key,
          status: isTimeout ? 'timeout' as const : 'error' as const,
          error: errorObj,
          duration,
        };
      }
    })
  );

  // Extract and format results
  return results.map(result => {
    if (result.status === 'fulfilled') {
      return result.value;
    } else {
      // This should not happen as we catch errors above
      return {
        key: 'unknown',
        status: 'error' as const,
        error: new Error(result.reason),
        duration: 0,
      };
    }
  });
}

/**
 * Retry an async operation with exponential backoff
 * @param operation Function that returns a promise
 * @param options Retry configuration
 * @returns Result of the operation
 */
export async function retryWithBackoff<T>(
  operation: () => Promise<T>,
  options?: {
    maxRetries?: number;
    initialDelay?: number;
    maxDelay?: number;
    backoffFactor?: number;
    shouldRetry?: (error: Error) => boolean;
  }
): Promise<T> {
  const {
    maxRetries = 3,
    initialDelay = 1000,
    maxDelay = 30000,
    backoffFactor = 2,
    shouldRetry = () => true,
  } = options || {};

  let lastError: Error | null = null;
  
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await operation();
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));
      
      // Check if we should retry this error
      if (!shouldRetry(lastError)) {
        throw lastError;
      }
      
      // If this was the last attempt, throw
      if (attempt === maxRetries) {
        throw lastError;
      }
      
      // Calculate delay with exponential backoff
      const delay = Math.min(
        initialDelay * Math.pow(backoffFactor, attempt),
        maxDelay
      );
      
      // Wait before next attempt
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  
  // This should never be reached, but TypeScript needs it
  throw lastError || new Error('Retry failed');
}

/**
 * Create a debounced async function
 * @param fn Async function to debounce
 * @param delay Delay in milliseconds
 * @returns Debounced function
 */
export function debounceAsync<T extends (...args: any[]) => Promise<any>>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => Promise<ReturnType<T>> {
  let timeoutId: NodeJS.Timeout | null = null;
  let pendingPromise: Promise<ReturnType<T>> | null = null;

  return (...args: Parameters<T>): Promise<ReturnType<T>> => {
    // Clear existing timeout
    if (timeoutId) {
      clearTimeout(timeoutId);
    }

    // If there's no pending promise, create one
    if (!pendingPromise) {
      pendingPromise = new Promise<ReturnType<T>>((resolve, reject) => {
        timeoutId = setTimeout(async () => {
          try {
            const result = await fn(...args);
            resolve(result);
          } catch (error) {
            reject(error);
          } finally {
            pendingPromise = null;
            timeoutId = null;
          }
        }, delay);
      });
    }

    return pendingPromise;
  };
}

/**
 * Create a throttled async function
 * @param fn Async function to throttle
 * @param limit Time limit in milliseconds
 * @returns Throttled function
 */
export function throttleAsync<T extends (...args: any[]) => Promise<any>>(
  fn: T,
  limit: number
): (...args: Parameters<T>) => Promise<ReturnType<T> | void> {
  let inThrottle = false;
  let lastResult: ReturnType<T> | null = null;

  return async (...args: Parameters<T>): Promise<ReturnType<T> | void> => {
    if (!inThrottle) {
      inThrottle = true;
      
      try {
        lastResult = await fn(...args);
        return lastResult;
      } finally {
        setTimeout(() => {
          inThrottle = false;
        }, limit);
      }
    }
    
    // Return last result if throttled
    return lastResult || undefined;
  };
}

/**
 * Race multiple promises with individual labels
 * @param promises Record of labeled promises
 * @returns Object with winner key and result
 */
export async function labeledRace<T extends Record<string, Promise<any>>>(
  promises: T
): Promise<{
  winner: keyof T;
  result: any;
  duration: number;
}> {
  const startTime = Date.now();
  
  const wrappedPromises = Object.entries(promises).map(
    async ([key, promise]) => {
      const result = await promise;
      return { winner: key, result, duration: Date.now() - startTime };
    }
  );

  return Promise.race(wrappedPromises);
}

/**
 * Execute async operations in sequence with results
 * @param operations Array of async operations
 * @returns Array of results in order
 */
export async function sequence<T>(
  operations: Array<() => Promise<T>>
): Promise<T[]> {
  const results: T[] = [];
  
  for (const operation of operations) {
    results.push(await operation());
  }
  
  return results;
}

/**
 * Batch async operations with concurrency control
 * @param items Items to process
 * @param operation Async operation to perform on each item
 * @param batchSize Maximum concurrent operations
 * @returns Array of results
 */
export async function batchProcess<T, R>(
  items: T[],
  operation: (item: T, index: number) => Promise<R>,
  batchSize: number = 5
): Promise<R[]> {
  const results: R[] = [];
  
  for (let i = 0; i < items.length; i += batchSize) {
    const batch = items.slice(i, i + batchSize);
    const batchResults = await Promise.all(
      batch.map((item, index) => operation(item, i + index))
    );
    results.push(...batchResults);
  }
  
  return results;
}

/**
 * Create a timeout wrapper for any promise
 * @param promise Promise to wrap
 * @param timeoutMs Timeout in milliseconds
 * @param timeoutError Optional custom error message
 * @returns Promise that rejects on timeout
 */
export function withTimeout<T>(
  promise: Promise<T>,
  timeoutMs: number,
  timeoutError = 'Operation timed out'
): Promise<T> {
  return Promise.race([
    promise,
    new Promise<never>((_, reject) =>
      setTimeout(() => reject(new Error(timeoutError)), timeoutMs)
    ),
  ]);
}

/**
 * Async sleep function
 * @param ms Milliseconds to sleep
 * @returns Promise that resolves after delay
 */
export function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}
