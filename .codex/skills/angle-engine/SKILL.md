---
name: angle-engine
description: Generate video concepts by mining the-brain corpus and connecting non-AI artifacts to AI-niche lanes through a controlled creativity slider (1-100, the CTV index) and multi-select angle/mode taxonomy — with fully transparent reasoning traces, tone-matched synopses, ranked output, longs/shorts separation, snippet ledgers below every script, and evidence-pointer emission for automated Playwright capture. Use for any concept, angle, or script generation request.
---

# Angle Engine (v3)

## Inputs
- creativity: 1-100 (the CTV creativity index — displayed on every card)
- modes: build-with-me | build-for-me | teardown/review | tutorial | documentary essay | live build | reaction-with-receipts
- angle twists: philosophical | reality-check | unrelated-artifact bridge | receipts/provenance | confession-opener | middleman frame | satire | sarcastic | ironic | funny | lighthearted
- lane: one of the 12 lanes from yt-niche-intel/script_inputs.json
- length: long | short
- presenter_mode: faceless | face-cam box | avatar | AI voice clone (default per video, can be requested by script)

## Creativity slider (magnitude of stretch)
- 1-20 Literal (same domain)
- 21-40 Adjacent (neighboring domain)
- 41-60 Metaphorical (structural mapping, argued in one sentence per link)
- 61-80 Cross-domain bridge (surprising link, explained stepwise)
- 81-100 Philosophical unification (reframes both domains)

## Procedure — the transparent reasoning trace
Every concept card carries the FULL ordered trace. The inference shows its work at every level:
1. CRITERIA DEFINITION. Before searching: what the angle needs for its goal to be met. What counts as a valid connection, what evidence types satisfy it, what fails it.
2. SEARCH PLAN. The corpus queries in the order run; state whether the pass is EXHAUSTIVE (brute force over all artifacts) or HEURISTIC (targeted filters), and why.
3. CANDIDATE HARVEST. N candidates found, each with artifact citations.
4. MAPPING TEST. For each survivor: the structural link + one-sentence mechanical justification ("same mechanism, not same vibes"). Reject vibes-only candidates explicitly, with the stated reason.
5. ATYPICALITY CHECK. Compare against lane winners (title bigrams, formats, proof types from script_inputs.md); reject or score.
6. EVIDENCE RESOLUTION. Emit evidence pointers for every claimed connection — handed to the evidence-capture skill for Playwright screenshot/recording. NO CONNECTION SHIPS WITHOUT RESOLVED EVIDENCE POINTERS.
7. VERDICT + RANK. Weighted score (connection strength x atypicality x lane fit); rank all outputs 1-50 and pin the rank at the top of the card.

## Synopsis contract
Every generated script is preceded by a synopsis paragraph (150-250 words) carrying the video's EXACT tone, mood, and angle. If the video is satirical, sarcastic, ironic, funny, or lighthearted, the synopsis is written in that voice; if earnest, it is earnest. The synopsis states topic, pattern, relationship, and angle, and cites textual evidence (pointing to the captured screenshots). No flat neutral summaries of a funny video.

## Snippet ledger (below the script, always)
Every generated script is FOLLOWED by the full snippet ledger: every snippet of text, screenshot, recording, audio clip, code line, AI-generated image, or uniquely-human artifact that the angle used to make its connections — annotated and extracted for direct render-manifest inclusion. Purpose: real evidence fills video time so fewer AI images must be generated.

Each ledger entry:
- id, snippet_type, source artifact + evidence pointer, extracted content (exact text/media)
- annotation: { reason for the connection through the selected angle, what the search was looking for when it found this (search context), why this was a good candidate, supporting details }
- recommended_animation (visually appealing, Remotion component + motion spec)
- manifest_slot: scene + time range, pre-wired for the render manifest as a time filler
- ctv_stretch_note: how far this annotation stretches, per the CTV scale below

## CTV-scaled annotation rule
Annotation legitimacy scales with the CTV index:
- LOW (1-30): connections must be logical, reasonable, intuitive — geniusly simple and obvious in hindsight but never said out loud by anyone but Oliver.
- MID (31-70): structural mappings, argued one sentence per link.
- HIGH (71-100): annotations may stretch — poetic, philosophical ties to the dynamics of the patterns and topics, connected to the brain's snippet contents as far as the index is high — each stretch flagged and justified.
Reasonable's definition moves with the index: the closer to 100, the more stretch allowed; the closer to 0, the more the connection must earn itself through logic while still being a thing nobody has said out loud.

## Output contract
- concept-card.json: rank, title, one-sentence caption (topic + pattern + relationship + angle), CTV index, lane, mode, length, presenter_mode, synopsis, full reasoning trace, evidence pointers, bridge + justification.
- script.md: synopsis first → timestamped narration (hook in first 3 seconds, zero intro; presenter_mode stated) → SNIPPET LEDGER (annotated, manifest-slotted).
- manifest.json: choreography per FACELESS-VISUAL-SYSTEM.md with evidence clips wired into ScreenCapture scenes; ledger manifest_slots merged in as time fillers.

## Longs / Shorts separation
- Longs and shorts are generated and listed in SEPARATE TABS (see videos/CONCEPT-CARDS-UI.md).
- Optional, post-script only, explicit user action: "Generate short from long" — a rendered long exports a snippet short via Remotion clip range; "Inspire long from short" — a standalone short spawns a long-form concept using its topic as the inspiration prompt.

## VO gating (approval gate)
- The voiceover file is generated ONLY after the script is approved. Order: script + ledger → user approval → VO file → media rendering. Never generate VO or render media from an unapproved script.

## Rules
- Nothing invents: every bridge traces to real corpus artifacts (brain prime rule).
- Every connection resolves to captured evidence before the script ships.
- The explanation must survive a skeptical viewer.
- Hook: confession opener, receipts, or bold on-screen text hook — first 2-3 seconds.