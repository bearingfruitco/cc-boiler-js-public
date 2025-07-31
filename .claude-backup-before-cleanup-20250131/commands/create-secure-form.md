# create-secure-form (Enhanced with Browser Testing)

Creates a form component with comprehensive security features and automatic browser testing.

## Usage
```bash
create-secure-form <name> [options]
/csf <name> [options]
```

## Arguments
- `name` - Name of the form component (e.g., `ContactForm`, `LoginForm`)

## Options
- `--captcha` - Include reCAPTCHA v3 (default: true for public forms)
- `--rate-limit <config>` - Rate limit: `strict` (3/10m), `standard` (5/10m), `relaxed` (10/10m)
- `--honeypot` - Include honeypot field (default: true)
- `--fields <fields>` - Comma-separated field names
- `--tracking` - Include event tracking (default: true)
- `--skip-browser` - Skip browser testing (NOT RECOMMENDED)

## Examples
```bash
# Create standard secure form with browser testing
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
- Accessibility features

### Security Features Included
- ✅ Input validation (Zod schemas)
- ✅ CAPTCHA protection (reCAPTCHA v3)
- ✅ Client-side rate limiting
- ✅ Honeypot bot detection
- ✅ CSRF protection (Next.js built-in)
- ✅ XSS prevention (React sanitization)
- ✅ Event tracking for monitoring
- ✅ Proper error messages

### NEW: Automatic Browser Testing
After form creation, automatically runs:

```bash
# 1. Form submission testing
/pw-form ContactForm
  - Tests empty submission
  - Tests validation errors
  - Tests successful submission
  - Verifies error messages display

# 2. Accessibility testing
/pw-a11y ContactForm
  - Keyboard navigation
  - Screen reader labels
  - Focus management
  - Error announcements

# 3. Security testing
  - CAPTCHA functionality
  - Rate limiting behavior
  - Honeypot effectiveness
  - XSS prevention

# 4. Visual verification
/pw-screenshot ContactForm
  - Default state
  - Error state
  - Success state
  - Loading state
```

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

// Accessibility
<form role="form" aria-label="Contact form">
  <label htmlFor="email" id="email-label">
    Email Address
    {errors.email && (
      <span role="alert" aria-live="polite">
        {errors.email.message}
      </span>
    )}
  </label>
</form>
```

## Browser Test Results
After creation, you'll see:

```
📊 Form Browser Test Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Form Submission Tests
  - Empty form shows validation ✓
  - Invalid email caught ✓
  - Valid submission works ✓
  - Success message displays ✓

✅ Security Tests
  - CAPTCHA loads correctly ✓
  - Rate limiting after 5 attempts ✓
  - Honeypot field hidden ✓
  - No XSS vulnerabilities ✓

✅ Accessibility Tests
  - All fields labeled ✓
  - Tab order correct ✓
  - Errors announced ✓
  - 100% keyboard navigable ✓

✅ Visual States
  - Default: Clean layout ✓
  - Error: Red indicators ✓
  - Loading: Spinner shows ✓
  - Success: Green confirmation ✓

📸 Screenshots saved to:
  - .claude/screenshots/ContactForm-default.png
  - .claude/screenshots/ContactForm-error.png
  - .claude/screenshots/ContactForm-success.png
```

## Post-Creation Steps
1. ✅ Browser tests already run automatically
2. Add reCAPTCHA site key to `.env.local`
3. Customize validation schema if needed
4. Add API endpoint for form submission
5. Re-run browser tests after changes: `/pw-form ContactForm`

## Integration
Works with:
- `/audit-form-security` - Verify security implementation
- `/test-security form` - Run security tests
- `/pw-form` - Re-test form behavior
- `/pw-a11y` - Check accessibility
- Event tracking system
- Analytics dashboard

## Why Browser Testing Matters for Forms

Forms are critical user touchpoints that must:
- Actually submit data correctly
- Show clear error messages
- Be fully accessible
- Work on all devices
- Handle edge cases gracefully

Browser testing ensures your secure forms actually work for users! 🔐🌐
