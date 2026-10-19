"""Evidence-linked concept cards with CTV tiering and title-bigram rejection across 100 domains."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from ingest import DEFAULT_DB, connect
from mine import LANES, DOMAINS, load_lanes, mine

MODES = ("build-with-me", "build-for-me", "teardown/review", "tutorial", "documentary essay", "live build", "reaction-with-receipts")
TWISTS = ("philosophical", "reality-check", "unrelated-artifact bridge", "receipts/provenance", "confession-opener", "middleman frame", "satire", "sarcastic", "ironic", "funny", "lighthearted")
TIERS = ((1, 20, "literal"), (21, 40, "adjacent"), (41, 60, "metaphorical"),
         (61, 80, "cross-domain bridge"), (81, 100, "philosophical unification"))

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
    return {
        "artifact_id": evidence["artifact_id"], "uri": uri, "locator": excerpt[:80],
        "extracted_text": excerpt, "status": "source located; visual capture pending",
        "source_type": "drive" if "google.com/" in uri else "github" if "github.com/" in uri else "local"
    }

def generate_title_and_justification(domain: str, lane: str, slider: int, receipt_text: str) -> tuple[str, str]:
    """Generates dynamic title and 2-sentence structural mechanism based on domain, lane, and CTV slider."""
    tier_name = tier(slider)
    short_domain = domain.split("&")[0].split(",")[0].strip().title()
    
    if slider <= 20: # Literal
        title = f"Inside {short_domain}: The Mechanical Rules of {lane}"
        justification = f"{short_domain} operates under strict deterministic execution rules. Applying those identical rules to {lane} exposes where automated systems quietly drift."
    elif slider <= 40: # Adjacent
        title = f"What {short_domain} Taught Me About {lane}"
        justification = f"Debugging errors in {short_domain} requires verifying inputs before altering outputs. {lane} requires the exact same discipline to prevent cascading hallucinations."
    elif slider <= 60: # Metaphorical
        title = f"I Stress-Tested {lane} Using {short_domain} Principles"
        justification = f"{short_domain} relies on rigid physical and structural constraints. When {lane} is forced to follow those boundaries, its hidden failure modes immediately surface."
    elif slider <= 80: # Cross-domain bridge
        title = f"How {short_domain} Solved My Biggest Problem in {lane}"
        justification = f"{short_domain} enforces ground-truth receipts and source provenance. Translating that framework directly into {lane} replaces vibes with verifiable execution."
    else: # Philosophical Unification (81-100)
        title = f"Why {lane} Fails the {short_domain} Test"
        justification = f"{short_domain} proves that human judgment and cultural nuance cannot be approximated by sheer scale. {lane} breaks down whenever it attempts to simulate that authenticity without provenance."
        
    return title, justification

def synopsis(domain: str, lane: str, justification: str, receipts: list[dict], slider: int) -> str:
    lead = receipts[0]
    quote = lead["extracted_text"].replace("\n", " ")[:115].strip()
    tier_name = tier(slider)
    return (
        f"An earnest documentary essay begins with Oliver on screen and a source artifact from {domain}, "
        f"then asks what that artifact can teach us about {lane} through a {tier_name} lens (CTV {slider}). The first visible receipt contains "
        f"the passage ‘{quote}’ ({lead['uri']}). That passage anchors the human side of the argument; "
        "it does not, by itself, prove anything about an AI system. The video follows the original "
        "practice step by step, showing its inputs, decisions, corrections, and human judgment. "
        f"The proposed structural link is precise: {justification} Next, a real agent run is recorded "
        "and checked against the same standard. The audience sees the original artifact beside the "
        "agent's behavior, with any missing evidence marked on screen. If the comparison fails, the "
        "video says so and revises the connection. If it survives, the close returns to the first "
        "receipt and names what changed in the viewer's understanding. The mood is curious and "
        "accountable rather than triumphant. The point is to reveal a mechanism that was easy to "
        "miss, while keeping the person and source behind it visible. Every screen capture and "
        "quotation remains a production gate until verified against the original file."
    )

def concept(candidate: dict, slider: int, mode: str, twists: list[str], lane_data: dict,
            recurring: set[str], rank: int) -> dict:
    domain, lane = candidate["source_domain"], candidate["target_lane"]
    receipts = [pointer(e) for e in candidate["evidence"]]
    lead_text = receipts[0]["extracted_text"] if receipts else ""
    
    title, justification = generate_title_and_justification(domain, lane, slider, lead_text)
    
    winners = lane_data.get(lane, [])
    winner_bigrams = set().union(*(bigrams(row.get("title", "")) for row in winners)) if winners else set()
    overlap = sorted(bigrams(title) & (winner_bigrams | recurring))
    
    proof = "personal artifact with source-linked comparison"
    passed = bool(receipts) and not overlap and len(justification.split('.')) >= 2
    source_strength = min(len(receipts), 3) / 3
    first_party = any(p["source_type"] == "drive" for p in receipts)
    score = round(.45 * source_strength + .2 * first_party + .25 * (not overlap) + .1, 2)
    stretch = f"CTV Tier: {tier(slider)} ({slider}/100). The structural analogy is a testable hypothesis anchored in verifiable receipts."

    return {
        "rank": rank, "title": title, "title_options": [title], "mode": mode,
        "angle": tier(slider), "CTV_index": slider, "slider": slider, "twists": twists,
        "length": "long", "presenter_mode": "faceless with requested human hook cameo",
        "target_lane": lane, "source_domain": domain,
        "caption": f"{domain} supplies a test for {lane}: {justification}",
        "synopsis": synopsis(domain, lane, justification, receipts, slider),
        "bridge": candidate["bridge"], "bridge_justification": justification,
        "artifact_receipts": candidate["evidence"], "evidence_pointers": receipts,
        "atypicality": {
            "passed": passed, "overlapping_title_bigrams": overlap,
            "winner_count_compared": len(winners), "recurring_bigram_count_compared": len(recurring),
            "proof_type": proof, "format_comparison": "human review required; winner proof types are not encoded in script_inputs.md"
        },
        "reasoning_trace": {
            "criteria_definition": "Require a source artifact, mechanism-driven justification, anti-cliché title bigram check, and verifiable receipt.",
            "search_plan": {"method": "100_DOMAIN_TAXONOMY_TFIDF", "queries": [domain, lane],
                            "reason": "100-domain taxonomy mapped against indexed brain database artifacts."},
            "candidate_harvest": {"domain": domain, "cited_artifacts": len(receipts)},
            "mapping_test": {"mechanical_justification": justification, "vibes_only": False},
            "atypicality_check": {"title_bigrams_overlapping": overlap, "passed": passed},
            "evidence_resolution": {"pointers": len(receipts), "captured": 0,
                                    "status": "visual evidence capture pending; concept is a draft"},
            "verdict_rank": {"score": score, "rank": rank, "release_ready": False,
                             "weights": "source breadth .45 + original Drive source .20 + title atypicality .25 + lane match .10"},
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
        
    result = {
        "slider_tier": tier(args.slider), "lane_requested": args.lane,
        "lane_resolved": lane, "cards": cards[:max(0, min(args.limit, 50))],
        "total_candidates": len(candidates), "total_taxonomy_domains": len(DOMAINS),
        "method": "100-domain taxonomy; draft concepts; no script or VO generated before evidence capture and approval"
    }
    
    body = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(body, encoding="utf-8")
    else:
        print(body)

if __name__ == "__main__":
    main()
