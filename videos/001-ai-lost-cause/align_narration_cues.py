"""Replace editorial cue times with timestamps from approved recorded VO.

Input JSON: {"S1": [{"text": "I", "start_sec": 0.12, "end_sec": 0.3}, ...], ...}
Times are relative to each chapter VO. This script refuses partial matches.
"""
import argparse
import json
import re
from pathlib import Path

root = Path(__file__).parent
parser = argparse.ArgumentParser()
parser.add_argument("word_timings", type=Path, help="Word-level JSON from approved recorded narration")
args = parser.parse_args()
words_by_scene = json.loads(args.word_timings.read_text(encoding="utf-8"))
cue_path = root / "narration-cues.json"
document = json.loads(cue_path.read_text(encoding="utf-8"))
manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
scene_starts = {scene["id"]: scene["start"] for scene in manifest["scenes"]}

def tokens(value):
    return re.findall(r"[\w’']+", value.casefold())

aligned = []
for cue in document["cues"]:
    scene = cue["scene"]
    words = words_by_scene.get(scene)
    if not words:
        raise ValueError(f"No recorded word timestamps for {scene}")
    expected = tokens(cue["spoken_anchor"])
    observed = [tokens(item["text"]) for item in words]
    flat = [token for item in observed for token in item]
    matches = [i for i in range(len(flat) - len(expected) + 1) if flat[i:i+len(expected)] == expected]
    if len(matches) != 1 or any(len(item) != 1 for item in observed):
        raise ValueError(f"Anchor must match exactly once in {scene}: {cue['spoken_anchor']}")
    offset = words[matches[0]]["start_sec"]
    start = round(scene_starts[scene] + offset, 3)
    if start < scene_starts[scene]:
        raise ValueError(f"Word timestamp outside {scene}: {cue['spoken_anchor']}")
    aligned.append({**cue, "start": start, "end": round(start + 4.5, 3), "timing_status": "recorded_word_alignment"})

document["cues"] = aligned
document["timing_status"] = "recorded_word_alignment"
document["note"] = "Aligned to approved recorded chapter VO word timestamps."
cue_path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Aligned {len(aligned)} cues to recorded word timestamps")
