#!/usr/bin/env python3
"""yt_niche_intel.py — free YouTube AI-niche intelligence pipeline for otpayt02.
Usage:
  python yt_niche_intel.py harvest      # search per subniche lane + snapshot stats (daily)
  python yt_niche_intel.py spikes       # diff snapshots -> view/sub spikes
  python yt_niche_intel.py rank         # rank channels by median views of last uploads
  python yt_niche_intel.py transcripts  # pull transcripts for hot videos (run locally!)
  python yt_niche_intel.py resolve      # resolve starter_channels.csv names -> IDs (day 1 only)
Setup: pip install google-api-python-client youtube-transcript-api requests
Env var YT_API_KEY = your free key (Google Cloud -> enable YouTube Data API v3).
Quota: search.list = 100 units (100/day bucket); all other reads = 1 unit (10,000/day).
"""
import sqlite3, sys, time, datetime, os, statistics, csv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

YT = build("youtube", "v3", developerKey=os.environ["YT_API_KEY"])
DB = sqlite3.connect("yt_ai_niche.db")
C = DB.cursor()
C.executescript("""
CREATE TABLE IF NOT EXISTS snapshots(video_id TEXT, ts TEXT, subniche TEXT,
  views INT, likes INT, comments INT, channel_id TEXT, subs INT, title TEXT,
  PRIMARY KEY(video_id, ts));
CREATE TABLE IF NOT EXISTS channels(channel_id TEXT PRIMARY KEY, name TEXT,
  subniche TEXT, subs INT, median_views INT, checked_at TEXT);
CREATE TABLE IF NOT EXISTS transcripts(video_id TEXT PRIMARY KEY, subniche TEXT,
  fetched_at TEXT, text TEXT);
""")
DB.commit()

def harvest():
    with open("subniche_lanes.csv", encoding="utf8") as f:
        rows = list(csv.DictReader(f))
    now = datetime.datetime.utcnow()
    week = (now - datetime.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    month = (now - datetime.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
    searched = 0
    search_limit = int(os.environ.get("YT_SEARCH_LIMIT", "95"))
    if not 1 <= search_limit <= 95:
        raise ValueError("YT_SEARCH_LIMIT must be between 1 and 95")
    for row in rows:
        for q, window in [(row["seed_query"], week), (row["seed_query"], month)]:
            if searched >= search_limit:
                DB.commit(); print("done:", searched, "searches"); return
            try:
                r = YT.search().list(q=q, type="video", videoDuration="long",
                    order="viewCount", publishedAfter=window, part="id",
                    maxResults=25, relevanceLanguage="en").execute()
            except HttpError as e:
                DB.commit()
                raise RuntimeError(
                    f"search stopped after {searched} searches (HTTP {e.resp.status}); "
                    "check YouTube API quotas and permissions"
                ) from None
            searched += 1
            ids = [i["id"]["videoId"] for i in r["items"]]
            for i in range(0, len(ids), 50):
                v = YT.videos().list(part="statistics,snippet",
                    id=",".join(ids[i:i+50])).execute()
                ch = list({x["snippet"]["channelId"] for x in v["items"]})
                subs = {c["id"]: int(c["statistics"].get("subscriberCount", 0))
                        for c in YT.channels().list(part="statistics",
                            id=",".join(ch)).execute()["items"]}
                for x in v["items"]:
                    C.execute("INSERT OR REPLACE INTO snapshots VALUES (?,?,?,?,?,?,?,?,?)",
                        (x["id"], now.isoformat(), row["subniche"],
                         int(x["statistics"].get("viewCount", 0)),
                         int(x["statistics"].get("likeCount", 0)),
                         int(x["statistics"].get("commentCount", 0)),
                         x["snippet"]["channelId"], subs[x["snippet"]["channelId"]],
                         x["snippet"]["title"]))
            time.sleep(0.5)
    DB.commit()
    print("done:", searched, "searches")

def spikes():
    for vid, title, sn, v0, v1 in C.execute("""
            SELECT video_id, MAX(title), MAX(subniche), MIN(views), MAX(views)
            FROM snapshots GROUP BY video_id"""):
        if v0 and (v1 - v0) / v0 > 0.3:
            print(f"VIEW SPIKE [{sn}] {title}  +{v1-v0}")
    for ch, s0, s1 in C.execute("""
            SELECT channel_id, MIN(subs), MAX(subs)
            FROM snapshots GROUP BY channel_id"""):
        if s1 - s0 > 300:
            print(f"SUB SPIKE  {ch}  +{s1-s0}")

def rank():
    ids = [r[0] for r in C.execute("SELECT DISTINCT channel_id FROM snapshots")]
    now = datetime.datetime.utcnow().isoformat()
    for i in range(0, len(ids), 50):
        for c in YT.channels().list(part="statistics,snippet,contentDetails",
                id=",".join(ids[i:i+50])).execute()["items"]:
            up = c["contentDetails"]["relatedPlaylists"]["uploads"]
            vids = YT.playlistItems().list(part="contentDetails", playlistId=up,
                    maxResults=25).execute()["items"]
            vs = YT.videos().list(part="statistics", id=",".join(
                    v["contentDetails"]["videoId"] for v in vids)).execute()["items"]
            views = [int(v["statistics"].get("viewCount", 0)) for v in vs]
            med = int(statistics.median(views)) if views else 0
            C.execute("INSERT OR REPLACE INTO channels VALUES (?,?,?,?,?,?)",
                (c["id"], c["snippet"]["title"], None,
                 int(c["statistics"].get("subscriberCount", 0)), med, now))
    DB.commit()
    for name, subs, med in C.execute(
            "SELECT name, subs, median_views FROM channels ORDER BY median_views DESC LIMIT 100"):
        print(f"{med:>12,} med views | {subs:>12,} subs | {name}")

def transcripts():
    from youtube_transcript_api import YouTubeTranscriptApi
    tta = YouTubeTranscriptApi()
    hot = {r[0]: r[1] for r in C.execute(
        "SELECT video_id, MAX(subniche) FROM snapshots GROUP BY video_id HAVING MAX(views) > 50000")}
    done = {r[0] for r in C.execute("SELECT video_id FROM transcripts")}
    for vid, sn in hot.items():
        if vid in done: continue
        try:
            t = tta.fetch(vid)
            C.execute("INSERT OR REPLACE INTO transcripts VALUES (?,?,?,?)",
                (vid, sn, datetime.datetime.utcnow().isoformat(),
                 " ".join(s.text for s in t)))
            print("got", vid)
        except Exception as e:
            print("miss", vid, type(e).__name__)
        time.sleep(3)
    DB.commit()

def resolve():
    with open("starter_channels.csv", encoding="utf8") as f:
        for row in csv.DictReader(f):
            r = YT.search().list(q=row["channel_name"], type="channel",
                    part="snippet", maxResults=1).execute()
            if r["items"]:
                it = r["items"][0]
                print(it["snippet"]["title"],
                      "https://youtube.com/channel/" + it["id"]["channelId"])

if __name__ == "__main__":
    try:
        {"harvest": harvest, "spikes": spikes, "rank": rank,
         "transcripts": transcripts, "resolve": resolve}[sys.argv[1]]()
    except HttpError as e:
        print(f"YouTube API HTTP {e.resp.status}; check quotas and permissions", file=sys.stderr)
        sys.exit(1)
