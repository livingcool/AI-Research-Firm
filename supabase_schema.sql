-- Run this in the Supabase SQL Editor

-- 1. Create tables if they don't exist
create table if not exists research_reports (
  id bigint primary key generated always as identity,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  topic text not null,
  type text not null, -- 'Academic' or 'Market'
  content text not null
);

create table if not exists usage_logs (
  id bigint primary key generated always as identity,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  user_id uuid references auth.users not null,
  model text not null,
  input_tokens int not null,
  output_tokens int not null
);

create table if not exists profiles (
  id uuid references auth.users on delete cascade primary key,
  role text not null default 'user' check (role in ('user', 'admin'))
);

-- 2. Add missing columns (Migration for existing tables)
do $$
begin
  if not exists (select 1 from information_schema.columns where table_name = 'research_reports' and column_name = 'user_id') then
    alter table research_reports add column user_id uuid references auth.users;
  end if;
end $$;

-- 3. Triggers
create or replace function public.handle_new_user()
returns trigger as $$
begin
  insert into public.profiles (id, role)
  values (new.id, 'user');
  return new;
end;
$$ language plpgsql security definer;

-- Drop trigger first to avoid error if it exists
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- 3b. Backfill Profiles for existing users (if any)
insert into public.profiles (id, role)
select id, 'user' from auth.users
on conflict (id) do nothing;

create table if not exists feedback (
  id bigint primary key generated always as identity,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  user_id uuid references auth.users not null,
  rating int not null check (rating >= 1 and rating <= 5),
  comment text
);

-- 4. RLS Policies
alter table research_reports enable row level security;
alter table usage_logs enable row level security;
alter table profiles enable row level security;
alter table feedback enable row level security;

-- Drop existing policies to avoid conflicts if re-running
drop policy if exists "Public profiles are viewable by everyone." on profiles;
drop policy if exists "Users can insert their own profile." on profiles;
drop policy if exists "Users can update own profile." on profiles;
drop policy if exists "Users can view own reports" on research_reports;
drop policy if exists "Admins can view all reports" on research_reports;
drop policy if exists "Users can insert own reports" on research_reports;
drop policy if exists "Users can view own logs" on usage_logs;
drop policy if exists "Admins can view all logs" on usage_logs;
drop policy if exists "Users can insert own logs" on usage_logs;
drop policy if exists "Users can insert own feedback" on feedback;
drop policy if exists "Admins can view all feedback" on feedback;

-- Re-create Policies
create policy "Public profiles are viewable by everyone." on profiles for select using ( true );
create policy "Users can insert their own profile." on profiles for insert with check ( auth.uid() = id );
create policy "Users can update own profile." on profiles for update using ( auth.uid() = id );

create policy "Users can view own reports" on research_reports for select using ( auth.uid() = user_id );
create policy "Admins can view all reports" on research_reports for select using ( 
  exists (select 1 from profiles where id = auth.uid() and role = 'admin')
);
create policy "Users can insert own reports" on research_reports for insert with check ( auth.uid() = user_id );

create policy "Users can view own logs" on usage_logs for select using ( auth.uid() = user_id );
create policy "Admins can view all logs" on usage_logs for select using ( 
  exists (select 1 from profiles where id = auth.uid() and role = 'admin')
);
create policy "Users can insert own logs" on usage_logs for insert with check ( auth.uid() = user_id );

create policy "Users can insert own feedback" on feedback for insert with check ( auth.uid() = user_id );
create policy "Admins can view all feedback" on feedback for select using ( 
  exists (select 1 from profiles where id = auth.uid() and role = 'admin')
);
