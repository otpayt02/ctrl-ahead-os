import re, json, difflib, pathlib, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
base = pathlib.Path.home()/"workspace/goals/ctrl-ahead-os-ai-video/files/pipeline/data/portfolio/2026-W43/005-model-leaks"
outdir = base/"v9"; outdir.mkdir(exist_ok=True)
# --- 1. align script words to whisper words ---
txt = re.sub(r"Narrator:\s*","", (base/"vo2/script.txt").read_text())
sents_raw = re.split(r'(?<=[.!?])\s+', txt.strip())
def norm(w): return re.sub(r'[^a-z0-9]', '', w.lower())
script_words = []
sent_bounds = []  # (start_idx, end_idx_exclusive)
for s in sents_raw:
    ws = s.split(); start=len(script_words); script_words.extend(ws); sent_bounds.append((start, len(script_words)))
wdata = json.load(open(base/"v9_words.json"))
wlist = []
for seg in wdata:
    wlist.extend(seg["words"])
sw_norm = [norm(w) for w in script_words]
ww_norm = [norm(w["word"]) for w in wlist]
sm = difflib.SequenceMatcher(a=sw_norm, b=ww_norm, autojunk=False)
aligned = [None]*len(script_words)  # whisper index or None
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag=="equal":
        for k in range(i2-i1): aligned[i1+k]=j1+k
# fill gaps by interpolation
last=None
for i,a in enumerate(aligned):
    if a is None:
        # use previous whisper word end as start, next as end estimate
        aligned[i]= (aligned[i-1] if i>0 else 0)
times=[]
for i,w in enumerate(script_words):
    wi=aligned[i]
    if wi is not None and wi < len(wlist):
        times.append((wlist[wi]["start"], wlist[wi]["end"]))
    else:
        times.append(times[-1] if times else (0,0.2))
# sentences with real times
sentences=[]
for si,(a,b) in enumerate(sent_bounds):
    sentences.append({"text":sents_raw[si],"start":times[a][0],"end":times[b-1][1],"words":script_words[a:b],"wtimes":times[a:b]})
json.dump(sentences, open(outdir/"sentences.json","w"), indent=1)
print(f"sentences={len(sentences)} script_words={len(script_words)} whisper_words={len(wlist)} matched={sum(1 for a in aligned if a is not None)}")
# --- 2. ASS subtitles: groups of 3-4 words, one event per word, current word expands then settles ---
def fmt(t):
    cs=int(round(t*100)); h=cs//360000; m=(cs%360000)//6000; s=(cs%6000)//100; c=cs%100
    return f"{h}:{m:02d}:{s:02d}.{c:02d}"
ass=["[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: TikTok,DejaVu Sans,88,&H00FFFFFF,&H0000FFFF,&H80000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,2,40,40,110,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"]
for s in sentences:
    ws=s["words"]; wt=s["wtimes"]
    # groups of 4 (3 for last short group handling: keep 3-4)
    groups=[]; i=0
    while i < len(ws):
        n=4 if len(ws)-i>=4 else len(ws)-i
        groups.append((i,i+n)); i+=n
    for (g0,g1) in groups:
        for k in range(g0,g1):
            st, en = wt[k]
            # event ends at next word start, or group end
            ev_end = wt[k+1][0] if k+1 < g1 else wt[g1-1][1]
            if ev_end <= st: ev_end = en
            dur_ms = max(80, int((ev_end-st)*1000))
            parts=[]
            for j in range(g0,g1):
                w=ws[j].replace("{","").replace("}","")
                if j==k:
                    parts.append(f"{{\\fscx135\\fscy135\\1c&H00FFD700&\\t(0,120,\\fscx150\\fscy150)\\t(120,{dur_ms},\\fscx120\\fscy120)}}{w}")
                else:
                    parts.append(f"{{\\fscx82\\fscy82\\1c&HFFFFFFFF&}}{w}")
            ass.append(f"Dialogue: 0,{fmt(st)},{fmt(ev_end)},TikTok,,0,0,0,,{' '.join(parts)}\n")
open(outdir/"tiktok9.ass","w").write("".join(ass))
print("ASS events:", len(ass))
# --- 3. banner images ---
gen = sorted((base/"v8/gen").glob("*.webp"))
print("gen images:", len(gen))
def banner(src, dst, label):
    im = Image.open(src).convert("RGB")
    im = im.resize((1920,1080))
    d = ImageDraw.Draw(im, "RGBA")
    try: f=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
    except Exception: f=ImageFont.load_default()
    d.rectangle([30,30,30+len(label)*17+40,74], fill=(0,0,0,170))
    d.text((50,40), label, fill=(255,215,0), font=f)
    d.rectangle([30,1030,700,1070], fill=(0,0,0,120))
    d.text((50,1038), "AI IMAGE — METAPHOR ONLY, NOT EVIDENCE" if "PROOF" not in label else "RENDERED FROM LIVE PAGE VISIT 2026-10-26 — NOT A LIVE SCREENSHOT", fill=(255,255,255), font=f)
    im.save(dst, quality=90)
bdir = outdir/"bannered"; bdir.mkdir(exist_ok=True)
for i,p in enumerate(gen):
    banner(p, bdir/f"img{i:02d}.jpg", "AI IMAGE")
proof_map = {"openai": base/"v4/proof_openai_card.png", "anthropic": base/"v4/proof_anthropic_card.png", "kie": base/"v4/proof_kie_card.png", "llmcheck": base/"v4/proof_llmcheck_card.png", "macrumors": base/"v4/proof_macrumors_card.png"}
for k,p in proof_map.items():
    if p.exists(): banner(p, bdir/f"proof_{k}.jpg", "PROOF — SOURCE TEXT")
print("bannered done")
# sentence -> image index (proportional, proof override by keywords)
def proof_for(text):
    t=text.lower()
    if "october 11" in t or "models page" in t or "astra" in t and "sol" in t: return "proof_openai"
    if "october 8" in t or "usage policy" in t or "november 12" in t: return "proof_anthropic"
    if "october 12" in t: return "proof_anthropic"
    if "business insider" in t or "october 9" in t: return "proof_kie"
    if "hugging face" in t or "september 22" in t or "alibaba" in t: return "proof_llmcheck"
    return None
plan=[]
for si,s in enumerate(sentences):
    img = proof_for(s["text"]) or f"img{min(48, si*49//74):02d}"
    # comma sub-cuts: split at comma words
    cuts=[s["start"]]
    for (w,(a,b)) in zip(s["words"], s["wtimes"]):
        if w.rstrip().endswith(",") and b < s["end"]-0.3: cuts.append(b)
    cuts.append(s["end"])
    plan.append({"sentence":si,"start":s["start"],"end":s["end"],"image":img,"cuts":cuts,"text":s["text"][:70]})
json.dump(plan, open(outdir/"plan.json","w"), indent=1)
print("plan sentences:", len(plan), "proof sentences:", sum(1 for p in plan if p["image"].startswith("proof")))
