# CtrlAhead OS (AheadofRush Engine)

> Private intelligence & content creation engine orchestrating multi-tenant pipelines for **AI Tools**, **Piano Improvisation**, and **Flameworking Glass Art**.

---

## 00-05 Architecture Breakdown

```
[00 BRAIN]      --> Personal training ground (Identity, Voice, Stories, Knowledge, Opinions, Language)
[01 INTEL]      --> 10-platform listener & weekly portfolio (Apify / YT API / Firecrawl / Whisper)
[02 PIPELINE]   --> 1 Core asset + 5 Trial reel variants generator (MoE spins + CapCut / FFmpeg)
[03 TRIALS]     --> Impression & hook performance learning engine (Non-follower reach optimization)
[04 DEPLOY]     --> Orchestrates tiny public frontends (Astro / Next.js)
[05 SYSTEM]     --> Supabase schema, pgvector store, automated cron triggers
```

---

## Low-Cost / Free-Tier Operational Stack

This architecture is optimized for near-zero recurring SaaS overhead:

| Layer | Recommended Free/Budget Tool | Operational Cost |
| :--- | :--- | :--- |
| **Brain DB / Store** | Supabase Free Tier (PostgreSQL + pgvector) | $0/mo |
| **Scheduled Tasks** | GitHub Actions (`.github/workflows/intel-cron.yml`) | Free (2,000 mins/mo) |
| **Transcription** | Local Whisper / OpenAI Whisper API | Negligible / Free local |
| **Frontend UI** | Vercel Hobby / Cloudflare Pages | $0/mo |
| **Audio Processing** | Local Demucs stem splitting + Python Librosa | Free (Local compute) |
| **Music Generation** | Suno Pro (existing plan) | Existing |

---

## Directory Structure

```
├── apps/
│   ├── landing/          # Cinematic liquid puppet landing interface
│   └── os/               # Private dashboard (Brain, Intel, Pipeline, Trials)
├── packages/
│   ├── brain/            # Persona prompts, test gates (Mirror/Friend/Troll)
│   ├── scrapers/         # Headless listeners & transcript extractors
│   ├── pipeline/         # MoE script rewriter & 5-trial variant generator
│   └── audio/            # Piano improv analyzer & stem separator
├── data/
│   ├── brain/            # Core Markdown persona docs
│   ├── improvs/          # Raw audio, analyzed JSONs, separated stems
│   ├── portfolio/        # Weekly creator intelligence archives
│   └── training/         # Clean WAV voice cloning & MP4 avatar data
└── scripts/              # Daily cron jobs & automation drivers
```

---

## Daily 90-Minute Creative Window

- **20 min (Listen):** Check `01 INTEL` weekly brief for trending hooks & topics.
- **50 min (Create):** Record 1 core 5-min video; batch 5 trial cuts (A/B hook, zoom, caption, cover, audio).
- **20 min (Publish):** Queue for 7:00 PM – 9:00 PM; log variations in `03 TRIALS`.
