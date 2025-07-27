# create-secure-form

Creates a form component with comprehensive security features built-in.

## Usage
```bash
create-secure-form <name> [options]
```

## Arguments
- `name` - Name of the form component (e.g., `ContactForm`, `LoginForm`)

## Options
- `--captcha` - Include reCAPTCHA v3 (default: true for public forms)
- `--rate-limit <config>` - Rate limit: `strict` (3/10m), `standard` (5/10m), `relaxed` (10/10m)
- `--honeypot` - Include honeypot field (default: true)
- `--fields <fields>` - Comma-separated field names
- `--tracking` - Include event tracking (default: true)

## Examples
```bash
# Create standard secure form
create-secure-form ContactForm

# Create form with specific fields
create-secure-form LeadForm --fields="name,email,phone,company"

# Create form with strict rate limiting
create-secure-form ApplicationForm --rate-limit=strict

# Create form without CAPTCHA (for authenticated users)
create-secure-form ProfileForm --captcha=false
```

## What it generates

### Form Component (`components/forms/[Name].tsx`)
- Zod validation schema
- React Hook Form integration
- CAPTCHA component (if enabled)
- Rate limiting hook
- Honeypot field (if enabled)
- Event tracking
- Error handling
- Loading states
- Success messages

### Security Features Included
- ✅ Input validation (Zod schemas)
- ✅ CAPTCHA protection (reCAPTCHA v3)
- ✅ Client-side rate limiting
- ✅ Honeypot bot detection
- ✅ CSRF protection (Next.js built-in)
- ✅ XSS prevention (React sanitization)
- ✅ Event tracking for monitoring
- ✅ Proper error messages

## Generated Code Structure
```typescript
// Validation schema
const schema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  // ... other fields
});

// Rate limiting
const { checkLimit } = useRateLimit('form-name', {
  max: 5,
  window: '10m'
});

// CAPTCHA integration
<ReCAPTCHA
  siteKey={process.env.NEXT_PUBLIC_RECAPTCHA_SITE_KEY}
  onChange={setCaptchaToken}
/>

// Event tracking
eventQueue.emit(LEAD_EVENTS.FORM_SUBMIT, {
  formName: 'secure-form',
  timestamp: Date.now()
});
```

## Post-Creation Steps
1. Add reCAPTCHA site key to `.env.local`
2. Customize validation schema
3. Add API endpoint for form submission
4. Test rate limiting
5. Verify CAPTCHA scoring

## Integration
Works with:
- `/audit-form-security` - Verify security implementation
- `/test-security form` - Run security tests
- Event tracking system
- Analytics dashboard
