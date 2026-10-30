# TEARDOWN — 5 AI-niche channels, 15 videos

Built 2026-10-30 for the Ctrl-Ahead OS render backend, at Oliver's direction: scrape 5 AI-niche
channels, tear down their videos, and distill a timestamped choreography spec (see
`CHOREOGRAPHY-SPEC.md` + `choreography.json` in this folder). Extends — does not replace — the
2026-10-26 `ai-reference-videos-playbook` (8 earlier teardowns; its 3–5s visual-change guide rule
and AI Frontier timestamp map are cited where used).

## Evidence discipline

Every claim below carries a source tag. Nothing was frame-measured and no transcript was
retrieved for any of these 15 videos, so **no cut counts, no retention figures, and no spoken
first-30-seconds are claimed anywhere in this document**.

- `[API]` — YouTube Data API v3 via the registered `custom.youtube` connector, live 2026-10-30
  (channel stats, view/like/comment counts, durations, full descriptions incl. chapters).
- `[page]` — the video's public watch page as fetched 2026-10-30 (description text as published).
- `[chapters]` — the creator's own chapter list in the description (via `[API]`/`[page]`).
  Chapter spacing = **section length**, not a cut count.
- `[thumbnail]` — the video's thumbnail image, downloaded and visually inspected 2026-10-30.
- `[playbook]` — the 2026-10-26 playbook artifact (secondary guides / earlier live research).
- `UNVERIFIED` — could not be established from public text or image evidence.

Snapshot note: all view counts are 2026-10-30 snapshots and will have moved.

## Channel selection

Picked against Ctrl-Ahead's own lanes (model comparisons, model-release breakdowns, AI news,
local-LLM setups, coding agents, paper walkthroughs, hype-vs-reality). Two of the five are fully
faceless (AI Explained, Two Minute Papers) — the closest structural peers to Ctrl-Ahead's
faceless render format. The first handle lookups for The AI Advantage and AI Explained resolved
to impersonator channels via the API; the real channels were confirmed by cross-referencing
multiple independent listings before sampling (handles below are the verified ones).

| Channel | Handle | Subs [API] | Why it's in the set |
|---|---|---|---|
| The AI Advantage (Igor Pogany) | @aiadvantage | 492,000 | Tool/product update lane; densest chapter pacing in the sample; logo-led thumbnails |
| MattVidPro AI | @MattVidPro | 305,000 | Hands-on model/tool testing; same-test-on-every-contender structure at long length |
| AI Andy | @TheAIAndy | 214,000 | Step-by-step build/automation lane; published a video on REA — Ctrl-Ahead 005's exact topic |
| Two Minute Papers (Károly Zsolnai-Fehér) | @TwoMinutePapers | 1,840,000 | Faceless paper/model explainers; logo-as-hero thumbnails; the reach ceiling of the faceless format |
| AI Explained (Philip) | @aiexplained-official | 457,000 | Faceless deep analysis; closest peer to Ctrl-Ahead's verdict-driven format; evidence-linked descriptions |

Sampling rule: from each channel's 20 most recent uploads [API], the 3 highest-viewed
long-form videos (≥ ~5 min; Shorts excluded), favouring recency. 15 videos total.

---

## 1 · The AI Advantage — product-update lane, fastest section clock in the sample

Channel pattern [API][chapters]: every sampled video opens its chapter list at 0:00 with the
product/feature itself ("Meet Claude Motion & Check Availability"), never a greeting chapter.
Descriptions lead with a course/community CTA before any content summary [page].

### 1a · "New Claude Motion is Insane" — qZqZ02AsYiA
- 79,716 views · 5:11 · published 2026-10-14 · 795 likes · 48 comments [API]
- Chapters (7) [chapters]: 0:00 Meet Claude Motion & Check Availability → 0:50 Create Your First
  Animation → 1:54 Edit Text & Timing → 2:31 Add Images & Make Targeted Changes → 3:15 Customize
  Colors & Branding → 3:53 Use Motion in Your Business → 4:43 Explore 500+ Claude Examples.
  Section lengths: 50s, 64s, 37s, 44s, 38s, 50s, 28s — a new labelled section roughly every
  **45 seconds**.
- Hook structure: title is evaluative claim + product name; first chapter is the product name
  itself, so the subject is on screen from 0:00 [chapters]. Spoken hook UNVERIFIED (no transcript).
- Visual system: a product-feature walkthrough — description promises "a practical example, how
  to edit it, and 500+ Claude animation examples" [page], i.e. the visual carrier is the product
  UI itself, section by section. Finer visual cadence UNVERIFIED.
- Thumbnail [thumbnail]: giant product wordmark "CLAUDE MOTION" + the Claude starburst mark,
  a "IN 5 MINS" time-box badge, and the actual product UI (an animation timeline) on a laptop
  screen; the presenter appears only as a small figure beside the laptop. **The product and its
  logo are the thumbnail; the human is set dressing.**
- Music/subtitles/transitions: UNVERIFIED from public text.

### 1b · "ChatGPT & Claude Keep Getting Better… Here's What Actually Matters!" — yWL93gjFNd8
- 49,890 views · 10:47 · 2026-10-09 · 685 likes [API]
- Chapters (13) [chapters]: update-roundup structure — one chapter per feature (GPT-6
  Intelligent UI, ChatGPT Meetings, ChatGPT Pages & Sites, Audio Uploads, Scan Documents, Claude
  in Google Docs/Sheets/Slides, …), closing chapter "Final Thoughts" at 10:18. Section lengths
  26s–98s, median ~48s.
- Pattern worth stealing: a multi-item update video holds pace by giving **every feature its own
  labelled section under a minute**; the items are the segmentation, no connective tissue chapters.
- Thumbnail [thumbnail]: the two rival brand marks (Claude starburst, ChatGPT knot) staged as
  opposing armoured riders — a versus metaphor built entirely from the two logos — over the
  banner "MUST-KNOW UPDATES". No presenter face.

### 1c · "My Honest Take on Muse, Grok Bot, Dots & Duet" — Bd8-geZPwI4
- 41,536 views · 17:26 · 2026-10-23 · 523 likes [API]
- Chapters (13) [chapters]: task-led, not feature-led — each chapter is a job done with an agent
  ("Booking Meetings Through Slack With Dots", "Daily Briefs and Urgent Alerts With Grok Bot"),
  then a comparison chapter ("Choosing Between Muse and Grok Bot", 7:02) and a verdict chapter
  ("My Final Picks: Muse, Dots, Duet, and Grok Bot", 14:36) that runs the last ~2:50.
- Pattern worth stealing: at 17+ minutes the channel still resolves to **verdict-by-product in a
  named final chapter** — the same verdict-by-job shape the playbook found in the comparison lane.
- Thumbnail [thumbnail]: presenter face centred behind a row of four oversized app-icon tiles
  (ChatGPT, Muse, Dots, Duet) under the question "WHICH ONE?" — the logo-card lineup *is* the
  comparison, readable before the title is.

**Channel takeaway:** name the product at 0:00, keep sections ≤ ~60s in the update format, and
let logos/product UI carry the visuals. Long videos still end in a named verdict chapter.

---

## 2 · MattVidPro AI — the same test, run long, with the failures left in

Channel pattern [chapters]: long narrative builds (18–25 min), chapters named after what he is
doing or building, verdict reserved for a named late chapter. Sponsor appears as its own labelled
chapter mid-video (see 2b) rather than a pre-roll block.

### 2a · "GPT-6 Astra will Make you Think BIGGER." — UZZ53F_kEAA
- 89,866 views · 24:28 · 2026-09-08 · 1,386 likes · 201 comments [API]
- Chapters (10) [chapters]: 0:00 First impressions → 0:55 What the community is building (5:11
  long — the longest single section in this channel's sample) → 6:06 My playable jelly game →
  8:11 Solving camera, physics and world-design problems → 10:59 Why specific direction matters →
  12:20 The RPG I left Astra to build → 16:42 Where autonomous development fell short → 18:21
  Using Astra in Codex → 20:52 Usage costs and computer use → 22:06 "Astra, Sol or Luna? My
  verdict" (final 2:22).
- Structure: **impressions → other people's results → my build → where it broke → cost →
  verdict-by-model**. The failure chapter ("Where autonomous development fell short") sits at
  ~68% — late enough that the viewer has seen the wins first, early enough to be believed.
  Matches the playbook's Fireship lesson: the embarrassing failure is the credibility beat.
- Thumbnail [thumbnail]: presenter face (small, left) beside the actual artifact he built — the
  jelly creature from the game — under "GPT-6 ASTRA / I MADE THIS!". The thumbnail shows the
  **output of the test**, not the tool's logo.

### 2b · "Claude Rebuilt This AI Video in Unreal Engine (Zero Imported Assets)" — B0HN9kLxf7A
- 34,928 views · 18:48 · 2026-10-21 · 689 likes [API]
- Chapters (11) [chapters]: 0:00 "An AI video... but what if you could walk inside it?" (a
  question as the opening chapter title) → 1:07 What a shader is (decoder beat) → 2:35 Seedance
  fakes a video game → 3:51 Round 1: driving the fake game → **5:53 Sponsor: Crusoe (84s,
  labelled as its own chapter, ~31% in)** → 7:17 The pirate cabin plan → 10:34 The pirate cabin,
  built in Unreal → 14:32 Unreal vs. the AI video → 16:48 "Shader or Unreal? My verdict" →
  17:25 Someone else used it for texture compression → 17:56 Outro (52s).
- Description [page]: states the method and the receipts in prose — what was rebuilt, in what
  tool, in how long (45 minutes), what it cost at API rates, plus links to the exact repo/prompt
  used. The description does the provenance work so the video doesn't have to.
- Thumbnail [thumbnail]: the rebuilt artifact itself (the Unreal pirate cabin) fills the frame;
  presenter face small at right; badge "0 IMPORTED ASSETS" restates the title's constraint as a
  proof-stat; headline "THIS IS UNREAL?".

### 2c · "Opus 5.5, GPT-6 Sol & Luna TESTED on Creative Ideas" — 2WyFHZ6lkWE
- 26,346 views · 22:32 · 2026-09-23 · 441 likes [API]
- Chapters (10) [chapters]: a **strictly mirrored A/B lattice** — 0:40 Opus Animation / 3:07 Sol
  & Luna Animation → 6:15 The Prompt → 6:59 Opus Game / 9:12 Sol & Luna Game → 12:45 Opus CRT /
  15:17 Sol & Luna CRT → 17:58 Community Builds → 19:45 Price & Verdict.
- Pattern worth stealing: identical briefs, identical order, contender swap as the only variable;
  the shared-prompt chapter (6:15) is placed *after* the first pair so the audience has seen one
  round before being shown the method. Price is folded into the verdict chapter, not given its
  own section.
- Thumbnail [thumbnail]: a frame of the actual test output (the lemon-vs-orange animation) with
  comic impact graphics, presenter pointing at it; headline is a verdict quote: 'CLAUDE JUST
  "GETS IT."'

**Channel takeaway:** the visual that carries each beat is **the thing being tested, running**.
Sections can run 2–4 minutes because the artifact on screen is itself changing. Ctrl-Ahead's
equivalent: the screen proof / the artifact run must be the hero visual of every test beat —
never a static slide *about* the test.

---

## 3 · AI Andy — numbered steps, and the catch gets its own chapter

Channel pattern [chapters]: build/setup videos are structured as numbered steps with a
late "catch" beat; descriptions carry a comment-prompt CTA and full tool links [page].

### 3a · "I Built JARVIS With GPT-6 Astra (It's INSANE!)" — z-YT6Ef6jxc
- 15,928 views · 16:50 · 2026-09-23 · 200 likes [API]. **No chapters published** — internal
  structure UNVERIFIED from public text.
- Description leads with a funnel CTA ("Get FULL Jarvis 5-MIN Install") before any summary [API].
- Thumbnail [thumbnail]: no presenter face at all — a generated robot hero image, the OpenAI
  logo glowing in its palm, labelled "GPT-6". The model logo is drawn as the power source of the
  build. (Faceless thumbnail on a face-led channel, on its most-viewed recent long video.)

### 3b · "Claude Edits My Videos While I Do Nothing (DaVinci Resolve Setup)" — 0ad9Qzc8GGQ
- 9,225 views · 16:49 · 2026-10-09 · 100 likes [API]
- Chapters (7) [chapters]: 0:00 Intro → 1:04 Step 1: Get the tools → 2:56 Step 2: The rough cut
  → 5:45 Step 3: Chapter animations → 8:18 Step 4: Overlays and tips → 11:01 Step 5: Editing the
  intro → 12:25 "The mistake to avoid" (final 4:24 — the longest section is the failure beat).
- Thumbnail [thumbnail]: two giant app-icon tiles — Claude starburst → arrow → DaVinci Resolve —
  with the presenter small between them, under "SET UP ONCE" (the payoff phrase, underlined in
  red). **The workflow is drawn as logo → logo.** A faceless render can copy this exactly:
  logo cards + one arrow + the payoff line.

### 3c · "How To Reverse Engineer Any Software in Minutes" — HLsMMsvPDLY
- 5,063 views · 13:34 · 2026-10-13 · 87 likes [API] — *the same topic as Ctrl-Ahead 005 (REA).*
- Chapters (8) [chapters]: 0:00 Intro → 0:44 Step 1: What is REA? → 1:56 Step 2: How it works →
  3:25 Step 3: Set it up → 4:29 Step 4: Pick an app (the prompt) → 7:41 Step 5: The result –
  TickTick vs my clone (3:12, the longest step) → 9:39 Step 6: The catch → 11:30 Step 7: Build on
  top of your own app.
- Description [page]: names the artifact and the honest limit in prose — he cloned TickTick
  "in about an hour", shows "the exact prompt I used, and where the clone still falls short";
  links the REA repo and the decompilers used. Comment CTA: 'Comment "REA" and tell me which
  one' — the close doubles as a sequel prompt (same mechanic as the playbook's knockout video).
- Thumbnail [thumbnail]: the repo path as the headline ("github/reverse-engineer", hand-underlined
  in red) beside a proof-stat, "★ 179k stars" — a number from the subject itself, not a claim
  about the video.

**Channel takeaway:** numbered steps make progress legible; the result step is the longest;
the catch is a named chapter, not a footnote; the thumbnail leads with the subject's own name
and a verifiable stat.

---

## 4 · Two Minute Papers — faceless, logo-as-hero, no published chapters

Channel pattern [API][page]: descriptions are minimal and identical in shape across the sample —
sponsor line first (Lambda), then links to the paper/source, then Patreon credits. **No chapters
in any of the 3 sampled videos**, so internal section structure is UNVERIFIED from public text;
the channel's established format (narration over paper figures and result clips) is recorded in
the playbook as secondary evidence [playbook], not re-verified here.

### 4a · "GPT-6 Astra Changes Everything" — eVBJIUxv8N8
- 580,163 views · 5:22 · 2026-09-08 · 10,433 likes · 1,128 comments [API] — the highest-viewed
  video in this teardown.
- Thumbnail [thumbnail]: the OpenAI knot, glowing, *leaping a chasm* — the claim of the title
  drawn as a literal metaphor image — beside two words, "MASSIVE LEAP". Channel bug top-left.
  No face, no screenshot: **logo + metaphor scene + 2-word verdict**.
- (Watch-page fetch for this video returned HTTP 429 on 2026-10-30; description/chapter data
  above is from the API record.)

### 4b · "OpenAI's New AI Is Doing Things We Barely Understand" — z_sXLlLVUls
- 367,875 views · 8:49 · 2026-10-13 · 5,723 likes [API]
- Description [page]: sponsor, then the paper links (OpenAI's own post + the github.com/openai/math
  repo) — the evidence is one click away and named in the first screen of text.
- Thumbnail [thumbnail]: giant orange OpenAI knot fused with the word "OPENAI" over a generated
  topographic landscape; headline "BREAKTHROUGH". The company name + logo occupy ~60% of the frame.

### 4c · "Gemini 4 Argon Is Not What I Expected" — LWxX6vvHfrc
- 249,344 views · 6:49 · 2026-10-19 · 3,836 likes [API]
- Thumbnail [thumbnail]: the Gemini swirl logo floating over a lush generated landscape, model
  name in huge type ("Gemini 4 ARGON"), and a small cartoon scientist scratching his head —
  the channel's only "presenter" is a mascot figure reacting to the subject.

**Channel takeaway:** at 5–9 minutes, faceless, with no face and no chapters, this channel
out-views every face-led channel in the sample by an order of magnitude. What it sells on the
thumbnail is exactly what Ctrl-Ahead can generate: **the subject's logo, one generated scene
that draws the claim's metaphor, and ≤ 4 words**. Duration discipline matters too — all three
hits are under 9 minutes.

---

## 5 · AI Explained — faceless deep analysis; the closest peer to Ctrl-Ahead

Channel pattern [chapters][page]: few, long chapters (4–7 across 24–38 min); a short
"Introduction" chapter (41–92s), then numbered Parts or claim-named sections; descriptions are
dense with source links — every section's evidence is linked in the description [page].

### 5a · "GPT 6 Astra, so good even OpenAI are worried" — Spuza-KwTJ4
- 857,606 views · 29:05 · 2026-09-04 · 10,725 likes · 1,346 comments [API] — the channel's top
  recent performer.
- Chapters (6) [chapters]: 0:00 Introduction (53s) → 0:53 vs Fable → 5:27 most impressive
  results → 13:06 bonus comparisons (plus trading) → 18:40 concerning trend → 21:24 Cot Control
  (final 7:41). Sections run 2:44–7:41.
- Description [page]: opens with a one-paragraph verdict-flavoured summary ("a day
  benchmark-makers got humbled, traders got excited, and AI safety researchers got unnerved"),
  then ~30 source links (lab post, safety paper, leaderboards, researcher posts) — the receipts
  live in the description, in full, so the narration never has to stop and cite itself.
- Thumbnail [thumbnail]: the starkest in the sample — "GPT-6" in black condensed type on white,
  two rules, nothing else. The model name alone is the visual.

### 5b · "OpenAI Security: Controlling Models is Now 'Hell'" — _rtp1XzaP6Q
- 297,304 views · 38:29 · 2026-10-01 · 4,695 likes [API]
- Chapters (7) [chapters]: 0:00 Introduction (1:32) → 1:32 "Wrong about Opus 5.5? Deciphering
  16th Century Text" → 5:01 Why the models keep breaking out → 11:40 What the models aren't
  telling us → 15:36 Gemini 4 and the race to release → 19:19 What happens when AI improves AI?
  → 28:31 Biology, consciousness, and what we still don't understand (final 9:58).
- Chapter titles are written as questions and confessions, not topics — each one is a small
  open loop. Note the self-correction chapter ("Wrong about Opus 5.5?") placed second: owning
  a miss early is a trust beat, the same function as MattVidPro's failure chapter.
- Thumbnail [thumbnail]: two cut-out photos of the named people (the lab leaders discussed)
  flanking the quoted claim: "OPENAI: CONTROLLING MODELS IS 'HELLISH'". The quote word does the
  hooking; the people are the subject, shown as themselves.

### 5c · "AI Labs Warn Race Makes Breach 'Inevitable'" — C4Sq3Rot8FU
- 155,538 views · 31:01 · 2026-10-12 · 3,029 likes [API]
- Chapters (4) [chapters]: 0:00 Introduction (0:41) → 0:41 Part 1: The Forthcoming Breach (8:02)
  → 8:43 Part 2: Why the Labs Keep Racing (6:58) → 15:41 Part 3: Why the Next 18 Months Are Hard
  to Predict (15:20 — half the video is the final part; the payoff section is the longest).
- Description [page] again opens with a one-paragraph synthesis naming the week's stories and
  his through-line, then links.
- Thumbnail [thumbnail]: the two lab leaders in profile, facing off across the headline
  "AI LAB BREACH 'INEVITABLE'" — versus staging with the subjects' own faces, quote as headline.

**Channel takeaway:** long sections survive because each is *one claim argued with evidence*,
and the evidence is visible (linked sources, quoted documents). The intro is under 90 seconds
even at 38 minutes total. The final part is allowed to be the longest — the payoff is the point.

---

## Cross-channel synthesis (what the 15 videos agree on)

1. **The subject is named in the first seconds and dominates the thumbnail.** In 15/15 samples
   the 0:00 chapter or title names the product/model/repo [chapters][API]; in 12/15 thumbnails
   the largest element is the subject's logo, name, artifact, or a stat about the subject
   [thumbnail]. Faces, where present, are reaction — never the subject.
2. **Section length scales with what the visual is doing.** Update format: ~45–60s sections
   (AI Advantage). Build/test format: 1.5–4 min sections where the artifact on screen is itself
   changing (MattVidPro, AI Andy). Analysis format: 3–10 min sections where one claim is argued
   (AI Explained). Nobody in the sample holds a *static* visual for a long section — long
   sections are always carried by a changing artifact or an unfolding argument.
3. **The verdict is a named, late beat — by job/product, never a single winner.** "My Final
   Picks" (14:36 of 17:26), "Astra, Sol or Luna? My verdict" (22:06 of 24:28), "Price & Verdict"
   (19:45 of 22:32), "Shader or Unreal? My verdict" (16:48 of 18:48) [chapters].
4. **The catch/failure is a named chapter, placed late-middle (~65–75%).** "Where autonomous
   development fell short" (16:42/24:28), "The mistake to avoid" (12:25/16:49, and it's the
   longest section), "Step 6: The catch" (9:39/13:34), "Wrong about Opus 5.5?" (1:32 — the
   early-trust variant) [chapters].
5. **Same test, same order, per contender.** MattVidPro's mirrored A/B lattice (2c) and the
   playbook's AI Frontier/Fireship findings agree: the comparison format's visual rhythm *is*
   the contender swap.
6. **Receipts live in the description, not the narration.** AI Explained links ~30 sources;
   MattVidPro and AI Andy link the exact repos/prompts/tools [page]. Provenance is one click
   away and never performed on screen — which is also Oliver's script-purity rule.
7. **Sponsors are labelled, bounded, and placed after the hook.** A mid-roll chapter (MattVidPro,
   5:53, 84s) or the first description line (Two Minute Papers) [chapters][page]. Never before
   the first content beat.
8. **Faceless is not the handicap.** The two faceless channels hold the sample's two biggest
   hits (857K, 580K) and its highest floor. What they spend instead of a face: logo-hero
   thumbnails, metaphor scenes, and claim-first titles.

## What could NOT be verified (do not quote downstream)

- **No transcripts were retrieved** for any of the 15 — spoken hooks, exact hook wording, and
  narration-to-visual alignment are UNVERIFIED except where a chapter title or description
  states the structure. (YouTube caption tracks need the video owner's auth via the Data API;
  no transcript tool was available in this environment.)
- **No frame-level cut counts exist** for these 15. Chapter spacing measures section length
  only. The finest verified visual-cadence evidence remains the playbook's: AI Frontier's
  captions changed per clause (~every 2–4s) with headline changes per claim [playbook], and
  two faceless guides' 3–5s visual-change rule [playbook, secondary guidance].
- **Transition types, subtitle styles, and music presence are UNVERIFIED** for all 15 — none
  are observable from page text, API data, or thumbnails. The choreography spec therefore takes
  its transition/subtitle/music rules from Oliver's own standing directions, not from these
  channels.
- **In-video logo timing** is verified only at chapter granularity (product named in the 0:00
  chapter and at section starts [chapters]). Second-level logo appearance timing is UNVERIFIED.
- One watch-page fetch (eVBJIUxv8N8) returned HTTP 429; that video's data is API-only.
- Subscriber counts are single-day API snapshots [API]; AI Andy's z-YT6Ef6jxc internal
  structure is UNVERIFIED (no chapters published).
