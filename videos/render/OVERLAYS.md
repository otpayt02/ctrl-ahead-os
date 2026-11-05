# Overlay animation demo

Reference study: [Matthew Berman — Hidden Codex Setting](https://www.youtube.com/shorts/IYvvbM7SKgY). Twelve frames inspected. Adapted split-screen hierarchy, short captions and drawn callout; original copy, interface and video base. Reference footage is not included. This is a silent motion-design sample with a fictional build-brief interface, not evidence of an agent completing the shown checks.

The 10-second 720 x 1280 MP4 uses the existing six-second brand master as its upper video layer, then timed captions, a drawn arrow, a traced highlight, staggered checkmarks and a progress line. All state comes from frame number. `src/overlays/index.tsx` contains the reusable source.

From `videos/render`, copy the previous ident master to `public/overlay-base.mp4`, then:

```powershell
npx.cmd remotion studio src/overlays/index.tsx --config brand.config.ts
npx.cmd remotion render src/overlays/index.tsx OverlayDemo out/overlay-demo.mp4 --config brand.config.ts --scale 0.6666666666666666 --codec h264 --crf 20 --concurrency 2
```

Omit `--scale` for 1080 x 1920. Local base media and renders are ignored. No external services, narration provider or copied reference assets are required.
