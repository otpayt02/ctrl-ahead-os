import json, pathlib, re
base = pathlib.Path.home()/"workspace/goals/ctrl-ahead-os-ai-video/files/pipeline/data/portfolio/2026-W43/005-model-leaks"
v9 = base/"v9"
sents = json.load(open(v9/"sentences.json"))
def fmt(t):
    cs=int(round(t*100)); h=cs//360000; m=(cs%360000)//6000; s=(cs%6000)//100; c=cs%100
    return f"{h}:{m:02d}:{s:02d}.{c:02d}"
header = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nScaledBorderAndShadow: yes\n\n"
"[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
"Style: TikTok,DejaVu Sans,88,&H0000D7FF&,&H00FFFFFF&,&H80000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,2,40,40,110,1\n\n"
"[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
# Note: PrimaryColour in ASS is BGR: &H0000D7FF& = gold (RGB FF D7 00). Secondary white.
events=[]
for s in sents:
    ws=s["words"]; wt=s["wtimes"]
    # monotonic word times within sentence
    mono=[]
    prev_end=None
    for (a,b) in wt:
        if prev_end is not None and a < prev_end: a=prev_end
        if b <= a: b=a+0.05
        mono.append((a,b)); prev_end=b
    i=0
    while i < len(ws):
        n=4 if len(ws)-i>=4 else len(ws)-i
        gws=ws[i:i+n]; gwt=mono[i:i+n]
        gs=gwt[0][0]; ge=gwt[-1][1]
        if ge<=gs: ge=gs+0.4*n
        # durations, scaled to group length
        raw=[]
        for k in range(n):
            if k<n-1: d=gwt[k+1][0]-gwt[k][0]
            else: d=gwt[k][1]-gwt[k][0]
            raw.append(max(0.02,d))
        tot=sum(raw); target=ge-gs
        durs=[max(2,int(round(r/tot*target*100))) for r in raw]
        text="".join(f"{{\\k{d}}}{w.replace('{','').replace('}','')} " for w,d in zip(gws,durs)).strip()
        events.append((gs,ge,text))
        i+=n
events.sort(key=lambda e:e[0])
# enforce strict non-overlap: end <= next start, drop zero-length
clean=[]
for idx,(gs,ge,text) in enumerate(events):
    if idx+1 < len(events):
        nxt=events[idx+1][0]
        if nxt<=gs: continue  # superseded by a group starting at/before this one
        ge=min(ge,nxt)
    if ge>gs:
        clean.append((gs,ge,text))
print(f"groups={len(events)} clean={len(clean)}")
# verify no overlaps
bad=sum(1 for a,b in zip(clean, clean[1:]) if b[0] < a[1]-0.001)
print("overlapping pairs:", bad)
with open(v9/"tiktok9_fixed.ass","w") as f:
    f.write(header)
    for gs,ge,text in clean:
        f.write(f"Dialogue: 0,{fmt(gs)},{fmt(ge)},TikTok,,0,0,0,,{text}\n")
