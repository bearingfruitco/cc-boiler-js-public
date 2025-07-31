# Environment Variables Guide

> Complete reference for all environment variables in Claude Code Boilerplate

## 🎯 Overview

Environment variables configure your application for different environments (development, staging, production). This guide covers all variables, their purposes, and security considerations.

## 📋 Complete Variable Reference

### Core Application

```env
# Application URL (required)
NEXT_PUBLIC_APP_URL=https://your-domain.com
# Used for: Canonical URLs, redirects, OAuth callbacks

# Application Name (optional)
NEXT_PUBLIC_APP_NAME="Claude App"
# Default: "Claude App"
# Used for: Page titles, emails, metadata

# Node Environment (required)
NODE_ENV=production
# Options: development, test, production
# Used for: Optimizations, error handling, logging
```

### Database Configuration

```env
# Primary Database URL (required)
DATABASE_URL=postgresql://user:password@host:5432/database?sslmode=require
# Format: postgresql://[user]:[password]@[host]:[port]/[database]?[params]

# Pooled Connection URL (recommended for serverless)
DATABASE_POOL_URL=postgresql://user:password@host:5432/database?sslmode=require&pgbouncer=true
# Used for: Serverless functions, edge runtime

# Database SSL Certificate (if required)
DATABASE_SSL_CERT="-----BEGIN CERTIFICATE-----..."
# Used for: Secure database connections
```

### Authentication

```env
# NextAuth Configuration (required)
NEXTAUTH_URL=https://your-domain.com
# Must match NEXT_PUBLIC_APP_URL in production

NEXTAUTH_SECRET=your-secret-key-min-32-chars
# Generate: openssl rand -base64 32
# Used for: JWT encryption, CSRF protection

# OAuth Providers (optional)
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxx

GITHUB_CLIENT_ID=xxx
GITHUB_CLIENT_SECRET=xxx

# Email Provider (optional)
EMAIL_SERVER_HOST=smtp.sendgrid.net
EMAIL_SERVER_PORT=587
EMAIL_SERVER_USER=apikey
EMAIL_SERVER_PASSWORD=xxx
EMAIL_FROM=noreply@your-domain.com
```

### Supabase Integration

```env
# Supabase Project URL (required if using Supabase)
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
# Found in: Project Settings > API

# Supabase Anonymous Key (required)
NEXT_PUBLIC_SUPABASE_ANON_KEY=xxx
# Found in: Project Settings > API > anon key
# Safe to expose, RLS provides security

# Supabase Service Role Key (required, keep secret!)
SUPABASE_SERVICE_ROLE_KEY=xxx
# Found in: Project Settings > API > service_role key
# NEVER expose to client
```

### Analytics & Monitoring

```env
# Analytics (optional)
NEXT_PUBLIC_ANALYTICS_ID=G-XXXXXXXXXX
# Google Analytics, Plausible, etc.

NEXT_PUBLIC_ENABLE_ANALYTICS=true
# Toggle analytics on/off

# Error Tracking - Sentry (optional)
NEXT_PUBLIC_SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx
# Public DSN for client-side errors

SENTRY_ORG=your-org
SENTRY_PROJECT=your-project
SENTRY_AUTH_TOKEN=xxx
# For source maps upload during build

# Performance Monitoring
NEXT_PUBLIC_ENABLE_WEB_VITALS=true
```

### External Services

```env
# Payment Processing - Stripe (optional)
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_xxx

# File Storage - AWS S3 (optional)
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_REGION=us-east-1
AWS_S3_BUCKET=your-bucket

# Email Service - SendGrid (optional)
SENDGRID_API_KEY=SG.xxx
SENDGRID_FROM_EMAIL=hello@your-domain.com

# SMS Service - Twilio (optional)
TWILIO_ACCOUNT_SID=xxx
TWILIO_AUTH_TOKEN=xxx
TWILIO_PHONE_NUMBER=+1234567890
```

### Feature Flags

```env
# Feature Toggles
NEXT_PUBLIC_FEATURE_NEW_UI=true
NEXT_PUBLIC_FEATURE_BETA_API=false
NEXT_PUBLIC_FEATURE_MAINTENANCE_MODE=false

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# Security Features
ENABLE_SECURITY_HEADERS=true
ENABLE_RATE_LIMITING=true
ENABLE_CSRF_PROTECTION=true
```

### Development & Testing

```env
# Development Tools
NEXT_PUBLIC_DEV_TOOLS=true
ANALYZE_BUNDLE=false
ENABLE_SOURCE_MAPS=true

# Testing
TEST_DATABASE_URL=postgresql://test:test@localhost:5432/test
E2E_TEST_BASE_URL=http://localhost:3000
PLAYWRIGHT_HEADLESS=true

# CI/CD
CI=true
VERCEL_ENV=production
VERCEL_URL=xxx.vercel.app
```

## 🔒 Security Best Practices

### Variable Naming Convention

```env
# Public variables (exposed to browser)
NEXT_PUBLIC_*=value

# Server-only variables (kept secret)
SECRET_*=value
*_SECRET=value
*_KEY=value
```

### Never Commit These

```gitignore
# .gitignore
.env
.env.local
.env.production
.env.*.local

# Only commit
.env.example
.env.test
```

### Secure Storage

1. **Local Development**: Use `.env.local`
2. **CI/CD**: Use encrypted secrets
3. **Production**: Use platform environment variables
4. **Never**: Store in code or version control

## 📁 Environment File Structure

```
project/
├── .env.example          # Template with all variables
├── .env.local           # Local development (gitignored)
├── .env.development     # Development defaults
├── .env.test           # Test environment
├── .env.staging        # Staging environment
└── .env.production     # Production (gitignored)
```

### .env.example Template

```env
# Copy this to .env.local and fill in values

# Required
DATABASE_URL=
NEXTAUTH_SECRET=
NEXT_PUBLIC_APP_URL=

# Supabase (if using)
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Optional Services
# STRIPE_SECRET_KEY=
# SENDGRID_API_KEY=
# NEXT_PUBLIC_SENTRY_DSN=
```

## 🔧 Loading Environment Variables

### Runtime Access

```typescript
// lib/env.ts
export const env = {
  // Required variables with validation
  database: {
    url: process.env.DATABASE_URL!,
    poolUrl: process.env.DATABASE_POOL_URL,
  },
  
  auth: {
    url: process.env.NEXTAUTH_URL!,
    secret: process.env.NEXTAUTH_SECRET!,
  },
  
  // Optional with defaults
  app: {
    url: process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000',
    name: process.env.NEXT_PUBLIC_APP_NAME || 'Claude App',
  },
  
  // Feature flags
  features: {
    analytics: process.env.NEXT_PUBLIC_ENABLE_ANALYTICS === 'true',
    maintenance: process.env.NEXT_PUBLIC_FEATURE_MAINTENANCE_MODE === 'true',
  },
};

// Validate on startup
if (!env.database.url) {
  throw new Error('DATABASE_URL is required');
}
```

### Client-Side Access

```typescript
// Only NEXT_PUBLIC_* variables
export const publicEnv = {
  appUrl: process.env.NEXT_PUBLIC_APP_URL!,
  supabaseUrl: process.env.NEXT_PUBLIC_SUPABASE_URL!,
  supabaseAnonKey: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
};
```

## 🚀 Platform-Specific Setup

### Vercel

```bash
# Set via CLI
vercel env add DATABASE_URL production

# Or via dashboard
# Project Settings > Environment Variables
```

### Heroku

```bash
heroku config:set DATABASE_URL=xxx
heroku config:set NEXTAUTH_SECRET=xxx
```

### Docker

```dockerfile
# Dockerfile
ARG DATABASE_URL
ENV DATABASE_URL=$DATABASE_URL
```

```yaml
# docker-compose.yml
services:
  app:
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
```

## ✅ Validation Script

```typescript
// scripts/validate-env.ts
const required = [
  'DATABASE_URL',
  'NEXTAUTH_SECRET',
  'NEXT_PUBLIC_APP_URL',
];

const missing = required.filter(key => !process.env[key]);

if (missing.length > 0) {
  console.error('❌ Missing required environment variables:');
  missing.forEach(key => console.error(`   - ${key}`));
  process.exit(1);
}

console.log('✅ All required environment variables are set');
```

## 🔄 Environment Switching

```typescript
// lib/config/env-switcher.ts
export function getApiUrl() {
  switch (process.env.VERCEL_ENV) {
    case 'production':
      return 'https://api.production.com';
    case 'preview':
      return 'https://api.staging.com';
    default:
      return 'http://localhost:3001';
  }
}
```

## 📊 Monitoring Environment Health

```typescript
// app/api/health/route.ts
export async function GET() {
  const checks = {
    database: await checkDatabase(),
    auth: !!process.env.NEXTAUTH_SECRET,
    supabase: await checkSupabase(),
    required_vars: checkRequiredVars(),
  };
  
  const healthy = Object.values(checks).every(Boolean);
  
  return NextResponse.json({
    status: healthy ? 'healthy' : 'unhealthy',
    checks,
    timestamp: new Date().toISOString(),
  });
}
```

## 🆘 Troubleshooting

### Variable Not Loading

```bash
# Debug loading
console.log('All env vars:', Object.keys(process.env));

# Check spelling and casing
DATABASE_URL ✅
database_url ❌
```

### Different Values in Production

```bash
# Verify deployed values
vercel env pull
cat .env.production.local
```

### Build vs Runtime

```typescript
// Build-time (baked into code)
const buildTime = process.env.NEXT_PUBLIC_BUILD_TIME;

// Runtime (can change)
const runtime = process.env.RUNTIME_SECRET;
```

## 📚 Related Documentation

- [Deployment Guide](./README.md)
- [Vercel Environment Variables](https://vercel.com/docs/environment-variables)
- [Next.js Environment Variables](https://nextjs.org/docs/basic-features/environment-variables)
