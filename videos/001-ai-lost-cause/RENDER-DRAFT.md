# Silent pacing draft

## Model-test revision gate (2026-10-20)

The narration now reflects Oliver's reported two-frontier-model tests: both models rejected the flattering Lost Cause prompt; the S'gaw Karen replies left conflicting counts and no model-retention measurement. Chapter 4's real two-model screen recording is still pending, so **do not render or publish a final video**. The three new test graphics say “GRAPHIC, NOT A CAPTURE” and cite Oliver's pasted summary, not a website or a raw model transcript. The editorial choreography covers 0–660 seconds; its timings must be aligned to the approved voice recording. Browser captures and blocked-page evidence are documented in `assets/captures/provenance.json`. The old MP4s remain ignored review copies of the superseded script. The manifest's inaccurate old overlays were corrected, but its final S4 timing and cuts must be checked against the approved capture before rendering.

## Remotion narration-cue preview (2026-10-20)

Local voice draft update (2026-10-21): eight private Sopro chapter WAVs now exist in ignored `vo/`; their combined speech duration is 540.46 seconds. `npm.cmd --prefix videos/render run prepare` detected eight VO tracks and 13 assets. The combined review MP3 is `vo/full-voice-draft.mp3`. Oliver requested the spoken form “SUH-GAW”; chapters 4, 5, 7, and 8 were regenerated with that phonetic input. Owner listening and cue alignment are still needed. The real Chapter 4 two-model recording remains pending; no new final MP4 was rendered.

`narration-cues.json` now provides 29 short, spoken-anchor cues. Remotion reads them during `prepare` and reveals their text with a masked word stagger. On scenes with these cues, the earlier seeded pacing chips and static chapter-wide kinetic caption are suppressed. Chapter titles and evidence graphics receive masked reveals too. The cue times are explicitly **editorial estimates** from the 67 visual beats; they are not word-aligned to Oliver's voice. Remotion Studio was inspected at frame 300 (the essay line) and frame 6030 (the Lost Cause control graphic and phrase cue). No final MP4 was rendered. Once approved chapter VO and word timestamps exist, run `align_narration_cues.py <word-timings.json>`, inspect the Studio timing, and then clear the final-render gate after the real S4 recording is present.

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

`CODEX_TASK.md` was executed again on 2026-10-19 after `git pull --rebase origin main` reported already up to date. The face and tracker rebuilds reproduced the committed asset SHA-256 hashes, the ledger retained exactly two slots, `prepare` found 10 assets, and lint/typecheck passed. A new `npm.cmd --prefix videos/render run render` exited 0 and reproduced the 660.011-second, 130,936,301-byte MP4. Ten frames from this new export were decoded and reviewed: S1 at 1 second shows the labeled face clip, S4 at 200 seconds shows the pending model-recording placeholder, S6 at 435 seconds shows the Row 29 graphic, and all seven chapter starts decoded with visible content.
