#!/usr/bin/env python3
"""Local YouTube niche collection and day-one script evidence exports.

Commands: resolve, harvest, enrich, velocity, comments, transcripts, mine,
rank, spikes. API keys and the SQLite database remain local.
"""
import collections
import csv
import datetime as dt
import json
import os
import re
import sqlite3
import statistics
import sys
import time

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


UTC = dt.timezone.utc
AI_TOPIC = re.compile(
    r"\b(?:ai|artificial intelligence|chatgpt|gpt\s?\d|claude|gemini|llm|"
    r"agent(?:ic)?|codex|openai|anthropic|deepseek|n8n|rag|vibe cod(?:e|ing)|"
    r"higgsfield|sora|grok|midjourney|veo|paperclip|mistral|qwen|glm|"
    r"copilot|cursor|perplexity|machine learning)\b", re.IGNORECASE)
DB = sqlite3.connect("yt_ai_niche.db")
DB.row_factory = sqlite3.Row
C = DB.cursor()
C.executescript("""
CREATE TABLE IF NOT EXISTS snapshots(video_id TEXT, ts TEXT, subniche TEXT,
  views INT, likes INT, comments INT, channel_id TEXT, subs INT, title TEXT,
  PRIMARY KEY(video_id, ts));
CREATE TABLE IF NOT EXISTS channels(channel_id TEXT PRIMARY KEY, name TEXT,
  subniche TEXT, subs INT, median_views INT, checked_at TEXT);
CREATE TABLE IF NOT EXISTS transcripts(video_id TEXT PRIMARY KEY, subniche TEXT,
  fetched_at TEXT, text TEXT);
CREATE TABLE IF NOT EXISTS comments(comment_id TEXT PRIMARY KEY, video_id TEXT,
  author TEXT, text TEXT, likes INT, published_at TEXT);
CREATE INDEX IF NOT EXISTS comments_video ON comments(video_id);
""")
for column, kind in (("duration", "TEXT"), ("tags", "TEXT"),
                     ("category", "INT"), ("published_at", "TEXT")):
    if column not in {row[1] for row in C.execute("PRAGMA table_info(snapshots)")}:
        C.execute(f"ALTER TABLE snapshots ADD COLUMN {column} {kind}")
DB.commit()


def youtube():
    key = os.environ.get("YT_API_KEY")
    if not key:
        raise RuntimeError("YT_API_KEY is missing from the process environment")
    return build("youtube", "v3", developerKey=key)


def utc(value):
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed.replace(tzinfo=UTC) if parsed.tzinfo is None else parsed.astimezone(UTC)


def duration_seconds(value):
    match = re.fullmatch(r"P(?:(\d+)D)?T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", value or "")
    if not match:
        return None
    days, hours, minutes, seconds = (int(part or 0) for part in match.groups())
    return days * 86400 + hours * 3600 + minutes * 60 + seconds


def looks_ai_related(title, tags):
    if AI_TOPIC.search(title or ""):
        return True
    return sum(bool(AI_TOPIC.search(tag)) for tag in tags) >= 2


def latest_videos():
    """Use the latest snapshot for each video and lane, without multiplying repeats."""
    return C.execute("""
        SELECT * FROM (
          SELECT *, ROW_NUMBER() OVER
            (PARTITION BY subniche, video_id ORDER BY ts DESC) AS row_number
          FROM snapshots
        ) WHERE row_number = 1
    """).fetchall()


def scored_videos(days=30):
    now = dt.datetime.now(UTC)
    lanes = collections.defaultdict(list)
    for row in latest_videos():
        if not row["published_at"] or not row["duration"]:
            continue
        try:
            published = utc(row["published_at"])
            sampled = utc(row["ts"])
        except ValueError:
            continue
        if not 0 <= (now - published).total_seconds() <= days * 86400:
            continue
        seconds = duration_seconds(row["duration"])
        if seconds is None:
            continue
        tags = [tag.strip() for tag in (row["tags"] or "").split(";") if tag.strip()]
        if not looks_ai_related(row["title"], tags):
            continue
        views = int(row["views"] or 0)
        age_hours = max((sampled - published).total_seconds() / 3600, 1)
        lanes[row["subniche"]].append({
            "video_id": row["video_id"], "title": row["title"],
            "duration": row["duration"], "published_at": row["published_at"],
            "views": views, "velocity": round(views / age_hours, 2),
            "like_ratio": round((row["likes"] or 0) / views, 4) if views else 0,
            "comment_ratio": round((row["comments"] or 0) / views, 4) if views else 0,
            "tags": tags,
            "is_short": seconds <= 180,
        })
    for videos in lanes.values():
        videos.sort(key=lambda item: (item["velocity"], item["views"]), reverse=True)
    return dict(sorted(lanes.items()))


def save_video(video, when, lane, subscribers):
    snippet = video["snippet"]
    stats = video.get("statistics", {})
    C.execute("""
        INSERT OR REPLACE INTO snapshots
        (video_id, ts, subniche, views, likes, comments, channel_id, subs, title,
         duration, tags, category, published_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (video["id"], when, lane, int(stats.get("viewCount", 0)),
          int(stats.get("likeCount", 0)), int(stats.get("commentCount", 0)),
          snippet["channelId"], subscribers.get(snippet["channelId"], 0),
          snippet["title"], video.get("contentDetails", {}).get("duration"),
          ";".join(snippet.get("tags", [])), int(snippet["categoryId"])
          if snippet.get("categoryId") else None, snippet.get("publishedAt")))


def harvest():
    api = youtube()
    with open("subniche_lanes.csv", encoding="utf8") as source:
        rows = list(csv.DictReader(source))
    now = dt.datetime.now(UTC)
    limit = int(os.environ.get("YT_SEARCH_LIMIT", "95"))
    if not 1 <= limit <= 95:
        raise ValueError("YT_SEARCH_LIMIT must be between 1 and 95")
    searches = 0
    for row in rows:
        for days in (7, 30):
            if searches >= limit:
                DB.commit()
                print(f"done: {searches} searches")
                return
            after = (now - dt.timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
            try:
                result = api.search().list(q=row["seed_query"], type="video",
                    order="viewCount", publishedAfter=after, part="id",
                    maxResults=25, relevanceLanguage="en").execute()
            except HttpError as error:
                DB.commit()
                raise RuntimeError(
                    f"search stopped after {searches} searches (HTTP {error.resp.status}); "
                    "check YouTube API quotas and permissions") from None
            searches += 1
            ids = [item["id"]["videoId"] for item in result.get("items", [])]
            if not ids:
                continue
            videos = api.videos().list(part="statistics,snippet,contentDetails",
                id=",".join(ids)).execute().get("items", [])
            channel_ids = list({item["snippet"]["channelId"] for item in videos})
            subscribers = {}
            if channel_ids:
                channels = api.channels().list(part="statistics", id=",".join(channel_ids)).execute()
                subscribers = {item["id"]: int(item["statistics"].get("subscriberCount", 0))
                    for item in channels.get("items", [])}
            for video in videos:
                save_video(video, now.isoformat(), row["subniche"], subscribers)
            DB.commit()
            time.sleep(0.5)
    print(f"done: {searches} searches")


def enrich():
    """Fill metadata on snapshots collected before this schema existed."""
    api = youtube()
    ids = [row[0] for row in C.execute("""
        SELECT DISTINCT video_id FROM snapshots
        WHERE published_at IS NULL OR duration IS NULL
    """)]
    updated = 0
    for start in range(0, len(ids), 50):
        batch = api.videos().list(part="snippet,contentDetails",
            id=",".join(ids[start:start + 50])).execute()
        for item in batch.get("items", []):
            snippet = item["snippet"]
            C.execute("""
                UPDATE snapshots SET duration=?, tags=?, category=?, published_at=?
                WHERE video_id=?
            """, (item.get("contentDetails", {}).get("duration"),
                  ";".join(snippet.get("tags", [])),
                  int(snippet["categoryId"]) if snippet.get("categoryId") else None,
                  snippet.get("publishedAt"), item["id"]))
            updated += 1
        DB.commit()
    print(f"enriched: {updated} videos")


def velocity():
    lanes = scored_videos()
    if not lanes:
        print("No velocity rows yet; run harvest or enrich first.")
    for lane, videos in lanes.items():
        print(f"\n[{lane}] {len(videos)} videos")
        for item in videos[:10]:
            print(f"{item['velocity']:>10,.0f} views/hour | {item['views']:>10,} views | "
                  f"likes {item['like_ratio']:.2%} | comments {item['comment_ratio']:.2%} | "
                  f"{item['duration']} | {item['title']}")


def comments():
    api = youtube()
    chosen = []
    seen = set()
    for lane, videos in scored_videos().items():
        for item in sorted(videos, key=lambda video: video["views"], reverse=True)[:3]:
            if item["video_id"] not in seen and len(chosen) < 40:
                chosen.append((item["video_id"], lane))
                seen.add(item["video_id"])
    stored = 0
    for video_id, _ in chosen:
        try:
            result = api.commentThreads().list(part="snippet", videoId=video_id,
                order="relevance", maxResults=50, textFormat="plainText").execute()
        except HttpError as error:
            print(f"comments skipped {video_id}: HTTP {error.resp.status}", file=sys.stderr)
            continue
        for item in result.get("items", []):
            top = item["snippet"]["topLevelComment"]
            snippet = top["snippet"]
            C.execute("""
                INSERT OR REPLACE INTO comments
                (comment_id, video_id, author, text, likes, published_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (top["id"], video_id, snippet.get("authorDisplayName", ""),
                  snippet.get("textDisplay", ""), int(snippet.get("likeCount", 0)),
                  snippet.get("publishedAt")))
            stored += 1
        DB.commit()
    print(f"comments: {stored} fetched, {C.execute('SELECT COUNT(*) FROM comments').fetchone()[0]} stored from {len(chosen)} videos")


def transcripts():
    from youtube_transcript_api import YouTubeTranscriptApi
    api = YouTubeTranscriptApi()
    selected = []
    seen = set()
    for lane, videos in scored_videos().items():
        for item in videos[:3]:
            if item["video_id"] not in seen and len(selected) < 40:
                selected.append((item["video_id"], lane))
                seen.add(item["video_id"])
    done = {row[0] for row in C.execute("SELECT video_id FROM transcripts")}
    success = 0
    for video_id, lane in selected:
        if video_id in done:
            continue
        try:
            text = " ".join(snippet.text for snippet in api.fetch(video_id))
            C.execute("INSERT OR REPLACE INTO transcripts VALUES (?,?,?,?)",
                (video_id, lane, dt.datetime.now(UTC).isoformat(), text))
            DB.commit()
            success += 1
        except Exception as error:
            print(f"transcript unavailable {video_id}: {type(error).__name__}", file=sys.stderr)
        time.sleep(1)
    print(f"transcripts: {success} new, {C.execute('SELECT COUNT(*) FROM transcripts').fetchone()[0]} stored")


def mine():
    lanes = scored_videos()
    transcript_text = {row[0]: row[1] for row in C.execute("SELECT video_id, text FROM transcripts")}
    exported = {}
    winners = []
    for lane, videos in lanes.items():
        exported[lane] = []
        for item in videos[:10]:
            data = dict(item)
            data["hook"] = transcript_text.get(item["video_id"], "")[:400]
            data["top_comments"] = [dict(row) for row in C.execute("""
                SELECT author, text, likes, published_at FROM comments
                WHERE video_id=? ORDER BY likes DESC LIMIT 5
            """, (item["video_id"],))]
            exported[lane].append(data)
            winners.append(data)
    unique_winners = {item["video_id"]: item for item in winners}
    distinct = list(unique_winners.values())
    decile = max(1, (len(distinct) + 9) // 10) if distinct else 0
    fastest = sorted(distinct, key=lambda item: item["velocity"], reverse=True)[:decile]
    hours = collections.Counter(utc(item["published_at"]).strftime("%H:00 UTC") for item in fastest)
    bigrams = collections.Counter()
    tags = collections.Counter()
    for item in distinct:
        words = re.findall(r"[\w]+", item["title"].casefold())
        bigrams.update(" ".join(pair) for pair in zip(words, words[1:])
                       if not (pair[0].isdigit() and pair[1].isdigit()))
        tags.update(tag.casefold() for tag in item["tags"])
    result = {
        "generated_at": dt.datetime.now(UTC).isoformat(),
        "method": "Latest snapshot per video/lane; lifetime views divided by age at snapshot. AI title/tag filter removes obvious off-topic results; search-query lane matches still need human review. Duration <=180s is a Shorts proxy, not verified format. Public engagement ratios are not CTR, retention, or viewed-versus-swiped-away.",
        "lanes": exported,
        "publish_hour_histogram_utc": dict(sorted(hours.items())),
        "title_bigrams": [{"phrase": phrase, "count": count}
            for phrase, count in bigrams.most_common() if count >= 2][:20],
        "recurring_tags": [{"tag": tag, "count": count}
            for tag, count in tags.most_common() if count >= 2][:20],
    }
    with open("script_inputs.json", "w", encoding="utf8") as output:
        json.dump(result, output, ensure_ascii=False, indent=2)
    lines = ["# Day-one script inputs", "", f"Generated: {result['generated_at']}", "",
             result["method"], "",
             f"Lanes: {len(exported)} | Lane placements: {len(winners)} | "
             f"Unique videos: {len(distinct)} | "
             f"With transcript hooks: {sum(bool(item['hook']) for item in winners)} | "
             f"With comments: {sum(bool(item['top_comments']) for item in winners)}", "",
             "## Publish hour of top-decile winners (UTC)", ""]
    lines += [f"- {hour}: {count}" for hour, count in result["publish_hour_histogram_utc"].items()]
    lines += ["", "## Recurring title bigrams", ""]
    lines += [f"- {item['phrase']}: {item['count']}" for item in result["title_bigrams"]]
    lines += ["", "## Recurring tags", ""]
    lines += [f"- {item['tag']}: {item['count']}" for item in result["recurring_tags"]]
    lines += ["", "## Lane leaders", ""]
    for lane, videos in exported.items():
        lines += [f"### {lane}", ""]
        lines += [f"- {item['title']} — {item['velocity']:,.0f} views/hour; "
                  f"{item['views']:,} views; {'<=3 min proxy' if item['is_short'] else 'longer video'}"
                  for item in videos[:3]]
        lines.append("")
    with open("script_inputs.md", "w", encoding="utf8") as output:
        output.write("\n".join(lines) + "\n")
    print(f"wrote script_inputs.json and script_inputs.md ({len(winners)} videos)")


def spikes():
    for video_id, title, lane, oldest, newest in C.execute("""
        SELECT video_id, MAX(title), MAX(subniche), MIN(views), MAX(views)
        FROM snapshots GROUP BY video_id
    """):
        if oldest and (newest - oldest) / oldest > 0.3:
            print(f"VIEW SPIKE [{lane}] {title} +{newest - oldest}")


def rank():
    api = youtube()
    ids = [row[0] for row in C.execute("SELECT DISTINCT channel_id FROM snapshots")]
    now = dt.datetime.now(UTC).isoformat()
    for start in range(0, len(ids), 50):
        for channel in api.channels().list(part="statistics,snippet,contentDetails",
                id=",".join(ids[start:start + 50])).execute().get("items", []):
            playlist = channel.get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")
            if not playlist:
                continue
            uploads = api.playlistItems().list(part="contentDetails", playlistId=playlist,
                maxResults=25).execute().get("items", [])
            video_ids = [item["contentDetails"]["videoId"] for item in uploads]
            if not video_ids:
                continue
            videos = api.videos().list(part="statistics", id=",".join(video_ids)).execute()
            views = [int(item.get("statistics", {}).get("viewCount", 0))
                for item in videos.get("items", [])]
            median = int(statistics.median(views)) if views else 0
            C.execute("INSERT OR REPLACE INTO channels VALUES (?,?,?,?,?,?)",
                (channel["id"], channel["snippet"]["title"], None,
                 int(channel["statistics"].get("subscriberCount", 0)), median, now))
        DB.commit()
    for name, subscribers, median in C.execute("""
        SELECT name, subs, median_views FROM channels
        ORDER BY median_views DESC LIMIT 100
    """):
        print(f"{median:>12,} med views | {subscribers:>12,} subs | {name}")


def resolve():
    api = youtube()
    with open("starter_channels.csv", encoding="utf8") as source:
        for row in csv.DictReader(source):
            result = api.search().list(q=row["channel_name"], type="channel",
                part="snippet", maxResults=1).execute()
            if result.get("items"):
                item = result["items"][0]
                print(item["snippet"]["title"],
                    "https://youtube.com/channel/" + item["id"]["channelId"])


if __name__ == "__main__":
    from livestreams import main as streams
    commands = {"resolve": resolve, "harvest": harvest, "enrich": enrich,
                "velocity": velocity, "comments": comments, "transcripts": transcripts,
                "mine": mine, "spikes": spikes, "rank": rank, "streams": streams}
    if len(sys.argv) != 2 or sys.argv[1] not in commands:
        print("usage: python yt_niche_intel.py " + "|".join(commands), file=sys.stderr)
        sys.exit(2)
    try:
        commands[sys.argv[1]]()
    except HttpError as error:
        print(f"YouTube API HTTP {error.resp.status}; check quotas and permissions", file=sys.stderr)
        sys.exit(1)
