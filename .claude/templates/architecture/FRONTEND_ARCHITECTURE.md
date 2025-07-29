# Frontend Architecture - [Project Name]

## Overview

This document defines the frontend architecture including component structure, state management, routing, and UI/UX patterns.

## Technology Stack

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript 5.x
- **Styling**: Tailwind CSS with custom design system
- **State Management**: Zustand + React Query
- **Forms**: React Hook Form + Zod
- **UI Components**: Shadcn/ui + custom components
- **Testing**: Vitest + React Testing Library
- **Animation**: Framer Motion

## Architecture Principles

1. **Component-Driven Development** - Build from atoms up
2. **Type Safety First** - Leverage TypeScript fully
3. **Performance by Default** - SSG/SSR where appropriate
4. **Accessibility Always** - WCAG 2.1 AA compliance
5. **Mobile-First Design** - Progressive enhancement
6. **Design System Strict** - 4 sizes, 2 weights, 4px grid

## Project Structure

```
app/                          # Next.js App Router
├── (public)/                # Public routes (no auth)
│   ├── page.tsx            # Landing page
│   ├── about/              # About pages
│   └── layout.tsx          # Public layout
├── (protected)/             # Protected routes (auth required)
│   ├── dashboard/          # Dashboard pages
│   ├── settings/           # Settings pages
│   └── layout.tsx          # Protected layout
├── api/                     # API routes
│   └── [...]/route.ts      # API endpoints
└── layout.tsx              # Root layout

components/                   # React components
├── ui/                      # Base UI components (Shadcn)
│   ├── button.tsx
│   ├── card.tsx
│   └── ...
├── features/                # Feature-specific components
│   ├── auth/               # Authentication components
│   ├── dashboard/          # Dashboard components
│   └── [feature]/          # Other features
├── forms/                   # Form components
│   ├── fields/             # Reusable form fields
│   └── [feature]-form.tsx  # Feature forms
└── layouts/                 # Layout components
    ├── header.tsx
    ├── footer.tsx
    └── sidebar.tsx

lib/                         # Utilities and helpers
├── api/                     # API client functions
├── hooks/                   # Custom React hooks
├── utils/                   # Utility functions
├── validations/            # Zod schemas
└── types/                  # TypeScript types

stores/                      # Zustand stores
├── auth-store.ts
├── ui-store.ts
└── [feature]-store.ts
```

## Component Architecture

### Component Hierarchy
```
App
├── Layout
│   ├── Header
│   ├── Sidebar (if applicable)
│   └── Footer
├── Page
│   ├── PageHeader
│   ├── PageContent
│   │   ├── Feature Components
│   │   └── UI Components
│   └── PageActions
└── Providers
    ├── ThemeProvider
    ├── AuthProvider
    └── QueryProvider
```

### Component Patterns

#### Base Component Template
```typescript
// components/features/[feature]/[component].tsx
import { cn } from '@/lib/utils'

interface ComponentProps {
  className?: string
  children?: React.ReactNode
  // Add specific props
}

export function Component({ 
  className,
  children,
  ...props 
}: ComponentProps) {
  return (
    <div className={cn(
      "base-styles",
      className
    )}>
      {children}
    </div>
  )
}
```

#### Feature Component Structure
```typescript
// components/features/[feature]/index.tsx
export { FeatureList } from './feature-list'
export { FeatureItem } from './feature-item'
export { FeatureForm } from './feature-form'
export { FeatureDetails } from './feature-details'
```

### Design System Components

#### Typography
```typescript
// Strict typography components enforcing design system
export function Heading1({ children, className }: HeadingProps) {
  return (
    <h1 className={cn("text-size-1 font-semibold", className)}>
      {children}
    </h1>
  )
}

export function BodyText({ children, className }: TextProps) {
  return (
    <p className={cn("text-size-3 font-regular", className)}>
      {children}
    </p>
  )
}
```

#### Layout Components
```typescript
// Consistent spacing with 4px grid
export function Section({ children, className }: SectionProps) {
  return (
    <section className={cn("p-4 md:p-6 lg:p-8", className)}>
      {children}
    </section>
  )
}

export function Container({ children, className }: ContainerProps) {
  return (
    <div className={cn("max-w-7xl mx-auto px-4", className)}>
      {children}
    </div>
  )
}
```

## State Management

### Client State (Zustand)
```typescript
// stores/ui-store.ts
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

interface UIState {
  sidebarOpen: boolean
  theme: 'light' | 'dark'
  toggleSidebar: () => void
  setTheme: (theme: 'light' | 'dark') => void
}

export const useUIStore = create<UIState>()(
  devtools(
    persist(
      (set) => ({
        sidebarOpen: false,
        theme: 'light',
        toggleSidebar: () => set((state) => ({ 
          sidebarOpen: !state.sidebarOpen 
        })),
        setTheme: (theme) => set({ theme }),
      }),
      { name: 'ui-store' }
    )
  )
)
```

### Server State (React Query)
```typescript
// lib/hooks/use-resources.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api'

export function useResources() {
  return useQuery({
    queryKey: ['resources'],
    queryFn: api.resources.list,
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

export function useCreateResource() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: api.resources.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['resources'] })
    },
  })
}
```

### Form State (React Hook Form)
```typescript
// components/forms/resource-form.tsx
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { resourceSchema } from '@/lib/validations'

export function ResourceForm({ onSubmit }: ResourceFormProps) {
  const form = useForm<ResourceFormData>({
    resolver: zodResolver(resourceSchema),
    defaultValues: {
      name: '',
      description: '',
    },
  })

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      <FormField
        control={form.control}
        name="name"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Name</FormLabel>
            <FormControl>
              <Input {...field} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )}
      />
    </form>
  )
}
```

## Routing Architecture

### Route Organization
```
app/
├── (public)/                    # No authentication required
│   ├── page.tsx                # /
│   ├── about/page.tsx          # /about
│   ├── pricing/page.tsx        # /pricing
│   └── blog/
│       ├── page.tsx            # /blog
│       └── [slug]/page.tsx     # /blog/[slug]
├── (protected)/                 # Authentication required
│   ├── dashboard/
│   │   ├── page.tsx            # /dashboard
│   │   └── analytics/page.tsx  # /dashboard/analytics
│   └── settings/
│       ├── page.tsx            # /settings
│       └── profile/page.tsx    # /settings/profile
└── api/                         # API routes
    └── v1/
        └── resources/
            └── route.ts         # /api/v1/resources
```

### Route Guards
```typescript
// app/(protected)/layout.tsx
import { redirect } from 'next/navigation'
import { getSession } from '@/lib/auth'

export default async function ProtectedLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const session = await getSession()
  
  if (!session) {
    redirect('/login')
  }

  return <>{children}</>
}
```

### Dynamic Routes
```typescript
// app/(protected)/resources/[id]/page.tsx
export async function generateStaticParams() {
  const resources = await api.resources.list()
  
  return resources.map((resource) => ({
    id: resource.id,
  }))
}

export default async function ResourcePage({
  params,
}: {
  params: { id: string }
}) {
  const resource = await api.resources.get(params.id)
  
  return <ResourceDetails resource={resource} />
}
```

## Data Fetching Patterns

### Server Components (Default)
```typescript
// app/(public)/blog/page.tsx
async function BlogPage() {
  // Fetch data on server
  const posts = await api.posts.list()
  
  return (
    <div>
      {posts.map((post) => (
        <BlogPost key={post.id} post={post} />
      ))}
    </div>
  )
}
```

### Client Components (Interactive)
```typescript
// components/features/comments/comment-list.tsx
'use client'

export function CommentList({ postId }: CommentListProps) {
  const { data: comments, isLoading } = useQuery({
    queryKey: ['comments', postId],
    queryFn: () => api.comments.list(postId),
  })

  if (isLoading) return <CommentSkeleton />
  
  return (
    <div>
      {comments?.map((comment) => (
        <Comment key={comment.id} comment={comment} />
      ))}
    </div>
  )
}
```

### Streaming (Suspense)
```typescript
// app/(public)/page.tsx
import { Suspense } from 'react'

export default function HomePage() {
  return (
    <div>
      <HeroSection />
      <Suspense fallback={<FeaturedPostsSkeleton />}>
        <FeaturedPosts />
      </Suspense>
    </div>
  )
}
```

## Performance Optimization

### Code Splitting
```typescript
// Dynamic imports for heavy components
import dynamic from 'next/dynamic'

const HeavyChart = dynamic(
  () => import('@/components/features/analytics/heavy-chart'),
  { 
    loading: () => <ChartSkeleton />,
    ssr: false 
  }
)
```

### Image Optimization
```typescript
import Image from 'next/image'

export function OptimizedImage({ src, alt }: ImageProps) {
  return (
    <Image
      src={src}
      alt={alt}
      width={800}
      height={600}
      sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
      priority={false}
      loading="lazy"
    />
  )
}
```

### Font Optimization
```typescript
// app/layout.tsx
import { Inter } from 'next/font/google'

const inter = Inter({ 
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
})

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.variable}>
      <body>{children}</body>
    </html>
  )
}
```

## Error Handling

### Error Boundaries
```typescript
// app/error.tsx
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="text-center">
        <h2 className="text-size-2 font-semibold">Something went wrong!</h2>
        <button
          onClick={reset}
          className="mt-4 rounded-xl bg-blue-600 px-4 py-2 text-white"
        >
          Try again
        </button>
      </div>
    </div>
  )
}
```

### Loading States
```typescript
// components/ui/skeleton.tsx
export function Skeleton({ className }: SkeletonProps) {
  return (
    <div
      className={cn(
        "animate-pulse rounded-md bg-gray-100",
        className
      )}
    />
  )
}

// Usage
export function PostSkeleton() {
  return (
    <div className="space-y-3">
      <Skeleton className="h-6 w-3/4" />
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-5/6" />
    </div>
  )
}
```

## Testing Strategy

### Unit Tests
```typescript
// components/ui/button.test.tsx
import { render, screen } from '@testing-library/react'
import { Button } from './button'

describe('Button', () => {
  it('renders children correctly', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('applies correct styles for primary variant', () => {
    render(<Button variant="primary">Test</Button>)
    const button = screen.getByRole('button')
    expect(button).toHaveClass('bg-blue-600')
  })
})
```

### Integration Tests
```typescript
// __tests__/features/auth/login.test.tsx
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { LoginForm } from '@/components/features/auth/login-form'

describe('Login Flow', () => {
  it('logs in user successfully', async () => {
    const user = userEvent.setup()
    render(<LoginForm />)
    
    await user.type(screen.getByLabelText('Email'), 'test@example.com')
    await user.type(screen.getByLabelText('Password'), 'password123')
    await user.click(screen.getByRole('button', { name: 'Sign in' }))
    
    await waitFor(() => {
      expect(window.location.pathname).toBe('/dashboard')
    })
  })
})
```

## Accessibility

### ARIA Patterns
```typescript
// components/ui/modal.tsx
export function Modal({ isOpen, onClose, children }: ModalProps) {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent
        role="dialog"
        aria-labelledby="modal-title"
        aria-describedby="modal-description"
      >
        {children}
      </DialogContent>
    </Dialog>
  )
}
```

### Keyboard Navigation
```typescript
// hooks/use-keyboard-navigation.ts
export function useKeyboardNavigation(items: string[]) {
  const [focusedIndex, setFocusedIndex] = useState(0)

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      switch (e.key) {
        case 'ArrowDown':
          e.preventDefault()
          setFocusedIndex((prev) => 
            prev < items.length - 1 ? prev + 1 : 0
          )
          break
        case 'ArrowUp':
          e.preventDefault()
          setFocusedIndex((prev) => 
            prev > 0 ? prev - 1 : items.length - 1
          )
          break
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [items.length])

  return focusedIndex
}
```

## Build & Deployment

### Build Configuration
```javascript
// next.config.js
module.exports = {
  output: 'standalone',
  images: {
    domains: ['your-cdn.com'],
    formats: ['image/avif', 'image/webp'],
  },
  experimental: {
    optimizeCss: true,
  },
}
```

### Environment Variables
```bash
# .env.example
NEXT_PUBLIC_API_URL=https://api.example.com
NEXT_PUBLIC_APP_URL=https://app.example.com
NEXT_PUBLIC_SENTRY_DSN=
```

### Performance Budgets
```javascript
// lighthouse.config.js
module.exports = {
  ci: {
    collect: {
      numberOfRuns: 3,
    },
    assert: {
      assertions: {
        'first-contentful-paint': ['error', { maxNumericValue: 1800 }],
        'interactive': ['error', { maxNumericValue: 3900 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
      },
    },
  },
}
```

## Best Practices

### Do's
- ✅ Use Server Components by default
- ✅ Implement proper loading states
- ✅ Handle errors gracefully
- ✅ Follow the design system strictly
- ✅ Write semantic HTML
- ✅ Test accessibility
- ✅ Optimize images and fonts
- ✅ Use TypeScript strictly

### Don'ts
- ❌ Don't use `any` type
- ❌ Don't ignore console errors
- ❌ Don't skip loading states
- ❌ Don't hardcode values
- ❌ Don't ignore accessibility
- ❌ Don't ship console.logs
- ❌ Don't use inline styles
- ❌ Don't violate design system
