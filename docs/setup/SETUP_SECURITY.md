# Security Setup Guide

This guide helps you properly configure all security-sensitive aspects of the boilerplate.

## 🔐 Environment Variables

### 1. Create Your Local Environment File
```bash
# Copy the example file
cp .env.example .env.local

# IMPORTANT: .env.local is gitignored and should NEVER be committed
```

### 2. Configure Required Variables

#### Database Configuration
```bash
DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
DATABASE_DIRECT_URL="postgresql://user:password@localhost:5432/dbname"
```

#### Supabase Configuration
```bash
NEXT_PUBLIC_SUPABASE_URL="https://your-project.supabase.co"
NEXT_PUBLIC_SUPABASE_ANON_KEY="your-anon-key"
SUPABASE_SERVICE_ROLE_KEY="your-service-role-key"
```
Get these from your [Supabase Dashboard](https://app.supabase.com) → Settings → API

#### Analytics (Optional)
```bash
NEXT_PUBLIC_RUDDERSTACK_KEY="your-write-key"
NEXT_PUBLIC_RUDDERSTACK_DATA_PLANE_URL="https://your-dataplane.rudderstack.com"
```

#### Error Tracking (Optional)
```bash
NEXT_PUBLIC_SENTRY_DSN="https://your-key@sentry.io/project-id"
SENTRY_AUTH_TOKEN="your-auth-token"
SENTRY_ORG="your-org"
SENTRY_PROJECT="your-project"
```

## 🔧 MCP (Model Context Protocol) Configuration

The `.mcp.json` file configures various AI tool integrations. All values are placeholders that must be replaced.

### 1. GitHub Integration
```json
"github": {
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_GITHUB_PAT"
  }
}
```

**To get your GitHub PAT:**
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with scopes: `repo`, `workflow`, `read:org`
3. Copy and replace `YOUR_GITHUB_PAT`

### 2. Brave Search
```json
"brave-search": {
  "env": {
    "BRAVE_API_KEY": "YOUR_BRAVE_API_KEY"
  }
}
```

**To get your Brave API key:**
1. Sign up at [brave.com/search/api](https://brave.com/search/api)
2. Create a new app
3. Copy your API key

### 3. Supabase MCP
```json
"supabase": {
  "env": {
    "SUPABASE_API_KEY": "YOUR_SUPABASE_SERVICE_ROLE_KEY"
  }
}
```
Use the same service role key from your `.env.local`

### 4. Other Services (Optional)
Each service in `.mcp.json` can be:
- Configured with real API keys if you'll use it
- Disabled by setting `"disabled": true`
- Left with placeholders if unused

## 🛡️ Security Best Practices

### Never Commit Secrets
```bash
# Good - Using environment variables
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

# Bad - Hardcoded values
const supabase = createClient(
  "https://xyzcompany.supabase.co",
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
)
```

### Use Server-Side for Sensitive Operations
```typescript
// app/api/secure/route.ts
// Service role key only on server
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!,
  { auth: { persistSession: false } }
)
```

### PII (Personally Identifiable Information) Handling
The boilerplate includes PII protection:
- Field-level encryption for sensitive data
- Audit logging for all PII access
- Server-side only processing
- No PII in URLs or client storage

### Regular Security Audits
```bash
# Run security check command
/sc

# Check for exposed secrets
grep -r "sk_" . --exclude-dir=node_modules --exclude-dir=.git
grep -r "API_KEY" . --exclude-dir=node_modules --exclude="*.md"
```

## 🚀 Deployment Security

### Vercel Deployment
1. Add all environment variables in Vercel Dashboard
2. Use different values for preview vs production
3. Enable [Vercel Environment Variable Encryption](https://vercel.com/docs/concepts/projects/environment-variables#encryption)

### Other Platforms
- **Netlify**: Use environment variables UI
- **AWS**: Use AWS Secrets Manager
- **Railway**: Use environment variables dashboard
- **Fly.io**: Use `fly secrets` command

## ⚠️ Common Security Mistakes to Avoid

1. **Committing .env.local**
   ```bash
   # If accidentally committed, remove from history
   git rm --cached .env.local
   git commit -m "Remove .env.local"
   ```

2. **Using client-side keys for server operations**
   - `NEXT_PUBLIC_*` vars are visible to browsers
   - Keep service keys server-side only

3. **Logging sensitive data**
   ```typescript
   // Bad
   console.log('User data:', userData)
   
   // Good
   console.log('User ID:', userData.id)
   ```

4. **Storing PII in localStorage**
   ```typescript
   // Bad
   localStorage.setItem('userEmail', email)
   
   // Good - Use secure server-side sessions
   ```

## 📚 Additional Resources

- [Next.js Security Best Practices](https://nextjs.org/docs/authentication)
- [Supabase Security](https://supabase.com/docs/guides/auth/row-level-security)
- [OWASP Security Guidelines](https://owasp.org/www-project-top-ten/)

## 🆘 Need Help?

If you're unsure about any security configuration:
1. Check the example values in `.env.example`
2. Refer to the service's official documentation
3. Use placeholder values during development
4. Ask in the project discussions/issues

Remember: **When in doubt, keep it out (of the repository)!**
