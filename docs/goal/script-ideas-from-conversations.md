# Script Ideas Pack — From Conversations

Ready-to-use pack for the Ideas tab. This document is the pack itself.

This document does not claim the Ideas tab was updated directly. The Ideas tab is owned by the background loop and there is no direct create tool in this work. Copy a card from here into Ideas when you pick it.

## Rules carried from the conversation

- Topic-first. Each idea is about a specific thing talked about this week, or a specific real-world test, not about Ctrl-Ahead parameters or the Ctrl-Ahead pipeline itself.
- Do not invent biography, clients, revenue, view counts, or dates not in the conversation. Anything not verified from a real capture or a dated source in the conversation is labelled UNVERIFIED.
- Do not claim YouTube velocity, CTR, retention, or swipe-away from public view counts.
- Demonstration rule from Oliver's latest instruction: do not just refer to a thing while talking. Show a screenshot or recording of trying it, or of the thing itself, on screen while talking about it. If the demonstration has not been run yet, the card says UNVERIFIED and the demonstration is the first step, before a final script is locked.
- One explicit exception is in this pack, and it is marked as such: the Muse idea at the end. Oliver explicitly requested it, even though it breaks the usual rule that a script must not refer to the pipeline itself.

## Status note for 003 and 004

- 003 and 004 were approved in the conversation for voiceover then render. Their full scripts already exist in `004-both-plus-10-more-concepts.md`. The cards below are summaries for Ideas use, not new full scripts.
- 005–014 are concept cards from that same bundle, not full scripts, unless noted otherwise.

---

## 003 — Nemotron Bolt: 74B in 24GB? Test It, Don't Trust It

- **Lane:** Local LLM setups, plus Open-source model spotlights
- **This-week hook:** NVIDIA Nemotron 3.5, launched 16 Oct 2026. Vendor description in the conversation research: Super VL 120B for docs and business software, Bolt 74B-A9B uses 9B of its 74B, claimed to fit in 24GB with 2-bit quantization on RTX and DGX Spark, Bolt E4B 4GB due 23 Oct, open weights on Hugging Face, OpenRouter, ModelScope, and NIM.
- **Departure from the usual baseline:** The usual baseline is an install guide that repeats the vendor claim. This idea departs by trying to break the claim: measure VRAM, quantization, and governance, and report what actually ran.
- **Artifact / proof:** Oliver's real local LLM work. The test itself is the proof, not a claim made in advance.
- **On-screen demonstration while talking:** A screen recording of the actual Nemotron test on the computer available to Muse, showing the model page, the pull or load step, and the VRAM log as it runs. A screenshot of the Hugging Face or NVIDIA announcement page, with the claim highlighted, shown next to the measured result. Outcome of the test on that machine is UNVERIFIED until the recording is made.

## 004 — n8n 3.0 Will Break Your Quiet Workflows: Audit Before You Upgrade

- **Lane:** n8n / Make workflows
- **This-week hook:** n8n 3.0 scheduled Oct 2026, Docker-only for self-host, with old nodes retiring: Function to Code, Cron to Schedule Trigger, Item Lists split, Read PDF to Extract from File, and AI Agent v1 going. In The Loop Berlin was 13–14 Oct, on production readiness, guardrails, and human-in-the-loop.
- **Departure from the usual baseline:** The usual baseline is an upgrade announcement or a feature list. This idea departs by auditing a real stack first: do not click upgrade until three things are checked.
- **Artifact / proof:** Oliver's real n8n and payroll work, framed as an audit of his own stack. No client, revenue, or workflow result is claimed in advance.
- **On-screen demonstration while talking:** A screen recording of a real n8n workflow inventory search, showing which workflows use a retiring node, a screenshot of the n8n docs or migration page, and a redacted Docker Compose file on screen. A real n8n instance is required for the inventory recording; if no real instance is available, that part is UNVERIFIED and must not be faked.

## 005 — Kimi K3.1 Pro: Open Weights You Cannot Run

- **Lane:** Open-source model spotlights, plus Model release breakdowns
- **This-week hook:** Moonshot Kimi K3.1 Pro, announced 24 Oct 2026. Conversation research: 3-trillion-parameter-class open-weight, weights planned by 4 Nov, cyber data removed. A 25 Oct writeup described Cerebras serving 3T Kimi across 59 wafers, at 1,000–2,000+ tokens per second.
- **Departure from the usual baseline:** The usual baseline is a release announcement that treats open weights as if they were usable by everyone. This idea departs by asking what open means when the model is too large to run locally, and what the practical route is instead.
- **Artifact / proof:** Oliver's real local LLM sizing work. The sizing comparison is the proof, not a claim that Kimi was run locally.
- **On-screen demonstration while talking:** Screenshots of the announcement and the weights timeline, shown while a sizing table is built on screen from the numbers in the announcement. Any local run claim is UNVERIFIED unless a real run is recorded.

## 006 — Claude Code Plugins and the Haiku Price Cliff

- **Lane:** AI coding agents
- **This-week hook:** Claude Haiku 5.5 released 7 Oct, with 1M context and a price of $0.10 / $0.50 under 100K, with a 5x cliff noted in the conversation research. Opus and Sonnet 5.5 also at 1M. Claude Code plugins became official in v2.1.302 on 17–18 Oct. Dynamic Workflows up to 1,000 agents was in beta 9 Oct. This Week in Coding Agents 19 Oct listed Claude Code 2.1.303, Codex CLI 0.163.0 on 15 Oct, Gemini CLI 0.64.0 on 13 Oct, and Cursor cloud canvases on 16 Oct.
- **Departure from the usual baseline:** The usual baseline is a changelog read-through. This idea departs by testing one plugin and one price boundary in a real coding task, and showing where the cost changes.
- **Artifact / proof:** Oliver's real coding and automation work, used as the test task. No client or revenue result is claimed.
- **On-screen demonstration while talking:** A screen recording of a plugin being installed and run in a real coding session, with the version number visible, and a screenshot or recording of the pricing boundary being crossed in a test. Cost outcome for a specific task is UNVERIFIED until the test is run.

## 007 — Gemini Small Business Hub, Tested on Payton Glass

- **Lane:** AI for small business
- **This-week hook:** Google Gemini hub for small business, 20 Oct, with Shopify, Xero, Google Ads, Adobe, Canva, Dropbox, Wix, and Zoho listed in the conversation research, plus saved brand style and finance graphics from spreadsheets and receipts.
- **Departure from the usual baseline:** The usual baseline is a hub announcement that lists integrations. This idea departs by testing the hub against one real small business: Payton Glass.
- **Artifact / proof:** Payton Glass Activity Center, the Louisville glass studio and gallery Oliver works on with his father Mark Payton, and its work to sell fully custom glass nationally.
- **On-screen demonstration while talking:** A screen recording of the hub being tested with a real Payton Glass input, such as a brand style or a finance graphic from a spreadsheet or receipt, with the output shown next to the input. Whether the hub output is usable for Payton Glass is UNVERIFIED until the test is run. No sales or revenue result is claimed.

## 008 — Sora Is Gone: Migrate by Clip Need, Not by Brand

- **Lane:** AI video generation
- **This-week hook:** Sora app shut 26 Apr 2026. Sora API shut 24 Sep 2026 and returns 410 Gone, with no successor named in the conversation research. The current field named there: Veo 3.1, Kling 4.0 Flash and 3.0, Gemini Omni Flash, Runway Gen-4.5, Seedance 2.5, and Wan 3.0.
- **Departure from the usual baseline:** The usual baseline is a shutdown news recap. This idea departs by treating 410 as deletion, not as a pause, and by choosing a replacement by clip need, not by brand loyalty.
- **Artifact / proof:** Oliver's real video work, including the Ctrl-Ahead video work itself as a test case for clip needs, without making the video about the pipeline. The clip test is the proof.
- **On-screen demonstration while talking:** A screen recording showing a 410 response for the old Sora API route, and recordings of the same clip need tried in two or more current tools, with the outputs compared on screen. Comparative quality claims are UNVERIFIED until those recordings are made.

## 009 — Ideogram Vector: Files, Not Pictures

- **Lane:** AI image generation
- **This-week hook:** Ideogram Vector 1.0 launched 22 Oct 2026. Conversation research: text or image to editable SVG, $0.13–$0.32, $0.10 conversion, opens in Illustrator and Figma, with a layer grouping caveat. Same day, Canva Craft in-house model was noted. Price ladder noted: Meta Muse $0.01, Krea edit $0.06, Ideogram SVG $0.10–$0.32.
- **Departure from the usual baseline:** The usual baseline is an image showcase that judges a picture by how it looks. This idea departs by judging editability: can the file be opened, grouped, and changed, or is it just a picture?
- **Artifact / proof:** A real vector file generated in the test, opened in an editor, as proof.
- **On-screen demonstration while talking:** A screen recording of a vector being generated, then opened in Illustrator or Figma, with layers grouped and edited on screen. The layer grouping caveat is shown, not hidden, if it appears in the test. Editability outcome is UNVERIFIED until the recording is made.

## 010 — TanStack AI and Baseten: Probabilities, Not Prose

- **Lane:** AI API integrations, plus Builders
- **This-week hook:** TanStack AI 1.0 on 23 Oct 2026, 76 packages stable, agent harness experimental, with client and server upgrade together noted in the conversation research. Baseten mammoth-1 27B and elephant-1 9B on 21 Oct, trained on 6.21M examples, returning probabilities for choices, scores, and yes-no answers, not text.
- **Departure from the usual baseline:** The usual baseline is a framework release note. This idea departs by testing routing thresholds: when a probability is high enough to act, and when it is not.
- **Artifact / proof:** A real routing test, built from the decision models described, as proof. No client or revenue result is claimed.
- **On-screen demonstration while talking:** A screen recording of a decision model returning a probability, and a threshold rule being applied on screen to route one input one way and another input the other way. Threshold results are UNVERIFIED until the test is run.

## 011 — AI Safety and Policy: What Open Weights Actually Allow

- **Lane:** AI safety and policy
- **This-week hook:** Moonshot curbing cyber data, noted with the Kimi announcement on 24 Oct 2026, plus China draft export controls and open-weight governance noted in the conversation research for the same week. Specific export control text and scope are UNVERIFIED in this pack and must be read from the source page on camera, not summarised from memory.
- **Departure from the usual baseline:** The usual baseline is a policy headline. This idea departs by reading what a governance change actually allows or blocks for a builder, and what review step it adds.
- **Artifact / proof:** Oliver's real S'Gaw Karen and open-weight work as the builder case where governance matters, without claiming a policy outcome in advance.
- **On-screen demonstration while talking:** Screenshots of the source policy pages, with the relevant lines highlighted, shown while the builder impact is walked through on screen. Policy interpretation is UNVERIFIED until the source pages are captured.

## 012 — Mac Local LLM Sizing: Pick by Memory, Not by Hype

- **Lane:** Local LLM setups
- **This-week hook:** Guides from Oct 2026 noted in the conversation research: Gemma 4 12B for 16GB Mac, Qwen3.8 27B for 32GB and above, Qwen3.5 9B about 6.6GB and 4B about 3.3GB. Claude Code local via Ollama on port 11434 and LM Studio on port 1234 was checked 14 Oct.
- **Departure from the usual baseline:** The usual baseline is a model list ranked by size or benchmark. This idea departs with a decision tree based on memory available, and a test on a real machine.
- **Artifact / proof:** Oliver's real local LLM work, and a sizing test run on a real machine.
- **On-screen demonstration while talking:** A screen recording of the memory check, the model load, and the actual memory use while the model runs, with the decision tree filled in from the measured result. Performance on a specific machine is UNVERIFIED until the recording is made.

## 013 — S'Gaw Karen AI: The Review Step Cannot Be Skipped

- **Lane:** Karen-language AI, the unique lane in the 35-lane list
- **This-week hook:** A real-world hook, not a dated news release in the conversation research: S'Gaw Karen OCR, dictionary, and music site work, and Oliver's real pipeline for that community work in Louisville.
- **Departure from the usual baseline:** The usual baseline is a language AI demo that shows output and stops. This idea departs by showing the review step that cannot be skipped, and what happens when it is skipped.
- **Artifact / proof:** Oliver's real S'Gaw Karen OCR, dictionary, and music site work. No community member, client, or outcome is claimed beyond what is in that work.
- **On-screen demonstration while talking:** A screen recording of an OCR or dictionary entry being checked and corrected on screen, with the before and after shown. Any accuracy claim is UNVERIFIED until a real checked example is recorded.

## 014 — Claude Duet and the Decisions API: An Agent That Works While You Are Away

- **Lane:** AI coding agents, plus AI for small business
- **This-week hook:** Claude Duet waitlist 21 Oct. OpenAI Decisions API general availability 22 Oct at $0.10 per million input tokens, noted in the conversation research. Agent Skills donated to the Linux Foundation 22 Oct. Hindsight agent memory v1.0 and v1.1 were also noted in the same week.
- **Departure from the usual baseline:** The usual baseline is an agent announcement that promises autonomy. This idea departs by starting with a permission list: what the agent is allowed to do while the user is away, and what it is not allowed to do.
- **Artifact / proof:** A real permission list, written for a real task, as proof. No autonomous action outcome is claimed in advance.
- **On-screen demonstration while talking:** A screen recording of the permission list being written, then a test task being run under those permissions, with the allowed and blocked actions shown on screen. Autonomy outcome is UNVERIFIED until the test is run.

---

## 015 — Payton Glass: Can a Custom Piece Be Sold Nationally Without Breaking in Shipping?

- **Lane:** AI for small business, plus Productizing AI
- **Real-world hook:** Payton Glass Activity Center, the Louisville glass studio and gallery Oliver works on with his father Mark Payton, revitalising its website to sell fully custom glass nationally, limited by budget, shipping and pickup, and the physical limits of glass.
- **Departure from the usual baseline:** The usual baseline is a studio tour or a product showcase. This idea departs by testing one constraint: the sale, the shipping or pickup choice, and the physical limit, in that order, for one specific custom piece type.
- **Artifact / proof:** The Payton Glass website work, including scroll-driven storytelling and 3D molecule models for dopamine, melanin, and coffee-related models, as described in the conversation memory. No sale, price, or shipping outcome is claimed in advance.
- **On-screen demonstration while talking:** A screen recording scrolling the site and rotating a 3D molecule model on screen, with a shipping and pickup checklist filled in for that piece type. Which piece types can be shipped, and which must be pickup, is UNVERIFIED until the checklist is completed from the real site and studio constraints.

## 016 — AP Music and Audio: Teach a Song by Ear in One Lesson, No Sheet Music First

- **Lane:** AI for beginners, plus AI music and audio
- **Real-world hook:** AP Music and Audio, co-built by Oliver with Alex, covering lessons, performance support, and equipment rental. Oliver is a church music director and piano teacher, with about 18 years of piano, improvisation, transcription, and playing by ear, as described in the conversation memory.
- **Departure from the usual baseline:** The usual baseline is a lesson announcement or a performance clip. This idea departs by teaching one song by ear, in order, and showing the listening, transcription, and playing steps, with sheet music deliberately last, not first.
- **Artifact / proof:** A real lesson structure from AP Music and Audio, and a real song taught by ear in the test. No student, lesson outcome, or booking result is claimed.
- **On-screen demonstration while talking:** A recording of the lesson steps on screen, with the listening and transcription notes shown, and the piano part played in sequence. Lesson outcome for a specific student is UNVERIFIED and must not be claimed.

## 017 — Payroll Media to Tasks: Turn a Voice Note Into Timestamped Tasks

- **Lane:** n8n / Make workflows, plus RAG and pipelines
- **Real-world hook:** Payroll media-to-tasks automation, described in the conversation memory as transcripts and timestamps to Notion and ClickUp.
- **Departure from the usual baseline:** The usual baseline is an automation diagram. This idea departs by running one real payroll media file through the pipeline and showing the tasks that appear, with timestamps, in Notion or ClickUp.
- **Artifact / proof:** The payroll automation project itself, and one real test media file run through it. No payroll amount, employee, client, or employer result is claimed.
- **On-screen demonstration while talking:** A screen recording of the transcript being generated, timestamps being attached, and tasks appearing in Notion or ClickUp, with the task list shown next to the transcript. Accuracy for a specific file is UNVERIFIED until the test recording is made, and any personal payroll content must be redacted on screen.

## 018 — GTD Workflow Auditor: Find the Stalled Items, Don't Reorganise Everything

- **Lane:** AI for small business, plus Prompt engineering
- **Real-world hook:** GTD workflow auditor, described in the conversation memory as an ongoing project.
- **Departure from the usual baseline:** The usual baseline is a productivity system explainer. This idea departs by auditing one real list and naming only the stalled items, with a reason each one stalled, instead of reorganising the whole system.
- **Artifact / proof:** The GTD workflow auditor project, and one real audited list. No task count, completion rate, or client result is claimed in advance.
- **On-screen demonstration while talking:** A screen recording of the auditor running on one list, with stalled items highlighted and the reason for each shown on screen. Audit results for a specific list are UNVERIFIED until the recording is made.

## 019 — Upwork Proposal System: Turn a Real Job Post Into a Proposal Without Inventing Results

- **Lane:** Freelance AI automation
- **Real-world hook:** Upwork proposal system, described in the conversation memory as an ongoing project, plus Oliver's freelance work on Upwork and Fiverr for AI automation, OCR, scraping, document processing, and prompt engineering, and a completed paid Upwork project automating a YouTube video pipeline. No revenue, client name, or proposal outcome is claimed here.
- **Departure from the usual baseline:** The usual baseline is a proposal template showcase. This idea departs by taking one real job post, filling the reusable proposal system from it, and showing what is left blank when proof does not exist, instead of inventing results.
- **Artifact / proof:** The Upwork proposal system and the prompt library `otpayt02/prompts-n-templates-lib`, described in the conversation memory, used as the template source. The completed YouTube pipeline project is proof of work type only, not proof of a proposal outcome.
- **On-screen demonstration while talking:** A screen recording of a real job post being read, the proposal template being filled on screen, and the blanks left where proof does not exist. Proposal success for a specific post is UNVERIFIED and must not be claimed.

## 020 — VIBER Knowledge Graph: Ask One Question and Trace the Answer to Its Source

- **Lane:** RAG and pipelines, plus AI paper walkthroughs
- **Real-world hook:** VIBER personal knowledge graph, described in the conversation memory as an ongoing project, including VIBER Nexus.
- **Departure from the usual baseline:** The usual baseline is a knowledge graph visualisation. This idea departs by asking one specific question, following the answer back to its source notes, and showing the chain, not just the graph.
- **Artifact / proof:** The VIBER knowledge graph itself, and one real question traced through it. No answer accuracy rate is claimed in advance.
- **On-screen demonstration while talking:** A screen recording of the question being asked, the graph nodes being followed on screen, and the source note being opened at the end of the chain. Trace outcome for a specific question is UNVERIFIED until the recording is made.

---

## 021 — Muse Actually Gets Shit Done [SPECIAL, USER-REQUESTED EXCEPTION]

- **Note on the exception:** This idea is an explicit user-requested exception to the usual rule that a script must not refer to the pipeline itself. Oliver explicitly requested this idea. It is included here because he asked for it, not because the usual rule was changed for other ideas.
- **Lane:** Demonstration, not a subniche lane. Do not file this under a 35-lane subniche unless Oliver says to.
- **Hook, in Oliver's own points, paraphrased faithfully:** Muse has approvals baked in, in one place. It has identity baked in. It has a separate computer it can actually do work on. It is the best version of browser use by ChatGPT he has ever had. It has a safe way for him to give it an API key, and it made its own secure input for him to give it to it. It has a main chat and side chats. It does not have to be limited to a specific scope. He corrected it and it just did what he wanted, without a huff and puff about the different approvals needed, and when approvals were needed they were swift.
- **Departure from the usual baseline:** The usual baseline for an AI assistant video is talking about features. This idea departs by demonstrating each point on screen, in sequence, instead of talking about it in general terms.
- **Artifact / proof:** The connected accounts and work from this conversation itself: Google Drive, GitHub, and other connected accounts as demonstration material, plus the Muse computer work, the harvest work, and the correction work. No other Muse feature is claimed in this card, and no result is claimed that was not in the conversation.
- **On-screen demonstration while talking, in order:**
  1. An approval card, shown in one place, being approved swiftly on screen.
  2. Identity shown as baked in, without re-entering it for each task.
  3. The separate computer running real work: a Playwright screenshot or recording being captured, and ffmpeg assembling a video, with the terminal and output files visible.
  4. The safe API key route: the secure input form Muse made for the YouTube key, shown without the key value ever appearing on screen or in chat.
  5. The harvest running, with the real search and output files shown as they are created.
  6. A correction being applied on screen, after Oliver corrected Muse, without a long approval argument, and the corrected result shown next to the original.
  7. Main chat and side chats shown as separate conversations, with work continuing across them without being limited to one specific scope.
- **What must not be faked:** Do not show a key value, do not show a harvest result before a real harvest runs, and do not show a correction before Oliver makes it. If a step has not been recorded yet, that step is UNVERIFIED and the recording is the first step.

---

## How to use a card

1. Pick one card.
2. Run the demonstration in the card first, on the real machine or real account named in the card.
3. Capture the screenshot or recording while you run it, and keep the captured file with the script.
4. Only then lock the script wording to what the capture actually shows.
5. If a capture cannot be made, keep the idea labelled UNVERIFIED and do not publish it as tested.
