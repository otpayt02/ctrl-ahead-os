# 003 — CORRECTED: This-week topic first, not pipeline parameters
## Research layer run by Muse, 2026-10-25 — DRAFT FOR APPROVAL, NOT RENDERED

You were right. The 002 draft was built from parameter names — subniche, artifact, format, creativity index — and its teaser even pointed at "the pipeline itself." That is backwards. The pipeline is not the topic. The topic is what people in a subniche were actually talking about this week, and the pipeline / research layer is only how we found it and checked it.

This file fixes that order: scrape first, topic second, script third. Voiceover and render are still HELD until you approve a script.

## 1. What the scrape is supposed to do, from the repo itself

Source checked 2026-10-25, repo otpayt02/ctrl-ahead-os at commit b554874, folder yt-niche-intel/:

- `subniche_lanes.csv` — 35 lanes, 103 seed queries. Not 12 lanes.
- `yt_niche_intel.py` — `harvest` searches each seed query for publishedAfter 7 days and 30 days, order viewCount, max 25, English, then filters with an AI-topic regex. `velocity` = views / age in hours. `comments` = top 3 by views per lane, max 40 videos. `transcripts` = top 3 by velocity per lane, max 40 videos. `mine` writes `script_inputs.json` / `script_inputs.md` with per-lane top 10, transcript hook (first 400 chars), top 5 comments, title bigrams, recurring tags, publish-hour histogram.
- `prompts.md` PROMPT 1 — top 3-5 channels per lane with median-views evidence, kill mega-only lanes, flag mid-size outliers.
- `prompts.md` PROMPT 2 — classify video type, extract TOP 10 recurring patterns, per lane name the winning title pattern / angle / proof type, and mark what is already common so a new concept departs visibly.
- `prompts.md` PROMPT 3 — script generation is artifact x 3 patterns, with an atypicality gate: state the lane baseline, then show a concrete visible departure. It does NOT say the script should be about the pipeline, the parameters, or Ctrl-Ahead OS itself.
- Google Drive / brain_index.json (2026-10-18, v3) — the artifacts that can ground a script are Oliver's real projects: local LLM work, n8n automation, S'Gaw Karen OCR, VIBER Nexus, payroll automation, Payton Glass, AP Music & Audio, etc. Drive folder `ctrl-ahead-os` on the currently connected account only contained a `.venv` folder on this check — no scrape spec file there. The spec lives in the repo, above, not in that Drive folder.

### Honest limit on this run
No `YT_API_KEY` exists on this Linux VM, and the local Windows tree / `yt_ai_niche.db` / `script_inputs.json` were not available. So I did NOT run `yt_niche_intel.py harvest/velocity/transcripts/mine`, and I am NOT claiming YouTube velocity, CTR, retention, or swipe-away for any video below.

What I did run myself, as the research layer, is the equivalent public check for this week (19-25 Oct 2026): news + web search across the seed-query lanes, with dates and sources, to find specific topics actually discussed this week. That is a proxy, not a replacement for a real harvest. A real harvest on your Windows machine with a key would still be needed before claiming any YouTube ranking.

## 2. This week's scrape — specific topics by lane, not parameters

All dates are publication dates found in search on 2026-10-25. No view counts are used as proof of quality.

### Local LLM setups + Open-source model spotlights — LEAD PICK
- **NVIDIA Nemotron 3.5 family, launched 16 Oct 2026.** Super VL 120B for document processing / business software, open weights on Hugging Face / OpenRouter / ModelScope / NVIDIA NIM. Bolt 74B-A9B uses 9B of 74B at a time, and with 2-bit quantization is claimed to fit in 24GB on RTX / DGX Spark. Bolt E4B 4GB was due 23 Oct.
- Why it matters for Oliver: this is directly testable on a desk rig, and it maps to his stated local-LLM work, privacy for client files, and home-rig interest. The testable question is not "is local AI cool?" — it is "does a 74B agent actually fit and work in 24GB, or does 2-bit quant break it?"
- Deductive angle I am adding, not from a parameter: NVIDIA also sells the hardware these models run best on, so speed/ranking claims need a local check. And as one analyst put it in the coverage: "The inference bill shrinks, and the governance surface grows" — local agents can slip past cloud gateways IT uses to watch AI use. That governance point is the real story for freelancers handling client data.

### Model release breakdowns + Open-source model spotlights
- **Moonshot Kimi K3.1 Pro, announced 24 Oct 2026.** Described as a 3-trillion-parameter-class open-weight model, weights planned by 4 Nov, with cyber-related data removed from training. Cerebras writeup 25 Oct shows serving a 3T Kimi across 59 wafers at 1,000-2,000+ tokens/sec.
- Why not lead: huge, interesting, but not runnable on Oliver's desk. Better as a news-recap mention, not a build/test video.

### AI coding agents
- **Claude Code this week:** Haiku 5.5 released 7 Oct, 1M context, $0.10/$0.50 per MTok under 100K tokens then a 5x price cliff; Opus 5.5 / Sonnet 5.5 also 1M context; official plugins + Mods system in v2.1.302 on 17-18 Oct; Dynamic Workflows up to 1,000 agents in beta 9 Oct; This Week in Coding Agents 19 Oct lists Claude Code 2.1.303, Codex CLI 0.163.0 (15 Oct), Gemini CLI 0.64.0 (13 Oct), Cursor cloud canvases (16 Oct).
- Why not lead this time: strong, but it is a changelog recap unless Oliver tests one plugin/workflow end-to-end. Keep as backup lane.

### n8n / Make workflows
- **n8n 3.0 coming Oct 2026, Docker-only for self-host.** Old nodes retiring: Function -> Code, Cron -> Schedule Trigger, Item Lists split, AI Agent v1 going. In The Loop Berlin 13-14 Oct focused on production readiness: guardrails, human-in-the-loop, observable / correctable workflows. n8n Boston HQ + Autom8 Boston 29 Oct.
- Why not lead this time: very relevant to Oliver's n8n / payroll work, and the "check before you upgrade or client workflows break" angle is urgent. This is my #2 pick if you prefer a workflow video over a local-model test. It is NOT about Ctrl-Ahead — it is about n8n breaking changes.

### AI news recaps + AI for small business
- **Week of 13-26 Oct roundup:** Claude Duet waitlist 21 Oct (agent app that works while you are away), OpenAI Decisions API GA 22 Oct at $0.10/M input tokens, Google Gemini hub for small business 20 Oct (Shopify, Xero, Google Ads), Agent Skills donated to Linux Foundation 22 Oct, Hindsight agent memory v1.0/1.1.
- Why not lead: too broad for one script. Use as context, not the topic.

### Other this-week signals noted, not chosen
- TanStack AI 1.0, 23 Oct, 76 packages stable. Baseten mammoth-1 27B / elephant-1 9B, 21 Oct, for scored decisions not text generation. Mistral Timestral time-series model, MiniMax M3.1 Flash weights 23 Oct. Ideogram Vector editable SVGs.

## 3. Corrected concept — 003, topic first

- **Video ID:** 003-nemotron-local-llm
- **Lane (from CSV):** Local LLM setups, with Open-source model spotlights as secondary. Seed queries that match: "local LLM setup", "run LLM on my PC", "ollama vs lm studio", "open source AI model", "best open LLM".
- **This-week topic, in one sentence:** NVIDIA's Nemotron 3.5 Bolt 74B-A9B, launched 16 Oct 2026, is claimed to run an agent-capable 74B model in 24GB with 2-bit quantization — so test it locally instead of repeating the spec sheet.
- **Real Oliver connection, not a parameter stretch:** Oliver builds local LLM / n8n systems so work and client data can stay on his own machine. That is from his Perplexity snapshot and his repos (local models, n8n, midrush-ai), not from HIST 105. The video does not claim he already ran Nemotron — it sets up the test he would run.
- **Format:** Long video, ~11 minutes, faceless after hook, same faceless palette and pacing as 001: 1920x1080, 30 fps, dwell 6-8s, max 15s per image, visible change every 3-5s, captions always on. No Suno bed in this draft — clean room audio, Suno only if you toggle it on in the Grill Me flow.
- **Departure from lane baseline (PROMPT 2 atypicality gate):** Lane baseline for local-LLM videos is usually "install Ollama, pull a small model, chat, done." Visible departure: start from a vendor performance claim (24GB, 74B) and try to break it — measure what actually fits, what 2-bit quant does to answers, and what governance you lose/gain when the model leaves the cloud. If it fails, the failure is the video.
- **What this video is NOT about:** It is not about Ctrl-Ahead OS, yt-niche-intel, subniche parameters, creativity index, or the pipeline. Those words do not appear in narration. The pipeline is the research method, mentioned at most in a production note, never as the subject.

## 4. Timestamped script — narration draft for approval

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
"So here's the checklist before you move a job to local: does it fit in VRAM with room left over, does it fail loudly, can you show the log to someone else, and does the quant version still give the same answer on a job you care about? If yes to all four, local wins for that job. If no to any, keep that job in the cloud and say why. Next video, if you want it: the n8n 3.0 upgrade — what breaks, what to move to Docker, and what to check before you click upgrade on a client workflow."

## 5. Snippet ledger — real captures only

- L1 0:00-0:25 kinetic title: "74B IN 24GB? TEST IT, DON'T TRUST IT" — video text, not a human artifact.
- L2 1:40-3:10 png: real NVIDIA Nemotron 3.5 announcement / Hugging Face page, opened in a real browser via Playwright, with date visible. Do not fake the page.
- L3 3:10-5:00 webm/png: real terminal / Ollama pull attempt, with real size and VRAM output — only a run actually executed, with its real log on screen. If the run has not happened yet, this slot stays PENDING, not staged.
- L4 5:00-6:50 text cards: governance checklist — log, permissions, audit trail.
- L5 6:50-8:30 png/text: memory ladder — 8GB / 16GB / 24GB / 32GB+ picks from this week's guides, labelled as guide recommendations, not measurements.
- L6 9:40-11:00 end card: "NEXT: n8n 3.0 — WHAT BREAKS BEFORE YOU UPGRADE" — note: this is a topic teaser, not a pipeline teaser.

## 6. How the UI should trigger this, corrected

Grill Me / any UI Generate button should NOT just take the picked parameters and write a script about those parameters.

Correct trigger order:
1. User picks lane / format / artifact toggle / reference in the UI.
2. UI triggers the research layer (Muse): run the lane's seed queries for the last 7 days, rank by the yt-niche-intel method where a real harvest exists, otherwise run a dated public search as above and label it as a proxy.
3. Research layer returns: specific this-week topics per lane, with dates/sources, lane baseline, and a visible departure — the inference step.
4. Only then generate the script, about the chosen topic, with the artifact used as proof/test, not as the subject.
5. Log parameters + topic + sources + satisfaction separately, as already requested for the CSV.

If step 2 has no fresh data, the UI must show UNVERIFIED / no fresh harvest, not invent a topic or fall back to "the pipeline."

## 7. What changes for 002

- 002 Freelance AI automation draft is HELD, not approved, not rendered, and its "NEXT EPISODE · THE PIPELINE ITSELF" teaser is withdrawn. Do not use it as the template for topic selection.
- The template to copy from 001 is only the render schema (660s, 1920x1080, 30fps, pacing, palette, caption rules), not the subject matter.
- Voiceover and render for 003 are also HELD until you approve this script in chat.
