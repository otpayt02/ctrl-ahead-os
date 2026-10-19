# Faceless Visual System — Spec

The operating system for faceless longs/shorts that rely on visualizations, audio, and text subtitles. Cinematic dark house style (deep navy #0a1628, amber #e8a33d, cool cyan #c9d6df, paper #f5efe6; EB Garamond display, JetBrains Mono data). Follows UI_RULES.md.

## Image pacing (configurable)
- DRAGGABLE NUMBER LINE 0-20 in the render config: sets the target AVERAGE visual dwell time (seconds per image/visual beat).
- HARD CAP: no single image exceeds 15 seconds. If the average target is above 15, scenes stack MULTIPLE visuals (images, evidence clips, overlay states) rather than stretching one image.
- NON-UNIFORM by design: never the same duration for each image. Per-visual duration varies around the target with jitter (roughly +/- 20-35%), weighted by annotation importance — key evidence beats dwell longer, transitions shorter.
- VISUAL CHANGE CADENCE (floor, overrides dwell): some visible change (cut, zoom, pan, overlay appearance, kinetic label, transition) at least every 3-5 seconds for educational content. Zooms, text overlays, and transitions all count as changes.
- Defaults: longs ~6-8s average dwell; shorts ~2-4s with fast pacing and minimal dead air.

## Overlay system (layered, informational — not decoration)
- L0 base: image/evidence clip with Ken Burns zooms and pans on static footage.
- L1 anchors: the "chew on this" layer — the anchor visual for each idea the narration is building; overlays ADD information (term definitions, statistics, sources, arrows, diagrams) so the visual is a thinking aid the viewer marinates on while listening.
- L2 kinetic labels: on-screen text for every major claim or statistic; data chips with JetBrains Mono; chapter cards.
- L3 subtitles: captions always on, sized for MOBILE (mobile retention runs 20%+ lower than desktop — larger fonts, simpler graphics).
- L4 presenter (optional per video): small face-cam box (bottom corner), avatar, or none. AI voice clone mode for VO. Script may REQUEST a live cameo (e.g., confession hook).
- High-contrast, clear imagery, impactful text; consistent fonts and colors across the whole channel so the identity reads with the sound off.

## Style consistency
- STYLE REFERENCE SHEET per video: one seed image defines the prompt template for all visuals (same lighting, palette, grain) so scenes feel cohesive.
- Palette locked from manifest style block; never invented per scene.

## Script rhetoric principles (researched)
- Say AND see: A/V pairing — every narration beat has a matching visual; if narration already conveys it, the visual shows the thing itself.
- Pattern interrupt in the first 5 seconds (+23% average retention vs static opening); bold on-screen text hook or direct promise hook ("Here's what happens when..." / "Three things nobody tells you about...").
- Critical thresholds: 70% retention at the 30-second mark; longs 10-15 min sweet spot; shorts 70%+ retention target.
- Three-act structure: Act One ~25% (subject + central question), Act Two ~50% (tension, obstacles, discoveries), Act Three ~25% (resolution, reflection) — in chapters.
- Narration: short clear sentences, active voice ("Glaciers are melting" not "glaciers have been melting"), conversational not academic, read-aloud tested — if you stumble, rewrite.
- Callback closers; circular structures.

## Shorts-specific rules
- Fast-paced editing, minimal dead air (72% of 1M+ view Shorts follow this).
- Loop techniques: end on the opening visual; circular narrative that satisfies on repeat; transformation reveals that restart naturally; open loops that pull the viewer back to the start.
- 15-30s length retains best; hook inside first 3 seconds.

## Presenter modes (per-video config)
- faceless (default) | face-cam box | avatar | AI voice clone VO | live cameo requested by script.

## Integration
- Render config (pacing slider + presenter mode) lives with the concept card; manifest.json scenes carry per-visual duration_sec values generated from the pacing rules; evidence-capture ledger slots merge as time fillers.