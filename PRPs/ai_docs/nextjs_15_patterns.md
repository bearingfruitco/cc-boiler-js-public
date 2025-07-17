# Next.js 15 Patterns - AI Reference

## Server Components by Default

```typescript
// ❌ Old pattern - client component for no reason
'use client';
export function UserList({ users }) {
  return users.map(u => <div>{u.name}</div>);
}

// ✅ New pattern - server component by default
export function UserList({ users }) {
  return users.map(u => <div>{u.name}</div>);
}

// ✅ Only use client when needed
'use client';
export function InteractiveButton() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

## Async Components Pattern

```typescript
// ✅ Direct async in server components
export async function UserProfile({ id }: { id: string }) {
  const user = await getUser(id);
  return <ProfileCard user={user} />;
}

// ✅ No useEffect for data fetching
export async function PostList() {
  const posts = await db.posts.findMany();
  return <div>{posts.map(p => <PostCard key={p.id} post={p} />)}</div>;
}
```

## Parallel Data Fetching

```typescript
// ❌ Sequential fetches
export async function Dashboard() {
  const user = await getUser();
  const posts = await getPosts(user.id);
  const stats = await getStats(user.id);
  // Takes sum of all request times
}

// ✅ Parallel fetches with Promise.all
export async function Dashboard() {
  const [user, posts, stats] = await Promise.all([
    getUser(),
    getPosts(),
    getStats()
  ]);
  // Takes time of slowest request only
  
  return <DashboardLayout {...{user, posts, stats}} />;
}
```

## Server Actions

```typescript
// ✅ Form actions without API routes
async function updateProfile(formData: FormData) {
  'use server';
  
  // Validate
  const name = formData.get('name');
  if (!name || typeof name !== 'string') {
    throw new Error('Name is required');
  }
  
  // Update database
  await db.user.update({
    where: { id: getSessionUserId() },
    data: { name }
  });
  
  // Revalidate cache
  revalidatePath('/profile');
}

export function ProfileForm({ user }) {
  return (
    <form action={updateProfile}>
      <input name="name" defaultValue={user.name} />
      <button type="submit">Update</button>
    </form>
  );
}
```

## Loading & Error Boundaries

```typescript
// app/dashboard/loading.tsx
export default function Loading() {
  return (
    <div className="grid gap-4">
      <div className="h-32 animate-pulse bg-gray-100 rounded-xl" />
      <div className="h-48 animate-pulse bg-gray-100 rounded-xl" />
    </div>
  );
}

// app/dashboard/error.tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="p-4 bg-red-50 rounded-xl">
      <h2 className="text-size-2 font-semibold text-red-900">
        Something went wrong!
      </h2>
      <p className="text-size-3 text-red-700">{error.message}</p>
      <button
        onClick={reset}
        className="mt-4 px-4 py-2 bg-red-600 text-white rounded-xl"
      >
        Try again
      </button>
    </div>
  );
}
```

## Metadata API

```typescript
// ✅ Static metadata
export const metadata = {
  title: 'My App',
  description: 'Welcome to my app',
};

// ✅ Dynamic metadata
export async function generateMetadata({ params }: Props) {
  const product = await getProduct(params.id);
  
  return {
    title: product.name,
    description: product.description,
    openGraph: {
      images: [product.image],
    },
  };
}
```

## Route Handlers

```typescript
// app/api/webhook/route.ts
import { headers } from 'next/headers';

export async function POST(request: Request) {
  // Get headers
  const headersList = await headers();
  const signature = headersList.get('x-webhook-signature');
  
  // Get body
  const body = await request.json();
  
  // Process webhook
  await processWebhook(body, signature);
  
  return Response.json({ received: true });
}
```

## Streaming & Suspense

```typescript
// ✅ Stream parts of the page as they're ready
import { Suspense } from 'react';

export default function Page() {
  return (
    <>
      <Header /> {/* Renders immediately */}
      
      <Suspense fallback={<PostsSkeleton />}>
        <Posts /> {/* Async component - streams when ready */}
      </Suspense>
      
      <Suspense fallback={<CommentsSkeleton />}>
        <Comments /> {/* Another async component */}
      </Suspense>
    </>
  );
}
```

## Common Gotchas

### 1. No `useEffect` in Server Components
```typescript
// ❌ This won't work
export function ServerComponent() {
  useEffect(() => {
    // Server components don't run in browser
  }, []);
}

// ✅ Use async directly
export async function ServerComponent() {
  const data = await fetchData();
  return <div>{data}</div>;
}
```

### 2. Headers/Cookies are Async
```typescript
// ❌ Old way
import { cookies } from 'next/headers';
const theme = cookies().get('theme');

// ✅ New way - await required
import { cookies } from 'next/headers';
const cookieStore = await cookies();
const theme = cookieStore.get('theme');
```

### 3. Dynamic Imports for Client-Only
```typescript
// ✅ For client-only libraries
import dynamic from 'next/dynamic';

const Chart = dynamic(() => import('react-chartjs-2'), {
  ssr: false,
  loading: () => <div>Loading chart...</div>
});
```

### 4. Hydration Mismatches
```typescript
// ❌ Can cause hydration errors
export function TimeDisplay() {
  return <div>{new Date().toLocaleTimeString()}</div>;
}

// ✅ Use useEffect for client-only values
'use client';
export function TimeDisplay() {
  const [time, setTime] = useState<string>('');
  
  useEffect(() => {
    setTime(new Date().toLocaleTimeString());
  }, []);
  
  return <div>{time || 'Loading...'}</div>;
}
```

### 5. Environment Variables
```typescript
// Server components have access to all env vars
const apiKey = process.env.SECRET_API_KEY; // ✅ Works

// Client components only see NEXT_PUBLIC_ vars
const publicKey = process.env.NEXT_PUBLIC_API_KEY; // ✅ Works
const secretKey = process.env.SECRET_API_KEY; // ❌ undefined
```

## Performance Tips

1. **Minimize Client Components**: Only what needs interactivity
2. **Use Streaming**: Suspense boundaries for slow data
3. **Parallel Fetches**: Always use Promise.all when possible
4. **Static When Possible**: Use generateStaticParams
5. **Image Optimization**: Always use next/image
6. **Font Optimization**: Use next/font

## Testing Patterns

```typescript
// Test server components
import { render } from '@testing-library/react';

test('renders user profile', async () => {
  // Mock the async function
  jest.mocked(getUser).mockResolvedValue({
    name: 'Test User'
  });
  
  // Await the component
  const component = await UserProfile({ id: '123' });
  const { getByText } = render(component);
  
  expect(getByText('Test User')).toBeInTheDocument();
});
```
