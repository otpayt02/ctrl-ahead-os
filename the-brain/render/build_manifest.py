"""Validate a script and produce a deterministic Remotion render manifest."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def build(script: dict) -> dict:
    for key in ("title", "fps", "width", "height", "scenes", "artifact_receipts"):
        if not script.get(key):
            raise ValueError(f"missing {key}")
    if not script["artifact_receipts"]:
        raise ValueError("source artifact required")
    fps = int(script["fps"])
    if not 24 <= fps <= 60:
        raise ValueError("fps must be 24..60")
    scenes = script["scenes"]
    if not scenes or not scenes[0].get("human_face"):
        raise ValueError("first scene must show a human face")
    if float(scenes[0].get("duration_seconds", 0)) > 3:
        raise ValueError("hook scene exceeds 3 seconds")
    first_text = (scenes[0].get("narration", "") + " " + scenes[0].get("on_screen_text", "")).lower()
    if any(x in first_text for x in ("welcome to", "in this video", "hey guys", "before we begin")):
        raise ValueError("hook contains an intro")
    out = []
    frame = 0
    for i, scene in enumerate(scenes):
        for key in ("duration_seconds", "narration", "visual_prompt", "music_cue"):
            if key not in scene:
                raise ValueError(f"scene {i} missing {key}")
        duration = float(scene["duration_seconds"])
        if not math.isfinite(duration) or duration <= 0:
            raise ValueError(f"scene {i} invalid duration")
        frames = max(1, round(duration * fps))
        out.append({"index": i, "start_frame": frame, "duration_frames": frames,
                    "visual_prompt": scene["visual_prompt"], "narration": scene["narration"],
                    "music_cue": scene["music_cue"], "on_screen_text": scene.get("on_screen_text", ""),
                    "human_face": bool(scene.get("human_face")), "asset_path": None})
        frame += frames
    return {"title": script["title"], "fps": fps, "width": int(script["width"]),
            "height": int(script["height"]), "duration_frames": frame,
            "artifact_receipts": script["artifact_receipts"], "scenes": out}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("script", type=Path)
    p.add_argument("output", type=Path)
    args = p.parse_args()
    manifest = build(json.loads(args.script.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{len(manifest['scenes'])} scenes, {manifest['duration_frames']} frames")


if __name__ == "__main__":
    main()
