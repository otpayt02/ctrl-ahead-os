# Silent pacing draft

The local draft is `../render/out/001-ai-lost-cause-draft-final.mp4`. It is intentionally git-ignored; render it again with `cd videos/render && npm.cmd run render`.

Verified on 2026-10-18 with Remotion's bundled `ffprobe`: 660.011 seconds, 30 fps, 960×540 H.264 video, AAC audio stream, 71,011,107 bytes. The AAC stream is silent. The draft uses all eight chapter slots from `manifest.json` and the eight generated illustrations in `assets/`.

This is a pacing and motion review copy. Human face footage, the two-model screen comparison, tracker screenshot, evidence snippets, and recorded narration remain to be captured and approved. Where media is absent, the renderer displays labeled placeholders. VO duration changes will extend chapter slots and move later chapters when recordings are added. The generated illustrations are labeled as such in the draft and described in `assets/provenance.json`.

## Deterministic pacing draft

The newer local review copy is `../render/out/001-ai-lost-cause-pacing-draft.mp4`, rendered from source commit `e42a6df`. It is also git-ignored. Remotion's bundled `ffprobe` reports 660.011 seconds, 30 fps, 960×540 H.264, an AAC silent track, and 112,852,604 bytes.

The renderer applies the manifest's seeded pacing plan in `Root.tsx`; each visual gets its own nested sequence and motion. Frame samples were extracted from the completed MP4 at the overlay beat (4 seconds), a stat chip (28 seconds), and every chapter boundary (25, 100, 190, 300, 390, 470, 580 seconds). All seven sampled boundaries contained image or a labeled media placeholder; none was black. The AI illustration label remained visible on sampled illustration cuts. The 190-second boundary shows the intentionally pending screen recording, and the 470-second illustration contains invented decorative glyphs, not authentic S'gaw Karen text.

Before this clean render, temporary ignored inputs tested (a) a 30-second S1 WAV extending the composition to 665.5 seconds / 19,965 frames and (b) a synthetic evidence ledger slot at 3–6 seconds suppressing the overlapping pacing chip while showing the ledger receipt. Those temporary inputs were removed, and media preparation returned to zero VO tracks. This review copy does not include approved footage, real receipts, or narration.

## Asset-integrated draft (2026-10-19)

The local file `../render/out/001-ai-lost-cause-assets-draft.mp4` was produced by `npm.cmd --prefix videos/render run render` after `prepare` copied 10 media assets. Remotion's bundled `ffprobe` reports **660.011 seconds**, **30 fps**, **960×540**, H.264 video, AAC audio, and **130,936,301 bytes**. This is the full-length review draft at half-size; the output is git-ignored.

`face-hook.mp4` uses the complete 8-second Veo picture at 1920×1080. The owner recording `hook-vo.wav` was 1.290667 seconds; leading silence was removed, presence was shaped, loudness measured -15.9 LUFS / -1.4 dBTP, source audio was replaced, and the remainder was padded with silence. There was no local lip-sync pass. The completed draft visibly contains the face at 1 second and a nonzero first-eight-second audio stream. The S6 graphic was rendered from `KOA-v4-project-tracker.xlsx`, `Project Plan!B29:F29`; it shows the task, `In Progress`, and `P0` at 435 seconds. It is a source-cell graphic, not a live spreadsheet screenshot or completion proof.

Nine frames were extracted from the completed MP4: S1 at 1 second, S6 at 435 seconds, and the seven chapter boundaries at 25, 100, 190, 300, 390, 470, and 580 seconds. All decoded as 960×540 images with nonzero luminance. The S4 boundary still contains a labeled pending-recording placeholder because the two-model comparison clip has not been captured. No full-chapter narration was present.
