# PRP: [Feature Name] - One-Pass Implementation Guide

> **PRP = PRD + Curated Codebase Intelligence + Validation Loops**
> This document provides everything needed for production-ready implementation on the first pass.

## 🎯 Goal
[One clear sentence stating what must be achieved]

## 🔑 Why This Matters
- **User Value**: [Direct benefit to users]
- **Business Value**: [Revenue/growth/efficiency impact]
- **Technical Value**: [System improvement/debt reduction]

## ✅ Success Criteria (Measurable)
- [ ] [Specific measurable outcome with number/metric]
- [ ] [Performance requirement: e.g., "Response time < 500ms at p95"]
- [ ] [Quality requirement: e.g., "Zero console errors in production"]
- [ ] [Business metric: e.g., "20% increase in completion rate"]

## 🎭 User Stories
1. **As a** [user type], **I want to** [action] **so that** [benefit]
2. **As a** [user type], **I want to** [action] **so that** [benefit]
3. **As a** [user type], **I want to** [action] **so that** [benefit]

## 📚 All Needed Context

### Documentation & References
```yaml
# Each reference must explain WHY it's needed and WHAT to look for
- url: https://nextjs.org/docs/app/api-reference/functions/server-actions
  why: We're using server actions for form submission
  section: "Error Handling"
  critical: Must wrap in try-catch for proper error boundaries

- file: components/forms/ContactForm.tsx
  why: Follow same validation pattern and field structure
  pattern: Note useFieldTracking hook usage (line 45-67)
  gotcha: Async validation requires loading state

- file: lib/api/client.ts
  why: Standard API error handling pattern
  pattern: ApiError class usage and retry logic

- doc: https://supabase.com/docs/guides/database/postgres-policies
  section: "Row Level Security"
  critical: Always enable RLS on new tables

- pattern: lib/events/lead-events.ts
  why: Event tracking must be non-blocking
  usage: eventQueue.emit() for all analytics
```

### Known Gotchas & Critical Warnings
```markdown
# CRITICAL: Design system - ONLY use text-size-[1-4] and font-regular/semibold
# CRITICAL: All forms must implement field-level PII encryption
# CRITICAL: Never await analytics events - use eventQueue.emit()
# CRITICAL: Touch targets minimum 44px (use h-11 or h-12)
# WARNING: This API endpoint has 100 req/min rate limit
# WARNING: Safari mobile requires -webkit prefixes for [feature]
# NOTE: Loading states required for ALL async operations
```

### Required Patterns From Codebase
```typescript
// 1. Form Pattern (from ContactForm.tsx)
const form = useForm<FormData>({
  resolver: zodResolver(formSchema),
  defaultValues: initialValues
});

// 2. Event Tracking Pattern (non-blocking)
eventQueue.emit(LEAD_EVENTS.FORM_SUBMIT, {
  formId: 'contact',
  fields: Object.keys(data),
  timestamp: Date.now()
});

// 3. Error Handling Pattern
try {
  const result = await apiCall();
  return { success: true, data: result };
} catch (error) {
  if (error instanceof ApiError) {
    return { success: false, error: error.message };
  }
  throw error; // Unexpected errors bubble up
}

// 4. Loading State Pattern
const [isLoading, setIsLoading] = useState(false);
// ALWAYS show loading UI during async operations
```

## 🏗️ Implementation Blueprint

### Phase 1: Data Layer & Backend (2-3 hours)
```typescript
// 1. Database Schema
// Run: bun run db:generate after creating
create table feature_name (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id),
  data jsonb not null,
  created_at timestamp with time zone default now()
);

// 2. Enable RLS
alter table feature_name enable row level security;

// 3. Create policies
create policy "Users can view own data" on feature_name
  for select using (auth.uid() = user_id);

// 4. API Route Structure
// app/api/feature/route.ts
export async function POST(request: Request) {
  // Implementation following lib/api patterns
}
```

**Validation**: `bun run db:push && bun run test:api`

### Phase 2: Component Development (3-4 hours)
```typescript
// 1. Create base component with design system
// components/features/FeatureName.tsx
export function FeatureName() {
  // MUST use only approved classes
  return (
    <div className="bg-white rounded-xl p-4 border border-gray-200">
      <h2 className="text-size-2 font-semibold text-gray-900">Title</h2>
      <p className="text-size-3 font-regular text-gray-600">Content</p>
    </div>
  );
}

// 2. Add loading states
{isLoading ? (
  <LoadingSpinner />
) : (
  <Content />
)}

// 3. Implement error boundaries
// Required for all async components
```

**Validation**: `/vd && bun run test:components`

### Phase 3: Integration & Polish (2-3 hours)
1. Connect frontend to API with proper error handling
2. Add comprehensive event tracking (non-blocking)
3. Implement all edge cases from PRD
4. Mobile responsive testing (min 44px touch targets)
5. Performance optimization (lazy loading, code splitting)

**Validation**: `bun run test:e2e && /grade`

## 🧪 Validation Loops

### Level 1: Code Quality (Continuous)
```bash
# Auto-runs on save via hooks, but can run manually:
bun run lint:fix          # Biome formatting
bun run typecheck         # TypeScript checking
/vd                       # Design system validation
/validate-async          # Async pattern checking
```
✅ **Must Pass Before**: Committing any code

### Level 2: Feature Testing (After each component)
```bash
# Component testing
bun run test components/features/FeatureName.test.tsx

# Hook testing if applicable
bun run test hooks/useFeatureName.test.ts

# API testing
bun run test:api feature
```
✅ **Must Pass Before**: Integration

### Level 3: Integration Testing (After connecting pieces)
```bash
# Full feature flow
bun run test:e2e features/feature-name

# Accessibility 
bun run test:a11y

# Visual regression (if applicable)
bun run test:visual
```
✅ **Must Pass Before**: PR creation

### Level 4: Production Readiness (Before merge)
```bash
# Performance audit
bun run lighthouse

# Bundle size check
bun run analyze

# Security audit
bun run security:check

# Requirements compliance
/grade --requirements
/review-requirements
```
✅ **Must Pass Before**: Deployment

### Automated Validation
These run automatically via hooks:
- Pre-commit: Design system, linting, types
- Pre-push: Tests for changed files
- PR: Full test suite + CodeRabbit review
- Post-merge: Performance monitoring

## 🔧 Common Commands During Development

```bash
# Check before creating anything
/exists ComponentName     # Prevent duplicates
/deps check Button       # Check dependencies

# During development
/vd                      # Validate design
/validate-async         # Check async patterns
/bt add "bug desc"      # Track bugs

# Testing
/btf                    # Browser test flow
/test-requirements      # Test against pinned requirements

# Completion
/sv check               # Validate stage
/grade                  # Check alignment
/capture-to-issue      # Create GitHub issue
```

## 📊 Monitoring & Success Tracking

### Technical Metrics (Automated)
```typescript
// These are tracked automatically
- Page Load: < 3s (measured by analytics)
- API Response: < 500ms p95 (measured by monitoring)
- Error Rate: < 0.1% (Sentry tracking)
- Bundle Size: < 50KB for feature
```

### Business Metrics (Manual)
```typescript
// Add specific tracking
eventQueue.emit('feature.conversion', {
  feature: 'feature-name',
  action: 'completed',
  value: conversionValue
});
```

## 🚀 Deployment Checklist

### Pre-Deployment
- [ ] All validation loops passing
- [ ] `/grade --requirements` score > 85%
- [ ] No console errors in development
- [ ] Mobile responsive verified
- [ ] Loading states for all async ops
- [ ] Error states for all failures
- [ ] Analytics events implemented

### Post-Deployment
- [ ] Monitor error rates in Sentry
- [ ] Check performance metrics
- [ ] Verify analytics events flowing
- [ ] User feedback collection enabled

## 💡 Quick Tips

1. **When Stuck**: Check similar implementations in codebase
2. **For UI**: Always validate with `/vd` before proceeding  
3. **For API**: Follow patterns in `lib/api/`
4. **For Forms**: Use field registry for PII fields
5. **For Events**: Never block on analytics
6. **For Testing**: Tests are auto-generated from success criteria

## 🔗 Related Resources

- Requirements: `#[ISSUE_NUMBER]` (pinned with `/pin-requirements`)
- Design: [Figma link if applicable]
- API Docs: [Internal API documentation]
- Previous Implementation: [Link to similar feature]

---

**Remember**: The goal is production-ready code on the first pass. Every section of this PRP is designed to prevent common mistakes and ensure quality.

**Next Steps**:
1. Review this PRP for completeness
2. Run `/prd-async [feature]` if async operations needed
3. Run `/prd-tests [feature]` to generate test suite
4. Begin with Phase 1 implementation
