# Design System Standards

## Typography - STRICT ENFORCEMENT

### Font Sizes (ONLY these 4)
- `text-size-1`: 32px (mobile: 28px) - Major headings only
- `text-size-2`: 24px (mobile: 20px) - Section headers
- `text-size-3`: 16px - ALL body text, buttons, inputs
- `text-size-4`: 12px - Small labels, captions

### Font Weights (ONLY these 2)
- `font-regular`: 400 - For ALL body text
- `font-semibold`: 600 - For ALL headings and buttons

### Forbidden Classes
❌ NEVER use: text-xs, text-sm, text-base, text-lg, text-xl, text-2xl, text-3xl, text-4xl, text-5xl, text-6xl
❌ NEVER use: font-thin, font-extralight, font-light, font-normal, font-medium, font-bold, font-extrabold, font-black

## Spacing - 4px Grid System

### Valid Spacing Values
All spacing must use the 4px grid system. Valid classes:
- p-1 (4px), p-2 (8px), p-3 (12px), p-4 (16px)
- p-6 (24px), p-8 (32px), p-10 (40px), p-12 (48px), p-14 (56px)
- p-16 (64px), p-20 (80px), p-24 (96px), p-32 (128px)

Same applies to margins (m-), gaps (gap-), and directional spacing (pt-, pr-, pb-, pl-, etc.)

### Invalid Spacing
❌ Avoid: p-5, p-7, p-9, p-11, p-13, p-15, p-17, p-18, p-19, etc.

## Color Distribution Rule
Every screen must follow the 60/30/10 distribution:
- **60%**: Neutral backgrounds (white, gray-50)
- **30%**: Text and borders (gray-700, gray-200)
- **10%**: Primary actions (blue-600, red-600 for errors)

## Mobile Requirements
- **Minimum touch targets**: 44px (use h-11 or h-12)
- **Minimum body text**: 16px (text-size-3)
- **Maximum content width**: max-w-md for mobile-first
- **Responsive font sizes**: Automatically handled by text-size classes

## Component Patterns

### Container Pattern
```tsx
<div className="min-h-screen bg-gray-50">
  <div className="max-w-md mx-auto p-4">
    {/* Content here */}
  </div>
</div>
```

### Card Pattern
```tsx
<div className="bg-white border border-gray-200 rounded-xl p-4 space-y-3">
  <h3 className="text-size-2 font-semibold text-gray-900">Title</h3>
  <p className="text-size-3 font-regular text-gray-600">Content</p>
</div>
```

### Button Patterns
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

## Enforcement Mode
Can be toggled with `/dmoff` (disable) and `/dmon` (enable) commands.
