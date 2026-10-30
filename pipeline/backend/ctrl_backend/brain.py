"""The Brain: indexes Oliver's real context and proposes angles ONLY from indexed items.

Sources (each item keeps a real source_ref — path or URL):
- local: goal workspace files + pipeline docs (titles/headings = keywords)
- Google Drive: file NAMES + mime types via the connected Drive CLI (metadata only, no content invented)
- GitHub: otpayt02 repos via the connected GitHub connector CLI (name + description)
Angles = keyword-overlap matches between a harvested topic and a brain item.
No overlap -> no angle. Nothing is fabricated."""
import datetime, json, re, subprocess
from . import config

STOP = set("ai the a an and or of to in on for with vs how what why best top new my your is it this that from".split())

def tokens(text):
    return {t for t in re.findall(r"[a-z0-9][a-z0-9\-]{2,}", (text or "").lower()) if t not in STOP}

def _now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def index_local(db):
    n = 0
    roots = [config.GOAL_DIR / "files", config.GOAL_DIR / "GOAL.md"]
    for root in roots:
        files = root.rglob("*.md") if root.is_dir() else [root]
        for p in files:
            try:
                head = p.read_text(errors="ignore")[:600]
            except Exception:
                continue
            title_line = next((ln.strip("# ").strip() for ln in head.splitlines() if ln.strip()), p.stem)
            db.execute("INSERT OR REPLACE INTO brain_items(id,kind,name,description,source_ref,keywords,indexed_at)"
                       " VALUES(?,?,?,?,?,?,?)",
                       (f"local:{p}", "local_file", title_line or p.stem, str(p.parent.name),
                        str(p), " ".join(sorted(tokens(title_line + " " + p.stem))), _now()))
            n += 1
    db.commit()
    return n, "ok"

def index_drive(db, limit=100):
    try:
        out = subprocess.run(
            ["/opt/hatch/bin/hatch_gws_cli", "drive", "files", "list",
             "--params", json.dumps({"pageSize": limit, "q": "trashed=false",
                                     "fields": "files(id,name,mimeType,modifiedTime,webViewLink)"})],
            capture_output=True, text=True, timeout=60)
        data = json.loads(out.stdout)
        files = data.get("files", []) if isinstance(data, dict) else []
    except Exception as e:
        return 0, f"skipped: {type(e).__name__}"
    for f in files:
        db.execute("INSERT OR REPLACE INTO brain_items(id,kind,name,description,source_ref,keywords,indexed_at)"
                   " VALUES(?,?,?,?,?,?,?)",
                   (f"drive:{f['id']}", "drive_file", f.get("name", ""), f.get("mimeType", ""),
                    f.get("webViewLink") or f"drive-file:{f['id']}",
                    " ".join(sorted(tokens(f.get("name", "")))), _now()))
    db.commit()
    return len(files), "ok"

def index_github(db, user="otpayt02", limit=50):
    try:
        out = subprocess.run(
            ["/opt/hatch/bin/github", "call-read-tool", "--name", "search_repositories",
             "--arguments-json", json.dumps({"query": f"user:{user}", "perPage": limit})],
            capture_output=True, text=True, timeout=60)
        raw = out.stdout
        items = []
        try:
            parsed = json.loads(raw)
            result = parsed.get("result", parsed) if isinstance(parsed, dict) else {}
            text = result.get("content", [{}])[0].get("text", "")
            items = json.loads(text).get("items", []) if text else []
        except Exception:
            items = []
    except Exception as e:
        return 0, f"skipped: {type(e).__name__}"
    for r in items:
        db.execute("INSERT OR REPLACE INTO brain_items(id,kind,name,description,source_ref,keywords,indexed_at)"
                   " VALUES(?,?,?,?,?,?,?)",
                   (f"github:{r.get('full_name')}", "github_repo", r.get("full_name", ""),
                    (r.get("description") or "")[:300], r.get("html_url", ""),
                    " ".join(sorted(tokens((r.get("full_name") or "") + " " + (r.get("description") or "")))), _now()))
    db.commit()
    return len(items), "ok" if items else "no items parsed from connector output"

def propose_angles(db, run_id, topics, max_per_topic=3):
    """topics: [(lane, title)]. Returns angle dicts, each citing its brain item's source_ref."""
    items = db.execute("SELECT * FROM brain_items").fetchall()
    item_tokens = [(it, tokens(it["name"] + " " + (it["description"] or "") + " " + (it["keywords"] or ""))) for it in items]
    angles = []
    for lane, title in topics:
        tt = tokens(title + " " + lane)
        scored = []
        for it, itok in item_tokens:
            overlap = tt & itok
            if len(overlap) >= 2:
                scored.append((len(overlap), it, overlap))
        for n, it, overlap in sorted(scored, reverse=True, key=lambda x: x[0])[:max_per_topic]:
            angle = (f"Topic '{title}' ({lane}) connects to Oliver's {it['kind']} "
                     f"'{it['name']}' via shared ground: {', '.join(sorted(overlap))}. "
                     f"Angle must be built from that artifact, cited, not asserted beyond it.")
            db.execute("INSERT INTO angles(topic,lane,brain_item_id,angle,overlap_tokens,score,source_ref,run_id)"
                       " VALUES(?,?,?,?,?,?,?,?)",
                       (title, lane, it["id"], angle, ",".join(sorted(overlap)), float(n), it["source_ref"], run_id))
            angles.append({"topic": title, "lane": lane, "brain_item": it["name"], "kind": it["kind"],
                           "angle": angle, "source_ref": it["source_ref"], "overlap": sorted(overlap)})
    db.commit()
    return angles
