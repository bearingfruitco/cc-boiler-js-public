Create a secure form component with automatic tracking for: $ARGUMENTS

Parse arguments:
- Component name (first argument)
- Vertical (--vertical=debt|healthcare|standard)
- Compliance level (--compliance=standard|hipaa|gdpr)

Steps:

1. Load field definitions:
   - Core tracking fields from field-registry/core/
   - Vertical fields if specified
   - Compliance requirements

2. Generate form component with:
   - All tracking fields auto-captured
   - Prepopulation for allowed fields only
   - PII protection built-in
   - Server-side processing
   - Field masking for sensitive data
   - Proper validation schemas

3. Create the component structure:

```tsx
'use client';

import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { SecureFormHandler } from '@/lib/forms/secure-form-handler';
import { trackingCapture } from '@/lib/forms/tracking-capture';
import { Button } from '@/components/ui/button-component';
import { Card } from '@/components/ui/card-component';

// Generate validation schema from field registry
const formSchema = z.object({
  // [Generated from field definitions]
});

export function $ARGUMENTS() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      // Prepopulated tracking fields only
    }
  });

  // Auto-capture tracking on mount
  useEffect(() => {
    const tracking = trackingCapture.getAll();
    Object.entries(tracking).forEach(([key, value]) => {
      if (form.getValues(key) === undefined) {
        form.setValue(key, value);
      }
    });
  }, []);

  const onSubmit = async (data: z.infer<typeof formSchema>) => {
    setIsSubmitting(true);
    
    try {
      const response = await fetch('/api/forms/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          formId: '$ARGUMENTS',
          data,
          // Tracking data handled server-side
        }),
      });
      
      if (!response.ok) throw new Error('Submission failed');
      
      // Success handling
    } catch (error) {
      // Error handling
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Card className="max-w-md mx-auto">
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        {/* Generated form fields with proper security */}
      </form>
    </Card>
  );
}
```

4. Create API route:

```typescript
// app/api/forms/submit/route.ts
import { NextResponse } from 'next/server';
import { SecureFormHandler } from '@/lib/forms/secure-form-handler';
import { headers } from 'next/headers';

export async function POST(request: Request) {
  const body = await request.json();
  const headersList = headers();
  
  const submission = {
    formData: body.data,
    metadata: {
      formId: body.formId,
      sessionId: headersList.get('x-session-id') || '',
      ipAddress: headersList.get('x-forwarded-for') || '',
      userAgent: headersList.get('user-agent') || '',
    },
  };
  
  const result = await SecureFormHandler.processFormSubmission(
    submission,
    process.env.ENCRYPTION_KEY!
  );
  
  if (!result.success) {
    return NextResponse.json({ errors: result.errors }, { status: 400 });
  }
  
  return NextResponse.json({ success: true, id: result.data?.id });
}
```

5. Security features included:
   - NO PII in console.log
   - NO PII in localStorage
   - NO PII in URLs
   - Server-side cookie capture
   - Automatic device fingerprinting
   - IP geolocation (server-side)
   - Field-level encryption for PII
   - Audit logging
   - Consent tracking

6. Save files:
   - components/forms/$ARGUMENTS.tsx
   - app/api/forms/submit/route.ts (if not exists)
   - lib/forms/schemas/$ARGUMENTS-schema.ts

Important reminders:
- All PII processing happens server-side only
- Tracking fields are auto-captured, not manually entered
- Prepopulation whitelist is strictly enforced
- All submissions are audit logged
- Encryption keys must be configured in .env
