# CHOREOGRAPHY SPEC — timestamped visual template for Ctrl-Ahead renders

Distilled 2026-10-30 from `TEARDOWN-5CH.md` (5 channels, 15 videos, evidence-tagged) plus the
2026-10-26 ai-reference-videos playbook and Oliver's standing render rules. Machine-readable
version: `choreography.json` in this folder — scriptgen consumes that file; this document is
the human-readable source of truth. Where the two disagree, this document wins and the JSON
must be fixed.

## The hard rules (non-negotiable, checked at manifest gate)

1. **Every narration beat gets a visual that shows what is being talked about.** When the voice
   names a company, the company's logo card is on screen. When it names a product, the product
   (UI capture, product shot, or generated visualisation) is on screen. When it states a result,
   the proof (screen capture, chart, output) is on screen. Words + word animation alone is
   **not** a visual. No text-only stretch longer than one caption line (~4s) is permitted
   anywhere in the render.
2. **Visual change cadence.** The on-screen visual changes at least every 3–6 seconds at the
   caption/headline level (a change must carry new information — a new claim line, a highlight
   moving to the cited words, a list item appearing as spoken). The hero asset changes at least
   every 20–45 seconds. No single static asset survives a whole section (teardown §synthesis-2).
3. **No slow zoom. No repeated image. No repeated motion.** Each generated image is used once.
   Motion vocabulary: popups, underlines, circles, cut-out reveals, spring settles, glimmer
   sweeps. Transitions are buttery: fades and glimmer sweeps on GSAP CustomEase butter curves.
4. **Subtitles:** one clean line at a time, spoken words in gold, never two lines, never
   karaoke-bounce on long-form.
5. **Proofs are cinematic text reveals** — full-screen, the cited text highlighted in sync with
   the spoken words (mouthfeed). A proof beat's visual is the document/output itself, never a
   generated image standing in for it. Generated media is metaphor/atmosphere only, never proof.
6. **Script purity** (baked into scriptgen, see `SCRIPT_PURITY_RULES`): the narration talks only
   about the topic and voices Oliver's opinions about the topic. It never mentions the
   production process, receipts/provenance, the pipeline, or the video's own attributes, and
   never presents obedience to build directions as reasoning — unless the pipeline itself is
   the topic.

## Beat template

Times are fractions of total runtime T, with an 8:00 (480s) reference render in brackets.
Formats scale: the **update** format (5–7 min) compresses beats 3–5; the **analysis** format
(12–15 min) stretches beat 4. Beat order is fixed.

### Beat 1 — HOOK · 0.00–0.04 T · [0:00–0:20]
- **Narration job:** dated facts → contradiction or stakes → promise. No greeting, no channel
  intro, no sponsor before the promise (teardown: 15/15 name the subject at 0:00).
- **Asset:** `logo_card` or `generated_image` — the subject itself: the lead company's logo
  card / product visual / the metaphor image that the thumbnail used. Subject on screen inside
  the first 2 seconds.
- **Motion:** spring settle-in of the logo card; headline claim builds word-group by word-group
  as spoken. **Transition in:** none (cold open). **Out:** glimmer sweep.
- **Subtitle:** active from the first word.

### Beat 2 — SETUP / DECODER · 0.04–0.12 T · [0:20–0:58]
- **Narration job:** what will be tested/checked, against what; decode any jargon name before
  evidence starts (playbook: name-decoder detour precedes evidence; teardown 2b: "What a
  shader is" is chapter 2).
- **Asset:** `logo_card` lineup — every contender named gets its logo card on screen as it is
  named (the AI Advantage "WHICH ONE?" lineup, faceless version); the test/checklist card
  builds item by item.
- **Motion:** cards slide/settle in sequence; checklist items pop in as spoken.
  **Transition:** fade.

### Beat 3 — PROOF BEATS (repeat per contender/item) · 0.12–0.55 T · [0:58–4:24]
- **Narration job:** claim → evidence → what it means, identical beat shape per contender
  (teardown 2c mirrored lattice). For update format: one feature = one beat, ≤ ~60s each
  (teardown §1).
- **Assets, in priority order:** `screen_proof` (the actual output/document, full-screen,
  cited text highlighted as spoken) → `chart` (numbers compared) → `generated_image`
  visualising the claim → `motion_clip` (generated clip, metaphor/atmosphere) → `logo_card`
  (when the beat is *about* the company rather than its output).
- **Motion:** still proof plates brought alive — popup callouts, underlines, circles land on
  the cited element exactly as it is spoken; comma/list changes appear as spoken.
  **Transitions:** fade between beats; glimmer sweep on contender swap (the swap is the rhythm).
- **Hard check:** a proof beat with no real proof asset is rendered as a generated
  visualisation + logo card and is *described in the script only as what it is* — never
  narrated as a run that didn't happen.

### Beat 4 — THE CATCH · 0.55–0.72 T · [4:24–5:46]
- **Narration job:** what breaks, what it costs, where the claim fails — Oliver's honest catch,
  as its own beat, placed late-middle (teardown §synthesis-4: ~65–75% in every channel that
  names it).
- **Asset:** `screen_proof` of the failure/limit where one exists, else `generated_image`
  visualising the limit (e.g. the VRAM wall, the price table as `chart`).
- **Motion:** the one deliberately different motion of the video — the glimmer sweep reverses,
  the headline settles slower. Signals "this is the part the launch post skipped."
  **Transition:** fade.

### Beat 5 — PAYOFF / VERDICT BY JOB · 0.72–0.88 T · [5:46–7:02]
- **Narration job:** verdict split by job/use — never a single overall winner (teardown
  §synthesis-3: every sampled comparison resolves this way).
- **Asset:** `logo_card` verdict table — one row per contender, logo + job + one-line verdict;
  rows light up as spoken. Cost-per-task figure appears as a `chart` element inside the row
  it belongs to.
- **Motion:** table builds row by row with spring settles; the recommended row gets the gold
  highlight sweep. **Transition:** glimmer sweep in.

### Beat 6 — WHAT YOU CAN DO (checklist close) · 0.88–0.96 T · [7:02–7:37]
- **Narration job:** the reusable artefact — checklist / cheat sheet / sizing rule the viewer
  can screenshot (teardown + playbook: the close is a tool, not a summary).
- **Asset:** `gsap_text` checklist card on the brand background; each item is accompanied by
  the mini visual of the thing it names (logo chip, icon, or thumbnail of the proof beat it
  refers back to) — the no-text-only rule applies here too.
- **Motion:** items build one by one, moving gold highlight. **Transition:** fade.

### Beat 7 — OUTRO · 0.96–1.00 T · [7:37–8:00]
- **Narration job:** welcome to first-time viewers, subscribe push, catchphrase.
- **Asset:** `logo_card` — Ctrl-Ahead brass-arrow brand mark, full-screen settle.
- **Motion:** brass-arrow spring settle + single glimmer pass. No new information after the
  catchphrase. **Transition:** fade to end card, hold ≥ 1.5s.

## Music
Background bed under all beats at felt-not-heard level (~10–15% of voiceover level, per the
playbook's guide rule): Suno-generated instrumental, selected per Oliver's AheadOfBeat rights
rule. Music presence in the 15 teardown samples is UNVERIFIED from public evidence — this rule
comes from Oliver's direction, not from the teardown. No beat change is ever timed to the
music; the narration clock rules the timeline.

## Format variants
- **Update format (5–7 min):** Beats 3 items ≤ 60s each; Beat 4 may merge into the last proof
  beat's tail but must still be *named* in the narration ("here's the catch").
- **Comparison format (7–13 min):** Beat 3 is the mirrored lattice — same asset order, same
  motion, contender swap only. Beat 5 verdict table is mandatory.
- **Analysis format (12–15 min):** Beat 3 sections may run 3–5 min **only** while the visual
  keeps changing at the headline/proof level (an unfolding argument is a changing visual;
  a static slide is not). Beat 2 decoder is mandatory.
- **Setup/build format:** Beats 3 items become numbered steps (teardown §3); the result step
  is the longest; Beat 4 is the mistake-to-avoid step.

## Manifest gate check (scriptgen should fail the build if any is false)
- [ ] Every segment in the manifest has a non-text hero asset assigned (asset_type ≠ gsap_text
      for at least one sub-beat per 20–45s window).
- [ ] Every named company/product in the script has a logo_card or product visual at its first
      mention.
- [ ] No image file appears twice; no motion preset repeats back-to-back.
- [ ] No slow-zoom motion anywhere in the manifest.
- [ ] Subtitle track is single-line with gold spoken-word styling.
- [ ] Script passes SCRIPT_PURITY_RULES (no process/receipt/pipeline/meta talk).
