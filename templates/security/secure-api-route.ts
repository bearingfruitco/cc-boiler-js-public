import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { createClient } from '@/lib/supabase/server';
import { rateLimit, validateInput, withAuth, compose } from '@/lib/security/middleware';
import { eventQueue, SECURITY_EVENTS } from '@/lib/events';

/**
 * Secure API Route Template
 * Includes rate limiting, input validation, and authentication
 */

// Input validation schema
const requestSchema = z.object({
  // Define your input schema here
  name: z.string().min(2).max(100),
  email: z.string().email(),
  message: z.string().min(10).max(1000),
});

type RequestData = z.infer<typeof requestSchema>;

// Rate limit configuration
const rateLimitConfig = {
  window: '1m',
  max: 10, // 10 requests per minute
  keyGenerator: (req: NextRequest) => {
    // Use user ID if authenticated, otherwise IP
    const userId = req.headers.get('x-user-id');
    return userId || req.headers.get('x-forwarded-for') || 'anonymous';
  }
};

/**
 * GET handler - Public endpoint with rate limiting
 */
export const GET = rateLimit({ window: '1m', max: 100 })(
  async (req: NextRequest) => {
    try {
      const { searchParams } = new URL(req.url);
      const id = searchParams.get('id');
      
      // Get Supabase client
      const supabase = createClient();
      
      // Query with RLS automatically applied
      const { data, error } = await supabase
        .from('{{table_name}}')
        .select('*')
        .eq('id', id)
        .single();
      
      if (error) throw error;
      
      return NextResponse.json({ data });
    } catch (error) {
      console.error('GET error:', error);
      return NextResponse.json(
        { error: 'Failed to fetch data' },
        { status: 500 }
      );
    }
  }
);

/**
 * POST handler - Protected endpoint with full security
 */
export const POST = compose(
  rateLimit(rateLimitConfig),
  validateInput(requestSchema),
  withAuth()
)(async (req: NextRequest & { validated: RequestData }, { session }: any) => {
  try {
    const data = req.validated;
    const userId = session.user.id;
    
    // Get Supabase client
    const supabase = createClient();
    
    // Insert with RLS
    const { data: result, error } = await supabase
      .from('{{table_name}}')
      .insert({
        ...data,
        user_id: userId,
        created_at: new Date().toISOString(),
      })
      .select()
      .single();
    
    if (error) throw error;
    
    // Track event (non-blocking)
    eventQueue.emit(SECURITY_EVENTS.API_SUCCESS, {
      endpoint: '/api/{{route_name}}',
      method: 'POST',
      userId,
      timestamp: Date.now(),
    });
    
    return NextResponse.json(
      { success: true, data: result },
      { status: 201 }
    );
  } catch (error) {
    // Track security event (non-blocking)
    eventQueue.emit(SECURITY_EVENTS.API_ERROR, {
      endpoint: '/api/{{route_name}}',
      method: 'POST',
      error: error instanceof Error ? error.message : 'Unknown error',
      timestamp: Date.now(),
    });
    
    console.error('POST error:', error);
    return NextResponse.json(
      { error: 'Failed to create resource' },
      { status: 500 }
    );
  }
});

/**
 * PUT handler - Update with ownership check
 */
export const PUT = compose(
  rateLimit({ window: '1m', max: 20 }),
  validateInput(requestSchema.partial()),
  withAuth()
)(async (req: NextRequest & { validated: Partial<RequestData> }, { session }: any) => {
  try {
    const data = req.validated;
    const userId = session.user.id;
    const { searchParams } = new URL(req.url);
    const id = searchParams.get('id');
    
    if (!id) {
      return NextResponse.json(
        { error: 'Resource ID required' },
        { status: 400 }
      );
    }
    
    const supabase = createClient();
    
    // Update with RLS (will fail if user doesn't own the resource)
    const { data: result, error } = await supabase
      .from('{{table_name}}')
      .update({
        ...data,
        updated_at: new Date().toISOString(),
      })
      .eq('id', id)
      .eq('user_id', userId) // Ownership check
      .select()
      .single();
    
    if (error) {
      if (error.code === 'PGRST116') {
        return NextResponse.json(
          { error: 'Resource not found or access denied' },
          { status: 404 }
        );
      }
      throw error;
    }
    
    return NextResponse.json({ success: true, data: result });
  } catch (error) {
    console.error('PUT error:', error);
    return NextResponse.json(
      { error: 'Failed to update resource' },
      { status: 500 }
    );
  }
});

/**
 * DELETE handler - Soft delete with ownership check
 */
export const DELETE = compose(
  rateLimit({ window: '1m', max: 10 }),
  withAuth()
)(async (req: NextRequest, { session }: any) => {
  try {
    const userId = session.user.id;
    const { searchParams } = new URL(req.url);
    const id = searchParams.get('id');
    
    if (!id) {
      return NextResponse.json(
        { error: 'Resource ID required' },
        { status: 400 }
      );
    }
    
    const supabase = createClient();
    
    // Soft delete with RLS
    const { error } = await supabase
      .from('{{table_name}}')
      .update({ deleted_at: new Date().toISOString() })
      .eq('id', id)
      .eq('user_id', userId); // Ownership check
    
    if (error) {
      if (error.code === 'PGRST116') {
        return NextResponse.json(
          { error: 'Resource not found or access denied' },
          { status: 404 }
        );
      }
      throw error;
    }
    
    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('DELETE error:', error);
    return NextResponse.json(
      { error: 'Failed to delete resource' },
      { status: 500 }
    );
  }
});

// Security headers for all responses
export async function middleware(req: NextRequest) {
  const response = NextResponse.next();
  
  // Security headers
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-XSS-Protection', '1; mode=block');
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  
  return response;
}
