# Render manifest — 006, "The 5-Day Roadmap, Explained"

**Status:** Manifest v1 — written 2026-10-29. This is the approval artifact for 006. Source of truth for all narration is `script.md` in this folder (production script v1, VO text decided — no VO line is rewritten, reworded, or reordered by this manifest). Next step after Oliver's approval: VO + HyperFrames build. Nothing in this manifest authorizes publishing.
**Format:** Explainer, HyperFrames + GSAP, one generated hero image per tool, Helio VO at natural pace, single-line captions.

## What carries over (pipeline presentation model, from 005 and the Muse builds)

- One visual idea per beat; overlays pop onto the scene at sentence/comma beats — no slow zoom, no pan-for-its-own-sake, no image used twice anywhere in the film.
- Every tool segment runs the same four-beat chip rail: **WHAT IT IS → WHY YOU NEED IT → IF YOU SKIP IT** (red) → **HOW** (green), chips stamping in exactly as the narration hits each beat (timing system specified below).
- Generated images are illustrated metaphors built on the VO's own analogy (time machine, utility meter, motion-sensor light…). They are never styled, framed, or captioned as real screenshots, recordings, dashboards, or evidence. Anything that looks like a terminal or console on screen is a drawn/simulated panel, labelled simulated in the build notes.
- The decided close text is the final VO of the film. The Ctrl-Ahead branded outro is a separate, silent closing beat after it (s09 below) — it does not touch the close text.
- All durations in this manifest are **estimates**. The build re-syncs every beat to the real VO (Whisper word timestamps), exactly as on 005 and the Muse Comeback builds.

## Scene table

VO word counts are exact (counted from `script.md`). VO estimates use the measured natural Helio pace of ~171 wpm from Oliver's other builds — estimates only; the build re-syncs to the real read. Raw narration totals ≈ **7:05**; the script's format target is ~9:05 of content inside a 9:30 ceiling, with the difference carried by the scripted visual holds (day cards, chip stamps completing, montage cuts, segment breathers). Note for the build: Day 5's source window (50s) is tighter than its VO estimate (~56s), so on the real grid the close and outro will start later than 9:05 — runtime is VO-driven, per pipeline standard.

| Scene | Script target | Content | VO words | VO est. @171 wpm |
|---|---|---|---|---|
| s01_hook | 0:00–0:25 | Hook montage + four beat labels flash | 68 | ~24s |
| s02_intro | 0:25–0:45 | Five day cards, 38 HOURS counter, stack chips | 38 | ~13s |
| s03_day1_setup | 0:45–3:45 | DAY 1 — SETUP (7 hrs): Git, AWS Account, Docker, Cursor + Claude, Amplify, SAM | 369 | ~2:10 |
| s04_day2_ui | 3:45–5:15 | DAY 2 — UI (8 hrs): React, Vibe Coding, API Gateway | 180 | ~1:03 |
| s05_day3_backend | 5:15–6:45 | DAY 3 — BACKEND (8 hrs): Lambda, AI Backend Build, Optionals [LATER] | 162 | ~57s |
| s06_day4_data | 6:45–8:15 | DAY 4 — DATA (8 hrs): DynamoDB, Testing, Optionals [LATER] | 172 | ~1:00 |
| s07_day5_launch | 8:15–9:05 | DAY 5 — LAUNCH (7 hrs): Deploy, CloudWatch, Optionals [LATER] | 160 | ~56s |
| s08_close | 9:05–~9:30 | Decided close VO; five day cards return, stamped SHIPPED | 61 | ~21s |
| s09_outro | after close (~8s) | Ctrl-Ahead branded outro — no VO | 0 | — |
| **Total** | **~9:30 ceiling** | **21 VO segments in 9 scenes** | **1,210** | **~7:05 narration** |

## The four-beat chip system (applies to every tool segment)

- **Stamp triggers.** Chips stamp on the spoken beat markers, located at build time by faster-whisper word alignment against the script text: WHAT IT IS stamps on the words "What it is" (or the segment's fused what-clause, noted per segment), WHY YOU NEED IT on "Why", IF YOU SKIP IT on "Skip it", HOW on "How". Target: chip fully landed within ~0.1s after the marker word starts. Inside a beat, each comma expansion in the VO gets its own visual switch-up (a chip sub-line, a counter, a card flip) — never a held static frame through a list.
- **Chip contents** are condensed from the VO line itself (listed per segment below); chip text never adds claims the VO doesn't make.
- **History clause.** Each tool's opening history clause lands with the hero image as a name card (TOOL NAME) + year chip (YEAR). Where the VO gives no year, there is no year chip (noted per segment — never invent one).
- **Colors.** WHAT/WHY chips in the standard card treatment; SKIP chip red; HOW chip green. Small tick SFX on every chip stamp (see Music/SFX).
- **OPTIONALS treatment.** Same chips and rail, but the whole segment frame is desaturated/muted with a **LATER** frame badge, one notch quieter (bed dips slightly, no stinger into or out of an optionals segment). Where an optionals segment's "skip" beat is a *defer* instruction ("skip both for now"), it stamps as a LATER chip, not a red warning.

## Generated-asset style rule (every prompt below)

All image prompts share this suffix, applied at generation: *cinematic digital illustration, deep charcoal-navy background in the channel grade, neon cyan and neon pink accents with warm brass-gold highlights, soft rim light, high detail, 16:9, no text, no words, no logos, no watermarks, no real software screenshots — an illustrated metaphor, not a depiction of real software.* Prompts below give the subject; the builder appends the suffix. Generated video clips follow the same grade and the same rule: atmosphere/metaphor only.

---

## s01_hook — [script target 0:00–0:25] — 68 words, VO est. ~24s

**Visual plan.** Fast montage, quick cuts landing on the VO's commas — no single frame held. The montage is the film's only generated-video moment: 3 clips (below), intercut with 3 matching still plates used as cut/hold frames. On the VO list "what it is, why you need it, what breaks if you skip it, and how to actually do it," the four beat labels (WHAT IT IS / WHY / SKIP IT / HOW) flash in sequence, one per clause — this is the chip rail's first appearance, drawn type, no SFX tick yet (ticks start with Day 1). Montage resolves to a dark beat, then the intro.

**Generated video clips (hook only — the film's entire generated-video allowance, max 3):**
- VID-HOOK-1 (deploy): "A code terminal window in a dark studio deploying an application, lines of build output scrolling upward, status checks flipping green one by one, subtle energetic push-in, cinematic." (~3–4s)
- VID-HOOK-2 (app loading): "A modern web app interface assembling itself piece by piece on a floating screen in a dark studio, then loading instantly, elements snapping into place, cinematic." (~3–4s)
- VID-HOOK-3 (dashboards): "A dark wall of analytics dashboards lighting up one screen at a time, gauges sweeping and charts drawing themselves, cinematic." (~3–4s)

**Generated plates (stills, cut frames between clips):**
- IMG-HOOK-1: "A developer's desk in a dark room at night, one monitor mid-deployment with green status lights, coffee beside the keyboard, cinematic still." 
- IMG-HOOK-2: "A glowing five-stop route map unfolding across a dark surface, five milestone nodes connected by a brass light trail, cinematic still."
- IMG-HOOK-3: "A launch control wall of status panels in a dark room, most lights green, one still amber, cinematic still."

## s02_intro — [script target 0:25–0:45] — 38 words, VO est. ~13s

**Visual plan.** IMG-INTRO as the base plate; the five day cards pop in one per VO beat — DAY 1 SETUP / DAY 2 UI / DAY 3 BACKEND / DAY 4 DATA / DAY 5 LAUNCH — drawn cards `pinCard`-style on "Day one…, day two…" through "day five you go live." The "38 HOURS" counter chip rolls up (odometer pattern) on "about 38 hours." Stack chips REACT · PYTHON · PAY-PER-REQUEST stamp across the bottom on the stack clause. Ends on "Let's go" with the DAY 1 card swelling forward into s03's day card.

- IMG-INTRO: "A dark planning wall with five empty glowing card slots arranged in a row like a film strip, a faint brass route line running beneath them, a subtle clock motif in the corner, cinematic."

## s03_day1_setup — [script target 0:45–3:45] — 369 words, VO est. ~2:10

**Chapter frame.** Full-screen day card first: **DAY 1 — SETUP — 7 HRS** (stinger + thump on entry; this card template repeats for every day chapter). Tool segments hang off the card, which shrinks to a corner tab (DAY 1 · SETUP) for the chapter's duration.

### s03.1 Git — 69 words, VO est. ~24s
- IMG-GIT: "A glowing trail of circular checkpoints stretching back along a winding path of code into darkness, like a time machine's light trail, each checkpoint a bright node, the nearest one in sharp focus."
- Name card GIT + year chip **2005**. Drawn/animated: checkpoint nodes light one by one along the hero image's trail during WHAT.
- Chips — WHAT: "a time machine for your code — every working version saved as a checkpoint" / WHY: "production code changes daily, and you need undo" / SKIP: "one bad edit costs you a day of guessing what changed" / HOW: "`git init` · commit every time something works · push to GitHub". On HOW, a drawn simulated mini-terminal types the three commands (drawn panel, not a screenshot).

### s03.2 AWS Account — 59 words, VO est. ~21s
- IMG-AWS-ACCOUNT: "A round brass utility meter mounted on the side of a soft glowing cloud, its dial resting at near-zero, a thin cable running down out of frame."
- Name card AWS ACCOUNT + year chip **2006** (the VO's history clause: the cloud's launch). Chips — WHAT: "where everything else in this video lives, metered like a utility" (meter dial twitches on "metered") / WHY: "an app with no traffic costs almost nothing" / SKIP: "you're building a website that only you can see" (hero dims to a single dark window on this beat) / HOW: "sign up · stay in the free tier · done in fifteen minutes" + **FREE TIER** chip stamped beside HOW.

### s03.3 Docker — 62 words, VO est. ~22s
- IMG-DOCKER: "A sealed glowing shipping box containing a complete miniature web app — tiny server, tiny database, tiny gears — a laptop on the left and a live server rack on the right, the box identical between them."
- Name card DOCKER + year chip **2013**. Chips — WHAT: "a box that packs your app plus everything it needs to run" / WHY: "the box behaves identically on your laptop and on the live site" (box pulses on both sides of the hero in turn) / SKIP: "'works on my machine' bug on launch day" + a drawn **WORKS ON MY MACHINE** bug card stamped with a red X exactly on the SKIP chip / HOW: "one Dockerfile · `docker build` — the 30-minute version".

### s03.4 Cursor + Claude — 64 words, VO est. ~23s
- IMG-CURSOR: "A code editor glowing in a dark room with a translucent ghost typist seated at the keyboard, lines of code streaming from its fingertips onto the screen."
- Name card CURSOR + CLAUDE + year chip **2023** + a paired-model chip **CLAUDE SONNET 4**. The VO fuses history and WHAT ("an editor with AI built in — paired with Claude Sonnet 4, it's a junior developer who types instantly"), so the WHAT chip stamps on "it's a junior developer who types instantly." Chips — WHAT: "an editor with AI built in — a junior developer who types instantly" / WHY: "the five-day timeline only exists because the AI writes the boilerplate while you review" / SKIP: "this is a five-week project" + a drawn calendar card flipping **5 DAYS → 5 WEEKS** on the chip / HOW: "install it · open your project · describe what you want in plain English".

### s03.5 AWS Amplify — 54 words, VO est. ~19s
- IMG-AMPLIFY: "A vintage printing press stamping fresh copies of a glowing website page, each copy coming off the press with a brass padlock seal in the corner, copies stacking neatly."
- Name card AWS AMPLIFY + year chip **2017**. Chips — WHAT: "a publisher — every push republishes your live site, certificates included" (a fresh copy stamps off the press per comma: push → republish → certificates) / WHY: "launch-day plumbing handled for free" / SKIP: "manually uploading files and babysitting expired certificates" (a drawn certificate card flickers EXPIRED on "expired") / HOW: "connect your GitHub repo once — never think about it again".

### s03.6 AWS SAM — 61 words, VO est. ~21s — ⚠ YEAR CHIP BLOCKED (see OPEN ITEMS, Flag 1)
- IMG-SAM: "An architect's blueprint unrolling across a dark table, its white line drawings rising off the paper into a three-dimensional backend diagram of connected boxes and routes."
- Name card AWS SAM. **Year chip: BLOCKED** — do not draw or stamp any year for SAM until Flag 1 is resolved (the VO's history clause "And SAM, from 2018" is itself flagged; see OPEN ITEMS). Chips — WHAT: "a blueprint — your entire backend described in one text file, built by a single command" / WHY: "reproducible, undoable infrastructure instead of clicking through twenty consoles" / SKIP: "your setup exists in no one's head, exactly once" / HOW: "write a `template.yaml` · deploy with the SAM CLI — three hours today, saves your whole week".


## s04_day2_ui — [script target 3:45–5:15] — 180 words, VO est. ~1:03

**Chapter frame.** Day card: **DAY 2 — UI — 8 HRS** (stinger on entry), then corner tab DAY 2 · UI.

### s04.1 React — 65 words, VO est. ~23s
- IMG-REACT: "Glowing interface building bricks — a button, a calendar, a card, a toggle — snapping together magnetically in mid-air to form a complete web page, dark background."
- Name card REACT + year chip **2013**. Chips — WHAT: "Lego for interfaces — build a button or calendar once, snap it in anywhere" (bricks in the hero snap on each comma) / WHY: "it's the industry standard — tutorials and help are everywhere" / SKIP: "you're hand-crafting every page from scratch" / HOW: "scaffold the project · build each page as bricks · half an hour of setup".

### s04.2 Vibe Coding — 56 words, VO est. ~20s
- IMG-VIBE: "A beautiful finished storefront facade glowing warmly at street level — and behind it, visible from the side, empty wooden scaffolding and nothing else."
- Name card VIBE CODING, **no year chip** (the VO gives none). This segment's rail is activity-led: an opening card **7 HOURS — BUILD THE WHOLE INTERFACE BY PROMPTING** stamps on the first clause, and the rule card **FAKE DATA · NO BACKEND** stamps as the segment's WHAT-equivalent on "with one rule: fake data, no backend." Chips — WHY: "you make the site look and feel finished before the plumbing exists" / SKIP: "you'll spend the day debugging connections instead of building" (stamps on "Skip this discipline…") / HOW: "prompt one component at a time · click through it · refine".

### s04.3 API Gateway — 59 words, VO est. ~21s
- IMG-GATEWAY: "A grand glowing front door set in a dark wall, a checker figure at the threshold examining each visitor in an orderly queue before waving them through."
- Name card API GATEWAY + year chip **2015**. Chips — WHAT: "the front door — it checks every incoming request before anything touches your code" / WHY: "security, throttling, and routing in one place" (three mini-chips pop on the three nouns) / SKIP: "browsers are poking your backend directly, unlocked" — on this beat the hero's door swings open unlocked, queue scattering / HOW: "create a REST API · one route per action — Day 3 has something to plug into" (a drawn route line reaches forward toward the DAY 3 tab).

## s05_day3_backend — [script target 5:15–6:45] — 162 words, VO est. ~57s

**Chapter frame.** Day card: **DAY 3 — BACKEND — 8 HRS** (stinger on entry), then corner tab DAY 3 · BACKEND.

### s05.1 Lambda — 80 words, VO est. ~28s
- IMG-LAMBDA: "A motion-sensor porch light above a dark path snapping on as a lone walker approaches, a small brass meter beside it ticking only while the light is on."
- Name card AWS LAMBDA + year chip **2014**. Chips — WHAT: "a motion-sensor light — your code turns on when a request arrives, off when it's done; you pay per flip" (hero light snaps on/off with the clauses) / WHY: "no traffic means near-zero cost, and 5,000 users scale automatically" + a **5,000 USERS** scale counter rolling up (odometer pattern) on the number / SKIP: "you're renting a server that runs 24/7 for a site nobody's found yet" (a drawn always-on bulb burns in an empty room on this beat) / HOW: "write a Python handler · connect it to the Gateway route" (drawn line plugs the handler into s04.3's door).

### s05.2 AI Backend Build — 35 words, VO est. ~12s
- IMG-AIBUILD: "A row of paper service tickets on a dark counter, three of them stamping themselves one by one — a check stub, a price stub, a mail stub — under a warm work lamp."
- Name card AI BACKEND BUILD, no year chip. **This segment does not use the four-chip rail** (the VO has no four-beat structure — it is a build-progress segment, per the script's decided visual): endpoint tickets stamp in one per clause — **CREATE / READ / CANCEL** lighting green by the end — with scope chips **VALIDATION · PRICING RULES · EMAILS** popping on their nouns, drawn TODO sticky notes pinned at the caching spot on "where caching belongs later," and a single HOW chip on "How: small scope." Segment ends with all three tickets green: "by tonight, creating, reading, and canceling works."

### s05.3 Optionals — FastAPI + SQS [LATER] — 47 words, VO est. ~17s
- IMG-FASTSQS: "A brass ticket dispenser at the front of an orderly queue, a flood of glowing request slips held back behind glass behind them, everything calm at the window."
- **Muted LATER frame treatment** (desaturated, LATER badge, quieter). Two mini name cards: **FASTAPI 2019** and **SQS**. Compressed rail: FASTAPI card "when one request involves many slow steps at once" stamps on its clause; SQS WHAT chip "the ticket dispenser — it queues a flood of requests so none bounce" stamps on "it queues a flood of requests"; a shared **LATER** chip — "Skip both for now; add them when traffic demands it" — stamps on "Skip both for now" (a defer chip, not the red SKIP treatment). Flag note: the SQS "first service" wording is one half of Flag 2 — see OPEN ITEMS; the BLOCKED mark in this film lands on the S3 line in s06.3, per the recommended fix.

## s06_day4_data — [script target 6:45–8:15] — 172 words, VO est. ~1:00

**Chapter frame.** Day card: **DAY 4 — DATA — 8 HRS** (stinger on entry), then corner tab DAY 4 · DATA.

### s06.1 DynamoDB — 83 words, VO est. ~29s
- IMG-DYNAMODB: "A tall filing cabinet in a dark archive whose drawers fly open in sequence as glowing lookup codes flash above them, paper answers snapping out instantly into a tray."
- Name card DYNAMODB + year chip **2012**. Chips — WHAT: "a filing cabinet with lookup codes — instant answers, no rigid schema" / WHY: "pay per request · millisecond speed · change your data shape weekly" (three mini-chips, one per clause) / SKIP: "either paying for an idle database server, or freezing your app's structure early" (the hero cabinet frosts over on "freezing") / HOW: "partition by what you'll ask for · sort by the piece ID · design the lookups first, always".

### s06.2 Testing — 44 words, VO est. ~15s
- IMG-TESTING: "Two halves of a machine being bolted together on a dark workbench, a test light running along the seam, a small bug sealed inside a glass jar on the bench beside a calendar page."
- Name card TESTING, no year chip. Rail mapping (the VO is activity-led): an opening activity card **5 HRS WIRING · 2 HRS TESTING** stamps on the first clause and serves as the WHAT position; WHY chip "bugs found on day four cost minutes; found on day five, they cost your launch" stamps on "Why:" — with the script's split visual: the jarred bug labelled by a drawn DAY 4 tag vs the same bug smashing a launch banner under a DAY 5 tag; SKIP chip "your users are your QA team" on "Skip it…". No separate HOW chip — the wiring/testing hours in the activity card are the how (noted here so the build doesn't invent one).

### s06.3 Optionals — RDS + S3 [LATER] — 45 words, VO est. ~16s — ⚠ S3 LINE BLOCKED (see OPEN ITEMS, Flag 2)
- IMG-RDSS3: "An endless garage interior stretching into darkness, labeled shelves of files, boxes, and film reels receding to a vanishing point, one strict grid-patterned spreadsheet cabinet standing near the door."
- **Muted LATER frame treatment.** Two mini name cards: **RDS 2009** and **S3**. RDS card: "the strict spreadsheet database — for the day payments get serious." S3 card: "an infinite garage for files and video." **The S3 card's history wording is BLOCKED**: the VO clause "Amazon's very first service" is flagged (Flag 2) — do not draw any "first service" chip, caption emphasis, or card text from that clause until the flag is resolved. Trigger chip "you'll need reports, or you'll need file storage" stamps on "How you'll know:"; LATER chip "Until then, skip" closes the segment.


## s07_day5_launch — [script target 8:15–9:05] — 160 words, VO est. ~56s

**Chapter frame.** Day card: **DAY 5 — LAUNCH — 7 HRS** (stinger on entry), then corner tab DAY 5 · LAUNCH. (Build note from the scene table: this chapter's VO estimate exceeds its source window — let the grid breathe; do not rush the read.)

### s07.1 Deploy — 49 words, VO est. ~17s
- IMG-DEPLOY: "A launch wall of round status lights in a dark control room flipping from amber to green one by one, two large brass buttons below the wall."
- Name card DEPLOY, no year chip. Payoff segment, rail replaced by two action cards keyed to the VO's two halves: **PUSH — FRONTEND** ("git push — Amplify republishes automatically, live HTTPS site") stamps on "Frontend:", with a callback thread drawn back to the DAY 1 tab; **DEPLOY — BACKEND** ("one SAM command ships every function, route, and database permission together — versioned and undoable") stamps on "Backend:", thread back to DAY 1 and DAY 4 tabs on "This is the payoff of Days 1 and 4." HOW chip: "connect GitHub to Amplify · run the deploy · watch it all go green" — the hero's remaining lights flip green across the chip.

### s07.2 CloudWatch — 69 words, VO est. ~24s
- IMG-CLOUDWATCH: "A heart-monitor trace glowing across a dark wall of small security-camera feeds, an alarm beacon mounted above them, the room otherwise still and night-quiet."
- Name card CLOUDWATCH + year chip **2009**. Chips — WHAT: "a heart monitor plus security cameras for your app — every request leaves a log, alarms email you when errors spike" / WHY: "when it breaks at 2 AM, this is how you know before your users tell you" — on "2 AM" the scene darkens and the hero's alarm light pulses *first*, before any customer figure appears / SKIP: "failures happen silently while angry customers wait" / HOW: "turn on logging · set one alarm on errors — that's 90% of the value".

### s07.3 Optionals — Grafana + X-Ray [LATER] — 42 words, VO est. ~15s
- IMG-GRAFXRAY: "A gauge-filled dashboard glowing in a dark room beside a parcel moving along a tracked route map, one slow segment of the route glowing amber."
- **Muted LATER frame treatment.** Two mini name cards: **GRAFANA 2014** ("a side project that became the standard dashboard for gauges and graphs") and **X-RAY** ("package-tracking for every request — shows which step is slow"). Closing chip **DAY 1 → DAY 1000** stamps on the final clause: "Nice on day one, essential by day one thousand."

## s08_close — [script target 9:05–~9:30] — 61 words, VO est. ~21s

**Visual plan.** IMG-CLOSE as a soft base plate under the returning cards. The five day cards (same drawn cards as s02, now complete) return in a row on "setup, frontend, backend, memory, launch," each stamped **SHIPPED** in turn (badge pulse per stamp) across "Thirty-eight hours, near-zero cost until you have users." A brass roadmap line draws itself complete underneath the row (string-draw pattern) on "every tool here does one job you can name." Recap chips land on the final imperatives: **FOLLOW THE FIVE DAYS IN ORDER** · **SKIP NOTHING ON DAY 1**. The subscribe/comment ask in the VO gets no on-screen text beyond the standard end-frame elements in s09 — the decided close text stands as the film's final VO, unchanged and unaccompanied by any extra spoken or written line.

- IMG-CLOSE: "The completed five-stop route seen from directly above, the full brass trail lit end to end, all five milestone nodes glowing steadily, dark map beneath, cinematic."

## s09_outro — branded closing beat, no VO (~8s)

A separate closing beat *after* the close VO ends — a hard scene change, not an overlay on s08. Drawn/animated only (no generated media): the Ctrl-Ahead **brass arrow** draws itself in (SVG stroke animation, the channel mark), holds, then the catchphrase sets beneath it: **"We don't chase the future. We check it."** — followed by the tagline **"Ctrl-Ahead — confirmed, not just claimed."** and a SUBSCRIBE pill. The music bed resolves and ends under this beat (no stinger — stingers belong to day changes only). Total outro ~8s; it is outside the film's 9:30 content ceiling.

---

## Implementation notes

**Engine & project shape.** HyperFrames (HeyGen) + GSAP, following the Muse Comeback project's architecture at `~/workspace/muse-comeback-v2/muse-comeback` — reference its patterns, do not copy or modify its files. Root composition at 3840×2160 design space, rendered at 1920×1080/30fps: `index.html` mounts **one sub-composition per scene** (s01–s09), with the five day chapters as sub-compositions whose tool segments are timed clips inside the chapter timeline — the same root/sub-composition split as the Comeback film's s1–s9. Every GSAP timeline is `{paused: true}` and registered on `window.__timelines["<id>"]` (a timeline that isn't registered renders as a still frame); animation is deterministic and seek-driven — transforms/opacity only, `fromTo()` preferred, no `Date.now()`/`Math.random()`/CSS transitions. TMPDIR for all HyperFrames/FFmpeg work points at a workspace cache dir, never `/tmp`. Pinned CLI from the Comeback project (0.8.210); nothing remote at render time — fonts and GSAP vendored locally, generated assets committed into the project's `assets/` before rendering.

**Helpers reused by pattern** (from the Comeback `js/shared.js`): `makeSceneTimeline(id, duration)` for every scene/segment timeline; `pinCard(el, tl, at)` for day cards, name cards, and chip stamps (the chip rail is pinCard with a stamp scale-punch); `redString(...)` redrawn in brass as the roadmap-line draw (s02 intro line, s07 callback threads, s08 completion line); `odometer(...)` for the 38 HOURS counter and Lambda's 5,000 USERS counter; `pulseBadge(...)` for the SHIPPED stamps in s08; `cameraPush` for the 0.4s dolly-in/out scene bookends. Theme: build a 006 theme on the Comeback `css/theme.css` structure (glass panel / evidence-card classes, neon + warm-brass palette), with the chip rail as a new component class (`.beat-chip` with `.skip` red and `.how` green variants, and a `.later` desaturated variant for optionals frames).

**Build order inside the film.** VO first (Helio, natural pace, verbatim from `script.md` — subject to the OPEN ITEMS holds below), then Whisper alignment, then scene re-sync: root `data-duration` and every scene/segment start are set from the *real* VO durations (scene = VO + tail padding, per the Comeback Phase 4 pattern), replacing every estimate in this manifest. Generated assets are produced from the prompts above into `assets/gen/` with a manifest log (file, prompt, scene) before scene assembly. Project check must pass at 0 errors before rendering; scenes render per-scene via temporary roots and are concatenated, per the established pattern.

**Captions plan.** Single clean line, pipeline standard: caption text is the script's VO text **verbatim** (never Whisper's transcription), timing from faster-whisper word timestamps aligned to the script words (timing only). Phrases re-split to ≤8 words so every caption is genuinely one line. Geometry follows the Comeback caption system: `.caption` style (64px, weight 600, white on a 60%-black plate) inside the `.caption-band` anchored at 68% of frame height, with per-scene band adjustments only where the checker flags a collision with cards/chips (the Comeback Phase 4 lesson: bottom-anchor the band where layouts are dense). The caption for the flagged S3 clause in s06.3 is held with that clause — see OPEN ITEMS.

**Music / SFX plan.** One understated synthesized electropop bed for the whole film, built in-project exactly as on the Muse Comeback build (synthesized, nothing downloaded or licensed), sidechain-ducked under the VO (~6 dB under speech), resolving under the outro. **Stingers: day changes only** — one stinger + thump on each of the five day cards (s03–s07 entries), and nowhere else: not on optionals, not on the outro. **Chip-stamp ticks:** the short synthesized tick on every chip stamp (the Comeback `tick.wav` pattern), a card-pin sound on name cards and day cards, a soft snap on the roadmap line completing in s08. Optionals segments sit one notch quieter (bed dipped ~2 dB inside the muted frame). SFX are synthesized at build; every asset's provenance is logged in the build report.

**Honesty rules carried into the build.** Generated images/clips are metaphors and are never presented as real product UI, real terminals, or real dashboards; the Git HOW mini-terminal and all consoles are drawn simulated panels. No benchmark, price, date, or capability appears on screen that the VO doesn't state. No provenance/meta labels are burned into the video (provenance lives in this manifest and the build report only).

## OPEN ITEMS — fact flags (unresolved; carried verbatim from `script.md`)

The two flags below are reproduced **verbatim** from the production script's FACT FLAGS section. This manifest does not resolve them, and no flagged wording is altered anywhere in the visual plan above.

> 1. **AWS SAM year.** The decided text says "SAM, from 2018." SAM was actually first released in **November 2016** (announced at re:Invent 2016 — verified by web search 2026-10-29). Recommended fix: "from 2016."
>
> 2. **Two "first service" claims.** The Day 3 optionals call SQS "AWS's first service" and the Day 4 optionals call S3 "Amazon's very first service." Both can't be first — SQS (2004) predates S3 (2006). Recommended fix: S3 line becomes "one of Amazon's first services."

**BLOCKED marks (build holds until Oliver settles the flags or the recommended fixes are adopted by default at VO time, per the script's production notes):**
- **s03.6 (SAM): the year chip is BLOCKED.** No year is drawn, stamped, or captioned for SAM. The VO history clause "And SAM, from 2018" is a flagged line and is not recorded until Flag 1 is settled.
- **s06.3 (RDS + S3): the S3 "very first service" line is BLOCKED.** No chip, card text, or caption emphasis is derived from the clause "Amazon's very first service," and that VO clause is not recorded until Flag 2 is settled.
- All other scenes and segments are unblocked and may proceed through VO and build on approval of this manifest. Per the script's production notes, VO does not record the flagged lines until they're settled — Oliver's word, or the recommended factual fix by default at manifest stage.

---

## BUILD UPDATE — 2026-10-30 (render complete)

Oliver approved this manifest in the side chat on 2026-10-30 ("do the video renderings right now"). Both OPEN ITEMS were resolved by applying the recommended fixes by default, exactly as this manifest's production notes allowed:
- **Flag 1 (SAM):** VO recorded "from **2016**"; SAM year chip drawn as **2016**.
- **Flag 2 (S3):** VO recorded "**one of Amazon's first services**"; S3 chip uses the same wording. The BLOCKED marks on s03.6 and s06.3 are lifted by these fixes.

Final film: `006-five-day-roadmap-final.mp4` in this folder — 496.13s, 1920×1080, h264/aac, verified with ffprobe, frame checks, and a no-dead-air silence scan. Full details, including the hook-montage fallback (still plates with quick cuts instead of generated video clips, because Vast.ai/LTX-2.3 was not yet rented and no spending was authorized), are in `BUILD_NOTES.md` in this folder. Not published.
