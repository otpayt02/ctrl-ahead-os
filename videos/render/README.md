# Manifest-driven Remotion renderer

Scaffolded with `npx create-video@latest --yes --blank --no-tailwind render`. `prepare` copies the selected source manifest into the renderer and discovers media. Set `VIDEO_MANIFEST` to another video's manifest path for future videos; no component edit is needed. The source manifest is not rewritten.

From this folder run `npm.cmd ci`, `npm.cmd run lint`, then `npm.cmd run render:draft`. Use `npm.cmd run dev` for Studio. The draft command writes a full-duration H.264 MP4 with an explicit silent audio track when no VO exists. `out/`, generated media copies, and recorded VO are ignored by Git.

Scenes read `id`, `chapter`, `start`, `end`, `component`, `motion`, `assets`, and `on_screen_text`. Missing media displays a labeled placeholder. The opening 3 seconds mark Oliver's face footage as pending. The model comparison and tracker screenshot remain real-media placeholders. The eight PNGs are AI illustrations, labeled in their asset provenance file.

An optional `evidence/evidence_manifest.json` with pointers following the evidence-capture skill merges each `manifest_slot` into its chapter as a time filler. The renderer shows extracted text and a provenance label; the capture process remains separate. Visual crop states shift about every 7 seconds for pacing review.

After script approval, put recorded `S1.wav`, `S1.mp3`, or `S1.m4a` (likewise S2–S8) in the video's ignored `vo/` folder. `prepare` measures each actual file and extends its chapter if needed, shifting later chapters. This project does not synthesize VO.
