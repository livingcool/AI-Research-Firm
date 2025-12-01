-- Run this in Supabase SQL Editor to FIX the "RLS Policy Violation" error

-- 1. Ensure RLS is enabled
alter table feedback enable row level security;

-- 2. Drop existing policies to start fresh
drop policy if exists "Users can insert own feedback" on feedback;
drop policy if exists "Admins can view all feedback" on feedback;

-- 3. Re-create the policies
-- Allow users to insert rows where the user_id matches their own ID
create policy "Users can insert own feedback" 
on feedback 
for insert 
with check ( auth.uid() = user_id );

-- Allow admins to view all feedback
create policy "Admins can view all feedback" 
on feedback 
for select 
using ( 
  exists (select 1 from profiles where id = auth.uid() and role = 'admin')
);

-- 4. Verify (Optional, for your info)
select * from pg_policies where tablename = 'feedback';
