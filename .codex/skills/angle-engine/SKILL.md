---
name: angle-engine
description: Generate video concepts by mining the-brain corpus and connecting non-AI artifacts to AI-niche lanes through a controlled creativity slider (1-100) and multi-select angle/mode taxonomy. Use for "give me a video concept", "find angles", or any script_inputs-to-video generation request.
---

# Angle Engine

## Inputs
- creativity: 1-100 (slider, selected before generation)
- modes: build-with-me | build-for-me | teardown/review | tutorial | documentary essay | live build | reaction-with-receipts
- angle twists: philosophical | reality-check | unrelated-artifact bridge | receipts/provenance | confession-opener | middleman frame
- lane: one of the 12 lanes from yt-niche-intel/script_inputs.json

## Creativity slider (magnitude of stretch)
- 1-20 Literal (same domain)
- 21-40 Adjacent (neighboring domain)
- 41-60 Metaphorical (structural mapping, argued in one sentence per link)
- 61-80 Cross-domain bridge (surprising link, explained stepwise)
- 81-100 Philosophical unification (reframes both domains)

## Procedure
1. Pull candidate artifacts from the-brain corpus (essays, repos, music, dictations, history, trackers).
2. Map each candidate's internal structure onto the target AI lane.
3. Generate the bridge at the selected slider magnitude; the bridge MUST include a one-sentence mechanical justification ("same mechanism, not same vibes"). If the mapping is only vibes, lower the slider.
4. Atypicality check (Journal of Marketing 2026): reject concepts too close to existing winners in the lane (title bigrams, formats, proof types from script_inputs.md).
5. Emit: title options (matching winning title patterns), mode, angle, slider value, bridge + justification, artifact receipts, target lane.

## Output contract
`concept-card.json` + `script.md` (timestamped narration, hook in first 3 seconds with human face, zero intro) + `manifest.json` (choreography: scenes, assets, motion, on-screen text, transitions).

## Rules
- Nothing invents: the bridge must trace to real corpus artifacts (brain prime rule).
- The explanation must survive a skeptical viewer.
- Hook uses Oliver's signature devices: confession opener or receipts, first 2-3 seconds, human on screen.