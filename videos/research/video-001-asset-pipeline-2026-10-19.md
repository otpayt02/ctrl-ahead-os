# Video 001 asset pipeline: pre-build check

1. **Official / first-party — 3 sources; high; CHANGE.** [FFmpeg filters](https://ffmpeg.org/ffmpeg-filters.html) document `silenceremove`, `highpass`, `equalizer`, `loudnorm`, and `apad`. [Remotion video](https://www.remotion.dev/docs/video) supports embedded video/audio. [openpyxl](https://openpyxl.readthedocs.io/en/stable/tutorial.html) reads the source workbook cells. Use measured input durations, trim the short VO's leading silence, pad its output to the full clip, and render the tracker from workbook data.
2. **Peer-reviewed — 0; none; IGNORE.** This is media processing and faithful data display; no behavioral or retention claim is needed.
3. **Industry benchmarks — 0; none; IGNORE.** The requested -16 LUFS is the owner-provided target, not a benchmark inferred from external data.
4. **Community / creator data — 0; none; IGNORE.** Anecdotal editing advice does not change the measured clip and VO durations.
5. **Open data / datasets — 1 local first-party workbook; high; CONFIRM.** `KOA-v4-project-tracker.xlsx`, `Project Plan!C29`, contains the target text and `F29` is `P0`. The full workbook stays outside the video repo; render only the cited row.
6. **Contradiction check — 3; high; CHANGE.** The current hook asset is 1.291 seconds because capture used `-shortest` with a 1.291-second WAV. The existing ledger has duplicate S1 entries and claims lip sync while configuration has no lip-sync command. Renderer preparation ignores `evidence-ledger.json`, so neither the video nor the tracker would appear without wiring.

**GO.** Deltas: preserve the full 8-second Veo picture; use processed owner VO for its first ~1 second and silence for the remainder; label lip sync as absent; replace duplicate ledger entries with one accurate S1 slot and one S6 row receipt; copy ledger media into render public assets; display the actual video/image in their slots; verify all chapter boundaries in the completed draft.
