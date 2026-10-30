# Ctrl-Ahead OS backend — schedule

Goal-owned crons under goal `ctrl-ahead-os-ai-video` (goal_5f4b02102812), America/New_York.
Created and verified 2026-10-30 via the cron tools (ids + next runs in the build report).

## Weekly harvest — Sundays, ~02:30 ET (job: `ctrl-ahead-weekly-harvest`)
Runs `python3 run_pipeline.py --mode auto` in `files/pipeline/backend/`:
- Day-split rule from the pipeline README still applies inside live mode: quota guard
  max 90 searches/day, stop on 429, NO same-day retry, checkpoint saved.
- With YT_API_KEY absent it runs proxy_existing mode and the run manifest says so —
  a proxy run is never reported as a fresh harvest.
- Output: dated folder in `backend/runs/` with run_manifest, top-100, per-lane
  script_inputs (top-10), angles, Grill Me snapshot, proof-capture tasks, render queue.
- Render queue entries stop at `queued_manifest_gate` — Gate 1: Oliver approves the
  full render manifest before anything publishes. Nothing publishes from a cron.

## Daily top-lane check — daily ~09:14 ET (job: `ctrl-ahead-daily-top-lane`)
Light check only: re-reads the latest run's top100/script_inputs + Brain angles,
recomputes nothing from YouTube (no quota burn), and surfaces at most ONE item —
the current chosen lane/topic and whether a manifest is waiting at Gate 1.
If nothing changed since yesterday, it reports nothing new.

## Between-Sunday listeners (specced, not separate crons)
- Changelog RSS + GitHub releases: 6-hour polling per pipeline README CP1/CP5 —
  implemented in the existing `../scripts/changelog_watcher.py` / `github_trending.py`;
  wiring them as their own crons is a v2 step, deliberately not multiplied here.
- YouTube: NO listener polling (quota). Velocity is recomputed from saved snapshots only.

## Manual run
`cd files/pipeline/backend && python3 run_pipeline.py --mode auto|live|proxy`
