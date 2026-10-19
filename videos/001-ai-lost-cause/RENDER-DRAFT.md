# Silent pacing draft

The local draft is `../render/out/001-ai-lost-cause-draft-final.mp4`. It is intentionally git-ignored; render it again with `cd videos/render && npm.cmd run render`.

Verified on 2026-10-18 with Remotion's bundled `ffprobe`: 660.011 seconds, 30 fps, 960×540 H.264 video, AAC audio stream, 71,011,107 bytes. The AAC stream is silent. The draft uses all eight chapter slots from `manifest.json` and the eight generated illustrations in `assets/`.

This is a pacing and motion review copy. Human face footage, the two-model screen comparison, tracker screenshot, evidence snippets, and recorded narration remain to be captured and approved. Where media is absent, the renderer displays labeled placeholders. VO duration changes will extend chapter slots and move later chapters when recordings are added. The generated illustrations are labeled as such in the draft and described in `assets/provenance.json`.

## Deterministic pacing draft

The newer local review copy is `../render/out/001-ai-lost-cause-pacing-draft.mp4`, rendered from source commit `e42a6df`. It is also git-ignored. Remotion's bundled `ffprobe` reports 660.011 seconds, 30 fps, 960×540 H.264, an AAC silent track, and 112,852,604 bytes.

The renderer applies the manifest's seeded pacing plan in `Root.tsx`; each visual gets its own nested sequence and motion. Frame samples were extracted from the completed MP4 at the overlay beat (4 seconds), a stat chip (28 seconds), and every chapter boundary (25, 100, 190, 300, 390, 470, 580 seconds). All seven sampled boundaries contained image or a labeled media placeholder; none was black. The AI illustration label remained visible on sampled illustration cuts. The 190-second boundary shows the intentionally pending screen recording, and the 470-second illustration contains invented decorative glyphs, not authentic S'gaw Karen text.

Before this clean render, temporary ignored inputs tested (a) a 30-second S1 WAV extending the composition to 665.5 seconds / 19,965 frames and (b) a synthetic evidence ledger slot at 3–6 seconds suppressing the overlapping pacing chip while showing the ledger receipt. Those temporary inputs were removed, and media preparation returned to zero VO tracks. This review copy does not include approved footage, real receipts, or narration.
