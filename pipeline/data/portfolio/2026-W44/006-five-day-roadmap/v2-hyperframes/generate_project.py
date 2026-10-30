#!/usr/bin/env python3
"""Generate the 006 v2 HyperFrames project from v1 timing data.
Sources (read-only): ../build/segments_data.py, timeline.json, chip_times.json, words.json
Output: index.html, compositions/*.html, css/theme.css, assets/{js,fonts,audio}
"""
import json, os, sys, shutil, html as H

BASE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(BASE, "..", "build")
MUSE = os.path.expanduser("~/workspace/muse-comeback-v2/muse-comeback")
sys.path.insert(0, BUILD)
from segments_data import SEGMENTS  # noqa

timeline = json.load(open(os.path.join(BUILD, "timeline.json")))
chip_times = json.load(open(os.path.join(BUILD, "chip_times.json")))
words = json.load(open(os.path.join(BUILD, "words.json")))
flat_words = []
for seg in words:
    for w in seg["words"]:
        flat_words.append((w["start"], w["end"], w["word"].strip()))
flat_words.sort()

SEG = {s["id"]: s for s in SEGMENTS}
TL = timeline["timeline"]
TOTAL = round(timeline["total"] + 8.0, 2)  # timeline total includes outro start; final = outro start + 8

IMG = {
    "s01": None,  # videos + desk image
    "s02": "img-s02-intro.webp",
    "s03_1": "img-s03-1-git.webp", "s03_2": "img-s03-2-aws.webp", "s03_3": "img-s03-3-docker.webp",
    "s03_4": "img-s03-4-cursor.webp", "s03_5": "img-s03-5-amplify.webp", "s03_6": "img-s03-6-sam.webp",
    "s04_1": "img-s04-1-react.webp", "s04_2": "img-s04-2-vibe.webp", "s04_3": "img-s04-3-gateway.webp",
    "s05_1": "img-s05-1-lambda.webp", "s05_2": "img-s05-2-aibuild.webp", "s05_3": "img-s05-3-queue.webp",
    "s06_1": "img-s06-1-dynamo.webp", "s06_2": "img-s06-2-testing.webp", "s06_3": "img-s06-3-garage.webp",
    "s07_1": "img-s07-1-deploy.webp", "s07_2": "img-s07-2-cloudwatch.webp", "s07_3": "img-s07-3-gauges.webp",
    "s08": "img-s08-route.webp",
}
VID = {  # seg -> (file, seconds used at scene start)
    "s03_3": ("vid-s03-3-docker.mp4", 10.0),
    "s05_1": ("vid-s05-1-lambda.mp4", 10.0),
    "s07_1": ("vid-s07-1-deploy.mp4", 10.0),
}
HOOK_VIDS = ["vid-hook-1-deploy.mp4", "vid-hook-2-app.mp4", "vid-hook-3-dashboards.mp4"]

import re
def add_ids(text, prefix):
    n = [0]
    def rep(m):
        tag, attrs = m.group(1), m.group(2)
        if " id=" in attrs or ' id="' in attrs:
            return m.group(0)
        n[0] += 1
        return f'<{tag} id="{prefix}-{n[0]}"{attrs}>'
    return re.sub(r'<(div|img|video|audio|span)([^>]*data-start[^>]*)>', rep, text)

def chip_kind(label):
    if label.startswith("WHAT"): return "what"
    if label.startswith("WHY"): return "why"
    if label.startswith("IF YOU SKIP"): return "skip"
    if label.startswith("HOW"): return "how"
    if label in ("FREE TIER",): return "gold"
    if label.startswith("LATER"): return "skip"
    return "gold"

def esc(s): return H.escape(s, quote=True)

def _ass_time(s):
    h, m, rest = s.split(":")
    return int(h) * 3600 + int(m) * 60 + float(rest)

def load_ass_groups():
    """Parse v1 captions.ass: true-timeline events, one per word-step of a
    caption group, script-verbatim text, gold word tagged 00D7FF.
    Returns groups: [{start, end, words:[(word, gold_start)]}]"""
    import re as _re
    events = []
    for line in open(os.path.join(BUILD, "captions.ass"), encoding="utf-8"):
        if not line.startswith("Dialogue:"):
            continue
        parts = line.split(",", 9)
        start, end = _ass_time(parts[1]), _ass_time(parts[2])
        raw = parts[9].rstrip("\n")
        toks = _re.split(r"(\{[^}]*\})", raw)
        words, gold = [], -1
        cur_gold = False
        for tok in toks:
            if tok.startswith("{"):
                cur_gold = "00D7FF" in tok
            elif tok.strip():
                for w in tok.split():
                    if cur_gold:
                        gold = len(words)
                    words.append(w)
        events.append((start, end, tuple(words), gold))
    groups = []
    for start, end, words, gold in events:
        if groups and groups[-1]["words_key"] == words:
            g = groups[-1]
            g["end"] = end
            if 0 <= gold < len(words) and g["gold"][gold] is None:
                g["gold"][gold] = start
        else:
            g = {"start": start, "end": end, "words_key": words,
                 "gold": [None] * len(words)}
            if 0 <= gold < len(words):
                g["gold"][gold] = start
            groups.append(g)
    out = []
    for g in groups:
        ws = [(w, g["gold"][i] if g["gold"][i] is not None else g["start"])
              for i, w in enumerate(g["words_key"])]
        out.append((g["start"], g["end"], ws))
    return out

ASS_GROUPS = load_ass_groups()

def caption_groups(start, end):
    """Groups (true timeline) starting inside [start, end); returns
    [(g_start, g_end, [(word, gold_start), ...]), ...]"""
    return [(gs, ge, ws) for gs, ge, ws in ASS_GROUPS if start <= gs < end]

SCENE_CSS = """
#root{position:absolute;inset:0;background:#0B0E14;overflow:hidden;font-family:Inter,sans-serif;color:#fff}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(5,7,12,.88) 0%,rgba(5,7,12,.45) 46%,rgba(5,7,12,.05) 75%),linear-gradient(0deg,rgba(5,7,12,.92) 0%,rgba(5,7,12,0) 34%),linear-gradient(180deg,rgba(5,7,12,.55) 0%,rgba(5,7,12,0) 26%)}
.mute{position:absolute;inset:0;background:rgba(20,22,30,.38)}
.pill{position:absolute;top:44px;left:56px;padding:10px 22px;border-radius:999px;background:rgba(8,10,16,.82);border:1.5px solid rgba(94,234,212,.55);font-family:"JetBrains Mono",monospace;font-size:21px;font-weight:700;letter-spacing:.18em;color:#5EEAD4}
.namecard{position:absolute;top:104px;left:56px;max-width:1150px}
.title{font-size:88px;font-weight:700;letter-spacing:-.02em;line-height:1.02;text-shadow:0 4px 30px rgba(0,0,0,.6)}
.subtitle{font-size:34px;color:rgba(255,255,255,.85);margin-top:10px;font-weight:600}
.yearchip{display:inline-block;margin-left:20px;padding:8px 20px;border-radius:999px;border:2px solid #FFD166;color:#FFD166;font-size:30px;font-weight:700;vertical-align:middle;position:relative}
.ule{position:absolute;left:2px;bottom:-16px;height:8px;width:0;background:linear-gradient(90deg,#FFD166,#FF5DA2);border-radius:4px}
.headline{position:absolute;left:56px;bottom:196px;width:1080px;font-size:52px;font-weight:700;line-height:1.16;letter-spacing:-.01em;text-shadow:0 3px 22px rgba(0,0,0,.75)}
.headline .hl-in{position:relative;display:inline-block}
.headline .bar{position:absolute;left:0;bottom:-14px;height:7px;width:0;background:#5EEAD4;border-radius:4px}
.rail{position:absolute;right:48px;top:150px;width:520px;display:flex;flex-direction:column;gap:16px}
.chip{border-radius:18px;padding:16px 20px 14px;background:rgba(8,11,18,.86);border:2px solid rgba(255,255,255,.25);box-shadow:0 10px 34px rgba(0,0,0,.45)}
.chip .k{font-family:"JetBrains Mono",monospace;font-size:19px;font-weight:700;letter-spacing:.16em;margin-bottom:6px}
.chip .t{font-size:25px;line-height:1.28;color:rgba(255,255,255,.94);font-weight:600}
.chip.what{border-color:#22D3EE}.chip.what .k{color:#22D3EE}
.chip.why{border-color:#A78BFA}.chip.why .k{color:#A78BFA}
.chip.skip{border-color:#F87171}.chip.skip .k{color:#F87171}
.chip.how{border-color:#4ADE80}.chip.how .k{color:#4ADE80}
.chip.gold{border-color:#FFD166}.chip.gold .k{color:#FFD166}
.laterbadge{position:absolute;top:44px;right:48px;padding:12px 26px;border-radius:12px;background:#B91C1C;color:#fff;font-family:"JetBrains Mono",monospace;font-weight:700;letter-spacing:.22em;font-size:24px;transform:rotate(3deg)}
.caps{position:absolute;left:0;right:0;bottom:52px;display:flex;justify-content:center}
.cap{background:rgba(0,0,0,.78);padding:12px 26px;border-radius:10px;font-size:39px;font-weight:600;text-align:center;max-width:1560px}
.cap span{color:#fff}
.bigflash{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:120px;font-weight:700;letter-spacing:-.01em;text-shadow:0 6px 44px rgba(0,0,0,.8)}
.daycard{position:absolute;inset:0;background:radial-gradient(1100px 620px at 50% 42%,#1B2436 0%,#0B0E14 70%);display:flex;flex-direction:column;align-items:center;justify-content:center}
.daycard .d1{font-family:"JetBrains Mono",monospace;letter-spacing:.3em;color:#5EEAD4;font-size:30px;font-weight:700}
.daycard .d2{font-size:150px;font-weight:700;letter-spacing:-.02em;margin-top:8px}
.daycard .d3{font-size:44px;color:rgba(255,255,255,.8);font-weight:600;margin-top:6px}
.daycard .rule{width:0;height:8px;background:linear-gradient(90deg,#FFD166,#FF5DA2);border-radius:4px;margin-top:34px}
.outro{position:absolute;inset:0;background:#07090F;display:flex;flex-direction:column;align-items:center;justify-content:center}
.outro img{width:760px;height:428px;object-fit:cover;border-radius:24px;box-shadow:0 0 120px rgba(255,209,102,.25)}
.outro .o1{font-size:64px;font-weight:700;margin-top:36px}
.outro .o2{font-size:34px;color:rgba(255,255,255,.75);margin-top:12px;font-weight:600}
.subpill{margin-top:30px;padding:16px 44px;border-radius:999px;background:#E11D48;font-size:32px;font-weight:700;letter-spacing:.14em}
.node{position:absolute;width:26px;height:26px;border-radius:50%;background:#223;border:3px solid rgba(255,255,255,.25)}
.counter{font-size:120px;font-weight:700;color:#FFD166}
"""

def seg_scene(item):
    sid, start, dur = item["id"], item["start"], item["dur"]
    s = SEG[sid]
    chips = chip_times.get(sid, [])
    rel = [(lbl, round(t - start, 2)) for lbl, t in chips]
    parts, script = [], []
    # media layer
    if sid == "s01":
        per = dur / 3.0
        for i, v in enumerate(HOOK_VIDS):
            parts.append(f'<video class="clip bg" data-start="{i*per:.2f}" data-duration="{per:.2f}" src="assets/gen/{v}" muted playsinline></video>')
        parts.append(f'<img class="clip bg" data-start="{dur-3.5:.2f}" data-duration="3.5" src="assets/gen/img-s01-hook-desk.webp" style="opacity:0">')
        script.append(f'tl.fromTo("#bgdesk",{{opacity:0}},{{opacity:1,duration:.5}}, {dur-3.5:.2f});')
        parts[-1] = parts[-1].replace('class="clip bg"', 'class="clip bg" id="bgdesk"')
    elif sid in VID:
        vf, vd = VID[sid]
        parts.append(f'<video class="clip bg" data-start="0" data-duration="{vd}" src="assets/gen/{vf}" muted playsinline></video>')
        parts.append(f'<img class="clip bg" id="bgimg-{sid}" data-start="{vd}" data-duration="{dur-vd:.2f}" src="assets/gen/{IMG[sid]}">')
    else:
        parts.append(f'<img class="clip bg" data-start="0" data-duration="{dur}" src="assets/gen/{IMG[sid]}">')
    parts.append(f'<div class="clip shade" data-start="0" data-duration="{dur}"></div>')
    if s.get("later"):
        parts.append(f'<div class="clip mute" data-start="0" data-duration="{dur}"></div>')
        parts.append(f'<div class="clip" data-start="0.3" data-duration="{dur-0.3}"><div class="laterbadge" id="later-{sid}">LATER</div></div>')
        script.append(f'tl.fromTo("#later-{sid}",{{scale:2.4,opacity:0}},{{scale:1,opacity:1,duration:.38,ease:"power4.out"}},0.3);')
    # pill + namecard
    parts.append(f'<div class="clip" data-start="0" data-duration="{dur}"><div class="pill" id="pill-{sid}">{esc(s["scene"])}</div></div>')
    year = f'<span class="yearchip">{esc(s["year"])}</span>' if s["year"] else ""
    parts.append(f'<div class="clip" data-start="0" data-duration="{dur}"><div class="namecard" id="nc-{sid}"><div class="title">{esc(s["title"])}{year}<div class="ule" id="ule-{sid}"></div></div><div class="subtitle">{esc(s["subtitle"])}</div></div></div>')
    script.append(f'tl.fromTo("#pill-{sid}",{{x:-60,opacity:0}},{{x:0,opacity:1,duration:.45,ease:"power3.out"}},0.05);')
    script.append(f'tl.fromTo("#nc-{sid}",{{y:44,opacity:0}},{{y:0,opacity:1,duration:.55,ease:"power3.out"}},0.18);')
    script.append(f'tl.to("#ule-{sid}",{{width:"62%",duration:.6,ease:"power2.inOut"}},0.55);')
    # headlines per chip beat (detail text), first headline = subtitle claim at 0.4
    heads = []
    if sid == "s01":
        heads = [(0.4, "A production-ready app. Five days. Almost free.")] + [(t, lbl.title()) for lbl, t in rel]
    elif sid == "s02":
        heads = [(0.4, "Five days. 38 hours. Pay-per-request everything.")] + [(t, lbl.title()) for lbl, t in rel]
    else:
        detail = {c[0]: c[1] for c in s["chips"]}
        heads = [(0.4, s["subtitle"] + ".")] + [(t, detail.get(lbl, lbl)) for lbl, t in rel]
    for i, (t0, txt) in enumerate(heads):
        t1 = heads[i + 1][0] if i + 1 < len(heads) else dur
        if t1 - t0 < 0.4: t1 = min(dur, t0 + 0.4)
        hid = f"h-{sid}-{i}"
        parts.append(f'<div class="clip headline" data-start="{t0}" data-duration="{t1-t0:.2f}"><span class="hl-in" id="{hid}">{esc(txt)}<span class="bar" id="{hid}-bar"></span></span></div>')
        script.append(f'tl.fromTo("#{hid}",{{y:36,opacity:0}},{{y:0,opacity:1,duration:.4,ease:"power3.out"}},{t0});')
        script.append(f'tl.to("#{hid}-bar",{{width:"100%",duration:.5,ease:"power2.out"}},{t0+0.15});')
    # chips rail
    rail_chips = []
    for i, (lbl, t0) in enumerate(rel):
        detail = {c[0]: c[1] for c in s["chips"]}
        txt = detail.get(lbl, "")
        if sid in ("s01",): txt = ""
        if sid == "s02": txt = ""
        cid = f"chip-{sid}-{i}"
        inner = f'<div class="k">{esc(lbl)}</div>' + (f'<div class="t">{esc(txt)}</div>' if txt else "")
        rail_chips.append(f'<div class="clip" data-start="{t0}" data-duration="{dur-t0:.2f}"><div class="chip {chip_kind(lbl)}" id="{cid}">{inner}</div></div>')
        script.append(f'tl.fromTo("#{cid}",{{scale:1.7,opacity:0,rotation:-4}},{{scale:1,opacity:1,rotation:0,duration:.42,ease:"back.out(2.2)"}},{t0});')
    if rail_chips:
        parts.append('<div class="rail">' + "".join(rail_chips) + '</div>')
    # git checkpoint nodes
    if sid == "s03_1":
        nodes = []
        for i in range(5):
            t0 = 1.2 + i * 1.6
            nid = f"node-{i}"
            nodes.append(f'<div class="clip" data-start="{t0}" data-duration="{dur-t0:.2f}"><div class="node" id="{nid}" style="left:{120+i*120}px;bottom:150px"></div></div>')
            script.append(f'tl.to("#{nid}",{{backgroundColor:"#FFD166",borderColor:"#FFD166",boxShadow:"0 0 34px rgba(255,209,102,.9)",duration:.3}},{t0});')
        parts.extend(nodes)
    # captions
    caps = []
    for gi, (gs, ge, gwords) in enumerate(caption_groups(start, start + dur)):
        g0 = round(gs - start, 2); g1 = round(ge - start, 2)
        if g1 <= g0: g1 = g0 + 0.3
        if g1 > dur: g1 = dur
        spans = "".join(f'<span id="w-{sid}-{gi}-{wi}">{esc(w)}</span> ' for wi, (w, gt) in enumerate(gwords))
        cid = f"cap-{sid}-{gi}"
        caps.append(f'<div class="clip caps" data-start="{g0}" data-duration="{g1-g0:.2f}"><div class="cap" id="{cid}">{spans}</div></div>')
        script.append(f'tl.fromTo("#{cid}",{{opacity:0}},{{opacity:1,duration:.07,ease:"none"}},{g0});')
        for wi, (w, gt) in enumerate(gwords):
            script.append(f'tl.to("#w-{sid}-{gi}-{wi}",{{color:"#FFD166",duration:.05,ease:"none"}},{round(gt-start,2)});')
    parts.extend(caps)
    body = add_ids("\n".join(parts), "el-"+sid)
    js = "\n".join(script)
    return f"""<template>
<link rel="stylesheet" href="css/theme.css">
<style>{SCENE_CSS}</style>
<div id="root" data-composition-id="{sid}" data-start="0" data-duration="{dur}" data-width="1920" data-height="1080">
{body}
</div>
<script src="assets/js/gsap.min.js"></script>
<script>
window.__timelines = window.__timelines || {{}};
(function(){{
  var tl = gsap.timeline({{ paused: true }});
{js}
  window.__timelines["{sid}"] = tl;
}})();
</script>
</template>
"""

def daycard(idx, name, hours, start):
    cid = f"day{idx}"
    return add_ids(f"""<template>
<link rel="stylesheet" href="css/theme.css">
<style>{SCENE_CSS}</style>
<div id="root" data-composition-id="{cid}" data-start="0" data-duration="1.6" data-width="1920" data-height="1080">
<div class="clip daycard" data-start="0" data-duration="1.6">
  <div class="d1" id="{cid}-a">DAY {idx} OF 5</div>
  <div class="d2" id="{cid}-b">{name}</div>
  <div class="d3" id="{cid}-c">{hours}</div>
  <div class="rule" id="{cid}-r"></div>
</div>
</div>
<script src="assets/js/gsap.min.js"></script>
<script>
window.__timelines = window.__timelines || {{}};
(function(){{
  var tl = gsap.timeline({{ paused: true }});
  tl.fromTo("#{cid}-a",{{opacity:0,y:-26}},{{opacity:1,y:0,duration:.3,ease:"power3.out"}},0.05);
  tl.fromTo("#{cid}-b",{{scale:1.6,opacity:0}},{{scale:1,opacity:1,duration:.42,ease:"back.out(1.8)"}},0.16);
  tl.fromTo("#{cid}-c",{{opacity:0}},{{opacity:1,duration:.3}},0.5);
  tl.to("#{cid}-r",{{width:520,duration:.5,ease:"power2.inOut"}},0.55);
  window.__timelines["{cid}"] = tl;
}})();
</script>
</template>
""", cid)

def outro():
    return add_ids(f"""<template>
<link rel="stylesheet" href="css/theme.css">
<style>{SCENE_CSS}</style>
<div id="root" data-composition-id="outro" data-start="0" data-duration="8" data-width="1920" data-height="1080">
<div class="clip outro" data-start="0" data-duration="8">
  <img id="out-img" src="assets/gen/img-outro-arrow.webp">
  <div class="o1" id="out-1">We don't chase the future. We check it.</div>
  <div class="o2" id="out-2">Ctrl-Ahead — confirmed, not just claimed.</div>
  <div class="subpill" id="out-3">SUBSCRIBE</div>
</div>
</div>
<script src="assets/js/gsap.min.js"></script>
<script>
window.__timelines = window.__timelines || {{}};
(function(){{
  var tl = gsap.timeline({{ paused: true }});
  tl.fromTo("#out-img",{{scale:.7,opacity:0,rotation:-6}},{{scale:1,opacity:1,rotation:0,duration:.7,ease:"back.out(1.6)"}},0.2);
  tl.fromTo("#out-1",{{y:40,opacity:0}},{{y:0,opacity:1,duration:.5,ease:"power3.out"}},0.9);
  tl.fromTo("#out-2",{{y:30,opacity:0}},{{y:0,opacity:1,duration:.5,ease:"power3.out"}},1.5);
  tl.fromTo("#out-3",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:.5,ease:"back.out(2.4)"}},2.2);
  tl.to("#out-3",{{scale:1.08,duration:.35,ease:"power2.inOut"}},3.4);
  tl.to("#out-3",{{scale:1,duration:.35,ease:"power2.inOut"}},3.8);
  window.__timelines["outro"] = tl;
}})();
</script>
</template>
""", "out")

def main():
    os.makedirs(os.path.join(BASE, "compositions"), exist_ok=True)
    os.makedirs(os.path.join(BASE, "css"), exist_ok=True)
    os.makedirs(os.path.join(BASE, "assets", "js"), exist_ok=True)
    os.makedirs(os.path.join(BASE, "assets", "fonts"), exist_ok=True)
    os.makedirs(os.path.join(BASE, "assets", "audio"), exist_ok=True)
    shutil.copy(os.path.join(MUSE, "assets/js/gsap.min.js"), os.path.join(BASE, "assets/js/gsap.min.js"))
    for f in os.listdir(os.path.join(MUSE, "assets/fonts")):
        shutil.copy(os.path.join(MUSE, "assets/fonts", f), os.path.join(BASE, "assets/fonts", f))
    with open(os.path.join(BASE, "css/theme.css"), "w") as fh:
        fh.write("""@font-face{font-family:"Inter";src:url("../assets/fonts/Inter-Regular.woff2") format("woff2");font-weight:400}
@font-face{font-family:"Inter";src:url("../assets/fonts/Inter-SemiBold.woff2") format("woff2");font-weight:600}
@font-face{font-family:"Inter";src:url("../assets/fonts/Inter-Bold.woff2") format("woff2");font-weight:700}
@font-face{font-family:"JetBrains Mono";src:url("../assets/fonts/JetBrainsMono-Regular.woff2") format("woff2");font-weight:400}
@font-face{font-family:"JetBrains Mono";src:url("../assets/fonts/JetBrainsMono-Bold.woff2") format("woff2");font-weight:700}
:root{--gold:#FFD166;--cyan:#5EEAD4}
*{margin:0;padding:0;box-sizing:border-box}
""")
    hosts, days = [], {1: ("SETUP", "7 HOURS"), 2: ("UI", "8 HOURS"), 3: ("BACKEND", "8 HOURS"), 4: ("DATA", "8 HOURS"), 5: ("LAUNCH", "7 HOURS")}
    for item in TL:
        if item["kind"] == "seg":
            fn = f"compositions/{item['id']}.html"
            open(os.path.join(BASE, fn), "w").write(seg_scene(item))
            hosts.append((item["id"], fn, item["start"], item["dur"]))
        elif item["kind"] == "daycard":
            idx = int(item["file"][3])
            cid = f"day{idx}"
            fn = f"compositions/{cid}.html"
            open(os.path.join(BASE, fn), "w").write(daycard(idx, days[idx][0], days[idx][1], item["start"]))
            hosts.append((cid, fn, item["start"], item["dur"]))
        elif item["kind"] == "outro":
            fn = "compositions/outro.html"
            open(os.path.join(BASE, fn), "w").write(outro())
            hosts.append(("outro", fn, item["start"], item["dur"]))
    total = round(max(h[2] + h[3] for h in hosts), 2)
    host_html = "\n".join(
        f'<div id="host-{hid}" data-composition-id="{hid}" data-composition-src="{fn}" data-start="{st}" data-duration="{du}" data-track-index="0" data-track-kind="graphics" data-width="1920" data-height="1080"></div>'
        for hid, fn, st, du in hosts)
    index = f"""<!doctype html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=1920, height=1080">
<script src="assets/js/gsap.min.js"></script>
<link rel="stylesheet" href="css/theme.css">
<style>html,body{{width:1920px;height:1080px;background:#0B0E14}}#root{{position:relative;width:100%;height:100%;overflow:hidden;background:#0B0E14}}</style>
</head><body>
<div id="root" data-composition-id="ctrl006v2" data-start="0" data-duration="{total}" data-width="1920" data-height="1080">
{host_html}
<audio id="mix" data-start="0" data-duration="{total}" src="assets/audio/final-mix.m4a"></audio>
</div>
<script>window.__timelines = window.__timelines || {{}}; window.__timelines["ctrl006v2"] = gsap.timeline({{paused:true}});</script>
</body></html>
"""
    open(os.path.join(BASE, "index.html"), "w").write(index)
    open(os.path.join(BASE, "meta.json"), "w").write(json.dumps({"id": "ctrl006v2", "name": "Ctrl-Ahead 006 v2 — HyperFrames"}, indent=1))
    open(os.path.join(BASE, "package.json"), "w").write(json.dumps({"name": "ctrl006v2", "private": True, "type": "module", "scripts": {"check": "npx --yes hyperframes@0.8.210 check", "render": "npx --yes hyperframes@0.8.210 render"}}, indent=1))
    open(os.path.join(BASE, "hyperframes.json"), "w").write(json.dumps({"$schema": "https://hyperframes.heygen.com/schema/hyperframes.json", "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"}, "media": {"autoProxy": True}}, indent=1))
    print("scenes:", len(hosts), "total:", total)

if __name__ == "__main__":
    main()
