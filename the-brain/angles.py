"""Create source-linked concept cards from reviewed mining candidates."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from ingest import DEFAULT_DB, connect
from mine import LANES, load_lanes, mine

MODES = ("build-with-me", "teardown", "tutorial", "documentary", "live")
TWISTS = ("philosophical", "reality-check", "unrelated-artifact bridge", "receipts", "confession-opener", "middleman frame")
TIERS = (
    (1, 20, "literal"), (21, 40, "adjacent"), (41, 60, "metaphorical"),
    (61, 80, "cross-domain bridge"), (81, 100, "philosophical unification"),
)


def tier(slider: int) -> str:
    if not 1 <= slider <= 100:
        raise ValueError("slider must be 1..100")
    return next(name for low, high, name in TIERS if low <= slider <= high)


def concept(candidate: dict, mode: str, twists: list[str], slider: int, lane_data: dict) -> dict:
    lane = candidate["target_lane"]
    domain = candidate["source_domain"]
    winning = lane_data.get(lane, [])
    lead = winning[0].get("title") if winning else None
    angle = tier(slider)
    title = f"I used {domain} to test {lane}"
    if angle == "literal":
        title = f"Building a {lane} workflow with receipts from {domain}"
    elif angle == "philosophical unification":
        title = f"What {domain} reveals about who controls {lane}"
    return {
        "title": title, "mode": mode, "angle": angle, "slider": slider, "twists": twists,
        "bridge": candidate["bridge"],
        "bridge_justification": "The source artifact supplies a concrete human practice; the lane supplies an AI workflow. Test the shared mechanism on screen rather than claiming the domains are identical.",
        "artifact_receipts": candidate["evidence"], "target_lane": lane,
        "lane_winner_reference": lead,
        "atypicality": "Use a personal artifact as the visible proof type; verify title/angle differs from the reference before release." if lead else "No winning-format reference available; human review required.",
        "review_required": True,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--slider", type=int, required=True)
    p.add_argument("--mode", choices=MODES, action="append", required=True, help="Repeat for multi-select")
    p.add_argument("--twist", choices=TWISTS, action="append", default=[], help="Repeat for multi-select")
    p.add_argument("--lane", help="Exact lane name; omit to use all lanes")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--db", type=Path, default=DEFAULT_DB)
    p.add_argument("--lanes", type=Path, default=LANES)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    level = tier(args.slider)
    data = json.loads(args.lanes.read_text(encoding="utf-8"))
    lane_data = data.get("lanes", {})
    if args.lane and args.lane not in lane_data:
        p.error(f"Unknown lane: {args.lane}")
    candidates = [c for c in mine(connect(args.db), load_lanes(args.lanes))
                  if c["type"] == "cross-domain-candidate" and (not args.lane or c["target_lane"] == args.lane)]
    cards = [concept(c, mode, args.twist, args.slider, lane_data) for c in candidates for mode in dict.fromkeys(args.mode)]
    result = {"slider_tier": level, "cards": cards[:max(0, args.limit)], "total_candidates": len(cards)}
    body = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(body, encoding="utf-8")
    else:
        print(body)


if __name__ == "__main__":
    main()
