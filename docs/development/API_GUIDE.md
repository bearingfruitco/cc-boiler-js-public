7. **Document thoroughly** - OpenAPI/Swagger
8. **Test at all levels** - Unit, integration, E2E
9. **Monitor performance** - Caching, query optimization
10. **Secure by default** - Headers, sanitization, CORS

## Common Patterns

### Search Endpoint

```typescript
// app/api/search/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';

const searchSchema = z.object({
  q: z.string().min(1).max(100),
  type: z.enum(['users', 'posts', 'all']).optional(),
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().positive().max(50).default(10)
});

export async function GET(request: NextRequest) {
  const query = parseQuery(request, searchSchema);
  
  const results = await performSearch(query);
  
  return NextResponse.json({
    success: true,
    data: results,
    meta: {
      query: query.q,
      type: query.type,
      page: query.page,
      totalResults: results.total
    }
  });
}
```

### File Upload

```typescript
// app/api/upload/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { writeFile } from 'fs/promises';
import path from 'path';

const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;
    
    if (!file) {
      throw new ApiError('No file provided', 400);
    }
    
    // Validate file
    if (file.size > MAX_FILE_SIZE) {
      throw new ApiError('File too large', 400);
    }
    
    if (!ALLOWED_TYPES.includes(file.type)) {
      throw new ApiError('Invalid file type', 400);
    }
    
    // Save file
    const bytes = await file.arrayBuffer();
    const buffer = Buffer.from(bytes);
    
    const filename = `${Date.now()}-${file.name}`;
    const filepath = path.join(process.cwd(), 'public/uploads', filename);
    
    await writeFile(filepath, buffer);
    
    // Save to database
    const upload = await createUpload({
      filename,
      originalName: file.name,
      mimeType: file.type,
      size: file.size,
      url: `/uploads/${filename}`
    });
    
    return NextResponse.json({
      success: true,
      data: upload
    }, { status: 201 });
  } catch (error) {
    return handleApiError(error);
  }
}
```

### Webhooks

```typescript
// app/api/webhooks/stripe/route.ts
import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET!;

export async function POST(request: NextRequest) {
  try {
    const body = await request.text();
    const signature = request.headers.get('stripe-signature')!;
    
    // Verify webhook
    const event = stripe.webhooks.constructEvent(
      body,
      signature,
      webhookSecret
    );
    
    // Handle events
    switch (event.type) {
      case 'payment_intent.succeeded':
        await handlePaymentSuccess(event.data.object);
        break;
      case 'customer.subscription.deleted':
        await handleSubscriptionCanceled(event.data.object);
        break;
      default:
        console.log(`Unhandled event type: ${event.type}`);
    }
    
    return NextResponse.json({ received: true });
  } catch (error) {
    console.error('Webhook error:', error);
    return NextResponse.json(
      { error: 'Webhook handler failed' },
      { status: 400 }
    );
  }
}
```

### Batch Operations

```typescript
// app/api/users/batch/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';

const batchSchema = z.object({
  operations: z.array(z.object({
    method: z.enum(['create', 'update', 'delete']),
    data: z.any()
  })).max(100)
});

export async function POST(request: NextRequest) {
  const body = await request.json();
  const { operations } = batchSchema.parse(body);
  
  const results = await db.transaction(async (tx) => {
    const results = [];
    
    for (const op of operations) {
      switch (op.method) {
        case 'create':
          results.push(await tx.insert(users).values(op.data));
          break;
        case 'update':
          results.push(await tx.update(users).set(op.data));
          break;
        case 'delete':
          results.push(await tx.delete(users).where(eq(users.id, op.data.id)));
          break;
      }
    }
    
    return results;
  });
  
  return NextResponse.json({
    success: true,
    data: results,
    meta: {
      totalOperations: operations.length,
      successful: results.filter(r => r.success).length
    }
  });
}
```

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Check allowed origins
   - Ensure preflight handling
   - Verify headers

2. **Authentication Failures**
   - Token expiration
   - Cookie settings
   - Session management

3. **Validation Errors**
   - Schema mismatches
   - Type coercion
   - Optional vs required

4. **Performance Issues**
   - N+1 queries
   - Missing indexes
   - Large payloads

### Debug Helpers

```typescript
// lib/api/debug.ts
export function debugMiddleware(name: string) {
  return async (request: NextRequest) => {
    console.log(`[${name}] ${request.method} ${request.url}`);
    console.log(`[${name}] Headers:`, Object.fromEntries(request.headers));
    
    if (request.method !== 'GET') {
      const body = await request.json();
      console.log(`[${name}] Body:`, body);
    }
    
    const start = Date.now();
    const response = NextResponse.next();
    const duration = Date.now() - start;
    
    console.log(`[${name}] Response time: ${duration}ms`);
    
    return response;
  };
}
```

## Resources

- [Next.js Route Handlers](https://nextjs.org/docs/app/building-your-application/routing/route-handlers)
- [Zod Documentation](https://zod.dev)
- [Drizzle ORM](https://orm.drizzle.team)
- [OpenAPI Specification](https://swagger.io/specification/)
- [REST API Best Practices](https://restfulapi.net)

## Summary

Building robust APIs with Next.js 15 App Router requires:
- Strong typing with TypeScript and Zod
- Consistent error handling
- Security-first approach
- Performance optimization
- Comprehensive testing
- Clear documentation

Follow these patterns and your APIs will be production-ready, maintainable, and scalable.
