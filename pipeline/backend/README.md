# Ctrl-Ahead OS — Backend Monolith v1

The automated system behind the videos. One orchestrator chains the whole pipeline;
every stage writes evidence-labelled output and the run manifest states coverage honestly.

## Layout
- `run_pipeline.py` — the one entrypoint (see its docstring for the chain + usage)
- `ctrl_backend/config.py` — paths, quota caps (90 searches/day, top-100/lane, top-10 script_inputs, comment caps)
- `ctrl_backend/harvest.py` — YouTube Data API v3 harvest (live) or proxy_existing loader (no key);
  velocity = lifetime views / age_hours ONLY; 429 = hard stop, no same-day retry, no invented metrics
- `ctrl_backend/mining.py` — comments + transcript hooks for already-identified video IDs only
- `ctrl_backend/scoring.py` — within-lane percentiles, README topic weights, stage narrowing
- `ctrl_backend/brain.py` — indexes local goal files + Google Drive (connected CLI, metadata) +
  GitHub otpayt02 repos (connected connector); angles = cited keyword-overlap matches only
- `ctrl_backend/grillme.py` — Grill Me front door: imports grill-log CSV / concept JSON exports
  from `~/workspace/space_data/grill-me/` or `backend/data/grill_inbox/` into one queue;
  approved concepts feed the same render queue as automate picks
- `ctrl_backend/scriptgen.py` — script draft + HyperFrames/GSAP render manifest with the
  reference-video rules baked in (one idea per slide, no slow zoom, no repeats, gold spoken-word
  captions, mouthfeed proofs, animated checklist close, branded outro; generated media = metaphor only)
- `ctrl_backend/proof_capture.py` — browser screenshot/screen-record task specs for the parent
  agent's browser feature (backend specs them; it cannot drive the live browser itself)
- `schema_backend.sql` — videos, snapshots, comments, transcripts, brain_items, angles,
  topics_scored, render_queue, proof_tasks, pipeline_runs (extends `../schema.sql`)
- `SCHEDULE.md` — the cadence + the goal-owned cron jobs
- `data/` — SQLite DB, quota checkpoint, Grill Me queue · `runs/` — dated run folders

## Console UI — Ctrl-Ahead OS Console (artifact `ctrl-ahead-os-console`)

The branded operator console (built 2026-10-30 at Oliver's direction: brass-arrow
branding, dark cinematic surfaces, gold accents, GSAP-grade buttery transitions).
It presents backend state truthfully (proxy mode is labelled, never dressed up as a
live harvest) and records the Gate 1 decision; it does not change harvesting logic.
Panel ↔ module mapping:

- **Run state / header** — latest `runs/<run>/run_manifest.{json,md}` + `SCHEDULE.md`
  cadence (weekly harvest, daily top-lane check; nothing publishes from a cron).
- **Harvest** — `harvest.py` + `scoring.py` output: `runs/<run>/top100.json` and
  per-lane `script_inputs/` (top-10/lane). Velocity = lifetime views / age_hours.
- **Brain** — `brain.py` output: `runs/<run>/angles.json` (Drive + GitHub otpayt02 +
  local files, cited keyword-overlap angles only). Grill Me sub-panel reads
  `data/grill_queue.json` (`grillme.py`); approved concepts join the render queue.
- **Script Gate (Gate 1)** — the only approval gate: `runs/<run>/render_queue.json`
  entries at `queued_manifest_gate`, backed by each draft's `render_manifest.json`
  from `scriptgen.py`. The console saves Oliver's approve / send-back decision.
  Script-purity rules (2026-10-30: topic-only scripts, no process/receipts/pipeline
  talk, directions never quoted as on-screen reasoning) are displayed at the gate.
- **Visuals pipeline** — per-scene asset plan from the draft's render manifest
  (generated images, logo cards, LTX-2.3 motion clips, `proof_capture.py` task specs
  from `runs/<run>/proof_capture_tasks.json`) plus the choreography slot, which
  ingests `teardown/choreography.json` (timestamped motion + asset assignments from
  the 5-channel teardown) when that file lands.
- **Music** — Suno bed status per video (instrumental beds via Oliver's Suno Pro;
  download slots spent only on release-bound tracks).
- **Render queue** — `render_queue.json` + portfolio state (005 v12 awaiting
  feedback, 006 v2 HyperFrames redo, Argon at Gate 1). Nothing auto-publishes.

Brand assets for the console live in `../../console-assets/` (logo lockup,
background texture, empty-state art — AI-generated 2026-10-30).

## Rules that never change (from GOAL.md + pipeline README)
Topic-first, dated, subniche-specific — never about the pipeline itself. Hands-free up to
Gate 1 (Oliver approves the full render manifest); stop only at the whole finished video
for feedback. No spending, no publishing, no invented velocity/CTR/retention, no fake proofs,
provenance lives in manifests — never on the video frames.

## Status v1 (2026-10-30)
Live-tested end-to-end in proxy mode — see the latest `runs/` folder's run_manifest.md.
Live YouTube harvest code is complete but untested against the API: **YT_API_KEY is not
in the environment** (blocker — same Secure Vault key requested 2026-10-25).
