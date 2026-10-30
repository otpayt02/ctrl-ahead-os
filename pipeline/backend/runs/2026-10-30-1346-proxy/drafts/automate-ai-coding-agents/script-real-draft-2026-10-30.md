# Script — REAL DRAFT (replaces the backend template slots)
Topic (corrected): Gemini 4 Argon untangled 6 million lines inside Chromium's 40-million-line codebase
Subniche: AI coding agents | Week: 2026-W44 | Origin: automate (proxy run 2026-10-30-1346)
Status: Written from verified evidence 2026-10-30. NOT a build approval — this is the real script + manifest content the Gate 1 approval was supposed to cover. Oliver's 2026-10-30 approval was given on a template; re-present this draft at the manifest gate before VO/render.

## Verification notes (kept off the video frames, per pipeline rules)
- Entity: Gemini 4 Argon is a real, shipped Google model — NOT unconfirmed. Announced 2026-09-30 (limited release to Fairwind Program cyber defenders first), generally available 2026-10-13. This matches Oliver's own verified notes from 2026-10-25/26 (Argon announced Sep 30, GA Oct 13; Opus 5.5 released Sep 22). A 2026-10-30 message in the main chat said "Gemini 4 as a shipped model is still unconfirmed" — that statement is wrong and should not be repeated.
- Correction to the harvest title: the source video is titled "Gemini 4 Argon: Modernizing 40 year code" (YouTube biOWEPYyS5c, published 2026-10-13 per the proxy harvest). The underlying Google story is NOT 40-year-old code: Argon helped separate core webpage handling from a ~6-million-line legacy folder inside Chromium's ~40-MILLION-line codebase, finishing months of restructuring work in weeks; changes were human-reviewed and verified by Chromium's test suites. The draft below uses the 40-million-line version.
- Timely hook (why now, honestly): Argon's introductory API pricing ($2 / $10 per million input/output tokens) runs through 2026-11-30 and doubles on 2026-12-01 ($4 / $20). That deadline — not the Oct 13 GA date — is the current news peg.
- Specs (Google-reported): 1,048,576-token combined input+output context; 77.9% on DeepSWE v1.1 (Google's figure); no free API tier.
- Coverage honesty: harvest data is the backend's PARTIAL proxy run (24 videos scored across 15 lanes from the W43 harvest; no new YouTube pull, YT_API_KEY still missing). The 11,345,114 views / velocity figures in script_inputs/ai-coding-agents.json are from that proxy data and are NOT independently verified — they are not used in the VO.
- Brain angle honesty: the cited "artifact" (files/pipeline/data/intel/ai-coding-agents/README.md) is a one-paragraph lane stub, not a worked artifact. So Segment 3 is framed as what this means for a coding-agent pipeline like Ctrl-Ahead's — analysis, NOT a claim that Oliver ran Argon. No live Argon test has been run.

## Segment 1 — Hook
VO: "Google pointed its newest coding model at the hardest codebase it owns — and it worked. Gemini 4 Argon helped untangle a six-million-line legacy folder buried inside Chromium's forty-million-line codebase, and work Google says would have taken months landed in weeks. This is Ctrl-Ahead — let's look at what actually happened, and what it costs you after December first."

## Segment 2 — Evidence
VO: "The dates first, because they matter. Google announced Argon on September thirtieth, but only vetted cybersecurity defenders got it at first. It went generally available on October thirteenth — so no, this is not a leak, and it's not brand new either. What's in it: a one-million-token context window, input and output combined, and a seventy-seven point nine percent score on DeepSWE, Google's own reported number. Treat vendor benchmarks as a claim, not a verdict — but the Chromium result has something benchmarks don't: commits, in a public tracker, reviewed by human engineers."

## Segment 3 — What it actually did (analysis, not a fake live test)
VO: "Here's the part worth stealing for your own projects. Chrome's problem wasn't bad code — it was tangled code: core webpage handling glued together with everyday browser features, so moving a live page between a tab, a panel, and a floating window could crash the whole browser. Argon didn't rewrite six million lines. It separated them — hundreds of files, multiple clean changes at a time, every one checked against Chromium's test suites and signed off by a human. That's the pattern that transfers: give the agent the mechanical separation work, keep the tests and the review gate human. It's the same shape as any serious coding-agent pipeline — automate the grind, never automate the approval."

## Segment 4 — What breaks / the catch
VO: "Now the catches, and there are three. One: almost every headline result so far comes from Google's own engineers on Google's own code — independent mileage will vary. Two: there's no free API tier. Three — and this is the deadline — the introductory price, two dollars per million input tokens and ten per million output, doubles on December first, to four and twenty. Whatever you plan to test on Argon, the cheap window closes November thirtieth."

## Segment 5 — What you can do (animated checklist close — items build in one by one)
VO: "So, what you can do this week. One: if you maintain a legacy codebase, pick one tangled module — not the whole repo — and run a separation pass with tests as the gate. Two: if Argon is on your test list, run your evaluation before November thirtieth, while it's half price. Three: whatever agent you use, keep a human review step on every change — that's not caution, that's literally how the Chromium result was produced."

## Segment 6 — Outro
VO: "That's the real story: not a model that magically fixes old code, but a workflow that turns months of mechanical untangling into weeks — with humans still holding the gate. If you're new here, welcome — this channel breaks down one AI development like this, with the evidence on screen, every time. Subscribe, and I'll see you in the next one."

## Manifest deltas needed before build (scene-level, replacing the skeleton's NOT RUN slots)
- S1: Chromium codebase visual — generated plate (vast tangled codebase metaphor), date chips "Announced Sep 30" / "GA Oct 13" stamping in as spoken.
- S2: Cinematic text reveals of the verified figures (1M combined context; DeepSWE 77.9% labelled "Google-reported").
- S3: Diagram-style animation of separation (core handling vs browser features splitting apart) — HyperFrames/GSAP, no screenshot-style proof.
- S4: Price-doubling graphic: $2/$10 → $4/$20 with "Dec 1" deadline chip.
- S5: Animated checklist per VO, moving highlight.
- S6: Standard branded outro (subscribe + catchphrase), per playbook.
- Engine rules unchanged from render_manifest.json (HyperFrames + GSAP, one idea per slide, no slow zoom, no repeats, gold spoken-word captions, LTX-2.3 clips as metaphor only once the Vast box is producing).
