# Pending Pipeline Tasks for Video 001

## 1. Build Final `face-hook.mp4`
- Source: `videos/capture/capture-inputs/veo-face.mp4` (or `veo_face_intro_wrong_speech.mp4`).
- Audio: If `hook-vo.wav` is available, trim leading silence, apply highpass/presence EQ and normalize to -16 LUFS, and mux over the full 8-second video (replacing synthetic audio). Otherwise, retain clean 8-second video.
- Format: Scale/crop to 1920x1080 -> `videos/001-ai-lost-cause/assets/face-hook.mp4`.

## 2. Generate S6 Tracker Receipt Graphic
- Source: `KOA-v4-project-tracker.xlsx`.
- Content: Render 1920x1080 dark theme graphic (`#0a1628`) highlighting Row 29 ("Store validated training pairs and consent records" | P0) in amber (`#e8a33d`).
- Destination: `videos/001-ai-lost-cause/assets/koa-tracker-row.png`.

## 3. Reconcile Evidence Ledger and Render
- Update `videos/001-ai-lost-cause/evidence-ledger.json` to link `assets/face-hook.mp4` (S1) and `assets/koa-tracker-row.png` (S6).
- Run `npm --prefix videos/render run prepare`.
- Render complete composition (`npm --prefix videos/render run render`).
- Verify duration (660s) and inspect chapter boundary frames.
