"""Velocity scoring + stage narrowing: niche -> subniches -> references -> chosen lane/topic.
Percentiles are within-lane, from scored snapshots only. No scored videos -> UNVERIFIED, score 0
on the YouTube component. Topic score weights are the pipeline README's (25/25/25/15/10);
changelog/GitHub components are filled by the orchestrator when those engines ran, else 0."""

def lane_top(db, lane, n=100):
    rows = db.execute(
        "SELECT v.video_id,v.title,v.channel,v.published_at,s.views,s.velocity,s.like_ratio,s.comment_ratio"
        " FROM videos v JOIN video_snapshots s ON s.video_id=v.video_id WHERE v.lane=?"
        " ORDER BY s.velocity DESC", (lane,)).fetchall()
    best = {}
    for r in rows:  # keep the latest/highest-velocity snapshot per video
        best.setdefault(r["video_id"], r)
    return sorted(best.values(), key=lambda r: r["velocity"] or 0, reverse=True)[:n]

def percentile(values, x):
    if not values:
        return 0.0
    below = sum(1 for v in values if v < x)
    return round(100.0 * below / len(values), 1)

def narrow(db, lanes):
    """Returns per-lane top lists + the single chosen (lane, top video) by velocity percentile head.
    Stage narrowing is recorded, not hidden: every lane's top-10 ships in script_inputs."""
    per_lane, chosen = {}, None
    for lane in lanes:
        top = lane_top(db, lane, 100)
        per_lane[lane] = top
        if top and (chosen is None or (top[0]["velocity"] or 0) > (chosen[1]["velocity"] or 0)):
            chosen = (lane, top[0])
    return per_lane, chosen

def topic_score(youtube_percentile, artifact_fit, buildability=10, changelog_recency=0, github_percentile=0):
    """README weights. artifact_fit: 15 yes / 7 partial / 0 no. buildability: 10 free / 0 paid."""
    return round(changelog_recency + 0.25 * github_percentile + 0.25 * youtube_percentile
                 + artifact_fit + buildability, 1)
