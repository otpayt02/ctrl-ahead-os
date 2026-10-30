#!/usr/bin/env python3
import json, pathlib, subprocess, sys, re
BASE = pathlib.Path.home()/"workspace/goals/ctrl-ahead-os-ai-video/files/pipeline/data/portfolio/2026-W43/005-model-leaks"
V10 = BASE/"v10"; SEG = V10/"segments"; TXT = V10/"texts"
SEG.mkdir(exist_ok=True); TXT.mkdir(exist_ok=True)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BANNER = BASE/"v9/bannered"
PROOF_BG = V10/"proof-bg.jpg"; ARROW = V10/"outro-arrow.jpg"
sents = json.load(open(BASE/"v9/sentences.json"))
plan = json.load(open(BASE/"v9/plan.json"))
plan_img = {p["sentence"]: p["image"] for p in plan}
# image slugs in bannered order (sorted v8 gen)
SLUGS = ["boxers","posters","detective","doors","scorecard","mirror","trophy-mirror","certainty","scale","hourglass","envelope","paperplane","empty-folder","label-jar","empty-nameplate","moons","crossed","locked-door","two-doors","stamp","searchbar","empty-stage","two-stamps","calendar","heart-bubble","door-closing","copy-machine","boxes","pause","fence","handshake","eraser","questions","fog-clearing","frosted","lab-bench","cloud-ruler","empty-shelf","vanishing","locked-app","treadmill","tier-cake","empty-library","poster","empty-chair","canyon-bridge","not-equal","bricks","ledger-FORBIDDEN"]
def img_path(idx):
    return BANNER/f"img{idx:02d}.jpg"
def slug(idx): return SLUGS[idx]
OVERRIDE = {6:5,7:6,8:7,9:8,13:10,14:12,21:21,22:22,27:29,28:24,29:38,35:34,40:41,44:37,45:44,47:45,52:46,54:40,68:47,74:45}
def base_img(si):
    if si in OVERRIDE: return OVERRIDE[si]
    im = plan_img.get(si,"")
    if im.startswith("img"):
        idx=int(im[3:])
        if idx>=48: idx=47
        return idx
    # proof or other: fallback proportional, never 48
    return min(47, si*47//74)
MOTIONS = ["pan-left","pan-right","slide-left","slide-right","crop-tl","crop-br","pan-up","pan-down"]
counter = [0]
def next_motion():
    m = MOTIONS[counter[0] % len(MOTIONS)]; counter[0]+=1; return m
def motion_filter(m, dur):
    D=f"{dur:.3f}"
    if m=="pan-left": return f"scale=2560:1440,crop=1920:1080:x='640*(1-t/{D})':y=180"
    if m=="pan-right": return f"scale=2560:1440,crop=1920:1080:x='640*(t/{D})':y=180"
    if m=="slide-left": return f"scale=2560:1440,crop=1920:1080:x='640*min(1\\,t/0.35)':y=180"
    if m=="slide-right": return f"scale=2560:1440,crop=1920:1080:x='640*(1-min(1\\,t/0.35))':y=180"
    if m=="crop-tl": return "scale=2560:1440,crop=1920:1080:x=0:y=0"
    if m=="crop-br": return "scale=2560:1440,crop=1920:1080:x=640:y=360"
    if m=="pan-up": return f"scale=1920:1440,crop=1920:1080:x=0:y='360*(1-t/{D})'"
    if m=="pan-down": return f"scale=1920:1440,crop=1920:1080:x=0:y='360*(t/{D})'"
    raise ValueError(m)
txtn=[0]
def txtfile(s):
    txtn[0]+=1; p=TXT/f"t{txtn[0]:04d}.txt"; p.write_text(s); return str(p)
def esc(t): return t.replace("\\","\\\\")
def run(cmd):
    r=subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if r.returncode!=0:
        print("FAILED:", " ".join(cmd)); print(r.stderr[-2000:]); sys.exit(1)
def render_segment(name, image, dur, motion, drawtexts):
    """drawtexts: list of dicts text,fontsize,color,y,enable(alpha optional),box(bool)"""
    if dur < 0.05: return None
    out = SEG/f"{name}.mp4"
    if out.exists(): return str(out)
    vf = [motion_filter(motion, dur)] if motion else ["scale=1920:1080"]
    for dt in drawtexts:
        tf = txtfile(dt["text"])
        box = "box=1:boxcolor=black@0.6:boxborderw=20" if dt.get("box") else "shadowcolor=black:shadowx=3:shadowy=3"
        en = dt.get("enable")
        al = dt.get("alpha")
        s = f"drawtext=fontfile={FONT}:textfile='{tf}':fontsize={dt['fontsize']}:fontcolor={dt['color']}:x=(w-text_w)/2:y={dt['y']}:{box}"
        if en: s += f":enable='{en}'"
        if al: s += f":alpha='{al}'"
        vf.append(s)
    run(["ffmpeg","-y","-v","error","-loop","1","-i",str(image),"-t",f"{dur:.3f}","-vf",",".join(vf),"-r","30","-c:v","libx264","-pix_fmt","yuv420p","-an",str(out)])
    return str(out)
def mono_times(s):
    out=[]; prev=None
    for (a,b) in s["wtimes"]:
        if prev is not None and a < prev: a=prev
        if b<=a: b=a+0.05
        out.append((a,b)); prev=b
    return out
def en_between(a,b): return f"gte(t\\,{a:.3f})*lte(t\\,{b:.3f})"
def alpha_fade(rel): return f"if(lt(t\\,{rel:.3f})\\,0\\,if(lt(t\\,{rel+0.4:.3f})\\,(t-{rel:.3f})/0.4\\,1))"
# ---- lists ----
LISTS = {
 1: [("GPT-7",0,0,15),("Claude REA banned",1,3,21),("Gemini Carbon",4,6,34),("Qwen 4 leaks",7,9,41)],
 3: [("a rumor",0,3,10),("could not find it",4,10,12),("a leak, no product",11,17,34),("real, not shipped",18,24,40)],
 14: [("no document",0,1,12),("no named source",2,4,10),("did not say GPT-7",5,11,16)],
 37: [("no model card",8,10,12),("no price",11,12,13),("no release date",13,15,23),("not confirmed",16,21,16)],
 56: [("GPT-6 Astra",16,17,4),("Claude Opus 5.5",18,20,6),("Gemini 4 Argon",21,27,15),("Qwen 3.8",28,29,43)],
 57: [("a rumor",5,6,10),("a missing model",7,9,21),("a leak",10,11,34),("a training run",13,15,40)],
 61: [("channel selling urgency",4,7,1),("seller selling access",8,11,13),("own desire to be first",12,18,5)],
 68: [("claimed",7,7,10),("sourced",8,8,2),("confirmed",9,9,4),("shipped",10,10,47)],
}
PROOFS = {
 15: ("October 11 — models page", [("GPT-6 Astra","gold"),("GPT-6.1 Sol","gold"),("GPT-6 Luna","gold"),("no Bel","gold")]),
 23: ("October 8 — policy, effective November 12", [("sustained, needless cruelty","gold"),("toward Claude","gold")]),
 24: ("October 12", [("tens of thousands of accounts banned","gold"),("for distillation","white")]),
 36: ("October 9", [("Carbon tested inside Google","white"),("no model card, no price, no date","gold"),("not confirmed","gold")]),
 41: ("September 22", [("Qwen 4 in training","gold"),("no specs, no date","gold")]),
 42: ("October 24", [("Max, Plus, Flash, 27B","white"),("no specs, no date","gold"),("no Qwen 4 weights on Hugging Face","gold")]),
 43: (None, [("Qwen 3.8 Flash-Next","white"),("no Qwen 4 weights on Hugging Face","gold")]),
}
choreo=[]; concat=[]
last_img=None
for si,s in enumerate(sents):
    seg_start=s["start"]; seg_end=sents[si+1]["start"] if si+1<len(sents) else 351.888
    dur=seg_end-seg_start
    wt=mono_times(s)
    if si in PROOFS:
        counter[0]+=1
        header, lines = PROOFS[si]
        dts=[]
        if header:
            dts.append({"text":header,"fontsize":44,"color":"white","y":260,"enable":en_between(0.1, dur),"box":False})
        n=len(lines)
        for k,(ltxt,col) in enumerate(lines):
            rel = 0.5 + k*max(1.0,(dur-1.5)/max(1,n)) if n>1 else 0.5
            fs = 76 if len(ltxt)<=28 else 60
            dts.append({"text":ltxt,"fontsize":fs,"color":"0xFFD700" if col=="gold" else "white","y":420+k*130,"enable":en_between(rel, dur),"alpha":alpha_fade(rel),"box":False})
        out=render_segment(f"s{si:02d}_proof", PROOF_BG, dur, None, dts)
        # proof bg static crop: render_segment with motion None gives scale 1920:1080 (stretched from 1280) - acceptable; note it
        concat.append(out); choreo.append({"sentence":si,"text":s["text"][:80],"motion":"proof-cinematic-reveal (gold-streak bg, text fade-in, no screenshot, no card)","image":"proof-bg (gold streak)","switches":f"proof lines: {[l for l,_ in lines]}"})
        last_img="proof-bg"; continue
    # build subsegments: list or comma
    subs=[]  # (rel_start, rel_end, image_idx, popup_label or None)
    if si in LISTS:
        items=LISTS[si]
        # item intervals in absolute time
        ivals=[]
        for label,wi0,wi1,im in items:
            a=wt[wi0][0]; b=wt[wi1][1]
            ivals.append((label,a,b,im))
        # monotonic clamp
        fixed=[]
        for label,a,b,im in ivals:
            if fixed and a < fixed[-1][2]: a=fixed[-1][2]
            if b<=a: b=a+0.4
            if b>seg_end: b=seg_end
            fixed.append((label,a,b,im))
        cur=seg_start
        bimg=base_img(si)
        for label,a,b,im in fixed:
            if a>cur+0.05: subs.append((cur-seg_start, a-seg_start, bimg, None))
            subs.append((a-seg_start, b-seg_start, im, label))
            cur=b
        if seg_end>cur+0.05: subs.append((cur-seg_start, seg_end-seg_start, bimg, None))
    else:
        cuts=[seg_start]
        for (w,(a,b)) in zip(s["words"], wt):
            if w.rstrip().endswith(",") and b < seg_end-0.3 and b-cuts[-1]>=0.3:
                cuts.append(b)
        cuts.append(seg_end)
        bimg=base_img(si)
        if last_img is not None and isinstance(last_img,int) and bimg==last_img:
            bimg=(bimg+1)%49
            if bimg==48: bimg=47
        for k in range(len(cuts)-1):
            a,b=cuts[k],cuts[k+1]
            if b-a<0.05: continue
            if k==0: im=bimg
            else:
                # alternate: different crop handled by motion, but also rotate image on odd comma cuts
                im=(bimg+2*k)%49
                if im==48: im=47
            subs.append((a-seg_start, b-seg_start, im, None))
    # render subs
    seg_choreo=[]
    for j,(rs,re_,im,label) in enumerate(subs):
        d=re_-rs
        if d<0.05: continue
        m=next_motion()
        dts=[]
        if label:
            dts.append({"text":label,"fontsize":96,"color":"0xFFD700","y":80,"enable":en_between(0, d),"box":True})
        out=render_segment(f"s{si:02d}_c{j}", img_path(im), d, m, dts)
        concat.append(out); seg_choreo.append({"rel":f"{rs:.2f}-{re_:.2f}","image":f"img{im:02d} ({slug(im)})","motion":m,"popup":label})
        last_img=im
    choreo.append({"sentence":si,"text":s["text"],"motion":" / ".join(x["motion"] for x in seg_choreo),"image":seg_choreo[0]["image"] if seg_choreo else "","switches":seg_choreo,"comma_cuts":len(subs)-1,"list":si in LISTS})
    print(f"sentence {si} done, {len(seg_choreo)} subsegments, total concat {len(concat)}", flush=True)
json.dump({"concat":concat,"choreo":choreo}, open(V10/"main_plan.json","w"), indent=1)
print("MAIN SEGMENTS DONE", len(concat))
