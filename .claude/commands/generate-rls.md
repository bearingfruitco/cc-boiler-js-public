# generate-rls

Generates Row Level Security (RLS) policies for Supabase tables.

## Usage
```bash
generate-rls <table> [template]
```

## Arguments
- `table` - Name of the database table
- `template` - Policy template to use (optional)

## Available Templates
- `user-owned` - Users can only access their own data (default)
- `public-read` - Anyone can read, authenticated users can write
- `role-based` - Different permissions based on user roles
- `team-access` - Team members share access to data
- `time-based` - Access expires after certain time
- `soft-delete` - Respects soft deletes

## Examples
```bash
# Generate default user-owned policies
generate-rls posts

# Generate public read policies
generate-rls articles public-read

# Generate team-based access
generate-rls projects team-access

# Generate role-based policies
generate-rls admin_panel role-based
```

## What it generates

### Migration File
Creates `supabase/migrations/[timestamp]_[table]_rls.sql` with:
- Enable RLS statement
- SELECT policies
- INSERT policies
- UPDATE policies
- DELETE policies
- Helper functions (if needed)

### Test File
Creates `tests/rls/[table].test.ts` with:
- Policy existence tests
- Access control tests
- Edge case tests

### Documentation
Updates `docs/rls-policies.md` with:
- Table policies overview
- Access matrix
- Testing instructions

## Policy Patterns

### User-Owned Data
```sql
-- Users can only see their own records
CREATE POLICY "Users can view own records"
  ON public.posts
  FOR SELECT
  USING (auth.uid() = user_id);
```

### Public Read
```sql
-- Anyone can read
CREATE POLICY "Public read access"
  ON public.articles
  FOR SELECT
  USING (true);

-- Only authenticated can write
CREATE POLICY "Authenticated write"
  ON public.articles
  FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL);
```

### Team Access
```sql
-- Team members can access shared data
CREATE POLICY "Team members access"
  ON public.projects
  FOR ALL
  USING (team_id IN (
    SELECT team_id FROM team_members
    WHERE user_id = auth.uid()
  ));
```

## Testing RLS Policies
```bash
# Run RLS tests
npm run test:rls

# Test specific table
npm run test:rls posts
```

## Best Practices
1. Always enable RLS on tables with user data
2. Test policies with different user roles
3. Use helper functions for complex logic
4. Document policy intent
5. Review policies during security audits
