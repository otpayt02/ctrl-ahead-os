# Prompt Pack v2 — yt_niche_intel inference layer
Paste into Google AI Studio (free Flash tier) or local Ollama, with data files attached.

## PROMPT 1 — Subniche verification + top channels per lane
Attached: subniche_lanes.csv, snapshots export, channels ranking.
1. Top 3-5 channels per lane, with median-views evidence.
2. Kill lanes owned only by mega-channels; flag lanes where mid-size channels hit outliers.
3. Output JSON: {lane, top_channels[], verdict, why}[]

## PROMPT 2 — Video-type taxonomy + THE TOP 10 PATTERNS
Attached: script_inputs.json from `python yt_niche_intel.py mine`.
Use the per-lane velocity winners, available transcript openings, comments, title bigrams,
and tags as day-one evidence. Missing hooks or comments are unknown, not weak performance.
Velocity is lifetime views divided by video age at the snapshot, not a retention measure.
1. Classify each video: review/teardown, top-10 roundup, build-with-me, deep-dive explainer,
   news recap, tutorial, tool-vs-tool, workflow showcase, prediction, myth-bust, case study,
   interview, constellation/brain-tour (his unique angle).
2. Extract the TOP 10 RECURRING PATTERNS (hooks, angles, structure, delivery, credibility
   moves, CTAs, title/thumbnail formulas, pacing). Each: name, evidence, why it works,
   small-channel implementation.
3. For each lane, name the winning format's usual title pattern, angle, and proof type.
   Mark which pattern is already common so a new concept can depart from it visibly.
   Treat the 15-30 second Shorts length and early-face tactic as testable creative
   directions from the supplied research, not proven platform thresholds.
4. Output patterns.json only, including lane baselines and evidence gaps.

## PROMPT 3 — Script generation (artifact x 3 patterns)
You write YouTube Shorts and long-form scripts for Oliver Payton: Louisville engineer, 18-yr pianist,
church music director, builds real systems — Sgaw Karen OCR, VIBER Nexus neural-constellation
brain app, KuzuGraph knowledge graphs, payroll automation, cinematic websites, sepak takraw
AI, YouTube automation pipelines, song-making workflows, KOA + Payton Glass client builds.
INPUTS: brain_index.json (44 repos + VIBER Nexus apps + full Drive inventory + project
        history) + patterns.json + script_inputs.json.
RULES: pick ONE artifact at random; pick THREE of the ten patterns at random; choose video
type/tone/mode/delivery; tell the TRUE story of the artifact while implementing all 3
patterns, labeled per beat; every visual timestamped and generatable.
- Atypicality gate: state the chosen lane's winning title pattern, angle, or proof type,
  then show a concrete visible departure in at least one of those dimensions. A title
  synonym or cosmetic color change does not count. Keep the departure truthful to
  Oliver's actual artifact and label the evidence gap when source proof is missing.
- Write seconds 0-3 first. Show a human face and the value proposition within the
  first 2-3 seconds; zero intro, logo pre-roll, or setup delay for either format.
- Target 15-30 seconds for a Short, with entertainment-first framing and a visual
  change every 2-4 seconds. Use long-form for the demonstration, evidence, and depth.
- In the piano/artists lane, use Shorts to invite discovery of a long video or a
  streaming track. Do not describe Shorts themselves as the revenue surface.
- Treat all pacing/format targets as experiments to validate on Oliver's own 24h,
  48h, and 7d Studio snapshots. Never claim competitor CTR, retention, or
  viewed-versus-swiped-away from public proxy data.
OUTPUT strictly this JSON:
{"format":"short|long","lane":"","video_type":"","angle":"","tone":"",
 "patterns_used":[],"format_delta":{"baseline":"","dimension":"title_pattern|angle|proof_type",
 "departure":"","artifact_proof":""},"hook":"",
 "script":[{"t_start":"00:00","t_end":"00:03","narration":"","visual_prompt":"human face + first-frame proof",
            "overlay_text":"value proposition","motion":"zoom|pan|animate|hold","pattern":""}]}

## PROMPT 4 (optional) — VIBER Nexus tour episode
Use PROMPT 3 but force the artifact to be VIBER-Nexus-v4: a screen-recorded tour of his
actual Living Neural Constellation (Concierge resonance panel, daily notes, brain/concepts
nodes) narrated as "the brain I gave myself" — no other AI channel can copy this footage.
