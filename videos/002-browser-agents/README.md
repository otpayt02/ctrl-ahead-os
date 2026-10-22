# Browser agents Short

Composition: `BrowserAgentsShort` in `videos/render/src/index.ts`, 1080×1920, 30 fps, 1200 frames.

Temporary audio lives at `videos/render/public/browser-agent/temporary-voice.wav` and is Git-ignored. Replace this WAV with an approved real recording at the same path, update the word events in `shot-manifest.json` from the recording, then render again. This is a review draft; timing is estimated.

Render command from `videos/render`:
`npx remotion render src/index.ts BrowserAgentsShort out/browser-agent/review.mp4 --codec h264 --crf 27 --concurrency 2 --browser-executable /usr/bin/chromium`

Review check: `ffprobe` measured the first render at 40.000 seconds; eight stills were extracted at 0.8, 4.2, 7.5, 10.5, 15, 22, 27, and 37 seconds and visually inspected as a contact sheet. These outputs are under ignored `videos/render/out/browser-agent/`.
