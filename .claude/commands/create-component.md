# Create Component Following Design System

Generate a new component with perfect design system compliance.

## Arguments:
- $COMPONENT_TYPE: ui|form|layout|feature
- $COMPONENT_NAME: Component name
- $PROPS: Optional props definition

## Steps:

1. **Component Structure**
   ```typescript
   // Always include:
   - TypeScript interface
   - Proper imports
   - Design system classes
   - Mobile-first approach
   - Error states (if applicable)
   ```

2. **Apply Design Patterns**
   - Use only 4 font sizes
   - Use only 2 font weights
   - Apply 4px grid spacing
   - Follow color distribution
   - Ensure 44px+ touch targets

3. **Add Animations**
   - Hover states (100-200ms)
   - Focus states
   - Loading states
   - Error transitions

4. **Include Variants**
   - Primary/secondary/ghost
   - Sizes (if applicable)
   - States (loading/disabled/error)

5. **Add Documentation**
   ```typescript
   /**
    * Component following design system
    * - 4 font sizes only
    * - 2 font weights only  
    * - 4px grid spacing
    * - Mobile-first
    */
   ```

## Example Output:
Complete component file with all variants and proper design system implementation.
