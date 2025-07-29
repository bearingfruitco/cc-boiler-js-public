Display current environment status and configuration:

1. Show current NODE_ENV
2. List available environments
3. Check environment file status
4. Validate current configuration
5. Show active features
6. Display deployment readiness

**Current Environment:**
!echo "NODE_ENV: $NODE_ENV"

**Environment Files:**
!ls -la .env* | grep -E "\.env\.(development|staging|production)$" || echo "No environment files found"

**Configuration Check:**
!node -e "
try {
  const { env, isDevelopment, isStaging, isProduction } = require('./lib/env');
  console.log('✅ Environment loaded successfully');
  console.log('');
  console.log('Current Environment:', env.NODE_ENV);
  console.log('App URL:', env.NEXT_PUBLIC_APP_URL);
  console.log('');
  console.log('Features Enabled:');
  console.log('- New Checkout:', env.ENABLE_NEW_CHECKOUT);
  console.log('- AI Assistant:', env.ENABLE_AI_ASSISTANT);
  console.log('- Analytics:', env.ENABLE_ANALYTICS);
  console.log('');
  console.log('Logging:');
  console.log('- Debug Logs:', env.ENABLE_DEBUG_LOGS);
  console.log('- SQL Logs:', env.ENABLE_SQL_LOGS);
} catch (error) {
  console.error('❌ Environment validation failed:', error.message);
  console.log('Run: npm run setup:env');
}
"

**Deployment Readiness:**
- Development: Always ready for local dev
- Staging: Run `/ssd` or `npm run deploy:staging`
- Production: Run `/spd` or `npm run deploy:production`

**Quick Actions:**
- Switch environment: `/env-switch [environment]`
- Validate config: `/env-validate`
- Deploy to staging: `/ssd`
- Check deployment history: `vercel list`
