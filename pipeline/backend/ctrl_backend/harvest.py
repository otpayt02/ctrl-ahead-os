"""Per-subniche top-100 YouTube harvest.

Live mode: YouTube Data API v3, quota-guarded (max MAX_SEARCHES_PER_DAY searches/day,
persisted in quota.json; on HTTP 429 -> QuotaStop, NO retry, NO endpoint switching).
Proxy mode (no YT_API_KEY): loads the existing per-lane intel bundles already on disk
(previous real harvest, 2026-W43, PARTIAL) and labels everything proxy_existing.
Velocity = lifetime views / age_hours at snapshot. Never CTR / retention / swipe-away.
"""
import csv, datetime, json, urllib.parse, urllib.request, urllib.error
from . import config

class QuotaStop(Exception):
    pass

def load_lanes():
    lanes = {}
    with open(config.LANES_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            lanes.setdefault(row["subniche"], {"cluster": row["cluster"], "queries": []})
            lanes[row["subniche"]]["queries"].append(row["seed_query"])
    return lanes

def _quota_today():
    today = datetime.date.today().isoformat()
    try:
        q = json.loads(config.QUOTA_FILE.read_text())
    except Exception:
        q = {}
    if q.get("date") != today:
        q = {"date": today, "searches": 0, "stopped_429": False}
    return q

def _quota_save(q):
    config.QUOTA_FILE.parent.mkdir(parents=True, exist_ok=True)
    config.QUOTA_FILE.write_text(json.dumps(q, indent=1))

def _api_get(path, params, key):
    q = _quota_today()
    if q["stopped_429"]:
        raise QuotaStop("429 already hit today — stopped, no same-day retry (pipeline rule)")
    if path == "search":
        if q["searches"] >= config.MAX_SEARCHES_PER_DAY:
            raise QuotaStop(f"search budget exhausted ({q['searches']}/{config.MAX_SEARCHES_PER_DAY})")
        q["searches"] += 1
        _quota_save(q)
    url = f"{config.YOUTUBE_API}/{path}?" + urllib.parse.urlencode({**params, "key": key})
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 429:
            q["stopped_429"] = True
            _quota_save(q)
            raise QuotaStop("YouTube API returned 429 — STOP for today, checkpoint saved")
        raise

def _age_hours(published_at, now):
    pub = datetime.datetime.fromisoformat(published_at.replace("Z", "+00:00"))
    return max(1.0, (now - pub).total_seconds() / 3600.0)

def harvest_live(db, lanes, per_lane_limit=50, days=30):
    """Real API harvest. Returns (videos_scored, searches_used)."""
    key = config.yt_api_key()
    now = datetime.datetime.now(datetime.timezone.utc)
    after = (now - datetime.timedelta(days=days)).isoformat().replace("+00:00", "Z")
    scored, seen = 0, set()
    for lane, meta in lanes.items():
        ids = []
        for query in meta["queries"]:
            data = _api_get("search", {"part": "snippet", "type": "video", "maxResults": 50,
                                       "order": "viewCount", "publishedAfter": after, "q": query}, key)
            for it in data.get("items", []):
                vid = it["id"]["videoId"]
                if vid not in seen:
                    seen.add(vid)
                    ids.append((vid, it["snippet"]))
            if len(ids) >= per_lane_limit:
                break
        for i in range(0, len(ids), 50):
            chunk = ids[i:i + 50]
            stats = _api_get("videos", {"part": "statistics,contentDetails,snippet",
                                        "id": ",".join(v for v, _ in chunk)}, key)
            by_id = {s["id"]: s for s in stats.get("items", [])}
            for vid, snip in chunk:
                s = by_id.get(vid)
                if not s:
                    continue
                views = int(s["statistics"].get("viewCount", 0))
                likes = int(s["statistics"].get("likeCount", 0))
                comments = int(s["statistics"].get("commentCount", 0))
                v = {"video_id": vid, "lane": lane, "title": s["snippet"].get("title"),
                     "channel": s["snippet"].get("channelTitle"),
                     "published_at": s["snippet"].get("publishedAt"),
                     "duration": s.get("contentDetails", {}).get("duration")}
                from . import db as dbmod
                dbmod.upsert_video(db, v, "live_api")
                vel = views / _age_hours(v["published_at"], now)
                dbmod.add_snapshot(db, vid, now.isoformat(), views, likes, comments,
                                   round(vel, 2), round(likes / views, 4) if views else 0,
                                   round(comments / views, 4) if views else 0)
                scored += 1
        db.commit()
    return scored, _quota_today()["searches"]

def harvest_proxy_existing(db):
    """No key: ingest the real per-lane intel bundles already harvested (2026-W43, PARTIAL).
    Returns (videos_scored, lanes_with_data, detail). No new numbers are created."""
    scored, lanes_with = 0, 0
    bundles = sorted(config.INTEL_DIR.glob("*/README.md"))
    # intel folders hold week_intelligence-style JSON where present; fall back to portfolio bundle
    candidates = list(config.INTEL_DIR.glob("*/*.json")) + \
        list((config.PIPELINE_DIR / "data" / "portfolio").glob("*/week_intelligence.json"))
    seen_files = set()
    for path in candidates:
        try:
            data = json.loads(path.read_text())
        except Exception:
            continue
        lane = data.get("subniche")
        dims = data.get("dimensions", {})
        items = []
        for dim in dims.values():
            items.extend(dim.get("items", []) if isinstance(dim, dict) else [])
        got = 0
        for it in items:
            vid = it.get("video_id")
            if not vid or vid in seen_files:
                continue
            seen_files.add(vid)
            from . import db as dbmod
            dbmod.upsert_video(db, {"video_id": vid, "lane": lane, "title": it.get("title"),
                                    "channel": it.get("channel"), "published_at": it.get("published_at"),
                                    "duration": it.get("duration")}, "proxy_existing_2026-W43")
            if it.get("views") is not None:
                dbmod.add_snapshot(db, vid, data.get("generated_at", "2026-W43"), it["views"],
                                   None, None, it.get("velocity"),
                                   it.get("like_ratio"), it.get("comment_ratio"))
                for c in (it.get("top_comments") or [])[:5]:
                    db.execute("INSERT INTO comments_mined(video_id,author,text,likes,mined_at,source)"
                               " VALUES(?,?,?,?,?,?)",
                               (vid, c.get("author"), c.get("text"), c.get("likes"),
                                data.get("generated_at"), "proxy_existing_2026-W43"))
                if it.get("hook"):
                    db.execute("INSERT OR REPLACE INTO transcripts(video_id,hook_400,status,fetched_at)"
                               " VALUES(?,?,?,?)", (vid, it["hook"][:400], "ok_proxy_existing",
                                                    data.get("generated_at")))
                scored += 1
                got += 1
        if got:
            lanes_with += 1
    # Also parse the W43 topics menu (real evidence, 15 lanes) — titles/views/velocity/video_id as printed there.
    import re
    menu_files = list((config.PIPELINE_DIR / "data" / "portfolio").glob("*/topics_per_subniche.md"))
    menu_lanes = set()
    for mf in menu_files:
        lane = None
        for line in mf.read_text(errors="ignore").splitlines():
            m = re.match(r"## \d+\. (.+)", line)
            if m:
                lane = m.group(1).strip()
                continue
            m = re.search(r'YouTube top in this lane: "(.+?)" — ([\d,]+) views, velocity ([\d.]+), published ([\d-]+), video_id (\S+)', line)
            if m and lane:
                title, views, vel, pub, vid = m.groups()
                if vid not in seen_files:
                    seen_files.add(vid)
                    from . import db as dbmod
                    dbmod.upsert_video(db, {"video_id": vid, "lane": lane, "title": title,
                                            "published_at": pub}, "proxy_existing_2026-W43-menu")
                    dbmod.add_snapshot(db, vid, "2026-W43", int(views.replace(",", "")), None, None, float(vel), None, None)
                    scored += 1
                menu_lanes.add(lane)
    lanes_with = len({r[0] for r in db.execute("SELECT DISTINCT lane FROM videos").fetchall() if r[0]})
    db.commit()
    return scored, lanes_with, (f"ingested {len(candidates)} existing intel bundle files + "
                                f"{len(menu_files)} topics menu file(s) covering {len(menu_lanes)} lanes; intel folders present: {len(bundles)}")
