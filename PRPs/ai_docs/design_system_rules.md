# Design System Rules - AI Reference

## Typography - ONLY These Classes

```css
/* Font Sizes - ONLY 4 OPTIONS */
.text-size-1 { font-size: 32px; line-height: 1.25; }  /* Major headings only */
.text-size-2 { font-size: 24px; line-height: 1.375; } /* Section headers */
.text-size-3 { font-size: 16px; line-height: 1.5; }   /* ALL body text, buttons, inputs */
.text-size-4 { font-size: 12px; line-height: 1.5; }   /* Small labels, captions */

/* Font Weights - ONLY 2 OPTIONS */
.font-regular { font-weight: 400; }   /* All body text */
.font-semibold { font-weight: 600; }  /* All headings and buttons */
```

## ❌ FORBIDDEN Classes

```tsx
// NEVER use these Tailwind defaults
text-xs, text-sm, text-base, text-lg, text-xl, text-2xl, text-3xl, text-4xl
font-thin, font-light, font-normal, font-medium, font-bold, font-extrabold

// ❌ WRONG
<p className="text-sm font-medium">

// ✅ CORRECT
<p className="text-size-3 font-regular">
```

## Spacing - 4px Grid ONLY

```css
/* ✅ VALID - All divisible by 4 */
p-0 (0px)    p-1 (4px)    p-2 (8px)    p-3 (12px)
p-4 (16px)   p-6 (24px)   p-8 (32px)   p-10 (40px)
p-12 (48px)  p-16 (64px)  p-20 (80px)  p-24 (96px)

/* ❌ INVALID - Not on 4px grid */
p-5 (20px)   p-7 (28px)   p-9 (36px)   p-11 (44px)
p-13 (52px)  p-14 (56px)  p-15 (60px)
```

## Component Patterns

### Button - Always Consistent

```tsx
// ✅ PRIMARY Button Pattern
<button className="w-full h-12 px-4 rounded-xl bg-blue-600 text-white text-size-3 font-semibold hover:bg-blue-700 transition-colors disabled:bg-gray-200 disabled:text-gray-400">
  Click Me
</button>

// ✅ SECONDARY Button Pattern  
<button className="w-full h-12 px-4 rounded-xl bg-gray-800 text-white text-size-3 font-semibold hover:bg-gray-900 transition-colors disabled:bg-gray-200 disabled:text-gray-400">
  Click Me
</button>

// ✅ GHOST Button Pattern
<button className="w-full h-12 px-4 rounded-xl bg-transparent text-gray-700 text-size-3 font-semibold hover:bg-gray-100 transition-colors disabled:text-gray-400">
  Click Me
</button>
```

### Card - Consistent Structure

```tsx
// ✅ Card Container
<div className="bg-white border border-gray-200 rounded-xl p-4 space-y-3">
  <h3 className="text-size-2 font-semibold text-gray-900">Card Title</h3>
  <p className="text-size-3 font-regular text-gray-600">
    Card content goes here with proper typography.
  </p>
  <div className="pt-2">
    <button className="w-full h-12 px-4 rounded-xl bg-blue-600 text-white text-size-3 font-semibold">
      Action
    </button>
  </div>
</div>
```

### Form Field - Accessible Pattern

```tsx
// ✅ Form Field Structure
<div className="space-y-2">
  <label 
    htmlFor="email" 
    className="text-size-3 font-semibold text-gray-700"
  >
    Email Address
  </label>
  <input
    id="email"
    type="email"
    className="w-full h-12 px-4 border-2 border-gray-200 rounded-xl text-size-3 focus:border-blue-500 focus:outline-none transition-colors"
    placeholder="your@email.com"
  />
  <p className="text-size-4 text-gray-500">
    We'll never share your email.
  </p>
</div>

// ✅ With Error State
<div className="space-y-2">
  <label htmlFor="email" className="text-size-3 font-semibold text-gray-700">
    Email Address
  </label>
  <input
    id="email"
    type="email"
    className="w-full h-12 px-4 border-2 border-red-500 rounded-xl text-size-3 focus:outline-none"
    aria-invalid="true"
    aria-describedby="email-error"
  />
  <p id="email-error" className="text-size-4 text-red-600">
    Please enter a valid email address
  </p>
</div>
```

### Layout Container

```tsx
// ✅ Mobile-First Container
<div className="min-h-screen bg-gray-50">
  <div className="max-w-md mx-auto p-4">
    {/* Content */}
  </div>
</div>

// ✅ With Header
<div className="min-h-screen bg-gray-50">
  <header className="bg-white border-b border-gray-200">
    <div className="max-w-md mx-auto p-4">
      <h1 className="text-size-2 font-semibold text-gray-900">App Name</h1>
    </div>
  </header>
  <main className="max-w-md mx-auto p-4">
    {/* Content */}
  </main>
</div>
```

## Mobile Requirements

### Touch Targets
```tsx
// ❌ Too small - 36px
<button className="h-9">Too Small</button>

// ✅ Minimum - 44px
<button className="h-11">Good Size</button>

// ✅ Preferred - 48px
<button className="h-12">Perfect Size</button>

// ✅ Large - 56px for emphasis
<button className="h-14">Large Action</button>
```

### Responsive Patterns
```tsx
// ✅ Stack on mobile, side-by-side on larger screens
<div className="flex flex-col sm:flex-row gap-4">
  <button className="w-full sm:w-auto h-12 px-6">Cancel</button>
  <button className="w-full sm:w-auto h-12 px-6">Save</button>
</div>

// ✅ Responsive grid
<div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
  {items.map(item => <Card key={item.id} {...item} />)}
</div>
```

## Color Distribution - 60/30/10 Rule

Every screen must follow this distribution:

### 60% - Background/Neutral
- `bg-white` - Primary backgrounds
- `bg-gray-50` - Secondary backgrounds
- `bg-gray-100` - Subtle backgrounds

### 30% - Content/Structure  
- `text-gray-900` - Primary text
- `text-gray-700` - Secondary text
- `text-gray-600` - Tertiary text
- `border-gray-200` - Borders
- `bg-gray-200` - Disabled states

### 10% - Actions/Accents
- `bg-blue-600` - Primary actions
- `text-blue-600` - Links
- `bg-red-600` - Destructive actions
- `text-red-600` - Errors
- `bg-green-600` - Success states

## Common Violations & Fixes

### Typography Violations
```tsx
// ❌ WRONG - Using Tailwind defaults
<h1 className="text-2xl font-bold">
<p className="text-sm text-gray-500">
<button className="text-lg font-medium">

// ✅ CORRECT - Using design system
<h1 className="text-size-1 font-semibold">
<p className="text-size-3 text-gray-600">
<button className="text-size-3 font-semibold">
```

### Spacing Violations
```tsx
// ❌ WRONG - Not on 4px grid
<div className="p-5 gap-7 mb-9">

// ✅ CORRECT - On 4px grid
<div className="p-4 gap-6 mb-8">
// or
<div className="p-6 gap-8 mb-10">
```

### Touch Target Violations
```tsx
// ❌ WRONG - Too small for mobile
<button className="px-2 py-1 text-size-4">

// ✅ CORRECT - Proper touch target
<button className="h-11 px-4 text-size-3">
```

## Quick Reference

### Text Hierarchy
- **Page Title**: `text-size-1 font-semibold`
- **Section Header**: `text-size-2 font-semibold`
- **Body Text**: `text-size-3 font-regular`
- **Caption/Label**: `text-size-4 font-regular`

### Spacing Scale
- **Tight**: `space-y-2` (8px)
- **Default**: `space-y-3` (12px)
- **Relaxed**: `space-y-4` (16px)
- **Loose**: `space-y-6` (24px)

### Border Radius
- **Always**: `rounded-xl` (12px)
- **Never**: `rounded`, `rounded-md`, `rounded-lg`

### Shadows
- **Avoid shadows** - Use borders instead
- If needed: `shadow-sm` only

## Enforcement

These rules are enforced by the design validation hook:
- `/vd` command checks all components
- Pre-commit hooks block violations
- CI/CD pipeline validates on PR

Remember: Consistency > Creativity in design systems!
