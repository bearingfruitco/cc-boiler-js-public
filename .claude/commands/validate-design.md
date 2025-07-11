# Validate Design System Compliance

Check current file or project against design system rules.

## Steps:

1. **Typography Check**
   ```typescript
   // Find violations
   const fontSizeViolations = findClasses(/(text-(xs|sm|base|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl))/g);
   const fontWeightViolations = findClasses(/(font-(thin|extralight|light|normal|medium|bold|extrabold|black))/g);
   
   // Flag each violation with line number
   ```

2. **Spacing Check**
   ```typescript
   // Check for non-4px grid values
   const spacingClasses = /(p|m|gap|space)-(5|7|9|10|11|13|14|15|17|18|19)/g;
   
   // Suggest nearest valid value
   ```

3. **Color Distribution Analysis**
   ```typescript
   // Count color usage
   const backgrounds = countClasses(/bg-(white|gray-50)/g);
   const textColors = countClasses(/text-(gray-[67]00)/g);
   const accents = countClasses(/(bg|text)-(blue|red|green)-[56]00/g);
   
   // Calculate percentages
   ```

4. **Touch Target Check**
   ```typescript
   // Find buttons and interactive elements
   const smallTargets = findElements('h-[0-9]+').filter(h => parseInt(h) < 44);
   ```

5. **Generate Report**
   ```markdown
   # Design System Validation Report
   
   ## ❌ Critical Violations (3)
   - Line 42: `text-sm` → use `text-size-4`
   - Line 67: `font-bold` → use `font-semibold`
   - Line 89: `p-5` → use `p-4` or `p-6`
   
   ## ⚠️ Warnings (2)
   - Touch target on line 34 is only 40px
   - Color distribution: 70/25/5 (should be 60/30/10)
   
   ## ✅ Passed Checks
   - All containers use max-w-md
   - Mobile-first approach confirmed
   - Proper error handling present
   ```

## Auto-fix Option:
Offer to automatically fix violations with user confirmation.
