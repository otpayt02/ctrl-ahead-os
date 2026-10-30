"""Comments + transcript mining. Live mode only, within repo caps.
Proxy mode: hooks/comments already stored by harvest_proxy_existing are reused, labelled.
Transcripts: youtube-transcript-api if installed, else a recorded skip — never a search bypass:
only video IDs already identified by the API/existing harvest are fetched."""
from . import config, harvest as hv

def mine_live(db, lanes_top_videos):
    """lanes_top_videos: {lane: [video_id,...]} — mines top COMMENTS_TOP_PER_LANE per lane, cap COMMENTS_CAP calls."""
    key = config.yt_api_key()
    calls, mined = 0, 0
    import datetime
    for lane, vids in lanes_top_videos.items():
        for vid in vids[:config.COMMENTS_TOP_PER_LANE]:
            if calls >= config.COMMENTS_CAP:
                return mined, calls, "comment cap reached"
            data = hv._api_get("commentThreads", {"part": "snippet", "videoId": vid,
                                                  "maxResults": 5, "order": "relevance"}, key)
            calls += 1
            for it in data.get("items", []):
                s = it["snippet"]["topLevelComment"]["snippet"]
                db.execute("INSERT INTO comments_mined(video_id,author,text,likes,mined_at,source)"
                           " VALUES(?,?,?,?,?,?)", (vid, s.get("authorDisplayName"), s.get("textOriginal"),
                                                    s.get("likeCount"), datetime.datetime.now(datetime.timezone.utc).isoformat(), "live_api"))
                mined += 1
        db.commit()
    return mined, calls, "ok"

def transcripts_for(db, video_ids):
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        for vid in video_ids:
            db.execute("INSERT OR REPLACE INTO transcripts(video_id,hook_400,status,fetched_at)"
                       " VALUES(?,?,?,?)", (vid, None, "skipped: youtube-transcript-api not installed", None))
        db.commit()
        return 0, "skipped: youtube-transcript-api not installed"
    import datetime
    ok = 0
    for vid in video_ids:
        try:
            parts = YouTubeTranscriptApi.get_transcript(vid)
            text = " ".join(p["text"] for p in parts)[:400]
            db.execute("INSERT OR REPLACE INTO transcripts(video_id,hook_400,status,fetched_at) VALUES(?,?,?,?)",
                       (vid, text, "ok", datetime.datetime.now(datetime.timezone.utc).isoformat()))
            ok += 1
        except Exception as e:
            db.execute("INSERT OR REPLACE INTO transcripts(video_id,hook_400,status,fetched_at) VALUES(?,?,?,?)",
                       (vid, None, f"skipped: {type(e).__name__}", None))
    db.commit()
    return ok, "ok"
