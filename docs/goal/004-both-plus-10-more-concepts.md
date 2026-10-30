# Both + 10 more — topic-first, not pipeline-first
## DRAFT FOR APPROVAL — VOICEOVER AND RENDER HELD FOR ALL OF THESE

This is the bundle you asked for: both lead scripts in full, then 10 more concepts.

Rules carried over from the correction:
- Every script below is about a specific thing talked about this week in a subniche, not about Ctrl-Ahead OS, yt-niche-intel, subniche parameters, or a creativity index.
- No YouTube velocity, CTR, retention, or swipe-away is claimed. No YouTube API harvest was run on this VM (no YT_API_KEY, no local Windows DB). Topics below are from dated public news/search on 2026-10-25, labelled as a proxy, not a harvest.
- Every on-screen claim must still be captured for real at render time (Playwright screenshot, ffmpeg/OBS recording, real log). Nothing is faked from memory.
- Format default for the two full scripts: long, ~11 min, faceless after hook, 1920x1080, 30 fps, faceless palette navy #0a1628 / amber #e8a33d / cyan #c9d6df / paper #f5efe6, captions always on. Concepts 005-014 list their own format.

---

# 003 — FULL SCRIPT: 74B in 24GB? Test Nemotron, don't trust it
Lane: Local LLM setups (secondary: Open-source model spotlights)
This-week topic: NVIDIA Nemotron 3.5, launched 16 Oct 2026. Bolt 74B-A9B uses 9B of 74B at a time, claimed to fit in 24GB with 2-bit quantization. Super VL 120B for docs/business software. Bolt E4B due 23 Oct. Open weights.
Oliver proof: his local LLM / n8n work — building systems so client data can stay on his own machine. Not a claim he already ran Nemotron.
Departure: lane baseline is "install Ollama, pull a small model, chat, done." Departure is start from a vendor claim and try to break it, with VRAM, quant damage, and governance checked.

**0:00–0:25 — HOOK**
"Last week NVIDIA said you can run a 74-billion-parameter agent in 24 gigabytes. That's either the most useful local AI news of the year, or a spec sheet doing a lot of heavy lifting. I'm going to test which one it is."

**0:25–1:40 — WHAT ACTUALLY LAUNCHED**
"On October 16, NVIDIA launched Nemotron 3.5. Three models. The big one, Super VL, is 120 billion parameters for documents and business software. The middle one is the interesting one: Bolt 74B-A9B. It has 74 billion parameters total, but only uses 9 billion at a time. With 2-bit quantization, NVIDIA says it fits in 24GB on an RTX card or a DGX Spark. The small one, Bolt E4B, was due October 23. All open weights — Hugging Face, OpenRouter, ModelScope, NIM. I am not repeating NVIDIA's speed claims as fact. NVIDIA sells the hardware these run best on."

**1:40–3:10 — WHY LOCAL MATTERS HERE**
"I build local systems for a reason. When a model runs on my machine, client files, notes, and code don't have to go to someone else's server to get an answer. That's privacy, that's offline work, and that's no per-token bill. The trade-off is real too: a smaller local model can be slower and wronger on hard reasoning. So the question isn't 'local good, cloud bad.' It's 'what can this specific 24GB setup actually do reliably?'"

**3:10–5:00 — THE TEST PLAN, ON SCREEN**
"Here's the test, before I run it. One: pull Bolt 74B-A9B and record the actual download size and VRAM use. Two: run the same three jobs — summarize a document, draft a workflow step, and answer a coding question — and keep the bad answers in. Three: check 2-bit quant damage by comparing it to a larger quant if the card allows it. Four: log what fails loudly and what fails quietly. If it fails quietly and says 'done,' that's a fail. That's the rule I use for client work, and I'm using it here too."

**5:00–6:50 — THE GOVERNANCE CATCH**
"There is a second story here that most install guides skip. When you move an agent off the cloud, you also move it off the cloud's guardrails. One analyst put it like this: the inference bill shrinks, and the governance surface grows. Local agents can slip past the gateways IT uses to watch AI use. That means you own the logging, the permissions, and the audit trail. If you sell this to a client, that audit trail is part of the product, not an extra."

**6:50–8:30 — WHAT TO DO IF YOU ONLY HAVE 16GB OR 8GB**
"If you don't have 24GB, don't pull the 74B model and hope. The guides this week are consistent on this: on a 16GB Mac, start with Gemma 4 12B; on 32GB+, Qwen3.8 27B is the usual pick; on 8GB, drop to Qwen3.5 2B or 4B. In Ollama, that's `ollama pull` with a tagged size, never an untagged default that can resolve bigger than you expect. LM Studio is the GUI path, Ollama is the CLI/API path — same models, different workflow. Pick by workflow, not by hype."

**8:30–9:40 — WHAT I AM NOT CLAIMING**
"I'm not claiming a YouTube velocity, a CTR, or a retention number for this topic, because I didn't run a YouTube API harvest for this draft and I won't invent one. I'm also not claiming NVIDIA's throughput or benchmark rank as my own result — those are NVIDIA's figures until I measure them. If a video shows you a chart with no run behind it, ask for the run."

**9:40–11:00 — VERDICT + CHECKLIST**
"So here's the checklist before you move a job to local: does it fit in VRAM with room left over, does it fail loudly, can you show the log to someone else, and does the quant version still give the same answer on a job you care about? If yes to all four, local wins for that job. If no to any, keep that job in the cloud and say why. Next, if you want it: the n8n 3.0 upgrade — what breaks, what to move to Docker, and what to check before you click upgrade on a client workflow."

Snippet ledger for 003: real NVIDIA / Hugging Face page via Playwright; real Ollama pull + VRAM log (PENDING until actually run, not staged); memory ladder cards; governance checklist cards.

---

# 004 — FULL SCRIPT: n8n 3.0 will break your quiet workflows — check before you upgrade
Lane: n8n / Make workflows (secondary: AI for small business)
This-week topic: n8n 3.0 scheduled Oct 2026, Docker-only for self-host, legacy nodes retiring, AI Agent v1 going. In The Loop Berlin 13-14 Oct 2026 on production readiness.
Oliver proof: his n8n work — payroll media-to-tasks, data processing, client automations. Framed as an audit of his own stack, not a named client job.
Departure: lane baseline is "here's a cool workflow I built." Departure is "here's a workflow that will stop working if you click upgrade, and the audit to save it."

**0:00–0:25 — HOOK**
"If you run n8n for yourself or for clients, do not click upgrade on 3.0 until you check three things. One of them will quietly break a workflow that looks fine today."

**0:25–1:40 — WHAT 3.0 ACTUALLY CHANGES**
"n8n 3.0 is scheduled for October 2026, and it's a tidy-up release with teeth. Self-hosted n8n will require Docker. If you installed with npm or npx, that road ends. Old nodes are retiring too: Function and Function Item become the Code node, Cron and Interval become the Schedule Trigger, Item Lists splits into Split Out, Aggregate, Sort and Limit, Read PDF becomes Extract from File, Workflow Trigger becomes the n8n Trigger, and the old OpenAI nodes move to the current OpenAI node. Version 1 of the AI Agent node is also going."

**1:40–3:10 — WHY QUIET BREAKS ARE WORSE THAN LOUD ONES**
"A workflow that errors on upgrade is annoying. A workflow that runs but does the wrong thing is dangerous — especially if it touches invoices, leads, payroll data, or customer messages. That's why this video isn't a feature tour. It's an audit. Open every workflow, search for the old node names, and write them down before you touch Docker."

**3:10–5:00 — THE AUDIT, STEP BY STEP**
"Step one: export or snapshot every active workflow. Step two: list every workflow that uses Function, Cron, Item Lists, Read PDF, Workflow Trigger, or AI Agent v1. Step three: move self-host to Docker Compose first, on a copy, not on the live server. Step four: migrate one workflow at a time, run it with sample data, and compare the output to the old run. If the output changes and you can't explain why, stop. That's not an upgrade, that's a rewrite you didn't plan."

**5:00–6:50 — PRODUCTION READINESS, FROM IN THE LOOP**
"n8n's own conference this month, In The Loop in Berlin on October 13 and 14, put it the right way: production readiness isn't 'can an agent do this task?' It's 'can this workflow be observed, controlled, and corrected when it doesn't behave?' That means guardrails and human-in-the-loop where it matters. Hold probabilistic AI to deterministic rules for routing, approvals, and limits before an action reaches a customer, a database, or a payment. If your workflow can't be paused, logged, and rolled back, it's a demo, not production."

**6:50–8:30 — A REAL CHECK: ERROR NOTIFICATIONS AND FALLBACKS**
"Here's the test I use. Turn on error notifications, feed the workflow a bad input on purpose, and watch where it stops. Does it tell you which node broke? Does it leave the bad output out of the client's file? Does it retry in a way you can see? If it fails quietly and still says done, fix that before 3.0, not after. And document each workflow in three lines: what triggers it, what it touches, and who gets paged when it fails. That doc is what saves you at 2 a.m."

**8:30–9:40 — WHAT NOT TO DO**
"Don't upgrade live on a Friday. Don't migrate five workflows at once and hope the diff is clean. Don't trust an AI-generated workflow that looks right but uses nodes that don't exist or fields with the wrong names — that's the exact failure mode other builders flagged this week for plain-English-to-n8n tools. Validate against real node schemas, test with sample data, and keep credentials in n8n credentials, never pasted into a node field."

**9:40–11:00 — VERDICT + CHECKLIST**
"So before 3.0: Docker first, on a copy. Old nodes list second. One-by-one migration third. Error test fourth. If you do that, 3.0 is a cleaner, safer platform. If you skip it, 3.0 is the update that breaks the quiet workflows you forgot you had. Next: Sora is gone — what to migrate to, and what not to promise a client anymore."

Snippet ledger for 004: real n8n docs / migration page via Playwright; real screen recording of an n8n workflow inventory search (only a real instance, not staged); Docker Compose file on screen, redacted credentials; checklist cards.

---

# 10 MORE CONCEPTS — 005 to 014

Each concept below is topic-first, with a hook, angle, lane, artifact, format, and departure. Full timestamped scripts can be generated from any one of these on approval — VO/render still held until you pick one.

## 005 — Kimi just got huge, and smaller at the same time
Lane: Model release breakdowns
Topic this week: Moonshot Kimi K3.1 Pro, announced 24 Oct 2026, 3-trillion-parameter-class open-weight, weights by 4 Nov, cyber data removed. Cerebras serving 3T Kimi across 59 wafers, 1,000-2,000+ tokens/sec, ~1.18 MW rig math in community discussion.
Angle: Open weights don't mean open access — a 3T model you can't run is a different kind of closed.
Oliver proof: his open-model / local-model work — what "open" actually means when the hardware bill is the gate.
Format: Long, ~10 min, explainer + test of what is actually downloadable vs runnable.
Hook: "A 3-trillion-parameter model just went open. You still can't run it. That's the story."
Departure: Don't recap specs. Show the gap between weights published and weights usable, and who actually benefits.

## 006 — Claude Code plugins are the real update, not the model
Lane: AI coding agents
Topic this week: Claude Code v2.1.302 plugins official 17-18 Oct, Mods system, cloud sessions that keep running after you close the laptop. Haiku 5.5 released 7 Oct, 1M context, $0.10/$0.50 under 100K tokens, then 5x price cliff. Dynamic Workflows up to 1,000 agents, beta 9 Oct.
Angle: The fight moved from which model writes code to who controls what an agent is allowed to do inside a repo.
Oliver proof: his Codex / Claude / repo work, AGENTS.md conventions, and prompt library otpayt02/prompts-n-templates-lib.
Format: Long, build-with-me, test one official plugin end-to-end and show the permission boundary.
Hook: "Everyone's arguing about Opus vs Sonnet. The plugin system just changed who gets to decide what your agent can touch."
Departure: Don't list changelog items. Test one plugin, show what it can and cannot do without approval, and price the Haiku cliff with a real long-context example.

## 007 — Google just gave small businesses a hub — should Payton Glass connect it?
Lane: AI for small business
Topic this week: Google Gemini small business hub, announced 20 Oct 2026. Business landing page, connections to Google Business Profile / Ads / Workspace plus Shopify, Wix, Zoho, Xero, Adobe, Canva, Dropbox. Saved brand style with Nano Banana 2.1, finance graphics from spreadsheets/receipts.
Angle: A hub is useful only if you decide what NOT to connect — brand, money, and customer data need different rules.
Oliver proof: Payton Glass Activity Center — a real Louisville studio/gallery that needs brand consistency and national custom-glass sales, without handing over its customer list blindly.
Format: Long, ~10 min, applied test: brand kit in, one launch asset out, one finance sheet turned into a graphic, with the approval step left in.
Hook: "Google will now run your brand and your books from one chat box. For a small studio, that's either a superpower or a leak you volunteered for."
Departure: Don't do a Google announcement recap. Run it against a real small business with real constraints — glass shipping, pickup, custom pricing — and show where the hub helps and where a human still signs off.

## 008 — Sora is gone. Your old workflow returns 410.
Lane: AI video generation
Topic this week: Sora app shut 26 Apr 2026, Sora API shut 24 Sep 2026, calls now return 410 Gone, no successor named. Current field Oct 2026: Veo 3.1 (8s, native audio), Kling 4.0 Flash (20s at 720p, full 4.0 not fully shipped), Gemini Omni Flash, Runway Gen-4.5, Seedance 2.5 (30s), Wan 3.0 (sub-$0.10/s value).
Angle: A 410 is not an outage — it's a deletion. Migrate by what the clip actually needed, not by brand loyalty.
Oliver proof: his YouTube / media automation history (yt-auto, Shorts pipeline) — sorting old briefs by need: talking head, long take, volume, edit-existing.
Format: Long, migration guide with a real re-brief: same brief, three models, cost and output compared on screen.
Hook: "If your code still calls Sora, it's not retrying. It's praying. Sora returns 410 now — gone for good."
Departure: Don't rank "best AI video generator." Show the migration decision tree and the cost per second that makes volume work or not.

## 009 — An AI image you can actually edit is worth more than a prettier picture
Lane: AI image generation
Topic this week: Ideogram Vector 1.0 launched 22 Oct 2026 — text or image to editable SVG, $0.13-$0.32 text-to-vector, $0.10 image-to-vector, opens in Illustrator/Figma, shapes/colors/gradients editable, but grouping into layers is still a caveat. Same day Canva launched Craft, its in-house image model. Price ladder this week: Meta Muse Image $0.01, Krea edit $0.06, Ideogram SVG $0.10-$0.32.
Angle: Pixels are for posting. Files are for owning. The price is for editability, not beauty.
Oliver proof: Payton Glass + AP Music & Audio brand work — logos, labels, posters that need to be recolored, resized, and printed, not just posted.
Format: Short-to-long hybrid: Short hook + long test — same logo brief in Ideogram Vector vs a raster model, then edit the SVG live.
Hook: "Every AI image tool gives you a picture. This week one finally gave you a file you can change."
Departure: Don't compare "which looks best." Compare what you can do after generation: recolor, rescale to billboard, fix one shape without regenerating everything.

## 010 — Stop asking AI to write. Ask it to decide — and show its confidence.
Lane: AI API integrations (secondary: RAG & pipelines)
Topic this week: Baseten mammoth-1 27B + elephant-1 9B, released 21 Oct 2026, trained on 6.21M examples, return probabilities for choices/scores/yes-no instead of text. TanStack AI 1.0, 23 Oct 2026, 76 packages stable, agent harness still experimental, client+server must upgrade together.
Angle: Most automation breaks because we parse prose. Decision models return a number you can route on — and escalate when confidence is low.
Oliver proof: his payroll / routing / classification workflows — transcripts to tasks, where a wrong parse is worse than a slow parse.
Format: Long, builder explainer: one routing job built twice — once with a chat model, once with a decision model — and the confidence threshold shown on screen.
Hook: "Your workflow doesn't need a better paragraph. It needs a probability and a rule for what to do when that number is low."
Departure: Don't hype "new models." Show the threshold: auto-route above X, human review below X, and what happens when you get it wrong.

## 011 — The most important AI safety news this week isn't a model. It's a refusal.
Lane: AI safety & policy
Topic this week: Moonshot curbing Kimi K3.1 Pro's cyber-offensive capability, removing cyber data from training, while China drafts export controls on AI malware-generation and vulnerability-discovery tools. Open-weight tension: inspection helps defense, but distribution removes central control.
Angle: Open weights change who is responsible — once files spread, the developer can't update safeguards the way a hosted service can.
Oliver proof: his local-model governance point from 003 — logging, permissions, audit trail — applied to safety, not just business.
Format: Long, news explainer with a clear separation: what Moonshot said, what the draft controls say, what is still open for comment, what is not proven.
Hook: "A lab just shipped a frontier model and deliberately made it worse at hacking. That choice tells you more about 2026 than the benchmark does."
Departure: Don't do fear or hype. Map the trade-off: security inspection vs loss of control, and what a small builder should actually do about it.

## 012 — Pick your local model by memory, not by leaderboard
Lane: Local LLM setups — buying guide angle, distinct from 003's Nemotron test
Topic this week: Oct 25 2026 Mac guide — Gemma 4 12B for 16GB Macs, Qwen3.8 27B for 32GB+, Qwen3.5 2B for 8GB. Ollama vs LM Studio workflow split, plus Oct 10 laptop guide: Qwen3.5 4B ~3.3GB for 8GB RAM, 9B ~6.6GB for 16GB. Claude Code local setup via Ollama :11434 / LM Studio :1234, checked 14 Oct, needs tool-calling + 64K context.
Angle: The best local model is the one you'll actually open tomorrow — and that's a memory math problem, not a benchmark.
Oliver proof: his laptop / home rig reality and his local LLM work — no invented specs for his machine, just the sizing rule and how to check it.
Format: Short, ~6-8 min, practical: memory ladder, one pull command with tagged size, one failure to avoid (untagged 70B default).
Hook: "An 18GB download looks fine until your browser starts dragging and you never open the model again. Pick by RAM first."
Departure: Don't do "top 10 local models." Do one decision tree: RAM -> model -> tool (Ollama CLI vs LM Studio GUI) -> first prompt that proves it works.

## 013 — A language Google Translate doesn't cover, built with open models
Lane: Karen-language AI (unique lane)
Topic this week, deductive: this week's open-weight drops (Nemotron, Kimi, Qwen family) make local, offline work for low-resource languages more feasible — but feasibility is not the same as accuracy, dataset, or shipping. No claim that a specific this-week release was built for Karen.
Angle: For S'Gaw Karen, the bottleneck was never "AI can't do languages." It was data, script, and review — and open local models change where that work can happen.
Oliver proof: his real S'Gaw Karen OCR, dictionary scraper, Karen music site with chord editor, and Louisville community automations. These are from brain_index and his snapshot, not invented for this video.
Format: Long, ~11 min, story + demo: OCR pipeline, dictionary lookup, and the human review step that cannot be skipped.
Hook: "Google Translate doesn't cover S'Gaw Karen. So we had to build the pipeline ourselves — and this week's open models change where that pipeline can live."
Departure: Don't claim a breakthrough. Show the pipeline, the error rate problem, and the review workflow — the honest version of low-resource AI.

## 014 — An agent that works while you're away — what would you actually hand it?
Lane: AI agency teardowns (secondary: AI news recaps)
Topic this week: Claude Duet waitlist 21 Oct 2026 — proactive agent app built on Claude Opus 5.5, works while you are away, for US Pro/Max. OpenAI Decisions API GA 22 Oct at $0.10/M input, no output charge. Agent Skills standard donated to Linux Foundation Agentic AI Foundation 22 Oct, used by 70+ platforms. Hindsight agent memory v1.0/1.1, 53k+ GitHub stars.
Angle: "Works while you're away" is only good if you also decide what it may NOT touch while you're away.
Oliver proof: his agent / workflow work — VIBER, MidRush routing, n8n guardrails — and his rule from 003/004: fail loudly, log everything, human sign-off for customer/money actions.
Format: Long, ~10 min, teardown: three jobs safe to hand off, three jobs to keep human, with permission boundaries on screen.
Hook: "Anthropic just opened a waitlist for an agent that works while you're away. The question isn't can it — it's what are you willing to let it do unsupervised?"
Departure: Don't recap the waitlist. Build the permission list first, then match jobs to it — the opposite of most agent hype videos.

---

## CSV / Grill Me logging note
For the Grill Me CSV, log these as one batch with separate columns, as previously requested:
- idea_satisfaction and build_satisfaction as separate columns, not one score
- status per concept: chosen_for_build / approved / denied / regenerated_whole_batch (if the whole batch is regenerated, mark it as such, not as approved/denied)
- parameters per concept: lane, this-week topic + date, format, artifact used / artifact off, departure dimension, source type (dated public search proxy, not YouTube harvest)
- Do NOT log YouTube velocity/CTR/retention for any of these — those fields stay empty until a real harvest exists.
