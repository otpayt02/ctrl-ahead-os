"""Explicit, local artifact import and SQLite-backed TF-IDF retrieval."""
from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import math
import re
import sqlite3
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
DEFAULT_DB = ROOT / "artifacts" / "brain.db"
TEXT_EXT = {".txt", ".md", ".markdown", ".html", ".htm", ".json", ".csv", ".enex"}
MAX_FILE = 20_000_000
TOKEN = re.compile(r"[\w']{2,}", re.UNICODE)


def connect(path: Path = DEFAULT_DB) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.executescript("""
        CREATE TABLE IF NOT EXISTS artifacts (
            id TEXT PRIMARY KEY, kind TEXT NOT NULL, source_uri TEXT NOT NULL,
            title TEXT NOT NULL, body TEXT NOT NULL, sha256 TEXT NOT NULL,
            domain TEXT, imported_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS artifacts_kind ON artifacts(kind);
    """)
    return db


def clean_markup(value: str) -> str:
    value = re.sub(r"(?is)<(script|style).*?</\1>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value))).strip()


def flatten_chatgpt(data: object) -> str:
    if not isinstance(data, dict):
        return ""
    messages = data.get("mapping", {})
    if not isinstance(messages, dict):
        return ""
    parts = []
    for node in sorted(messages.values(), key=lambda n: (n.get("message") or {}).get("create_time") or 0):
        msg = node.get("message") or {}
        content = msg.get("content") or {}
        role = (msg.get("author") or {}).get("role", "unknown")
        chunks = content.get("parts") or []
        line = " ".join(part for part in chunks if isinstance(part, str))
        if line.strip():
            parts.append(f"{role}: {line}")
    return "\n".join(parts)


def records(name: str, raw: bytes, kind: str, source: str):
    suffix = Path(name).suffix.lower()
    decoded = raw.decode("utf-8-sig", errors="replace")
    if suffix == ".enex":
        try:
            root = ET.fromstring(decoded)
        except ET.ParseError:
            return
        for i, note in enumerate(root.findall("note")):
            title = note.findtext("title") or f"Evernote {i+1}"
            body = clean_markup(note.findtext("content") or "")
            if body:
                yield (f"{source}#note-{i+1}", title, body, "evernote")
        return
    if suffix == ".json":
        try:
            data = json.loads(decoded)
        except json.JSONDecodeError:
            return
        if isinstance(data, list) and any(isinstance(x, dict) and "mapping" in x for x in data):
            for i, item in enumerate(data):
                if isinstance(item, dict):
                    body = flatten_chatgpt(item)
                    if body:
                        yield (f"{source}#conversation-{i+1}", item.get("title") or f"Conversation {i+1}", body, "chatgpt")
            return
        if isinstance(data, dict) and "mapping" in data:
            body = flatten_chatgpt(data)
            if body:
                yield (source, data.get("title") or Path(name).stem, body, "chatgpt")
            return
        if "watch-history" in name.lower() and isinstance(data, list):
            for i, item in enumerate(data):
                if isinstance(item, dict):
                    body = " ".join(str(item.get(k, "")) for k in ("title", "titleUrl", "time", "subtitles"))
                    yield (f"{source}#watch-{i+1}", item.get("title", "Watch event"), body, "youtube-watch")
            return
        title = data.get("title", Path(name).stem) if isinstance(data, dict) else Path(name).stem
        yield (source, str(title), json.dumps(data, ensure_ascii=False), kind)
        return
    if kind == "drive" and decoded.startswith("Source: https://"):
        header, _, remaining = decoded.partition("\n")
        uri = header.removeprefix("Source: ").strip()
        if uri.startswith(("https://docs.google.com/", "https://drive.google.com/")):
            source, decoded = uri, remaining
    body = clean_markup(decoded) if suffix in {".html", ".htm"} else decoded.strip()
    if body:
        yield (source, Path(name).stem, body, kind)


def add(db: sqlite3.Connection, source: str, title: str, body: str, kind: str, domain: str = "") -> bool:
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    artifact_id = hashlib.sha256(source.encode("utf-8")).hexdigest()[:20]
    old = db.execute("SELECT sha256 FROM artifacts WHERE id=?", (artifact_id,)).fetchone()
    db.execute("INSERT INTO artifacts(id,kind,source_uri,title,body,sha256,domain) VALUES(?,?,?,?,?,?,?) "
               "ON CONFLICT(id) DO UPDATE SET kind=excluded.kind,title=excluded.title,body=excluded.body,sha256=excluded.sha256,domain=excluded.domain,imported_at=CURRENT_TIMESTAMP",
               (artifact_id, kind, source, title, body, digest, domain))
    return old is None or old[0] != digest


def ingest_path(db: sqlite3.Connection, path: Path, kind: str, domain: str = "") -> tuple[int, int]:
    if not path.exists():
        raise FileNotFoundError(path)
    changed = skipped = 0
    paths = sorted(path.rglob("*")) if path.is_dir() else [path]
    for item in paths:
        if not item.is_file() or item.is_symlink():
            continue
        if item.suffix.lower() == ".zip":
            with zipfile.ZipFile(item) as archive:
                for member in archive.infolist():
                    if member.is_dir() or member.file_size > MAX_FILE or Path(member.filename).suffix.lower() not in TEXT_EXT:
                        skipped += 1
                        continue
                    with archive.open(member) as stream:
                        for row in records(member.filename, stream.read(MAX_FILE + 1), kind, f"{item.resolve()}!{member.filename}"):
                            changed += add(db, *row, domain)
        elif item.suffix.lower() in TEXT_EXT and item.stat().st_size <= MAX_FILE:
            for row in records(item.name, item.read_bytes(), kind, str(item.resolve())):
                changed += add(db, *row, domain)
        else:
            skipped += 1
    db.commit()
    return changed, skipped


def search(db: sqlite3.Connection, query: str, limit: int = 10):
    words = Counter(TOKEN.findall(query.lower()))
    if not words:
        return []
    rows = db.execute("SELECT * FROM artifacts").fetchall()
    n = len(rows)
    docs = [Counter(TOKEN.findall(row["body"].lower())) for row in rows]
    df = Counter(word for counts in docs for word in counts)
    scores = []
    for row, counts in zip(rows, docs):
        norm = math.sqrt(sum((c * (1 + math.log((n + 1) / (df[w] + 1)))) ** 2 for w, c in counts.items())) or 1
        score = sum(q * counts[w] * (1 + math.log((n + 1) / (df[w] + 1))) ** 2 for w, q in words.items()) / norm
        if score:
            scores.append((score, dict(row)))
    return sorted(scores, key=lambda pair: pair[0], reverse=True)[:limit]


def gh_json(endpoint: str):
    result = subprocess.run(["gh", "api", endpoint], check=True, capture_output=True, text=True, encoding="utf-8")
    return json.loads(result.stdout)


def ingest_github(db: sqlite3.Connection, owner: str = "otpayt02") -> dict:
    """Import README/spec Markdown from repos visible to the logged-in gh identity."""
    if not re.fullmatch(r"[A-Za-z0-9-]+", owner):
        raise ValueError("invalid owner")
    repos = gh_json("user/repos?per_page=100&affiliation=owner")
    repos = [r for r in repos if r.get("owner", {}).get("login", "").lower() == owner.lower()]
    changed = documents = errors = 0
    for repo in repos:
        full = repo["full_name"]
        try:
            tree = gh_json(f"repos/{full}/git/trees/{repo['default_branch']}?recursive=1")
        except subprocess.CalledProcessError:
            errors += 1
            continue
        paths = [item["path"] for item in tree.get("tree", [])
                 if item.get("type") == "blob" and len(item["path"].split("/")) <= 4
                 and re.search(r"(?:^|/)(?:readme|spec|specification|design|architecture)[^/]*\.md$", item["path"], re.I)]
        for path in paths[:20]:
            try:
                encoded_path = "/".join(quote(part, safe="") for part in path.split("/"))
                payload = gh_json(f"repos/{full}/contents/{encoded_path}?ref={repo['default_branch']}")
                raw = base64.b64decode(payload.get("content", ""))
                if len(raw) > MAX_FILE:
                    continue
                source = payload.get("html_url") or f"https://github.com/{full}/blob/{repo['default_branch']}/{path}"
                for record in records(path, raw, "github", source):
                    changed += add(db, *record, "github")
                    documents += 1
            except (subprocess.CalledProcessError, ValueError):
                errors += 1
        db.commit()
    return {"repos_seen": len(repos), "documents": documents, "changed": changed, "errors": errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    sub = parser.add_subparsers(dest="command", required=True)
    load = sub.add_parser("import")
    load.add_argument("path", type=Path)
    load.add_argument("--kind", required=True, choices=["chatgpt", "perplexity", "takeout", "evernote", "github", "dictated", "drive", "other"])
    load.add_argument("--domain", default="")
    find = sub.add_parser("search")
    find.add_argument("query")
    find.add_argument("--limit", type=int, default=10)
    sub.add_parser("stats")
    github = sub.add_parser("github")
    github.add_argument("--owner", default="otpayt02")
    args = parser.parse_args()
    db = connect(args.db)
    if args.command == "import":
        changed, skipped = ingest_path(db, args.path, args.kind, args.domain)
        print(json.dumps({"changed": changed, "skipped": skipped, "total": db.execute("SELECT COUNT(*) FROM artifacts").fetchone()[0]}))
    elif args.command == "search":
        for score, row in search(db, args.query, args.limit):
            print(json.dumps({"score": round(score, 4), "id": row["id"], "kind": row["kind"], "title": row["title"], "source_uri": row["source_uri"]}))
    elif args.command == "github":
        print(json.dumps(ingest_github(db, args.owner)))
    else:
        print(json.dumps({r[0]: r[1] for r in db.execute("SELECT kind,COUNT(*) FROM artifacts GROUP BY kind")}))


if __name__ == "__main__":
    main()
