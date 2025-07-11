# Design System Rules - STRICT ENFORCEMENT

## Typography (4 Sizes, 2 Weights ONLY)
- text-size-1: 32px (major headings)
- text-size-2: 24px (section headers)  
- text-size-3: 16px (body text)
- text-size-4: 12px (small labels)
- font-semibold: 600 (headings/buttons)
- font-regular: 400 (everything else)

## Spacing (4px Grid ONLY)
- All values divisible by 4
- Use: 4, 8, 12, 16, 20, 24, 32, 48
- Never: 5, 10, 15, 18, 25, 30

## Colors (60/30/10 Distribution)
- 60%: Neutral backgrounds
- 30%: Text and borders
- 10%: Accent colors

## Mobile (Touch-Friendly)
- Min touch: 44px (h-11)
- Preferred: 48px (h-12)
- Min text: 16px

## Quick Validation Checklist

Before any code review or commit:
- [ ] Only 4 font sizes used?
- [ ] Only 2 font weights used?
- [ ] All spacing divisible by 4?
- [ ] Following 60/30/10 color rule?
- [ ] Touch targets at least 44px?
- [ ] Works on mobile?

## 🚫 Common Violations to Flag

```jsx
/* ❌ WRONG - Too many font sizes */
text-sm text-base text-lg text-xl text-2xl text-3xl

/* ✅ RIGHT - Only 4 sizes */
text-size-1 text-size-2 text-size-3 text-size-4

/* ❌ WRONG - Wrong font weights */
font-light font-medium font-bold

/* ✅ RIGHT - Only 2 weights */
font-regular font-semibold

/* ❌ WRONG - Not on 4px grid */
p-5 gap-7 m-10

/* ✅ RIGHT - On 4px grid */
p-4 gap-6 m-8
```
