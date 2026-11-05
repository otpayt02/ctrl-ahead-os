# Ahead of Rush AI — signal brand animation

Six-second vertical ident: gold head, purple cloud, nine seeded strands and one emerald output. SVG preserves the silhouette and exact screen-space arrow angle; lit Three.js tubes provide depth. This is a new vector interpretation of the supplied local artwork, not its original vector master. Silent by design.

From this `videos/render` directory, with Node 22.13+ (Node 22 may require `--experimental-strip-types` for the check script) and FFmpeg on PATH:

```powershell
npm.cmd ci
npx.cmd remotion studio src/brand/index.ts --config brand.config.ts --port 3125
node scripts/check-brand.mjs
npx.cmd remotion render src/brand/index.ts AheadOfRushSignal out/aor-signal-draft.mp4 --config brand.config.ts --props brand-manifest.json --scale 0.5 --codec h264 --crf 23
npx.cmd remotion render src/brand/index.ts AheadOfRushSignal out/aor-signal-final.mp4 --config brand.config.ts --props brand-manifest.json --codec h264 --crf 17 --pixel-format yuv420p
ffmpeg -y -i out/aor-signal-final.mp4 -vf "select='eq(n,0)+eq(n,16)+eq(n,33)+eq(n,49)+eq(n,65)+eq(n,81)+eq(n,98)+eq(n,114)+eq(n,130)+eq(n,146)+eq(n,163)+eq(n,179)',scale=270:480,tile=4x3:padding=8:margin=8:color=0x111118" -frames:v 1 out/aor-signal-contact-sheet.png
```

The contact sheet runs left to right, top to bottom at frames 0, 16, 33, 49, 65, 81, 98, 114, 130, 146, 163, 179 (0.000 through 5.967 seconds). Integer rounding makes the intervals differ by at most one frame.

Edit `brand-manifest.json` to change seed, wave count (3–18), amplitudes, spatial convergence intervals, palette, fps, or duration. Intervals are x coordinates within the cloud; at least three must differ. Duration retimes the full choreography proportionally. `calculateMetadata` validates input and computes the frame count. No wall clock, random state accumulation, `useFrame`, remote font, or external media dependency is used.

The independent entry point and `brand.config.ts` preserve the documentary composition. For programmatic rendering, pass `chromiumOptions: {gl: 'angle'}` explicitly; Remotion's CLI config does not apply to Node rendering APIs. See the source-linked research note in `research/2026-11-03-aor-signal-brand.md`.

Renders remain ignored under `out/`. Delivery copies and validation results are recorded in `BRAND-DELIVERY.md`.
