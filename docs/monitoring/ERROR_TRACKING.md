# Error Tracking with Sentry

> Comprehensive guide to implementing error tracking in production

## 🎯 Overview

This guide covers setting up Sentry for error tracking, including configuration, custom error boundaries, source maps, and privacy considerations.

## 📦 Installation & Setup

### 1. Install Dependencies

```bash
pnpm add @sentry/nextjs
```

### 2. Run the Setup Wizard

```bash
npx @sentry/wizard@latest -i nextjs
```

This wizard will:
- Create configuration files
- Set up source maps uploading
- Add necessary environment variables
- Configure build settings

### 3. Manual Configuration Files

If you prefer manual setup, create these files:

#### `sentry.client.config.ts`
```typescript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  
  // Environment configuration
  environment: process.env.NODE_ENV,
  enabled: process.env.NODE_ENV === "production",
  
  // Performance Monitoring
  tracesSampleRate: process.env.NODE_ENV === "production" ? 0.1 : 1.0,
  
  // Session Replay
  integrations: [
    Sentry.replayIntegration({
      // Privacy settings
      maskAllText: true,
      maskAllInputs: true,
      blockAllMedia: true,
      
      // Sampling
      sessionSampleRate: 0.01, // 1% of sessions
      errorSampleRate: 0.1,    // 10% of sessions with errors
    }),
  ],
  
  // Release tracking
  release: process.env.NEXT_PUBLIC_VERCEL_GIT_COMMIT_SHA,
  
  // Error filtering
  beforeSend(event, hint) {
    // Filter out non-critical errors
    if (event.exception?.values?.[0]?.value?.includes("ResizeObserver")) {
      return null;
    }
    
    // Scrub PII
    if (event.request?.cookies) {
      delete event.request.cookies;
    }
    
    return event;
  },
  
  // Breadcrumb filtering
  beforeBreadcrumb(breadcrumb) {
    // Don't log console.debug breadcrumbs
    if (breadcrumb.category === 'console' && breadcrumb.level === 'debug') {
      return null;
    }
    return breadcrumb;
  },
});
```

#### `sentry.server.config.ts`
```typescript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.SENTRY_DSN || process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  
  // Server-specific settings
  tracesSampleRate: 0.1,
  
  // Profiling (Node.js 16+)
  profilesSampleRate: 0.1,
  
  // Custom error filtering
  beforeSend(event) {
    // Don't log database connection errors in development
    if (process.env.NODE_ENV === 'development' && 
        event.exception?.values?.[0]?.type === 'DatabaseError') {
      return null;
    }
    return event;
  },
});
```

#### `sentry.edge.config.ts`
```typescript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.SENTRY_DSN || process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  
  // Edge runtime specific
  tracesSampleRate: 0.1,
  
  // Disable features not available in edge runtime
  autoSessionTracking: false,
});
```

## 🛡️ Error Handling Patterns

### 1. Custom Error Boundaries

```typescript
// components/ErrorBoundary.tsx
import React from 'react';
import * as Sentry from '@sentry/nextjs';

interface Props {
  children: React.ReactNode;
  fallback?: React.ComponentType<{ error: Error; reset: () => void }>;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    // Log to Sentry
    Sentry.withScope((scope) => {
      scope.setExtras(errorInfo);
      Sentry.captureException(error);
    });
  }

  render() {
    if (this.state.hasError) {
      const { fallback: Fallback } = this.props;
      
      if (Fallback) {
        return (
          <Fallback
            error={this.state.error!}
            reset={() => this.setState({ hasError: false, error: null })}
          />
        );
      }

      return (
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-2xl font-semibold mb-4">Something went wrong</h1>
            <button
              onClick={() => this.setState({ hasError: false, error: null })}
              className="px-4 py-2 bg-blue-500 text-white rounded"
            >
              Try again
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
```

### 2. API Error Handling

```typescript
// lib/api/error-handler.ts
import * as Sentry from '@sentry/nextjs';

export class APIError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public code?: string
  ) {
    super(message);
    this.name = 'APIError';
  }
}

export function handleAPIError(error: unknown) {
  if (error instanceof APIError) {
    // Known API errors
    Sentry.captureException(error, {
      level: error.statusCode >= 500 ? 'error' : 'warning',
      tags: {
        api_error: true,
        status_code: error.statusCode,
        error_code: error.code,
      },
    });
  } else if (error instanceof Error) {
    // Unknown errors
    Sentry.captureException(error, {
      level: 'error',
      tags: {
        unexpected_error: true,
      },
    });
  }
  
  // Re-throw for Next.js error handling
  throw error;
}

// Usage in API route
export async function POST(request: Request) {
  try {
    // Your API logic
  } catch (error) {
    handleAPIError(error);
  }
}
```

### 3. Form Error Tracking

```typescript
// hooks/useFormTracking.ts
import * as Sentry from '@sentry/nextjs';

export function useFormTracking(formName: string) {
  const trackFormError = (field: string, error: string) => {
    Sentry.captureMessage(`Form validation error: ${formName}`, {
      level: 'info',
      tags: {
        form_name: formName,
        field,
      },
      extra: {
        error_message: error,
      },
    });
  };

  const trackFormSubmission = (success: boolean, data?: any) => {
    Sentry.addBreadcrumb({
      category: 'form',
      message: `Form ${formName} submitted`,
      level: 'info',
      data: {
        success,
        form_name: formName,
        // Don't log sensitive data
        field_count: data ? Object.keys(data).length : 0,
      },
    });
  };

  return { trackFormError, trackFormSubmission };
}
```

## 🗺️ Source Map Configuration

### 1. Next.js Configuration

```javascript
// next.config.js
const { withSentryConfig } = require('@sentry/nextjs');

const nextConfig = {
  // Your Next.js config
};

const sentryWebpackPluginOptions = {
  // Organization and project
  org: process.env.SENTRY_ORG,
  project: process.env.SENTRY_PROJECT,
  authToken: process.env.SENTRY_AUTH_TOKEN,

  // Suppresses source map uploading logs during build
  silent: true,

  // Upload source maps for production builds
  hideSourceMaps: true,

  // Automatically release
  release: process.env.NEXT_PUBLIC_VERCEL_GIT_COMMIT_SHA,
};

module.exports = withSentryConfig(nextConfig, sentryWebpackPluginOptions);
```

### 2. Vercel Integration

```bash
# Add to Vercel environment variables
SENTRY_ORG=your-org
SENTRY_PROJECT=your-project
SENTRY_AUTH_TOKEN=your-auth-token
NEXT_PUBLIC_SENTRY_DSN=your-public-dsn
```

## 🚨 Alert Configuration

### 1. Create Alert Rules in Sentry

```typescript
// Example alert configurations (set in Sentry UI)

// High Error Rate Alert
{
  name: "High Error Rate",
  conditions: [
    {
      id: "event_frequency",
      value: 100,
      interval: "1h"
    }
  ],
  actions: [
    {
      id: "send_email",
      targetType: "team",
      targetIdentifier: "engineering"
    }
  ]
}

// Performance Degradation Alert
{
  name: "Slow API Response",
  conditions: [
    {
      id: "p95_transaction_duration",
      value: 3000, // 3 seconds
      dataset: "transactions"
    }
  ],
  actions: [
    {
      id: "send_slack",
      channel: "#alerts"
    }
  ]
}
```

### 2. Custom Alert Logic

```typescript
// lib/monitoring/alerts.ts
import * as Sentry from '@sentry/nextjs';

export function checkCriticalError(error: Error) {
  const criticalErrors = [
    'PaymentProcessingError',
    'DatabaseConnectionError',
    'AuthenticationError',
  ];

  if (criticalErrors.includes(error.name)) {
    Sentry.captureException(error, {
      level: 'fatal',
      tags: {
        critical: true,
        alert_required: true,
      },
    });
    
    // Additional notification logic
    notifyOncall(error);
  }
}
```

## 🔐 Privacy & Security

### 1. PII Scrubbing

```typescript
// sentry.client.config.ts
Sentry.init({
  // ... other config
  
  beforeSend(event) {
    // Remove sensitive data
    if (event.user) {
      delete event.user.email;
      delete event.user.ip_address;
    }
    
    // Scrub URL parameters
    if (event.request?.url) {
      event.request.url = scrubSensitiveParams(event.request.url);
    }
    
    // Remove form data
    if (event.request?.data) {
      delete event.request.data;
    }
    
    return event;
  },
});

function scrubSensitiveParams(url: string): string {
  const sensitiveParams = ['token', 'api_key', 'password', 'secret'];
  const urlObj = new URL(url);
  
  sensitiveParams.forEach(param => {
    if (urlObj.searchParams.has(param)) {
      urlObj.searchParams.set(param, '[REDACTED]');
    }
  });
  
  return urlObj.toString();
}
```

### 2. Data Retention

```typescript
// Configure in Sentry project settings
{
  "dataScrubbing": true,
  "dataScrubberDefaults": true,
  "sensitiveFields": [
    "password",
    "secret",
    "passwd",
    "api_key",
    "apikey",
    "access_token",
    "auth",
    "credentials",
    "mysql_pwd",
    "stripetoken",
    "card[number]"
  ],
  "safeFields": [
    "id",
    "email",
    "username"
  ]
}
```

## 📊 Performance Impact

### Optimization Tips

1. **Sampling Rates**
   ```typescript
   // Adjust based on traffic
   const sampleRate = process.env.NODE_ENV === 'production' 
     ? 0.1  // 10% in production
     : 1.0; // 100% in development
   ```

2. **Lazy Loading**
   ```typescript
   // Only load Sentry when needed
   const initSentry = async () => {
     const Sentry = await import('@sentry/nextjs');
     Sentry.init({ /* config */ });
   };
   ```

3. **Minimal Breadcrumbs**
   ```typescript
   Sentry.init({
     maxBreadcrumbs: 50, // Default is 100
     beforeBreadcrumb(breadcrumb) {
       // Only keep important breadcrumbs
       const allowedCategories = ['navigation', 'error', 'transaction'];
       if (!allowedCategories.includes(breadcrumb.category || '')) {
         return null;
       }
       return breadcrumb;
     },
   });
   ```

## 🧪 Testing Error Tracking

### Local Testing

```typescript
// pages/api/test-sentry.ts
import type { NextApiRequest, NextApiResponse } from 'next';
import * as Sentry from '@sentry/nextjs';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (process.env.NODE_ENV !== 'development') {
    return res.status(404).end();
  }

  try {
    throw new Error('Test Sentry Error');
  } catch (error) {
    Sentry.captureException(error);
    res.status(500).json({ error: 'Test error sent to Sentry' });
  }
}
```

### Production Verification

```bash
# Verify Sentry is working in production
curl https://your-app.com/api/health-check

# Check Sentry dashboard for test event
```

## 📚 Best Practices

1. **Use Appropriate Severity Levels**
   - `fatal` - Application crashes
   - `error` - Handled errors affecting functionality
   - `warning` - Recoverable issues
   - `info` - Notable events
   - `debug` - Development information

2. **Add Context**
   ```typescript
   Sentry.withScope((scope) => {
     scope.setTag('feature', 'checkout');
     scope.setContext('order', { id: orderId, total: orderTotal });
     scope.setUser({ id: userId });
     Sentry.captureException(error);
   });
   ```

3. **Group Similar Errors**
   ```typescript
   Sentry.init({
     beforeSend(event) {
       // Group by error message pattern
       if (event.exception?.values?.[0]?.value?.includes('timeout')) {
         event.fingerprint = ['timeout-error'];
       }
       return event;
     },
   });
   ```

4. **Monitor Error Budget**
   - Set acceptable error rate (e.g., 1%)
   - Alert when approaching limit
   - Review and fix top errors weekly

## 🔗 Integration with CI/CD

### GitHub Actions

```yaml
# .github/workflows/sentry-release.yml
name: Create Sentry Release

on:
  push:
    branches: [main]

jobs:
  create-release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Create Sentry release
        uses: getsentry/action-release@v1
        env:
          SENTRY_AUTH_TOKEN: ${{ secrets.SENTRY_AUTH_TOKEN }}
          SENTRY_ORG: ${{ secrets.SENTRY_ORG }}
          SENTRY_PROJECT: ${{ secrets.SENTRY_PROJECT }}
        with:
          environment: production
          version: ${{ github.sha }}
```

## 🚀 Next Steps

1. Set up [Performance Monitoring](./PERFORMANCE.md)
2. Configure [Custom Dashboards](https://docs.sentry.io/product/dashboards/)
3. Implement [Release Health](https://docs.sentry.io/product/releases/health/)
4. Enable [Profiling](https://docs.sentry.io/product/profiling/) (if needed)

---

**Remember**: The goal is to catch errors before users report them. Start with basic error tracking and gradually add more sophisticated monitoring as your application grows.
