# Veo + Free Video Animation Notes — Ctrl-Ahead OS
Date: 2026-10-26. Sources are search results checked 2026-10-26, not Google's own live pricing page — check Flow / Gemini API pricing before spending or publishing. No Veo clips were generated for this note; this is a prompt and usage plan, not a clip delivery.

## 1. What "free Veo" actually is
- Google Veo 3.1 lives in Google Flow, the Gemini app, Google Vids, AI Studio, and the Gemini API. Veo 2 is no longer served in Flow.
- Flow free: 50 Flow credits per day, no rollover, 18+, supported region. Per multiple guides reading Google's help pages: Veo 3.1 Lite = 10 credits, Fast = 20, Quality = 100. So free day = 5 Lite clips OR 2 Fast clips, never 1 Quality clip. Daily credits vanish at next refresh; non-subscribers may be blocked at peak hours (guides say roughly 2-5 PM UTC).
- Clip length: 4, 6, or 8 seconds (Quality: 8 only), plus Extend to chain clips. One minute of Veo = about 8 clips. Failed generations are not charged, per guides.
- Gemini API: NO free tier for Veo. API pricing per guides: Lite $0.05-0.08/sec, Fast $0.10-0.12/sec (1080p), Standard $0.40/sec, all with audio. So "free Veo" = Flow consumer credits, not API.
- Paid context, for budgeting only: Google AI Plus $4.99/mo (+200 monthly credits), Pro $19.99/mo (+1,000), Ultra $99.99 / $199.99 (+10,000 / +25,000). Students: guides say Google AI Pro free for a year if eligible — check terms, do not assume.
- Veo output carries invisible SynthID, per guides, not a visible watermark on free Flow clips. That does NOT make a Veo clip evidence — it is still AI-generated, and must be labelled AI on screen.
- Muse cannot generate Veo clips hands-free today: there is no Flow account connected here, no API free tier, and generating under Oliver's Google account would need his sign-in / credits. That is outside blanket approval (accounts/spending). Oliver generates in Flow, or Muse uses the open-source fallback below.

## 2. Open-source / free fallback that already works here
- ffmpeg + PIL (already used in v4/v5/v6): slow zoompan on a still (1.0 -> 1.08-1.35), fade in/out 0.8s, headline cards, highlighted proof cards, karaoke subtitles. This is the "good enough" clip-stringing system when Veo credits run out: one still + one slow camera move + one text move = one clip, strung with fades.
- Wan 2.2 / 2.5: truly open-source, Apache 2.0, no credits, no watermark, commercial use allowed per guides — BUT it needs a real GPU (guides say RTX 3060 or better). It cannot run on Muse's VM (7.7 GB RAM, no GPU, ~1.3 GB free). It is a route for Oliver's own machine / a rented GPU, not for this VM.
- Other hosted free tiers, all with catches (guides, Oct 2026):
  - Kling: ~66 credits/day, watermark, no commercial use on free, ~5-6 short clips/day, strong motion.
  - Hailuo: ~3 clips/day, watermark, 720p, good faces/expressions.
  - Luma Dream Machine: ~30 generations/month on free tier in some guides, watermark, 720p; other guides say Luma has no free plan now — check live before relying on it.
  - Runway: 125 credits one-time only, watermark, 720p.
  - PixVerse: daily credits, watermark, up to 540-720p.
  - Dreamina (Seedance): daily credits, watermark, cinematic shots.
  - Google Vids: 6 AI clips/month, 1080p, SynthID only — per one guide.
  - Pika: guides conflict / 0 monthly credits on free in Oct 2026 checks — do not rely on it.
- Rule: never publish a watermarked free-tier clip as clean, and never assume free-tier commercial use. Check the live licence for the tier actually used, and label the clip AI.

## 3. Oliver's personality / style, translated into animation direction
- Direct, informal, blunt, no corporate stock, no filler. Animation must be purposeful: one move per clip, not a montage of effects.
- Cinematic, world-class, purposeful motion. Slow push-in or slow pan, never a fast whip-pan inside an 8-second Veo clip — the move should feel like a camera, not a transition pack.
- Topic-first, evidence-first, hype-vs-reality. Veo is for metaphor and irony ONLY. Never for proof, numbers, tables, prices, benchmarks, or a model run. Proof stays as zoomed screenshots / rendered pages + highlighted cited text (mouthfeed rule).
- Philosophical directive close. The close animation is a ledger building, not a celebration: columns appear, the last two light up.
- Labels stay on every frame: "AI CLIP — NOT A REAL MODEL / NOT A SCREENSHOT" on any Veo/generated clip, "RENDERED FROM LIVE PAGE VISIT — NOT A LIVE SCREENSHOT" on proofs, "ANIMATED GRAPHIC" on cards.

## 4. Situation -> clip type (for the 005 angle, and reusable)
Use ONE action per 8-second clip. Put all on-screen text in ffmpeg AFTER generation, never rely on Veo to spell a model name, a number, or a headline — Veo text rendering garbles exactly the names this niche needs (Astra/Argon/Sol in the live AI Frontier transcript came out as Argonne/Saul in auto-transcription; do not add Veo text errors on top).

| Situation in narration | Humorous / ironic Veo (or fallback) clip | Camera | Why it fits Oliver's angle |
|---|---|---|---|
| Hook: three labs, three winners | Three boxers in a ring, each holding up his own scorecard, all claiming a win. Dry, literal, ironic. | Slow push-in on the scorecards, 8s | The AI Frontier boxing metaphor, made literal. The joke IS the fact-check. |
| GPT-7 Bel: single anonymous post becomes "GPT-7" | A whisper in a dark room, then the same whisper blown up onto a giant billboard. Or a paper plane becoming a rocket, then popping. | Slow zoom out, whisper -> billboard | Shows scale inflation without claiming Bel exists. Ironic scale, not a product shot. |
| Claude REA: no model found | An empty chair on a stage, a "RESERVED" sign, a ban hammer that hits a policy document, not a robot. | Slow pan across the empty stage to the document | The absence is the punchline. Do NOT show a robot being banned — that would invent the model. |
| Gemini Carbon: internal leak, not a product | A model behind frosted glass / a locked lab door, a hand peeking through a crack. Frosted, unfinished, no face. | Slow pan left-to-right across the glass, 8s | Leak = peek, not launch. Frosted glass = unconfirmed, by design. |
| Qwen 4: in training, not shipped | A model on a treadmill / a construction site with a "UNDER CONSTRUCTION" sign, scaffolding, no finished building. | Slow push-in on the sign, then the scaffolding | Training is work, not a release. Construction is honest and a little funny. |
| Leak commentary: gap between lab and public | A gap / canyon between two cliffs, a small bridge being built plank by plank. | Slow zoom out to show the gap | The philosophical beat, visualised without inventing a model. |
| What you can do: ledger | Four columns building, one by one; the first two grey, the last two (Confirmed, Shipped) lighting gold. This is already done in ffmpeg in v3/v5 — Veo is optional here, ffmpeg is cleaner for text. | Static camera, columns build (ffmpeg) | The directive close must be readable, not a Veo hallucination. Use ffmpeg for text, Veo only for mood if at all. |
| Verdict-by-job / routing | A switchboard / train yard: one train routed to coding, one to documents, one to science, no single "winner" train. | Slow pan along the tracks | Verdict-by-job, not a champion. Ironic only in that everyone wanted one winner. |
| A claim that turns out false | A balloon labelled with the claim, popping in slow motion, confetti that is just paper. Dry, not cruel. | Slow-motion pop, then slow zoom on the paper | The pop is the correction. Keep it dry — Oliver's humour is blunt, not slapstick. |

When NOT to use Veo / generated video:
- Proof: screenshots, launch pages, benchmark tables, prices, model cards — use zoomed proof + highlighted text.
- Any number, date, or name that must be exact — Veo will garble it, and a garbled number in a fact-check video kills trust.
- A model "running" — a Veo clip of a robot typing is not a run. Label it AI, or do not use it as a run.
- More than one Veo clip per narration beat — one metaphor per beat, then back to proof. Veo is spice, not the meal.

## 5. How to string clips together (good-enough example, open-source)
1. Storyboard by VO chunk (estimated timings from word-count, labelled as estimates until measured).
2. Per chunk, pick AT MOST one Veo/generated clip (8s max, one action, slow camera). Everything else is proof zoom, headline card, or animated close in ffmpeg.
3. Generate in Flow on Lite first (10 credits). Only re-run the winner on Fast/Quality if the clip is a keeper — do not burn Quality on a first draft.
4. Budget a 6-minute video on free Flow alone: 5 Lite clips/day = about 40 seconds of Veo/day. A full Veo video would take days of free credits. That is why v4/v5/v6 use Veo-style ffmpeg motion for most of the video and reserve generated clips for 2-4 metaphor beats.
5. Assemble in ffmpeg: Veo clip (8s, no on-screen text) -> fade 0.8s -> proof zoom -> fade -> headline card -> fade -> animated close. Add karaoke subtitles last (ASS, gold = spoken, white = not yet spoken, spanning the viewport), plus a separate SRT sidecar for YouTube upload.
6. Label every generated clip on its face: "AI CLIP — METAPHOR ONLY, NOT A REAL MODEL / NOT EVIDENCE". Put the label in ffmpeg, not in the Veo prompt, so it cannot be cropped out by a reframe.
7. Prompt template (for Flow / any free model):
   "Slow cinematic push-in, one action only, [subject], [ironic situation], dark background, muted colours, no text, no numbers, no logos, 8 seconds, 16:9"
   Negative: "no text, no numbers, no logos, no fast cuts, no morphing faces, no extra characters"
   Then add the real text in ffmpeg after generation.

## 6. What to check before publishing a Veo clip
- Is the clip's subject a metaphor, or does it look like evidence? If it looks like evidence, cut it or re-label it.
- Does it contain any readable text/numbers? If yes, check every character; if any are wrong, do not use it as proof — use it only as mood, with the AI label, or regenerate.
- Is the licence/watermark for the tier actually used cleared for YouTube commercial use? Free Kling/Hailuo/Luma/PixVerse tiers are generally watermarked / personal-use only per guides — do not publish those as clean commercial clips.
- Is the clip's length within the free daily budget, or did it burn Quality credits? Record credits used in the manifest, like quota is recorded for YouTube.
