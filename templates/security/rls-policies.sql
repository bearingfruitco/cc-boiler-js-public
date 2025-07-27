-- RLS Policy Templates for Supabase
-- These templates cover common access patterns

-- ============================================
-- TEMPLATE 1: User-Owned Data
-- Users can only access their own records
-- ============================================

-- Enable RLS on the table
ALTER TABLE public.{{table_name}} ENABLE ROW LEVEL SECURITY;

-- Users can view their own records
CREATE POLICY "Users can view own {{table_name}}"
  ON public.{{table_name}}
  FOR SELECT
  USING (auth.uid() = user_id);

-- Users can insert their own records
CREATE POLICY "Users can insert own {{table_name}}"
  ON public.{{table_name}}
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Users can update their own records
CREATE POLICY "Users can update own {{table_name}}"
  ON public.{{table_name}}
  FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Users can delete their own records
CREATE POLICY "Users can delete own {{table_name}}"
  ON public.{{table_name}}
  FOR DELETE
  USING (auth.uid() = user_id);

-- ============================================
-- TEMPLATE 2: Public Read, Authenticated Write
-- Anyone can read, only authenticated users can write
-- ============================================

-- Enable RLS on the table
ALTER TABLE public.{{table_name}} ENABLE ROW LEVEL SECURITY;

-- Anyone can read
CREATE POLICY "Public read access"
  ON public.{{table_name}}
  FOR SELECT
  USING (true);

-- Only authenticated users can insert
CREATE POLICY "Authenticated users can insert"
  ON public.{{table_name}}
  FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL);

-- Only owners can update
CREATE POLICY "Owners can update"
  ON public.{{table_name}}
  FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Only owners can delete
CREATE POLICY "Owners can delete"
  ON public.{{table_name}}
  FOR DELETE
  USING (auth.uid() = user_id);

-- ============================================
-- TEMPLATE 3: Role-Based Access
-- Different permissions based on user roles
-- ============================================

-- Enable RLS on the table
ALTER TABLE public.{{table_name}} ENABLE ROW LEVEL SECURITY;

-- Function to check user role
CREATE OR REPLACE FUNCTION auth.user_role()
RETURNS TEXT AS $$
  SELECT role FROM public.profiles WHERE id = auth.uid();
$$ LANGUAGE SQL SECURITY DEFINER;

-- Admins can do everything
CREATE POLICY "Admins have full access"
  ON public.{{table_name}}
  FOR ALL
  USING (auth.user_role() = 'admin');

-- Moderators can read and update
CREATE POLICY "Moderators can read"
  ON public.{{table_name}}
  FOR SELECT
  USING (auth.user_role() IN ('moderator', 'admin'));

CREATE POLICY "Moderators can update"
  ON public.{{table_name}}
  FOR UPDATE
  USING (auth.user_role() IN ('moderator', 'admin'))
  WITH CHECK (auth.user_role() IN ('moderator', 'admin'));

-- Regular users can only read public content
CREATE POLICY "Users can read public content"
  ON public.{{table_name}}
  FOR SELECT
  USING (
    is_public = true 
    OR auth.uid() = user_id
  );

-- ============================================
-- TEMPLATE 4: Team/Organization Access
-- Members of same team can access shared data
-- ============================================

-- Enable RLS on the table
ALTER TABLE public.{{table_name}} ENABLE ROW LEVEL SECURITY;

-- Function to get user's team
CREATE OR REPLACE FUNCTION auth.user_team_id()
RETURNS UUID AS $$
  SELECT team_id FROM public.team_members WHERE user_id = auth.uid();
$$ LANGUAGE SQL SECURITY DEFINER;

-- Team members can view team data
CREATE POLICY "Team members can view team {{table_name}}"
  ON public.{{table_name}}
  FOR SELECT
  USING (team_id = auth.user_team_id());

-- Team members can insert team data
CREATE POLICY "Team members can insert team {{table_name}}"
  ON public.{{table_name}}
  FOR INSERT
  WITH CHECK (team_id = auth.user_team_id());

-- Only creators or team admins can update
CREATE POLICY "Creators and admins can update"
  ON public.{{table_name}}
  FOR UPDATE
  USING (
    auth.uid() = created_by
    OR EXISTS (
      SELECT 1 FROM public.team_members
      WHERE user_id = auth.uid()
      AND team_id = {{table_name}}.team_id
      AND role = 'admin'
    )
  );

-- ============================================
-- TEMPLATE 5: Time-Based Access
-- Access expires after certain time
-- ============================================

-- Enable RLS on the table
ALTER TABLE public.{{table_name}} ENABLE ROW LEVEL SECURITY;

-- Users can only access non-expired content
CREATE POLICY "Users can view non-expired {{table_name}}"
  ON public.{{table_name}}
  FOR SELECT
  USING (
    (expires_at IS NULL OR expires_at > NOW())
    AND (auth.uid() = user_id OR is_public = true)
  );

-- ============================================
-- TEMPLATE 6: Soft Delete Support
-- Respect soft deletes in all policies
-- ============================================

-- Enable RLS on the table
ALTER TABLE public.{{table_name}} ENABLE ROW LEVEL SECURITY;

-- Only show non-deleted records
CREATE POLICY "Users can view non-deleted {{table_name}}"
  ON public.{{table_name}}
  FOR SELECT
  USING (
    deleted_at IS NULL
    AND (auth.uid() = user_id OR is_public = true)
  );

-- Soft delete instead of hard delete
CREATE POLICY "Users can soft delete own {{table_name}}"
  ON public.{{table_name}}
  FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (
    auth.uid() = user_id
    AND deleted_at IS NOT NULL -- Only allow setting deleted_at
  );

-- ============================================
-- Testing RLS Policies
-- ============================================

-- Test as anonymous user
SET SESSION AUTHORIZATION anon;
SELECT * FROM public.{{table_name}}; -- Should only see public records

-- Test as authenticated user
SET SESSION AUTHORIZATION authenticated;
SET request.jwt.claim.sub = 'user-uuid-here';
SELECT * FROM public.{{table_name}}; -- Should see own records

-- Reset session
RESET SESSION AUTHORIZATION;
