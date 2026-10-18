# Render-chain pre-build research pass

Date: 2026-10-18. Scope: manifest-driven Remotion draft and future VO timing.

1. **Official / first-party — 4 sources; high; CHANGE.** [Remotion TransitionSeries](https://www.remotion.dev/docs/transitions/transitionseries) overlaps sequences and shortens total duration; exact 660-second chapter boundaries therefore need an explicit timeline rather than naïvely summing transition sequences. [Remotion Composition](https://www.remotion.dev/docs/composition) registers a renderable root. [Remotion fonts](https://www.remotion.dev/docs/google-fonts/) supports EB Garamond and JetBrains Mono. [Remotion render CLI](https://www.remotion.dev/docs/render) can produce local H.264 MP4. Use deterministic frame positions and local font assets.
2. **Peer-reviewed — 0 sources; none; IGNORE.** No psychological or causal claim is needed to implement this render pipeline.
3. **Industry benchmarks — 0 sources; none; IGNORE.** Pacing must follow the supplied first-party chapter times, not generic retention benchmarks.
4. **Community / creator-backed — 0 sources; none; IGNORE.** No creator anecdote changes frame math or source requirements.
5. **Open datasets / leaks — 0 datasets; none; CONFIRM.** The supplied script/manifest are the sole timing and image-prompt sources. No third-party footage or unlicensed audio is imported.
6. **Contradiction check — 2; high; CHANGE.** The supplied 660-second manifest has eight chapter boundaries, while audio and screen recordings are not yet supplied. Draft must retain all 19,800 frames with placeholders and an explicit silent audio track; later VO must extend rather than truncate a chapter. The hook imagery prompt does not include a human face, so the draft must visibly flag the required face footage as pending.

**GO.** Deltas: preserve absolute chapter starts/ends; implement transitions as overlays inside those bounds; render even with missing assets; add narration duration metadata to a derived local timing plan; keep recorded VO and draft output ignored.
