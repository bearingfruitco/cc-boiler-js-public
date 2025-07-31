# Deployment Guide

> Complete guide to deploying Claude Code Boilerplate applications to production

## 🎯 Overview

This guide covers deployment options, configuration, and best practices for taking your Claude Code Boilerplate application to production. We'll focus on Vercel deployment while covering other platforms.

## 🚀 Quick Start

### Deploy to Vercel (Recommended)

```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Deploy
vercel

# 3. Follow prompts
# - Link to existing project or create new
# - Configure environment variables
# - Deploy to production
```

### One-Click Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-repo/claude-code-boilerplate)

## 📋 Pre-Deployment Checklist

### Code Quality
- [ ] All tests passing: `npm test`
- [ ] TypeScript compiles: `npm run typecheck`
- [ ] No linting errors: `npm run lint`
- [ ] Design system compliant: `/vd`
- [ ] Security audit passed: `/chain security-audit`

### Performance
- [ ] Lighthouse score > 90
- [ ] Bundle size optimized
- [ ] Images optimized
- [ ] Fonts preloaded
- [ ] Critical CSS inlined

### Security
- [ ] Environment variables secure
- [ ] API routes protected
- [ ] CORS configured
- [ ] Rate limiting enabled
- [ ] CSP headers set

### Legal/Compliance
- [ ] Privacy policy updated
- [ ] Terms of service ready
- [ ] Cookie consent implemented
- [ ] GDPR compliance checked
- [ ] Analytics configured

## 🌍 Deployment Platforms

### [Vercel (Recommended)](./VERCEL_GUIDE.md)
Best for Next.js applications with excellent DX and performance.

**Pros:**
- Zero-config Next.js deployment
- Automatic HTTPS
- Edge functions
- Preview deployments
- Analytics included

**Cons:**
- Vendor lock-in for some features
- Pricing can scale quickly

### AWS (Amplify/EC2)
For full control and scalability.

**Pros:**
- Complete infrastructure control
- Cost-effective at scale
- Many service integrations
- Global reach

**Cons:**
- Complex setup
- Requires DevOps knowledge
- Manual scaling configuration

### Self-Hosted (Docker)
For on-premise or custom requirements.

**Pros:**
- Full control
- No vendor lock-in
- Custom security
- Predictable costs

**Cons:**
- Maintenance burden
- Manual updates
- Infrastructure management

## 🔧 Environment Configuration

### [Complete Environment Variables Guide](./ENVIRONMENT_VARIABLES.md)

### Essential Variables

```env
# Application
NEXT_PUBLIC_APP_URL=https://your-domain.com
NODE_ENV=production

# Database
DATABASE_URL=postgresql://...
DATABASE_POOL_URL=postgresql://...?pgbouncer=true

# Authentication
NEXTAUTH_URL=https://your-domain.com
NEXTAUTH_SECRET=generate-with-openssl-rand-base64-32

# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=xxx
SUPABASE_SERVICE_ROLE_KEY=xxx

# Error Tracking
NEXT_PUBLIC_SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx
SENTRY_AUTH_TOKEN=xxx
```

### Environment-Specific Config

```typescript
// lib/config/environment.ts
export const config = {
  isProd: process.env.NODE_ENV === 'production',
  isStaging: process.env.VERCEL_ENV === 'preview',
  isDev: process.env.NODE_ENV === 'development',
  
  app: {
    url: process.env.NEXT_PUBLIC_APP_URL!,
    name: process.env.NEXT_PUBLIC_APP_NAME || 'Claude App',
  },
  
  features: {
    analytics: process.env.NEXT_PUBLIC_ENABLE_ANALYTICS === 'true',
    sentry: process.env.NEXT_PUBLIC_SENTRY_DSN ? true : false,
  },
};
```

## 📊 Monitoring & Observability

### Error Tracking (Sentry)

```typescript
// sentry.client.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.VERCEL_ENV || 'development',
  tracesSampleRate: 0.1, // 10% in production
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
});
```

### Analytics

```typescript
// lib/analytics.ts
export function trackEvent(
  event: string,
  properties?: Record<string, any>
) {
  if (!config.features.analytics) return;
  
  // Your analytics implementation
  if (window.gtag) {
    window.gtag('event', event, properties);
  }
}
```

### Performance Monitoring

```typescript
// app/layout.tsx
export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              // Web Vitals
              if (typeof window !== 'undefined') {
                window.addEventListener('load', () => {
                  if ('PerformanceObserver' in window) {
                    // Monitor CLS, FID, LCP
                  }
                });
              }
            `,
          }}
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

## 🔒 Security Headers

### Next.js Security Headers

```typescript
// next.config.js
const securityHeaders = [
  {
    key: 'X-DNS-Prefetch-Control',
    value: 'on',
  },
  {
    key: 'Strict-Transport-Security',
    value: 'max-age=63072000; includeSubDomains; preload',
  },
  {
    key: 'X-Frame-Options',
    value: 'SAMEORIGIN',
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff',
  },
  {
    key: 'Referrer-Policy',
    value: 'strict-origin-when-cross-origin',
  },
  {
    key: 'Content-Security-Policy',
    value: ContentSecurityPolicy.replace(/\s{2,}/g, ' ').trim(),
  },
];

module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: securityHeaders,
      },
    ];
  },
};
```

### Content Security Policy

```typescript
const ContentSecurityPolicy = `
  default-src 'self';
  script-src 'self' 'unsafe-eval' 'unsafe-inline' *.vercel-analytics.com;
  style-src 'self' 'unsafe-inline';
  img-src 'self' blob: data: https:;
  font-src 'self';
  object-src 'none';
  base-uri 'self';
  form-action 'self';
  frame-ancestors 'none';
  upgrade-insecure-requests;
`;
```

## 🚄 Performance Optimization

### Build Optimization

```typescript
// next.config.js
module.exports = {
  // Enable SWC minification
  swcMinify: true,
  
  // Optimize images
  images: {
    domains: ['your-cdn.com'],
    formats: ['image/avif', 'image/webp'],
  },
  
  // Bundle analyzer
  webpack: (config, { isServer }) => {
    if (process.env.ANALYZE === 'true') {
      const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');
      config.plugins.push(
        new BundleAnalyzerPlugin({
          analyzerMode: 'static',
          openAnalyzer: true,
        })
      );
    }
    return config;
  },
};
```

### Edge Optimization

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Add security headers
  const response = NextResponse.next();
  
  // Cache static assets
  if (request.nextUrl.pathname.startsWith('/_next/static')) {
    response.headers.set(
      'Cache-Control',
      'public, max-age=31536000, immutable'
    );
  }
  
  return response;
}
```

## 🔄 CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 20
          cache: 'npm'
      
      - run: npm ci
      - run: npm run test
      - run: npm run typecheck
      - run: npm run lint

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: vercel/action@v3
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

### Pre-Deployment Scripts

```json
// package.json
{
  "scripts": {
    "predeploy": "npm run test && npm run build",
    "deploy": "vercel --prod",
    "deploy:preview": "vercel"
  }
}
```

## 🔄 Database Migrations

### Production Migration Strategy

```bash
# 1. Backup database
npm run db:backup

# 2. Run migrations
npm run db:migrate:deploy

# 3. Verify
npm run db:verify
```

### Migration Script

```typescript
// scripts/migrate-prod.ts
import { sql } from '@vercel/postgres';

async function migrate() {
  console.log('Starting production migration...');
  
  try {
    // Run migrations
    await sql`CREATE TABLE IF NOT EXISTS ...`;
    
    console.log('Migration completed successfully');
  } catch (error) {
    console.error('Migration failed:', error);
    process.exit(1);
  }
}

migrate();
```

## 🔁 Rollback Strategy

### Instant Rollback

```bash
# Vercel instant rollback
vercel rollback

# Or via dashboard
# Visit: https://vercel.com/[team]/[project]/deployments
```

### Database Rollback

```bash
# Revert last migration
npm run db:migrate:undo

# Restore from backup
npm run db:restore -- --backup-id=xxx
```

## 📱 Post-Deployment

### Smoke Tests

```typescript
// tests/smoke/production.test.ts
import { test, expect } from '@playwright/test';

const PROD_URL = 'https://your-app.com';

test.describe('Production Smoke Tests', () => {
  test('homepage loads', async ({ page }) => {
    await page.goto(PROD_URL);
    await expect(page).toHaveTitle(/Your App/);
  });
  
  test('critical paths work', async ({ page }) => {
    // Test login
    await page.goto(`${PROD_URL}/login`);
    await expect(page.locator('form')).toBeVisible();
    
    // Test API
    const response = await page.request.get(`${PROD_URL}/api/health`);
    expect(response.ok()).toBeTruthy();
  });
});
```

### Monitoring Alerts

```typescript
// Set up alerts for:
// - Error rate > 1%
// - Response time > 3s
// - Failed deployments
// - Database connection issues
// - Memory usage > 80%
```

## 🎯 Production Checklist

### [Full Production Checklist](./PRODUCTION_CHECKLIST.md)

Quick checklist:
- [ ] Environment variables set
- [ ] Database migrations run
- [ ] SSL certificate active
- [ ] CDN configured
- [ ] Error tracking enabled
- [ ] Analytics configured
- [ ] Backups scheduled
- [ ] Monitoring alerts set
- [ ] Rate limiting active
- [ ] Security headers verified

## 📚 Platform-Specific Guides

- [Vercel Deployment Guide](./VERCEL_GUIDE.md)
- [AWS Deployment Guide](./AWS_GUIDE.md)
- [Docker Deployment Guide](./DOCKER_GUIDE.md)

## 🆘 Troubleshooting

### Common Issues

**Build Failures**
```bash
# Clear cache and rebuild
rm -rf .next
npm run build
```

**Environment Variables Missing**
```bash
# Verify all required vars
npm run env:check
```

**Database Connection Issues**
```bash
# Test connection
npm run db:test-connection
```

## 🔗 Related Documentation

- [Environment Variables](./ENVIRONMENT_VARIABLES.md)
- [CI/CD Setup](./CI_CD_SETUP.md)
- [Monitoring Guide](../monitoring/README.md)
- [Security Guide](../SECURITY_GUIDE.md)
