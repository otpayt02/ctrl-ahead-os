# Build notes — 006, "The 5-Day Roadmap, Explained" — FINAL RENDER 2026-10-30

**Final file:** `006-five-day-roadmap-final.mp4` in this folder; identical copy at `~/workspace/your_files/006-five-day-roadmap-final.mp4` (md5 0e916e19ef469143eb5835b76580c0ff).
**Verified (ffprobe):** 496.13s (8:16), 1920×1080, 30fps, h264 + aac (160k), 23,154,506 bytes (~23 MB).
**Audio check:** volumedetect mean −15.7 dB, max −0.8 dB; silencedetect (−45 dB, ≥2s) found NO dead-air gaps (music bed fills day-card/outro beats).
**Frame checks:** extracted and visually inspected frames at 2s, 10s, 25s, 37s (Day 1 card), 50s (Git + WHAT chip + gold caption word), 120s, 175s (SAM), 200s, 260s, 330s, 390s (RDS+S3 LATER frame), 400s, 470s, 492s (outro). All on-grade, chips and captions legible and synced.

## Fact fixes applied (both verified 2026-10-29, applied by default at VO stage per manifest OPEN ITEMS)
1. **AWS SAM year:** VO recorded as "And SAM, from **2016**" (not 2018); on-screen year chip is **2016**. SAM first released Nov 2016.
2. **S3 first-service claim:** VO recorded as "And S3, **one of Amazon's first services**" (not "Amazon's very first service"); the S3 chip reads the same. SQS (2004) predates S3 (2006) and keeps its own "AWS's first service" line in the Day 3 optionals, unchanged.
No other VO wording, order, or claims were changed. VO text as recorded is in `build/segments_data.py` and `build/vo/*.txt`.

## What was built
- All 21 VO segments from the manifest, Helio voice (`avocado_v2:MAI_03`) at natural pace (speed 100), recorded segment-by-segment via the TTS CLI. Raw narration 468.4s; final runtime is VO-driven with 0.55s segment tails, five 1.6s day cards, and the 8s outro.
- Timing/captions: faster-whisper (base.en) word timestamps on the concatenated VO (1,224 whisper words aligned to the 1,210 script words via difflib, the 005 method). Captions are the script VO text verbatim, re-split to ≤6-word single lines, current spoken word in gold (ASS, burned in). No provenance/meta labels on any frame — provenance lives in this file and the manifest only.
- Visuals: one illustrated metaphor plate per segment, drawn in-project (PIL) in the channel grade (charcoal-navy, neon cyan/pink, brass-gold) — time-machine checkpoint trail (Git), utility meter (AWS Account), packed box (Docker), ghost-typist editor (Cursor), printing press (Amplify), blueprint (SAM), bricks (React), facade (Vibe Coding), front door (Gateway), motion-sensor lamp (Lambda), endpoint tickets (AI Backend), ticket queue (FastAPI+SQS), filing cabinet (DynamoDB), bolted seam (Testing), garage shelves (RDS+S3), launch wall (Deploy), heart-monitor trace (CloudWatch), gauges (Grafana+X-Ray), route map (hook/close). No image is reused as another segment's plate; no slow zoom anywhere (static plates, cuts only).
- Chip system: WHAT / WHY / IF YOU SKIP IT (red) / HOW (green) chips pop in at the Whisper-aligned trigger word for each beat, with a synthesized tick at every stamp; day cards get a stinger + thump (day changes only); OPTIONALS segments carry the muted treatment + red LATER badge. Synthesized electropop music bed (in-project, Am–F–C–G) mixed low under VO, loudnorm −14 LUFS on the final mix.
- Outro (s09): separate silent 8s beat after the decided close VO — brass arrow, catchphrase "We don't chase the future. We check it.", tagline "Ctrl-Ahead — confirmed, not just claimed.", SUBSCRIBE pill. Close VO text unchanged.
- Build pipeline used: PIL plates + ffmpeg segment renders + concat + ASS burn-in (the established 005-style pipeline), rather than a fresh HyperFrames project — same presentation model, deterministic and re-renderable from `build/` (`segments_data.py`, `build_video.py`, `render.py`, `captions.ass`, `timeline.json`, `chip_times.json`).

## Fallback used — hook montage (honest record)
The manifest's 3 generated-video hook clips (VID-HOOK-1/2/3) were **NOT** generated: Vast.ai / LTX-2.3 is not yet rented and no spending was authorized for this build. Per the build instructions, the hook was built from still plates instead: three distinct plates (route map → launch wall → gauges) with quick cuts at the segment thirds, with the four beat labels flashing as chips across the cuts. If Oliver wants the LTX hook later, s01 (0:00–0:19.7) can be re-cut without touching the rest of the film.

## Known cosmetic notes (left for Oliver's feedback pass, not silently re-rendered)
- On two-line chips, the second line's descenders sit close to the chip's bottom border (readable in frame checks, e.g. Git WHAT chip at 50s).
- The garage-shelves plate for RDS+S3 is the most abstract of the plates.

## Status
Rendered, verified, **NOT published**. Awaiting Oliver's whole-video feedback.
