# Async Event Workflow Guide (v2.3.6)

## Overview

The async event system enables fire-and-forget patterns for non-critical operations, ensuring that tracking, analytics, and notifications never block the user experience.

## Core Concepts

### Critical vs Non-Critical Operations

**Critical Operations** (user must wait):
- Form submission to your API
- Payment processing  
- User authentication
- Data that affects what the user sees next

**Non-Critical Operations** (fire-and-forget):
- Analytics tracking
- Marketing pixels
- Webhooks to external services
- Email notifications
- Audit logging
- Performance metrics

### The Event Queue

```typescript
import { eventQueue, LEAD_EVENTS } from '@/lib/events';

// Fire and forget - returns immediately
eventQueue.emit(LEAD_EVENTS.FORM_SUBMIT, formData);

// Critical operation - must await
await api.submitForm(formData);
```

## Workflow Steps

### 1. Start with PRD Including Async Requirements

```bash
# Create feature PRD
/prd contact-form

# Add async requirements section
/prd-async contact-form
```

The async section will specify:
- What operations are critical (blocking)
- What operations are non-critical (fire-and-forget)
- Required loading states
- Timeout strategies

### 2. Create Forms with Built-in Tracking

```bash
/create-tracked-form ContactForm --vertical=standard --compliance=tcpa
```

This generates a form with:
- Automatic event tracking via `useLeadFormEvents` hook
- Non-blocking submission pattern
- Required loading states
- Proper error handling

### 3. Add Custom Event Handlers

```bash
/create-event-handler facebook-pixel
/create-event-handler crm-webhook
/create-event-handler email-notification
```

Each handler includes:
- Timeout protection (default 5s)
- Retry logic with exponential backoff
- Error isolation (failures don't affect other handlers)

### 4. Validate Before Committing

```bash
/validate-async
```

This checks for:
- Sequential awaits that could be parallel
- Missing loading states
- Blocking analytics calls
- Synchronous event handlers

## Real-World Examples

### Example 1: Lead Capture Form

```typescript
// components/forms/LeadCaptureForm.tsx
export function LeadCaptureForm() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { trackFormSubmit, trackSubmissionResult } = useLeadFormEvents('lead-capture');

  const onSubmit = async (data: FormData) => {
    setIsSubmitting(true);
    
    try {
      // Track form start (non-blocking)
      const startTime = await trackFormSubmit(data);
      
      // Critical path - user waits for this
      const result = await api.submitLead(data);
      
      // Fire all tracking events (non-blocking)
      eventQueue.emit(LEAD_EVENTS.FORM_SUBMIT, {
        formId: 'lead-capture',
        leadId: result.id,
        ...data
      });
      
      // Track success (non-blocking)
      trackSubmissionResult(true, startTime);
      
      // Navigate to thank you page
      router.push('/thank-you');
      
    } catch (error) {
      // Track failure (non-blocking)
      trackSubmissionResult(false, Date.now(), { error });
      
      // Show error to user
      toast.error('Submission failed. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Form fields */}
      
      <Button type="submit" disabled={isSubmitting}>
        {isSubmitting ? <LoadingSpinner /> : 'Submit'}
      </Button>
    </form>
  );
}
```

### Example 2: Event Handler with Retry

```typescript
// lib/events/handlers/crm-webhook.ts
import { eventQueue, LEAD_EVENTS } from '@/lib/events';

const MAX_RETRIES = 3;
const RETRY_DELAY = 1000; // Start with 1 second

eventQueue.on(LEAD_EVENTS.FORM_SUBMIT, async (data) => {
  let attempt = 0;
  
  while (attempt < MAX_RETRIES) {
    try {
      const response = await fetch(process.env.CRM_WEBHOOK_URL!, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
        signal: AbortSignal.timeout(5000), // 5s timeout
      });
      
      if (!response.ok) {
        throw new Error(`Webhook failed: ${response.status}`);
      }
      
      // Success - exit retry loop
      break;
      
    } catch (error) {
      attempt++;
      
      if (attempt >= MAX_RETRIES) {
        // Log final failure but don't throw
        console.error('CRM webhook failed after retries:', error);
        break;
      }
      
      // Exponential backoff
      await new Promise(resolve => 
        setTimeout(resolve, RETRY_DELAY * Math.pow(2, attempt - 1))
      );
    }
  }
});
```

### Example 3: Parallel Data Fetching

```typescript
// ❌ BAD - Sequential (detected by /validate-async)
export async function DashboardPage() {
  const user = await fetchUser();
  const stats = await fetchStats();
  const notifications = await fetchNotifications();
  const recommendations = await fetchRecommendations();
  
  return <Dashboard {...{ user, stats, notifications, recommendations }} />;
}

// ✅ GOOD - Parallel
export async function DashboardPage() {
  const [user, stats, notifications, recommendations] = await Promise.all([
    fetchUser(),
    fetchStats(), 
    fetchNotifications(),
    fetchRecommendations()
  ]);
  
  return <Dashboard {...{ user, stats, notifications, recommendations }} />;
}
```

## Integration with Rudderstack

The event system automatically bridges to Rudderstack:

```typescript
// Your code
eventQueue.emit(LEAD_EVENTS.FORM_SUBMIT, {
  formId: 'contact',
  email: 'user@example.com',
  phone: '555-0123',
  utm_source: 'google',
  utm_campaign: 'summer-2024'
});

// Automatically calls
rudderanalytics.track('Form Submitted', {
  form_id: 'contact',
  email: 'user@example.com', 
  phone: '555-0123',
  context: {
    campaign: {
      source: 'google',
      name: 'summer-2024'
    }
  }
});
```

### Event Name Mapping

| Event Queue Event | Rudderstack Event |
|------------------|-------------------|
| `lead.form.view` | `Form Viewed` |
| `lead.form.start` | `Form Started` |
| `lead.form.field_change` | `Form Field Changed` |
| `lead.form.submit` | `Form Submitted` |
| `lead.captured` | `Lead Captured` |
| `lead.qualified` | `Lead Qualified` |

## Common Patterns

### Pattern 1: Loading States for Every Async Operation

```typescript
// Required by the system
const [isLoading, setIsLoading] = useState(false);
const [isSubmitting, setIsSubmitting] = useState(false);
const [isSaving, setIsSaving] = useState(false);

// Hook warns if async operation without loading state
const handleSave = async () => {
  setIsSaving(true); // Required!
  try {
    await saveData();
  } finally {
    setIsSaving(false);
  }
};
```

### Pattern 2: Timeout Protection

```typescript
// All external calls need timeout
const response = await fetch(url, {
  signal: AbortSignal.timeout(5000), // 5 second timeout
});

// Or with custom timeout handling
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 5000);

try {
  const response = await fetch(url, { signal: controller.signal });
  clearTimeout(timeoutId);
} catch (error) {
  if (error.name === 'AbortError') {
    // Handle timeout specifically
  }
}
```

### Pattern 3: Error Boundaries for Event Handlers

```typescript
// Event handlers should never crash the app
eventQueue.on(LEAD_EVENTS.FORM_SUBMIT, async (data) => {
  try {
    await riskyOperation(data);
  } catch (error) {
    // Log but don't throw
    console.error('Event handler error:', error);
    
    // Optionally track the error
    eventQueue.emit(ANALYTICS_EVENTS.ERROR, {
      error: error.message,
      context: 'form_submit_handler'
    });
  }
});
```

## Testing Async Flows

```bash
# Test a complete async flow
/test-async-flow contact-form

# This will:
# 1. Submit a test form
# 2. Verify critical path completes
# 3. Check all events were emitted
# 4. Confirm handlers executed
# 5. Validate no blocking occurred
```

## Debugging Tips

### Check Event Queue Status

```typescript
// In browser console
window.__eventQueue?.getStats()

// Shows:
// - Events emitted
// - Handlers registered
// - Queue depth
// - Processing status
```

### Enable Debug Mode

```typescript
// In development
if (process.env.NODE_ENV === 'development') {
  eventQueue.on('*', (event, data) => {
    console.log(`[Event] ${event}:`, data);
  });
}
```

### Common Issues

1. **Form submission feels slow**
   - Check if analytics are awaited instead of emitted
   - Run `/validate-async` to find blocking calls

2. **Events not firing**
   - Ensure handlers are registered on app startup
   - Check event name constants match

3. **Timeout errors**
   - Increase timeout for slow endpoints
   - Add retry logic for flaky services

4. **Memory leaks**
   - Remove event listeners on component unmount
   - Use `eventQueue.once()` for one-time handlers

## Best Practices

1. **Always use constants for event names**
   ```typescript
   // Good
   eventQueue.emit(LEAD_EVENTS.FORM_SUBMIT, data);
   
   // Bad
   eventQueue.emit('lead.form.submit', data);
   ```

2. **Group related handlers**
   ```typescript
   // lib/events/handlers/analytics.ts
   // All analytics-related handlers in one file
   ```

3. **Document async requirements in PRDs**
   ```bash
   /prd-async feature-name
   ```

4. **Test both success and failure paths**
   ```typescript
   // Test that failures don't block user
   ```

5. **Monitor event queue health**
   ```typescript
   // Add to your monitoring dashboard
   ```

## Migration Guide

If you have existing forms without async patterns:

1. Run `/validate-async` to find blocking operations
2. Move analytics to event queue
3. Add loading states
4. Test with `/test-async-flow`
5. Deploy with confidence!

The async event system is designed to be incrementally adoptable - you can migrate one form at a time.
