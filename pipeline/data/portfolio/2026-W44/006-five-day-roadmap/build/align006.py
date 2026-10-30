import json
from faster_whisper import WhisperModel
model = WhisperModel("base.en", device="cpu", compute_type="int8")
segs, info = model.transcribe("vo_full_raw.mp3", language="en", word_timestamps=True, vad_filter=True)
out=[]
for s in segs:
    w=[{"word":x.word,"start":round(x.start,3),"end":round(x.end,3)} for x in (s.words or [])]
    out.append({"start":round(s.start,3),"end":round(s.end,3),"text":s.text.strip(),"words":w})
json.dump(out, open("words.json","w"), indent=1)
print("segments", len(out), "words", sum(len(x["words"]) for x in out))
