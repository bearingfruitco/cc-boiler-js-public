Validate environment configuration and check all required variables:

1. Check all .env files exist
2. Validate required variables are set
3. Test service connections
4. Verify API endpoints accessible
5. Check database connectivity
6. Display configuration report

**File validation:**
!ls -la .env* | grep -v ".local"

**Required variables check:**
!node -e "
const required = [
  'NODE_ENV',
  'DATABASE_URL',
  'NEXT_PUBLIC_SUPABASE_URL',
  'NEXT_PUBLIC_SUPABASE_ANON_KEY',
  'SUPABASE_SERVICE_ROLE_KEY',
  'NEXT_PUBLIC_API_URL'
];

const missing = required.filter(key => !process.env[key]);
if (missing.length > 0) {
  console.error('❌ Missing required variables:', missing);
  process.exit(1);
} else {
  console.log('✅ All required variables set');
}
"

**Service connectivity tests:**
```bash
# Test database connection
npm run db:test

# Test Supabase
curl -I $NEXT_PUBLIC_SUPABASE_URL

# Test API endpoint
curl -I $NEXT_PUBLIC_API_URL/health
```

**Environment report:**
- Current: $NODE_ENV
- App URL: $NEXT_PUBLIC_APP_URL
- Features enabled: Check config/index.ts
