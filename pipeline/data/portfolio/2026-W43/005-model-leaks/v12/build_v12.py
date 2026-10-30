#!/usr/bin/env python3
"""v11: presentation-style re-edit. Static slides, fades, overlay motion only.
No zoompan/pan/crop-motion on base slides. Blue subtitles reused from v10."""
import json, pathlib, subprocess, sys, glob, re
from PIL import Image, ImageDraw, ImageFont

BASE = pathlib.Path.home()/"workspace/goals/ctrl-ahead-os-ai-video/files/pipeline/data/portfolio/2026-W43/005-model-leaks"
V10 = BASE/"v10"; V11 = BASE/"v12"
SLIDES = V11/"slides"; OV = V11/"overlays"; SEG = V11/"segments"; TXT = V11/"texts"
for d in (SLIDES, OV, SEG, TXT): d.mkdir(parents=True, exist_ok=True)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def font(sz):
    try: return ImageFont.truetype(FONT, sz)
    except Exception: return ImageFont.load_default()
def run(cmd):
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if r.returncode != 0:
        print("FAILED:", " ".join(cmd)); print(r.stderr[-3000:]); sys.exit(1)

sents = json.load(open(BASE/"v12/sentences.json"))
# ---- slide grouping: (sentence_start, sentence_end, image_concept, reason, proof_lines or None) ----
# image_concept: v8 gen slug, or 'proof-bg' / 'outro-arrow' (handled specially)
SLIDES_DEF = [
 (0,1,"boxers","Hook: four names as contenders in a ring — the fight the title promises.",None),
 (2,2,"detective","Checked against what companies actually said — detective work, not a retweet.",None),
 (3,4,"scorecard","Four verdicts plus the scorecard itself: a scorecard, not a hype reel.",None),
 (5,8,"mirror","A rumor is a mirror: it shows what you already wanted to be true.",None),
 (9,9,"certainty","Titles sell certainty in a field that has almost none.",None),
 (10,10,"scale","Want the truth more than the headline — a balance, truth against headline.",None),
 (11,11,"hourglass","Hold that for six minutes — discipline is a time discipline.",None),
 (12,12,"moons","GPT-7 Bel: far-off, unreachable, pictured as distant moons.",None),
 (13,13,"envelope","One anonymous post: an envelope with no sender on it.",None),
 (14,14,"empty-folder","No document, no named source — an empty folder where evidence should be.",None),
 (15,15,"proof-bg","PROOF: OpenAI Oct 11 models page, cinematic reveal.",[("October 11 — models page","white"),("GPT-6 Astra","gold"),("GPT-6.1 Sol","gold"),("GPT-6 Luna","gold"),("No Bel","white")]),
 (16,16,"empty-nameplate","No Bel, no GPT-7: a nameplate with no name on it.",None),
 (17,18,"locked-door","An internal model, locked inside the lab — true, but not the same as Bel.",None),
 (19,19,"stamp","Verdict: unverified — stamped, not shipped.",None),
 (20,22,"lab-bench","REA intro: a workshop bench, not a model — REA stands for Reverse Engineer Anything.",None),
 (23,23,"detective","REA repo: an agent inspecting code it is allowed to examine — detective work on code.",None),
 (24,24,"handshake","REA plugs into agents through an MCP server — a handshake between tools.",None),
 (25,26,"poster","REA went viral in mid-October, and was never banned by Anthropic — posters everywhere, no ban.",None),
 (27,27,"two-stamps","Two Anthropic bans, separately, neither is REA — two stamps, two different things.",None),
 (28,29,"proof-bg","PROOF: Anthropic Oct 8 policy + Oct 12 account bans, cinematic reveal, separate from REA.",[("October 8 — usage policy","white"),("effective November 12","gold"),("sustained, needless cruelty","gold"),("October 12 — accounts banned","white"),("tens of thousands","gold"),("for distillation","gold")]),
 (30,30,"crossed","Banned is real, but accounts and a policy, and REA is a repo — the ban crossed out for REA.",None),
 (31,31,"questions","Three different things, one scary title — questions, not panic.",None),
 (32,33,"fence","To ban an account is to draw a boundary — a fence around a community.",None),
 (34,34,"heart-bubble","To ban a behavior is about how we treat a mind — a heart, not a hammer.",None),
 (35,35,"vanishing","To ban a model would be erasing a capability — a figure vanishing.",None),
 (36,36,"label-jar","To mistake a repo for a model is a mislabel — a jar with the wrong label on it.",None),
 (37,38,"questions","The title collapses all of them, and ask whether the thing named is even a model at all.",None),
 (39,40,"fog-clearing","Precision is the difference between fear and understanding — fog clearing.",None),
 (41,42,"frosted","Carbon: closest to real, still not a product — seen through frosted glass, not in your hands.",None),
 (43,43,"proof-bg","PROOF: Business Insider Oct 9 Carbon, cinematic reveal.",[("October 9 — Business Insider","white"),("Carbon tested inside Google","gold"),("No model card","gold"),("No price","gold"),("No date","gold"),("Not confirmed","white")]),
 (44,44,"cloud-ruler","Feels like is not a benchmark — trying to measure a cloud with a ruler.",None),
 (45,45,"door-closing","A checkpoint briefly appeared, then was pulled — a door closing.",None),
 (46,46,"locked-app","Carbon is a leak, not a model you can use — a locked app.",None),
 (47,47,"tier-cake","Fourth, Qwen 4 — tiers stacked like a cake before anything ships.",None),
 (48,50,"proof-bg","PROOF: Alibaba Sep 22 Qwen 4 in training + Oct 24 no weights, cinematic reveal.",[("September 22 — Alibaba","white"),("Qwen 4 in training","gold"),("Max, Plus, Flash, 27B","gold"),("No specs","gold"),("No date","gold"),("October 24 — no Qwen 4 weights","white"),("Qwen 3.8 Flash-Next preview","gold")]),
 (51,51,"treadmill","Real as a project, not shipped — moving, going nowhere yet.",None),
 (52,52,"empty-chair","Qwen 4 Coder does not exist yet — an empty director's chair.",None),
 (53,54,"canyon-bridge","A leak lives in the gap between what a lab knows and what the public may know.",None),
 (55,57,"trophy-mirror","We fill the unknown with the biggest thing we can picture — a trophy in the mirror.",None),
 (58,58,"pause","Let the unknown stay unknown a little longer — pause.",None),
 (59,62,"not-equal","Checkpoint is not a product, feeling is not a benchmark, training is not a release — not equal.",None),
 (63,63,"bricks","Pick from the ones that actually shipped — bricks you can build on, each with its date.",None),
 (64,64,"boxes","The other four names, sorted into four boxes: rumor, repo, leak, training run.",None),
 (65,65,"doors","News versus hype — two doors, and the difference is the whole point.",None),
 (66,67,"searchbar","One last test: ask who benefits — search the motive, not just the claim.",None),
 (68,68,"poster","Channel selling urgency, seller selling access, desire to be first — advertising posters.",None),
 (69,70,"hourglass","Speed is not insight; waiting for confirmation takes time — an hourglass, not a sprint.",None),
 (71,73,"handshake","Do not bet your work, money, or reputation on a rumor — a handshake is a bet.",None),
 (74,77,"scorecard","Four columns as a scorecard — claimed, sourced, confirmed, shipped — no document shown.",None),
 (78,80,"canyon-bridge","The future will arrive whether you hype it or not — the bridge is still there to cross.",None),
]
# list popups: sentence idx -> labels in order (item chunk starts computed from commas)
LIST_LABELS = {
 1: ["GPT-7","REA — a repo, not a model","Gemini Carbon","Qwen 4 leaks"],
 3: ["a rumor","a repo","a leak","a training run"],
 14: ["No document","No named source","did not say GPT-7"],
 44: ["No model card","No price","No release date","Not confirmed"],
 64: ["a rumor","a repo","a leak","a training run"],
 68: ["channel selling urgency","seller selling access","own desire to be first"],
 74: ["claimed","sourced","confirmed","shipped"],
}
CUSTOM_LABELS = {
 22: [(0,"Reverse Engineer Anything — github.com/morluto/rea")],
 24: [(12,"MCP server"),(16,"analysis runs locally")],
 25: [(2,"Viral in mid-October")],
 63: [(16,"GPT-6 Astra"),(18,"Claude Opus 5.5 — Sep 22, 2026"),(30,"Gemini 4 Argon — Sep 30 / Oct 13"),(42,"Qwen 3.8")],
}
def gen_img_path(concept):
    if concept == "proof-bg": return str(V10/"proof-bg.jpg")
    hits = glob.glob(str(BASE/f"v8/gen/*-{concept}-*.webp"))
    # empty-chair file is empty-chair-director
    if not hits and concept == "empty-chair":
        hits = glob.glob(str(BASE/"v8/gen/*-empty-chair-*.webp"))
    if not hits: raise SystemExit(f"no image for {concept}")
    return hits[0]
def slide_jpg(concept, idx):
    out = SLIDES/f"s{idx:02d}_{concept}.jpg"
    if not out.exists():
        run(["ffmpeg","-y","-v","error","-i",gen_img_path(concept),"-vf","scale=1920:1080:force_original_aspect_ratio=disable","-frames:v","1",str(out)])
    return out
def popup_png(text, name):
    out = OV/f"{name}.png"
    if out.exists(): return out
    f = font(64)
    # wrap at ~30 chars
    words = text.split(); lines=[]; cur=""
    for w in words:
        if len(cur)+len(w)+1 > 30 and cur: lines.append(cur); cur=w
        else: cur = (cur+" "+w).strip()
    if cur: lines.append(cur)
    tmp = Image.new("RGBA",(10,10)); d = ImageDraw.Draw(tmp)
    widths = [d.textlength(l, font=f) for l in lines]
    W = int(max(widths))+80; H = len(lines)*84+56
    im = Image.new("RGBA",(W,H),(0,0,0,180)); d = ImageDraw.Draw(im)
    for i,l in enumerate(lines):
        d.text((40,28+i*84), l, fill=(255,215,0), font=f)
    im.save(out); return out
def cutout_png(slide_jpg_path, name, box):
    out = OV/f"{name}.png"
    if out.exists(): return out
    im = Image.open(slide_jpg_path).convert("RGBA").crop(box).resize((700,400))
    d = ImageDraw.Draw(im); d.rectangle([0,0,699,399], outline=(255,215,0), width=8)
    im.save(out); return out
def underline_png(name):
    out = OV/f"{name}.png"
    if not out.exists():
        im = Image.new("RGBA",(900,16),(255,215,0,255)); im.save(out)
    return out
def circle_png(name):
    out = OV/f"{name}.png"
    if not out.exists():
        im = Image.new("RGBA",(400,400),(0,0,0,0)); d = ImageDraw.Draw(im)
        d.ellipse([10,10,390,390], outline=(255,215,0), width=10); im.save(out)
    return out

# timeline: slide start = first sentence start; slide end = next slide first sentence start, last = 351.888
starts = []
for (a,b,_,_,_) in SLIDES_DEF: starts.append(sents[a]["start"])
ends = starts[1:] + [417.48]
# proof slides: no list popups, reveal lines instead (drawtext)
CUT_BOXES = [(510,270,1210,670),(100,100,800,500),(1120,100,1820,500),(100,580,800,980),(610,340,1310,740)]
CUT_POS = [(610,100),(610,200),(610,300),(200,150),(1010,150)]
CIRCLE_POS = [(760,140),(260,180),(1260,180),(760,280)]
UNDER_Y = [620,680,560,640]
def build_slide(idx, sdef, start, end):
    a,b,concept,reason,proof_lines = sdef
    dur = end - start
    assert dur > 0.9, (idx, dur)
    img = slide_jpg(concept, idx)
    inputs = [str(img)]
    filt = [f"[0:v]scale=1920:1080:force_original_aspect_ratio=disable,setsar=1[v0]"]
    cur = "v0"
    if proof_lines is not None:
        # drawtext reveals, then fade at end
        n = len(proof_lines)
        for li,(text,color) in enumerate(proof_lines):
            rel = 0.5 + li * max(1.2, (dur-1.0)/n)
            tf = TXT/f"s{idx:02d}_proof{li}.txt"; tf.write_text(text)
            fc = "0xFFD700" if color=="gold" else "white"
            y = 280 + li*100
            filt.append(f"[{cur}]drawtext=fontfile={FONT}:textfile='{tf}':fontsize=64:fontcolor={fc}:x=(w-text_w)/2:y={y}:shadowcolor=black:shadowx=3:shadowy=3:alpha='if(lt(t,{rel:.3f}),0,if(lt(t,{rel+0.5:.3f}),(t-{rel:.3f})/0.5,1))':enable='between(t,{rel:.3f},{dur:.3f})'[v{idx}p{li}]")
            cur = f"v{idx}p{li}"
    else:
        # overlay events
        events = []  # (rel_time, kind, label_or_None)
        # sentence starts + comma ends
        for si in range(a, b+1):
            s = sents[si]
            events.append((s["start"]-start, "sent", " ".join(s["words"][:4])))
            for ki,(w,(ws,we)) in enumerate(zip(s["words"], s["wtimes"])):
                if w.endswith(","):
                    events.append((we-start, "comma", " ".join(s["words"][ki+1:ki+5])))
        # list popups (forced, replace generic event at same time if present)
        list_events = []
        if a in LIST_LABELS or any(si in LIST_LABELS for si in range(a,b+1)):
            for si in range(a,b+1):
                if si not in LIST_LABELS: continue
                s = sents[si]
                # chunk starts: first word + each word after a comma word
                chunk_starts = [0]
                for k,w in enumerate(s["words"]):
                    if w.endswith(","): chunk_starts.append(k+1)
                labels = LIST_LABELS[si]
                for ci,lab in enumerate(labels):
                    if ci < len(chunk_starts):
                        wi = chunk_starts[ci]
                        list_events.append((s["wtimes"][wi][0]-start, "list", lab))
        events.extend(list_events)
        for si, labs in CUSTOM_LABELS.items():
            if a <= si <= b:
                s = sents[si]
                for wi, lab in labs:
                    if wi < len(s["wtimes"]):
                        events.append((s["wtimes"][wi][0]-start, "list", lab))
        events = sorted(set(events))
        # dedupe by time (keep list popup over generic)
        ded = {}
        for t,kind,lab in events:
            key = round(t,2)
            if key not in ded or kind=="list": ded[key]= (t,kind,lab)
        events = sorted(ded.values())
        # 5s ticks
        filled=[]
        prev=0.0
        for t,kind,lab in events:
            while t - prev > 4.5:
                filled.append((prev+4.5, "tick", None)); prev = prev+4.5
            filled.append((t,kind,lab)); prev=t
        events = filled
        # build overlays
        cycle = ["cutout","underline","circle","popup"]; ci=0
        for ei,(t,kind,lab) in enumerate(events):
            if t < 0: t = 0.0
            if t >= dur: continue
            nxt = events[ei+1][0] if ei+1 < len(events) else dur
            if nxt <= t: nxt = min(dur, t+0.5)
            if kind == "list":
                otype="popup"; label=lab
            elif kind == "sent":
                otype="popup"; label=lab
                # sentence starts: popup only every other sentence to vary; others use cycle
                if ei % 2 == 1: otype=cycle[ci % len(cycle)]; ci+=1
            elif kind=="tick":
                otype=["cutout","underline","circle"][ci % 3]; ci+=1
            else:
                otype=cycle[ci % len(cycle)]; ci+=1
            if otype=="popup":
                # label: for list, exact; for sent, first words; for comma tick, short
                txt = label if label else "key point"
                png = popup_png(txt, f"s{idx:02d}_e{ei:02d}")
                W = Image.open(png).width; H = Image.open(png).height
                inputs.append(str(png))
                oi = len(inputs)-1
                filt.append(f"[{oi}:v]format=rgba[ov{idx}_{ei}]")
                # slide down from top
                filt.append(f"[{cur}][ov{idx}_{ei}]overlay=x=(1920-{W})/2:y='-({H})+({80+H})*min(1,(t-{t:.3f})/0.4)':enable='between(t,{t:.3f},{nxt:.3f})'[v{idx}_{ei}]")
                cur = f"v{idx}_{ei}"
            elif otype=="cutout":
                box = CUT_BOXES[ei % len(CUT_BOXES)]; pos = CUT_POS[ei % len(CUT_POS)]
                png = cutout_png(img, f"s{idx:02d}_e{ei:02d}", box)
                inputs.append(str(png)); oi=len(inputs)-1
                filt.append(f"[{oi}:v]format=rgba[ov{idx}_{ei}]")
                fy = pos[1]
                filt.append(f"[{cur}][ov{idx}_{ei}]overlay=x={pos[0]}:y='{fy}+(1080-{fy})*max(0,1-(t-{t:.3f})/0.5)':enable='between(t,{t:.3f},{nxt:.3f})'[v{idx}_{ei}]")
                cur = f"v{idx}_{ei}"
            elif otype=="underline":
                png = underline_png(f"s{idx:02d}_e{ei:02d}")
                inputs.append(str(png)); oi=len(inputs)-1
                filt.append(f"[{oi}:v]format=rgba[ov{idx}_{ei}]")
                uy = UNDER_Y[ei % len(UNDER_Y)]
                filt.append(f"[{cur}][ov{idx}_{ei}]overlay=x='510-(510+900)*max(0,1-(t-{t:.3f})/0.4)':y={uy}:enable='between(t,{t:.3f},{nxt:.3f})'[v{idx}_{ei}]")
                cur = f"v{idx}_{ei}"
            else: # circle
                png = circle_png(f"s{idx:02d}_e{ei:02d}")
                inputs.append(str(png)); oi=len(inputs)-1
                filt.append(f"[{oi}:v]format=rgba[ov{idx}_{ei}]")
                pos = CIRCLE_POS[ei % len(CIRCLE_POS)]
                filt.append(f"[{cur}][ov{idx}_{ei}]overlay=x={pos[0]}:y='-400+({pos[1]}+400)*min(1,(t-{t:.3f})/0.4)':enable='between(t,{t:.3f},{nxt:.3f})'[v{idx}_{ei}]")
                cur = f"v{idx}_{ei}"
    filt.append(f"[{cur}]fade=t=in:st=0:d=0.4,fade=t=out:st={dur-0.4:.3f}:d=0.4[vout]")
    out = SEG/f"slide{idx:02d}.mp4"
    if out.exists(): return str(out), dur
    cmd = ["ffmpeg","-y","-v","error"]
    for inp in inputs: cmd += ["-loop","1","-i",inp]
    cmd += ["-filter_complex",";".join(filt),"-map","[vout]","-t",f"{dur:.3f}","-r","30","-c:v","libx264","-pix_fmt","yuv420p","-an",str(out)]
    run(cmd)
    return str(out), dur

concat=[]
for idx,sdef in enumerate(SLIDES_DEF):
    path,dur = build_slide(idx, sdef, starts[idx], ends[idx])
    concat.append(path)
    print(f"slide {idx:02d} {sdef[2]} {dur:.2f}s -> {path}", flush=True)
# fade black 0.5s
fade = SEG/"fade.mp4"
if not fade.exists():
    run(["ffmpeg","-y","-v","error","-f","lavfi","-i","color=c=black:s=1920x1080:r=30:d=0.5","-c:v","libx264","-pix_fmt","yuv420p","-an",str(fade)])
concat.append(str(fade))
# outro: static arrow slide 25.92s with popups at beats
arrow = slide_jpg("outro-arrow", 99) if False else str(V10/"outro-arrow.jpg")
# build outro as a slide with popup overlays at 12, 19, 23.5
out_inputs=[arrow]
out_filt=["[0:v]scale=1920:1080:force_original_aspect_ratio=disable,setsar=1[v0]"]
cur="v0"
for ei,(t,txt) in enumerate([(12.0,"SUBSCRIBE"),(19.0,"We don't chase the future. We check it."),(23.5,"Ctrl-Ahead — confirmed, not just claimed.")]):
    png = popup_png(txt, f"outro_e{ei}")
    W=Image.open(png).width; H=Image.open(png).height
    out_inputs.append(str(png)); oi=len(out_inputs)-1
    nxt=[19.0,23.5,25.92][ei]
    out_filt.append(f"[{oi}:v]format=rgba[ov_o{ei}]")
    out_filt.append(f"[{cur}][ov_o{ei}]overlay=x=(1920-{W})/2:y='-({H})+({80+H})*min(1,(t-{t:.3f})/0.4)':enable='between(t,{t:.3f},{nxt:.3f})'[vo{ei}]")
    cur=f"vo{ei}"
out_filt.append(f"[{cur}]fade=t=in:st=0:d=0.4,fade=t=out:st=25.52:d=0.4[vout]")
outro_seg = SEG/"outro.mp4"
if not outro_seg.exists():
    cmd=["ffmpeg","-y","-v","error"]
    for inp in out_inputs: cmd+=["-loop","1","-i",inp]
    cmd+=["-filter_complex",";".join(out_filt),"-map","[vout]","-t","25.92","-r","30","-c:v","libx264","-pix_fmt","yuv420p","-an",str(outro_seg)]
    run(cmd)
concat.append(str(outro_seg))
with open(V11/"concat.txt","w") as f:
    for x in concat: f.write(f"file '{x}'\n")
print("concat segments:", len(concat))
run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",str(V11/"concat.txt"),"-i",str(V11/"audio_full.mp3"),
     "-vf",f"subtitles={V11/'tiktok12_blue.ass'}:force_style='Fontname=DejaVu Sans,Fontsize=88'",
     "-c:v","libx264","-pix_fmt","yuv420p","-r","30","-c:a","aac",str(V11/"v12-render.mp4")])
print("V12 DONE")
