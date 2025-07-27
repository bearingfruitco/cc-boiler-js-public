/**
 * Security Middleware Stack
 * Provides rate limiting, input validation, and auth wrappers
 */

import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { headers } from 'next/headers';

// Rate limiting configuration
interface RateLimitConfig {
  window: string; // e.g., '1m', '1h'
  max: number;
  keyGenerator?: (req: NextRequest) => string;
  message?: string;
}

// In-memory store for rate limiting (use Redis in production)
const rateLimitStore = new Map<string, { count: number; resetAt: number }>();

/**
 * Rate limiting middleware
 * @example
 * export const POST = rateLimit({ window: '1m', max: 10 })(handler);
 */
export function rateLimit(config: RateLimitConfig) {
  return function (handler: Function) {
    return async function (req: NextRequest, ...args: any[]) {
      const key = config.keyGenerator?.(req) || getClientIp(req) || 'anonymous';
      const now = Date.now();
      const windowMs = parseWindow(config.window);
      
      const limit = rateLimitStore.get(key) || { count: 0, resetAt: now + windowMs };
      
      if (now > limit.resetAt) {
        limit.count = 0;
        limit.resetAt = now + windowMs;
      }
      
      limit.count++;
      rateLimitStore.set(key, limit);
      
      if (limit.count > config.max) {
        return NextResponse.json(
          { error: config.message || 'Too many requests' },
          { 
            status: 429,
            headers: {
              'X-RateLimit-Limit': config.max.toString(),
              'X-RateLimit-Remaining': '0',
              'X-RateLimit-Reset': new Date(limit.resetAt).toISOString()
            }
          }
        );
      }
      
      // Add rate limit headers to response
      const response = await handler(req, ...args);
      if (response instanceof NextResponse) {
        response.headers.set('X-RateLimit-Limit', config.max.toString());
        response.headers.set('X-RateLimit-Remaining', Math.max(0, config.max - limit.count).toString());
        response.headers.set('X-RateLimit-Reset', new Date(limit.resetAt).toISOString());
      }
      
      return response;
    };
  };
}

/**
 * Input validation middleware
 * @example
 * export const POST = validateInput(schema)(handler);
 */
export function validateInput<T>(schema: z.ZodSchema<T>) {
  return function (handler: Function) {
    return async function (req: NextRequest, ...args: any[]) {
      try {
        const body = await req.json();
        const validated = schema.parse(body);
        
        // Pass validated data to handler
        const modifiedReq = new NextRequest(req);
        (modifiedReq as any).validated = validated;
        
        return handler(modifiedReq, ...args);
      } catch (error) {
        if (error instanceof z.ZodError) {
          return NextResponse.json(
            { 
              error: 'Validation failed',
              details: error.errors 
            },
            { status: 400 }
          );
        }
        
        return NextResponse.json(
          { error: 'Invalid request body' },
          { status: 400 }
        );
      }
    };
  };
}

/**
 * Authentication middleware
 * @example
 * export const GET = withAuth(handler);
 * export const POST = withAuth({ role: 'admin' })(handler);
 */
export function withAuth(options?: { role?: string }) {
  return function (handler: Function) {
    return async function (req: NextRequest, ...args: any[]) {
      // Get auth session (implement based on your auth provider)
      const session = await getServerSession();
      
      if (!session) {
        return NextResponse.json(
          { error: 'Unauthorized' },
          { status: 401 }
        );
      }
      
      // Check role if specified
      if (options?.role && session.user.role !== options.role) {
        return NextResponse.json(
          { error: 'Forbidden' },
          { status: 403 }
        );
      }
      
      // Pass session to handler
      return handler(req, { ...args[0], session });
    };
  };
}

/**
 * Combine multiple middleware
 * @example
 * export const POST = compose(
 *   rateLimit({ window: '1m', max: 10 }),
 *   validateInput(schema),
 *   withAuth()
 * )(handler);
 */
export function compose(...middlewares: Function[]) {
  return function (handler: Function) {
    return middlewares.reduceRight((acc, middleware) => middleware(acc), handler);
  };
}

// Helper functions
function parseWindow(window: string): number {
  const match = window.match(/^(\d+)([smhd])$/);
  if (!match) throw new Error('Invalid window format');
  
  const [, num, unit] = match;
  const multipliers = { s: 1000, m: 60000, h: 3600000, d: 86400000 };
  
  return parseInt(num) * multipliers[unit as keyof typeof multipliers];
}

function getClientIp(req: NextRequest): string | null {
  const forwarded = req.headers.get('x-forwarded-for');
  const ip = forwarded ? forwarded.split(',')[0].trim() : req.headers.get('x-real-ip');
  return ip || null;
}

// Placeholder for actual auth implementation
async function getServerSession(): Promise<any> {
  // Implement based on your auth provider (Supabase, NextAuth, etc.)
  return null;
}

// Export common rate limit configs
export const rateLimits = {
  public: { window: '1m', max: 100 },
  authenticated: { window: '1m', max: 200 },
  sensitive: { window: '1m', max: 10 },
  strict: { window: '1m', max: 5 }
};
