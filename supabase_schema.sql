-- Run this in the Supabase SQL Editor

create table if not exists research_reports (
  id bigint primary key generated always as identity,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  topic text not null,
  type text not null, -- 'Academic' or 'Market'
  content text not null
);

-- Optional: Enable Row Level Security (RLS) if you want to restrict access
-- alter table research_reports enable row level security;
-- create policy "Enable read access for all users" on research_reports for select using (true);
-- create policy "Enable insert access for all users" on research_reports for insert with check (true);
