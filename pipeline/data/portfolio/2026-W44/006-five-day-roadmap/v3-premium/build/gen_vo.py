#!/usr/bin/env python3
"""Generate fresh VO for 006 v3 from Oliver's verbatim script.
Voice: Helio avocado_v2:MAI_03, speed 100 (natural pace — the established 006 settings, same as v1)."""
import json, pathlib, subprocess, sys
BASE = pathlib.Path(__file__).parent.parent  # v3-premium/
sys.path.insert(0, str(BASE / "build"))
from segments_v3 import SEGMENTS

VO = BASE / "vo"; VO.mkdir(exist_ok=True)
durations = {}
for s in SEGMENTS:
    mp3 = VO / f"{s['id']}.mp3"
    (VO / f"{s['id']}.txt").write_text(s["vo"])
    if not mp3.exists():
        r = subprocess.run(["/opt/hatch/bin/tts", "speak", "--voice", "avocado_v2:MAI_03",
                            "--speed", "100", "--language", "en", "--output", str(mp3), "--text-stdin"],
                           input=s["vo"], capture_output=True, text=True, timeout=300)
        if r.returncode != 0:
            print("TTS FAIL", s["id"], r.stdout[-500:], r.stderr[-500:]); sys.exit(1)
        print("tts ok", s["id"], flush=True)
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(mp3)], capture_output=True, text=True)
    durations[s["id"]] = round(float(d.stdout.strip()), 3)
    print(s["id"], durations[s["id"]], flush=True)
json.dump(durations, open(BASE / "build" / "vo_durations.json", "w"), indent=1)
print("TOTAL VO", round(sum(durations.values()), 2))
