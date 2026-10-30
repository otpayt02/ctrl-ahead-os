-- Ctrl-Ahead OS backend monolith v1 — extends ../schema.sql (applied first if present)
CREATE TABLE IF NOT EXISTS pipeline_runs (
  run_id TEXT PRIMARY KEY, started_at TEXT NOT NULL, mode TEXT NOT NULL, -- live|proxy_existing|dry
  week_window TEXT, lanes_covered INTEGER DEFAULT 0, videos_scored INTEGER DEFAULT 0,
  coverage TEXT, notes TEXT, finished_at TEXT);
CREATE TABLE IF NOT EXISTS videos (
  video_id TEXT PRIMARY KEY, lane TEXT, title TEXT, channel TEXT, published_at TEXT,
  duration TEXT, source TEXT NOT NULL, evidence_url TEXT);
CREATE TABLE IF NOT EXISTS video_snapshots (
  id INTEGER PRIMARY KEY, video_id TEXT NOT NULL, snapshot_at TEXT NOT NULL,
  views INTEGER, likes INTEGER, comments INTEGER, velocity REAL, -- lifetime views / age_hours ONLY
  like_ratio REAL, comment_ratio REAL, UNIQUE(video_id, snapshot_at));
CREATE TABLE IF NOT EXISTS comments_mined (
  id INTEGER PRIMARY KEY, video_id TEXT, author TEXT, text TEXT, likes INTEGER, mined_at TEXT, source TEXT);
CREATE TABLE IF NOT EXISTS transcripts (
  video_id TEXT PRIMARY KEY, hook_400 TEXT, status TEXT NOT NULL, -- ok|skipped:<reason>
  fetched_at TEXT);
CREATE TABLE IF NOT EXISTS brain_items (
  id TEXT PRIMARY KEY, kind TEXT NOT NULL, -- drive_file|github_repo|local_file|goal
  name TEXT NOT NULL, description TEXT, source_ref TEXT NOT NULL, -- path or URL, always real
  keywords TEXT, indexed_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS angles (
  id INTEGER PRIMARY KEY, topic TEXT NOT NULL, lane TEXT, brain_item_id TEXT,
  angle TEXT NOT NULL, overlap_tokens TEXT, score REAL, source_ref TEXT NOT NULL, run_id TEXT);
CREATE TABLE IF NOT EXISTS topics_scored (
  id INTEGER PRIMARY KEY, run_id TEXT, lane TEXT, topic TEXT, score REAL,
  youtube_percentile REAL, artifact_fit INTEGER, buildability INTEGER,
  evidence_sources INTEGER, status TEXT); -- candidate|single-source|grill-queued|automate-pick
CREATE TABLE IF NOT EXISTS render_queue (
  id INTEGER PRIMARY KEY, run_id TEXT, topic TEXT, lane TEXT, origin TEXT, -- automate|grill_me
  script_path TEXT, manifest_path TEXT, status TEXT NOT NULL, -- queued_manifest_gate|draft_ready
  created_at TEXT);
CREATE TABLE IF NOT EXISTS proof_tasks (
  id INTEGER PRIMARY KEY, run_id TEXT, topic TEXT, kind TEXT, -- screenshot|screen_record
  target TEXT, instruction TEXT, status TEXT NOT NULL); -- specced|not_needed
