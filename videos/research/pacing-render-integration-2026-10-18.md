# Pacing renderer integration: pre-build check

1. **Official / first-party — 2 sources; high; CONFIRM.** Remotion [Sequence](https://www.remotion.dev/docs/sequence) nests timing and resets `useCurrentFrame()` to the child sequence origin; [useCurrentFrame](https://www.remotion.dev/docs/use-current-frame) therefore suits per-visual motion and overlay offsets. Use integer frame boundaries calculated once in the timeline.
2. **Peer-reviewed — 0; none; IGNORE.** The requested change is timing implementation, not a behavioral or retention claim.
3. **Industry benchmarks — 0; none; IGNORE.** Manifest pacing settings are first-party creative direction. Generic benchmarks do not override them.
4. **Community / creator data — 0; none; IGNORE.** Anecdotal editing practices do not settle frame allocation or evidence precedence.
5. **Open data / datasets — 1 supplied manifest; high; CONFIRM.** `videos/001-ai-lost-cause/manifest.json` supplies eight chapter bounds and overlay pools. No external dataset is needed.
6. **Contradiction check — 2; high; CHANGE.** Existing SceneView treats each chapter as one image with a seven-second motion reset, so it does not honor `scene.visuals`. Original manifest bounds must remain authoritative while VO may lengthen the derived timeline; allocate visual frames proportionally over that derived scene duration. Evidence slots are separately merged and must take precedence over overlapping pacing chips.

**GO.** Deltas: apply the seeded pacing engine at the Root, distribute integer frames across visuals, render nested visual sequences, suppress pacing chips during evidence slots, preserve fixed provenance labeling, verify a new silent draft at chapter and chip frames.
