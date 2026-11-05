# Current brand animation delivery

Verified 2026-11-05. Source implementation: `2bd0733`, branch `codex/aor-signal-brand`.

Actual delivery copies:

- `C:\Users\olive\Videos\Ahead-of-Rush-Signal\ahead-of-rush-signal-final.mp4` — 1,064,226 bytes; H.264; 1080 x 1920; 30 fps; 180 decoded frames; 6.000000 seconds; silent.
- `C:\Users\olive\Videos\Ahead-of-Rush-Signal\ahead-of-rush-signal-720p.mp4` — 350,426 bytes; lighter playable twin.
- `C:\Users\olive\Videos\Ahead-of-Rush-Signal\ahead-of-rush-signal-draft.mp4` — 211,983 bytes; half-resolution draft.
- `C:\Users\olive\Videos\Ahead-of-Rush-Signal\ahead-of-rush-signal-contact-sheet.png` — 318,951 bytes; 12 frames sampled from final master.

Master and delivery SHA-256 both: `4CF1DCE940654C49C4FA239C5971B8E188679FBE5B0C2103F5FFE6DD73223E69`.

Verification: TypeScript and scoped ESLint passed; `node scripts/check-brand.mjs` passed. FFprobe counted 180 frames and confirmed dimensions/rate/duration. Full FFmpeg decode completed without errors. Draft and final 12-frame sheets were visually inspected: clear cloud silhouette, inputs crossing rear outline, gradual alignment inside cloud, strands fading as common path takes over, unclipped wordmark and arrow. Arrow shaft angle and junction tangent also checked mathematically. Interactive Studio was opened; final visual acceptance here is based on exported frames, not an asserted real-time playback check. Source is pushed; no public video publication performed.

See `BRAND.md` for exact preview/render/contact-sheet commands and manifest parameters.
