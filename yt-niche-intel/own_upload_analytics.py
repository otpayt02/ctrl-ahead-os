#!/usr/bin/env python3
"""Record owner-only YouTube Studio metrics locally, without OAuth or API calls."""

import argparse
import csv
from datetime import datetime, timedelta, timezone
import math
from pathlib import Path
import sqlite3
import sys


WINDOWS = {"24h": 24, "48h": 48, "7d": 168}
DEFAULT_DB = Path(__file__).with_name("own_upload_analytics.db")
DEFAULT_CSV = Path(__file__).with_name("own_upload_analytics.csv")


def timestamp(value):
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise argparse.ArgumentTypeError("use an ISO 8601 timestamp with a timezone") from error
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise argparse.ArgumentTypeError("timestamp needs a timezone offset or Z")
    return parsed.astimezone(timezone.utc).isoformat()


def percent(value):
    try:
        number = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("percentage must be a number from 0 to 100") from error
    if not 0 <= number <= 100:
        raise argparse.ArgumentTypeError("percentage must be from 0 to 100")
    return number


def nonnegative_int(value):
    try:
        number = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("count must be a nonnegative integer") from error
    if number < 0:
        raise argparse.ArgumentTypeError("count must be a nonnegative integer")
    return number


def nonnegative_float(value):
    try:
        number = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("duration must be nonnegative seconds") from error
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError("duration must be nonnegative seconds")
    return number


def connect(path):
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys=ON")
    connection.executescript("""
        CREATE TABLE IF NOT EXISTS own_uploads (
            video_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            format TEXT NOT NULL CHECK(format IN ('short', 'long')),
            lane TEXT,
            published_at TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS own_upload_snapshots (
            video_id TEXT NOT NULL REFERENCES own_uploads(video_id),
            window TEXT NOT NULL CHECK(window IN ('24h', '48h', '7d')),
            measured_at TEXT NOT NULL,
            source TEXT NOT NULL DEFAULT 'youtube_studio_manual',
            viewed_pct REAL CHECK(viewed_pct BETWEEN 0 AND 100),
            shown_in_feed INTEGER CHECK(shown_in_feed >= 0),
            swipe_pct REAL CHECK(swipe_pct BETWEEN 0 AND 100),
            ctr_pct REAL CHECK(ctr_pct BETWEEN 0 AND 100),
            retention_30s_pct REAL CHECK(retention_30s_pct BETWEEN 0 AND 100),
            avd_seconds REAL CHECK(avd_seconds >= 0),
            notes TEXT,
            PRIMARY KEY(video_id, window)
        );
    """)
    return connection


def register(connection, args):
    connection.execute("""
        INSERT INTO own_uploads(video_id, title, format, lane, published_at, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (args.video_id, args.title, args.format, args.lane, args.published_at,
          datetime.now(timezone.utc).isoformat()))
    connection.commit()
    print(f"registered {args.format} {args.video_id}; checkpoints: 24h, 48h, 7d")


def snapshot(connection, args):
    upload = connection.execute("SELECT * FROM own_uploads WHERE video_id=?",
                                (args.video_id,)).fetchone()
    if upload is None:
        raise ValueError("register this upload before recording a snapshot")
    due = datetime.fromisoformat(upload["published_at"]) + timedelta(hours=WINDOWS[args.window])
    if datetime.fromisoformat(args.measured_at) < due:
        raise ValueError(f"{args.window} checkpoint is not due until {due.isoformat()}")
    short_fields = (args.viewed_pct, args.shown_in_feed, args.swipe_pct)
    long_fields = (args.ctr_pct, args.retention_30s_pct, args.avd_seconds)
    if upload["format"] == "short":
        if any(value is not None for value in long_fields):
            raise ValueError("CTR, first-30s retention, and AVD belong to long videos")
        if all(value is None for value in short_fields):
            raise ValueError("enter at least one Shorts Studio metric")
        viewed = args.viewed_pct
        swiped = args.swipe_pct
        if viewed is not None and swiped is not None and abs(viewed + swiped - 100) > 0.1:
            raise ValueError("viewed and swipe percentages must sum to 100")
        if viewed is None and swiped is not None:
            viewed = round(100 - swiped, 2)
        if swiped is None and viewed is not None:
            swiped = round(100 - viewed, 2)
    else:
        if any(value is not None for value in short_fields):
            raise ValueError("viewed, shown-in-feed, and swipe metrics belong to Shorts")
        if all(value is None for value in long_fields):
            raise ValueError("enter at least one long-video Studio metric")
        viewed = swiped = None
    connection.execute("""
        INSERT INTO own_upload_snapshots
        (video_id, window, measured_at, viewed_pct, shown_in_feed, swipe_pct,
         ctr_pct, retention_30s_pct, avd_seconds, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(video_id, window) DO UPDATE SET
          measured_at=excluded.measured_at,
          viewed_pct=COALESCE(excluded.viewed_pct, own_upload_snapshots.viewed_pct),
          shown_in_feed=COALESCE(excluded.shown_in_feed, own_upload_snapshots.shown_in_feed),
          swipe_pct=COALESCE(excluded.swipe_pct, own_upload_snapshots.swipe_pct),
          ctr_pct=COALESCE(excluded.ctr_pct, own_upload_snapshots.ctr_pct),
          retention_30s_pct=COALESCE(excluded.retention_30s_pct, own_upload_snapshots.retention_30s_pct),
          avd_seconds=COALESCE(excluded.avd_seconds, own_upload_snapshots.avd_seconds),
          notes=CASE WHEN excluded.notes='' THEN own_upload_snapshots.notes ELSE excluded.notes END
    """, (args.video_id, args.window, args.measured_at, viewed,
          args.shown_in_feed, swiped, args.ctr_pct, args.retention_30s_pct,
          args.avd_seconds, args.notes))
    connection.commit()
    print(f"recorded {args.video_id} {args.window} from YouTube Studio")


def target_label(upload_format, row):
    if upload_format == "short":
        viewed = row["viewed_pct"]
        if viewed is None:
            parts = ["viewed unknown"]
        elif viewed < 60:
            parts = [f"viewed {viewed:g}% below 60% working floor"]
        elif viewed < 70:
            parts = [f"viewed {viewed:g}% above floor, below 70% working target"]
        else:
            parts = [f"viewed {viewed:g}% at/above 70% working target"]
        if row["swipe_pct"] is not None:
            parts.append(f"swipe {row['swipe_pct']:g}%")
        if row["shown_in_feed"] is not None:
            parts.append(f"shown in feed {row['shown_in_feed']:,}")
        return "; ".join(parts)
    parts = []
    if row["ctr_pct"] is not None:
        value = row["ctr_pct"]
        tier = "below" if value < 3 else "within" if value <= 6 else "above"
        parts.append(f"CTR {value:g}% ({tier} 3-6% working range)")
    if row["retention_30s_pct"] is not None:
        value = row["retention_30s_pct"]
        tier = "below" if value < 60 else "within" if value <= 75 else "above"
        parts.append(f"30s retention {value:g}% ({tier} 60-75% working range)")
    if row["avd_seconds"] is not None:
        parts.append(f"AVD {row['avd_seconds']:g}s")
    return "; ".join(parts)


def status(connection, args):
    uploads = connection.execute("SELECT * FROM own_uploads ORDER BY published_at DESC").fetchall()
    if not uploads:
        print("No own uploads registered.")
        return
    now = datetime.now(timezone.utc)
    for upload in uploads:
        print(f"{upload['video_id']} [{upload['format']}] {upload['title']}")
        rows = {row["window"]: row for row in connection.execute(
            "SELECT * FROM own_upload_snapshots WHERE video_id=?", (upload["video_id"],))}
        for window, hours in WINDOWS.items():
            due = datetime.fromisoformat(upload["published_at"]) + timedelta(hours=hours)
            if window in rows:
                print(f"  {window}: RECORDED {rows[window]['measured_at']} — {target_label(upload['format'], rows[window])}")
            else:
                state = "DUE" if now >= due else "PENDING"
                print(f"  {window}: {state} {due.isoformat()}")


def csv_text(value):
    # Keep human-entered titles/notes from becoming formulas when CSV opens in a spreadsheet.
    return "'" + value if isinstance(value, str) and value.startswith(("=", "+", "-", "@")) else value


def export(connection, args):
    columns = ("video_id", "title", "format", "lane", "published_at", "window",
               "measured_at", "source", "viewed_pct", "shown_in_feed", "swipe_pct",
               "ctr_pct", "retention_30s_pct", "avd_seconds", "notes")
    rows = connection.execute("""
        SELECT u.video_id, u.title, u.format, u.lane, u.published_at,
               s.window, s.measured_at, s.source, s.viewed_pct, s.shown_in_feed,
               s.swipe_pct, s.ctr_pct, s.retention_30s_pct, s.avd_seconds, s.notes
        FROM own_uploads u JOIN own_upload_snapshots s USING(video_id)
        ORDER BY u.published_at, u.video_id,
          CASE s.window WHEN '24h' THEN 1 WHEN '48h' THEN 2 ELSE 3 END
    """).fetchall()
    with open(args.output, "w", encoding="utf-8", newline="") as destination:
        writer = csv.writer(destination)
        writer.writerow(columns)
        for row in rows:
            writer.writerow([csv_text(row[column]) for column in columns])
    print(f"exported {len(rows)} snapshots to {args.output}")


def parser():
    root = argparse.ArgumentParser(description=__doc__)
    root.add_argument("--db", type=Path, default=DEFAULT_DB,
                      help="local SQLite path (default: ignored file beside script)")
    commands = root.add_subparsers(dest="command", required=True)
    add = commands.add_parser("register", help="register an owned upload")
    add.add_argument("--video-id", required=True)
    add.add_argument("--title", required=True)
    add.add_argument("--format", choices=("short", "long"), required=True)
    add.add_argument("--lane", default="")
    add.add_argument("--published-at", type=timestamp, required=True)
    measure = commands.add_parser("snapshot", help="record one Studio checkpoint")
    measure.add_argument("--video-id", required=True)
    measure.add_argument("--window", choices=WINDOWS, required=True)
    measure.add_argument("--measured-at", type=timestamp,
                         default=datetime.now(timezone.utc).isoformat())
    measure.add_argument("--viewed-pct", type=percent)
    measure.add_argument("--shown-in-feed", type=nonnegative_int)
    measure.add_argument("--swipe-pct", type=percent)
    measure.add_argument("--ctr-pct", type=percent)
    measure.add_argument("--retention-30s-pct", type=percent)
    measure.add_argument("--avd-seconds", type=nonnegative_float)
    measure.add_argument("--notes", default="")
    commands.add_parser("status", help="show due checkpoints and working targets")
    output = commands.add_parser("export", help="write ignored CSV from local DB")
    output.add_argument("--output", type=Path, default=DEFAULT_CSV)
    return root


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = parser().parse_args()
    connection = connect(args.db)
    try:
        {"register": register, "snapshot": snapshot,
         "status": status, "export": export}[args.command](connection, args)
    except (ValueError, sqlite3.IntegrityError) as error:
        raise SystemExit(f"error: {error}") from None
    finally:
        connection.close()


if __name__ == "__main__":
    main()
