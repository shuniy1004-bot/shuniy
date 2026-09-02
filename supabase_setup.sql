-- =============================================================
-- SHUNI OFFICIAL — Supabase setup (tables + row level security)
-- Supabase -> SQL Editor -> paste all -> Run. Safe to re-run.
--
-- Order
--   1) Authentication -> Users -> Add user (Auto Confirm User on)
--   2) run this file
--   Reversed, writes lock to `authenticated` and even the owner cannot save.
--
-- Access
--   read           : anyone (the site renders it)
--   insert/update/delete : signed-in admin only
--   comments       : anonymous insert allowed (fans leave them)
--   inquiries      : anonymous insert only; reading is admin only
-- =============================================================


-- profile (single row id=1 holding the whole JSON)
CREATE TABLE IF NOT EXISTS profile (
  id         BIGINT PRIMARY KEY,
  data       JSONB NOT NULL DEFAULT '{}'::jsonb,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE profile ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "profile_all" ON profile;
DROP POLICY IF EXISTS "profile_read" ON profile;
DROP POLICY IF EXISTS "profile_anon_insert" ON profile;
DROP POLICY IF EXISTS "profile_insert" ON profile;
DROP POLICY IF EXISTS "profile_update" ON profile;
DROP POLICY IF EXISTS "profile_delete" ON profile;
CREATE POLICY "profile_read"   ON profile FOR SELECT USING (true);
CREATE POLICY "profile_insert" ON profile FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "profile_update" ON profile FOR UPDATE TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "profile_delete" ON profile FOR DELETE TO authenticated USING (true);


-- notice
CREATE TABLE IF NOT EXISTS notice (
  id         BIGSERIAL PRIMARY KEY,
  title      TEXT NOT NULL,
  content    TEXT,
  pinned     BOOLEAN DEFAULT FALSE,
  image_url  TEXT,
  images     JSONB DEFAULT '[]'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE notice ADD COLUMN IF NOT EXISTS image_url TEXT;
ALTER TABLE notice ADD COLUMN IF NOT EXISTS images JSONB DEFAULT '[]'::jsonb;
ALTER TABLE notice ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "notice_all" ON notice;
DROP POLICY IF EXISTS "notice_read" ON notice;
DROP POLICY IF EXISTS "notice_anon_insert" ON notice;
DROP POLICY IF EXISTS "notice_insert" ON notice;
DROP POLICY IF EXISTS "notice_update" ON notice;
DROP POLICY IF EXISTS "notice_delete" ON notice;
CREATE POLICY "notice_read"   ON notice FOR SELECT USING (true);
CREATE POLICY "notice_insert" ON notice FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "notice_update" ON notice FOR UPDATE TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "notice_delete" ON notice FOR DELETE TO authenticated USING (true);


-- diary
CREATE TABLE IF NOT EXISTS diary (
  id         BIGSERIAL PRIMARY KEY,
  title      TEXT NOT NULL,
  content    TEXT,
  mood       TEXT,
  diary_date DATE,
  image_url  TEXT,
  images     JSONB DEFAULT '[]'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE diary ADD COLUMN IF NOT EXISTS image_url TEXT;
ALTER TABLE diary ADD COLUMN IF NOT EXISTS images JSONB DEFAULT '[]'::jsonb;
ALTER TABLE diary ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "diary_all" ON diary;
DROP POLICY IF EXISTS "diary_read" ON diary;
DROP POLICY IF EXISTS "diary_anon_insert" ON diary;
DROP POLICY IF EXISTS "diary_insert" ON diary;
DROP POLICY IF EXISTS "diary_update" ON diary;
DROP POLICY IF EXISTS "diary_delete" ON diary;
CREATE POLICY "diary_read"   ON diary FOR SELECT USING (true);
CREATE POLICY "diary_insert" ON diary FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "diary_update" ON diary FOR UPDATE TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "diary_delete" ON diary FOR DELETE TO authenticated USING (true);


-- diary comments
CREATE TABLE IF NOT EXISTS comments (
  id         BIGSERIAL PRIMARY KEY,
  diary_id   BIGINT NOT NULL,
  nickname   TEXT,
  message    TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE comments ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "comments_all" ON comments;
DROP POLICY IF EXISTS "comments_read" ON comments;
DROP POLICY IF EXISTS "comments_anon_insert" ON comments;
DROP POLICY IF EXISTS "comments_insert" ON comments;
DROP POLICY IF EXISTS "comments_update" ON comments;
DROP POLICY IF EXISTS "comments_delete" ON comments;
CREATE POLICY "comments_read"   ON comments FOR SELECT USING (true);
CREATE POLICY "comments_anon_insert" ON comments FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY "comments_insert" ON comments FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "comments_update" ON comments FOR UPDATE TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "comments_delete" ON comments FOR DELETE TO authenticated USING (true);


-- schedule (calendar)
CREATE TABLE IF NOT EXISTS schedule (
  id          BIGSERIAL PRIMARY KEY,
  title       TEXT NOT NULL,
  date        DATE NOT NULL,
  time        TEXT,
  type        TEXT DEFAULT '일반',
  note        TEXT,
  color       TEXT DEFAULT 'green',
  highlight   BOOLEAN DEFAULT FALSE,
  time2       TEXT,
  title2      TEXT,
  type2       TEXT,
  description TEXT,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);
-- end_date: empty = single day, set = band across days on the calendar
ALTER TABLE schedule ADD COLUMN IF NOT EXISTS end_date DATE;
ALTER TABLE schedule ADD COLUMN IF NOT EXISTS color       TEXT DEFAULT 'green';
ALTER TABLE schedule ADD COLUMN IF NOT EXISTS highlight   BOOLEAN DEFAULT FALSE;
ALTER TABLE schedule ADD COLUMN IF NOT EXISTS time2       TEXT;
ALTER TABLE schedule ADD COLUMN IF NOT EXISTS title2      TEXT;
ALTER TABLE schedule ADD COLUMN IF NOT EXISTS type2       TEXT;
ALTER TABLE schedule ADD COLUMN IF NOT EXISTS description TEXT;
ALTER TABLE schedule ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "schedule_all" ON schedule;
DROP POLICY IF EXISTS "schedule_read" ON schedule;
DROP POLICY IF EXISTS "schedule_anon_insert" ON schedule;
DROP POLICY IF EXISTS "schedule_insert" ON schedule;
DROP POLICY IF EXISTS "schedule_update" ON schedule;
DROP POLICY IF EXISTS "schedule_delete" ON schedule;
CREATE POLICY "schedule_read"   ON schedule FOR SELECT USING (true);
CREATE POLICY "schedule_insert" ON schedule FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "schedule_update" ON schedule FOR UPDATE TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "schedule_delete" ON schedule FOR DELETE TO authenticated USING (true);


-- song book: covers
CREATE TABLE IF NOT EXISTS songs (
  id         BIGSERIAL PRIMARY KEY,
  title      TEXT NOT NULL,
  artist     TEXT,
  genre      TEXT DEFAULT '기타',
  difficulty INT  DEFAULT 3,
  memo       TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE songs ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "songs_all" ON songs;
DROP POLICY IF EXISTS "songs_read" ON songs;
DROP POLICY IF EXISTS "songs_anon_insert" ON songs;
DROP POLICY IF EXISTS "songs_insert" ON songs;
DROP POLICY IF EXISTS "songs_update" ON songs;
DROP POLICY IF EXISTS "songs_delete" ON songs;
CREATE POLICY "songs_read"   ON songs FOR SELECT USING (true);
CREATE POLICY "songs_insert" ON songs FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "songs_update" ON songs FOR UPDATE TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "songs_delete" ON songs FOR DELETE TO authenticated USING (true);


-- replay clips (SOOP VOD) — the profile page reads this into #ovod-grid
CREATE TABLE IF NOT EXISTS original_songs (
  id         BIGSERIAL PRIMARY KEY,
  title      TEXT NOT NULL,
  vod_id     TEXT,
  thumbnail  TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
-- the profile page orders by sort_order
ALTER TABLE original_songs ADD COLUMN IF NOT EXISTS sort_order INT DEFAULT 0;
ALTER TABLE original_songs ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "original_songs_all" ON original_songs;
DROP POLICY IF EXISTS "original_songs_read" ON original_songs;
DROP POLICY IF EXISTS "original_songs_anon_insert" ON original_songs;
DROP POLICY IF EXISTS "original_songs_insert" ON original_songs;
DROP POLICY IF EXISTS "original_songs_update" ON original_songs;
DROP POLICY IF EXISTS "original_songs_delete" ON original_songs;
CREATE POLICY "original_songs_read"   ON original_songs FOR SELECT USING (true);
CREATE POLICY "original_songs_insert" ON original_songs FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "original_songs_update" ON original_songs FOR UPDATE TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "original_songs_delete" ON original_songs FOR DELETE TO authenticated USING (true);


-- wardrobe (hair / lens / outfit) — images are pasted URLs, no Storage bucket
CREATE TABLE IF NOT EXISTS public.dress_items (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  category    TEXT NOT NULL DEFAULT 'hair',
  name        TEXT NOT NULL,
  description TEXT DEFAULT '',
  image_key   TEXT DEFAULT '',
  image_url   TEXT DEFAULT '',
  badges      JSONB DEFAULT '[]',
  is_event    BOOLEAN DEFAULT FALSE,
  glow_color  TEXT DEFAULT '',
  sort_order  INT DEFAULT 0,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_dress_items_category ON public.dress_items(category);
ALTER TABLE public.dress_items ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "dress_all" ON public.dress_items;
DROP POLICY IF EXISTS "dress_items_read" ON public.dress_items;
DROP POLICY IF EXISTS "dress_items_anon_insert" ON public.dress_items;
DROP POLICY IF EXISTS "dress_items_insert" ON public.dress_items;
DROP POLICY IF EXISTS "dress_items_update" ON public.dress_items;
DROP POLICY IF EXISTS "dress_items_delete" ON public.dress_items;
CREATE POLICY "dress_items_read"   ON public.dress_items FOR SELECT USING (true);
CREATE POLICY "dress_items_insert" ON public.dress_items FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "dress_items_update" ON public.dress_items FOR UPDATE TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "dress_items_delete" ON public.dress_items FOR DELETE TO authenticated USING (true);


-- upbo: viewers
CREATE TABLE IF NOT EXISTS viewers (
  id         BIGSERIAL PRIMARY KEY,
  nickname   TEXT NOT NULL,
  soop_id    TEXT,
  memo       TEXT,
  sort_order INT DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE viewers ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "viewers_all" ON viewers;
DROP POLICY IF EXISTS "viewers_read" ON viewers;
DROP POLICY IF EXISTS "viewers_anon_insert" ON viewers;
DROP POLICY IF EXISTS "viewers_insert" ON viewers;
DROP POLICY IF EXISTS "viewers_update" ON viewers;
DROP POLICY IF EXISTS "viewers_delete" ON viewers;
CREATE POLICY "viewers_read"   ON viewers FOR SELECT USING (true);
CREATE POLICY "viewers_insert" ON viewers FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "viewers_update" ON viewers FOR UPDATE TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "viewers_delete" ON viewers FOR DELETE TO authenticated USING (true);


-- upbo: types
CREATE TABLE IF NOT EXISTS upbo_types (
  id         BIGSERIAL PRIMARY KEY,
  name       TEXT NOT NULL,
  category   TEXT DEFAULT '일반',
  sort_order INT DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE upbo_types ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "upbo_types_all" ON upbo_types;
DROP POLICY IF EXISTS "upbo_types_read" ON upbo_types;
DROP POLICY IF EXISTS "upbo_types_anon_insert" ON upbo_types;
DROP POLICY IF EXISTS "upbo_types_insert" ON upbo_types;
DROP POLICY IF EXISTS "upbo_types_update" ON upbo_types;
DROP POLICY IF EXISTS "upbo_types_delete" ON upbo_types;
CREATE POLICY "upbo_types_read"   ON upbo_types FOR SELECT USING (true);
CREATE POLICY "upbo_types_insert" ON upbo_types FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "upbo_types_update" ON upbo_types FOR UPDATE TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "upbo_types_delete" ON upbo_types FOR DELETE TO authenticated USING (true);


-- upbo: counts (viewer x type)
CREATE TABLE IF NOT EXISTS upbo_counts (
  id         BIGSERIAL PRIMARY KEY,
  viewer_id  BIGINT NOT NULL,
  type_id    BIGINT NOT NULL,
  count      INT DEFAULT 0,
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE (viewer_id, type_id)
);
ALTER TABLE upbo_counts ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "upbo_counts_all" ON upbo_counts;
DROP POLICY IF EXISTS "upbo_counts_read" ON upbo_counts;
DROP POLICY IF EXISTS "upbo_counts_anon_insert" ON upbo_counts;
DROP POLICY IF EXISTS "upbo_counts_insert" ON upbo_counts;
DROP POLICY IF EXISTS "upbo_counts_update" ON upbo_counts;
DROP POLICY IF EXISTS "upbo_counts_delete" ON upbo_counts;
CREATE POLICY "upbo_counts_read"   ON upbo_counts FOR SELECT USING (true);
CREATE POLICY "upbo_counts_insert" ON upbo_counts FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "upbo_counts_update" ON upbo_counts FOR UPDATE TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "upbo_counts_delete" ON upbo_counts FOR DELETE TO authenticated USING (true);


-- inquiries — the profile page writes { message } here
CREATE TABLE IF NOT EXISTS inquiries (
  id         BIGSERIAL PRIMARY KEY,
  nickname   TEXT,
  message    TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE inquiries ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "inquiries_all" ON inquiries;
DROP POLICY IF EXISTS "inquiries_read" ON inquiries;
DROP POLICY IF EXISTS "inquiries_anon_insert" ON inquiries;
DROP POLICY IF EXISTS "inquiries_insert" ON inquiries;
DROP POLICY IF EXISTS "inquiries_update" ON inquiries;
DROP POLICY IF EXISTS "inquiries_delete" ON inquiries;
CREATE POLICY "inquiries_read"   ON inquiries FOR SELECT TO authenticated USING (true);
CREATE POLICY "inquiries_anon_insert" ON inquiries FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY "inquiries_insert" ON inquiries FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "inquiries_update" ON inquiries FOR UPDATE TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "inquiries_delete" ON inquiries FOR DELETE TO authenticated USING (true);


-- OBS overlay: "now playing", single row
CREATE TABLE IF NOT EXISTS public.overlay_state (
  id          INT PRIMARY KEY DEFAULT 1 CHECK (id = 1),
  song_title  TEXT DEFAULT '',
  song_artist TEXT DEFAULT '',
  is_visible  BOOLEAN DEFAULT FALSE,
  updated_at  TIMESTAMPTZ DEFAULT NOW()
);
INSERT INTO public.overlay_state (id) VALUES (1) ON CONFLICT (id) DO NOTHING;
ALTER TABLE public.overlay_state ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "overlay_all" ON public.overlay_state;
DROP POLICY IF EXISTS "overlay_state_read" ON public.overlay_state;
DROP POLICY IF EXISTS "overlay_state_anon_insert" ON public.overlay_state;
DROP POLICY IF EXISTS "overlay_state_insert" ON public.overlay_state;
DROP POLICY IF EXISTS "overlay_state_update" ON public.overlay_state;
DROP POLICY IF EXISTS "overlay_state_delete" ON public.overlay_state;
CREATE POLICY "overlay_state_read"   ON public.overlay_state FOR SELECT USING (true);
CREATE POLICY "overlay_state_insert" ON public.overlay_state FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "overlay_state_update" ON public.overlay_state FOR UPDATE TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "overlay_state_delete" ON public.overlay_state FOR DELETE TO authenticated USING (true);


-- one Supabase project holds one person. Reusing a project keeps the old row,
-- because the insert below does nothing on conflict. To start clean, uncomment
-- the delete and run once.
-- DELETE FROM profile WHERE id = 1;
INSERT INTO profile (id, data) VALUES (1, '{}'::jsonb) ON CONFLICT (id) DO NOTHING;
