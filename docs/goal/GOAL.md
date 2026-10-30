# Ctrl-Ahead OS AI video

Goal ID: goal_5f4b02102812
Goal slug: ctrl-ahead-os-ai-video

## Description
Make a fully rendered video through Ctrl-Ahead OS, starting with the AI niche and expanding to other niches later. Use a real Oliver artifact, a specific AI subniche and angle, and free tools for screenshots, screen recordings, and voiceover.

HANDS-FREE RULE — set by Oliver 2026-10-26: Muse runs the pipeline hands-free. Oliver's blanket approval already covers topic pick, script, voiceover, draft render, captures/recordings, and edits. The ONLY approval before publish is Oliver approving the full render manifest. After that, Oliver gives feedback on the final video and Muse iterates on it. Muse takes captures/recordings itself — never ask Oliver to screenshot or record. If a tool cannot export a true screenshot, use its best in-system capture, label it honestly, and keep going. Blanket approval does NOT cover spending, account/payment setup, or publishing under Oliver's sign-in.

## Current shape
- Repo verified at commit b554874: no apps/, packages/, or scripts/ in the root. The working scrape is only yt-niche-intel (YouTube Data API v3).
- Subniches: 35 lanes in yt-niche-intel/subniche_lanes.csv, 103 seed queries.
- Randomised draft for video 002: subniche Freelance AI automation, artifact HIST 105 - Race and Reunion Essay 1 (found in Drive by name, content not quoted in the draft), format long video ~11 min faceless after hook, creativity index 73 (cross-domain, 61-80).
- Angle in one sentence: Freelance AI automation clients don't buy the automation, they buy a receipt they can check — the same lesson from writing about contested history in HIST 105.
- Draft concept, script, snippet ledger, and render manifest are in files/ for this goal, for Oliver's approval.
- CORRECTION 2026-10-25, per Oliver: 002 is HELD and its "pipeline itself" teaser is withdrawn. Scripts must be about a specific thing talked about this week in a subniche, not about Ctrl-Ahead parameters or the pipeline. The research layer (Muse) must run the scrape/inference itself first — yt-niche-intel harvest/velocity/comments/transcripts/mine where a key + local DB exist, otherwise a dated public search labelled as a proxy, never invented YouTube velocity/CTR/retention.
- Corrected lead for 003, in files/003-nemotron-local-llm-this-week-research-and-concept.md: Local LLM setups lane, this-week topic NVIDIA Nemotron 3.5 Bolt 74B-A9B (launched 16 Oct 2026, claimed 24GB with 2-bit quant), tested locally. Backup topic: n8n 3.0 Docker-only breaking changes. Voiceover/render for 003 also HELD until script approval.
- Bundle delivered 2026-10-25 per Oliver ("give me both and then 10 more"), in files/004-both-plus-10-more-concepts.md: full scripts for 003 Nemotron and 004 n8n 3.0, plus concepts 005-014 (Kimi, Claude Code plugins, Gemini small business hub, Sora gone/Veo-Kling migration, Ideogram Vector, TanStack/Baseten decisions, AI safety curbs, Mac local LLM sizing, S'Gaw Karen OCR, Claude Duet/Decisions API). All topic-first, VO/render HELD until Oliver picks one in chat.
- APPROVED 2026-10-25 by Oliver in chat: BOTH 003 Nemotron and 004 n8n 3.0 approved for voiceover then render, in that order per script. VO/render no longer held for these two.
- Harvest gap 2026-10-25: Grill Me is a client-only static artifact (no server actions), so it cannot run yt-niche-intel harvest itself. Harvest must run via Muse (research layer) with a YouTube Data API v3 key, then import script_inputs.json via the scrape-import box. API key request sent via Secure Vault; harvest runner to be added once key is supplied.

## Commitments and boundaries
- HANDS-FREE ORDER (2026-10-26, supersedes script-approval gate): research -> script -> render manifest -> VO -> render, all hands-free under blanket approval. Then: manifest approval (only pre-publish approval) -> final video -> Oliver feedback -> iterate -> publish (once manifest-approved and feedback incorporated, unless Oliver says hold).
- Do not invent biography. If the corpus did not say it, the script does not say it.
- Do not claim view velocity, CTR, retention, or swipe-away from public view counts.
- Do not use Apify, TikTok, Instagram, or Firecrawl as built — they are roadmap items, not implemented code.
- Free tools only for this video: Playwright screenshots, ffmpeg/OBS screen recordings, ffmpeg assembly, Piper TTS for voiceover, clean room audio (no paid Suno bed).
- Local Windows tree (C:\Users\olive\Projects\ctrl-ahead-os) and its local SQLite DB were not available on this Linux VM, so no fresh harvest, velocity, transcript, or script_inputs evidence was used in this draft. That evidence is UNVERIFIED / missing, not assumed.
- Idea gate is PARTIAL: the angle does not duplicate videos/001-ai-lost-cause, but the last 5 shipped angles could not be verified from the repo alone. Oliver must confirm that check before render.
- Capacity context from memory: Oliver is a chemical engineering student finishing at J.B. Speed School, an engineer/IT manager for a non-profit, and freelances in AI automation on Upwork/Fiverr. Keep the workload humane and do not optimise away sleep, rest, or other commitments.

- ANIMATION RULE (2026-10-26, Oliver): the 'what you can do' section is animated — checklist items build in, highlight moves, takeaway lands visually — to make the actionable close visually appealing. Animation spices up the presentation only; it never changes evidence, never fakes a run/screenshot, and labels stay on the frames.

- MILESTONE RULE (2026-10-26, Oliver): stop and ask for approval/feedback ONLY at the entire video, strung together and ready for YouTube as one final file. Never stop on individual segments, visuals, or VO chunks — iterate on the whole video every time.

- MOUTHFEED PROOF RULE (Ctrl-Ahead, set 2026-10-26, Oliver): every proof visual — screenshot, live render, or feed — is shown FULL-SCREEN, ZOOMED IN, with a smooth zoom/pan that lines up with the narration, and the cited textual evidence or concept being spoken about is HIGHLIGHTED on screen in large, easy-to-read text as it is said. The viewer does not search the page themselves; the video feeds it to them, passively. Use cinematic, buttery-smooth transitions (fades, not hard static cuts), animation overlays, and microinteractions (cards sliding in, highlight moving, items building) so the video has spark — the visuals carry the energy, because flat narration alone feels robotic. Animation/highlighting never invents text that is not on the source, never presents a render as a live screenshot, and labels stay on every frame.
