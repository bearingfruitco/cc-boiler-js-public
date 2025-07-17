# Supabase Patterns - AI Reference

## Authentication Patterns

### Client-Side Auth Setup
```typescript
// lib/supabase/client.ts
import { createBrowserClient } from '@supabase/ssr';

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}
```

### Server-Side Auth Setup
```typescript
// lib/supabase/server.ts
import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';

export async function createClient() {
  const cookieStore = await cookies();
  
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) => {
            cookieStore.set(name, value, options);
          });
        },
      },
    }
  );
}
```

### Auth Flow Patterns

#### Sign Up
```typescript
// app/auth/signup/route.ts
export async function POST(request: Request) {
  const formData = await request.formData();
  const email = formData.get('email') as string;
  const password = formData.get('password') as string;
  
  const supabase = await createClient();
  
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      emailRedirectTo: `${process.env.NEXT_PUBLIC_SITE_URL}/auth/callback`,
    },
  });
  
  if (error) {
    return redirect('/signup?error=Could not create user');
  }
  
  return redirect('/signup?message=Check email to continue');
}
```

#### Sign In
```typescript
// app/auth/signin/route.ts
export async function POST(request: Request) {
  const formData = await request.formData();
  const email = formData.get('email') as string;
  const password = formData.get('password') as string;
  
  const supabase = await createClient();
  
  const { error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });
  
  if (error) {
    return redirect('/login?error=Invalid credentials');
  }
  
  return redirect('/dashboard');
}
```

#### Protected Routes
```typescript
// app/(protected)/layout.tsx
export default async function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const supabase = await createClient();
  
  const { data: { user } } = await supabase.auth.getUser();
  
  if (!user) {
    return redirect('/login');
  }
  
  return <>{children}</>;
}
```

## Database Patterns

### Type-Safe Queries with Generated Types
```typescript
// First, generate types:
// npx supabase gen types typescript --project-id your-project > types/supabase.ts

import { Database } from '@/types/supabase';

type Profile = Database['public']['Tables']['profiles']['Row'];
type InsertProfile = Database['public']['Tables']['profiles']['Insert'];
type UpdateProfile = Database['public']['Tables']['profiles']['Update'];
```

### CRUD Operations

#### Select with Relations
```typescript
// Fetch user with profile
const { data, error } = await supabase
  .from('users')
  .select(`
    *,
    profile:profiles(*)
  `)
  .eq('id', userId)
  .single();

// Fetch posts with author info
const { data: posts } = await supabase
  .from('posts')
  .select(`
    *,
    author:users(
      id,
      name,
      avatar_url
    )
  `)
  .order('created_at', { ascending: false })
  .limit(10);
```

#### Insert with RLS
```typescript
// Insert with automatic user association
const { data, error } = await supabase
  .from('posts')
  .insert({
    title: 'My Post',
    content: 'Content here',
    // user_id automatically set by RLS policy
  })
  .select()
  .single();

if (error) throw error;
```

#### Update with Optimistic UI
```typescript
// In a React component
const updatePost = async (id: string, updates: UpdatePost) => {
  // Optimistic update
  setPost(current => ({ ...current, ...updates }));
  
  const { error } = await supabase
    .from('posts')
    .update(updates)
    .eq('id', id)
    .eq('user_id', user.id); // Extra safety
  
  if (error) {
    // Revert on error
    setPost(originalPost);
    toast.error('Failed to update');
  }
};
```

#### Delete with Soft Delete
```typescript
// Soft delete pattern
const { error } = await supabase
  .from('posts')
  .update({ deleted_at: new Date().toISOString() })
  .eq('id', postId);

// Hard delete
const { error } = await supabase
  .from('posts')
  .delete()
  .eq('id', postId);
```

## Row Level Security (RLS) Patterns

### Basic RLS Policies
```sql
-- Enable RLS
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Users can only see their own posts
CREATE POLICY "Users can view own posts" ON posts
  FOR SELECT USING (auth.uid() = user_id);

-- Users can only insert their own posts
CREATE POLICY "Users can insert own posts" ON posts
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Users can only update their own posts
CREATE POLICY "Users can update own posts" ON posts
  FOR UPDATE USING (auth.uid() = user_id);

-- Users can only delete their own posts
CREATE POLICY "Users can delete own posts" ON posts
  FOR DELETE USING (auth.uid() = user_id);
```

### Public Read Pattern
```sql
-- Anyone can read published posts
CREATE POLICY "Public can view published posts" ON posts
  FOR SELECT USING (
    published = true 
    AND deleted_at IS NULL
  );

-- Authors can see all their posts
CREATE POLICY "Authors can view own posts" ON posts
  FOR SELECT USING (auth.uid() = user_id);
```

### Role-Based Access
```sql
-- Check user role from profiles table
CREATE POLICY "Admins can do anything" ON posts
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'admin'
    )
  );
```

## Real-Time Subscriptions

### Subscribe to Changes
```typescript
// Subscribe to new posts
useEffect(() => {
  const subscription = supabase
    .channel('posts')
    .on(
      'postgres_changes',
      {
        event: 'INSERT',
        schema: 'public',
        table: 'posts',
      },
      (payload) => {
        setPosts(current => [payload.new as Post, ...current]);
      }
    )
    .subscribe();
  
  return () => {
    subscription.unsubscribe();
  };
}, []);

// Subscribe to specific record updates
useEffect(() => {
  const subscription = supabase
    .channel(`post:${postId}`)
    .on(
      'postgres_changes',
      {
        event: 'UPDATE',
        schema: 'public',
        table: 'posts',
        filter: `id=eq.${postId}`,
      },
      (payload) => {
        setPost(payload.new as Post);
      }
    )
    .subscribe();
  
  return () => {
    subscription.unsubscribe();
  };
}, [postId]);
```

### Presence (Who's Online)
```typescript
// Track online users
const channel = supabase.channel('online-users');

channel
  .on('presence', { event: 'sync' }, () => {
    const state = channel.presenceState();
    setOnlineUsers(Object.keys(state).length);
  })
  .subscribe(async (status) => {
    if (status === 'SUBSCRIBED') {
      await channel.track({
        user_id: user.id,
        online_at: new Date().toISOString(),
      });
    }
  });
```

## Storage Patterns

### Upload Files
```typescript
// Upload avatar
const uploadAvatar = async (file: File) => {
  const fileExt = file.name.split('.').pop();
  const fileName = `${user.id}/avatar-${Date.now()}.${fileExt}`;
  
  const { data, error } = await supabase.storage
    .from('avatars')
    .upload(fileName, file, {
      cacheControl: '3600',
      upsert: true,
    });
  
  if (error) throw error;
  
  // Get public URL
  const { data: { publicUrl } } = supabase.storage
    .from('avatars')
    .getPublicUrl(fileName);
  
  // Update user profile
  await supabase
    .from('profiles')
    .update({ avatar_url: publicUrl })
    .eq('id', user.id);
  
  return publicUrl;
};
```

### Storage Policies
```sql
-- Users can upload their own avatars
CREATE POLICY "Users can upload own avatar" ON storage.objects
  FOR INSERT WITH CHECK (
    bucket_id = 'avatars' AND
    (storage.foldername(name))[1] = auth.uid()::text
  );

-- Anyone can view avatars
CREATE POLICY "Avatars are publicly accessible" ON storage.objects
  FOR SELECT USING (bucket_id = 'avatars');
```

## Error Handling Patterns

### Typed Error Handling
```typescript
import { PostgrestError } from '@supabase/supabase-js';

const handleSupabaseError = (error: PostgrestError) => {
  // Check for specific error codes
  switch (error.code) {
    case '23505': // Unique violation
      return 'This record already exists';
    case '23503': // Foreign key violation
      return 'Related record not found';
    case '23502': // Not null violation
      return 'Required field missing';
    case 'PGRST116': // RLS violation
      return 'You do not have permission';
    default:
      return error.message;
  }
};
```

### Retry Logic
```typescript
const retryOperation = async <T>(
  operation: () => Promise<T>,
  maxRetries = 3
): Promise<T> => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await operation();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      
      // Exponential backoff
      await new Promise(resolve => 
        setTimeout(resolve, Math.pow(2, i) * 1000)
      );
    }
  }
  throw new Error('Max retries reached');
};

// Usage
const data = await retryOperation(() =>
  supabase.from('posts').select('*')
);
```

## Performance Optimization

### Query Optimization
```typescript
// ❌ N+1 query problem
const posts = await supabase.from('posts').select('*');
for (const post of posts.data) {
  const author = await supabase
    .from('users')
    .select('*')
    .eq('id', post.user_id)
    .single();
}

// ✅ Single query with join
const { data: posts } = await supabase
  .from('posts')
  .select(`
    *,
    author:users(id, name, avatar_url)
  `);
```

### Pagination
```typescript
// Cursor-based pagination
const PAGE_SIZE = 10;

const fetchPage = async (cursor?: string) => {
  let query = supabase
    .from('posts')
    .select('*')
    .order('created_at', { ascending: false })
    .limit(PAGE_SIZE);
  
  if (cursor) {
    query = query.lt('created_at', cursor);
  }
  
  const { data, error } = await query;
  
  return {
    posts: data || [],
    nextCursor: data?.[data.length - 1]?.created_at,
    hasMore: data?.length === PAGE_SIZE,
  };
};
```

## Common Gotchas

1. **RLS is not enabled by default** - Always enable it
2. **Anon key is public** - Never use service key client-side
3. **Timestamps need timezone** - Use `timestamptz` not `timestamp`
4. **Realtime needs replica identity** - Set for tables with subscriptions
5. **Storage URLs change** - Store path, generate URL dynamically
6. **Auth cookies need proper config** - Server/client setup differs
