-- Ctrl-Ahead OS harvest DB — extends the existing yt_ai_niche.db pattern
-- Run: sqlite3 yt_ai_niche.db < schema.sql  (idempotent: IF NOT EXISTS)
CREATE TABLE IF NOT EXISTS checkpoints (
  week_window TEXT NOT NULL, checkpoint TEXT NOT NULL, status TEXT NOT NULL,
  detail TEXT, checked_at TEXT NOT NULL, PRIMARY KEY (week_window, checkpoint));
CREATE TABLE IF NOT EXISTS companies (
  company TEXT PRIMARY KEY, cluster TEXT NOT NULL, kind TEXT NOT NULL, -- incumbent|challenger
  changelog_url TEXT, rss_url TEXT, github_org TEXT);
CREATE TABLE IF NOT EXISTS changelog_entries (
  guid TEXT PRIMARY KEY, company TEXT NOT NULL, title TEXT, url TEXT,
  published_at TEXT, summary TEXT, diff_text TEXT, fetched_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS github_repos (
  full_name TEXT PRIMARY KEY, cluster TEXT, subniche TEXT, url TEXT,
  description TEXT, stars INTEGER, stars_7d REAL, forks INTEGER,
  language TEXT, pushed_at TEXT, snapshot_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS github_releases (
  id INTEGER PRIMARY KEY, repo TEXT NOT NULL, tag TEXT, name TEXT,
  published_at TEXT, body TEXT, url TEXT, fetched_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS week_intelligence (
  week_window TEXT NOT NULL, subniche TEXT NOT NULL, dimension TEXT NOT NULL,
  rank INTEGER, item TEXT, evidence_url TEXT, evidence_value TEXT,
  coverage TEXT NOT NULL, -- EVIDENCE | PARTIAL | UNVERIFIED
  PRIMARY KEY (week_window, subniche, dimension, rank));
CREATE TABLE IF NOT EXISTS topics (
  week_window TEXT NOT NULL, subniche TEXT NOT NULL, topic TEXT NOT NULL,
  score REAL, changelog_recency INTEGER, github_percentile REAL,
  youtube_percentile REAL, artifact_fit INTEGER, buildability INTEGER,
  evidence_sources INTEGER, status TEXT, -- candidate|approved|rejected
  PRIMARY KEY (week_window, subniche, topic));
-- Existing YouTube tables (from harvest_run.py) are NOT recreated here:
-- snapshots(video_id, lane, views, published_at, snapshot_at, ...),
-- scored videos, comments, transcripts. This schema only adds the new engines.
