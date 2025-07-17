# PRP: [Component Name] - TypeScript/React Implementation Guide

> **Component-Focused PRP for TypeScript/React Development**
> Optimized for your design system with strict type safety

## 🎯 Component Goal
[What UI problem does this component solve?]

## 📦 Component Specification

### Props Interface
```typescript
interface [ComponentName]Props {
  // Required props
  id: string;
  onSubmit: (data: FormData) => Promise<void>;
  
  // Optional props  
  initialData?: Partial<FormData>;
  className?: string;
  disabled?: boolean;
}

// Data types
interface FormData {
  // Define the shape of data
}
```

### Component Behavior
- **Initial State**: [How component appears on load]
- **Interactive States**: [Hover, focus, active, disabled]
- **Loading States**: [How async operations display]
- **Error States**: [How errors are shown]
- **Success States**: [Completion feedback]

## 📚 Required Context

### Design System Compliance
```typescript
// ONLY these classes are allowed:
// Text: text-size-1, text-size-2, text-size-3, text-size-4
// Weight: font-regular, font-semibold
// Spacing: p-1(4px), p-2(8px), p-3(12px), p-4(16px), p-6(24px), p-8(32px)
// Touch: min height h-11(44px) or h-12(48px) for interactive elements

// Example compliant component:
<button className="h-12 px-4 rounded-xl bg-blue-600 text-white text-size-3 font-semibold hover:bg-blue-700 transition-colors">
  Click Me
</button>
```

### Pattern References
```yaml
- file: components/ui/Button.tsx
  why: Standard button patterns and prop interfaces
  pattern: Note disabled state handling and loading spinner

- file: components/forms/ContactForm.tsx  
  why: Form validation and submission patterns
  critical: useFieldTracking hook for analytics (line 45)

- file: hooks/useAsync.ts
  why: Standard async state management
  usage: Handles loading, error, and data states

- pattern: lib/utils/cn.ts
  why: Class name merging for variants
  usage: cn(baseClasses, variantClasses, className)
```

### Critical TypeScript Patterns
```typescript
// 1. Strict Event Handler Types
const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
  event.preventDefault();
  // Handle click
};

// 2. Proper Form Event Types
const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
  event.preventDefault();
  // Handle submit
};

// 3. Generic Component Props
interface BaseProps<T> {
  data: T;
  onUpdate: (updated: T) => void;
}

// 4. Discriminated Unions for State
type AsyncState<T> = 
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };
```

## 🏗️ Implementation Blueprint

### Step 1: Type Definitions
```typescript
// types/[feature].ts
export interface [ComponentName]Data {
  // Data structure with strict types
}

export interface [ComponentName]Props {
  // Component props with JSDoc comments
  /** Unique identifier for tracking */
  id: string;
  
  /** Callback fired on successful submission */
  onSuccess?: (data: [ComponentName]Data) => void;
}

// Validation schema
export const [componentName]Schema = z.object({
  // Zod schema matching the interface
});
```

### Step 2: Component Structure
```typescript
// components/[feature]/[ComponentName].tsx
'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { eventQueue, LEAD_EVENTS } from '@/lib/events';
import { cn } from '@/lib/utils';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';

export function [ComponentName]({ 
  id,
  onSuccess,
  className 
}: [ComponentName]Props) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const form = useForm<[ComponentName]Data>({
    resolver: zodResolver([componentName]Schema),
    defaultValues: {
      // Set defaults
    }
  });

  const handleSubmit = async (data: [ComponentName]Data) => {
    setIsSubmitting(true);
    
    try {
      // Fire non-blocking analytics
      eventQueue.emit(LEAD_EVENTS.FORM_SUBMIT, {
        formId: id,
        timestamp: Date.now()
      });
      
      // API call
      const result = await apiClient.post('/api/[endpoint]', data);
      
      // Success handling
      onSuccess?.(result.data);
      
    } catch (error) {
      // Error handling following pattern
      console.error('Submission failed:', error);
      form.setError('root', {
        message: 'Something went wrong. Please try again.'
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form 
      onSubmit={form.handleSubmit(handleSubmit)}
      className={cn('space-y-4', className)}
    >
      {/* Component implementation */}
      
      {/* Always show loading state during async operations */}
      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full h-12 px-4 rounded-xl bg-blue-600 text-white text-size-3 font-semibold hover:bg-blue-700 transition-colors disabled:bg-gray-300"
      >
        {isSubmitting ? <LoadingSpinner /> : 'Submit'}
      </button>
      
      {/* Error display */}
      {form.formState.errors.root && (
        <p className="text-size-4 text-red-600">
          {form.formState.errors.root.message}
        </p>
      )}
    </form>
  );
}
```

### Step 3: Component Tests
```typescript
// components/[feature]/[ComponentName].test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { [ComponentName] } from './[ComponentName]';

describe('[ComponentName]', () => {
  const defaultProps = {
    id: 'test-form',
    onSuccess: vi.fn()
  };

  it('renders with correct design system classes', () => {
    render(<[ComponentName] {...defaultProps} />);
    
    const button = screen.getByRole('button');
    expect(button).toHaveClass('h-12'); // Touch target
    expect(button).toHaveClass('text-size-3'); // Typography
  });

  it('shows loading state during submission', async () => {
    render(<[ComponentName] {...defaultProps} />);
    
    const button = screen.getByRole('button');
    fireEvent.click(button);
    
    expect(button).toBeDisabled();
    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
  });

  it('handles errors gracefully', async () => {
    // Mock API failure
    vi.mocked(apiClient.post).mockRejectedValueOnce(new Error('Network error'));
    
    render(<[ComponentName] {...defaultProps} />);
    
    const button = screen.getByRole('button');
    fireEvent.click(button);
    
    await waitFor(() => {
      expect(screen.getByText(/something went wrong/i)).toBeInTheDocument();
    });
  });
});
```

### Step 4: Storybook Story (Optional)
```typescript
// components/[feature]/[ComponentName].stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { [ComponentName] } from './[ComponentName]';

const meta = {
  title: 'Features/[ComponentName]',
  component: [ComponentName],
  parameters: {
    layout: 'centered',
  },
} satisfies Meta<typeof [ComponentName]>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    id: 'story-form',
    onSuccess: (data) => console.log('Success:', data),
  },
};

export const Loading: Story = {
  args: {
    ...Default.args,
  },
  play: async ({ canvasElement }) => {
    // Simulate loading state
  },
};
```

## 🧪 Validation Loops

### TypeScript Validation
```bash
# Continuous type checking
bun run typecheck

# Strict mode check
bun run typecheck:strict

# Check for any types
grep -r "any" components/[feature]/ # Should return nothing
```

### Component Testing
```bash
# Unit tests
bun run test [ComponentName].test.tsx

# Visual regression (if set up)
bun run test:visual [ComponentName]

# Accessibility
bun run test:a11y [ComponentName]
```

### Integration Testing
```bash
# With API
bun run test:integration [feature]

# E2E flow
bun run test:e2e [feature]
```

## 🚨 Common TypeScript Pitfalls

### ❌ Avoid These
```typescript
// Bad: Using any
const handleData = (data: any) => { }

// Bad: Ignoring errors
// @ts-ignore
const result = someFunction();

// Bad: Loose event types
const onClick = (e) => { }

// Bad: String literals instead of enums
const status = 'active'; // Use const enum or union types
```

### ✅ Do These Instead
```typescript
// Good: Specific types
const handleData = (data: UserData) => { }

// Good: Type assertions with checks
const result = someFunction() as ExpectedType;
if (!isExpectedType(result)) throw new Error();

// Good: Proper event types
const onClick = (e: React.MouseEvent<HTMLButtonElement>) => { }

// Good: Type safety with const
const status = 'active' as const;
// Or enum
enum Status { Active = 'active', Inactive = 'inactive' }
```

## 📋 Pre-Commit Checklist

- [ ] All props have TypeScript interfaces
- [ ] No `any` types used
- [ ] Event handlers properly typed
- [ ] Design system classes only (run `/vd`)
- [ ] Loading states for async operations
- [ ] Error boundaries implemented
- [ ] Touch targets >= 44px
- [ ] Form validation with Zod
- [ ] Analytics events non-blocking
- [ ] Component tests passing

## 🔗 Resources

- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
- Internal Types: `types/index.ts`
- Component Library: `components/ui/`

---

**Next Steps**:
1. Copy this template
2. Fill in component-specific details
3. Run `/vd` frequently during development
4. Test with `/btf` for real browser testing
