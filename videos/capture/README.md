# CTRL AHEAD — Artifact Capture Kit

Playwright drives a logged-in browser; ffmpeg (bundled in `../render/`) composites the recordings. The S4 replay command opens saved model replies and writes a ledger entry only after all four pages are verified and captured.

## One-time setup

1. `npm install`
2. `npx playwright install chromium`
3. Log in once per site — sessions persist in gitignored browser profiles:
   - `npm run login -- chatgpt`
   - `npm run login -- gemini`
   - `npm run login -- perplexity` (for the saved Chapter 4 test threads)
   - `npm run login -- google`  (Drive — for the tracker shot)

## Record the actual Chapter 4 model tests

The earlier tests used two frontier models inside Perplexity. A fresh ChatGPT/Gemini query cannot reproduce those replies. To record the **existing** replies, copy `s4-replay.example.json` to the ignored `capture-inputs/s4-replay.json`. Supply four saved Perplexity thread URLs: two Lost Cause replies and two S’gaw Karen replies. For each URL, paste a short phrase that is visibly present in that reply into `expected_text`. Do not put URLs or raw replies in the tracked example file.

```powershell
cd C:\Users\olive\Projects\ctrl-ahead-os\videos\capture
npm.cmd install
npx.cmd playwright install chromium
npm.cmd run login -- perplexity
Copy-Item s4-replay.example.json capture-inputs\s4-replay.json
# Edit capture-inputs\s4-replay.json with the four saved thread URLs and phrases.
npm.cmd run s4
```

Close the login browser to save its profile, then run `s4` with the browser visible. The command opens each exact URL, waits for its expected phrase, saves a proof screenshot and video, and stacks the two model replies for each test. It joins the two 55-second comparisons into a 1920×1080, 110-second `assets/s4-two-model-replay.mp4`. Only a successful four-thread capture replaces `S4-PENDING-TWO-MODEL-CAPTURE` with the **190–300 second** ledger slot. The video and private URL provenance remain Git-ignored; the tracked ledger stores URL hashes and a pending owner-review status. Inspect the four screenshots under `out/s4-replay/`, play the resulting MP4, and compare the visible replies with `../001-ai-lost-cause/script.md` before treating S4 as cleared.

If a thread cannot be reopened, or the expected reply text is hidden by a login wall, the command fails and leaves S4 pending. Do not substitute a newly generated answer for the recorded test.

## Local voice draft

Oliver's confirmed voice reference stays under the ignored `capture-inputs/voice-candidates/` directory. The local Sopro script uses that reference for zero-shot synthesis; it does not train or upload a voice model. The generated chapter WAVs and combined review audio stay under the ignored `../001-ai-lost-cause/vo/` directory.

```powershell
cd C:\Users\olive\Projects\ctrl-ahead-os\videos\capture
& .venv\Scripts\python.exe -m pip install -r requirements-voice.txt
& .venv\Scripts\python.exe scripts\generate-local-vo.py
# To regenerate only chapters containing S'gaw Karen:
& .venv\Scripts\python.exe scripts\generate-local-vo.py 4 5 7 8 --sgaw-spoken "suh gaw"
npm.cmd --prefix ..\render run prepare
```

The default reference path is `capture-inputs/voice-candidates/past-reference-final.wav`. Use `--reference <path>` for a different locally held owner recording. Listen to the WAVs before approval: written captions retain “S’gaw,” while the synthesizer receives Oliver's requested spoken form “suh gaw.” `prepare` detects chapter tracks but does not clear the Chapter 4 recording gate.

## Hands-off captures

| Command | What it does | Fills | Output |
|---|---|---|---|
| `npm run face` | Takes your Veo face clip + your VO recording from `capture-inputs/`, re-lipsyncs the mouth to your voice, trims to 1080p, muxes your audio | S1 face footage | `../001-ai-lost-cause/assets/face-hook.mp4` |
| `npm run vo` | Records your mic to `capture-inputs/hook-vo.wav` (list devices first, then pass `-Mic "<name>"`) | S1 VO | `capture-inputs/hook-vo.wav` |
| `npm run s4` | Opens four saved Perplexity replies, verifies visible text, and composites the two tests | S4 after owner review | `../001-ai-lost-cause/assets/s4-two-model-replay.mp4` |
| `npm run demo` | Asks ChatGPT + Gemini the config question as a new, separate experiment; does not change S4 evidence | New-run demo only | `../001-ai-lost-cause/assets/screen-compare-new-run.mp4` |
| `npm run tracker` | Opens the KOA v4 tracker Drive preview, spotlights the provenance row in amber, screenshots it | S6 tracker screenshot | `../001-ai-lost-cause/assets/koa-tracker-row.png` |
| `npm run webcam` | Records 6s face hook footage from your webcam via ffmpeg dshow (fallback if you skip the Veo route) | S1 face footage | `../001-ai-lost-cause/assets/face-hook.mp4` |
| `npm run snap -- --url <url> [--text "..."] [--sel "..."] [--out name.png] [--scene S6] [--note "..."]` | Generic screenshot of any page, optionally scrolled/highlighted to matching text | any evidence slot | `../001-ai-lost-cause/assets/` |

Face hook details: see `FACE-HOOK.md` (Veo prompt + VO recording + lipsync setup). Webcam first run lists devices; rerun with `powershell -ExecutionPolicy Bypass -File scripts/record-webcam.ps1 -Camera "<device name>"`.

Face stills for the face-cam box: copy your best local picture (Pictures folder, mirrored in Drive "My Computers") to `../001-ai-lost-cause/assets/face-still.png`, or use the GitHub avatar URL in `capture.config.json`.

## Evidence ledger

Capture commands that establish a matching artifact write to `../001-ai-lost-cause/evidence-ledger.json`. `npm run demo` does not write an S4 entry. `npm run s4` replaces the pending S4 entry only after all four saved replies are visible and a complete video is written. The renderer's evidence-slot merge places ledger assets into chapters; ledger slots outrank pacing overlays on collision.

## Codex run prompt (paste after captures)

> `videos/capture` is the new artifact capture kit. Reconcile its ledger output (`videos/001-ai-lost-cause/evidence-ledger.json`, manifest_slots shape) with the renderer's evidence manifest path, re-run media preparation, and re-render video 001 with the captured artifacts: `assets/face-hook.mp4` (S1, lipsynced to Oliver's real VO), `assets/screen-compare.mp4` (S4), `assets/koa-tracker-row.png` (S6). Never commit `videos/capture/auth/`, `videos/capture/out/`, or `videos/capture/capture-inputs/`. Verify duration and inspect frames at S1, S4, and S6.
