"""Source-cited, review-required pattern candidates across life and AI lanes."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from ingest import DEFAULT_DB, connect

ROOT = Path(__file__).resolve().parent
LANES = ROOT.parent / "yt-niche-intel" / "script_inputs.json"
DOMAINS = {
    "piano/improvisation": ("piano", "improvis", "chord", "music"),
    "church music": ("church", "hymn", "worship", "choir"),
    "automotive diagnostics": ("automotive", "car repair", "vehicle", "mechanic", "chevy", "malibu", "obd"),
    "S'gaw Karen preservation": ("s'gaw", "karen", "ocr", "translation"),
    "essays": ("essay", "speech", "writing", "rhetoric"),
}
CONSTANTS = {
    "provenance over portrait": ("source", "provenance", "citation", "receipt"),
    "human-in-the-loop": ("approval", "review", "human", "permission"),
    "free-tier discipline": ("free", "local", "open-source", "no paid"),
    "serving underserved users": ("underserved", "accessibility", "preservation", "community"),
    "middleman instinct": ("bridge", "translate", "connect", "intermediary"),
}
BRIDGES = {
    "piano/improvisation": "Iteration under constraints: compare improvising a variation with steering an AI workflow while preserving a theme.",
    "church music": "Participation design: compare a shared musical cue with how an AI tool invites or excludes human participation.",
    "automotive diagnostics": "Diagnostic sequence: compare symptoms, tests, and repair verification with debugging an AI system.",
    "S'gaw Karen preservation": "Data stewardship: compare OCR correction and permission checks with evaluation of AI outputs for a low-resource language.",
    "essays": "Argument structure: compare thesis, evidence, and revision with a prompt and its verifiable output.",
}


def excerpt(text: str, term: str, width: int = 180) -> str:
    match = re.search(re.escape(term), text, flags=re.I)
    if not match:
        return text[:width].replace("\n", " ")
    start = max(0, match.start() - 50)
    return text[start:start + width].replace("\n", " ")


def load_lanes(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    return list(data.get("lanes", {}))


def mine(db, lanes: list[str]):
    rows = [dict(r) for r in db.execute("SELECT id,title,source_uri,body,kind,domain FROM artifacts")]
    rows.sort(key=lambda r: (0 if r["source_uri"].startswith(("https://docs.google.com/", "https://drive.google.com/")) else 1 if r["kind"] == "github" else 2, r["title"]))
    candidates = []
    for name, terms in CONSTANTS.items():
        evidence = []
        for row in rows:
            term = next((t for t in terms if t in row["body"].lower()), None)
            if term:
                evidence.append({"artifact_id": row["id"], "source_uri": row["source_uri"], "excerpt": excerpt(row["body"], term)})
        if evidence:
            candidates.append({"type": "cross-era-constant", "label": name, "evidence": evidence[:5],
                               "confidence": "low" if len(evidence) < 2 else "medium",
                               "review_required": True, "note": "Era consistency requires dated independent artifacts."})
    for domain, terms in DOMAINS.items():
        evidence = []
        for row in rows:
            hay = f"{row['title']} {row['domain']} {row['source_uri']} {row['body']}".lower()
            if domain == "automotive diagnostics" and "chevy-malibu-2022-lt" not in row["source_uri"].lower() and "automotive" not in f"{row['title']} {row['domain']}".lower():
                continue
            term = next((t for t in terms if t in hay), None)
            if term:
                evidence.append({"artifact_id": row["id"], "source_uri": row["source_uri"], "excerpt": excerpt(row["body"], term)})
        if not evidence:
            continue
        candidates.append({"type": "positive-trait-hypothesis", "label": f"Experience with {domain}",
                           "evidence": evidence[:3], "confidence": "low", "review_required": True,
                           "note": "Artifact mention does not prove skill or personal identity."})
        for lane in lanes:
            candidates.append({"type": "cross-domain-candidate", "source_domain": domain,
                               "target_lane": lane, "bridge": BRIDGES[domain], "evidence": evidence[:3],
                               "confidence": "low", "review_required": True,
                               "note": "Mechanical analogy for creative review, not a proven connection."})
    return candidates


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--db", type=Path, default=DEFAULT_DB)
    p.add_argument("--lanes", type=Path, default=LANES)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    if not args.lanes.exists():
        p.error(f"Lane file missing: {args.lanes}")
    result = {"method": "keyword-supported candidates; all interpretations require review",
              "lanes": load_lanes(args.lanes), "candidates": mine(connect(args.db), load_lanes(args.lanes))}
    body = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(body, encoding="utf-8")
    else:
        print(body)


if __name__ == "__main__":
    main()
