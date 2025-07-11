import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

export type ApiHandler<T = any> = (
  request: NextRequest,
  context: { params: T }
) => Promise<NextResponse>;

export function withErrorHandler<T = any>(handler: ApiHandler<T>) {
  return async (request: NextRequest, context: { params: T }) => {
    try {
      return await handler(request, context);
    } catch (error) {
      console.error('API Error:', error);
      
      if (error instanceof z.ZodError) {
        return NextResponse.json(
          { 
            error: 'Validation failed', 
            details: error.errors.map(e => ({
              path: e.path.join('.'),
              message: e.message
            }))
          },
          { status: 400 }
        );
      }
      
      if (error instanceof ApiError) {
        return NextResponse.json(
          { error: error.message },
          { status: error.status }
        );
      }
      
      // Log unexpected errors
      console.error('Unexpected error:', error);
      
      return NextResponse.json(
        { error: 'Internal server error' },
        { status: 500 }
      );
    }
  };
}

// Utility functions for common responses
export const responses = {
  success: (data: any, status = 200) => 
    NextResponse.json(data, { status }),
    
  created: (data: any) => 
    NextResponse.json(data, { status: 201 }),
    
  noContent: () => 
    new NextResponse(null, { status: 204 }),
    
  badRequest: (message = 'Bad request') => 
    NextResponse.json({ error: message }, { status: 400 }),
    
  unauthorized: (message = 'Unauthorized') => 
    NextResponse.json({ error: message }, { status: 401 }),
    
  forbidden: (message = 'Forbidden') => 
    NextResponse.json({ error: message }, { status: 403 }),
    
  notFound: (message = 'Not found') => 
    NextResponse.json({ error: message }, { status: 404 }),
};

// Parse request body with validation
export async function parseBody<T>(
  request: NextRequest,
  schema: z.ZodSchema<T>
): Promise<T> {
  const body = await request.json();
  return schema.parse(body);
}
