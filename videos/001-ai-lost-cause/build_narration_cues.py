"""Make provisional phrase cues from the editorial choreography.

Each on-screen phrase must be present in the adjacent spoken_line. The
estimated onset is its word position within that beat, never a claim of
alignment to a recording.
"""
import json
import re
from pathlib import Path

root = Path(__file__).parent
beats = json.loads((root / "choreography.json").read_text(encoding="utf-8"))["visual_changes"]
phrases = [
    ("S1", "I read it and I didn't think twice", "I read it and I didn't think twice"),
    ("S1", "two different frontier models", "TWO DIFFERENT FRONTIER MODELS"),
    ("S2", "The Lost Cause offered a flattering story", "THE FLATTERING STORY"),
    ("S2", "A claim has a trail", "A CLAIM HAS A TRAIL"),
    ("S3", "A citation can make a sentence feel inspected", "A CITATION CAN FEEL INSPECTED"),
    ("S3", "Was the source opened", "WAS THE SOURCE OPENED?"),
    ("S3", "That's not what happened", "THAT'S NOT WHAT HAPPENED"),
    ("S4", "Both refused that framing and attached sources", "BOTH REFUSED · BOTH SOURCED"),
    ("S4", "That's the control, not the failure", "THE CONTROL, NOT THE FAILURE"),
    ("S4", "one sentence of its own framing UNCITED", "OWN FRAMING: UNCITED"),
    ("S4", "Two sources were used from excerpts only", "TWO SOURCES: EXCERPT ONLY"),
    ("S4", "did not open Rutherford's original pamphlet", "ORIGINAL PAMPHLET: NOT OPENED"),
    ("S4", "Fluency with links is not the same as opening the page", "LINKS ≠ OPENED PAGES"),
    ("S4", "three speaker counts that do not agree", "THREE COUNTS THAT DISAGREE"),
    ("S4", "general Google Research page about memorization", "GENERAL MEMORIZATION PAGE"),
    ("S4", "not a measurement of S’gaw Karen retention", "NO S'GAW RETENTION MEASUREMENT"),
    ("S5", "I didn't inspect the training data", "TRAINING DATA NOT INSPECTED"),
    ("S5", "A row of links can be helpful", "A LINK STARTS THE CHECK"),
    ("S5", "I will show the disagreement", "LEAVE THE DISAGREEMENT VISIBLE"),
    ("S6", "Store validated training pairs and consent records", "VALIDATED PAIRS + CONSENT RECORDS"),
    ("S6", "Status: In Progress", "ROW 29 · P0 · IN PROGRESS"),
    ("S6", "It is a task, not a shipped system", "A TASK, NOT A SHIPPED SYSTEM"),
    ("S7", "S’gaw Karen is not absent from the internet", "PUBLIC PAGES EXIST"),
    ("S7", "neither answer showed a S’gaw-specific measurement", "RETENTION NOT MEASURED"),
    ("S7", "The loud story now has documents", "THE LOUD STORY HAS DOCUMENTS"),
    ("S7", "no retention receipt in this test", "NO RETENTION RECEIPT"),
    ("S8", "Did I inspect the source", "DID I OPEN THE SOURCE?"),
    ("S8", "Both models passed the first test", "BOTH PASSED THE CONTROL"),
    ("S8", "For now, don't stop at the link. Open the page", "OPEN THE PAGE"),
]

def words(value):
    return re.findall(r"[\w’']+", value.casefold())

cues = []
for scene, anchor, display in phrases:
    match = next((beat for beat in beats if beat["scene"] == scene and anchor.casefold() in beat["spoken_line"].casefold()), None)
    if match is None:
        raise ValueError(f"Missing spoken anchor in one choreography beat: {scene} {anchor}")
    before = match["spoken_line"].casefold().split(anchor.casefold(), 1)[0]
    fraction = len(words(before)) / max(1, len(words(match["spoken_line"])))
    start = round(match["start"] + (match["end"] - match["start"]) * fraction, 3)
    cues.append({
        "scene": scene,
        "start": start,
        "end": round(min(match["end"], start + 4.5), 3),
        "text": display,
        "spoken_anchor": anchor,
        "timing_status": "editorial_estimate",
    })

cues.sort(key=lambda cue: cue["start"])
(root / "narration-cues.json").write_text(json.dumps({
    "video_id": "001-ai-lost-cause",
    "timing_status": "editorial_estimate_no_chapter_vo",
    "note": "Update starts from approved recorded word timestamps before final render.",
    "cues": cues,
}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"{len(cues)} provisional spoken-phrase cues")
