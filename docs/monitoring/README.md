# Monitoring and Observability

> Comprehensive monitoring strategy for production Claude Code Boilerplate applications

## 🎯 Overview

This guide covers the complete monitoring and observability setup for production environments, including error tracking, analytics, performance monitoring, and logging strategies.

## 📊 Monitoring Philosophy

Our monitoring approach follows these principles:

1. **Privacy-First**: All tracking respects user privacy and complies with GDPR/CCPA
2. **Performance-Conscious**: Monitoring should never degrade user experience
3. **Actionable Insights**: Every metric should drive specific actions
4. **Cost-Effective**: Balance comprehensive monitoring with reasonable costs
5. **Developer-Friendly**: Easy to implement and debug

## 🛠️ Available Tools & Integrations

### Error Tracking
- **Sentry** (Recommended) - Real-time error tracking with source maps
- **Rollbar** - Alternative error tracking solution
- **Custom Error Boundaries** - React-based error handling

### Analytics
- **Plausible** - Privacy-focused, lightweight analytics
- **PostHog** - Product analytics with session recording
- **Custom Event System** - Built-in async event tracking

### Performance Monitoring
- **Vercel Analytics** - Core Web Vitals and Real User Monitoring
- **Sentry Performance** - Transaction-based performance tracking
- **Custom Performance Monitoring** - Built-in performance utilities

### Uptime Monitoring
- **Better Uptime** - Simple uptime monitoring with status pages
- **Checkly** - Synthetic monitoring and API checks
- **Vercel Monitoring** - Built-in deployment monitoring

### Log Aggregation
- **Axiom** - Fast, cost-effective log aggregation
- **LogDNA** - Real-time log management
- **Vercel Logs** - Built-in function logs

## 🚀 Quick Start Guide

### 1. Essential Setup (Required)

```bash
# Install monitoring dependencies
pnpm add @sentry/nextjs @vercel/analytics

# Set up environment variables
cat >> .env.local << EOL
# Error Tracking
NEXT_PUBLIC_SENTRY_DSN=your_sentry_dsn
SENTRY_ORG=your_org
SENTRY_PROJECT=your_project
SENTRY_AUTH_TOKEN=your_auth_token

# Analytics (optional but recommended)
NEXT_PUBLIC_PLAUSIBLE_DOMAIN=your-domain.com
EOL
```

### 2. Initialize Error Tracking

```typescript
// sentry.client.config.ts
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  integrations: [
    Sentry.replayIntegration({
      maskAllText: true, // Privacy
      blockAllMedia: true, // Performance
    }),
  ],
  tracesSampleRate: process.env.NODE_ENV === "production" ? 0.1 : 1.0,
  replaysSessionSampleRate: 0.01,
  replaysOnErrorSampleRate: 0.1,
});
```

### 3. Add Analytics

```typescript
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

### 4. Implement Custom Events

```typescript
// Using the built-in event system
import { trackEvent } from '@/lib/events';

// Track user actions
trackEvent('user_signup', {
  method: 'google',
  plan: 'free'
});

// Track performance metrics
trackEvent('api_response_time', {
  endpoint: '/api/users',
  duration: 245,
  status: 200
});
```

## 📋 Implementation Checklist

### Phase 1: Foundation (Day 1)
- [ ] Set up Sentry for error tracking
- [ ] Configure source maps for production
- [ ] Add custom error boundaries
- [ ] Test error reporting flow

### Phase 2: Analytics (Day 2)
- [ ] Choose and implement analytics solution
- [ ] Set up cookie consent flow
- [ ] Implement custom event tracking
- [ ] Configure conversion tracking

### Phase 3: Performance (Day 3)
- [ ] Enable Vercel Analytics
- [ ] Set up Core Web Vitals monitoring
- [ ] Configure performance budgets
- [ ] Implement custom performance tracking

### Phase 4: Operations (Day 4)
- [ ] Set up uptime monitoring
- [ ] Configure alert channels (email, Slack)
- [ ] Implement log aggregation
- [ ] Create monitoring dashboard

## 💰 Cost Considerations

### Estimated Monthly Costs (10k MAU)

| Service | Free Tier | Paid Tier | Recommended |
|---------|-----------|-----------|-------------|
| Sentry | 5k errors/month | $26/month | Start free, upgrade as needed |
| Plausible | 30-day trial | $9/month | Worth it for privacy |
| Vercel Analytics | Included | Included | Use it! |
| Better Uptime | 10 monitors | $29/month | Essential for production |
| Axiom | 500MB/month | $25/month | Only if needed |

**Total**: ~$60-90/month for comprehensive monitoring

## 🔗 Related Documentation

- [Error Tracking Guide](./ERROR_TRACKING.md) - Detailed Sentry setup
- [Analytics Implementation](./ANALYTICS.md) - Privacy-first analytics
- [Performance Monitoring](./PERFORMANCE.md) - Core Web Vitals and more
- [Logging Strategy](./LOGGING.md) - Structured logging approach

## 🚨 Common Pitfalls to Avoid

1. **Over-tracking**: Don't track everything - focus on actionable metrics
2. **PII Exposure**: Always scrub personal data from errors and logs
3. **Performance Impact**: Monitor the monitors - ensure low overhead
4. **Alert Fatigue**: Set reasonable thresholds to avoid noise
5. **Cost Creep**: Regularly review usage and optimize

## 🎯 Key Metrics to Track

### User Experience
- Page load time (LCP < 2.5s)
- Interactivity (FID < 100ms)
- Visual stability (CLS < 0.1)
- Error rate (< 1%)
- Bounce rate

### Business Metrics
- User signups
- Feature adoption
- Conversion rates
- Retention metrics
- Revenue events

### Technical Health
- API response times
- Database query performance
- Error rates by endpoint
- Deployment success rate
- Infrastructure costs

## 🔧 Debugging Monitoring Issues

### Error Tracking Not Working?
```bash
# Verify Sentry is initialized
console.log(window.__SENTRY__);

# Test error manually
Sentry.captureException(new Error('Test error'));

# Check network tab for Sentry requests
```

### Analytics Not Recording?
```bash
# Check if blocked by ad blockers
# Verify domain configuration
# Test in incognito mode
# Check cookie consent state
```

### Performance Metrics Missing?
```bash
# Ensure Analytics script is loaded
# Check if running locally (some metrics production-only)
# Verify Vercel Analytics is enabled in dashboard
```

## 📚 Next Steps

1. Start with [Error Tracking](./ERROR_TRACKING.md) - Most critical for production
2. Implement [Analytics](./ANALYTICS.md) - Understand your users
3. Add [Performance Monitoring](./PERFORMANCE.md) - Ensure fast experience
4. Configure [Logging](./LOGGING.md) - Debug production issues

---

**Remember**: Good monitoring is invisible to users but invaluable to developers. Start simple and expand based on actual needs.
