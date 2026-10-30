"""SQLite layer — applies ../schema.sql (if present) + schema_backend.sql."""
import sqlite3
from . import config

def connect():
    config.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(config.DB_PATH)
    db.row_factory = sqlite3.Row
    for sql_file in (config.PIPELINE_DIR / "schema.sql", config.BACKEND_DIR / "schema_backend.sql"):
        if sql_file.exists():
            db.executescript(sql_file.read_text())
    db.commit()
    return db

def upsert_video(db, v, source):
    db.execute(
        "INSERT INTO videos(video_id,lane,title,channel,published_at,duration,source,evidence_url)"
        " VALUES(?,?,?,?,?,?,?,?) ON CONFLICT(video_id) DO UPDATE SET lane=excluded.lane,title=excluded.title",
        (v["video_id"], v.get("lane"), v.get("title"), v.get("channel"), v.get("published_at"),
         v.get("duration"), source, f"https://www.youtube.com/watch?v={v['video_id']}"))

def add_snapshot(db, video_id, snap_at, views, likes, comments, velocity, like_ratio, comment_ratio):
    db.execute(
        "INSERT OR REPLACE INTO video_snapshots(video_id,snapshot_at,views,likes,comments,velocity,like_ratio,comment_ratio)"
        " VALUES(?,?,?,?,?,?,?,?)",
        (video_id, snap_at, views, likes, comments, velocity, like_ratio, comment_ratio))
