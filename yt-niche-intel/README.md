# yt-niche-intel — YouTube AI-Niche Intelligence Pack (v3)
Built 2026-10-18. v3 = COMPLETE Drive inventory (multi-batch sweep, both accounts:
27 current + 10 previous files), VIBER Nexus apps, 44 GitHub repos, project history.

## Files
- yt_niche_intel.py — pipeline (harvest / spikes / rank / transcripts / resolve)
- subniche_lanes.csv — 35 lanes, 103 seed queries
- starter_channels.csv — 19 seed channels from 2026 lists
- brain_index.json — v3: full Drive inventory + VIBER Nexus + repos + project history
- prompts.md — v2: 4 inference prompts incl. VIBER Nexus tour episode

## Day 1 (30 min)
1. Google Cloud -> enable YouTube Data API v3 -> free key
2. pip install google-api-python-client youtube-transcript-api requests
3. setx YT_API_KEY "yourkey" (then open a NEW terminal)
4. python yt_niche_intel.py resolve
5. python yt_niche_intel.py harvest

## Daily: harvest + spikes + rank   |   Weekly: transcripts + AI Studio prompts 1-3
Everything runs on free tiers: YouTube API free quota, Gemini Flash free tier, home-IP
transcripts, local SQLite.

## Never commit
.env, *.db (add to .gitignore before pushing further changes)
