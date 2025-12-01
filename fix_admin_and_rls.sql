-- 1. Fix Profiles RLS (Crucial for Admin check)
alter table profiles enable row level security;
drop policy if exists "Public profiles are viewable by everyone" on profiles;
drop policy if exists "Users can insert their own profile" on profiles;
drop policy if exists "Users can update own profile" on profiles;

create policy "Public profiles are viewable by everyone"
on profiles for select
using ( true );

create policy "Users can insert their own profile"
on profiles for insert
with check ( auth.uid() = id );

create policy "Users can update own profile"
on profiles for update
using ( auth.uid() = id );

-- 2. Fix Feedback RLS
alter table feedback enable row level security;
drop policy if exists "Users can insert own feedback" on feedback;
drop policy if exists "Admins can view all feedback" on feedback;

create policy "Users can insert own feedback"
on feedback for insert
with check ( auth.uid() = user_id );

create policy "Admins can view all feedback"
on feedback for select
using ( true );

-- 3. PROMOTE YOURSELF TO ADMIN
-- Replace 'your_email@example.com' with your actual email address below
-- update profiles
-- set role = 'admin'
-- where id in (select id from auth.users where email = 'your_email@example.com');
