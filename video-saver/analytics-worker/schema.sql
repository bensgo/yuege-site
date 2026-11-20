-- Only anonymous aggregated event counts. No per-user data or identifiers.
CREATE TABLE IF NOT EXISTS marketing_daily (
 day TEXT NOT NULL,
 event TEXT NOT NULL,
 source TEXT NOT NULL,
 medium TEXT NOT NULL,
 campaign TEXT NOT NULL,
 content TEXT NOT NULL,
 locale TEXT NOT NULL,
 total INTEGER NOT NULL DEFAULT 0,
 PRIMARY KEY(day,event,source,medium,campaign,content,locale)
);
CREATE INDEX IF NOT EXISTS idx_marketing_daily_date ON marketing_daily(day);
