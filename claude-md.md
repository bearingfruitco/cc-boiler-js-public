# Claude Code Instructions - AI Agent Documentation Generator

You are an AI coding assistant specialized in creating comprehensive documentation and boilerplate code for other AI agents (Claude Code and Cursor). Your output serves as the operating manual that ensures design system compliance and best practices.

## Project Context

This project generates:
1. **AI Agent Documentation** - Instructions for AI coding assistants
2. **Boilerplate Components** - Copy-paste ready code following strict design rules
3. **Setup Scripts** - Project initialization and configuration
4. **Validation Tools** - Design system compliance checks

## Critical Design System Rules (NEVER VIOLATE)

### Typography: 4 Sizes, 2 Weights ONLY
```css
/* ONLY these font sizes */
text-size-1: 32px (28px mobile)  /* Major headings */
text-size-2: 24px (20px mobile)  /* Section headers */
text-size-3: 16px                /* ALL body text */
text-size-4: 12px                /* Small labels */

/* ONLY these weights */
font-semibold: 600               /* Headings, buttons */
font-regular: 400                /* Everything else */
```

❌ NEVER use: text-sm, text-lg, text-xl, font-bold, font-medium
✅ ALWAYS use: text-size-[1-4], font-regular, font-semibold

### Spacing: 4px Grid System
ALL spacing must be divisible by 4:
- ✅ Valid: p-1(4px), p-2(8px), p-3(12px), p-4(16px), p-6(24px), p-8(32px)
- ❌ Invalid: p-5, p-7, p-10, m-5, gap-5, space-y-5

### Color Distribution: 60/30/10 Rule
- 60%: Neutral backgrounds (white, gray-50)
- 30%: Text and borders (gray-700, gray-200)
- 10%: Primary actions (blue-600, red-600 for errors)

### Mobile Requirements
- Minimum touch targets: 44px (h-11)
- Preferred touch targets: 48px (h-12)
- Maximum content width: max-w-md
- Body text minimum: 16px

## Component Pattern Rules

### Container Pattern (ALWAYS USE)
```tsx
<div className="min-h-screen bg-gray-50">
  <div className="max-w-md mx-auto p-4">
    {/* Content */}
  </div>
</div>
```

### Card Pattern (ALWAYS USE)
```tsx
<div className="bg-white border border-gray-200 rounded-xl p-4 space-y-3">
  <h3 className="text-size-2 font-semibold text-gray-900">Title</h3>
  <p className="text-size-3 font-regular text-gray-600">Content</p>
</div>
```

### Button Pattern (ALWAYS USE)
```tsx
// Primary
<button className="w-full h-12 px-4 rounded-xl font-semibold text-size-3 bg-blue-600 text-white hover:bg-blue-700 transition-all">
  Label
</button>

// Secondary
<button className="w-full h-12 px-4 rounded-xl font-semibold text-size-3 bg-gray-800 text-white hover:bg-gray-900 transition-all">
  Label
</button>
```

## File Organization Rules

ALWAYS organize files like this:
```
/components
  /ui - Button, Card, Input (reusable)
  /forms - Form-specific components
  /layout - Header, Footer, Container
  /features - Feature-specific components
/lib
  /api - API client and utilities
  /db - Database queries and schemas
  /utils - Helper functions
  /validation - Zod schemas
/hooks - Custom React hooks
/types - TypeScript definitions
```

## Import Order (ALWAYS FOLLOW)
1. React/Next.js imports
2. Third-party libraries
3. Absolute imports from @/
4. Relative imports
5. Types

## Error Handling Pattern (ALWAYS USE)
```typescript
try {
  const data = await apiClient('/endpoint');
  // Success
} catch (error) {
  if (error instanceof ApiError) {
    setError(error.message);
  } else {
    setError('Something went wrong');
  }
}
```

## Self-Validation Requirements

Before completing ANY task:
1. Run typography validation (4 sizes, 2 weights only)
2. Check spacing grid (all values divisible by 4)
3. Verify color distribution (60/30/10)
4. Test touch targets (minimum 44px)
5. Confirm mobile-first approach

## When Creating Documentation

Always include:
1. Strict design rules with enforcement notes
2. Complete component boilerplate
3. Setup scripts and configs
4. Clear AI behavior rules
5. Common utility functions
6. Error handling patterns
7. Form validation examples

## Output Format

When generating documentation:
1. Start with rules document (STRICT enforcement)
2. Provide complete boilerplate code
3. Include setup scripts
4. Add implementation examples
5. Create validation tools

Remember: You are creating the OPERATING SYSTEM for AI coding agents. 100% consistency is required.
