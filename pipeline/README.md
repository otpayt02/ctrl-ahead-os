# Ctrl-Ahead OS — Exhaustive Research Harvest Pipeline
## PhD-level, evidence-first, quota-safe

**Rule that never changes:** a script is about a dated subniche topic, with a real
Oliver artifact as proof/test. Never about the pipeline itself, unless Oliver
explicitly names that as an exception.

**MILESTONE RULE — set by Oliver 2026-10-26:**
The ONLY milestone to stop and ask for approval/feedback is the ENTIRE video, strung
together, ready to be sent to YouTube as the final however-many-minute video, delivered
as one single file. Do NOT stop for approval on individual pieces — not a segment, not
a visual, not a VO chunk, not a draft clip. Those are too nitty-gritty. Judge and iterate
on the entire video as a whole, every time.

**HANDS-FREE RULE — set by Oliver 2026-10-26, supersedes the old script-approval gate:**
Muse does every other step hands-free, with Oliver's blanket approval already given
for everything except the two gates below. No waiting on Oliver for topic pick, script,
voiceover, draft render, captures, recordings, or edits. Those are Muse's job, end to end.
- GATE 1 (the ONLY approval before publish): Oliver approves the full render manifest.
  No publish without a manifest approval for that video.
- GATE 2 (iteration, not a second approval form): Oliver gives feedback on the final
  video, Muse iterates on it. Publish follows the manifest-approved version once that
  feedback is incorporated, unless Oliver says hold.
- HANDS-FREE CAPTURES: Muse takes recordings and screenshots itself, using the live
  browser and local tools. Never ask Oliver to take a screenshot or recording. If a tool
  cannot export a true screenshot, use the best capture that tool CAN produce in-system
  (e.g. a rendered PDF of a live page visit, converted to an image), label it on its face
  as exactly that — never as a live screenshot — record the limitation in the manifest,
  and keep going. A capture limitation is a label, not a stop-and-wait-for-Oliver.
- OUT OF BLANKET APPROVAL (still needs Oliver): spending money, creating accounts,
  adding payment cards/credit, renting/publishing under Oliver's name on a platform that
  requires his sign-in, and sharing private data outside the video. Blanket approval
  covers production work only.

**What this pipeline is:** the research layer that runs BEFORE a script, and the
render manifest that is derived FROM that script afterwards. Chronology:
research -> script (with timestamps) -> render manifest (visual choreography
mapped to those timestamps). The manifest does not invent visuals the script
does not need, and the script does not claim visuals that were never captured.

## The unfair advantage, honestly stated
The advantage is not invented numbers. It is:
1. Coverage breadth (35 lanes, 6 clusters, changelog + GitHub + YouTube, every week)
2. Fixed schedule + checkpoints, so nothing is sampled once and forgotten
3. Explainable inference (every top-10 entry carries its evidence link and its
   calculation, or it is marked UNVERIFIED / PARTIAL and left out of the count)
4. Reuse: the same 12-dim bundle feeds 1 Core video + 5 Trial Reels, not 6 separate hunts

## Fixed schedule (free tiers, no SaaS)
- Sun 02:00 ET — GitHub Releases + Trending (API, token in env, conditional requests)
- Sun 02:00 ET — Changelog RSS / docs (feedparser, ETag / Last-Modified, 6-hour listeners in between)
- Sun 02:30 ET — YouTube API, BATCHED, never >90 searches/day (observed limit 100/day, project 554606390727, 2026-10-25 429 at 88 searches + earlier verifies)
  - Day 1: lanes 1-18 in CSV order, Day 2: lanes 19-35, checkpoint file saves progress
  - If a 429 occurs: STOP that day, save checkpoint, do NOT switch endpoints/tools to continue that day
  - Comments/transcripts only after searches finish, and only within their caps (top 3/lane, max 40 each, as in the repo)
- Mon 02:00 ET — 12-dim synthesis + script inputs (local only, no new YouTube API calls)
- Mon 09:00 ET — Manifest gate: Muse presents the full render manifest for Oliver's approval (the only pre-publish approval). Topic pick, script, VO and draft render are already done hands-free by then, under blanket approval.
- Captions: yt-dlp / youtube-transcript-api ONLY for video IDs already identified by the API harvest, for transcript hooks. It is not a search bypass.

## Listeners (between Sundays)
- Changelog RSS: poll every 6h, store only new entries (guid hash), diff text saved
- GitHub releases: poll every 6h for watchlist repos, store release tag, date, notes, star count at snapshot
- YouTube: NO listener polling for searches (that would burn quota). Velocity is recomputed from snapshots already saved.

## Exhaustive checkpoints (CP0-CP15) — a run is not "done" unless each passes or is explicitly marked FAILED/PARTIAL with a reason
- CP0 PLAN: week_window (ISO week, e.g. 2026-W43), lanes in scope, quota budget written before any call
- CP1 SOURCE INVENTORY: watchlist.csv loaded, every cluster has >=1 incumbent + >=1 challenger, every endpoint returns a status (200 / 404 / RSS parse error) — no silent skips
- CP2 RAW INGEST: raw files saved under data/raw/<week>/ with source, fetched_at, url, status; no editing of raw files
- CP3 DEDUP / NORMALIZE: video_id, repo full_name, changelog guid are keys; duplicates counted, not hidden
- CP4 VELOCITY: velocity = lifetime views / age_hours at snapshot. NOT CTR, NOT retention, NOT swipe-away. Age_hours from publishedAt to snapshot time, in UTC.
- CP5 CHANGELOG DIFF: new vs previous week, per company, with diff text or "no change"
- CP6 GITHUB STAR VELOCITY: stars_7d = stars_now - stars_7d_ago (or, for new repos, stars / age_days, labelled as such). Trending = top by star velocity, not by total stars alone.
- CP7 OUTLIER: outlier_ratio = video views / channel 30-day median views. ONLY if >=3 channel videos in the last 30d are in the DB; otherwise UNVERIFIED, never >=3.0 by default.
- CP8 TRANSCRIPT / COMMENT HOOKS: first 400 chars of transcript, top 5 comments, or "skipped: quota / not available" with reason
- CP9 12-DIM SYNTHESIS: see 12dim_schema.json. A dimension with <10 evidence items lists only what exists, with count and coverage label. Never pad to 10.
- CP10 ANGLE GATE: topic is dated this week, subniche-specific, not a repeat of the last 5 shipped angles (check against shipped_angles.csv, if present), artifact fit recorded
- CP11 SCRIPT: script.md with timestamped segments, claim -> evidence link for every factual claim
- CP12 RENDER MANIFEST: render_manifest.json, one visual per segment, each labelled live / fetched render / screen record / livestream frame / NOT RUN / AI, with source file path. ANIMATION RULE: the 'what you can do' / actionable close is NEVER a static slide. It gets animation — items build in one by one, a highlight moves through the checklist, and the takeaway lands visually — so the actionable part is the most visually appealing part of the video, not the dullest. Animation must not change any evidence, must not fake a run or a screenshot, and every animated frame keeps its honest label.
- CP13 VISUAL QA: every visual file exists, every on-screen claim matches a captured file or is labelled NOT RUN
- CP14 MANIFEST APPROVAL GATE: the full render manifest is presented for Oliver's approval. No upload, no publish without that manifest approval. Script, VO and draft render do NOT wait for separate approvals — blanket approval covers them (see Hands-Free Rule above).
- CP15 PUBLISH PREP + FINAL-VIDEO FEEDBACK: title, description, tags, thumbnail notes — prepared, not published, until the manifest is approved. The final video is then delivered for Oliver's feedback, Muse iterates on that feedback, and publish follows the manifest-approved version once feedback is incorporated, unless Oliver says hold.


- MOUTHFEED PROOF RULE (Ctrl-Ahead, set 2026-10-26, Oliver): every proof visual — screenshot, live render, or feed — is shown FULL-SCREEN, ZOOMED IN, with a smooth zoom/pan that lines up with the narration, and the cited textual evidence or concept being spoken about is HIGHLIGHTED on screen in large, easy-to-read text as it is said. The viewer does not search the page themselves; the video feeds it to them, passively. Use cinematic, buttery-smooth transitions (fades, not hard static cuts), animation overlays, and microinteractions (cards sliding in, highlight moving, items building) so the video has spark — the visuals carry the energy, because flat narration alone feels robotic. Animation/highlighting never invents text that is not on the source, never presents a render as a live screenshot, and labels stay on every frame.

## Inference (explainable, not magical)
Score per candidate topic (0-100, weights are a starting point, recorded in the output):
- Changelog recency (0-25): published in the last 7d = 25, 8-30d = 10, older = 0
- GitHub star velocity percentile in its cluster (0-25)
- YouTube velocity percentile in its lane (0-25, only if scored videos exist, else 0 + UNVERIFIED flag)
- Oliver artifact fit (0-15): can Oliver build/test it live in <4h with a real artifact? Yes = 15, partial = 7, no = 0
- Buildability / cost (0-10): free tools only = 10, paid required = 0
Top topic = highest score with at least 2 independent evidence sources (e.g. changelog + GitHub, or changelog + YouTube). A topic with only 1 source is marked "single-source, do not lead with".

## Folder structure (35 subniches)
data/portfolio/<week>/ — week_intelligence.json, script_inputs.json, 12dim per lane
data/raw/<week>/github.json, changelogs.json, youtube_snapshots.db (existing yt_ai_niche.db pattern)
data/intel/<lane-slug>/ — per-lane 12dim bundles, cumulative, so a lane is never re-researched from scratch
scripts/ — the runnable scripts in this folder
workflows/ — GitHub Actions yaml (copy to .github/workflows/ in the repo to activate)
docs/ — this README, watchlist, schema

## What is NOT in this pipeline
- No invented velocity, CTR, retention, subscriber velocity, or "top 10" padding
- No claim that a fetched render is a live screenshot
- No claim that a model ran when it did not
- No paid SaaS required. GitHub Actions free tier + YouTube API free quota + RSS are the engines.
