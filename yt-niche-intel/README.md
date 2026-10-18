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
6. python yt_niche_intel.py enrich  # fills metadata on older snapshots
7. python yt_niche_intel.py velocity
8. python yt_niche_intel.py comments
9. python yt_niche_intel.py transcripts
10. python yt_niche_intel.py mine

`script_inputs.json` and `script_inputs.md` are local generated inputs for PROMPT 2.
Velocity is views divided by age at the latest snapshot, a cross-sectional proxy.
An AI title/tag filter removes obvious off-topic search hits, but lane labels still
come from search queries and require human review before script selection.
The duration <=3 minutes flag is a Shorts candidate, not proof of YouTube format.
Public data cannot reveal competitor CTR, retention, or viewed-versus-swiped-away.
The comments command reads at most 40 videos per run; transcripts target at most
three velocity leaders per lane, capped at 40 videos.

## Own-upload analytics (local, manual Studio entry)

`own_upload_analytics.py` stores owner-only measurements separately from public
competitor snapshots. Register each upload, then record Studio values after 24h,
48h, and 7d. The database and default CSV export are ignored by Git. No OAuth
or channel connection is configured.

```text
python own_upload_analytics.py register --video-id VIDEO_ID --format short --title "Video title" --published-at 2026-10-18T12:00:00-04:00 --lane "AI tools"
python own_upload_analytics.py snapshot --video-id VIDEO_ID --window 24h --measured-at 2026-10-19T12:00:00-04:00 --viewed-pct 72 --shown-in-feed 1000
python own_upload_analytics.py status
python own_upload_analytics.py export
```

For a long video, enter `--ctr-pct`, `--retention-30s-pct`, and `--avd-seconds`
instead. `swipe_pct` is derived as `100 - viewed_pct` when a Shorts viewed value
is supplied. Missing Studio values remain empty. The 70% Shorts viewed target
(60% working floor), 3-6% long CTR range, and 60-75% first-30s retention range
are starting review targets from the supplied brief, not YouTube distribution rules.
See [the pre-build check](research/first-party-analytics-sanity-check.md).

## Daily: harvest + spikes + rank   |   Weekly: transcripts + AI Studio prompts 1-3
Everything runs on free tiers: YouTube API free quota, Gemini Flash free tier, home-IP
transcripts, local SQLite.

## Never commit
.env, *.db (add to .gitignore before pushing further changes)
