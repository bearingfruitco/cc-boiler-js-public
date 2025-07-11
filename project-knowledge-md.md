# Project Knowledge Base - [Project Name]

## Project Overview
[Detailed description of what this application does]

## Design System Enforcement

### Critical Rules (AI MUST FOLLOW)
1. **Typography**: 4 sizes, 2 weights ONLY
2. **Spacing**: 4px grid system ONLY
3. **Colors**: 60/30/10 distribution
4. **Mobile**: 44px+ touch, 16px+ text

### Quick Validation
```bash
# Check typography
grep -r "text-\(sm\|lg\|xl\|2xl\)" --include="*.tsx" .

# Check font weights  
grep -r "font-\(light\|medium\|bold\)" --include="*.tsx" .

# Check spacing
grep -r "\(p\|m\|gap\|space\)-[57]" --include="*.tsx" .
```

## Component Library

### Approved Patterns
- Container: max-w-md mx-auto p-4
- Card: bg-white border rounded-xl p-4
- Button: h-12 rounded-xl font-semibold
- Input: h-12 border-2 rounded-xl

### Anti-Patterns (NEVER USE)
- Small text: text-sm, text-xs
- Wrong weights: font-bold, font-medium
- Off-grid: p-5, m-7, gap-10
- Small touch: h-8, h-10 for buttons

## Business Logic
[Link to separate BUSINESS_LOGIC.md]

### Core Features
1. [Feature 1 description]
2. [Feature 2 description]
3. [Feature 3 description]

### User Flows
1. [Primary user flow]
2. [Secondary user flow]
3. [Edge cases]

## Technical Stack
- Next.js 15
- React 19
- TypeScript 5.8
- Tailwind CSS 4.0
- Supabase
- Framer Motion

## File Structure
```
project-name/
├── components/
│   ├── ui/          # Reusable components
│   ├── forms/       # Form components
│   ├── layout/      # Layout components
│   └── features/    # Feature-specific
├── lib/
│   ├── api/         # API utilities
│   ├── db/          # Database queries
│   ├── utils/       # Helper functions
│   └── validation/  # Zod schemas
├── hooks/           # Custom React hooks
├── types/           # TypeScript types
└── app/             # Next.js app router
    ├── api/         # API routes
    ├── (public)/    # Public pages
    └── (protected)/ # Auth-required pages
```

## Common Tasks

### Adding a New Feature
1. Follow design system strictly
2. Use existing components
3. Test on mobile first
4. Add proper error handling
5. Include loading states

### Fixing Design Violations
1. Run `/validate-design` command
2. Fix all critical violations
3. Address warnings
4. Re-validate

## Integration Notes

### When Using External Libraries
1. Wrap in design system components
2. Override styles to match
3. Ensure mobile compatibility
4. Test all states

### When Adding Animations
1. Use Framer Motion
2. Follow timing guidelines
3. Test performance on mobile
4. Add reduced motion support

## Validation Checklist

Before any code review or commit:
- [ ] Only 4 font sizes used?
- [ ] Only 2 font weights used?
- [ ] All spacing divisible by 4?
- [ ] Following 60/30/10 color rule?
- [ ] Touch targets at least 44px?
- [ ] Works on mobile?

## Remember
The design system is LAW. Every violation reduces trust and consistency.
