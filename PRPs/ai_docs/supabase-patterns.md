# Supabase Patterns - AI Context Document

> Common patterns, best practices, and gotchas for Supabase integration

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

export function createClient() {
  const cookieStore = cookies();
  
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value;
        },
        set(name: string, value: string, options: any) {
          cookieStore.set({ name, value, ...options });
        },
        remove(name: string, options: any) {
          cookieStore.set({ name, value: '', ...options });
        },
      },
    }
  );
}
```

### Auth Flow Example
```typescript
// Sign up
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'password',
  options: {
    data: {
      // Custom user metadata
      full_name: 'John Doe',
    }
  }
});

// Sign in
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'password',
});

// Sign out
await supabase.auth.signOut();

// Get session
const { data: { session } } = await supabase.auth.getSession();

// Get user
const { data: { user } } = await supabase.auth.getUser();
```

## Database Patterns

### Type-Safe Database Queries
```typescript
// types/database.types.ts
export type Database = {
  public: {
    Tables: {
      posts: {
        Row: {
          id: string;
          title: string;
          content: string;
          user_id: string;
          created_at: string;
        };
        Insert: {
          id?: string;
          title: string;
          content: string;
          user_id: string;
          created_at?: string;
        };
        Update: {
          id?: string;
          title?: string;
          content?: string;
          user_id?: string;
          created_at?: string;
        };
      };
    };
  };
};

// Usage
const supabase = createClient<Database>();
const { data, error } = await supabase
  .from('posts')
  .select('*')
  .eq('user_id', userId); // Type-safe!
```

### Common Query Patterns
```typescript
// Select with joins
const { data } = await supabase
  .from('posts')
  .select(`
    *,
    author:profiles(name, avatar_url),
    comments(count)
  `)
  .order('created_at', { ascending: false })
  .limit(10);

// Insert
const { data, error } = await supabase
  .from('posts')
  .insert({
    title: 'New Post',
    content: 'Content here',
    user_id: user.id
  })
  .select()
  .single();

// Update
const { error } = await supabase
  .from('posts')
  .update({ title: 'Updated Title' })
  .eq('id', postId)
  .eq('user_id', user.id); // Security: ensure user owns the post

// Delete
const { error } = await supabase
  .from('posts')
  .delete()
  .eq('id', postId)
  .eq('user_id', user.id);

// Upsert
const { data, error } = await supabase
  .from('user_settings')
  .upsert({
    user_id: user.id,
    theme: 'dark',
    notifications: true
  })
  .select();
```

## Row Level Security (RLS)

### Basic RLS Policies
```sql
-- Enable RLS
alter table posts enable row level security;

-- Users can only see their own posts
create policy "Users can view own posts" on posts
  for select using (auth.uid() = user_id);

-- Users can only insert their own posts
create policy "Users can insert own posts" on posts
  for insert with check (auth.uid() = user_id);

-- Users can only update their own posts
create policy "Users can update own posts" on posts
  for update using (auth.uid() = user_id);

-- Users can only delete their own posts
create policy "Users can delete own posts" on posts
  for delete using (auth.uid() = user_id);
```

### Advanced RLS Patterns
```sql
-- Public read, authenticated write
create policy "Anyone can read posts" on posts
  for select using (true);

create policy "Authenticated users can create posts" on posts
  for insert with check (auth.uid() is not null);

-- Role-based access
create policy "Admins can do anything" on posts
  for all using (
    auth.uid() in (
      select user_id from user_roles
      where role = 'admin'
    )
  );

-- Time-based access
create policy "Can only edit recent posts" on posts
  for update using (
    auth.uid() = user_id AND
    created_at > now() - interval '24 hours'
  );
```

## Realtime Subscriptions

### Subscribe to Changes
```typescript
// Subscribe to all changes
const subscription = supabase
  .channel('posts-channel')
  .on(
    'postgres_changes',
    { event: '*', schema: 'public', table: 'posts' },
    (payload) => {
      console.log('Change received!', payload);
    }
  )
  .subscribe();

// Subscribe to specific events
const insertSubscription = supabase
  .channel('posts-insert')
  .on(
    'postgres_changes',
    { event: 'INSERT', schema: 'public', table: 'posts' },
    (payload) => {
      console.log('New post:', payload.new);
    }
  )
  .subscribe();

// Subscribe with filters
const userPostsSubscription = supabase
  .channel('user-posts')
  .on(
    'postgres_changes',
    {
      event: '*',
      schema: 'public',
      table: 'posts',
      filter: `user_id=eq.${user.id}`
    },
    (payload) => {
      console.log('User post changed:', payload);
    }
  )
  .subscribe();

// Cleanup
subscription.unsubscribe();
```

### Presence (Who's Online)
```typescript
const channel = supabase.channel('room-1');

// Track presence
channel
  .on('presence', { event: 'sync' }, () => {
    const state = channel.presenceState();
    console.log('Online users:', state);
  })
  .on('presence', { event: 'join' }, ({ key, newPresences }) => {
    console.log('User joined:', newPresences);
  })
  .on('presence', { event: 'leave' }, ({ key, leftPresences }) => {
    console.log('User left:', leftPresences);
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

### File Upload
```typescript
// Upload file
const { data, error } = await supabase.storage
  .from('avatars')
  .upload(`${user.id}/avatar.png`, file, {
    cacheControl: '3600',
    upsert: true
  });

// Get public URL
const { data: publicUrl } = supabase.storage
  .from('avatars')
  .getPublicUrl(`${user.id}/avatar.png`);

// Download file
const { data, error } = await supabase.storage
  .from('avatars')
  .download(`${user.id}/avatar.png`);

// Delete file
const { error } = await supabase.storage
  .from('avatars')
  .remove([`${user.id}/avatar.png`]);

// List files
const { data, error } = await supabase.storage
  .from('avatars')
  .list(user.id, {
    limit: 100,
    offset: 0
  });
```

### Storage Policies
```sql
-- Only users can upload their own avatars
create policy "Users can upload own avatar" on storage.objects
  for insert with check (
    bucket_id = 'avatars' AND
    auth.uid()::text = (storage.foldername(name))[1]
  );

-- Anyone can view avatars
create policy "Anyone can view avatars" on storage.objects
  for select using (bucket_id = 'avatars');
```

## Error Handling

### Consistent Error Handling
```typescript
// lib/supabase/errors.ts
export class SupabaseError extends Error {
  constructor(
    message: string,
    public code?: string,
    public details?: any
  ) {
    super(message);
    this.name = 'SupabaseError';
  }
}

export async function handleSupabaseError(error: any): Promise<never> {
  if (error?.code === 'PGRST301') {
    throw new SupabaseError('Authentication required', 'AUTH_REQUIRED');
  }
  
  if (error?.code === '23505') {
    throw new SupabaseError('This record already exists', 'DUPLICATE');
  }
  
  throw new SupabaseError(
    error?.message || 'An unexpected error occurred',
    error?.code,
    error
  );
}

// Usage
try {
  const { data, error } = await supabase
    .from('posts')
    .insert({ title, content });
    
  if (error) await handleSupabaseError(error);
  
  return data;
} catch (error) {
  if (error instanceof SupabaseError) {
    // Handle known errors
    console.error(`Supabase error: ${error.code}`, error.message);
  }
  throw error;
}
```

## Performance Optimization

### Query Optimization
```typescript
// ❌ N+1 query problem
const posts = await supabase.from('posts').select('*');
for (const post of posts.data) {
  const author = await supabase
    .from('profiles')
    .select('*')
    .eq('id', post.user_id)
    .single();
}

// ✅ Single query with join
const { data: posts } = await supabase
  .from('posts')
  .select(`
    *,
    author:profiles(*)
  `);

// ✅ Partial selection for performance
const { data } = await supabase
  .from('posts')
  .select('id, title, created_at') // Only needed fields
  .range(0, 9); // Pagination
```

### Connection Pooling
```typescript
// For serverless environments
import { createClient } from '@supabase/supabase-js';

// Create singleton instance
let supabase: ReturnType<typeof createClient> | null = null;

export function getSupabaseClient() {
  if (!supabase) {
    supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_ROLE_KEY!,
      {
        auth: {
          persistSession: false,
          autoRefreshToken: false,
        },
      }
    );
  }
  return supabase;
}
```

## Common Gotchas

### 1. RLS Not Enabled
```typescript
// ❌ Forgetting to enable RLS exposes all data
// Always check: alter table [table_name] enable row level security;
```

### 2. Using Wrong Key
```typescript
// ❌ Using service key on client
const supabase = createClient(url, SERVICE_ROLE_KEY); // SECURITY RISK!

// ✅ Use anon key on client
const supabase = createClient(url, ANON_KEY);
```

### 3. Forgetting to Handle Errors
```typescript
// ❌ No error handling
const { data } = await supabase.from('posts').select('*');
console.log(data); // Could be null!

// ✅ Always check for errors
const { data, error } = await supabase.from('posts').select('*');
if (error) {
  console.error('Error fetching posts:', error);
  return;
}
```

### 4. Not Waiting for Auth
```typescript
// ❌ Race condition
const user = supabase.auth.getUser();
const posts = await supabase.from('posts').select('*'); // Might fail!

// ✅ Wait for auth
const { data: { user } } = await supabase.auth.getUser();
if (user) {
  const posts = await supabase.from('posts').select('*');
}
```

### 5. Realtime Without RLS
```typescript
// ❌ Realtime subscriptions bypass RLS by default
// Enable realtime RLS:
alter publication supabase_realtime add table posts;

// Then add RLS policies for realtime
create policy "Users can subscribe to own posts" on posts
  for select using (auth.uid() = user_id);
```

## Testing Patterns

### Mock Supabase Client
```typescript
// __mocks__/supabase.ts
export const mockSupabase = {
  from: jest.fn(() => ({
    select: jest.fn(() => ({
      data: [],
      error: null,
    })),
    insert: jest.fn(() => ({
      data: null,
      error: null,
    })),
  })),
  auth: {
    getUser: jest.fn(() => ({
      data: { user: { id: 'test-user' } },
      error: null,
    })),
  },
};

// In tests
jest.mock('@/lib/supabase/client', () => ({
  createClient: () => mockSupabase,
}));
```

## Migrations Best Practices

### Migration Files
```sql
-- migrations/001_create_posts.sql
create table if not exists posts (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  content text,
  user_id uuid references auth.users(id) on delete cascade,
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now()
);

-- Enable RLS
alter table posts enable row level security;

-- Add policies
create policy "Users can CRUD own posts" on posts
  for all using (auth.uid() = user_id);

-- Add indexes
create index posts_user_id_idx on posts(user_id);
create index posts_created_at_idx on posts(created_at desc);
```

## Security Checklist

- [ ] All tables have RLS enabled
- [ ] Service role key never exposed to client
- [ ] User input sanitized before queries
- [ ] Policies check user ownership
- [ ] API routes validate authentication
- [ ] File uploads restricted by type/size
- [ ] Realtime subscriptions use RLS
- [ ] Environment variables properly configured
- [ ] Error messages don't leak sensitive info
- [ ] Regular security audits performed

## Remember

1. **Always enable RLS** on tables
2. **Check for errors** in every query
3. **Use the right key** (anon for client, service for server)
4. **Type your database** for safety
5. **Optimize queries** with proper selections and joins
6. **Handle auth states** properly
7. **Test with mocks** for reliability
8. **Monitor performance** in production
