# Script DRAFT — NOT APPROVED — VO/render HELD
Topic: AI Agent Memory — How LLM Agents Manage State in Production
Subniche: n8n / Make workflows (business cluster) | Week: 2026-W43
Status: DRAFT for Oliver's approval in chat. No voiceover recorded, no render made, no manifest made from this yet.

## Why this one, in one line
It is the most recent dated changelog evidence we actually have this week (n8n, Oct 23, 2026),
it is specific to a tool Oliver already uses (n8n), and it can be built and tested live in under
4 hours with a real workflow — unlike the GitHub list, which needs filtering first, and unlike
Bolt, which cannot run on the Muse VM.

## Evidence (every factual claim below must trace to one of these, or be marked UNVERIFIED)
- n8n blog, Oct 23, 2026: "AI Agent Memory: How LLM Agents Manage State in Production"
  https://blog.n8n.io/ai-agent-memory-how-llm-agents-manage-state-in-production/
- n8n blog, Oct 22, 2026: "Stateful vs. Stateless: Managing Context in AI Agent Builds"
  https://blog.n8n.io/stateful-vs-stateless/
- n8n blog, Oct 22, 2026: "Self-Hosted LLM vs. Cloud APIs: How to Route Between Them"
  https://blog.n8n.io/self-hosted-llm/
- n8n blog, Oct 19, 2026: "Run your n8n AI workflows on NVIDIA DGX Spark, with no cloud API"
  https://blog.n8n.io/n8n-nvidia-dgx-spark/
- UNVERIFIED / NOT RUN yet: the actual n8n workflow test described below has NOT been run.
  Do not present it as run until it is run and recorded, livestream-style.

## 00:00-00:30 — Hook (30s)
VO draft: "Your AI agent forgot what you just told it. Not because it's dumb — because nobody gave
it memory. This week, n8n put agent memory front and centre, and the difference between an agent
that remembers and one that starts over every single time is the difference between a demo and
a production workflow."
Visual note: title card only for now — no visual claimed as run.

## 00:30-02:00 — Evidence (90s)
VO draft: "On October 23rd, n8n published a piece on how LLM agents manage state in production.
The day before, they published the other half of the same problem: stateful versus stateless.
Stateless means every run starts blank. Stateful means the agent carries context forward — what
the user said, what it already tried, what failed. That is not a vibe, that is a design choice,
and n8n is now writing about it as a production issue, not a toy issue."
Visual note: fetched render of the n8n blog pages above, labelled FETCHED RENDER — NOT A LIVE SCREENSHOT,
until a live re-capture is done.

## 02:00-04:00 — Live test, planned (120s) — NOT RUN YET
VO draft: "Here is the test I want to run, live, so you can see it break and then work. First,
an agent with no memory: ask it a question, then ask a follow-up that depends on the first answer,
and watch it fail. Then the same agent with a memory node, same two questions, and watch it carry
the answer forward. If the second version does not actually remember, I will show that too — I am
not going to cut around a failed test."
Test plan, to be recorded: (1) n8n workflow, chat trigger, LLM node, no memory node, two-turn test;
(2) same workflow with a memory node / session key; (3) same two turns again. Record n8n's own
output, not a re-typed summary. DGX Spark is NOT tested here — that n8n post is context only,
and running on DGX Spark would need hardware we do not have.

## 04:00-05:30 — What breaks / what to watch (90s)
VO draft: "Memory is not free. It grows, it gets stale, it can carry a bad answer forward just as
easily as a good one. It also costs tokens, and if you route that memory through a cloud API
instead of a self-hosted model, you are sending that state out of your own system — which is
exactly the routing choice n8n wrote about on October 22nd. So the question is not 'add memory',
it is 'what memory, for how long, and where does it live?'"
Visual note: diagram of stateful vs stateless, labelled as a diagram, not a screenshot.

## 05:30-06:00 — Close + next step (30s)
VO draft: "If you are building an agent in n8n this week, do this one thing: give it a session key
and a memory node, test it with two turns, and see if it actually remembers. If it does not, you
just found the bug before your users did. That is the whole video — memory is not a feature,
it is the difference between an agent and a chatbot that starts over."
Total planned: 360 seconds (6:00). This is a script duration, NOT a voiceover duration — no VO
has been recorded from this script.

## Approval gate
Oliver: approve / reject / edit this script in chat. Only an approved script moves to:
script -> render manifest (visuals mapped to the timestamps above) -> VO -> render.
No upload, no publish, without separate approval.
