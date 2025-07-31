# Production Deployment Checklist

> Comprehensive checklist to ensure safe, secure, and successful production deployments of Claude Code Boilerplate applications.

## ? Table of Contents

1. [Pre-Deployment Checks](#pre-deployment-checks)
2. [Security Audit](#security-audit)
3. [Performance Validation](#performance-validation)
4. [Database Preparation](#database-preparation)
5. [Environment Setup](#environment-setup)
6. [Deployment Steps](#deployment-steps)
7. [Post-Deployment Verification](#post-deployment-verification)
8. [Monitoring Setup](#monitoring-setup)
9. [Rollback Plan](#rollback-plan)
10. [Documentation Updates](#documentation-updates)

## Pre-Deployment Checks

### Code Quality
- [ ] All tests passing (`npm test`)
- [ ] No TypeScript errors (`npm run typecheck`)
- [ ] Linting passes (`npm run lint`)
- [ ] Build succeeds (`npm run build`)
- [ ] No console.log statements in production code
- [ ] No commented-out code blocks
- [ ] No TODO comments in critical paths

### Design System Compliance
- [ ] Run `/vd all --strict`
- [ ] All components use approved typography (text-size-[1-4])
- [ ] All spacing follows 4px grid
- [ ] Touch targets meet 44px minimum
- [ ] Color contrast passes WCAG AA

### Test Coverage
- [ ] Unit test coverage > 80%
- [ ] All critical paths have E2E tests
- [ ] Integration tests for API endpoints
- [ ] Performance tests pass budgets
- [ ] Visual regression tests updated

### Dependencies
- [ ] No security vulnerabilities (`npm audit`)
- [ ] All dependencies up to date
- [ ] Lock file committed (`package-lock.json`)
- [ ] No unused dependencies
- [ ] License compliance verified

## Security Audit

### Authentication & Authorization
- [ ] JWT secrets are strong and unique
- [ ] Session management implemented correctly
- [ ] Password policies enforced
- [ ] MFA available for admin accounts
- [ ] OAuth providers configured correctly

### API Security
- [ ] All endpoints require authentication (except public)
- [ ] Rate limiting configured
- [ ] CORS properly configured
- [ ] Input validation on all endpoints
- [ ] SQL injection protection verified
- [ ] XSS protection implemented

### Data Protection
- [ ] PII fields encrypted at rest
- [ ] PII fields masked in logs
- [ ] GDPR compliance verified
- [ ] Data retention policies implemented
- [ ] Backup encryption enabled

### Infrastructure Security
- [ ] SSL/TLS certificates valid
- [ ] Security headers configured
- [ ] Secrets stored in environment variables
- [ ] No hardcoded credentials
- [ ] Database access restricted
- [ ] CDN security settings enabled

### Compliance
- [ ] GDPR requirements met
- [ ] CCPA requirements met
- [ ] TCPA compliance for communications
- [ ] Privacy policy updated
- [ ] Terms of service updated
- [ ] Cookie consent implemented

## Performance Validation

### Core Web Vitals
- [ ] LCP < 2.5s
- [ ] FID < 100ms
- [ ] CLS < 0.1
- [ ] TTFB < 600ms

### Bundle Size
- [ ] JavaScript bundle < 200KB (gzipped)
- [ ] CSS bundle < 50KB (gzipped)
- [ ] Image optimization enabled
- [ ] Code splitting implemented
- [ ] Tree shaking verified

### API Performance
- [ ] Response times < 200ms (p95)
- [ ] Database queries optimized
- [ ] N+1 queries eliminated
- [ ] Caching strategy implemented
- [ ] CDN configured for static assets

### Load Testing
- [ ] Load tests pass (100 concurrent users)
- [ ] No memory leaks detected
- [ ] Database connection pooling works
- [ ] Auto-scaling configured (if applicable)

## Database Preparation

### Schema Updates
- [ ] Migrations tested in staging
- [ ] Rollback scripts prepared
- [ ] Schema changes backward compatible
- [ ] Indexes optimized for production load
- [ ] Foreign key constraints verified

### Data Migration
- [ ] Data migration scripts tested
- [ ] Backup taken before migration
- [ ] Migration time estimated
- [ ] Downtime window communicated
- [ ] Data integrity checks prepared

### Backup & Recovery
- [ ] Automated backups configured
- [ ] Backup retention policy set
- [ ] Recovery procedure tested
- [ ] Point-in-time recovery available
- [ ] Backup monitoring enabled

## Environment Setup

### Environment Variables
```bash
# Required for Production
- [ ] DATABASE_URL
- [ ] NEXT_PUBLIC_APP_URL
- [ ] NEXTAUTH_URL
- [ ] NEXTAUTH_SECRET
- [ ] NEXT_PUBLIC_SUPABASE_URL
- [ ] NEXT_PUBLIC_SUPABASE_ANON_KEY
- [ ] SUPABASE_SERVICE_ROLE_KEY

# Optional but Recommended
- [ ] SENTRY_DSN
- [ ] SENTRY_AUTH_TOKEN
- [ ] RUDDERSTACK_KEY
- [ ] SMTP_HOST
- [ ] SMTP_USER
- [ ] SMTP_PASS
```

### Infrastructure Configuration
- [ ] Domain DNS configured
- [ ] SSL certificates installed
- [ ] CDN endpoints configured
- [ ] Load balancer health checks
- [ ] Auto-scaling policies set
- [ ] Firewall rules configured

### Third-Party Services
- [ ] Payment processor production keys
- [ ] Email service configured
- [ ] Analytics tracking enabled
- [ ] Error tracking enabled
- [ ] Log aggregation configured
- [ ] Monitoring alerts set

## Deployment Steps

### 1. Final Checks
```bash
# Run all checks
npm run predeploy

# Verify environment
./scripts/verify-production-env.sh

# Check dependencies
npm audit --production
```

### 2. Database Migration
```bash
# Backup production database
npm run db:backup:prod

# Run migrations
npm run db:migrate:prod

# Verify migration
npm run db:verify:prod
```

### 3. Deploy Application

#### Vercel Deployment
```bash
# Deploy to production
vercel --prod

# Or via Git
git push origin main
```

#### Manual Deployment
```bash
# Build application
npm run build

# Upload to server
rsync -avz .next/ user@server:/app/.next/

# Restart services
ssh user@server 'pm2 restart all'
```

### 4. Cache Warming
```bash
# Warm critical paths
./scripts/warm-cache.sh

# Preload static assets
./scripts/preload-cdn.sh
```

## Post-Deployment Verification

### Smoke Tests
- [ ] Homepage loads successfully
- [ ] Login/logout works
- [ ] Critical user paths function
- [ ] API health check passes
- [ ] Database connectivity verified
- [ ] Third-party integrations work

### Performance Checks
- [ ] Page load times acceptable
- [ ] API response times normal
- [ ] No JavaScript errors in console
- [ ] Images loading correctly
- [ ] CDN serving assets
- [ ] SSL certificate valid

### Functionality Tests
- [ ] Forms submit correctly
- [ ] Email notifications sending
- [ ] Payment processing works
- [ ] Search functionality works
- [ ] File uploads working
- [ ] Real-time features functional

### SEO & Analytics
- [ ] Robots.txt accessible
- [ ] Sitemap.xml generated
- [ ] Meta tags present
- [ ] Analytics tracking events
- [ ] Google Search Console verified
- [ ] Social media cards working

## Monitoring Setup

### Application Monitoring
- [ ] APM tool configured (e.g., New Relic, DataDog)
- [ ] Error tracking active (Sentry)
- [ ] Custom metrics defined
- [ ] Performance budgets set
- [ ] Uptime monitoring enabled

### Infrastructure Monitoring
- [ ] Server metrics tracked
- [ ] Database performance monitored
- [ ] CDN performance tracked
- [ ] SSL certificate expiry alerts
- [ ] Disk space alerts configured

### Business Metrics
- [ ] Conversion tracking enabled
- [ ] User journey analytics set
- [ ] Revenue tracking configured
- [ ] Custom events defined
- [ ] Dashboard created

### Alerting
- [ ] Critical error alerts to Slack/Email
- [ ] Performance degradation alerts
- [ ] Security incident alerts
- [ ] Downtime alerts configured
- [ ] On-call rotation set

## Rollback Plan

### Preparation
- [ ] Previous version tagged in Git
- [ ] Database rollback script ready
- [ ] Previous deployment URL saved
- [ ] Team notified of deployment
- [ ] Rollback decision criteria defined

### Rollback Triggers
- [ ] Error rate > 5%
- [ ] Response time > 2x normal
- [ ] Critical functionality broken
- [ ] Security vulnerability discovered
- [ ] Data corruption detected

### Rollback Procedure
```bash
# 1. Immediate rollback (Vercel)
vercel rollback

# 2. Git-based rollback
git revert HEAD
git push origin main

# 3. Database rollback
npm run db:rollback:prod

# 4. Clear caches
./scripts/clear-all-caches.sh

# 5. Notify team
./scripts/notify-rollback.sh
```

### Post-Rollback
- [ ] Verify application stability
- [ ] Check data integrity
- [ ] Document incident
- [ ] Schedule retrospective
- [ ] Create fix for issue

## Documentation Updates

### Technical Documentation
- [ ] API documentation updated
- [ ] Database schema documented
- [ ] Deployment guide updated
- [ ] Environment variables documented
- [ ] Architecture diagrams current

### User Documentation
- [ ] User guides updated
- [ ] FAQ updated
- [ ] Help videos current
- [ ] Release notes published
- [ ] Known issues documented

### Internal Documentation
- [ ] Runbooks updated
- [ ] Incident response plan current
- [ ] Team contacts updated
- [ ] Escalation procedures defined
- [ ] SLAs documented

## Final Checklist

### Communication
- [ ] Deployment schedule communicated
- [ ] Maintenance window announced
- [ ] Support team briefed
- [ ] Customers notified (if needed)
- [ ] Success criteria defined

### Legal & Compliance
- [ ] Privacy policy version updated
- [ ] Terms of service reviewed
- [ ] Compliance audit trail created
- [ ] Data processing agreements current
- [ ] Security audit completed

### Business Readiness
- [ ] Customer support prepared
- [ ] Marketing materials updated
- [ ] Sales team briefed
- [ ] Pricing changes implemented
- [ ] Feature flags configured

## Post-Deployment Tasks

### Immediate (0-1 hour)
- [ ] Monitor error rates
- [ ] Check performance metrics
- [ ] Verify critical paths
- [ ] Review user feedback
- [ ] Check system resources

### Short-term (1-24 hours)
- [ ] Analyze user behavior
- [ ] Review performance trends
- [ ] Check for security alerts
- [ ] Gather team feedback
- [ ] Document any issues

### Long-term (1-7 days)
- [ ] Conduct retrospective
- [ ] Update documentation
- [ ] Plan improvements
- [ ] Share learnings
- [ ] Celebrate success! ?

## Emergency Contacts

```
On-Call Engineer: ____________
DevOps Lead: ________________
Security Team: ______________
Database Admin: _____________
Product Manager: ____________
```

## Sign-offs

- [ ] Engineering Lead: ___________
- [ ] Security Review: ___________
- [ ] QA Lead: __________________
- [ ] Product Manager: __________
- [ ] DevOps: __________________

---

**Remember**: A successful deployment is a boring deployment. If everything goes according to plan, that's perfect!

**Pro tip**: Keep this checklist in your repository and update it based on lessons learned from each deployment.
