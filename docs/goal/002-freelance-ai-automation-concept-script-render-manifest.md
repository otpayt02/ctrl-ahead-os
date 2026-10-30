# 002 — Freelance AI automation: sell the receipt, not the claim
## Concept card — DRAFT FOR APPROVAL, NOT RENDERED

- **Video ID:** 002-freelance-ai-automation
- **Repo checked:** https://github.com/otpayt02/ctrl-ahead-os at commit `b554874ab40feb4b9c61062b2c861f1127a2eea1`
- **Root check:** apps/, packages/, and scripts/ are NOT in the root at this commit. Do not run package.json scripts dev:landing, dev:os, intel:scrape, improv:analyze, or trial:generate as if they exist.
- **Subniche count:** 35 lanes in `yt-niche-intel/subniche_lanes.csv`, 103 seed queries. The angle-engine skill note about 12 lanes does not override the CSV — use the CSV lanes.
- **Subniche (randomised):** Freelance AI automation — seed queries in the CSV include "freelance AI automation", "sell automation to clients", "AI service business".
- **Artifact (randomised, human):** HIST 105 - Race and Reunion Essay 1 — found in Google Drive by name. Its text was NOT quoted in this draft, because its content was not opened here. A real capture must open the actual document and record extracted text before any line from it is used on screen or in narration.
- **Format (randomised):** Long video, about 11 minutes (660 seconds, same runtime shape as 001), faceless after the hook. The agent-alone version is fully faceless; a face-cam hook is optional only if Oliver records it.
- **Creativity index (randomised):** 73 / 100 — cross-domain band 61–80. Stretch flagged: a college history essay does not prove anything about freelance automation. The only transferable connection used here is provenance: show what was opened, what changed, and what failed, instead of asking the viewer to trust a summary.
- **Angle, in one sentence:** Freelance AI automation clients don't buy the automation, they buy a receipt they can check — the same lesson from writing about contested history in HIST 105.
- **Tone:** Direct, informal, unpolished, high contrast. Not corporate. The viewer-facing script below does not explain production tools.
- **Palette (faceless video, from videos/FACELESS-VISUAL-SYSTEM.md):** navy #0a1628, amber #e8a33d, cyan #c9d6df, paper #f5efe6. Display: EB Garamond. Data: JetBrains Mono. Do not mix this with the UI_RULES.md product palette in the same surface.

## Numbered task report

1. **Check the repo and count subniches — DONE.** Root listing at b554874 confirmed; 35 distinct subniches counted from subniche_lanes.csv; yt-niche-intel is the only working scrape pipeline.
2. **Pick subniche, angle, format, artifact, and creativity index — DONE.** Randomised picks are listed above. No hand-picked lane was substituted.
3. **Generate a script from the AI-niche parameters — DONE (draft).** Synopsis and timestamped narration are below, for approval. No scraped velocity, CTR, retention, or client result is claimed.
4. **Build a render manifest the agent can execute alone, free tools only — DONE (draft).** Timestamps, capture directions, and assembly steps are below. Screenshots and screen recordings are real captures only — never generated from memory.
5. **Voiceover and final render — HELD.** Do not run VO or render until Oliver approves the script. After approval: VO first, then render, in that order.
6. **Fresh YouTube intel (harvest / velocity / comments / transcripts / mine) — BLOCKED.** The local Windows tree and its gitignored yt_ai_niche.db were not available on this Linux VM, and script_inputs.json is not in the repo. Run that step on Oliver's Windows machine before claiming any lane velocity, top channel, or transcript pattern. UNVERIFIED claims in this draft are labelled as such.
7. **Idea-gate duplicate check against the last 5 shipped angles — PARTIAL.** This angle does not duplicate videos/001-ai-lost-cause, but only 001 is visible in the repo listing checked here. Oliver must confirm the last 5 shipped angles before render.

## Synopsis (in the video's actual tone, 150–250 words)

Most freelance AI pitches sound the same. Faster. Smarter. Automated. And the client has no way to check any of it until something breaks.

I learned the opposite habit writing history. When different memories fight over the same event, a clean summary is the most dangerous thing you can hand someone. A citation is not proof you opened the source. Repetition is not proof it's true. The only thing that holds up is the receipt: who said it, when, what you actually looked at, and where it disagreed with something else.

That's how I want to sell automation now. Not "trust the agent." Show the run. Show the input, the step that failed, the fix, and the output the client can open themselves. If the automation can't produce that receipt, it isn't ready to sell — it's just a demo with better lighting.

This video walks through that rule with a real document I wrote, a real repo, and a real freelance workflow, and it ends with a checklist a client can actually use to audit a job before they pay for it.

## Timestamped script — narration (draft, for approval)

**0:00–0:25 — HOOK**
"Your client doesn't care that your automation is smart. They care whether they can check it. If they can't check it, you didn't sell them a system. You sold them a story."

**0:25–1:40 — THE PROBLEM WITH A CLEAN PITCH**
"Most AI automation pitches are just a clean before-and-after. Before: messy work. After: done. No middle. No failure. No receipt. And that's exactly why clients get burned. A demo that never fails is not proof. It's editing."

**1:40–3:10 — THE ARTIFACT ON SCREEN**
"This is a paper I wrote for HIST 105, Race and Reunion. [ON SCREEN: real Drive document title only, until its text is captured and verified — do not quote lines that have not been extracted.] When histories disagree, the tidy version wins because it's easy to repeat. The messy version — the one with conflicting sources — is harder to sell, and it's the honest one. I don't need you to care about the history paper. I need you to steal the habit."

**3:10–5:00 — THE TRANSFER, FLAGGED AS A STRETCH**
"This is a cross-domain stretch, and I'm flagging it as one. A history essay doesn't prove a business rule. But the test transfers: open the source, keep the disagreement visible, and keep a record someone else can follow. In automation, that means: what input went in, what step ran, what failed, what changed, and what output the client can open without you in the room."

**5:00–6:50 — WHAT A RECEIPT LOOKS LIKE**
"A receipt for a freelance automation job is not a screenshot of a green checkmark. It's five things. One: the original input, untouched. Two: the prompt or rule that ran. Three: the run log, including the failure. Four: the output, in a file the client owns. Five: the thing you checked by hand, and what you found. If any of those are missing, say so. Missing is information. Hidden is a problem."

**6:50–8:30 — THE FAILURE TEST**
"Here's the test I use before I call anything done. Break it on purpose. Feed it a bad input. Watch where it stops. If it fails quietly and still says 'done,' it's not ready. A good system fails loudly. It tells you which step broke, and it leaves the bad output out of the client's file. That one habit is worth more than a faster model."

**8:30–9:40 — WHAT NOT TO CLAIM**
"I'm not claiming a client result, a revenue number, or a view count here, because I don't have a verified one for this video. [UNVERIFIED: no fresh harvest, velocity, or Studio metric was available for this draft.] If a freelancer shows you a number with no run behind it, treat it the same way you'd treat a citation nobody opened. Ask for the receipt."

**9:40–11:00 — VERDICT + CHECKLIST**
"So the rule is simple. Don't sell the automation. Sell the audit trail. Input. Rule. Log. Output. Hand-check. If you can hand a client that five-line receipt, you can charge for the work. If you can't, you still have building to do. Next video in this series: the pipeline itself, built in public, with the failures left in."

## Snippet ledger — real captures only, nothing faked

| Slot | Time | Type | Source to capture, for real | Status |
|---|---|---|---|---|
| L1 | 0:00–0:25 | text_block / kinetic type | "SELL THE RECEIPT, NOT THE CLAIM" — generated title card, labelled as video text, not a human artifact | To generate in render, after approval |
| L2 | 1:40–3:10 | png | Drive document title for HIST 105 - Race and Reunion Essay 1, opened in a real browser/Drive viewer via Playwright | PENDING — open the real document first, record extracted text |
| L3 | 3:10–5:00 | code_line / png | Repo tree for ctrl-ahead-os at b554874, and yt-niche-intel/subniche_lanes.csv lane "Freelance AI automation" | PENDING — Playwright screenshot of the real GitHub page / CSV viewer |
| L4 | 5:00–6:50 | text_block | Five-line receipt checklist, as video text | To generate in render, after approval |
| L5 | 6:50–8:30 | webm | Screen recording of a real, local automation run failing loudly on a bad input — only a run the agent or Oliver actually executes, with its real log on screen | PENDING — do not stage a fake client job |
| L6 | 9:40–11:00 | png | End card, series "CTRL AHEAD / BUILD IN PUBLIC", teaser "NEXT EPISODE · THE PIPELINE ITSELF" | To generate in render, after approval |

Every capture must store extracted_text so the script matches the screen. AI images are labelled AI. Human artifacts are labelled human. A real browser must open the referenced page. Do not fake a screenshot from memory.

## Render manifest — timestamps + directions for the agent, free tools only

**Global render settings (copy the 001 schema):**
- Resolution 1920x1080, 30 fps, runtime 660 seconds.
- Pacing: long-form default dwell 6–8 seconds, hard cap 15 seconds per image, jitter ±20–35%, a visible change (cut, zoom, pan, overlay) at least every 3–5 seconds, key evidence beats dwell ~30% longer, floor 2.5 seconds per visual.
- Layers: L0 Ken Burns base, L1 information anchors, L2 kinetic labels, L3 mobile-sized captions always on, L4 none (faceless agent-alone version).
- Audio: clean room audio only. No paid Suno bed for this video. Silence drop-out at the 9:40 callback, as in 001.

**Scene-by-scene directions:**

| Scene | Time | Visual direction | Capture / build step, free only |
|---|---|---|---|
| S1 HOOK | 0:00–0:25 | Ken Burns push-in 1.0x→1.12x, kinetic title "SELL THE RECEIPT, NOT THE CLAIM" | Build title card in the faceless palette; captions always on |
| S2 CLEAN PITCH | 0:25–1:40 | Split frame: clean before/after on one side, hidden middle on the other | Generate a labelled AI illustration only if used, and label it AI on screen; otherwise use plain kinetic type |
| S3 ARTIFACT | 1:40–3:10 | Slow push-in on the real document title, then a highlight on the title line only | Playwright screenshot of the real Drive document, opened in a real browser. No quoted text until extracted text is recorded |
| S4 TRANSFER | 3:10–5:00 | Lateral drift, questions building on screen: "WHICH INPUT? WHICH STEP? WHAT FAILED?" | Playwright screenshot of the real repo / CSV lane; kinetic overlays for the three questions |
| S5 RECEIPT | 5:00–6:50 | Five numbered cards, one per receipt line, each dwelling ~18 seconds with a cut or zoom inside the card | Build cards in the faceless palette; do not use a stock "checkmark" image as proof |
| S6 FAILURE TEST | 6:50–8:30 | Screen recording, full screen, cursor visible only if it is a real tutorial-style recording; otherwise use cinematic capture + synthetic cursor in post, and say so in the manifest notes | ffmpeg screen capture or OBS Studio (both free) of a real local run failing loudly. Keep the real log visible. Trim with ffmpeg. Export a waveform PNG if audio is trimmed |
| S7 WHAT NOT TO CLAIM | 8:30–9:40 | Kinetic type only, no fake metric graphic | Do not render a views, CTR, or revenue chart. The UNVERIFIED label in the script is intentional |
| S8 VERDICT + CTA | 9:40–11:00 | Slow pull-back, three takeaway cards, end card with subscribe + next-episode teaser | Build end card in the faceless palette; 0.5s crossfade within chapters, 12-frame whip-pan between chapters |

**Voiceover — HELD until approval, then free only:**
1. After Oliver approves the script in chat, generate VO with Piper TTS (free, local, open source) using a clear English voice model. Do not use a paid TTS or voice-clone service for this video.
2. Split VO by scene (S1–S8), normalise each file with ffmpeg loudnorm, and align cues to the timestamps above. If a VO line runs long, cut the visual, not the meaning — do not speed the VO up to hide a long line.
3. If Oliver prefers his own voice, that replaces Piper, and the agent-alone render pauses at this step for his recording.

**Assembly — agent alone, free only:**
1. Capture all PENDING ledger items for real, with extracted text saved alongside each file.
2. Assemble in ffmpeg (free) or, if a visual timeline is needed, in a free editor the agent can drive from the manifest — do not buy or trial-lock a paid editor for this video.
3. Export 1920x1080, 30 fps, with captions burned in or as a sidecar SRT, plus a silent 9:40 drop-out check.
4. Final QA before any upload: every on-screen claim traces to a captured file in the ledger; every AI image is labelled AI; every human artifact is labelled human; no metric, client name, or revenue figure appears unless a verified source was added after approval.
5. Do NOT upload, publish, or claim a Studio result. Upload and Studio logging (24h, 48h, 7d) are Oliver's next steps after he watches the render.

**Files to produce at render time (not in this draft):**
- `videos/002-freelance-ai-automation/concept-card.json`
- `videos/002-freelance-ai-automation/script.md`
- `videos/002-freelance-ai-automation/evidence/evidence_manifest.json` + media
- `videos/002-freelance-ai-automation/manifest.json` (copy the 001 schema, with the scenes above)
- `videos/002-freelance-ai-automation/render.mp4` (only after approval + VO)
