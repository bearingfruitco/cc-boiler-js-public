# Vercel Deployment Guide

> Comprehensive guide for deploying Claude Code Boilerplate to Vercel with edge optimization, preview deployments, and production best practices.

## ? Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Environment Configuration](#environment-configuration)
4. [Deployment Process](#deployment-process)
5. [Custom Domain Setup](#custom-domain-setup)
6. [Edge Functions](#edge-functions)
7. [Cron Jobs](#cron-jobs)
8. [Preview Deployments](#preview-deployments)
9. [Performance Optimization](#performance-optimization)
10. [Monitoring & Analytics](#monitoring--analytics)
11. [Rollback Procedures](#rollback-procedures)
12. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Accounts
- **Vercel Account**: [Sign up at vercel.com](https://vercel.com/signup)
- **GitHub Account**: Repository must be on GitHub
- **Supabase Account**: For database (or your chosen provider)

### Local Requirements
```bash
# Verify installations
node --version  # v18+ required
npm --version   # v8+ required
git --version   # Any recent version

# Install Vercel CLI (optional but recommended)
npm i -g vercel
```

### Repository Setup
- Repository must be pushed to GitHub
- Main branch should be production-ready
- `.gitignore` properly configured
- Environment variables documented

## Initial Setup

### 1. Connect GitHub to Vercel

1. **Log in to Vercel Dashboard**
   ```
   https://vercel.com/dashboard
   ```

2. **Import Project**
   - Click "New Project"
   - Select "Import Git Repository"
   - Authorize GitHub if needed
   - Select your repository

3. **Configure Project**
   ```
   Framework Preset: Next.js
   Root Directory: ./
   Build Command: npm run build
   Output Directory: .next
   Install Command: npm install
   ```

### 2. Initial Configuration

```bash
# Using Vercel CLI
vercel

# Follow prompts:
# - Set up and deploy: Y
# - Which scope: Select your team/personal
# - Link to existing project: N (first time)
# - Project name: your-project-name
# - Directory: ./
# - Override settings: N
```

## Environment Configuration

### 1. Required Environment Variables

Create these in Vercel Dashboard ? Project ? Settings ? Environment Variables:

```bash
# Database (Supabase)
DATABASE_URL="postgresql://..."
NEXT_PUBLIC_SUPABASE_URL="https://xxx.supabase.co"
NEXT_PUBLIC_SUPABASE_ANON_KEY="eyJ..."
SUPABASE_SERVICE_ROLE_KEY="eyJ..."

# App Configuration
NEXT_PUBLIC_APP_URL="https://yourdomain.com"
NEXTAUTH_URL="https://yourdomain.com"
NEXTAUTH_SECRET="generate-with-openssl-rand-base64-32"

# Optional Services
NEXT_PUBLIC_SENTRY_DSN="https://...@sentry.io/..."
SENTRY_AUTH_TOKEN="..."
NEXT_PUBLIC_RUDDERSTACK_KEY="..."
NEXT_PUBLIC_RUDDERSTACK_URL="..."

# Feature Flags
NEXT_PUBLIC_FEATURES_AUTH="true"
NEXT_PUBLIC_FEATURES_ANALYTICS="true"
```

### 2. Environment-Specific Variables

Set different values per environment:

| Variable | Development | Preview | Production |
|----------|------------|---------|------------|
| `NEXT_PUBLIC_APP_URL` | `http://localhost:3000` | `https://[branch]-[project].vercel.app` | `https://yourdomain.com` |
| `DATABASE_URL` | Dev DB | Preview DB | Production DB |
| `NEXT_PUBLIC_FEATURES_*` | All enabled | Most enabled | Selective |

### 3. Secret Management

```bash
# Add secrets via CLI
vercel env add DATABASE_URL production
vercel env add SUPABASE_SERVICE_ROLE_KEY production

# Pull to local .env
vercel env pull .env.local
```

## Deployment Process

### 1. Production Deployment

#### Via GitHub (Recommended)
```bash
# Ensure main branch is ready
git checkout main
git pull origin main

# Run pre-deployment checks
npm run lint
npm run test
npm run build

# Deploy
git push origin main
# Vercel auto-deploys from main branch
```

#### Via CLI
```bash
# Deploy to production
vercel --prod

# Deploy with specific configuration
vercel --prod --build-env NODE_ENV=production
```

### 2. Build Configuration

Create `vercel.json` for custom configuration:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "regions": ["iad1"],
  "functions": {
    "app/api/heavy-computation/route.ts": {
      "maxDuration": 60
    }
  },
  "crons": [
    {
      "path": "/api/cron/daily-cleanup",
      "schedule": "0 0 * * *"
    }
  ],
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "s-maxage=60, stale-while-revalidate"
        }
      ]
    }
  ],
  "rewrites": [
    {
      "source": "/blog/:path*",
      "destination": "https://blog.example.com/:path*"
    }
  ]
}
```

### 3. Build Optimizations

```javascript
// next.config.js
module.exports = {
  images: {
    domains: ['yourdomain.com'],
    formats: ['image/avif', 'image/webp'],
  },
  experimental: {
    optimizeCss: true,
  },
  swcMinify: true,
  compress: true,
  poweredByHeader: false,
  generateEtags: true,
}
```

## Custom Domain Setup

### 1. Add Domain to Vercel

1. **Navigate to Domains**
   ```
   Project ? Settings ? Domains
   ```

2. **Add Domain**
   ```
   yourdomain.com
   www.yourdomain.com (redirect to apex)
   ```

3. **Configure DNS**

   **Option A: Vercel Nameservers (Recommended)**
   ```
   ns1.vercel-dns.com
   ns2.vercel-dns.com
   ```

   **Option B: A Record**
   ```
   Type: A
   Name: @
   Value: 76.76.21.21
   ```

   **Option C: CNAME (for subdomains)**
   ```
   Type: CNAME
   Name: app
   Value: cname.vercel-dns.com
   ```

### 2. SSL Configuration

- Automatic SSL provisioning via Let's Encrypt
- Force HTTPS in project settings
- HSTS headers automatically added

### 3. Domain Verification

```bash
# Check DNS propagation
dig yourdomain.com

# Verify SSL
curl -I https://yourdomain.com
```

## Edge Functions

### 1. Edge Configuration

```typescript
// app/api/edge-function/route.ts
import { NextRequest } from 'next/server';

export const runtime = 'edge'; // Enable edge runtime
export const dynamic = 'force-dynamic';

export async function GET(request: NextRequest) {
  // Runs at edge locations globally
  const country = request.geo?.country || 'US';
  
  return new Response(JSON.stringify({
    message: `Hello from ${country}`,
    region: request.geo?.region,
    city: request.geo?.city,
  }), {
    headers: {
      'content-type': 'application/json',
      'cache-control': 'max-age=60',
    },
  });
}
```

### 2. Edge Middleware

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Run on edge before route handlers
  const country = request.geo?.country || 'US';
  
  // Add geo headers
  const response = NextResponse.next();
  response.headers.set('x-user-country', country);
  
  // Redirect based on location
  if (country === 'CN' && request.nextUrl.pathname === '/') {
    return NextResponse.redirect(new URL('/cn', request.url));
  }
  
  return response;
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
};
```

### 3. Regional Deployments

```json
// vercel.json
{
  "regions": ["iad1", "sfo1", "fra1", "sin1"],
  "functions": {
    "app/api/compute-heavy/route.ts": {
      "regions": ["iad1"],
      "maxDuration": 300
    }
  }
}
```

## Cron Jobs

### 1. Define Cron Jobs

```json
// vercel.json
{
  "crons": [
    {
      "path": "/api/cron/hourly-sync",
      "schedule": "0 * * * *"
    },
    {
      "path": "/api/cron/daily-cleanup",
      "schedule": "0 0 * * *"
    },
    {
      "path": "/api/cron/weekly-report",
      "schedule": "0 0 * * 0"
    }
  ]
}
```

### 2. Implement Cron Handlers

```typescript
// app/api/cron/daily-cleanup/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { headers } from 'next/headers';

export async function GET(request: NextRequest) {
  // Verify cron secret
  const authHeader = headers().get('authorization');
  if (authHeader !== `Bearer ${process.env.CRON_SECRET}`) {
    return new Response('Unauthorized', { status: 401 });
  }
  
  try {
    // Perform cleanup
    await cleanupOldSessions();
    await purgeExpiredTokens();
    await archiveOldLogs();
    
    return NextResponse.json({
      success: true,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error('Cron job failed:', error);
    return NextResponse.json(
      { error: 'Cleanup failed' },
      { status: 500 }
    );
  }
}
```

### 3. Monitor Cron Jobs

- View execution logs in Vercel Dashboard
- Set up alerts for failures
- Track execution times

## Preview Deployments

### 1. Automatic Preview Deployments

Every push to a non-production branch creates a preview:

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and push
git add .
git commit -m "feat: add new feature"
git push origin feature/new-feature

# Preview URL format:
# https://your-project-git-feature-new-feature-your-team.vercel.app
```

### 2. Preview Environment Variables

Set preview-specific variables:

```bash
# Via Dashboard
# Settings ? Environment Variables ? Preview

# Via CLI
vercel env add DATABASE_URL preview
```

### 3. Preview Protection

```typescript
// middleware.ts - Password protect previews
export function middleware(request: NextRequest) {
  const isPreview = process.env.VERCEL_ENV === 'preview';
  
  if (isPreview) {
    const basicAuth = request.headers.get('authorization');
    
    if (!basicAuth || !verifyAuth(basicAuth)) {
      return new Response('Authentication required', {
        status: 401,
        headers: {
          'WWW-Authenticate': 'Basic realm="Secure Preview"',
        },
      });
    }
  }
  
  return NextResponse.next();
}
```

## Performance Optimization

### 1. Image Optimization

```typescript
// next.config.js
module.exports = {
  images: {
    loader: 'default',
    domains: ['yourdomain.com'],
    deviceSizes: [640, 750, 828, 1080, 1200],
    imageSizes: [16, 32, 48, 64, 96],
    formats: ['image/avif', 'image/webp'],
    minimumCacheTTL: 60,
  },
};
```

### 2. Caching Strategy

```typescript
// app/api/data/route.ts
export async function GET() {
  const data = await fetchData();
  
  return NextResponse.json(data, {
    headers: {
      'Cache-Control': 's-maxage=60, stale-while-revalidate=300',
      'CDN-Cache-Control': 'max-age=3600',
    },
  });
}
```

### 3. Bundle Analysis

```bash
# Install analyzer
npm install --save-dev @next/bundle-analyzer

# Configure
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
  // your config
});

# Run analysis
ANALYZE=true npm run build
```

### 4. Web Vitals Monitoring

```typescript
// app/layout.tsx
export function reportWebVitals(metric: any) {
  // Send to analytics
  window.analytics?.track('Web Vitals', {
    metric: metric.name,
    value: metric.value,
    label: metric.id,
  });
  
  // Log poor performance
  if (metric.name === 'CLS' && metric.value > 0.1) {
    console.warn('Poor CLS:', metric);
  }
}
```

## Monitoring & Analytics

### 1. Vercel Analytics

```bash
# Install
npm install @vercel/analytics

# Add to layout
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

### 2. Speed Insights

```bash
# Install
npm install @vercel/speed-insights

# Add to layout
import { SpeedInsights } from '@vercel/speed-insights/next';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <SpeedInsights />
      </body>
    </html>
  );
}
```

### 3. Custom Monitoring

```typescript
// lib/monitoring.ts
export function trackDeployment() {
  const deploymentId = process.env.VERCEL_DEPLOYMENT_ID;
  const gitCommit = process.env.VERCEL_GIT_COMMIT_SHA;
  
  // Send to monitoring service
  fetch('https://monitoring.example.com/deployment', {
    method: 'POST',
    body: JSON.stringify({
      deploymentId,
      gitCommit,
      timestamp: new Date().toISOString(),
      environment: process.env.VERCEL_ENV,
    }),
  });
}
```

## Rollback Procedures

### 1. Instant Rollback

Via Dashboard:
1. Go to Deployments tab
2. Find last working deployment
3. Click "..." ? "Promote to Production"
4. Confirm promotion

Via CLI:
```bash
# List recent deployments
vercel list

# Promote specific deployment
vercel promote [deployment-url]
```

### 2. Git-based Rollback

```bash
# Find last good commit
git log --oneline -10

# Revert to commit
git revert HEAD
git push origin main

# Or reset (careful!)
git reset --hard [commit-hash]
git push origin main --force
```

### 3. Rollback Checklist

- [ ] Identify issue in production
- [ ] Find last stable deployment
- [ ] Notify team of rollback
- [ ] Execute rollback
- [ ] Verify rollback success
- [ ] Create incident report
- [ ] Fix issue in development
- [ ] Test thoroughly
- [ ] Re-deploy with fix

## Troubleshooting

### Common Issues

#### 1. Build Failures

**Error**: "Module not found"
```bash
# Clear cache and rebuild
vercel --force

# Check package.json
npm list [missing-module]
npm install [missing-module]
```

**Error**: "Out of memory"
```json
// vercel.json
{
  "functions": {
    "app/api/heavy/route.ts": {
      "memory": 3008
    }
  }
}
```

#### 2. Environment Variable Issues

**Missing Variables**
```bash
# List all env vars
vercel env ls

# Pull to check
vercel env pull .env.check

# Add missing
vercel env add KEY_NAME production
```

**Wrong Environment**
```typescript
// Debug helper
console.log({
  env: process.env.VERCEL_ENV,
  url: process.env.VERCEL_URL,
  region: process.env.VERCEL_REGION,
});
```

#### 3. Domain Issues

**SSL Certificate Pending**
- Wait 10-15 minutes for provisioning
- Check DNS propagation
- Verify domain ownership

**Redirect Loops**
```typescript
// Check middleware
if (request.nextUrl.pathname === '/redirect-target') {
  // Prevent infinite loop
  return NextResponse.next();
}
```

#### 4. Performance Issues

**Slow Cold Starts**
- Use Edge Functions for critical paths
- Optimize bundle size
- Reduce dependencies

**High Latency**
- Deploy to multiple regions
- Use CDN for static assets
- Implement caching

### Debug Mode

```bash
# Enable debug logs
DEBUG=* vercel

# Verbose output
vercel --debug

# Check function logs
vercel logs [deployment-url]
```

### Support Resources

- **Vercel Documentation**: https://vercel.com/docs
- **Next.js on Vercel**: https://vercel.com/docs/frameworks/nextjs
- **Status Page**: https://www.vercel-status.com/
- **Support**: https://vercel.com/support

## Best Practices

1. **Use Preview Deployments** - Test every change
2. **Monitor Performance** - Set up alerts
3. **Implement Caching** - Reduce load and costs
4. **Secure Secrets** - Never commit env vars
5. **Automate Tests** - Run in CI/CD
6. **Document Changes** - Update deployment docs
7. **Plan Rollbacks** - Know your recovery plan
8. **Scale Gradually** - Monitor as you grow

## Summary

Vercel provides a powerful platform for deploying Next.js applications with:
- Automatic deployments from Git
- Global edge network
- Built-in performance optimization
- Easy rollback capabilities
- Comprehensive monitoring

Follow this guide for a smooth deployment experience and optimal performance in production.
