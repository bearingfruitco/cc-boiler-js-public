Deploy current branch to staging environment:

1. Run all tests to ensure code quality
2. Build production bundle with staging config
3. Run deployment validation checks
4. Deploy to staging environment
5. Run smoke tests on staging
6. Notify team of deployment

**Pre-deployment checks:**
- All tests passing
- No console.logs in production code
- Environment variables configured
- Database migrations ready
- Branch is up to date with main

!npm test
!npm run lint
!NODE_ENV=staging npm run build

**Deployment steps:**
```bash
# Validate build
npm run validate:build

# Deploy to Vercel staging
vercel --env=preview

# Run smoke tests
npm run test:staging

# Notify team
echo "✅ Deployed to staging: $VERCEL_URL"
```

**Post-deployment:**
- Check staging URL is accessible
- Verify all features work
- Monitor error logs
- Test critical user paths
