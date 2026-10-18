"""Evidence-linked concept cards with CTV tiering and title-bigram rejection."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from ingest import DEFAULT_DB, connect
from mine import LANES, load_lanes, mine

MODES = ("build-with-me", "build-for-me", "teardown/review", "tutorial", "documentary essay", "live build", "reaction-with-receipts")
TWISTS = ("philosophical", "reality-check", "unrelated-artifact bridge", "receipts/provenance", "confession-opener", "middleman frame", "satire", "sarcastic", "ironic", "funny", "lighthearted")
TIERS = ((1, 20, "literal"), (21, 40, "adjacent"), (41, 60, "metaphorical"),
         (61, 80, "cross-domain bridge"), (81, 100, "philosophical unification"))
TITLE_ANGLES = {
    "piano/improvisation": ("The Five-Chord Test for an Agent That Keeps Losing the Theme",
                            "A pianist preserves a theme while changing chords; an AI coding agent must preserve the task goal while revising its plan."),
    "church music": ("Can an Agent Follow a Cue Without Taking Over the Choir?",
                     "A choir uses cues to coordinate independent voices; an AI agent needs explicit handoffs to coordinate tools without replacing human judgment."),
    "automotive diagnostics": ("I Gave a Coding Agent the Mechanic's Fault-Finding Test",
                               "A mechanic tests a symptom before replacing a part; a coding agent should test a failure before rewriting a component."),
    "S'gaw Karen preservation": ("A Language Ledger Exposes the Agent's Missing Sources",
                                   "An OCR correction record links each accepted character to its source; an agent's answer needs the same trace from claim to evidence."),
    "essays": ("My 2021 History Essay Became an Agent Memory Stress Test",
               "A history essay checks a repeated narrative against cited sources; an AI agent must check a fluent summary against the underlying records."),
}
WORD = re.compile(r"[a-z0-9]+")


def tier(slider: int) -> str:
    if not 1 <= slider <= 100:
        raise ValueError("slider must be 1..100")
    return next(label for low, high, label in TIERS if low <= slider <= high)


def bigrams(value: str) -> set[str]:
    words = WORD.findall(value.lower())
    return {f"{a} {b}" for a, b in zip(words, words[1:])}


def recurrent_bigrams(markdown: Path) -> set[str]:
    if not markdown.exists():
        return set()
    text = markdown.read_text(encoding="utf-8")
    section = text.split("## Recurring title bigrams", 1)[-1].split("##", 1)[0]
    return {match.group(1).lower() for match in re.finditer(r"^- ([^:]+): \d+\s*$", section, re.M)}


def pointer(evidence: dict) -> dict:
    uri = evidence["source_uri"]
    excerpt = evidence.get("excerpt", "")
    return {"artifact_id": evidence["artifact_id"], "uri": uri, "locator": excerpt[:80],
            "extracted_text": excerpt, "status": "source located; visual capture pending",
            "source_type": "drive" if "google.com/" in uri else "github" if "github.com/" in uri else "local"}


def concept(candidate: dict, slider: int, mode: str, twists: list[str], lane_data: dict,
            recurring: set[str], rank: int) -> dict:
    domain, lane = candidate["source_domain"], candidate["target_lane"]
    title, justification = TITLE_ANGLES[domain]
    winners = lane_data.get(lane, [])
    winner_bigrams = set().union(*(bigrams(row.get("title", "")) for row in winners)) if winners else set()
    overlap = sorted(bigrams(title) & (winner_bigrams | recurring))
    receipts = [pointer(e) for e in candidate["evidence"]]
    proof = "personal artifact with source-linked comparison"
    passed = bool(receipts) and not overlap and len(justification.split('.')) == 2
    score = round((1 if receipts else 0) * .45 + (1 if not overlap else 0) * .35 + .2, 2)
    stretch = "The structural analogy is a hypothesis for viewer testing, not a claim that the domains are identical."
    return {
        "rank": rank, "title": title, "title_options": [title], "mode": mode,
        "angle": tier(slider), "CTV_index": slider, "slider": slider, "twists": twists,
        "length": "long", "presenter_mode": "faceless with requested human hook cameo",
        "target_lane": lane, "source_domain": domain,
        "caption": f"{domain} supplies a test for {lane}: {justification}",
        "bridge": candidate["bridge"], "bridge_justification": justification,
        "artifact_receipts": candidate["evidence"], "evidence_pointers": receipts,
        "atypicality": {"passed": passed, "overlapping_title_bigrams": overlap,
                         "winner_count_compared": len(winners), "recurring_bigram_count_compared": len(recurring),
                         "proof_type": proof, "format_comparison": "human review required; winner proof types are not encoded in script_inputs.md"},
        "reasoning_trace": {
            "criteria_definition": "Require a source artifact, one sentence naming the shared mechanism, a distinct title-bigram pattern, and a visible test or receipt.",
            "search_plan": {"method": "HEURISTIC", "queries": [domain, lane],
                            "reason": "Source-domain keyword filters over all imported artifacts; private exports are not yet present."},
            "candidate_harvest": {"domain": domain, "cited_artifacts": len(receipts)},
            "mapping_test": {"mechanical_justification": justification, "vibes_only": False,
                             "rejected_candidates": "Other domain candidates without matching source terms were excluded by mine.py."},
            "atypicality_check": {"title_bigrams_overlapping": overlap, "passed": passed},
            "evidence_resolution": {"pointers": len(receipts), "captured": 0,
                                    "status": "visual evidence capture pending; concept is a draft"},
            "verdict_rank": {"score": score, "rank": rank, "release_ready": False},
        },
        "ctv_stretch_note": stretch,
        "review_required": True,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--slider", type=int, required=True)
    p.add_argument("--mode", choices=MODES, action="append", required=True)
    p.add_argument("--twist", choices=TWISTS, action="append", default=[])
    p.add_argument("--lane", default="AI coding agents", help="Exact lane; 'AI agents' aliases to AI coding agents")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--db", type=Path, default=DEFAULT_DB)
    p.add_argument("--lanes", type=Path, default=LANES)
    p.add_argument("--lane-markdown", type=Path, default=LANES.with_suffix('.md'))
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    tier(args.slider)
    data = json.loads(args.lanes.read_text(encoding="utf-8"))
    lane_data = data.get("lanes", {})
    lane = "AI coding agents" if args.lane.lower() == "ai agents" else args.lane
    if lane not in lane_data:
        p.error(f"Unknown lane: {lane}")
    recurring = recurrent_bigrams(args.lane_markdown)
    candidates = [c for c in mine(connect(args.db), load_lanes(args.lanes))
                  if c["type"] == "cross-domain-candidate" and c["target_lane"] == lane]
    cards = [concept(c, args.slider, mode, args.twist, lane_data, recurring, i + 1)
             for i, (c, mode) in enumerate((c, mode) for c in candidates for mode in dict.fromkeys(args.mode))]
    cards = [c for c in cards if c["atypicality"]["passed"]]
    cards.sort(key=lambda c: (-c["reasoning_trace"]["verdict_rank"]["score"], c["rank"]))
    for index, card in enumerate(cards, 1):
        card["rank"] = index
        card["reasoning_trace"]["verdict_rank"]["rank"] = index
    result = {"slider_tier": tier(args.slider), "lane_requested": args.lane,
              "lane_resolved": lane, "cards": cards[:max(0, min(args.limit, 50))],
              "total_candidates": len(candidates), "method": "draft concepts; no script or VO generated before evidence capture and approval"}
    body = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(body, encoding="utf-8")
    else:
        print(body)


if __name__ == "__main__":
    main()
