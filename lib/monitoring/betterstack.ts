import { pino } from 'pino';

// BetterStack logging integration
const BETTERSTACK_SOURCE_TOKEN = process.env.BETTERSTACK_SOURCE_TOKEN;

// Create base logger
const logger = pino({
  level: process.env.NODE_ENV === 'production' ? 'info' : 'debug',
  transport: process.env.NODE_ENV === 'development'
    ? {
        target: 'pino-pretty',
        options: {
          colorize: true,
          ignore: 'pid,hostname',
          translateTime: 'SYS:standard',
        },
      }
    : undefined,
  formatters: {
    level: (label) => {
      return { level: label };
    },
  },
  timestamp: pino.stdTimeFunctions.isoTime,
});

// Send logs to BetterStack in production
export async function logToBetterStack(
  level: 'debug' | 'info' | 'warn' | 'error' | 'fatal',
  message: string,
  metadata?: Record<string, any>
) {
  // Log locally
  logger[level](metadata, message);

  // Send to BetterStack if configured
  if (BETTERSTACK_SOURCE_TOKEN && process.env.NODE_ENV === 'production') {
    try {
      await fetch('https://in.logs.betterstack.com', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${BETTERSTACK_SOURCE_TOKEN}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          level,
          message,
          ...metadata,
          timestamp: new Date().toISOString(),
          environment: process.env.NODE_ENV,
          service: 'nextjs-app',
        }),
      });
    } catch (error) {
      // Don't throw on logging errors
      console.error('Failed to send log to BetterStack:', error);
    }
  }
}

// Convenience methods
export const log = {
  debug: (message: string, metadata?: Record<string, any>) =>
    logToBetterStack('debug', message, metadata),
  info: (message: string, metadata?: Record<string, any>) =>
    logToBetterStack('info', message, metadata),
  warn: (message: string, metadata?: Record<string, any>) =>
    logToBetterStack('warn', message, metadata),
  error: (message: string, metadata?: Record<string, any>) =>
    logToBetterStack('error', message, metadata),
  fatal: (message: string, metadata?: Record<string, any>) =>
    logToBetterStack('fatal', message, metadata),
};

// Performance monitoring
export async function trackPerformance(
  operation: string,
  duration: number,
  metadata?: Record<string, any>
) {
  await logToBetterStack('info', `Performance: ${operation}`, {
    ...metadata,
    duration_ms: duration,
    type: 'performance',
  });
}

// Error tracking
export async function trackError(
  error: Error,
  context?: Record<string, any>
) {
  await logToBetterStack('error', error.message, {
    ...context,
    stack: error.stack,
    type: 'error',
    error_name: error.name,
  });
}

// API monitoring
export async function trackApiCall(
  method: string,
  endpoint: string,
  statusCode: number,
  duration: number,
  metadata?: Record<string, any>
) {
  const level = statusCode >= 500 ? 'error' : statusCode >= 400 ? 'warn' : 'info';
  
  await logToBetterStack(level, `API ${method} ${endpoint}`, {
    ...metadata,
    method,
    endpoint,
    status_code: statusCode,
    duration_ms: duration,
    type: 'api',
  });
}

// Export the base logger for direct use
export { logger };
