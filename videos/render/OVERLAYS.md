# Overlay animation demo

Reference study: [Matthew Berman — Hidden Codex Setting](https://www.youtube.com/shorts/IYvvbM7SKgY). Twelve frames inspected. Adapted split-screen hierarchy, short captions and drawn callout; original copy, interface and video base. Reference footage is not included. This is a silent motion-design sample with a fictional build-brief interface, not evidence of an agent completing the shown checks.

The 10-second 1080 x 1920 MP4 uses the existing six-second brand master as its upper video layer, then timed captions, a drawn arrow, a traced highlight, staggered checkmarks and a progress line. All state comes from frame number. `src/overlays/index.tsx` contains the reusable source.

From `videos/render`, copy the previous ident master to `public/overlay-base.mp4`, then:

```powershell
npx.cmd remotion studio src/overlays/index.tsx --config brand.config.ts
npx.cmd remotion render src/overlays/index.tsx OverlayDemo out/overlay-demo.mp4 --config brand.config.ts --codec h264 --crf 20 --concurrency 2
```

Use FFmpeg to create a lighter 720p copy after rendering. Local base media and renders are ignored. No external services, narration provider or copied reference assets are required.

Verified delivery (2026-11-05): C:\Users\olive\Videos\Ahead-of-Rush-Overlays\overlay-demo-final.mp4; H.264, 1080 x 1920, 30 fps, 300 frames, 10.000 seconds, 1,035,312 bytes. Full decode passed; delivery/master SHA256 both 14886A586B0B79B5043A283BD008B362E515D86EE30701AE9A4A6D5B1742D4A4. A 720p twin and 12-frame contact sheet are beside it. Contact sheet visually inspected. TypeScript and scoped ESLint passed.
