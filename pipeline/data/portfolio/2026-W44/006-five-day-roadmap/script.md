# 006 — The 5-Day Roadmap, Explained

**Status:** Production script v1 — written 2026-10-29. Next pipeline step: render manifest (approval artifact), then VO + build.
**Source:** Oliver's Perplexity thread https://www.perplexity.ai/search/afe8b753-8919-4ac4-916a-cedf58fe39cc — the thread's LAST response is the decided text; VO below is that text verbatim (Perplexity citation markers stripped, stage directions converted to visual beats). Original Short being explained: https://youtube.com/shorts/zxfTArjbyto
**Format:** Explainer, ~9:05 of content inside a 9:30 ceiling (~25s buffer for natural pauses). Ctrl-Ahead OS pipeline. Build: HyperFrames + GSAP, generated image per tool, Helio VO at natural pace. Segment timecodes are the source's targets; production re-syncs every beat to the real VO, same as 005 and the Muse builds.
**Structure (decided):** every tool gets the same four beats — WHAT IT IS / WHY YOU NEED IT / WHAT BREAKS IF YOU SKIP IT / HOW TO DO IT — plus a one-clause history so viewers learn each tool's story.

## FACT FLAGS (settle before VO — see production notes)

1. **AWS SAM year.** The decided text says "SAM, from 2018." SAM was actually first released in **November 2016** (announced at re:Invent 2016 — verified by web search 2026-10-29). Recommended fix: "from 2016."
2. **Two "first service" claims.** The Day 3 optionals call SQS "AWS's first service" and the Day 4 optionals call S3 "Amazon's very first service." Both can't be first — SQS (2004) predates S3 (2006). Recommended fix: S3 line becomes "one of Amazon's first services."

## VISUAL SYSTEM (applies to every tool segment)

- One generated hero image per tool, built on the VO's own analogy (time machine, utility meter, motion-sensor light, ticket dispenser, filing cabinet, heart monitor…). Image pops in with the tool's name card + year chip; no slow zoom, no image used twice.
- The four beats stamp in as labeled chips exactly as the narration hits them: **WHAT IT IS → WHY YOU NEED IT → IF YOU SKIP IT** (red) → **HOW** (green). Visual switch-up on every beat change and on comma expansions inside a beat.
- Day chapters get a full-screen day card (DAY N — name — hours) that the tool segments hang off.
- OPTIONALS segments get a muted "LATER" frame treatment — same chips, desaturated, one notch quieter.
- Captions: single clean line, pipeline standard. Music: understated synth bed under VO, stingers on day changes only.

---

## [0:00 – HOOK]

**VO:** "There's a roadmap going around claiming you can build a production-ready full-stack web app in five days, almost free. It's real — and in the next nine and a half minutes I'm going to explain every tool in it: what it is, why you need it, what breaks if you skip it, and how to actually do it. If you can follow a recipe, you can follow this."

**VISUAL:** Fast montage — terminal deploying, app loading, dashboards lighting up (generated clips/images, quick cuts on the commas). The four beat labels (WHAT IT IS / WHY / SKIP IT / HOW) flash in sequence on "what it is, why you need it, what breaks if you skip it, and how to actually do it."

## [0:25 – INTRO]

**VO:** "Five days, about 38 hours, React frontend, Python backend, pay-per-request everything. Day one sets up your tools, day two builds what users see, day three the logic, day four the memory, day five you go live. Let's go."

**VISUAL:** Five day cards pop in one per beat (SETUP / UI / BACKEND / DATA / LAUNCH), "38 HOURS" counter chip, stack chips: REACT · PYTHON · PAY-PER-REQUEST.

---

## [0:45 – DAY 1: SETUP (7 hrs)]

### GIT

**VO:** "Git, created in 2005 when Linus Torvalds built a version-control system in about ten days. What it is: a time machine for your code — every working version saved as a checkpoint. Why you need it: production code changes daily, and you need undo. Skip it, and one bad edit costs you a day of guessing what changed. How: `git init`, commit every time something works, push to GitHub."

**VISUAL:** Hero image — a code timeline with glowing checkpoints stretching back like a time machine's trail. Chips stamp in per beat; on HOW, a mini terminal types the three commands.

### AWS ACCOUNT

**VO:** "Your AWS account. Amazon's cloud launched in 2006 with one storage service. What it is: where everything else in this video lives, metered like a utility. Why: an app with no traffic costs almost nothing. Skip it and you're building a website that only you can see. How: sign up, stay in the free tier, done in fifteen minutes."

**VISUAL:** Hero image — a utility meter on a cloud, dial at near-zero. "FREE TIER" chip on HOW.

### DOCKER

**VO:** "Docker, open-sourced in 2013 by a tiny startup called dotCloud. What it is: a box that packs your app plus everything it needs to run. Why: the box behaves identically on your laptop and on the live site. Skip it and you'll meet the 'works on my machine' bug on launch day. How: one Dockerfile, `docker build` — that's the 30-minute version."

**VISUAL:** Hero image — a sealed shipping box containing a whole miniature app, laptop on one side, live server on the other, box identical in both. "WORKS ON MY MACHINE" bug card stamped with a red X on the SKIP beat.

### CURSOR + CLAUDE

**VO:** "Cursor, released in 2023 by four MIT students, an editor with AI built in — paired with Claude Sonnet 4, it's a junior developer who types instantly. Why: the five-day timeline only exists because the AI writes the boilerplate while you review. Skip it and this is a five-week project. How: install it, open your project, and describe what you want in plain English."

**VISUAL:** Hero image — an editor with a ghost typist at the keyboard, code streaming. Calendar flips 5 DAYS → 5 WEEKS on the SKIP beat.

### AWS AMPLIFY

**VO:** "Amplify, born in 2017. What it is: a publisher — every time you push code, it automatically republishes your live site, with security certificates included. Why: launch-day plumbing handled for free. Skip it and you're manually uploading files and babysitting expired certificates. How: connect your GitHub repo once, and never think about it again."

**VISUAL:** Hero image — a printing press stamping fresh copies of a website, a padlock/certificate seal on each copy.

### AWS SAM

**VO:** "And SAM, from 2018. What it is: a blueprint — your entire backend described in one text file, built by a single command. Why: reproducible, undoable infrastructure instead of clicking through twenty consoles. Skip it and your setup exists in no one's head, exactly once. How: write a `template.yaml`, deploy with the SAM CLI. Three hours today, saves your whole week."

**VISUAL:** Hero image — an architect's blueprint unrolling into a full backend diagram. **[FLAG 1: year — recommended "from 2016."]**

---

## [3:45 – DAY 2: UI (8 hrs)]

### REACT

**VO:** "Day two. React, built at Facebook by Jordan Walke, released in 2013. What it is: Lego for interfaces — build a button or calendar once, snap it in anywhere. Why: it's the industry standard, so tutorials and help are everywhere. Skip it and you're hand-crafting every page from scratch. How: scaffold the project, build each page as bricks, done in half an hour of setup."

**VISUAL:** Hero image — interface bricks (button, calendar, card) snapping together into a page.

### VIBE CODING

**VO:** "Then seven hours building the whole interface by prompting the AI — with one rule: fake data, no backend. Why: you make the site look and feel finished before the plumbing exists. Skip this discipline and you'll spend the day debugging connections instead of building. How: prompt one component at a time, click through it, refine."

**VISUAL:** Hero image — a finished-looking storefront facade with scaffolding behind it (facade = UI, nothing behind yet). "FAKE DATA · NO BACKEND" rule card.

### API GATEWAY

**VO:** "Last half hour: API Gateway, launched 2015. What it is: the front door — it checks every incoming request before anything touches your code. Why: security, throttling, and routing in one place. Skip it and browsers are poking your backend directly, unlocked. How: create a REST API, one route per action, and Day 3 has something to plug into."

**VISUAL:** Hero image — a grand front door with a checker at the threshold; requests queue as visitors. Door shown unlocked and swinging on the SKIP beat.

---

## [5:15 – DAY 3: BACKEND (8 hrs)]

### LAMBDA

**VO:** "Day three, the logic — and the star: AWS Lambda, announced in 2014. What it is: a motion-sensor light. Your code turns on when a request arrives, off when it's done — you pay per flip, not for an always-on bulb. Why: no traffic means near-zero cost, and 5,000 users scale automatically. Skip it and you're renting a server that runs 24/7 for a site nobody's found yet. How: write a Python handler and connect it to the Gateway route."

**VISUAL:** Hero image — a motion-sensor light snapping on as a request walks up, off as it leaves; a meter that only ticks on flips. "5,000 USERS" scale counter on WHY.

### AI BACKEND BUILD

**VO:** "Six hours of AI-assisted development: validation, pricing rules, emails — prompted into existence one endpoint at a time, with TODO comments where caching belongs later. How: small scope. By tonight, creating, reading, and canceling works."

**VISUAL:** Hero image — endpoints appearing one by one as stamped tickets (CREATE / READ / CANCEL lighting green by the end). TODO sticky notes on the caching spot.

### OPTIONALS — FASTAPI + SQS [LATER]

**VO:** "Two upgrades for later: FastAPI, from 2019, when one request involves many slow steps at once. And SQS — the ticket dispenser: it was AWS's *first* service — it queues a flood of requests so none bounce. Skip both for now; add them when traffic demands it."

**VISUAL:** Muted LATER frame. Hero image — a ticket dispenser feeding an orderly queue while a flood waits behind glass.

---

## [6:45 – DAY 4: DATA (8 hrs)]

### DYNAMODB

**VO:** "Day four, your app gets a memory: DynamoDB, released in 2012, grown from the database Amazon built for its own shopping cart. What it is: a filing cabinet with lookup codes — instant answers, no rigid schema. Why: pay per request, millisecond speed, change your data shape weekly. Skip it and you're either paying for an idle database server or freezing your app's structure early. How: partition by what you'll ask for, sort by the piece ID — design the lookups first, always."

**VISUAL:** Hero image — a filing cabinet whose drawers fly open by lookup code, answers snapping out instantly.

### TESTING

**VO:** "Five hours wiring real reads and writes end to end, two hours testing both halves separately with logging on. Why: bugs found on day four cost minutes; found on day five, they cost your launch. Skip it and your users are your QA team."

**VISUAL:** Hero image — two halves of a machine being bolted together with a test light running along the seam; a bug caught in a jar on DAY 4 vs the same bug smashing a launch banner on DAY 5.

### OPTIONALS — RDS + S3 [LATER]

**VO:** "Later, not now: RDS, from 2009 — the strict spreadsheet database, for the day payments get serious. And S3, Amazon's very first service — an infinite garage for files and video. How you'll know: you'll need reports, or you'll need file storage. Until then, skip."

**VISUAL:** Muted LATER frame. Hero image — an endless garage with labeled shelves of files and film reels. **[FLAG 2: "very first service" — SQS (Day 3) holds the first-service claim; recommended "one of Amazon's first services."]**

---

## [8:15 – DAY 5: LAUNCH (7 hrs)]

### DEPLOY

**VO:** "Day five. Frontend: `git push` — Amplify republishes automatically, live HTTPS site. Backend: one SAM command ships every function, route, and database permission together, versioned and undoable. This is the payoff of Days 1 and 4. How: connect GitHub to Amplify, run the deploy, watch it all go green."

**VISUAL:** Hero image — a launch wall of status lights flipping green one by one; two buttons: PUSH (frontend) and DEPLOY (backend).

### CLOUDWATCH

**VO:** "Then CloudWatch, from 2009. What it is: a heart monitor plus security cameras for your app — every request leaves a log, alarms email you when errors spike. Why: when it breaks at 2 AM, this is how you know before your users tell you. Skip it and failures happen silently while angry customers wait. How: turn on logging, set one alarm on errors. That's 90% of the value."

**VISUAL:** Hero image — a heart-monitor trace over a wall of security-camera feeds; at "2 AM" the room darkens and the alarm light pulses first, before any customer appears.

### OPTIONALS — GRAFANA + X-RAY [LATER]

**VO:** "And the polish, when you're ready: Grafana — a 2014 side project that became the standard dashboard for gauges and graphs — and X-Ray, package-tracking for every request, showing which step is slow. Nice on day one, essential by day one thousand."

**VISUAL:** Muted LATER frame. Hero image — a gauge-filled dashboard beside a parcel moving along a tracked route, one slow segment glowing amber. "DAY 1 → DAY 1000" chip.

---

## [9:05 – CLOSE]

**VO:** "That's the whole roadmap: setup, frontend, backend, memory, launch. Thirty-eight hours, near-zero cost until you have users, and every tool here does one job you can name. Follow the five days in order — skip nothing on Day 1 — and ship something real this week. Subscribe if this mapped it out for you, and comment which day you're starting with."

**VISUAL:** The five day cards return in a row, all stamped SHIPPED; the roadmap line draws itself complete underneath. Then the channel outro per Ctrl-Ahead standard (brass arrow, catchphrase) as a separate closing beat — the decided close text above is unchanged.

---

## PRODUCTION NOTES

- VO: Helio, natural pace, verbatim from this script. Segment timecodes re-sync to the real VO in the build (pipeline standard); the ~25s buffer lives in the day-card transitions.
- The two FACT FLAGS stay unresolved in this file on purpose: VO does not record the flagged lines until they're settled — Oliver's word, or the recommended factual fix by default at manifest stage.
- The same Perplexity response also carried "Dad Reframe Lines" for the Payton Glass gallery episode and stream scripts. Those are NOT part of this video and are not in this script; they have not been applied anywhere yet.
- Next: render manifest (scene-by-scene, generated-image prompts per tool, beat-chip timing plan, SFX/music plan) → Oliver's manifest approval → VO + HyperFrames build → full-video delivery for feedback. Nothing published.
