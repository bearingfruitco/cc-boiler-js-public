# CLAUDE_TYPESCRIPT.md - TypeScript-Specific Guidelines

## TypeScript Configuration

This project uses TypeScript in strict mode with these non-negotiable settings:

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

## Type Patterns

### Component Props - Always Explicit
```typescript
// ✅ CORRECT - Explicit interface
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'ghost';
  size?: 'default' | 'large' | 'small';
  onClick?: () => void;
  disabled?: boolean;
  loading?: boolean;
  children: React.ReactNode;
  className?: string;
}

// ❌ WRONG - Inline types
function Button({ variant, onClick }: { variant: string; onClick: any }) {}
```

### Event Handlers - Proper Types
```typescript
// ✅ CORRECT - Specific event types
const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
  e.preventDefault();
};

const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault();
};

const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  setValue(e.target.value);
};

// ❌ WRONG - Generic or any
const handleClick = (e: any) => {};
const handleSubmit = (e) => {};
```

### API Responses - Type Everything
```typescript
// ✅ CORRECT - Full typing with Zod
import { z } from 'zod';

// Define schema
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(1),
  createdAt: z.string().datetime(),
});

type User = z.infer<typeof UserSchema>;

// Use in API
async function getUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  const data = await response.json();
  
  // Validate at runtime
  return UserSchema.parse(data);
}

// ❌ WRONG - Untyped or partial
async function getUser(id: string) {
  const response = await fetch(`/api/users/${id}`);
  return response.json(); // Return type is 'any'
}
```

### Form Data - Validated Types
```typescript
// ✅ CORRECT - Form with validation
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const FormSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email'),
  age: z.number().min(18, 'Must be 18 or older'),
});

type FormData = z.infer<typeof FormSchema>;

function MyForm() {
  const form = useForm<FormData>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      name: '',
      email: '',
      age: 18,
    },
  });
  
  const onSubmit = (data: FormData) => {
    // data is fully typed and validated
  };
}
```

### Database Types - From Schema
```typescript
// ✅ CORRECT - Generated from Supabase
import { Database } from '@/types/supabase';

type Tables = Database['public']['Tables'];
type User = Tables['users']['Row'];
type InsertUser = Tables['users']['Insert'];
type UpdateUser = Tables['users']['Update'];

// Type-safe queries
const getUsers = async (): Promise<User[]> => {
  const { data, error } = await supabase
    .from('users')
    .select('*');
    
  if (error) throw error;
  return data;
};
```

## Common Anti-Patterns to Avoid

### 1. Never Use `any`
```typescript
// ❌ WRONG
const processData = (data: any) => {
  return data.map((item: any) => item.value);
};

// ✅ CORRECT
interface DataItem {
  id: string;
  value: number;
}

const processData = (data: DataItem[]) => {
  return data.map(item => item.value);
};
```

### 2. Never Use `@ts-ignore`
```typescript
// ❌ WRONG
// @ts-ignore
const result = someFunction();

// ✅ CORRECT - Fix the type issue
const result = someFunction() as ExpectedType;
// Or better: fix someFunction to return correct type
```

### 3. Never Use Non-Null Assertion Without Checks
```typescript
// ❌ WRONG
const value = possiblyNull!.property;

// ✅ CORRECT
if (possiblyNull) {
  const value = possiblyNull.property;
}
// Or
const value = possiblyNull?.property ?? defaultValue;
```

### 4. Always Handle Union Types
```typescript
// ❌ WRONG
function processStatus(status: 'success' | 'error' | 'pending') {
  if (status === 'success') {
    return 'Done';
  }
  // Missing cases!
}

// ✅ CORRECT - Exhaustive handling
function processStatus(status: 'success' | 'error' | 'pending') {
  switch (status) {
    case 'success':
      return 'Done';
    case 'error':
      return 'Failed';
    case 'pending':
      return 'Processing';
    default:
      // This ensures all cases are handled
      const _exhaustive: never = status;
      return _exhaustive;
  }
}
```

## Utility Types

### Use Built-in Utilities
```typescript
// Partial - Make all properties optional
type PartialUser = Partial<User>;

// Required - Make all properties required
type RequiredUser = Required<User>;

// Pick - Select specific properties
type UserName = Pick<User, 'id' | 'name'>;

// Omit - Exclude specific properties
type UserWithoutPassword = Omit<User, 'password'>;

// Record - Create object type with known keys
type UserRoles = Record<string, 'admin' | 'user' | 'guest'>;

// Readonly - Make all properties readonly
type ReadonlyUser = Readonly<User>;
```

### Custom Utility Types
```typescript
// Make specific properties optional
type PartialBy<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

// Make specific properties required
type RequiredBy<T, K extends keyof T> = T & Required<Pick<T, K>>;

// Deep partial
type DeepPartial<T> = T extends object ? {
  [P in keyof T]?: DeepPartial<T[P]>;
} : T;

// Async function return type
type AsyncReturnType<T extends (...args: any) => Promise<any>> = 
  T extends (...args: any) => Promise<infer R> ? R : never;
```

## Generic Components

### Properly Typed Generic Components
```typescript
// ✅ CORRECT - Generic list component
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  keyExtractor: (item: T) => string;
  onItemClick?: (item: T) => void;
}

function List<T>({ items, renderItem, keyExtractor, onItemClick }: ListProps<T>) {
  return (
    <ul>
      {items.map(item => (
        <li 
          key={keyExtractor(item)}
          onClick={() => onItemClick?.(item)}
        >
          {renderItem(item)}
        </li>
      ))}
    </ul>
  );
}

// Usage
<List
  items={users}
  renderItem={(user) => <span>{user.name}</span>}
  keyExtractor={(user) => user.id}
  onItemClick={(user) => console.log(user.id)}
/>
```

## Async Patterns

### Proper Error Handling
```typescript
// ✅ CORRECT - Type-safe error handling
class ApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public code?: string
  ) {
    super(message);
  }
}

async function fetchData<T>(url: string): Promise<T> {
  try {
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new ApiError(
        'Request failed',
        response.status,
        'FETCH_ERROR'
      );
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      // Handle API errors
      console.error(`API Error ${error.statusCode}: ${error.message}`);
    } else if (error instanceof Error) {
      // Handle other errors
      console.error(`Error: ${error.message}`);
    }
    throw error;
  }
}
```

## Type Guards

### Creating Type Guards
```typescript
// User-defined type guards
function isString(value: unknown): value is string {
  return typeof value === 'string';
}

function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'email' in value &&
    'name' in value
  );
}

// Using type guards
function processValue(value: unknown) {
  if (isString(value)) {
    // value is typed as string here
    return value.toUpperCase();
  }
  
  if (isUser(value)) {
    // value is typed as User here
    return value.email;
  }
  
  throw new Error('Invalid value type');
}
```

## Module Augmentation

### Extending Third-Party Types
```typescript
// types/next-auth.d.ts
import NextAuth from 'next-auth';

declare module 'next-auth' {
  interface Session {
    user: {
      id: string;
      email: string;
      name: string;
      role: 'admin' | 'user';
    };
  }
}

// types/react.d.ts
import 'react';

declare module 'react' {
  interface CSSProperties {
    '--custom-property'?: string;
  }
}
```

## Testing Types

### Type-Safe Tests
```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

// Mock with proper types
const mockOnClick = jest.fn<void, [User]>();

// Type component props in tests
const defaultProps: ButtonProps = {
  variant: 'primary',
  onClick: mockOnClick,
  children: 'Click me',
};

test('button click', async () => {
  const user = userEvent.setup();
  render(<Button {...defaultProps} />);
  
  await user.click(screen.getByRole('button'));
  
  expect(mockOnClick).toHaveBeenCalledTimes(1);
});
```

## Performance Considerations

### Const Assertions
```typescript
// Use 'as const' for literal types
const COLORS = {
  primary: '#007bff',
  secondary: '#6c757d',
  success: '#28a745',
} as const;

type Color = typeof COLORS[keyof typeof COLORS];
// Type is: '#007bff' | '#6c757d' | '#28a745'
```

### Type-Only Imports
```typescript
// Use type-only imports when possible
import type { User } from './types';
import { type UserRole, processUser } from './user';

// This helps with tree-shaking and build performance
```

## Remember

1. **No `any`** - Ever. Use `unknown` if truly unknown
2. **No `@ts-ignore`** - Fix the issue properly
3. **Explicit is better than implicit** - Define all types
4. **Validate external data** - Use Zod for runtime validation
5. **Use strict mode** - Always
6. **Type everything** - Props, events, API responses, errors

The TypeScript compiler is your friend. If it complains, fix it properly - don't silence it.
