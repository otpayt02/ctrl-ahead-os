#!/usr/bin/env python3
"""006 v3 PREMIUM — HyperFrames + GSAP project generator.
New motion design: full-bleed generated media, gold sweep reveals, glass panels,
drifting glows (no slow zoom), beat headlines built word-group by word-group,
chip rail with a gold progress spine, single-line gold-word captions, segment
progress bar, and scheduled glimmer sweeps so a visible change lands at least
every ~4.5s of major-event time (caption lines change far more often).
Reads: build/segments_v3.py, build/vo_durations.json, build/words.json.
Writes: compositions/*.html, index.html, build/timeline_v3.json, build/events_v3.json."""
import html, json, pathlib, re, sys
BASE = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(BASE / "build"))
from segments_v3 import SEGMENTS, DAY_CARDS, TAIL, DAYCARD_DUR, OUTRO_DUR

DUR = json.load(open(BASE / "build" / "vo_durations.json"))
WORDS = json.load(open(BASE / "build" / "words.json"))
COMP = BASE / "compositions"; COMP.mkdir(exist_ok=True)

def norm(w): return re.sub(r"[^a-z0-9']", "", w.lower())

def find_trigger(words, phrase, start_idx=0):
    """Find phrase (first up-to-4 words) in aligned script words; return (time, next_idx)."""
    pw = [norm(x) for x in phrase.split() if norm(x)][:4]
    sw = [norm(w["word"]) for w in words]
    for i in range(start_idx, len(sw) - len(pw) + 1):
        if sw[i:i + len(pw)] == pw:
            return words[i]["start"], i + len(pw)
    return None, start_idx

def caption_lines(words):
    lines, cur = [], []
    for w in words:
        cur.append(w)
        endmark = w["word"].rstrip("\"'”").endswith((".", "!", "?"))
        colonmark = w["word"].endswith((":", ";"))
        if len(cur) >= 6 or (endmark and len(cur) >= 3) or (colonmark and len(cur) >= 4):
            lines.append(cur); cur = []
    if cur: lines.append(cur)
    out = []
    for ln in lines:
        out.append({"start": ln[0]["start"], "end": ln[-1]["end"], "words": ln})
    return out

# chip display overrides for the two non-tool segments
CHIP_TXT = {
 "s01": ["every tool in the roadmap, explained", "why you need it", "what breaks if you skip it", "how to actually do it"],
 "s02": ["sets up your tools", "builds what users see", "the logic", "the memory", "you go live"],
}
KIND = {"WHAT IT IS": "what", "WHY YOU NEED IT": "why", "IF YOU SKIP IT": "skip", "HOW": "how"}

CSS = """
#root{position:absolute;inset:0;background:#07090F;overflow:hidden;font-family:Inter,sans-serif;color:#fff}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.glowA{position:absolute;width:900px;height:900px;left:-260px;top:-320px;background:radial-gradient(circle,rgba(255,209,102,.20) 0%,rgba(255,209,102,0) 62%);pointer-events:none}
.glowB{position:absolute;width:1000px;height:1000px;right:-320px;bottom:-420px;background:radial-gradient(circle,rgba(94,234,212,.13) 0%,rgba(94,234,212,0) 62%);pointer-events:none}
.shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(4,6,11,.90) 0%,rgba(4,6,11,.55) 52%,rgba(4,6,11,.12) 82%),linear-gradient(0deg,rgba(4,6,11,.94) 0%,rgba(4,6,11,0) 36%),linear-gradient(180deg,rgba(4,6,11,.5) 0%,rgba(4,6,11,0) 24%)}
.mute{position:absolute;inset:0;background:rgba(16,18,26,.42)}
.sweep{position:absolute;top:-12%;height:124%;width:300px;left:0;background:linear-gradient(100deg,rgba(255,209,102,0) 0%,rgba(255,209,102,.34) 45%,rgba(255,246,214,.75) 50%,rgba(255,209,102,.34) 55%,rgba(255,209,102,0) 100%);transform:skewX(-14deg);opacity:0;pointer-events:none}
.gsweep{position:absolute;top:-12%;height:124%;width:170px;left:0;background:linear-gradient(100deg,rgba(255,209,102,0) 0%,rgba(255,209,102,.16) 50%,rgba(255,209,102,0) 100%);transform:skewX(-14deg);opacity:0;pointer-events:none}
.panel{position:absolute;top:96px;left:56px;width:1080px;padding:38px 46px 34px;background:linear-gradient(135deg,rgba(13,18,30,.82),rgba(9,12,20,.68));border:1px solid rgba(201,168,118,.45);border-radius:22px;box-shadow:0 30px 80px rgba(0,0,0,.5)}
.pill{display:inline-block;padding:10px 22px;border-radius:999px;background:rgba(6,8,13,.85);border:1.5px solid rgba(94,234,212,.55);font-family:"JetBrains Mono",monospace;font-size:20px;font-weight:700;letter-spacing:.18em;color:#5EEAD4}
.title{font-weight:700;letter-spacing:-.02em;line-height:1.02;margin-top:22px;text-shadow:0 4px 30px rgba(0,0,0,.65)}
.yearchip{display:inline-block;margin-left:22px;padding:8px 20px;border-radius:999px;border:2px solid #FFD166;color:#FFD166;font-size:30px;font-weight:700;vertical-align:middle}
.rule{height:7px;width:0;margin-top:24px;background:linear-gradient(90deg,#C9A876,#FFD166,#FF5DA2);border-radius:4px}
.subtitle{font-size:33px;color:rgba(255,255,255,.88);margin-top:16px;font-weight:600}
.stage{position:absolute;left:56px;bottom:216px;width:1170px}
.headline{position:absolute;left:0;bottom:0;width:1170px;font-size:53px;font-weight:700;line-height:1.17;letter-spacing:-.01em;text-shadow:0 3px 24px rgba(0,0,0,.8)}
.headline .wg{display:inline-block}
.headline .bar{position:absolute;left:0;bottom:-16px;height:7px;width:0;background:#5EEAD4;border-radius:4px}
.rail{position:absolute;right:48px;top:150px;width:520px;display:flex;flex-direction:column;gap:15px}
.spine{position:absolute;right:600px;top:170px;width:5px;height:560px;background:rgba(255,255,255,.10);border-radius:3px;overflow:hidden}
.spinefill{width:100%;height:100%;background:linear-gradient(180deg,#FFD166,#C9A876);transform-origin:top;transform:scaleY(0)}
.chip{border-radius:18px;padding:15px 20px 13px;background:rgba(7,10,17,.88);border:2px solid rgba(255,255,255,.25);box-shadow:0 14px 40px rgba(0,0,0,.5)}
.chip .k{font-family:"JetBrains Mono",monospace;font-size:18px;font-weight:700;letter-spacing:.16em;margin-bottom:5px}
.chip .t{font-size:24px;line-height:1.27;color:rgba(255,255,255,.95);font-weight:600}
.chip.what{border-color:#22D3EE}.chip.what .k{color:#22D3EE}
.chip.why{border-color:#A78BFA}.chip.why .k{color:#A78BFA}
.chip.skip{border-color:#F87171}.chip.skip .k{color:#F87171}
.chip.how{border-color:#4ADE80}.chip.how .k{color:#4ADE80}
.chip.gold{border-color:#FFD166}.chip.gold .k{color:#FFD166}
.laterbadge{position:absolute;top:44px;right:48px;padding:12px 26px;border-radius:12px;background:#B91C1C;color:#fff;font-family:"JetBrains Mono",monospace;font-weight:700;letter-spacing:.22em;font-size:24px;transform:rotate(3deg);z-index:5}
.prog{position:absolute;left:56px;right:56px;bottom:132px;height:5px;background:rgba(255,255,255,.13);border-radius:3px;overflow:hidden}
.progfill{height:100%;width:100%;background:linear-gradient(90deg,#C9A876,#FFD166);transform-origin:left;transform:scaleX(0)}
.caps{position:absolute;left:0;right:0;bottom:50px;display:flex;justify-content:center}
.cap{background:rgba(0,0,0,.8);padding:12px 28px;border-radius:10px;font-size:39px;font-weight:600;text-align:center;max-width:1580px;box-shadow:0 10px 34px rgba(0,0,0,.45)}
.cap span{color:#fff}
.bigflash{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:118px;font-weight:700;letter-spacing:-.01em;color:#FFD166;text-shadow:0 8px 54px rgba(0,0,0,.85);opacity:0}
.node{position:absolute;width:24px;height:24px;border-radius:50%;background:#1B2436;border:3px solid rgba(255,255,255,.28)}
.daycard{position:absolute;inset:0;background:radial-gradient(1150px 640px at 50% 42%,#1B2436 0%,#07090F 72%);display:flex;flex-direction:column;align-items:center;justify-content:center;overflow:hidden}
.daycard .d1{font-family:"JetBrains Mono",monospace;letter-spacing:.34em;color:#5EEAD4;font-size:31px;font-weight:700}
.daycard .d2{font-size:158px;font-weight:700;letter-spacing:-.02em;margin-top:10px}
.daycard .d3{font-size:43px;color:rgba(255,255,255,.82);font-weight:600;margin-top:8px}
.daycard .rule2{width:0;height:8px;background:linear-gradient(90deg,#FFD166,#FF5DA2);border-radius:4px;margin-top:36px}
.outro{position:absolute;inset:0;background:#07090F;display:flex;flex-direction:column;align-items:center;justify-content:center;overflow:hidden}
.outro img{width:740px;height:416px;object-fit:cover;border-radius:24px;box-shadow:0 0 130px rgba(255,209,102,.28)}
.outro .o0{font-family:"JetBrains Mono",monospace;letter-spacing:.3em;color:#5EEAD4;font-size:26px;font-weight:700;margin-top:34px}
.outro .o1{font-size:66px;font-weight:700;margin-top:14px;letter-spacing:-.01em}
.outro .o2{font-size:35px;color:rgba(255,255,255,.8);margin-top:12px;font-weight:600}
.outro .o3{font-size:29px;color:#FFD166;margin-top:10px;font-weight:700;letter-spacing:.04em}
.subpill{margin-top:30px;padding:16px 46px;border-radius:999px;background:#E11D48;font-size:32px;font-weight:700;letter-spacing:.14em;box-shadow:0 14px 44px rgba(225,29,72,.4)}
"""

def esc(t): return html.escape(t, quote=True)

def title_size(t):
    n = len(t)
    return 100 if n <= 6 else 88 if n <= 12 else 74 if n <= 18 else 62

def word_groups(text, per=3):
    ws = text.split()
    return [" ".join(ws[i:i + per]) for i in range(0, len(ws), per)]

def build_segment(s):
    sid = s["id"]; words = WORDS[sid]
    dur = round(DUR[sid] + TAIL, 3)
    # chips with triggers (sequential search keeps narration order)
    chips = []; idx = 0
    for ci, (label, txt) in enumerate(s["chips"]):
        disp = CHIP_TXT.get(sid, [None] * len(s["chips"]))[ci] or txt
        trig_src = txt
        t, idx2 = find_trigger(words, trig_src, idx)
        if t is None: t, idx2 = find_trigger(words, disp, 0)
        if t is None: t = 0.45 + ci * 3.0
        else: idx = idx2
        kind = KIND.get(label, "gold")
        chips.append({"label": label, "text": disp, "t": round(t, 2), "kind": kind})
    # headlines: subtitle first, then one per chip
    headlines = [{"text": s["subtitle"], "t": 0.45}]
    for c in chips:
        headlines.append({"text": c["text"], "t": c["t"]})
    # caption lines
    lines = caption_lines(words)
    # major events + sweep insertion (gap > 4.6s between major events)
    major = sorted(set([0.0] + [h["t"] for h in headlines] + [c["t"] for c in chips]))
    sweeps = []
    pts = major + [dur]
    for a, b in zip(pts, pts[1:]):
        t = a + 4.4
        while t < b - 0.3:
            sweeps.append(round(t, 2)); t += 4.4
    allevents = sorted(set(major + [round(l["start"], 2) for l in lines] + sweeps))
    gaps = [round(b - a, 2) for a, b in zip(allevents, allevents[1:] + [dur])]
    maxgap = max(gaps) if gaps else dur

    el = []   # html elements
    js = []   # gsap lines
    n = [0]
    def nid():
        n[0] += 1; return f"el-{sid}-{n[0]}"
    # background: video (first ~10s) over still, or still only
    img_id = nid()
    el.append(f'<img id="{img_id}" class="clip bg" data-start="0" data-duration="{dur}" src="assets/gen/{s["img"]}">')
    if s.get("vid"):
        vid_id = nid()
        el.append(f'<video id="{vid_id}" class="clip bg" data-start="0" data-duration="{dur}" src="assets/gen/{s["vid"]}" muted playsinline></video>')
        js.append(f'tl.to("#{vid_id}",{{opacity:0,duration:0.9,ease:"power2.inOut"}},9.3);')
    if s.get("vids"):
        # HOOK MONTAGE: quick cuts at segment thirds (per the script's stage direction), glimmer at each cut
        third = dur / 3
        for vi, vf in enumerate(s["vids"]):
            vstart = round(vi * third, 2)
            vdur = round(third if vi < 2 else dur - vstart, 2)
            vid_id = nid()
            el.append(f'<video id="{vid_id}" class="clip bg" data-start="{vstart}" data-duration="{vdur}" src="assets/gen/{vf}" muted playsinline></video>')
            if vi > 0:
                gw = nid(); el.append(f'<div id="{gw}" class="clip gsweep" data-start="{vstart}" data-duration="0.9"></div>')
                js.append(f'tl.fromTo("#{gw}",{{x:-460,opacity:1}},{{x:2250,opacity:1,duration:.7,ease:"power2.inOut"}},{vstart});')
                js.append(f'tl.to("#{gw}",{{opacity:0,duration:.12}},{round(vstart + 0.72, 2)});')
    for g in ("glowA", "glowB"):
        gid = nid()
        el.append(f'<div id="{gid}" class="clip {g}" data-start="0" data-duration="{dur}"></div>')
        drift = {"glowA": ("x:70,y:44"), "glowB": ("x:-64,y:-40")}[g]
        js.append(f'tl.fromTo("#{gid}",{{x:0,y:0}},{{{drift},duration:{dur},ease:"sine.inOut"}},0);')
    sh = nid(); el.append(f'<div id="{sh}" class="clip shade" data-start="0" data-duration="{dur}"></div>')
    if s.get("later"):
        mu = nid(); el.append(f'<div id="{mu}" class="clip mute" data-start="0" data-duration="{dur}"></div>')
        lb = nid(); el.append(f'<div id="{lb}" class="clip" data-start="0.5" data-duration="{dur - 0.5}"><div class="laterbadge">LATER</div></div>')
        js.append(f'tl.fromTo("#{lb}",{{scale:2.1,opacity:0,rotation:9}},{{scale:1,opacity:1,rotation:0,duration:.38,ease:"back.out(2)"}},0.5);')
    # entry gold sweep
    sw = nid(); el.append(f'<div id="{sw}" class="clip sweep" data-start="0" data-duration="1.3"></div>')
    js.append(f'tl.fromTo("#{sw}",{{x:-560,opacity:1}},{{x:2300,opacity:1,duration:.95,ease:"power3.inOut"}},0.02);')
    js.append(f'tl.to("#{sw}",{{opacity:0,duration:.2}},1.0);')
    for st in sweeps:
        gw = nid(); el.append(f'<div id="{gw}" class="clip gsweep" data-start="{st}" data-duration="1.1"></div>')
        js.append(f'tl.fromTo("#{gw}",{{x:-460,opacity:1}},{{x:2250,opacity:1,duration:.85,ease:"power2.inOut"}},{st});')
        js.append(f'tl.to("#{gw}",{{opacity:0,duration:.15}},{round(st + 0.88, 2)});')
    # panel
    year = f'<span class="yearchip">{esc(s["year"])}</span>' if s["year"] else ""
    pn = nid()
    el.append(f'<div id="{pn}" class="clip" data-start="0" data-duration="{dur}"><div class="panel" id="panel-{sid}">'
              f'<span class="pill" id="pill-{sid}">{esc(s["scene"])}</span>'
              f'<div class="title" style="font-size:{title_size(s["title"])}px">{esc(s["title"])}{year}</div>'
              f'<div class="rule" id="rule-{sid}"></div>'
              f'<div class="subtitle">{esc(s["subtitle"])}</div></div></div>')
    js.append(f'tl.fromTo("#panel-{sid}",{{y:56,opacity:0}},{{y:0,opacity:1,duration:.6,ease:"power3.out"}},0.12);')
    js.append(f'tl.to("#rule-{sid}",{{width:"100%",duration:.7,ease:"power2.inOut"}},0.5);')
    # headlines
    for hi, h in enumerate(headlines):
        hend = (headlines[hi + 1]["t"] if hi + 1 < len(headlines) else dur)
        hd = round(max(0.6, hend - h["t"]), 2)
        groups = word_groups(h["text"])
        spans = " ".join(f'<span class="wg" id="hg-{sid}-{hi}-{gi}">{esc(g)}</span>' for gi, g in enumerate(groups))
        hid = nid()
        el.append(f'<div id="{hid}" class="clip stage" data-start="{h["t"]}" data-duration="{hd}"><div class="headline">{spans}<div class="bar" id="hbar-{sid}-{hi}"></div></div></div>')
        for gi in range(len(groups)):
            js.append(f'tl.fromTo("#hg-{sid}-{hi}-{gi}",{{y:38,opacity:0}},{{y:0,opacity:1,duration:.38,ease:"power3.out"}},{round(h["t"] + gi * 0.09, 2)});')
        js.append(f'tl.to("#hbar-{sid}-{hi}",{{width:"72%",duration:.5,ease:"power2.out"}},{round(h["t"] + 0.15, 2)});')
        if hi + 1 < len(headlines):
            js.append(f'tl.to("#{hid}",{{opacity:0,y:-16,duration:.25,ease:"power2.in"}},{round(hend - 0.27, 2)});')
    # spine + chips rail
    sp = nid()
    el.append(f'<div id="{sp}" class="clip spine" data-start="0" data-duration="{dur}"><div class="spinefill" id="spine-{sid}"></div></div>')
    rail = [f'<div class="rail">']
    for ci, c in enumerate(chips):
        cd = round(dur - c["t"], 2)
        rail.append(f'<div id="{nid()}" class="clip" data-start="{c["t"]}" data-duration="{cd}"><div class="chip {c["kind"]}" id="chip-{sid}-{ci}"><div class="k">{esc(c["label"])}</div><div class="t">{esc(c["text"])}</div></div></div>')
        js.append(f'tl.fromTo("#chip-{sid}-{ci}",{{scale:1.6,opacity:0,rotation:-3.5}},{{scale:1,opacity:1,rotation:0,duration:.42,ease:"back.out(2.1)"}},{c["t"]});')
        js.append(f'tl.to("#spine-{sid}",{{scaleY:{round((ci + 1) / len(chips), 3)},duration:.45,ease:"power2.out"}},{c["t"]});')
    rail.append('</div>')
    el.append("".join(rail))
    # segment motifs: checkpoint nodes for Git + Close route
    if sid in ("s03_1", "s08"):
        for ni in range(5):
            nt = round(1.1 + ni * 1.55, 2)
            nd = nid()
            el.append(f'<div id="{nd}" class="clip" data-start="{nt}" data-duration="{round(dur - nt, 2)}"><div class="node" id="node-{sid}-{ni}" style="left:{120 + ni * 118}px;bottom:158px"></div></div>')
            js.append(f'tl.to("#node-{sid}-{ni}",{{backgroundColor:"#FFD166",borderColor:"#FFD166",boxShadow:"0 0 32px rgba(255,209,102,.9)",duration:.3}},{nt});')
    # hook big flashes
    if sid == "s01":
        for phrase, label in (("five days", "FIVE DAYS"), ("It's real", "IT'S REAL")):
            t, _ = find_trigger(words, phrase, 0)
            if t is not None:
                bf = nid()
                el.append(f'<div id="{bf}" class="clip" data-start="{round(t, 2)}" data-duration="1.7"><div class="bigflash" id="flash-{label.replace(" ", "-")}">{label}</div></div>')
                js.append(f'tl.fromTo("#flash-{label.replace(" ", "-")}",{{scale:1.7,opacity:0}},{{scale:1,opacity:1,duration:.34,ease:"back.out(1.9)"}},{round(t, 2)});')
                js.append(f'tl.to("#flash-{label.replace(" ", "-")}",{{opacity:0,duration:.3}},{round(t + 1.32, 2)});')
    # progress bar
    pg = nid()
    el.append(f'<div id="{pg}" class="clip prog" data-start="0" data-duration="{dur}"><div class="progfill" id="prog-{sid}"></div></div>')
    js.append(f'tl.to("#prog-{sid}",{{scaleX:1,duration:{dur},ease:"none"}},0);')
    # captions
    for li, ln in enumerate(lines):
        cend = (lines[li + 1]["start"] if li + 1 < len(lines) else dur)
        cdur = round(max(0.3, min(cend, dur) - ln["start"]), 2)
        spans = " ".join(f'<span id="w-{sid}-{li}-{wi}">{esc(w["word"])}</span>' for wi, w in enumerate(ln["words"]))
        cid = nid()
        el.append(f'<div id="{cid}" class="clip caps" data-start="{round(ln["start"], 2)}" data-duration="{cdur}"><div class="cap" id="cap-{sid}-{li}">{spans}</div></div>')
        js.append(f'tl.fromTo("#cap-{sid}-{li}",{{opacity:0}},{{opacity:1,duration:.07,ease:"none"}},{round(ln["start"], 2)});')
        for wi, w in enumerate(ln["words"]):
            js.append(f'tl.to("#w-{sid}-{li}-{wi}",{{color:"#FFD166",duration:.05,ease:"none"}},{round(w["start"], 2)});')
    body = "\n".join(el)
    script = "\n".join(js)
    doc = f"""<template>
<link rel="stylesheet" href="css/theme.css">
<style>{CSS}</style>
<div id="root" data-composition-id="{sid}" data-start="0" data-duration="{dur}" data-width="1920" data-height="1080">
{body}
</div>
<script src="assets/js/gsap.min.js"></script>
<script>
window.__timelines = window.__timelines || {{}};
(function(){{
  var tl = gsap.timeline({{ paused: true }});
{script}
  window.__timelines["{sid}"] = tl;
}})();
</script>
</template>
"""
    (COMP / f"{sid}.html").write_text(doc)
    return {"id": sid, "dur": dur, "chips": chips, "headlines": headlines,
            "caption_lines": len(lines), "sweeps": sweeps, "max_gap_major": round(max([b - a for a, b in zip(major, major[1:] + [dur])]), 2),
            "max_gap_all": maxgap}

def build_daycard(key, kick, big, sub):
    cid = {"s03_1": "day1", "s04_1": "day2", "s05_1": "day3", "s06_1": "day4", "s07_1": "day5"}[key]
    doc = f"""<template>
<link rel="stylesheet" href="css/theme.css">
<style>{CSS}</style>
<div id="root" data-composition-id="{cid}" data-start="0" data-duration="{DAYCARD_DUR}" data-width="1920" data-height="1080">
<div class="daycard">
<div class="glowA" id="{cid}-g"></div>
<div class="d1" id="{cid}-a">{esc(kick)}</div>
<div class="d2" id="{cid}-b">{esc(big)}</div>
<div class="d3" id="{cid}-c">{esc(sub)}</div>
<div class="rule2" id="{cid}-r"></div>
<div class="sweep" id="{cid}-s"></div>
</div>
</div>
<script src="assets/js/gsap.min.js"></script>
<script>
window.__timelines = window.__timelines || {{}};
(function(){{
  var tl = gsap.timeline({{ paused: true }});
  tl.fromTo("#{cid}-a",{{opacity:0,y:-26}},{{opacity:1,y:0,duration:.3,ease:"power3.out"}},0.05);
  tl.fromTo("#{cid}-b",{{scale:1.55,opacity:0}},{{scale:1,opacity:1,duration:.44,ease:"back.out(1.8)"}},0.16);
  tl.fromTo("#{cid}-c",{{opacity:0,y:18}},{{opacity:1,y:0,duration:.3,ease:"power3.out"}},0.48);
  tl.to("#{cid}-r",{{width:560,duration:.5,ease:"power2.inOut"}},0.55);
  tl.fromTo("#{cid}-s",{{x:-560,opacity:1}},{{x:2300,opacity:1,duration:.8,ease:"power3.inOut"}},0.62);
  tl.to("#{cid}-s",{{opacity:0,duration:.15}},1.42);
  window.__timelines["{cid}"] = tl;
}})();
</script>
</template>
"""
    (COMP / f"{cid}.html").write_text(doc)
    return {"id": cid, "dur": DAYCARD_DUR}

def build_outro():
    doc = f"""<template>
<link rel="stylesheet" href="css/theme.css">
<style>{CSS}</style>
<div id="root" data-composition-id="outro" data-start="0" data-duration="{OUTRO_DUR}" data-width="1920" data-height="1080">
<div class="outro">
<div class="glowA" id="out-g"></div>
<img id="out-img" src="assets/gen/img-outro-arrow.webp">
<div class="o0" id="out-0">NEW HERE? WELCOME</div>
<div class="o1" id="out-1">AHEAD OF RUSH AI</div>
<div class="o2" id="out-2">We don't chase the future. We check it.</div>
<div class="o3" id="out-3">CONFIRMED, NOT JUST CLAIMED</div>
<div class="subpill" id="out-4">SUBSCRIBE</div>
<div class="sweep" id="out-s"></div>
</div>
</div>
<script src="assets/js/gsap.min.js"></script>
<script>
window.__timelines = window.__timelines || {{}};
(function(){{
  var tl = gsap.timeline({{ paused: true }});
  tl.fromTo("#out-img",{{scale:1.24,opacity:0}},{{scale:1,opacity:1,duration:.7,ease:"back.out(1.5)"}},0.15);
  tl.fromTo("#out-0",{{opacity:0,y:22}},{{opacity:1,y:0,duration:.4,ease:"power3.out"}},0.75);
  tl.fromTo("#out-1",{{opacity:0,y:26}},{{opacity:1,y:0,duration:.45,ease:"power3.out"}},1.0);
  tl.fromTo("#out-2",{{opacity:0}},{{opacity:1,duration:.5}},1.65);
  tl.fromTo("#out-3",{{opacity:0}},{{opacity:1,duration:.5}},2.25);
  tl.fromTo("#out-4",{{scale:.4,opacity:0}},{{scale:1,opacity:1,duration:.5,ease:"back.out(2.4)"}},3.1);
  tl.fromTo("#out-s",{{x:-560,opacity:1}},{{x:2300,opacity:1,duration:.95,ease:"power3.inOut"}},5.6);
  tl.to("#out-s",{{opacity:0,duration:.2}},6.6);
  window.__timelines["outro"] = tl;
}})();
</script>
</template>
"""
    (COMP / "outro.html").write_text(doc)
    return {"id": "outro", "dur": OUTRO_DUR}

def main():
    (BASE / "css").mkdir(exist_ok=True)
    (BASE / "css" / "theme.css").write_text(
        '@font-face{font-family:"Inter";src:url("../assets/fonts/Inter-Regular.woff2") format("woff2");font-weight:400}\n'
        '@font-face{font-family:"Inter";src:url("../assets/fonts/Inter-SemiBold.woff2") format("woff2");font-weight:600}\n'
        '@font-face{font-family:"Inter";src:url("../assets/fonts/Inter-Bold.woff2") format("woff2");font-weight:700}\n'
        '@font-face{font-family:"JetBrains Mono";src:url("../assets/fonts/JetBrainsMono-Regular.woff2") format("woff2");font-weight:400}\n'
        '@font-face{font-family:"JetBrains Mono";src:url("../assets/fonts/JetBrainsMono-Bold.woff2") format("woff2");font-weight:700}\n'
        '*{margin:0;padding:0;box-sizing:border-box}\n')
    (BASE / "hyperframes.json").write_text(json.dumps({"$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
        "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"}, "media": {"autoProxy": True}}, indent=1))
    (BASE / "package.json").write_text(json.dumps({"name": "ctrl006v3", "private": True, "type": "module",
        "scripts": {"check": "npx --yes hyperframes@0.8.210 check", "render": "npx --yes hyperframes@0.8.210 render"}}, indent=1))
    (BASE / "meta.json").write_text(json.dumps({"id": "ctrl006v3", "name": "Ctrl-Ahead 006 v3 — Premium (Ahead of Rush AI)"}))

    timeline, events, t = [], {}, 0.0
    for s in SEGMENTS:
        if s["id"] in DAY_CARDS:
            dc = build_daycard(s["id"], *DAY_CARDS[s["id"]])
            timeline.append({**dc, "start": round(t, 3), "kind": "daycard"}); t += dc["dur"]
        info = build_segment(s)
        timeline.append({"id": s["id"], "start": round(t, 3), "dur": info["dur"], "kind": "segment"})
        events[s["id"]] = info; t += info["dur"]
    oc = build_outro()
    timeline.append({**oc, "start": round(t, 3), "kind": "outro"}); t += oc["dur"]
    total = round(t, 3)
    json.dump({"timeline": timeline, "total": total,
               "seg_start": {x["id"]: x["start"] for x in timeline}},
              open(BASE / "build" / "timeline_v3.json", "w"), indent=1)
    json.dump(events, open(BASE / "build" / "events_v3.json", "w"), indent=1)
    hosts = "\n".join(
        f'<div id="host-{x["id"]}" data-composition-id="{x["id"]}" data-composition-src="compositions/{x["id"]}.html" '
        f'data-start="{x["start"]}" data-duration="{x["dur"]}" data-track-index="0" data-track-kind="graphics" data-width="1920" data-height="1080"></div>'
        for x in timeline)
    (BASE / "index.html").write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=1920, height=1080">
<script src="assets/js/gsap.min.js"></script>
<link rel="stylesheet" href="css/theme.css">
<style>html,body{{width:1920px;height:1080px;background:#07090F}}#root{{position:relative;width:100%;height:100%;overflow:hidden;background:#07090F}}</style>
</head><body>
<div id="root" data-composition-id="ctrl006v3" data-start="0" data-duration="{total}" data-width="1920" data-height="1080">
{hosts}
</div>
<script>window.__timelines = window.__timelines || {{}}; window.__timelines["ctrl006v3"] = gsap.timeline({{paused:true}});</script>
</body></html>
""")
    print("TOTAL", total)
    for sid, e in events.items():
        print(sid, "dur", e["dur"], "chips", len(e["chips"]), "caps", e["caption_lines"],
              "sweeps", len(e["sweeps"]), "max_gap_major", e["max_gap_major"], "max_gap_all", e["max_gap_all"])

if __name__ == "__main__":
    main()
