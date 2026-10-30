# Corrected render manifest — 005, REA correction (supersedes v10/v11 on REA and shipped dates)

## Correction summary
- REA section is rebuilt, not patched: REA is a repo, not a model. No empty-stage "missing model" visual, no "Claude REA banned" popup, no Anthropic proof card presented as if it were REA.
- Shipped-list visuals carry dates: Opus 5.5 — Sep 22, 2026; Argon — announced Sep 30, 2026, generally available Oct 13, 2026. Neither is presented as new in the week of Oct 25, 2026.
- Everything else from v11 carries over: presentation model (one static slide per idea, fade in/out, overlays popping onto the slide at sentences/commas, no slow zoom, no pan, no image twice in a row), blue expand/compress subtitles (blue spoken word, white unspoken, spoken expands, others compressed, zero overlaps), cinematic proof text reveals (no screenshot, no document frame, no ledger manifest on screen), and the outro (first video, SUBSCRIBE, brass arrow, "We don't chase the future. We check it." / "Ctrl-Ahead — confirmed, not just claimed.").

## New / changed segments
1. Hook + verdict: four names, four different categories — rumor (GPT-7 Bel), repo (REA), leak (Carbon), training run (Qwen 4). Popup labels must say "REA — a repo" not "Claude REA banned".
2. REA slide (replaces the old "missing model" slide): a workshop/code slide — terminal and decompiler tools, an agent inspecting code it is allowed to examine. Popup: "Reverse Engineer Anything — github.com/morluto/rea". Overlay at the comma beats: MCP server, local analysis, viral in mid-October.
3. Anthropic bans slide (separate from REA): cinematic text reveal only — Oct 8 policy, effective Nov 12; Oct 12 tens of thousands of accounts banned for distillation. No wording that links either ban to REA.
4. "Banned" philosophy slide: four collapses, not three — account, behavior, model, and repo-mistaken-for-model (workshop vs worker). Popups: account = boundary, behavior = how we treat a mind, model = erasing a capability, repo = workshop, not worker.
5. Shipped list slide: GPT-6 Astra; Claude Opus 5.5 (Sep 22, 2026); Gemini 4 Argon (Sep 30 announced / Oct 13 generally available); Qwen 3.8. Each item gets its own popup with its date where the script gives one.
6. Recap slide: "a rumor, a repo, a leak, and a training run" — four popups, REA popup again as a repo, never as a banned model.

## Pipeline changes
- Source of truth for 005 is now script-corrected-rea.md, not vo2/script.txt. Any future render must start from the corrected script, re-record voiceover, re-align word times, and rebuild subtitles from the corrected text — do not reuse v10/v11 subtitle files for the REA section, because the words and timings changed.
- v10-render.mp4, v10-render-blue (killed mid-render, superseded), and v11-render.mp4 remain on disk for comparison only. They are NOT the corrected video and must not be published as the 005 video.
- Next build: v12, from the corrected script, following the v11 presentation model and the v10 blue subtitle system, with the segment changes above.
