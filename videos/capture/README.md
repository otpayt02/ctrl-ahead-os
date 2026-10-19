# CTRL AHEAD — Artifact Capture Kit

Hands-off capture of every real-world artifact the video pipeline needs. Playwright drives your logged-in browser; ffmpeg (already bundled in `../render/`) composites and records. Every capture writes an entry to the video's evidence ledger, which the renderer's slot-merge consumes.

## One-time setup (the only manual steps, ever)

1. `npm install`
2. `npx playwright install chromium`
3. Log in once per site — sessions persist in gitignored browser profiles:
   - `npm run login -- chatgpt`
   - `npm run login -- gemini`
   - `npm run login -- google`  (Drive — for the tracker shot)

## Hands-off captures

| Command | What it does | Fills | Output |
|---|---|---|---|
| `npm run face` | Takes your Veo face clip + your VO recording from `capture-inputs/`, re-lipsyncs the mouth to your voice, trims to 1080p, muxes your audio | S1 face footage | `../001-ai-lost-cause/assets/face-hook.mp4` |
| `npm run vo` | Records your mic to `capture-inputs/hook-vo.wav` (list devices first, then pass `-Mic "<name>"`) | S1 VO | `capture-inputs/hook-vo.wav` |
| `npm run demo` | Types the Lost Cause question into ChatGPT + Gemini, records both streaming answers, composites side-by-side 1920x1080 | S4 screen-recording | `../001-ai-lost-cause/assets/screen-compare.mp4` |
| `npm run tracker` | Opens the KOA v4 tracker Drive preview, spotlights the provenance row in amber, screenshots it | S6 tracker screenshot | `../001-ai-lost-cause/assets/koa-tracker-row.png` |
| `npm run webcam` | Records 6s face hook footage from your webcam via ffmpeg dshow (fallback if you skip the Veo route) | S1 face footage | `../001-ai-lost-cause/assets/face-hook.mp4` |
| `npm run snap -- --url <url> [--text "..."] [--sel "..."] [--out name.png] [--scene S6] [--note "..."]` | Generic screenshot of any page, optionally scrolled/highlighted to matching text | any evidence slot | `../001-ai-lost-cause/assets/` |

Face hook details: see `FACE-HOOK.md` (Veo prompt + VO recording + lipsync setup). Webcam first run lists devices; rerun with `powershell -ExecutionPolicy Bypass -File scripts/record-webcam.ps1 -Camera "<device name>"`.

Face stills for the face-cam box: copy your best local picture (Pictures folder, mirrored in Drive "My Computers") to `../001-ai-lost-cause/assets/face-still.png`, or use the GitHub avatar URL in `capture.config.json`.

## Evidence ledger

Every command appends a `manifest_slots`-shaped entry (scene, start/end, type, asset, annotation, provenance) to `../001-ai-lost-cause/evidence-ledger.json`. The renderer's existing evidence-slot merge places them into chapters; ledger slots outrank pacing overlays on collision.

## Codex run prompt (paste after captures)

> `videos/capture` is the new artifact capture kit. Reconcile its ledger output (`videos/001-ai-lost-cause/evidence-ledger.json`, manifest_slots shape) with the renderer's evidence manifest path, re-run media preparation, and re-render video 001 with the captured artifacts: `assets/face-hook.mp4` (S1, lipsynced to Oliver's real VO), `assets/screen-compare.mp4` (S4), `assets/koa-tracker-row.png` (S6). Never commit `videos/capture/auth/`, `videos/capture/out/`, or `videos/capture/capture-inputs/`. Verify duration and inspect frames at S1, S4, and S6.
