# DIRECTIONS — Ctrl-Ahead OS

The binding directions for all Ctrl-Ahead work, compiled from Oliver's standing
rules (goal file, pipeline README CP0–CP15, and his dated corrections through
2026-10-30). Where an older note conflicts with a newer dated rule, the newer
rule wins. Oliver's own words outrank everything in this repo.

## Brand

- The YouTube channel is **Ahead of Rush AI**. Ctrl-Ahead OS is the pipeline /
  system that makes the videos — it is not the channel name, and videos are
  never branded "Ctrl-Ahead" as the channel.
- Brand mark: the brass arrow.
- Catchphrase: **"We don't chase the future. We check it."**
- Tagline pattern: **"Ahead of Rush AI — confirmed, not just claimed."**

## What a script is

- A script is about a specific, dated thing talked about this week in a
  subniche, with a real Oliver artifact as proof/test where one fits. Never
  about the pipeline itself, unless Oliver explicitly names that exception.
- **Script purity (2026-10-30, binding):** scripts talk ONLY about the topic /
  concept and voice Oliver's opinions about that concept. Never about the
  production process, receipts/provenance, the pipeline, or the video's own
  attributes. Never twist a build direction into on-screen reasoning, and never
  present obedience to a direction as support inside the video.
- Do not invent biography. If the corpus did not say it, the script does not
  say it.
- Do not claim view velocity, CTR, retention, or swipe-away from public view
  counts. Velocity means one thing only (see Harvest): lifetime views /
  age_hours at snapshot.
- **Verify before scripting:** check what an entity is and when it was
  released against its primary source before scripting any claim about it.
  A repo, a policy change, and an account ban are three different things.

## How work runs

- **Hands-free (2026-10-26):** topic pick, research, script, voiceover, draft
  render, captures/recordings and edits all run without waiting on Oliver.
  Muse takes captures and recordings itself — never ask Oliver to screenshot
  or record.
- **Gate 1 — the only pre-publish approval:** Oliver approves the full render
  manifest for that video. No manifest approval, no publish.
- **Gate 2 — whole-video feedback:** the only other stop is the entire video,
  strung together as one final file, ready for YouTube. Never stop on a
  segment, a visual, a VO chunk, or a draft clip. Feedback is on the whole
  video; iterate on the whole video.
- Blanket approval does NOT cover: spending money, account or payment setup,
  or publishing under Oliver's sign-in. Those need his explicit approval for
  that step.
- Before a "regenerate," check whether the task is still running; if it is,
  leave it running.

## Harvest rules (research layer)

- Lanes and seed queries live in `yt-niche-intel/subniche_lanes.csv` (35 lanes,
  CSV order is the work order). Sweep 7-day first, then 30-day; viewCount;
  maxResults 25.
- Quota guard: max ~90 YouTube searches/day. On HTTP 429: STOP that day, save
  the checkpoint, do not switch endpoints or tools to keep going that day.
- `velocity` = lifetime views / age_hours at snapshot time. It is NOT CTR,
  retention, or swipe-away, and is never presented as such.
- Topic scoring: changelog 25 + GitHub 25 + YouTube 25 + artifact fit 15 +
  buildability 10. A top topic needs at least 2 independent evidence sources;
  a single-source topic is marked single-source and never leads.
- Never pad a list to a round number. What exists, with its coverage label
  (verified / partial / proxy / UNVERIFIED), is what gets reported.
- Captions/transcripts only for video IDs already found by the API harvest —
  never as a search bypass.

## Video craft

- One slide per idea. A meaningful generated image per concept, used once.
- A still base brought alive by motion: popups, underlines, circles, cut-outs
  sliding in as they are spoken; switch-ups on commas and list expansions;
  fades between slides. No slow zoom. No repeated image or motion.
- **Every narration beat gets a visual that shows what is being talked
  about** (2026-10-30): generated images visualizing the narration, company /
  product logo cards when a company is the subject, proofs, generated motion
  clips. Words and word animation alone are not enough.
- **Something on screen changes at least every 5 seconds** (2026-10-30).
- Proofs: cinematic text reveals and generated visuals. "Receipts" means
  claim-proof visuals — do not build screenshot proofs unless genuinely
  necessary; when showing something Oliver did, use a pretty, concise rendered
  recreation instead of a screenshot receipt. Never present a fetched render
  as a live screenshot, an AI interpolation as an exact product view, or a
  drawn panel as a real screenshot. Provenance labels live in the manifest,
  never burned onto video frames.
- The "what you can do" close is animated: checklist items build in one by
  one, a highlight moves through them, the takeaway lands visually.
- Captions: single clean line, 3–4 word groups, real Whisper timestamps,
  caption text always from the approved script; the spoken word in gold.
- Outro: first-video welcome energy, push subscribe, brass-arrow mark,
  catchphrase, tagline.
- **Music:** background beds are Suno-generated instrumentals (Oliver's Suno
  Pro). Download slots are spent only on tracks headed for a monetized
  release — rights follow the download while subscribed.

## Delivery

- Deliver a finished video as a real file copy — never a symlink, never a
  deep-folder path alone — plus a lighter 720p playable twin beside the
  master. Verify before calling anything delivered: ffprobe duration /
  streams, file size and hash against the master, frame checks at start /
  middle / end, no dead-air gaps.
- Update the current-version note for the project so it points at the
  verified delivery copy, not a superseded version.

## Repo hygiene (from AGENTS.md — still binding)

- `script_inputs.json`, `script_inputs.md`, `*.db`, scraped exports, and API
  keys stay out of git. The YouTube API key lives in the Secure Vault /
  connector config only — never in this repo, in any file, at any depth.
- Commit and push after every meaningful unit of work, with conventional
  prefixes (`feat:`, `fix:`, `docs:`, `chore:`, `research:`).
- Data layout: `pipeline/` is the research + render pipeline (CP0–CP15 in
  `pipeline/README.md`); `pipeline/backend/` is the scheduled backend
  (harvest → Brain → Grill Me front door → scriptgen → render queue);
  `video-projects/` holds per-video build projects (code only — renders and
  media stay out of git); `docs/goal/` holds the goal file and production
  documents the pipeline was run from.
