# Model comparisons — scripts and render manifests (chosen lane only)

Chosen lane: Model comparisons, from stage 1-4 inference on 2026-10-26.
Stage 1: 35 lanes, 35 searches, 7d window. Stage 2: 10 searches, 5 shorts + 5 longs per lane for 5 lanes.
Total YouTube API searches today: 1 verify + 35 + 10 = 46, within the 90/day guard. No same-day retry after a 429 (none hit today).

## Why this lane, in one line
Median velocity 670 in stage 1, with buildable, testable topics (a model audit, not just a recap), and a direct fit to your real work — the 005 source video is itself the top model-comparison video this week.

## Excluded, with reasons
- Interviews & podcasts, AI predictions & roadmaps: medians driven by BBC, Diary Of A CEO, and drama outliers, not by buildable AI-niche videos.
- Faceless YouTube systems: pipeline-as-topic, excluded by your own rule.
- AI video generation: stage 2 pool was polluted by non-English drama, weaker than its stage 1 median suggested.

## Parameters extracted from the references
- Hook: name a dated change or a test result in the first line, then promise a verdict.
- Long shape: hook 0-30s, evidence beats in 60-120s blocks, verdict/checklist close.
- Short shape: one claim, one proof beat, one close, under 60s.
- Visual boilerplate: dark grid, one headline per claim, pill label, word-pop captions, slow zoom, proof card zoom/pan on evidence beats.
- These parameters are from reference titles, durations, velocities and channels. They are NOT a frame-by-frame watch of every reference — watch the chosen references before a final render.

## Script 1 — Claude Duet, full breakdown
Hook: Anthropic just dropped Claude Duet — here is what it actually changes, and what it does not.
Beats: what Duet is (from the Brock Mesarich breakdown, 459s, velocity 2737), what it is not (a new model vs a feature), who it helps, verdict: use it if you already live in Claude, do not switch for it alone.
Manifest: long, 6-8 min target, 8-10 segments, proof card on the Duet announcement beat, animated checklist close.

## Script 2 — The open model that beats Claude on a 4GB laptop
Hook: An open model beating Claude, running free on a 4GB laptop — the claim, the test, and the catch.
Beats: the InsiderForce claim (velocity 3539), what beating Claude means (which task, which benchmark — or no benchmark given), what 4GB actually runs, verdict: promising for small tasks, not a Claude replacement.
Manifest: long, 6-8 min, test/audit structure, proof card on the claim beat, no benchmark invented where the source gives none.

## Script 3 — GPT-7 Bel, one week later: what actually shipped?
Hook: A week after the viral model-leak video, which of the four names moved?
Beats: re-check Bel/GPT-7, Claude REA, Gemini Carbon, Qwen 4 against what the companies said since 005, scorecard update, verdict: build on what shipped.
Manifest: long, follow-up to 005, same scorecard template, proof cards on each re-check beat, animated ledger close.

## Next step, only for this lane
Deeper scrape for Model comparisons only (channels, outliers, comments, transcripts for top videos already found by the API), then full scripts, then render manifests for approval, then whole-video render. No other lane gets a deeper scrape in this run.
