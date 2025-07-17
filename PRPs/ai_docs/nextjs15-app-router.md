# Next.js 15 App Router - AI Context Document

> Critical patterns and gotchas for Next.js 15 App Router development

## Server Components vs Client Components

### Default: Server Components
```typescript
// This is a Server Component by default
// ✅ Can fetch data directly
// ✅ Can access backend resources
// ❌ No useState, useEffect, or browser APIs
export default async function Page() {
  const data = await fetchData(); // Direct async/await
  return <div>{data}</div>;
}
```

### Client Components: 'use client'
```typescript
'use client'; // Required directive at top

// ✅ Can use hooks and browser APIs
// ✅ Can have interactivity
// ❌ Cannot be async
// ❌ Increases bundle size
export default function Interactive() {
  const [state, setState] = useState();
  return <button onClick={() => setState(true)}>Click</button>;
}
```

## Data Fetching Patterns

### Parallel Data Fetching (Recommended)
```typescript
// ✅ Fetch in parallel for better performance
export default async function Page() {
  const [user, posts, settings] = await Promise.all([
    fetchUser(),
    fetchPosts(),
    fetchSettings()
  ]);
  
  return <>{/* render */}</>;
}
```

### Sequential Fetching (Avoid)
```typescript
// ❌ Slower - each awaits completion
export default async function Page() {
  const user = await fetchUser();
  const posts = await fetchPosts(); // Waits for user
  const settings = await fetchSettings(); // Waits for posts
}
```

## Form Handling with Server Actions

### Server Action Pattern
```typescript
// app/actions.ts
'use server';

export async function submitForm(formData: FormData) {
  // Validate on server
  const data = Object.fromEntries(formData);
  
  // Process (runs on server)
  await saveToDatabase(data);
  
  // Revalidate cache
  revalidatePath('/');
}

// app/form.tsx
export function Form() {
  return (
    <form action={submitForm}>
      <input name="email" type="email" required />
      <button type="submit">Submit</button>
    </form>
  );
}
```

## Error Handling

### Error Boundary (error.tsx)
```typescript
'use client'; // Error boundaries must be client components

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

## Loading States

### Loading UI (loading.tsx)
```typescript
export default function Loading() {
  // Automatically shown while page is loading
  return <LoadingSpinner />;
}
```

### Suspense for Components
```typescript
import { Suspense } from 'react';

export default function Page() {
  return (
    <Suspense fallback={<Loading />}>
      <AsyncComponent />
    </Suspense>
  );
}
```

## Route Handlers (API Routes)

### New Route Handler Pattern
```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const id = searchParams.get('id');
  
  return NextResponse.json({ id });
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  
  return NextResponse.json(
    { message: 'Created' },
    { status: 201 }
  );
}
```

## Metadata

### Static Metadata
```typescript
export const metadata = {
  title: 'Page Title',
  description: 'Page description',
};
```

### Dynamic Metadata
```typescript
export async function generateMetadata({ params }) {
  const product = await fetchProduct(params.id);
  
  return {
    title: product.name,
    description: product.description,
  };
}
```

## Common Gotchas

### 1. Hydration Errors
```typescript
// ❌ Causes hydration mismatch
export default function Problem() {
  return <div>{new Date().toISOString()}</div>;
}

// ✅ Use useEffect for client-only values
'use client';
export default function Fixed() {
  const [date, setDate] = useState<string>('');
  
  useEffect(() => {
    setDate(new Date().toISOString());
  }, []);
  
  return <div>{date}</div>;
}
```

### 2. Using Browser APIs in Server Components
```typescript
// ❌ Will error - window is not defined
export default function ServerComponent() {
  const width = window.innerWidth; // ERROR!
}

// ✅ Move to client component
'use client';
export default function ClientComponent() {
  const [width, setWidth] = useState(0);
  
  useEffect(() => {
    setWidth(window.innerWidth);
  }, []);
}
```

### 3. Importing Client Components in Server Components
```typescript
// ✅ You CAN import and render client components in server components
import ClientButton from './ClientButton'; // has 'use client'

export default function ServerComponent() {
  return (
    <div>
      <h1>Server Rendered</h1>
      <ClientButton /> {/* This works! */}
    </div>
  );
}

// ❌ You CANNOT pass functions as props from server to client
export default function ServerComponent() {
  const serverFunction = () => {}; // Defined on server
  
  return (
    <ClientButton onClick={serverFunction} /> // ERROR!
  );
}
```

## Performance Tips

### 1. Minimize Client Components
- Default to server components
- Only use 'use client' when needed for interactivity
- Extract interactive parts into small client components

### 2. Optimize Images
```typescript
import Image from 'next/image';

// Automatic optimization
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority // Load immediately for above-fold
/>
```

### 3. Font Optimization
```typescript
import { Inter } from 'next/font/google';

const inter = Inter({ 
  subsets: ['latin'],
  display: 'swap', // Prevent layout shift
});
```

## Testing Patterns

### Server Component Testing
```typescript
// Can test server components directly
import { render } from '@testing-library/react';
import Page from '@/app/page';

test('renders page', async () => {
  const { getByText } = render(await Page());
  expect(getByText('Welcome')).toBeInTheDocument();
});
```

### Client Component Testing
```typescript
// Standard React testing
import { render, fireEvent } from '@testing-library/react';
import Button from '@/components/Button';

test('handles click', () => {
  const onClick = jest.fn();
  const { getByRole } = render(<Button onClick={onClick} />);
  
  fireEvent.click(getByRole('button'));
  expect(onClick).toHaveBeenCalled();
});
```

## Security Considerations

### 1. Environment Variables
```typescript
// Server-only (without NEXT_PUBLIC_)
const apiKey = process.env.API_KEY; // Only on server

// Client-accessible (with NEXT_PUBLIC_)
const publicKey = process.env.NEXT_PUBLIC_KEY; // Available everywhere
```

### 2. Server Actions Security
```typescript
'use server';

import { auth } from '@/lib/auth';

export async function secureAction(data: FormData) {
  // Always validate on server
  const session = await auth();
  if (!session) throw new Error('Unauthorized');
  
  // Validate input
  const validated = schema.parse(data);
  
  // Process securely
}
```

## Debugging Tips

### 1. Check Component Type
```typescript
// Add temporary console logs
console.log('Rendering on:', typeof window === 'undefined' ? 'server' : 'client');
```

### 2. Use React DevTools
- Install browser extension
- Check component tree
- Identify server vs client components

### 3. Network Tab
- Server components: HTML in initial response
- Client components: Separate JS chunks

## Remember
- Server Components = Default, fast, secure
- Client Components = Interactive, larger bundle
- Always validate on server
- Handle errors gracefully
- Optimize for performance
