#!/usr/bin/env python3
"""Word-timestamp the v3 VO with faster-whisper, then align Oliver's verbatim script
words onto the whisper timings via difflib (the 005/006 method), so captions show the
script text exactly while gold-highlighting follows the actual speech."""
import difflib, json, pathlib, re, sys
BASE = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(BASE / "build"))
from segments_v3 import SEGMENTS
from faster_whisper import WhisperModel

def norm(w):
    return re.sub(r"[^a-z0-9']", "", w.lower())

model = WhisperModel("base.en", device="cpu", compute_type="int8")
out = {}
for s in SEGMENTS:
    mp3 = str(BASE / "vo" / f"{s['id']}.mp3")
    segs, _ = model.transcribe(mp3, language="en", word_timestamps=True, vad_filter=True)
    ww = []
    for sg in segs:
        for x in (sg.words or []):
            ww.append({"word": x.word.strip(), "start": round(x.start, 3), "end": round(x.end, 3)})
    script_words = s["vo"].split()
    a = [norm(w) for w in script_words]
    b = [norm(w["word"]) for w in ww]
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    starts = [None] * len(script_words)
    ends = [None] * len(script_words)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                starts[i1 + k] = ww[j1 + k]["start"]; ends[i1 + k] = ww[j1 + k]["end"]
    # fill gaps by interpolation between known neighbours
    known = [i for i, v in enumerate(starts) if v is not None]
    for i in range(len(script_words)):
        if starts[i] is None:
            prev = max([k for k in known if k < i], default=None)
            nxt = min([k for k in known if k > i], default=None)
            if prev is not None and nxt is not None:
                frac = (i - prev) / (nxt - prev)
                starts[i] = starts[prev] + frac * (starts[nxt] - starts[prev]); ends[i] = starts[i] + 0.18
            elif prev is not None:
                starts[i] = ends[prev] + 0.05; ends[i] = starts[i] + 0.18
            else:
                starts[i] = 0.0; ends[i] = 0.18
    # enforce monotonicity
    for i in range(1, len(starts)):
        if starts[i] < starts[i - 1]: starts[i] = starts[i - 1] + 0.01
        if ends[i] <= starts[i]: ends[i] = starts[i] + 0.1
    out[s["id"]] = [{"word": script_words[i], "start": round(starts[i], 3), "end": round(ends[i], 3)}
                    for i in range(len(script_words))]
    print(s["id"], "script", len(script_words), "whisper", len(ww), "matched", len(known), flush=True)
json.dump(out, open(BASE / "build" / "words.json", "w"), indent=1)
print("words.json written")
