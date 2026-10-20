"""Create an editorial visual-change plan from the narration's fixed chapter slots."""
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).parent
script = (ROOT / "script.md").read_text(encoding="utf-8")
manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
heads = list(re.finditer(r"^### CH(\d) — [^\n]*$", script, re.M))
assert len(heads) == 8
body = {}
for i, match in enumerate(heads):
    tail = heads[i+1].start() if i+1 < len(heads) else script.index("\n## Production gate")
    body[f"S{match.group(1)}"] = script[match.end():tail].strip().replace("**", "").replace("*", "")

capture = "assets/captures/"
source = {
    "lost-cause": "https://encyclopediavirginia.org/entries/lost-cause-the/",
    "united-daughters": "https://encyclopediavirginia.org/entries/united-daughters-of-the-confederacy/",
    "atlanta-textbooks": "https://www.atlantahistorycenter.com/blog/spreading-memory-georgia-history-textbooks-and-the-lost-cause/",
    "mississippi-declaration": "https://avalon.law.yale.edu/19th_century/csa_missec.asp",
    "wikipedia-sgaw": "https://en.wikipedia.org/wiki/S%27gaw_Karen_language",
    "google-privacy": "https://research.google/blog/privacy-considerations-in-large-language-models/",
}
def asset_for(scene, beat):
    if scene == "S1" and beat == 0:
        return "assets/face-hook.mp4", "real file", None
    if scene == "S2" and beat in (3, 5, 7):
        key = {3:"lost-cause", 5:"united-daughters", 7:"atlanta-textbooks"}[beat]
        return capture + key + ".png", "real file", source[key]
    if scene == "S4":
        if beat == 1:
            return "assets/graphics/lost-cause-control.png", "labeled graphic", None
        if beat == 4:
            return "assets/graphics/thin-receipt.png", "labeled graphic", None
        if beat == 7:
            return "assets/graphics/karen-counts.png", "labeled graphic", None
        if beat == 3:
            return capture + "mississippi-declaration.png", "real file", source["mississippi-declaration"]
        if beat == 9:
            return capture + "google-privacy.png", "real file", source["google-privacy"]
        return None, "pending real file: two-model screen recording", None
    if scene == "S6" and beat in (4, 5):
        return "assets/koa-tracker-row.png", "labeled graphic rendered from source workbook", None
    if scene == "S7" and beat == 2:
        return capture + "wikipedia-sgaw.png", "real file", source["wikipedia-sgaw"]
    assets = next(s for s in manifest["scenes"] if s["id"] == scene)["assets"]
    eligible = [a for a in assets if a.startswith("assets/")]
    return eligible[min(beat % len(eligible), len(eligible)-1)] if eligible else None, "labeled graphic", None

entries = []
for scene in manifest["scenes"]:
    sid, start, end = scene["id"], scene["start"], scene["end"]
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z“])", re.sub(r"\s+", " ", body[sid]))
    count = math.ceil((end-start)/10)
    for beat in range(count):
        a = round(start + (end-start)*beat/count, 3)
        b = round(start + (end-start)*(beat+1)/count, 3)
        first = math.floor(len(sentences)*beat/count)
        last = math.floor(len(sentences)*(beat+1)/count)
        spoken = " ".join(sentences[first:max(last,first+1)]).strip()
        asset, kind, uri = asset_for(sid, beat)
        entries.append({
            "scene": sid, "start": a, "end": b,
            "spoken_line": spoken,
            "on_screen_text": ("GRAPHIC, NOT A CAPTURE" if "graphic" in kind else "SCREEN RECORDING PENDING" if asset is None else ""),
            "asset_path": asset, "receipt_uri": uri, "asset_kind": kind,
        })

assert entries[0]["start"] == 0 and entries[-1]["end"] == 660
assert all(entries[i]["end"] == entries[i+1]["start"] for i in range(len(entries)-1))
(ROOT / "choreography.json").write_text(json.dumps({
    "video_id": "001-ai-lost-cause",
    "timing_status": "editorial estimate; align to approved recorded VO",
    "source_status": "model behavior paraphrased from owner test summary; S4 recording pending",
    "visual_changes": entries,
}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"{len(entries)} visual changes, 0–660 seconds")
