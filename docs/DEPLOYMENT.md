# Environment & Deployment Guide

## Overview

This boilerplate now includes comprehensive environment management for development, staging, and production deployments. All operations are environment-aware with safety checks and validation.

## Quick Start

```bash
# 1. Set up all environment files
npm run setup:env

# 2. Validate environment configuration  
npm run env:validate

# 3. Switch between environments
npm run env:switch staging

# 4. Start development server
npm run dev           # Development on :3000
npm run dev:staging   # Staging on :3001
```

## Environment Files

### Structure
```
.env.example       # Template with all variables
.env.development   # Local development
.env.staging       # Staging environment
.env.production    # Production environment
.env.local         # Active environment (git ignored)
```

### Key Differences

| Variable | Development | Staging | Production |
|----------|------------|---------|------------|
| NODE_ENV | development | staging | production |
| DEBUG_LOGS | true | true | false |
| API_TIMEOUT | 30000 | 30000 | 15000 |
| FEATURES | all enabled | most enabled | selective |

## Deployment Workflows

### Deploy to Staging

```bash
# Using chain (recommended)
/ssd  # or /safe-staging-deploy

# Manual steps
npm run build:staging
npm run deploy:staging
npm run smoke:staging
```

### Deploy to Production

```bash
# Using chain (recommended)
/spd  # or /safe-production-deploy

# Manual steps
npm run env:switch production
npm run build:production
npm run deploy:production
npm run smoke:production
```

## Environment-Aware Features

### 1. Hooks Protection

The system includes environment-aware hooks that:
- **Block destructive operations** in production
- **Warn about sensitive changes** in staging
- **Log all operations** by environment
- **Validate deployment readiness**

### 2. Database Safety

```typescript
// Migration script checks environment
if (isProduction) {
  // Requires confirmation
  // Creates backup
  // Logs operation
}
```

### 3. Feature Flags

```typescript
import { features } from '@/lib/env';

if (features.newCheckout) {
  // New checkout flow
}
```

### 4. Performance Budgets

Different limits per environment:
- **Development**: No limits
- **Staging**: 1MB bundle, 3s load
- **Production**: 500KB bundle, 2s load

## Deployment Checklist

### Pre-Deployment

- [ ] All tests passing
- [ ] No console.logs in code
- [ ] Environment variables set
- [ ] Database migrations ready
- [ ] Security scan passed
- [ ] Bundle size acceptable
- [ ] TypeScript compiles
- [ ] Lint checks pass

### Staging Deployment

1. **Validate**: `npm run env:validate`
2. **Build**: `npm run build:staging`
3. **Deploy**: `npm run deploy:staging`
4. **Test**: `npm run smoke:staging`
5. **Monitor**: Check logs and metrics

### Production Deployment

1. **Switch env**: `npm run env:switch production`
2. **Pre-check**: `npm run pre-deploy`
3. **Preview**: `npm run preview`
4. **Deploy**: `npm run deploy:production`
5. **Verify**: `npm run smoke:production`
6. **Monitor**: Watch metrics closely

## Emergency Procedures

### Rollback

```bash
# Quick rollback using chain
/rb  # or /rollback-deployment

# Manual rollback
vercel rollback
npm run smoke:production
```

### Database Rollback

```bash
# Restore from backup
psql $DATABASE_URL < backups/backup-[timestamp].sql
```

## Configuration Reference

### Environment Variables

See `.env.example` for complete list with descriptions.

### Type-Safe Access

```typescript
import { env, isDevelopment, isProduction } from '@/lib/env';

// Validated and typed
console.log(env.DATABASE_URL);

// Environment checks
if (isProduction) {
  // Production-only code
}
```

### Configuration Module

```typescript
import config from '@/config';

// Access configuration
const apiUrl = config.api.url;
const timeout = config.api.timeout;

// Check features
if (config.features.analytics) {
  // Track event
}
```

## Team Collaboration

### Setting Up New Developer

1. Clone repository
2. Run `npm run setup:env`
3. Get environment values from team lead
4. Update `.env.development` with values
5. Run `npm run env:validate`

### Sharing Staging

- Staging URL: `https://staging.yourapp.com`
- All team members can deploy to staging
- Automatic notifications on deployment

### Production Access

- Limited to authorized developers
- Requires confirmation at multiple steps
- All deployments logged

## Monitoring & Observability

### Logs by Environment

```
.claude/logs/environments/
├── development-operations.log
├── staging-operations.log
└── production-operations.log
```

### Deployment Reports

```
.claude/deployment/
├── pre-deploy-report-[timestamp].json
└── deployment-history.json
```

## Best Practices

1. **Always validate** before deployment
2. **Test in staging** before production
3. **Monitor after deployment**
4. **Keep backups** of production data
5. **Document changes** in deployment notes
6. **Notify team** of production deployments

## Troubleshooting

### Environment not switching
```bash
# Check current environment
echo $NODE_ENV

# Force reload
source ~/.bashrc  # or ~/.zshrc
```

### Build failures
```bash
# Clear cache and rebuild
npm run clean:cache
npm run build:staging
```

### Connection errors
```bash
# Validate all services accessible
npm run env:validate
npm run db:test
```

## Integration with CI/CD

### GitHub Actions
```yaml
env:
  NODE_ENV: ${{ github.ref == 'refs/heads/main' && 'production' || 'staging' }}
```

### Vercel
- Environment variables set per branch
- Preview deployments use staging config
- Production deployments require approval

This environment system ensures safe, predictable deployments while maintaining development velocity.
