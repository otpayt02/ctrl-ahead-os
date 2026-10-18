# Video 001 — "AI Has a Lost Cause Problem"

**Lane:** AI agents & society · **Mode:** documentary essay with live receipts · **Angle:** unrelated-artifact bridge (history essay → training data) · **Creativity slider:** 50 (structural mapping, explained) · **Runtime:** ~11:00 · **Format:** 16:9, 30fps

## Concept card
- **Bridge:** HIST 105 essay (2021, Race and Reunion) on how America's collective Civil War memory was written by whoever did the remembering — structurally mapped onto LLM training: corpus = textbook, majority-text bias = Lost Cause narrative, RLHF = reconciliationism, provenance + consent + validated pairs = emancipationism.
- **Justification (one sentence, same mechanism not same vibes):** both are memory consolidated through repetition without provenance.
- **Receipts:** HIST 105 essay, the-brain-v1 constants, KOA v4 tracker ("store validated training pairs and consent records"), Karen-Web-Scraper / learn-s-gaw-karen repos, script_inputs.json lanes.
- **Atypicality:** nothing in the 12 lanes does historiography × training data with personal receipts.

## Title options
1. AI Has a Lost Cause Problem (I Found It in My College Notes)
2. I Graded My AI Using a 2021 History Essay — It Failed
3. Your AI Model Misremembers on Purpose. History Explains Why.

## Narration script (timestamped)

### CH1 — HOOK (0:00-0:25) · asset 001-hook
"Every AI you've ever used has the exact same flaw as your high school history textbook — and I can prove it, because the proof is sitting in my homework from 2021. That year I wrote a college essay about how America misremembers the Civil War. Five years later, I build AI pipelines for a living. And once you see what I'm about to show you, you'll never look at a chatbot the same way again."

### CH2 — THE TEXTBOOK (0:25-1:40) · asset 002-two-memories
"Quick setup. In 2021, my history class handed me David Blight's Race and Reunion, and it detonated a memory I didn't know I had. The textbook most of us grew up on carried pieces of a story called the Lost Cause: a version of the Civil War where the South's cause was noble, the war wasn't really about slavery, and everyone reconciled nicely afterward. Here's the sentence from my essay that matters: 'I read it and I didn't think twice about its accuracy.' Hold onto that sentence — it's the whole video. Blight's argument was that collective memory isn't neutral: the version that survives is the version written by whoever did the remembering, repeated the most, and got printed. Three forces fought over that memory. White supremacism — the loud version. Emancipationism — the version with receipts, sources, and page numbers. And reconciliationism — the smoothing force, the 'can't we all just get along' that quietly decided which parts got sanded off. Write those three names down. Because five years later I opened the internals of an AI model — and all three were in there."

### CH3 — THE MAPPING (1:40-3:10) · asset 003-internet-textbook
"Today I build AI pipelines. And when I looked at how these systems learn, I didn't see math first — I saw historiography. The mapping, one sentence each, because I'm not doing vibes — this is structural. A training corpus is a textbook. Nobody wrote it on purpose: it's the internet, a textbook written by whoever showed up. The Lost Cause is majority-text bias: when the loudest sources agree, the model memorizes the agreed version, and the quiet versions just don't get written down. And 'I read it and I didn't think twice'? That's the default state of every person who's ever trusted a fluent answer. The mechanism is identical: memory, consolidated through repetition, with no provenance. A textbook doesn't cite every voice. Neither does a training set."

### CH4 — THE EXPERIMENT (3:10-5:00) · screen recording
"So let's test it. I asked two models about something the internet remembers selectively..." [PRODUCER NOTE: record real demo — prompt 2 models on a topic where online consensus is oversimplified or an undercovered topic is flattened; screen-record prompts + answers; red-underline the uncited claim. Fluent ≠ accurate; fluent is packaging.]

### CH5 — RECONCILIATIONISM IS RLHF (5:00-6:30) · asset 004-rlhf-sphere
"Now the uncomfortable part. After a model learns the raw corpus, humans fine-tune it — RLHF, alignment, helpfulness. Real, necessary work. But understand what it optimizes for: acceptability. An agreeable, both-sided, polished answer. A rough stone polished into a smooth sphere that offends nobody and commits to nothing. Both-sidesing history didn't start with AI. AI industrialized it, and gave it a friendly voice. I'm not saying alignment is evil. I'm saying it makes memory-politics decisions, and we should say that out loud instead of pretending it's neutral plumbing."

### CH6 — EMANCIPATIONISM IS PROVENANCE (6:30-7:50) · asset 005-provenance + tracker screenshot
"So what's the counter-force? In the essay it was the emancipationists — the people with receipts. In AI, it's provenance. And I have a receipt for this one, because I'm building it: this is my actual project tracker, and this line is a real task in a real schema — 'Store validated training pairs and consent records.' Consent records. Validation. Who said it, whether they agreed, whether it checked out. Emancipationism, as a database schema. The memory gets repaired the way it always has been: by citing sources."

### CH7 — THE LANGUAGE THE INTERNET FORGOT (7:50-9:40) · assets 006-karen-corpus, 007-single-shelf
"Here's where it gets real. I work with S'gaw Karen — a language spoken by a community the internet barely wrote down. Almost no footprint. Think about what that means: a model trained on the internet cannot remember what nobody uploaded. A language the internet forgot is invisible to every model built on it. That's either a tragedy or an opening. It's an opening if you're the one who writes it down — with permission gates, provenance tracking, and the community's consent about their own words. OCR pipelines, scrapers, translation pairs: building the corpus the old-fashioned way, the way Blight recovered the memory the textbooks sanded off. Getting the language on the map. AI can't remember what nobody wrote down. So we write it down."

### CH8 — VERDICT + CTA (9:40-11:00) · asset 008-callback
"So, the verdict paragraph — every good essay ends with one. In 2021, I wrote that incomplete historical information is misleading and manipulative to naive citizens. In 2026, we are all the naive citizens. We just outsourced the reading. Three things you can actually do. One: ask your model for sources, and watch what happens. Two: treat fluency as packaging, not proof. Three: if you belong to a community the internet forgot — build the corpus, because that's the only fix that has ever worked. The last line of my essay said a single viewpoint would make our politics a lot less complicated. The machine gives us one viewpoint, smoothly, at scale. Don't read it and not think twice. I'm building all of this in public — the pipeline, the datasets, the renders. Subscribe if you want the build. Next time: the build itself."