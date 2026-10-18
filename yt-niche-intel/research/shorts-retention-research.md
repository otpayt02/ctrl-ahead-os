# Shorts/Longs Retention & Viewed-vs-Swiped-Away — Pre-Build Research Dump

Date: 2026-10-18 · Lanes: official docs, peer-reviewed, industry, community, contradiction check

## Verdict: GO — with 6 plan changes (see Delta list)

## 1. Official / first-party
- YouTube introduced two Shorts metrics in May 2024: "Shown in Feed" and "Viewed (vs. swiped away)" (YouTube Help community announcement, 2024-05-08).
- CRITICAL CONSTRAINT: this data is owner-only (YouTube Studio). No public API, no per-niche public dataset. Public views/likes/comments cannot infer swipe-away — Codex's caveat in 3ee427a is confirmed correct.
- Consequence: the pipeline must build a first-party measurement loop from upload #1 (track viewed-vs-swiped per Short in a sheet/db) instead of expecting competitor swipe data.

## 2. Peer-reviewed findings
- Bravin, Clegg, Hofstetter, Pouly & Berger (Journal of Marketing, 2026): across 85,000+ TikTok videos plus a creator field experiment, MORE ATYPICAL trend entries generate more engagement. Close copies of winning formats underperform. → Differentiate from the 12 lanes' winning formats; don't clone them.
- Cakmak, Agarwal & Poudel (arXiv 2507.04605, 2025): YouTube Shorts recommendation analyzed across 685,842 videos — popularity bias (high-engagement videos disproportionately promoted), drift toward entertainment/positive-toned content over serious topics. → AI-niche Shorts need entertainment-first framing; put depth in longs.
- Dagtas, Cakmak & Agarwal (arXiv 2507.04534, 2025): simulated watch-time study — small watch-time differences change recommendation chains; higher watch-time → rising topical relevance. → Early retention is the lever that compounds reach.
- Skurla et al. (ACM 2024, TikTok engagement): user attention share stays ~45% while daily usage grows. → Steady attention across sessions; hook quality decides the slice you win.
- Roberts & David (CyberPsychology, Behavior & Social Networking, 2025): recommendation accuracy + perceived effortlessness affordances drive SFV engagement; TikTok rated higher than Reels and YouTube Shorts on these affordances.
- Tian (2026, short-video dissemination study): clustering retention curves shows format adaptation (short-video-native editing) significantly improves EARLY retention and sharing; KOL/influencer seeding dramatically amplifies reach. → Pub-hour histogram + collab seeding belong in the plan.
- Cheng, Ofek & Yoganarasimhan (Marketing Science, 2026, UMG-TikTok dispute): short-form exposure acts as discovery for lesser-known artists (tracks removed from TikTok saw 1-3% stream declines; partial-presence artists benefited). → Directly relevant to the piano/glass-artists pipeline.

## 3. Industry / creator benchmarks (community-backed, medium confidence)
- Viewed-vs-swiped targets: 60% minimum, 70%+ strong, ~75-85% viral territory; below ~50% the Short dies in the feed (Paddy Galloway via r/NewTubers; Thunderbit 2025 benchmarks; Reelrise tiers).
- First 3 seconds: 70-80%+ of viewers should survive; 71% of TikTok users decide within 3s. TikTok Symphony data: humans shown in first 2s = 1.5x hooking power; 90% of ad recall happens within 6s.
- Shorts length: 15-30s retains best (often 80%+); avoid intros entirely.
- Long-form CTR benchmarks: new channels 3-6% (home/suggested), established 5-10%; search 2-5% / 4-8%. First-30s retention: 60-75% (new), 70-85% (established).
- AVD: absolute minutes beat percentages — 20min @ 40% AVD often outperforms 5min @ 80% in suggested traffic. CTR decays fast; first 24-48h window decides; A/B test thumbnails.
- 2026 algorithm emphasis: session contribution, post-watch satisfaction surveys, session continuation.

## 4. Contradiction check
- No evidence contradicts the velocity-ranking approach; lifetime-views/hour is a reasonable day-one proxy but is NOT retention. Public API cannot fix this gap.
- The plan's "public metrics infer performance" assumption is partially wrong: infer packaging/engagement only; swipe data requires first-party uploads.

## 5. Delta list — plan changes from this pass
1. CHANGE: add upload #1 first-party analytics loop — record viewed-vs-swiped, shown-in-feed, swipe rate per Short (target ≥70%, floor 60%).
2. CHANGE: hook budget — value proposition + human face within first 2-3 seconds; zero intro on both Shorts and longs.
3. CONFIRM: 15-30s Shorts cadence; longs carry depth (AI niche skews informational → Shorts feed drift favors entertainment framing).
4. CHANGE: atypicality rule — each lane entry must differ visibly from the lane's winning format (title pattern, angle, or proof type).
5. CONFIRM: pub-hour + cadence consistency; add collab/KOL seeding to roadmap as a reach amplifier.
6. CHANGE: piano/artists lane — treat Shorts as discovery that lifts streaming/longs (UMG study), not as the revenue surface itself.