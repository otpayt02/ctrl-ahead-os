import json, pathlib
BASE = pathlib.Path.home()/"workspace/goals/ctrl-ahead-os-ai-video/files/pipeline/data/portfolio/2026-W43/005-model-leaks"
V10 = BASE/"v10"
def fmt(t):
    cs=int(round(t*100)); h=cs//360000; m=(cs%360000)//6000; s=(cs%6000)//100; c=cs%100
    return f"{h}:{m:02d}:{s:02d}.{c:02d}"
header = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nScaledBorderAndShadow: yes\n\n"
"[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
"Style: TikTok,DejaVu Sans,88,&H00FFFFFF,&H0000FFFF,&H80000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,2,40,40,110,1\n\n"
"[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
raw=[]  # (start, end, group_words, highlight_idx)
# main sentences
sents=json.load(open(BASE/"v9/sentences.json"))
for s in sents:
    ws=s["words"]; wt=s["wtimes"]
    i=0
    while i < len(ws):
        n=4 if len(ws)-i>=4 else len(ws)-i
        gws=ws[i:i+n]; gwt=wt[i:i+n]
        for k in range(n):
            st=gwt[k][0]
            en = gwt[k+1][0] if k+1<n else gwt[k][1]
            if en<=st: en=gwt[k][1] if gwt[k][1]>st else st+0.2
            raw.append((st,en,gws,k))
        i+=n
# outro
script_text = "And hey welcome to Ctrl-Ahead. This is the first video, so if you made it this far, you're early, and early is exactly where you want to be. Next time, we won't just check the hype, we'll test what actually shipped, on a real machine, and show you the receipts. So hit subscribe, and bring your skepticism. Because here, we don't chase the future. We check it. Ctrl-Ahead confirmed, not just claimed."
script_words = script_text.replace("—"," ").split()
wdata=json.load(open(V10/"outro_words.json")); ww=[]
for seg in wdata: ww.extend(seg["words"])
times=[]; prev=0
for i,w in enumerate(script_words):
    a,b = (ww[i]["start"], ww[i]["end"]) if i < len(ww) else (prev+0.2, prev+0.4)
    if a < prev: a=prev
    if b<=a: b=a+0.2
    times.append((a,b)); prev=b
OFFSET=351.888+0.5
i=0
while i < len(script_words):
    n=4 if len(script_words)-i>=4 else len(script_words)-i
    gws=script_words[i:i+n]; gwt=times[i:i+n]
    for k in range(n):
        st=OFFSET+gwt[k][0]
        en = OFFSET+(gwt[k+1][0] if k+1<n else gwt[k][1])
        if en<=st: en=st+0.2
        raw.append((st,en,gws,k))
    i+=n
raw.sort(key=lambda e:e[0])
# de-overlap by slicing same-start runs, truncating to next distinct start
clean=[]
idx=0
while idx < len(raw):
    st=raw[idx][0]
    j=idx
    while j < len(raw) and raw[j][0]==st: j+=1
    run=raw[idx:j]
    nxt = raw[j][0] if j < len(raw) else None
    if len(run)==1:
        s,e,gws,k = run[0]
        if nxt is not None and nxt>s: e=min(e,nxt)
        if e<=s: e=s+0.08
        clean.append((s,e,gws,k))
    else:
        window = (nxt-st) if nxt is not None else max(e for _,e,_,_ in run)-st
        if window<=0: window=0.08*len(run)
        sl=window/len(run)
        for m,(s,e,gws,k) in enumerate(run):
            clean.append((st+m*sl, st+(m+1)*sl, gws, k))
    idx=j
clean.sort(key=lambda e:e[0])
# verify no overlaps (allow end==next start)
bad=sum(1 for a,b in zip(clean,clean[1:]) if b[0] < a[1]-0.001)
print(f"raw={len(raw)} clean={len(clean)} overlapping={bad}")
BLUE="\\1c&H00FF0000&"; WHITE="\\1c&H00FFFFFF&"
out=[header]
for s,e,gws,k in clean:
    dur_ms=int(round((e-s)*1000))
    parts=[]
    for j,w in enumerate(gws):
        w=w.replace("{","").replace("}","")
        if j==k:
            if dur_ms>=160:
                parts.append(f"{{\\fscx135\\fscy135{BLUE}\\t(0,120,\\fscx150\\fscy150)\\t(120,{dur_ms},\\fscx120\\fscy120)}}{w}")
            else:
                parts.append(f"{{\\fscx135\\fscy135{BLUE}}}{w}")
        else:
            parts.append(f"{{\\fscx82\\fscy82{WHITE}}}{w}")
    out.append(f"Dialogue: 0,{fmt(s)},{fmt(e)},TikTok,,0,0,0,,{' '.join(parts)}\n")
open(V10/"tiktok11_blue.ass","w").write("".join(out))
print("wrote tiktok11_blue.ass")
