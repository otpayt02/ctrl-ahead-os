"""Ctrl-Ahead OS backend — shared config. Stdlib only."""
import os
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
PIPELINE_DIR = BACKEND_DIR.parent
GOAL_DIR = PIPELINE_DIR.parent.parent
LANES_CSV = GOAL_DIR / "hidden_files" / "harvest" / "subniche_lanes.csv"
INTEL_DIR = PIPELINE_DIR / "data" / "intel"
DB_PATH = BACKEND_DIR / "data" / "ctrl_ahead.db"
RUNS_DIR = BACKEND_DIR / "runs"
QUOTA_FILE = BACKEND_DIR / "data" / "quota.json"
GRILL_QUEUE = BACKEND_DIR / "data" / "grill_queue.json"
GRILL_SPACE_DATA = Path.home() / "workspace" / "space_data" / "grill-me"

MAX_SEARCHES_PER_DAY = 90          # observed limit 100/day; hard stop, no same-day retry after 429
MAX_PER_LANE_TOP = 100             # per-subniche top-100 harvest target
SCRIPT_INPUTS_TOP_N = 10           # per-lane top-10 script_inputs (repo pattern)
COMMENTS_TOP_PER_LANE = 3          # videos per lane to mine comments for
COMMENTS_CAP = 40                  # total comment-mining calls cap (repo pattern)
YOUTUBE_API = "https://www.googleapis.com/youtube/v3"

def yt_api_key():
    return os.environ.get("YT_API_KEY", "").strip()

def week_window(dt=None):
    import datetime
    dt = dt or datetime.date.today()
    iso = dt.isocalendar()
    return f"{iso[0]}-W{iso[1]:02d}"
