import json, re, sys
from difflib import SequenceMatcher
from faster_whisper import WhisperModel

model = WhisperModel("tiny.en", device="cpu", compute_type="int8")
segs = json.load(open('work/segments.json'))

def norm(w):
    return re.sub(r'[^a-z0-9]', '', w.lower())

for n in ['1','2','3','4','5','6']:
    segments, info = model.transcribe(f'assets/audio/vo_s{n}.mp3', word_timestamps=True, language='en')
    wwords = []
    for s in segments:
        for w in (s.words or []):
            wwords.append({'w': w.word.strip(), 'start': w.start, 'end': w.end})
    script_words = segs[n].split()
    a = [norm(w) for w in script_words]
    b = [norm(w['w']) for w in wwords]
    sm = SequenceMatcher(None, a, b, autojunk=False)
    times = [None]*len(script_words)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            for k in range(i2-i1):
                times[i1+k] = (wwords[j1+k]['start'], wwords[j1+k]['end'])
    # fill gaps by interpolation between known anchors
    known = [i for i,t in enumerate(times) if t]
    dur = wwords[-1]['end'] if wwords else 0
    for i in range(len(times)):
        if times[i]: continue
        prev = max([k for k in known if k < i], default=None)
        nxt = min([k for k in known if k > i], default=None)
        ps = times[prev][1] if prev is not None else 0.0
        ne = times[nxt][0] if nxt is not None else dur
        gap = (nxt if nxt is not None else len(times)) - (prev if prev is not None else -1) - 1
        pos = i - (prev if prev is not None else -1)
        st = ps + (ne-ps) * (pos-0.5)/max(gap,1) if gap else ps
        en = ps + (ne-ps) * (pos+0.5)/max(gap,1) if gap else ne
        times[i] = (max(st, ps), max(en, st+0.05))
    out = [{'w': script_words[i], 'start': round(times[i][0],3), 'end': round(times[i][1],3)} for i in range(len(script_words))]
    json.dump(out, open(f'work/words_s{n}.json','w'), indent=1)
    matched = sum(1 for t in times if t)
    print(f's{n}: script {len(script_words)} words, whisper {len(wwords)} words, vo_end {dur:.2f}')
