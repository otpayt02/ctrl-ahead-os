"""Grill Me front door. Grill Me is a client-only static artifact (no server actions),
so the backend meets it at its export boundary: grill-log CSV / concept JSON dropped in
~/workspace/space_data/grill-me/ (or backend/data/grill_inbox/) is imported into one queue.
Approved Grill Me concepts enter the SAME script -> manifest -> render queue as automate picks.
Queue file: backend/data/grill_queue.json — [{concept, subniche, format, angle, status}]"""
import csv, json
from . import config

INBOX_DIRS = [config.GRILL_SPACE_DATA, config.BACKEND_DIR / "data" / "grill_inbox"]

def load_queue():
    try:
        return json.loads(config.GRILL_QUEUE.read_text())
    except Exception:
        return []

def save_queue(q):
    config.GRILL_QUEUE.parent.mkdir(parents=True, exist_ok=True)
    config.GRILL_QUEUE.write_text(json.dumps(q, indent=1))

def import_exports():
    """Import any Grill Me exports found. Returns (imported, sources_checked)."""
    q = load_queue()
    known = {item.get("concept") for item in q}
    imported, checked = 0, []
    for folder in INBOX_DIRS:
        if not folder.exists():
            checked.append(f"{folder}: absent")
            continue
        for path in list(folder.glob("*.csv")) + list(folder.glob("*.json")):
            checked.append(str(path))
            try:
                if path.suffix == ".csv":
                    rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
                else:
                    rows = json.loads(path.read_text())
                    rows = rows if isinstance(rows, list) else rows.get("concepts", [])
            except Exception:
                continue
            for r in rows:
                concept = r.get("concept") or r.get("title") or r.get("id")
                if not concept or concept in known:
                    continue
                known.add(concept)
                q.append({"concept": concept, "subniche": r.get("subniche", ""),
                          "format": r.get("format", ""), "angle": r.get("angle", ""),
                          "status": r.get("status", "grill_logged"), "source_file": str(path)})
                imported += 1
    save_queue(q)
    return imported, checked

def approved_concepts():
    return [i for i in load_queue() if str(i.get("status", "")).lower() in
            ("approved", "kept", "chosen", "grill_approved")]
