"""Discover completed AI build streams; preserve unknown chat/co-stream fields."""
from __future__ import annotations

import datetime as dt
import json
import os
import re
from pathlib import Path

from googleapiclient.discovery import build

QUERY = 'AI "build with me" OR "build in public"'
COHOST = re.compile(r"\b(?:with|featuring|co-host(?:ed)? by|collab(?:oration)? with)\s+@?[A-Z][\w.-]+", re.I)
FORMAT = {
    "code-along": re.compile(r"\b(?:code|coding|build|program|app)\b", re.I),
    "workflow demo": re.compile(r"\b(?:workflow|automation|agent|n8n)\b", re.I),
    "critique/Q&A": re.compile(r"\b(?:q&a|review|critique|office hours)\b", re.I),
}


def parse_time(value: str):
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def classify(video: dict) -> dict:
    snippet = video.get("snippet", {})
    live = video.get("liveStreamingDetails", {})
    stats = video.get("statistics", {})
    title = snippet.get("title", "")
    description = snippet.get("description", "")
    start, end = live.get("actualStartTime"), live.get("actualEndTime")
    minutes = round((parse_time(end) - parse_time(start)).total_seconds() / 60, 1) if start and end else None
    formats = [name for name, pattern in FORMAT.items() if pattern.search(title + " " + description)]
    collaborators = COHOST.findall(description)
    return {"video_id": video["id"], "url": f"https://youtube.com/watch?v={video['id']}",
            "title": title, "channel": snippet.get("channelTitle"), "duration_minutes": minutes,
            "views": int(stats.get("viewCount", 0)), "comments": int(stats.get("commentCount", 0)),
            "format_signals": formats, "chat_engagement": None,
            "chat_note": "Historical live-chat engagement is unavailable through this public API collection.",
            "co_streaming": "description signal; verify manually" if collaborators else "unknown",
            "cohost_description_signals": collaborators,
            "evidence": {"metadata": "YouTube Data API v3 videos.list", "description_excerpt": description[:500]}}


def collect(limit: int = 25) -> dict:
    key = os.environ.get("YT_API_KEY")
    if not key:
        raise RuntimeError("YT_API_KEY missing")
    api = build("youtube", "v3", developerKey=key)
    response = api.search().list(part="id,snippet", q=QUERY, type="video", eventType="completed",
                                 maxResults=min(50, max(1, limit)), order="viewCount").execute()
    ids = [item["id"]["videoId"] for item in response.get("items", [])]
    videos = api.videos().list(part="snippet,statistics,liveStreamingDetails,contentDetails", id=",".join(ids)).execute().get("items", []) if ids else []
    rows = [classify(video) for video in videos
            if video.get("liveStreamingDetails", {}).get("actualStartTime")
            and re.search(r"\b(ai|agent|llm|vibe coding)\b", video.get("snippet", {}).get("title", ""), re.I)
            and re.search(r"\b(build|building|coding)\b", video.get("snippet", {}).get("title", ""), re.I)
            and not re.search(r"\bpodcast\b", video.get("snippet", {}).get("title", ""), re.I)]
    rows.sort(key=lambda r: (r["views"], r["duration_minutes"] or 0), reverse=True)
    return {"query": QUERY, "collected_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "search_units_estimate": 100, "sample_size": len(rows),
            "method": "Public search sample, sorted by views; not all AI streams. Format/co-host fields are text signals, not verified facts. Chat unknown.",
            "streams": rows}


def main():
    result = collect()
    output = Path(__file__).resolve().parent / "exports" / "livestream_research.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{result['sample_size']} completed streams -> {output}")
    for row in result["streams"][:10]:
        line = f"{row['views']:>9,} views | {row['duration_minutes']} min | {row['title']} | {row['url']}"
        print(line.encode("ascii", errors="replace").decode("ascii"))


if __name__ == "__main__":
    main()
