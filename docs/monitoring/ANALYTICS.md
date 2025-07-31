# Analytics Implementation Guide

> Privacy-first analytics for understanding user behavior and making data-driven decisions

## 🎯 Overview

This guide covers implementing analytics that respect user privacy while providing actionable insights. We focus on GDPR/CCPA compliance and lightweight tracking solutions.

## 🛡️ Privacy Principles

1. **Minimal Data Collection** - Only track what drives decisions
2. **No Personal Data** - Never track PII without explicit consent
3. **Transparent Tracking** - Clear cookie policies and opt-out options
4. **Data Ownership** - You own your analytics data
5. **Performance First** - Analytics should never slow down the site

## 📊 Analytics Solutions

### Recommended: Plausible Analytics

**Why Plausible?**
- No cookies by default (GDPR compliant without banner)
- Lightweight script (<1KB)
- Privacy-focused
- Simple, actionable metrics
- Real-time data

### Alternative Options

| Solution | Privacy | Size | Cost | Best For |
|----------|---------|------|------|----------|
| Plausible | Excellent | <1KB | $9/mo | Privacy-first sites |
| Fathom | Excellent | 1KB | $14/mo | Simple analytics |
| PostHog | Good | 15KB | Free/$$$ | Product analytics |
| Vercel Analytics | Good | 5KB | Included | Vercel users |
| Google Analytics | Poor | 45KB | Free | Not recommended |

## 🚀 Implementation

### 1. Plausible Setup

```bash
# No installation needed for basic setup
# For self-hosted or proxy setup:
pnpm add next-plausible
```

#### Basic Implementation

```typescript
// app/layout.tsx
import Script from 'next/script';

export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        <Script
          defer
          data-domain="your-domain.com"
          src="https://plausible.io/js/script.js"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

#### Advanced Implementation with Proxy

```typescript
// app/layout.tsx
import PlausibleProvider from 'next-plausible';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <PlausibleProvider
          domain="your-domain.com"
          customDomain="https://your-domain.com"
          selfHosted
          trackOutboundLinks
          revenue
        >
          {children}
        </PlausibleProvider>
      </body>
    </html>
  );
}

// next.config.js - Proxy to avoid ad blockers
module.exports = {
  async rewrites() {
    return [
      {
        source: '/js/script.js',
        destination: 'https://plausible.io/js/script.js'
      },
      {
        source: '/api/event',
        destination: 'https://plausible.io/api/event'
      },
    ];
  },
};
```

### 2. Custom Event Tracking

```typescript
// lib/analytics/events.ts
import { usePlausible } from 'next-plausible';

// Event types for type safety
export type AnalyticsEvent = 
  | 'signup'
  | 'login'
  | 'purchase'
  | 'feature_used'
  | 'form_submitted'
  | 'error_boundary';

export interface EventProperties {
  // Common properties
  method?: string;
  value?: string | number;
  path?: string;
  
  // Revenue tracking
  amount?: number;
  currency?: string;
  
  // Feature tracking
  feature?: string;
  variant?: string;
}

// Hook for components
export function useAnalytics() {
  const plausible = usePlausible();
  
  const trackEvent = (eventName: AnalyticsEvent, props?: EventProperties) => {
    if (typeof window !== 'undefined') {
      // Also track in our event system
      import('@/lib/events').then(({ trackEvent: internalTrack }) => {
        internalTrack(`analytics_${eventName}`, props);
      });
      
      // Track in Plausible
      plausible(eventName, { props });
    }
  };
  
  return { trackEvent };
}

// Direct tracking function
export function trackEvent(eventName: AnalyticsEvent, props?: EventProperties) {
  if (typeof window !== 'undefined' && window.plausible) {
    window.plausible(eventName, { props });
  }
}
```

#### Usage Examples

```typescript
// In a component
function SignupForm() {
  const { trackEvent } = useAnalytics();
  
  const handleSubmit = async (data) => {
    try {
      await signup(data);
      trackEvent('signup', { 
        method: data.provider,
        path: window.location.pathname 
      });
    } catch (error) {
      trackEvent('error_boundary', { 
        feature: 'signup',
        value: error.message 
      });
    }
  };
}

// Revenue tracking
trackEvent('purchase', {
  amount: 99.99,
  currency: 'USD',
  value: 'pro_plan'
});

// Feature usage
trackEvent('feature_used', {
  feature: 'ai_assistant',
  variant: 'chat'
});
```

### 3. Cookie Consent Implementation

```typescript
// components/CookieConsent.tsx
import { useState, useEffect } from 'react';
import { trackEvent } from '@/lib/analytics/events';

export function CookieConsent() {
  const [showBanner, setShowBanner] = useState(false);
  
  useEffect(() => {
    const consent = localStorage.getItem('analytics-consent');
    if (!consent) {
      setShowBanner(true);
    }
  }, []);
  
  const handleAccept = () => {
    localStorage.setItem('analytics-consent', 'accepted');
    setShowBanner(false);
    trackEvent('consent_given', { type: 'analytics' });
    
    // Load analytics scripts
    loadAnalytics();
  };
  
  const handleDecline = () => {
    localStorage.setItem('analytics-consent', 'declined');
    setShowBanner(false);
    
    // Disable all tracking
    window['ga-disable-GA_MEASUREMENT_ID'] = true;
    delete window.plausible;
  };
  
  if (!showBanner) return null;
  
  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t p-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <p className="text-sm">
          We use privacy-friendly analytics to improve your experience.
          No personal data is collected.
        </p>
        <div className="flex gap-3">
          <button
            onClick={handleDecline}
            className="px-4 py-2 text-sm border rounded"
          >
            Decline
          </button>
          <button
            onClick={handleAccept}
            className="px-4 py-2 text-sm bg-blue-600 text-white rounded"
          >
            Accept
          </button>
        </div>
      </div>
    </div>
  );
}
```

### 4. Server-Side Event Tracking

```typescript
// app/api/track/route.ts
import { headers } from 'next/headers';

const PLAUSIBLE_API = 'https://plausible.io/api/event';

export async function POST(request: Request) {
  const { eventName, url, props } = await request.json();
  
  // Get user agent and IP for Plausible
  const headersList = headers();
  const userAgent = headersList.get('user-agent');
  const ip = headersList.get('x-forwarded-for');
  
  try {
    // Send to Plausible
    const response = await fetch(PLAUSIBLE_API, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': userAgent || '',
        'X-Forwarded-For': ip || '',
      },
      body: JSON.stringify({
        name: eventName,
        url: url || 'https://your-domain.com',
        domain: 'your-domain.com',
        props,
      }),
    });
    
    return Response.json({ success: true });
  } catch (error) {
    console.error('Analytics tracking error:', error);
    return Response.json({ success: false }, { status: 500 });
  }
}

// Usage in server components or API routes
async function trackServerEvent(eventName: string, props?: any) {
  await fetch('https://your-domain.com/api/track', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ eventName, props }),
  });
}
```

## 📈 Custom Events Strategy

### Event Taxonomy

```typescript
// lib/analytics/taxonomy.ts

// User Journey Events
export const USER_EVENTS = {
  // Acquisition
  SIGNUP_STARTED: 'signup_started',
  SIGNUP_COMPLETED: 'signup_completed',
  LOGIN: 'login',
  LOGOUT: 'logout',
  
  // Activation
  ONBOARDING_STARTED: 'onboarding_started',
  ONBOARDING_COMPLETED: 'onboarding_completed',
  FIRST_ACTION: 'first_action_completed',
  
  // Engagement
  FEATURE_USED: 'feature_used',
  CONTENT_VIEWED: 'content_viewed',
  SEARCH_PERFORMED: 'search_performed',
  
  // Retention
  SUBSCRIPTION_STARTED: 'subscription_started',
  SUBSCRIPTION_RENEWED: 'subscription_renewed',
  SUBSCRIPTION_CANCELLED: 'subscription_cancelled',
  
  // Revenue
  PURCHASE_INITIATED: 'purchase_initiated',
  PURCHASE_COMPLETED: 'purchase_completed',
  PURCHASE_FAILED: 'purchase_failed',
} as const;

// System Events
export const SYSTEM_EVENTS = {
  ERROR_OCCURRED: 'error_occurred',
  PERFORMANCE_ISSUE: 'performance_issue',
  API_CALL_FAILED: 'api_call_failed',
} as const;
```

### Funnel Tracking

```typescript
// hooks/useFunnelTracking.ts
export function useFunnelTracking(funnelName: string) {
  const { trackEvent } = useAnalytics();
  const [currentStep, setCurrentStep] = useState(0);
  
  const trackStep = (step: number, stepName: string) => {
    trackEvent('funnel_step', {
      funnel: funnelName,
      step: step.toString(),
      step_name: stepName,
      previous_step: currentStep.toString(),
    });
    setCurrentStep(step);
  };
  
  const trackCompletion = (value?: any) => {
    trackEvent('funnel_completed', {
      funnel: funnelName,
      total_steps: currentStep.toString(),
      value,
    });
  };
  
  const trackAbandonment = (reason?: string) => {
    trackEvent('funnel_abandoned', {
      funnel: funnelName,
      step: currentStep.toString(),
      reason,
    });
  };
  
  return { trackStep, trackCompletion, trackAbandonment };
}

// Usage
function CheckoutFlow() {
  const funnel = useFunnelTracking('checkout');
  
  // Track each step
  funnel.trackStep(1, 'cart_view');
  funnel.trackStep(2, 'shipping_info');
  funnel.trackStep(3, 'payment_info');
  funnel.trackCompletion(orderTotal);
}
```

## 🎯 Conversion Tracking

### Goal Setup

```typescript
// lib/analytics/goals.ts
export const GOALS = {
  // Micro conversions
  NEWSLETTER_SIGNUP: {
    id: 'newsletter_signup',
    value: 5, // Assign values for optimization
  },
  DEMO_REQUEST: {
    id: 'demo_request',
    value: 50,
  },
  
  // Macro conversions
  TRIAL_START: {
    id: 'trial_start',
    value: 100,
  },
  PAID_CONVERSION: {
    id: 'paid_conversion',
    value: 1000,
  },
} as const;

export function trackGoal(goal: keyof typeof GOALS, metadata?: any) {
  const goalConfig = GOALS[goal];
  
  trackEvent('goal_completed', {
    goal_id: goalConfig.id,
    goal_value: goalConfig.value,
    ...metadata,
  });
  
  // Also track as custom event
  trackEvent(goalConfig.id as any, metadata);
}
```

### E-commerce Tracking

```typescript
// lib/analytics/ecommerce.ts
export function trackEcommerce(action: 'view' | 'add' | 'remove' | 'purchase', data: {
  items: Array<{
    id: string;
    name: string;
    category?: string;
    price: number;
    quantity: number;
  }>;
  value?: number;
  currency?: string;
  transaction_id?: string;
}) {
  const eventName = `ecommerce_${action}`;
  
  trackEvent(eventName as any, {
    value: data.value || data.items.reduce((sum, item) => sum + (item.price * item.quantity), 0),
    currency: data.currency || 'USD',
    item_count: data.items.length,
    transaction_id: data.transaction_id,
  });
}
```

## 📊 A/B Testing Integration

### Simple A/B Testing

```typescript
// lib/experiments/ab-testing.ts
import { trackEvent } from '@/lib/analytics/events';

export function useABTest(experimentName: string, variants: string[]) {
  const [variant, setVariant] = useState<string>('');
  
  useEffect(() => {
    // Get or assign variant
    const storedVariant = localStorage.getItem(`ab_${experimentName}`);
    
    if (storedVariant && variants.includes(storedVariant)) {
      setVariant(storedVariant);
    } else {
      // Random assignment
      const newVariant = variants[Math.floor(Math.random() * variants.length)];
      localStorage.setItem(`ab_${experimentName}`, newVariant);
      setVariant(newVariant);
      
      // Track assignment
      trackEvent('experiment_assigned', {
        experiment: experimentName,
        variant: newVariant,
      });
    }
  }, [experimentName, variants]);
  
  const trackConversion = (value?: any) => {
    trackEvent('experiment_converted', {
      experiment: experimentName,
      variant,
      value,
    });
  };
  
  return { variant, trackConversion };
}

// Usage
function PricingPage() {
  const { variant, trackConversion } = useABTest('pricing_layout', ['grid', 'table']);
  
  const handlePurchase = () => {
    trackConversion('pro_plan');
    // ... purchase logic
  };
  
  return variant === 'grid' ? <GridPricing /> : <TablePricing />;
}
```

## 🐛 Analytics Debugging

### Debug Mode

```typescript
// lib/analytics/debug.ts
export function enableAnalyticsDebug() {
  if (typeof window !== 'undefined') {
    // Plausible debug
    localStorage.setItem('plausible_debug', 'true');
    
    // Log all tracking calls
    const originalTrack = window.plausible;
    window.plausible = function(...args) {
      console.log('[Analytics]', ...args);
      if (originalTrack) originalTrack(...args);
    };
  }
}

// Usage in development
if (process.env.NODE_ENV === 'development') {
  enableAnalyticsDebug();
}
```

### Testing Analytics

```typescript
// __tests__/analytics.test.ts
import { renderHook } from '@testing-library/react';
import { useAnalytics } from '@/lib/analytics/events';

describe('Analytics', () => {
  beforeEach(() => {
    window.plausible = jest.fn();
  });
  
  it('tracks events correctly', () => {
    const { result } = renderHook(() => useAnalytics());
    
    result.current.trackEvent('signup', { method: 'google' });
    
    expect(window.plausible).toHaveBeenCalledWith('signup', {
      props: { method: 'google' }
    });
  });
});
```

## 📈 Custom Dashboards

### Plausible API Integration

```typescript
// app/api/analytics/stats/route.ts
const PLAUSIBLE_API_KEY = process.env.PLAUSIBLE_API_KEY;
const SITE_ID = 'your-domain.com';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const period = searchParams.get('period') || '30d';
  
  const response = await fetch(
    `https://plausible.io/api/v1/stats/aggregate?site_id=${SITE_ID}&period=${period}&metrics=visitors,pageviews,bounce_rate,visit_duration`,
    {
      headers: {
        Authorization: `Bearer ${PLAUSIBLE_API_KEY}`,
      },
    }
  );
  
  const data = await response.json();
  return Response.json(data);
}
```

### Internal Dashboard Component

```typescript
// components/analytics/Dashboard.tsx
export function AnalyticsDashboard() {
  const [stats, setStats] = useState(null);
  
  useEffect(() => {
    fetch('/api/analytics/stats')
      .then(res => res.json())
      .then(setStats);
  }, []);
  
  if (!stats) return <div>Loading...</div>;
  
  return (
    <div className="grid grid-cols-4 gap-4">
      <StatCard
        title="Visitors"
        value={stats.visitors.value}
        change={stats.visitors.change}
      />
      <StatCard
        title="Page Views"
        value={stats.pageviews.value}
        change={stats.pageviews.change}
      />
      <StatCard
        title="Bounce Rate"
        value={`${stats.bounce_rate.value}%`}
        change={stats.bounce_rate.change}
      />
      <StatCard
        title="Avg Duration"
        value={formatDuration(stats.visit_duration.value)}
        change={stats.visit_duration.change}
      />
    </div>
  );
}
```

## 🔒 Privacy Compliance

### GDPR Compliance Checklist

- [ ] No cookies used (Plausible is cookieless)
- [ ] No personal data collected
- [ ] Clear privacy policy
- [ ] Opt-out mechanism available
- [ ] Data processing agreement with analytics provider
- [ ] Data retention policy defined
- [ ] Right to deletion implemented

### Privacy Policy Template

```markdown
## Analytics

We use Plausible Analytics to understand how visitors use our website. 
This analytics service is privacy-friendly and doesn't use cookies or 
collect personal data. The following information is collected:

- Page URL
- HTTP Referrer
- Browser
- Operating system
- Device type
- Country (from IP address, not stored)

No personal information is collected, and all data is aggregated.

You can opt out by enabling "Do Not Track" in your browser settings.
```

## 🎯 Best Practices

1. **Track Actions, Not Pages**
   - Focus on what users do, not just where they go
   - Track meaningful interactions

2. **Use Consistent Naming**
   - Establish naming conventions early
   - Document your event taxonomy

3. **Avoid Over-Tracking**
   - Every event should answer a question
   - Remove unused events regularly

4. **Respect Privacy**
   - Never track without consent where required
   - Always provide opt-out options

5. **Monitor Performance**
   - Analytics should be <3% of page load time
   - Use async loading always

## 🚀 Next Steps

1. Set up [Performance Monitoring](./PERFORMANCE.md)
2. Configure [Error Tracking](./ERROR_TRACKING.md) 
3. Implement [Custom Dashboards](https://plausible.io/docs/stats-api)
4. Create [Goal Funnels](https://plausible.io/docs/goal-conversions)

---

**Remember**: The best analytics setup is one that provides actionable insights while respecting user privacy. Start simple and add complexity only when needed.
