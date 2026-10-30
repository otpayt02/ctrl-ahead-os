#!/usr/bin/env python3
"""Generate the six HyperFrames compositions for the Ahead of Rush AI Argon video.
Caption text comes ONLY from the approved script (work/segments.json via the
aligned word timings in work/words_sN.json). Scene beats are anchored to the
real word timestamps measured from the Helio VO."""
import json, os

ROOT = os.path.expanduser('~/workspace/ctrl-ahead-argon')
VO_DUR = {1: 22.368, 2: 35.568, 3: 41.352, 4: 29.28, 5: 26.688, 6: 19.152}
SCENE_DUR = {n: round(VO_DUR[n] + 1.2, 3) for n in VO_DUR}
STARTS = {}
_acc = 0.0
for n in range(1, 7):
    STARTS[n] = round(_acc, 3)
    _acc += SCENE_DUR[n]
TOTAL = round(_acc, 3)


def build_captions(n):
    words = json.load(open(f'{ROOT}/work/words_s{n}.json'))
    toks = []
    for w in words:
        if w['w'] == '—' and toks:
            toks[-1]['w'] += ' —'
            toks[-1]['end'] = max(toks[-1]['end'], w['end'])
        else:
            toks.append(dict(w))
    phrases, cur = [], []
    for tk in toks:
        cur.append(tk)
        text = ' '.join(x['w'] for x in cur)
        last = tk['w'][-1] if tk['w'] else ''
        if last in '.!?;:' or (last == ',' and len(cur) >= 4) or len(cur) >= 7 or len(text) > 52:
            phrases.append(cur); cur = []
    if cur:
        phrases.append(cur)
    out = []
    for i, ph in enumerate(phrases):
        start = ph[0]['start']
        end = ph[-1]['end']
        if i + 1 < len(phrases):
            nxt = phrases[i + 1][0]['start']
            end = min(max(end, nxt - 0.35), nxt - 0.03) if nxt - end < 0.5 else end
            end = min(end, nxt - 0.03)
        out.append({'start': round(start, 2), 'end': round(end, 2),
                    'words': [{'w': x['w'], 'start': round(x['start'], 2), 'end': round(x['end'], 2)} for x in ph]})
    return out


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def caption_html(n, phrases):
    divs = []
    for p, ph in enumerate(phrases):
        spans = ' '.join(
            f'<span class="w" id="s{n}-w-{p}-{i}">{esc(w["w"])}</span>'
            for i, w in enumerate(ph['words']))
        divs.append(f'          <div class="caption" id="s{n}-cap-{p}" style="opacity:0;">{spans}</div>')
    return '\n'.join(divs)


def caption_js(n, phrases):
    items = []
    for p, ph in enumerate(phrases):
        ws = ','.join(f'["s{n}-w-{p}-{i}",{w["start"]:.2f},{w["end"]:.2f}]' for i, w in enumerate(ph['words']))
        items.append(f'{{el:"s{n}-cap-{p}",start:{ph["start"]:.2f},end:{ph["end"]:.2f},words:[{ws}]}}')
    return ('      var CAPS = [' + ','.join(items) + '];\n'
            '      driveCaptions(tl, CAPS.map(function (p) { return { el: document.getElementById(p.el), start: p.start, end: p.end, words: p.words.map(function (w) { return [document.getElementById(w[0]), w[1], w[2]]; }) }; }));')


CAP_CSS = """
  #s{n}-captions {{ top:auto; bottom:36px; height:204px; }}
  #s{n}-captions .caption {{ position:absolute; left:420px; right:420px; bottom:0; display:block; white-space:nowrap; font-size:62px; }}
  .caption .w {{ color: rgba(255,255,255,0.42); }}
"""

SCENE_HEAD = """<template>
  <link rel="stylesheet" href="css/theme.css" />
  <style>
    #root {{ position:absolute; inset:0; background:var(--dark-bg); overflow:hidden; }}
{css}
  </style>
  <div id="root" data-composition-id="{sid}" data-start="0" data-duration="{dur}" data-width="3840" data-height="2160">
{body}
  </div>
  <script src="assets/js/gsap.min.js"></script>
  <script src="js/shared.js"></script>
  <script>
    (function () {{
      const tl = makeSceneTimeline("{sid}", {dur});
      window.__timelines["{sid}"] = tl;
{js}
    }})();
  </script>
</template>
"""


def scene(n, sid, css, body, js):
    phrases = build_captions(n)
    body = body.replace('__CAPTIONS__', caption_html(n, phrases))
    body = body.replace('__DUR__', fmt(SCENE_DUR[n]))
    js = js.replace('__CAPJS__', caption_js(n, phrases))
    js = js.replace('__DURM__', fmt(SCENE_DUR[n] - 0.3))
    css = css + CAP_CSS.format(n=n)
    html = SCENE_HEAD.format(css=css, sid=sid, dur=SCENE_DUR[n], body=body, js=js)
    path = f'{ROOT}/compositions/{sid}.html'
    with open(path, 'w') as fh:
        fh.write(html)
    print('wrote', path, 'scene dur', SCENE_DUR[n], 'captions', len(phrases))


# ---------------------------------------------------------------- S1 HOOK
S1_CSS = """
  .stage { position:absolute; inset:0; overflow:hidden; }
  .plate { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }
  .scrim { position:absolute; inset:0; background:linear-gradient(90deg, rgba(5,7,11,0.86) 0%, rgba(5,7,11,0.52) 52%, rgba(5,7,11,0.18) 100%); }
  .scrim-b { position:absolute; inset:0; background:linear-gradient(0deg, rgba(5,7,11,0.88) 0%, rgba(5,7,11,0) 30%); }
  .kicker { position:absolute; font-family:var(--font-mono); font-weight:600; letter-spacing:0.30em; color:var(--neon-cyan); font-size:46px; }
  .stmt-small { font-size:58px; font-weight:600; color:rgba(255,255,255,0.72); letter-spacing:0.04em; }
  .stmt-big { font-size:118px; font-weight:700; letter-spacing:-0.02em; color:#fff; line-height:1.08; margin-top:18px; }
  .chip { position:absolute; padding:22px 38px; border-radius:999px; border:3px solid rgba(255,255,255,0.30); background:rgba(10,13,20,0.82); font-size:46px; font-weight:600; white-space:nowrap; }
  .chip.gold { border-color:var(--gold); color:var(--gold); }
  .chip.cyan { border-color:var(--neon-cyan); color:var(--neon-cyan); }
  .headline { position:absolute; font-weight:700; letter-spacing:-0.02em; line-height:1.02; color:#fff; }
  .stat { position:absolute; padding:40px 48px; }
  .stat .num { font-family:var(--font-mono); font-weight:700; font-size:118px; color:var(--gold); line-height:1; }
  .stat .num.white { color:#fff; font-size:104px; }
  .stat .lbl { font-size:44px; font-weight:600; color:rgba(255,255,255,0.85); margin-top:16px; line-height:1.25; }
  .fadeblack { position:absolute; inset:0; background:#000; pointer-events:none; }
  #s1-underline { position:absolute; left:428px; top:1168px; width:1480px; height:10px; background:var(--gold); transform-origin:0 50%; }
  #s1-mw-strike { position:absolute; left:34px; top:50%; width:300px; height:8px; background:var(--skeptic-red); transform-origin:0 50%; }
"""

S1_BODY = """
    <div id="s1-cam" class="clip" data-start="0" data-duration="__DUR__" data-track-index="0">
      <div class="stage">
        <img class="plate" src="assets/img/plate_s1.webp" alt="" />
        <div class="scrim"></div>
        <div class="scrim-b"></div>
        <div id="s1-kicker" class="kicker" style="left:420px; top:190px; opacity:0;">AHEAD OF RUSH AI &nbsp;·&nbsp; AI CODING AGENTS</div>
        <div id="s1-statement" style="position:absolute; left:420px; top:300px; width:2900px; opacity:0;">
          <div class="stmt-small">GOOGLE POINTED ITS NEWEST CODING MODEL AT</div>
          <div class="stmt-big">THE HARDEST CODEBASE<br/>IT OWNS.</div>
        </div>
        <div id="s1-worked" class="chip gold" style="left:2790px; top:290px; opacity:0;">AND IT WORKED</div>
        <div id="s1-headline" class="headline" style="left:420px; top:620px; font-size:205px; opacity:0;">GEMINI 4<br/><span style="color:var(--gold);">ARGON</span></div>
        <div id="s1-underline" style="transform:scaleX(0);"></div>
        <div id="s1-chip1" class="chip cyan" style="left:420px; top:1250px; opacity:0;">ANNOUNCED — SEP 30</div>
        <div id="s1-chip2" class="chip cyan" style="left:1330px; top:1250px; opacity:0;">GENERALLY AVAILABLE — OCT 13</div>
        <div id="s1-card1" class="glass-panel stat" style="left:2380px; top:720px; width:1180px; opacity:0;">
          <div class="num" id="s1-num1">0</div>
          <div class="lbl">LINES OF LEGACY CODE,<br/>UNTANGLED</div>
        </div>
        <div id="s1-card2" class="glass-panel stat" style="left:2380px; top:1090px; width:1180px; opacity:0;">
          <div class="num white">40,000,000-LINE</div>
          <div class="lbl">CHROMIUM CODEBASE<br/>IT WAS BURIED IN</div>
        </div>
        <div id="s1-mw" class="chip" style="left:420px; top:1420px; opacity:0; font-size:56px; padding:26px 44px;">
          <span style="position:relative; display:inline-block;">MONTHS<span id="s1-mw-strike" style="transform:scaleX(0);"></span></span>
          <span style="color:rgba(255,255,255,0.5);">&nbsp;&nbsp;→&nbsp;&nbsp;</span><span id="s1-weeks" style="color:var(--gold); font-weight:700; opacity:0;">WEEKS</span>
        </div>
        <div id="s1-dec" class="chip gold" style="left:2380px; top:1440px; opacity:0;">AFTER DECEMBER FIRST →</div>
        <div id="s1-brand" class="chip" style="left:1170px; top:1640px; width:1500px; text-align:center; opacity:0; font-family:var(--font-mono); letter-spacing:0.28em; font-size:44px;">THIS IS AHEAD OF RUSH AI</div>
        <div class="caption-band" id="s1-captions">
__CAPTIONS__
        </div>
        <div id="s1-fade" class="fadeblack"></div>
      </div>
    </div>
"""

S1_JS = """
      const cam1 = document.getElementById("s1-cam");
      cameraPush(cam1, 0.97, 1.0, 0.4, tl, 0);
      tl.fromTo("#s1-fade", { opacity: 1 }, { opacity: 0, duration: 0.3, ease: "none" }, 0);
      tl.fromTo("#s1-fade", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "none", immediateRender: false }, __DURM__);
      tl.fromTo("#s1-kicker", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.5 }, 0.3);
      tl.fromTo("#s1-statement", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, 2.3);
      stampIn(document.getElementById("s1-worked"), tl, 4.2);
      tl.to("#s1-statement", { opacity: 0, y: -30, duration: 0.4, ease: "power2.in" }, 5.15);
      tl.fromTo("#s1-headline", { opacity: 0, scale: 0.82, y: 60 }, { opacity: 1, scale: 1, y: 0, duration: 0.55, ease: "back.out(1.6)" }, 5.3);
      tl.fromTo("#s1-underline", { scaleX: 0 }, { scaleX: 1, duration: 0.5, ease: "power3.out" }, 5.85);
      stampIn(document.getElementById("s1-chip1"), tl, 6.3);
      stampIn(document.getElementById("s1-chip2"), tl, 7.15);
      pinCard(document.getElementById("s1-card1"), tl, 8.2);
      countUp(document.getElementById("s1-num1"), 0, 6000000, 1.4, tl, 8.2);
      pinCard(document.getElementById("s1-card2"), tl, 11.4);
      pinCard(document.getElementById("s1-mw"), tl, 14.2);
      tl.fromTo("#s1-mw-strike", { scaleX: 0 }, { scaleX: 1, duration: 0.35, ease: "power2.out" }, 14.9);
      tl.fromTo("#s1-weeks", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, 15.35);
      tl.to(["#s1-card1", "#s1-card2"], { opacity: 0.5, duration: 0.5 }, 16.4);
      tl.fromTo("#s1-brand", { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.5 }, 17.2);
      stampIn(document.getElementById("s1-dec"), tl, 21.2);
__CAPJS__
"""

# ---------------------------------------------------------------- S2 EVIDENCE
S2_CSS = """
  .stage { position:absolute; inset:0; overflow:hidden; }
  .plate { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; opacity:0.55; }
  .scrim-b { position:absolute; inset:0; background:linear-gradient(0deg, rgba(5,7,11,0.9) 0%, rgba(5,7,11,0) 32%); }
  .kicker { position:absolute; font-family:var(--font-mono); font-weight:600; letter-spacing:0.30em; color:var(--neon-cyan); font-size:46px; }
  .beat { position:absolute; left:420px; top:520px; width:3000px; }
  .beat .blabel { font-family:var(--font-mono); font-size:52px; letter-spacing:0.24em; color:var(--neon-cyan); }
  .beat .giant { font-family:var(--font-mono); font-weight:700; font-size:330px; line-height:1.05; color:#fff; letter-spacing:-0.02em; margin-top:26px; }
  .beat .giant.gold { color:var(--gold); }
  .beat .bsub { font-size:56px; font-weight:600; color:rgba(255,255,255,0.88); margin-top:30px; }
  .chip { position:absolute; padding:22px 38px; border-radius:999px; border:3px solid rgba(255,255,255,0.30); background:rgba(10,13,20,0.85); font-size:46px; font-weight:600; white-space:nowrap; }
  .chip.red { border-color:var(--skeptic-red); color:#ff8080; }
  .chip.gold { border-color:var(--gold); color:var(--gold); }
  .claim { position:absolute; left:420px; top:640px; width:3000px; font-weight:700; letter-spacing:-0.02em; line-height:1.12; }
  .fadeblack { position:absolute; inset:0; background:#000; pointer-events:none; }
"""

S2_BODY = """
    <div id="s2-cam" class="clip" data-start="0" data-duration="__DUR__" data-track-index="0">
      <div class="stage">
        <img class="plate" src="assets/img/plate_s2.webp" alt="" />
        <div class="scrim-b"></div>
        <div id="s2-kicker" class="kicker" style="left:420px; top:190px; opacity:0;">THE EVIDENCE — DATES FIRST</div>
        <div id="s2-gA" class="beat" style="opacity:0;">
          <div class="blabel">ANNOUNCED</div>
          <div class="giant">SEP 30</div>
          <div class="bsub" id="s2-gA-sub" style="opacity:0;">FIRST RELEASE — VETTED CYBERSECURITY DEFENDERS ONLY</div>
        </div>
        <div id="s2-gB" class="beat" style="opacity:0;">
          <div class="blabel">GENERALLY AVAILABLE</div>
          <div class="giant">OCT 13</div>
        </div>
        <div id="s2-stamp1" class="chip red" style="left:420px; top:1420px; opacity:0;">NOT A LEAK</div>
        <div id="s2-stamp2" class="chip red" style="left:1050px; top:1420px; opacity:0;">NOT BRAND NEW</div>
        <div id="s2-gC" class="beat" style="opacity:0;">
          <div class="blabel">CONTEXT WINDOW</div>
          <div class="giant gold" id="s2-num-ctx">0</div>
          <div class="bsub" id="s2-gC-sub" style="opacity:0;">TOKENS — INPUT + OUTPUT, COMBINED</div>
        </div>
        <div id="s2-gD" class="beat" style="opacity:0;">
          <div class="blabel">DeepSWE v1.1 SCORE</div>
          <div class="giant gold" id="s2-num-swe">0.0%</div>
          <div class="bsub">GOOGLE'S OWN BENCH, GOOGLE'S OWN NUMBER</div>
        </div>
        <div id="s2-tag" class="chip gold" style="left:420px; top:1420px; opacity:0;">GOOGLE-REPORTED</div>
        <div id="s2-gE" class="claim" style="opacity:0;">
          <div style="font-size:180px; color:#fff;">TREAT IT AS A CLAIM,</div>
          <div id="s2-verdict" style="font-size:180px; color:var(--skeptic-red); opacity:0;">NOT A VERDICT.</div>
        </div>
        <div id="s2-gF" style="position:absolute; left:420px; top:560px; width:3000px; opacity:0;">
          <div style="font-size:64px; font-weight:600; color:rgba(255,255,255,0.9); line-height:1.3;">THE CHROMIUM RESULT HAS WHAT<br/>BENCHMARKS DON'T:</div>
        </div>
        <div id="s2-chip1" class="chip" style="left:420px; top:1020px; opacity:0; font-size:56px;">COMMITS</div>
        <div id="s2-chip2" class="chip" style="left:420px; top:1200px; opacity:0; font-size:56px;">IN A PUBLIC TRACKER</div>
        <div id="s2-chip3" class="chip gold" style="left:420px; top:1380px; opacity:0; font-size:56px;">REVIEWED BY HUMAN ENGINEERS</div>
        <div class="caption-band" id="s2-captions">
__CAPTIONS__
        </div>
        <div id="s2-fade" class="fadeblack"></div>
      </div>
    </div>
"""

S2_JS = """
      const cam2 = document.getElementById("s2-cam");
      cameraPush(cam2, 0.97, 1.0, 0.4, tl, 0);
      tl.fromTo("#s2-fade", { opacity: 1 }, { opacity: 0, duration: 0.3, ease: "none" }, 0);
      tl.fromTo("#s2-fade", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "none", immediateRender: false }, __DURM__);
      tl.fromTo("#s2-kicker", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.5 }, 0.3);
      tl.fromTo("#s2-gA", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 2.3);
      tl.fromTo("#s2-gA-sub", { opacity: 0 }, { opacity: 1, duration: 0.45 }, 4.9);
      tl.to("#s2-gA", { opacity: 0, y: -40, duration: 0.35, ease: "power2.in" }, 7.8);
      tl.fromTo("#s2-gB", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 8.1);
      stampIn(document.getElementById("s2-stamp1"), tl, 11.0);
      stampIn(document.getElementById("s2-stamp2"), tl, 12.9);
      tl.to(["#s2-gB", "#s2-stamp1", "#s2-stamp2"], { opacity: 0, y: -40, duration: 0.35, ease: "power2.in" }, 15.2);
      tl.fromTo("#s2-gC", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 15.5);
      countUp(document.getElementById("s2-num-ctx"), 0, 1000000, 1.6, tl, 15.5);
      tl.fromTo("#s2-gC-sub", { opacity: 0 }, { opacity: 1, duration: 0.45 }, 17.9);
      tl.to("#s2-gC", { opacity: 0, y: -40, duration: 0.35, ease: "power2.in" }, 19.9);
      tl.fromTo("#s2-gD", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 20.2);
      countUp(document.getElementById("s2-num-swe"), 0, 77.9, 1.5, tl, 20.2, function (v) { return v.toFixed(1) + "%"; });
      stampIn(document.getElementById("s2-tag"), tl, 23.5);
      tl.to(["#s2-gD", "#s2-tag"], { opacity: 0, y: -40, duration: 0.35, ease: "power2.in" }, 25.4);
      tl.fromTo("#s2-gE", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 25.7);
      tl.fromTo("#s2-verdict", { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.4, ease: "power3.out" }, 27.6);
      tl.to("#s2-gE", { opacity: 0, y: -40, duration: 0.35, ease: "power2.in" }, 28.5);
      tl.fromTo("#s2-gF", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 28.8);
      pinCard(document.getElementById("s2-chip1"), tl, 31.8);
      pinCard(document.getElementById("s2-chip2"), tl, 32.6);
      pinCard(document.getElementById("s2-chip3"), tl, 33.7);
__CAPJS__
"""


# ---------------------------------------------------------------- S3 DIAGRAM
S3_CSS = """
  .stage { position:absolute; inset:0; overflow:hidden; }
  .grid { position:absolute; inset:0; background-image:linear-gradient(rgba(97,218,251,0.05) 2px, transparent 2px), linear-gradient(90deg, rgba(97,218,251,0.05) 2px, transparent 2px); background-size:120px 120px; }
  .scrim-b { position:absolute; inset:0; background:linear-gradient(0deg, rgba(5,7,11,0.92) 0%, rgba(5,7,11,0) 30%); }
  .kicker { position:absolute; font-family:var(--font-mono); font-weight:600; letter-spacing:0.30em; color:var(--neon-cyan); font-size:46px; }
  .headline { position:absolute; font-weight:700; letter-spacing:-0.02em; color:#fff; }
  .cluster { position:absolute; width:1300px; height:920px; border-radius:28px; border:3px dashed rgba(255,255,255,0.22); }
  .cluster .clabel { position:absolute; left:44px; top:36px; font-family:var(--font-mono); font-size:44px; letter-spacing:0.14em; font-weight:700; }
  .node { position:absolute; padding:18px 30px; border-radius:14px; background:rgba(255,255,255,0.07); border:2px solid rgba(255,255,255,0.25); font-family:var(--font-mono); font-size:38px; white-space:nowrap; }
  .chip { position:absolute; padding:22px 38px; border-radius:999px; border:3px solid rgba(255,255,255,0.30); background:rgba(10,13,20,0.88); font-size:46px; font-weight:600; white-space:nowrap; }
  .chip.gold { border-color:var(--gold); color:var(--gold); }
  .chip.red { border-color:var(--skeptic-red); color:#ff8080; }
  .chip.cyan { border-color:var(--neon-cyan); color:var(--neon-cyan); }
  .tangle { position:absolute; inset:0; pointer-events:none; }
  .tangle path { fill:none; stroke-width:6; stroke-linecap:round; opacity:0.75; }
  .clean { position:absolute; inset:0; pointer-events:none; }
  .clean path { fill:none; stroke-width:7; stroke-linecap:round; }
  .take { position:absolute; top:1740px; width:1420px; padding:30px 40px; border-radius:18px; font-size:48px; font-weight:700; }
  .slam { position:absolute; left:0; width:3840px; text-align:center; font-weight:700; letter-spacing:-0.02em; }
  .fadeblack { position:absolute; inset:0; background:#000; pointer-events:none; }
  #s3-rw-strike { position:absolute; left:30px; top:50%; width:92%; height:8px; background:var(--skeptic-red); transform-origin:0 50%; }
"""

S3_BODY = """
    <div id="s3-cam" class="clip" data-start="0" data-duration="__DUR__" data-track-index="0">
      <div class="stage" id="s3-stage">
        <div class="grid"></div>
        <div class="scrim-b"></div>
        <div id="s3-kicker" class="kicker" style="left:420px; top:170px; opacity:0;">WHAT IT ACTUALLY DID</div>
        <div id="s3-head" class="headline" style="left:420px; top:250px; font-size:88px; opacity:0;">THE PART WORTH STEALING</div>
        <div id="s3-diagram">
          <svg class="tangle" id="s3-tangle" viewBox="0 0 3840 2160" preserveAspectRatio="none">
            <path style="stroke-dasharray:100; stroke-dashoffset:100;" id="s3-t1" pathLength="100" stroke="#61dafb" d="M 1500 900 C 1900 500, 1950 1500, 2350 950" />
            <path style="stroke-dasharray:100; stroke-dashoffset:100;" id="s3-t2" pathLength="100" stroke="#ffd166" d="M 1550 1200 C 1850 1600, 2000 700, 2300 1250" />
            <path style="stroke-dasharray:100; stroke-dashoffset:100;" id="s3-t3" pathLength="100" stroke="#61dafb" d="M 1480 1050 C 1750 1050, 2100 1080, 2380 1080" />
            <path style="stroke-dasharray:100; stroke-dashoffset:100;" id="s3-t4" pathLength="100" stroke="#ffd166" d="M 1520 760 C 1980 1250, 1880 800, 2330 780" />
            <path style="stroke-dasharray:100; stroke-dashoffset:100;" id="s3-t5" pathLength="100" stroke="#61dafb" d="M 1560 1380 C 1900 1000, 1960 1450, 2290 1400" />
          </svg>
          <svg class="clean" id="s3-clean" viewBox="0 0 3840 2160" preserveAspectRatio="none">
            <path style="stroke-dasharray:100; stroke-dashoffset:100;" id="s3-c1" pathLength="100" stroke="#61dafb" d="M 1330 950 L 2510 950" />
            <path style="stroke-dasharray:100; stroke-dashoffset:100;" id="s3-c2" pathLength="100" stroke="#ffd166" d="M 1330 1250 L 2510 1250" />
          </svg>
          <div id="s3-clA" class="cluster" style="left:420px; top:520px; opacity:0;">
            <div class="clabel" style="color:var(--neon-cyan);">CORE WEBPAGE HANDLING</div>
            <div class="node" style="left:60px; top:150px;">PAGE RENDER</div>
            <div class="node" style="left:480px; top:170px;">NAVIGATION</div>
            <div class="node" style="left:180px; top:400px;">TAB CORE</div>
            <div class="node" style="left:640px; top:430px;">PAGE LIFECYCLE</div>
            <div class="node" style="left:330px; top:660px;">INPUT ROUTING</div>
          </div>
          <div id="s3-clB" class="cluster" style="left:2120px; top:520px; opacity:0;">
            <div class="clabel" style="color:var(--gold);">EVERYDAY BROWSER FEATURES</div>
            <div class="node" style="left:60px; top:150px;">BOOKMARKS</div>
            <div class="node" style="left:520px; top:170px;">EXTENSIONS</div>
            <div class="node" style="left:200px; top:400px;">HISTORY</div>
            <div class="node" style="left:660px; top:430px;">DOWNLOADS</div>
            <div class="node" style="left:360px; top:660px;">SETTINGS</div>
          </div>
          <div id="s3-mv1" class="chip cyan" style="left:1560px; top:600px; opacity:0; font-size:40px;">TAB</div>
          <div id="s3-mv2" class="chip cyan" style="left:1980px; top:760px; opacity:0; font-size:40px;">PANEL</div>
          <div id="s3-mv3" class="chip cyan" style="left:1620px; top:1560px; opacity:0; font-size:40px;">FLOATING WINDOW</div>
          <div id="s3-crash" class="chip red" style="left:1690px; top:1000px; opacity:0; font-size:64px; font-weight:700;">CRASH</div>
          <div id="s3-rw" class="chip" style="left:1240px; top:330px; opacity:0; font-size:52px;"><span style="position:relative; display:inline-block;">REWRITE SIX MILLION LINES<span id="s3-rw-strike" style="transform:scaleX(0);"></span></span></div>
          <div id="s3-sep" class="chip gold" style="left:1560px; top:330px; opacity:0; font-size:58px; font-weight:700;">SEPARATED</div>
          <div id="s3-files" class="chip" style="left:420px; top:1560px; opacity:0;">HUNDREDS OF FILES — CLEAN CHANGES, A FEW AT A TIME</div>
          <div id="s3-chk1" class="chip cyan" style="left:420px; top:1560px; opacity:0;">PASS — CHROMIUM TEST SUITES</div>
          <div id="s3-chk2" class="chip gold" style="left:1980px; top:1560px; opacity:0;">SIGNED OFF — BY A HUMAN</div>
        </div>
        <div id="s3-take1" class="take" style="left:420px; background:rgba(97,218,251,0.12); border:2px solid var(--neon-cyan); color:#c9f2ff; opacity:0;">THE AGENT → MECHANICAL SEPARATION</div>
        <div id="s3-take2" class="take" style="left:2000px; background:rgba(255,209,102,0.12); border:2px solid var(--gold); color:#ffe9b0; opacity:0;">THE HUMAN → TESTS + REVIEW GATE</div>
        <div id="s3-slam1" class="slam" style="top:820px; font-size:140px; color:#fff; opacity:0;">AUTOMATE THE GRIND.</div>
        <div id="s3-slam2" class="slam" style="top:1010px; font-size:140px; color:var(--gold); opacity:0;">NEVER AUTOMATE THE APPROVAL.</div>
        <div class="caption-band" id="s3-captions">
__CAPTIONS__
        </div>
        <div id="s3-fade" class="fadeblack"></div>
      </div>
    </div>
"""

S3_JS = """
      const cam3 = document.getElementById("s3-cam");
      cameraPush(cam3, 0.97, 1.0, 0.4, tl, 0);
      tl.fromTo("#s3-fade", { opacity: 1 }, { opacity: 0, duration: 0.3, ease: "none" }, 0);
      tl.fromTo("#s3-fade", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "none", immediateRender: false }, __DURM__);
      tl.fromTo("#s3-kicker", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.5 }, 0.3);
      tl.fromTo("#s3-head", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.55, ease: "power3.out" }, 0.5);
      /* tangled state: clusters fade in, curves draw between them */
      tl.fromTo("#s3-clA", { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }, 6.7);
      tl.fromTo("#s3-clB", { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }, 8.6);
      ["#s3-t1", "#s3-t2", "#s3-t3", "#s3-t4", "#s3-t5"].forEach(function (p, i) {
        tl.fromTo(p, { strokeDasharray: 100, strokeDashoffset: 100 }, { strokeDashoffset: 0, duration: 0.55, ease: "power2.inOut" }, 9.0 + i * 0.28);
      });
      pinCard(document.getElementById("s3-mv1"), tl, 11.4);
      pinCard(document.getElementById("s3-mv2"), tl, 12.8);
      pinCard(document.getElementById("s3-mv3"), tl, 13.6);
      stampIn(document.getElementById("s3-crash"), tl, 14.6);
      tl.fromTo("#s3-stage", { x: 0, y: 0 }, { keyframes: [
        { x: -12, y: 7, duration: 0.05 }, { x: 10, y: -5, duration: 0.05 },
        { x: -6, y: 3, duration: 0.05 }, { x: 0, y: 0, duration: 0.05 } ] }, 14.66);
      tl.to(["#s3-mv1", "#s3-mv2", "#s3-mv3", "#s3-crash"], { opacity: 0, duration: 0.3 }, 16.0);
      /* not a rewrite — a separation */
      pinCard(document.getElementById("s3-rw"), tl, 16.8);
      tl.fromTo("#s3-rw-strike", { scaleX: 0 }, { scaleX: 1, duration: 0.35, ease: "power2.out" }, 18.3);
      tl.to("#s3-rw", { opacity: 0.35, duration: 0.3 }, 18.6);
      tl.to("#s3-clA", { x: -240, duration: 1.1, ease: "power3.inOut" }, 19.3);
      tl.to("#s3-clB", { x: 240, duration: 1.1, ease: "power3.inOut" }, 19.3);
      tl.to("#s3-tangle", { opacity: 0, duration: 0.6 }, 19.5);
      ["#s3-c1", "#s3-c2"].forEach(function (p, i) {
        tl.fromTo(p, { strokeDasharray: 100, strokeDashoffset: 100 }, { strokeDashoffset: 0, duration: 0.7, ease: "power2.inOut" }, 19.9 + i * 0.3);
      });
      tl.to("#s3-rw", { opacity: 0, duration: 0.3 }, 20.2);
      stampIn(document.getElementById("s3-sep"), tl, 20.5);
      pinCard(document.getElementById("s3-files"), tl, 20.6);
      tl.to("#s3-files", { opacity: 0, duration: 0.3 }, 23.4);
      pinCard(document.getElementById("s3-chk1"), tl, 24.2);
      pinCard(document.getElementById("s3-chk2"), tl, 26.4);
      tl.to("#s3-sep", { opacity: 0, duration: 0.3 }, 28.2);
      tl.fromTo("#s3-take1", { opacity: 0, y: 44 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 30.1);
      tl.fromTo("#s3-take2", { opacity: 0, y: 44 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 32.6);
      /* closing slam: diagram dims, the rule lands */
      tl.to("#s3-diagram", { opacity: 0.15, duration: 0.5 }, 38.2);
      tl.to(["#s3-take1", "#s3-take2"], { opacity: 0.25, duration: 0.5 }, 38.2);
      tl.fromTo("#s3-slam1", { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.7)" }, 38.6);
      tl.fromTo("#s3-slam2", { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.7)" }, 39.7);
__CAPJS__
"""

# ---------------------------------------------------------------- S4 CATCHES
S4_CSS = """
  .stage { position:absolute; inset:0; overflow:hidden; background:radial-gradient(ellipse at 50% 26%, rgba(255,59,59,0.08), rgba(5,7,11,0) 62%); }
  .scrim-b { position:absolute; inset:0; background:linear-gradient(0deg, rgba(5,7,11,0.92) 0%, rgba(5,7,11,0) 30%); }
  .kicker { position:absolute; font-family:var(--font-mono); font-weight:600; letter-spacing:0.30em; color:#ff8080; font-size:46px; }
  .headline { position:absolute; font-weight:700; letter-spacing:-0.02em; color:#fff; }
  .ccard { position:absolute; top:560px; width:960px; height:1060px; padding:52px 56px; }
  .ccard .cnum { font-family:var(--font-mono); font-weight:700; font-size:110px; color:var(--skeptic-red); line-height:1; }
  .ccard .ctitle { font-size:66px; font-weight:700; line-height:1.16; margin-top:30px; color:#fff; }
  .ccard .csub { font-size:46px; font-weight:600; color:var(--gold); margin-top:30px; line-height:1.3; }
  .price-old, .price-new { position:absolute; left:56px; top:520px; }
  .price-num { font-family:var(--font-mono); font-weight:700; font-size:128px; line-height:1; }
  .price-lbl { font-family:var(--font-mono); font-size:36px; letter-spacing:0.12em; color:rgba(255,255,255,0.65); margin-top:18px; }
  .chip { position:absolute; padding:20px 34px; border-radius:999px; border:3px solid rgba(255,255,255,0.30); background:rgba(10,13,20,0.88); font-size:42px; font-weight:600; white-space:nowrap; }
  .chip.red { border-color:var(--skeptic-red); color:#ff8080; }
  .banner { position:absolute; left:420px; top:1700px; width:3000px; text-align:center; font-weight:700; }
  .fadeblack { position:absolute; inset:0; background:#000; pointer-events:none; }
"""

S4_BODY = """
    <div id="s4-cam" class="clip" data-start="0" data-duration="__DUR__" data-track-index="0">
      <div class="stage">
        <div class="scrim-b"></div>
        <div id="s4-kicker" class="kicker" style="left:420px; top:190px; opacity:0;">WHAT BREAKS — THE HONEST CATCH</div>
        <div id="s4-head" class="headline" style="left:420px; top:270px; font-size:130px; opacity:0;">THREE CATCHES.</div>
        <div id="s4-card1" class="glass-panel ccard" style="left:420px; opacity:0;">
          <div class="cnum">1</div>
          <div class="ctitle">GOOGLE'S OWN ENGINEERS.<br/>GOOGLE'S OWN CODE.</div>
          <div class="csub" id="s4-c1-sub" style="opacity:0;">INDEPENDENT MILEAGE WILL VARY</div>
        </div>
        <div id="s4-card2" class="glass-panel ccard" style="left:1440px; opacity:0;">
          <div class="cnum">2</div>
          <div class="ctitle">NO FREE<br/>API TIER.</div>
          <div class="csub" id="s4-c2-sub" style="opacity:0;">EVERY TOKEN IS PAID</div>
        </div>
        <div id="s4-card3" class="glass-panel ccard" style="left:2460px; opacity:0;">
          <div class="cnum">3</div>
          <div class="ctitle">THE PRICE<br/>DOUBLES.</div>
          <div class="price-old" id="s4-pold" style="opacity:0;">
            <div class="price-num" style="color:var(--gold);">$2 / $10</div>
            <div class="price-lbl">PER 1M TOKENS · IN / OUT — INTRO PRICE</div>
          </div>
          <div class="price-new" id="s4-pnew" style="opacity:0;">
            <div class="price-num" style="color:var(--skeptic-red);">$4 / $20</div>
            <div class="price-lbl">PER 1M TOKENS · IN / OUT</div>
          </div>
          <div id="s4-dec1" class="chip red" style="left:56px; top:830px; opacity:0;">FROM DEC 1</div>
        </div>
        <div id="s4-banner" class="banner" style="opacity:0; font-size:84px;">THE CHEAP WINDOW CLOSES <span id="s4-nov30" style="color:var(--gold); opacity:0;">NOV 30</span></div>
        <div class="caption-band" id="s4-captions">
__CAPTIONS__
        </div>
        <div id="s4-fade" class="fadeblack"></div>
      </div>
    </div>
"""

S4_JS = """
      const cam4 = document.getElementById("s4-cam");
      cameraPush(cam4, 0.97, 1.0, 0.4, tl, 0);
      tl.fromTo("#s4-fade", { opacity: 1 }, { opacity: 0, duration: 0.3, ease: "none" }, 0);
      tl.fromTo("#s4-fade", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "none", immediateRender: false }, __DURM__);
      tl.fromTo("#s4-kicker", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.5 }, 0.3);
      tl.fromTo("#s4-head", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.55, ease: "power3.out" }, 0.6);
      pinCard(document.getElementById("s4-card1"), tl, 2.7);
      tl.fromTo("#s4-c1-sub", { opacity: 0 }, { opacity: 1, duration: 0.45 }, 9.3);
      pinCard(document.getElementById("s4-card2"), tl, 10.9);
      tl.fromTo("#s4-c2-sub", { opacity: 0 }, { opacity: 1, duration: 0.45 }, 12.4);
      pinCard(document.getElementById("s4-card3"), tl, 13.9);
      tl.fromTo("#s4-pold", { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 16.3);
      tl.to("#s4-pold", { opacity: 0, scale: 0.88, duration: 0.3, ease: "power2.in" }, 21.6);
      tl.fromTo("#s4-pnew", { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.6)" }, 21.75);
      stampIn(document.getElementById("s4-dec1"), tl, 21.95);
      tl.fromTo("#s4-banner", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 26.3);
      tl.fromTo("#s4-nov30", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, 27.9);
__CAPJS__
"""


# ---------------------------------------------------------------- S5 CHECKLIST
S5_CSS = """
  .stage { position:absolute; inset:0; overflow:hidden; }
  .scrim-b { position:absolute; inset:0; background:linear-gradient(0deg, rgba(5,7,11,0.92) 0%, rgba(5,7,11,0) 30%); }
  .kicker { position:absolute; font-family:var(--font-mono); font-weight:600; letter-spacing:0.30em; color:var(--neon-cyan); font-size:46px; }
  .headline { position:absolute; font-weight:700; letter-spacing:-0.02em; color:#fff; }
  .panel { position:absolute; left:520px; top:470px; width:2800px; height:1210px; }
  .glowframe { position:absolute; left:520px; top:470px; width:2800px; height:1210px; border-radius:12px; border:4px solid var(--gold); opacity:0; pointer-events:none; }
  .hl { position:absolute; left:496px; top:540px; width:14px; height:320px; background:var(--gold); border-radius:7px; }
  .row { position:absolute; left:600px; width:2640px; }
  .box { position:absolute; left:0; top:6px; width:104px; height:104px; border:5px solid rgba(255,255,255,0.45); border-radius:18px; }
  .box svg { position:absolute; inset:0; }
  .box path { fill:none; stroke:var(--gold); stroke-width:11; stroke-linecap:round; stroke-linejoin:round; }
  .rtext { position:absolute; left:170px; top:0; width:2400px; }
  .rtitle { font-size:66px; font-weight:700; color:#fff; line-height:1.15; }
  .rsub { font-size:47px; font-weight:600; color:rgba(255,255,255,0.78); margin-top:12px; line-height:1.3; }
  .rsub.gold { color:var(--gold); }
  .fadeblack { position:absolute; inset:0; background:#000; pointer-events:none; }
"""

def s5_row(idx, top, title, subs):
    sub_html = ''.join(f'<div class="rsub{" gold" if g else ""}" id="s5-r{idx}-sub{j}" style="opacity:0;">{s}</div>' for j, (s, g) in enumerate(subs))
    return f"""
        <div class="row" id="s5-row{idx}" style="top:{top}px; opacity:0;">
          <div class="box" id="s5-box{idx}"><svg viewBox="0 0 104 104"><path style="stroke-dasharray:100;stroke-dashoffset:100;" id="s5-chk{idx}" pathLength="100" d="M 24 56 L 44 76 L 82 30" /></svg></div>
          <div class="rtext">
            <div class="rtitle">{title}</div>
            {sub_html}
          </div>
        </div>"""

S5_BODY = """
    <div id="s5-cam" class="clip" data-start="0" data-duration="__DUR__" data-track-index="0">
      <div class="stage">
        <div class="scrim-b"></div>
        <div id="s5-kicker" class="kicker" style="left:420px; top:170px; opacity:0;">WHAT YOU CAN DO</div>
        <div id="s5-head" class="headline" style="left:420px; top:250px; font-size:96px; opacity:0;">THIS WEEK:</div>
        <div id="s5-panel" class="glass-panel panel" style="opacity:0;"></div>
        <div id="s5-hl" class="hl" style="opacity:0;"></div>
__ROWS__
        <div id="s5-glow" class="glowframe"></div>
        <div class="caption-band" id="s5-captions">
__CAPTIONS__
        </div>
        <div id="s5-fade" class="fadeblack"></div>
      </div>
    </div>
"""

S5_JS = """
      const cam5 = document.getElementById("s5-cam");
      cameraPush(cam5, 0.97, 1.0, 0.4, tl, 0);
      tl.fromTo("#s5-fade", { opacity: 1 }, { opacity: 0, duration: 0.3, ease: "none" }, 0);
      tl.fromTo("#s5-fade", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "none", immediateRender: false }, __DURM__);
      tl.fromTo("#s5-kicker", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.5 }, 0.2);
      tl.fromTo("#s5-head", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.55, ease: "power3.out" }, 0.5);
      tl.fromTo("#s5-panel", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 0.9);
      tl.fromTo("#s5-hl", { opacity: 0 }, { opacity: 1, duration: 0.4 }, 2.5);
      /* item 1 */
      tl.fromTo("#s5-row1", { opacity: 0, x: -36 }, { opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }, 2.5);
      tl.fromTo("#s5-r1-sub0", { opacity: 0 }, { opacity: 1, duration: 0.4 }, 6.7);
      tl.fromTo("#s5-r1-sub1", { opacity: 0 }, { opacity: 1, duration: 0.4 }, 8.2);
      tl.fromTo("#s5-chk1", { strokeDasharray: 100, strokeDashoffset: 100 }, { strokeDashoffset: 0, duration: 0.4, ease: "power2.out" }, 10.3);
      tl.to("#s5-box1", { borderColor: "#ffd166", duration: 0.3 }, 10.3);
      /* item 2 */
      tl.to("#s5-hl", { y: 370, duration: 0.45, ease: "power2.inOut" }, 11.2);
      tl.fromTo("#s5-row2", { opacity: 0, x: -36 }, { opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }, 11.2);
      tl.fromTo("#s5-r2-sub0", { opacity: 0 }, { opacity: 1, duration: 0.4 }, 15.2);
      tl.fromTo("#s5-chk2", { strokeDasharray: 100, strokeDashoffset: 100 }, { strokeDashoffset: 0, duration: 0.4, ease: "power2.out" }, 16.5);
      tl.to("#s5-box2", { borderColor: "#ffd166", duration: 0.3 }, 16.5);
      /* item 3 */
      tl.to("#s5-hl", { y: 740, duration: 0.45, ease: "power2.inOut", immediateRender: false }, 17.8);
      tl.fromTo("#s5-row3", { opacity: 0, x: -36 }, { opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }, 17.8);
      tl.fromTo("#s5-r3-sub0", { opacity: 0 }, { opacity: 1, duration: 0.4 }, 20.0);
      tl.fromTo("#s5-chk3", { strokeDasharray: 100, strokeDashoffset: 100 }, { strokeDashoffset: 0, duration: 0.4, ease: "power2.out" }, 21.8);
      tl.to("#s5-box3", { borderColor: "#ffd166", duration: 0.3 }, 21.8);
      tl.fromTo("#s5-r3-sub1", { opacity: 0 }, { opacity: 1, duration: 0.45 }, 24.0);
      tl.fromTo("#s5-glow", { opacity: 0 }, { opacity: 0.55, duration: 0.8, ease: "power1.inOut" }, 25.4);
__CAPJS__
"""

# ---------------------------------------------------------------- S6 OUTRO
S6_CSS = """
  .stage { position:absolute; inset:0; overflow:hidden; }
  .scrim-b { position:absolute; inset:0; background:linear-gradient(0deg, rgba(5,7,11,0.92) 0%, rgba(5,7,11,0) 30%); }
  .kicker { position:absolute; font-family:var(--font-mono); font-weight:600; letter-spacing:0.30em; color:var(--neon-cyan); font-size:46px; }
  .bigcard { position:absolute; left:720px; top:520px; width:2400px; padding:64px 70px; text-align:center; }
  .bigcard .blab { font-family:var(--font-mono); font-size:52px; letter-spacing:0.26em; font-size:52px; }
  .bigcard .btext { font-size:86px; font-weight:700; line-height:1.18; color:#fff; margin-top:26px; }
  #s6-slash { position:absolute; left:-40px; top:56%; width:2480px; height:12px; background:var(--skeptic-red); transform-origin:0 50%; }
  .mono-big { font-family:var(--font-mono); font-weight:700; font-size:150px; line-height:1.1; margin-top:30px; }
  .chip { position:absolute; padding:24px 42px; border-radius:999px; border:3px solid rgba(255,255,255,0.30); background:rgba(10,13,20,0.88); font-size:50px; font-weight:600; white-space:nowrap; }
  .chip.gold { border-color:var(--gold); color:var(--gold); }
  .welcome { position:absolute; left:0; width:3840px; text-align:center; }
  .arrowimg { position:absolute; left:540px; top:430px; width:860px; height:860px; object-fit:cover; border-radius:44px; border:4px solid rgba(255,209,102,0.75); box-shadow:0 30px 90px rgba(0,0,0,0.55); }
  .wordmark { position:absolute; left:1560px; top:520px; font-size:176px; font-weight:700; letter-spacing:-0.02em; color:#fff; }
  .catch { position:absolute; left:1560px; top:780px; width:1900px; font-size:86px; font-weight:600; line-height:1.25; color:#fff; }
  .subbtn { position:absolute; left:1560px; top:1140px; background:var(--skeptic-red); color:#fff; font-weight:700; border-radius:999px; padding:34px 76px; font-size:64px; }
  .tagline { position:absolute; left:1560px; top:1420px; font-family:var(--font-mono); font-size:48px; letter-spacing:0.18em; color:var(--neon-cyan); }
  .fadeblack { position:absolute; inset:0; background:#000; pointer-events:none; }
"""

S6_BODY = """
    <div id="s6-cam" class="clip" data-start="0" data-duration="__DUR__" data-track-index="0">
      <div class="stage">
        <div class="scrim-b"></div>
        <div id="s6-kicker" class="kicker" style="left:420px; top:190px; opacity:0;">THE REAL STORY</div>
        <div id="s6-bad" class="glass-panel bigcard" style="opacity:0;">
          <div class="blab" style="color:#ff8080;">NOT THIS</div>
          <div class="btext">A MODEL THAT MAGICALLY<br/>FIXES OLD CODE</div>
          <div id="s6-slash" style="transform:rotate(-3deg) scaleX(0);"></div>
        </div>
        <div id="s6-flow" class="glass-panel bigcard" style="opacity:0;">
          <div class="blab" style="color:var(--neon-cyan);">THIS</div>
          <div class="btext">A WORKFLOW THAT TURNS</div>
          <div class="mono-big"><span id="s6-months" style="opacity:0;">MONTHS</span> <span id="s6-arrow" style="color:rgba(255,255,255,0.55); opacity:0;">→</span> <span id="s6-weeks" style="color:var(--gold); opacity:0;">WEEKS</span></div>
        </div>
        <div id="s6-gate" class="chip gold" style="left:1240px; top:1230px; opacity:0;">WITH HUMANS HOLDING THE GATE</div>
        <div id="s6-welcome" class="welcome" style="top:600px; opacity:0;">
          <div style="font-size:124px; font-weight:700; color:#fff;">NEW HERE? WELCOME.</div>
          <div id="s6-wsub1" style="font-size:64px; font-weight:600; color:rgba(255,255,255,0.82); margin-top:44px; opacity:0;">ONE AI DEVELOPMENT AT A TIME.</div>
          <div id="s6-wsub2" style="font-size:64px; font-weight:700; color:var(--gold); margin-top:20px; opacity:0;">EVIDENCE ON SCREEN — EVERY TIME.</div>
        </div>
        <div id="s6-end" style="position:absolute; inset:0; opacity:0;">
          <img class="arrowimg" id="s6-arrowimg" src="assets/img/brass_arrow.webp" alt="" />
          <div class="wordmark">AHEAD OF RUSH AI</div>
          <div class="catch">We don't chase the future.<br/><span style="color:var(--gold);">We check it.</span></div>
          <div class="subbtn" id="s6-sub">SUBSCRIBE</div>
          <div class="tagline">AHEAD OF RUSH AI — CONFIRMED, NOT JUST CLAIMED.</div>
        </div>
        <div class="caption-band" id="s6-captions">
__CAPTIONS__
        </div>
        <div id="s6-fade" class="fadeblack"></div>
      </div>
    </div>
"""

S6_JS = """
      const cam6 = document.getElementById("s6-cam");
      cameraPush(cam6, 0.97, 1.0, 0.4, tl, 0);
      tl.fromTo("#s6-fade", { opacity: 1 }, { opacity: 0, duration: 0.3, ease: "none" }, 0);
      tl.fromTo("#s6-fade", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "none", immediateRender: false }, __DURM__);
      tl.fromTo("#s6-kicker", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.5 }, 0.3);
      pinCard(document.getElementById("s6-bad"), tl, 1.5);
      tl.fromTo("#s6-slash", { scaleX: 0, rotation: -3 }, { scaleX: 1, rotation: -3, duration: 0.35, ease: "power2.out" }, 2.8);
      tl.to("#s6-bad", { opacity: 0, scale: 0.94, duration: 0.35, ease: "power2.in" }, 4.05);
      pinCard(document.getElementById("s6-flow"), tl, 4.3);
      tl.fromTo("#s6-months", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.35 }, 5.3);
      tl.fromTo("#s6-arrow", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 6.4);
      tl.fromTo("#s6-weeks", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, 7.3);
      pinCard(document.getElementById("s6-gate"), tl, 8.2);
      tl.to(["#s6-flow", "#s6-gate"], { opacity: 0, y: -30, duration: 0.4, ease: "power2.in" }, 10.15);
      tl.fromTo("#s6-welcome", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 10.4);
      tl.fromTo("#s6-wsub1", { opacity: 0 }, { opacity: 1, duration: 0.45 }, 12.1);
      tl.fromTo("#s6-wsub2", { opacity: 0 }, { opacity: 1, duration: 0.45 }, 14.5);
      tl.to("#s6-welcome", { opacity: 0, y: -30, duration: 0.4, ease: "power2.in" }, 16.35);
      tl.to("#s6-end", { opacity: 1, duration: 0.5 }, 16.6);
      tl.fromTo("#s6-arrowimg", { scale: 0.8, rotation: -4 }, { scale: 1, rotation: 0, duration: 0.55, ease: "back.out(1.6)" }, 16.7);
      tl.fromTo("#s6-sub", { scale: 0.7 }, { scale: 1, duration: 0.4, ease: "back.out(2.2)" }, 17.1);
      pulseBadge(document.getElementById("s6-sub"), tl, 18.4);
__CAPJS__
"""

# ---------------------------------------------------------------- SFX + INDEX
# (scene, local_start, file, clip_duration, volume)
SFX = [
    (1, 5.3, 'thump.wav', 0.50, 1), (1, 6.3, 'card-pin.wav', 0.14, 0.7),
    (1, 7.15, 'card-pin.wav', 0.14, 0.7), (1, 8.2, 'card-pin.wav', 0.14, 0.7),
    (1, 11.4, 'card-pin.wav', 0.14, 0.7), (1, 21.2, 'tick.wav', 0.09, 0.9),
    (2, 15.5, 'thump.wav', 0.50, 1), (2, 20.2, 'thump.wav', 0.50, 1),
    (2, 31.8, 'card-pin.wav', 0.14, 0.7), (2, 32.6, 'card-pin.wav', 0.14, 0.7),
    (2, 33.7, 'card-pin.wav', 0.14, 0.7),
    (3, 19.3, 'string-snap.wav', 0.45, 0.8), (3, 24.2, 'card-pin.wav', 0.14, 0.7),
    (3, 26.4, 'card-pin.wav', 0.14, 0.7), (3, 38.6, 'thump.wav', 0.50, 1),
    (4, 2.7, 'card-pin.wav', 0.14, 0.7), (4, 10.9, 'card-pin.wav', 0.14, 0.7),
    (4, 21.75, 'thump.wav', 0.50, 1),
    (5, 10.3, 'tick.wav', 0.09, 0.9), (5, 16.5, 'tick.wav', 0.09, 0.9),
    (5, 21.8, 'tick.wav', 0.09, 0.9),
    (6, 17.1, 'thump.wav', 0.50, 1),
]
SIDS = {1: 's1_hook', 2: 's2_evidence', 3: 's3_separation', 4: 's4_catches', 5: 's5_checklist', 6: 's6_outro'}


def fmt(x):
    return '%g' % round(x, 3)


def write_index():
    mounts, audios = [], []
    for n in range(1, 7):
        sid = SIDS[n]
        mounts.append(f'''      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{fmt(STARTS[n])}" data-duration="{fmt(SCENE_DUR[n])}" data-track-index="0" data-track-kind="graphics" data-width="3840" data-height="2160"></div>''')
        audios.append(f'''      <audio id="vo-s{n}" class="clip" data-start="{fmt(STARTS[n])}" data-duration="{fmt(VO_DUR[n])}" data-track-index="1" data-volume="1" src="assets/audio/vo_s{n}.mp3"></audio>''')
    audios.append(f'''      <audio id="music" class="clip" data-start="0" data-duration="{fmt(TOTAL)}" data-track-index="2" data-volume="1" src="assets/audio/music.mp3"></audio>''')
    for i, (sn, t, f, d, v) in enumerate(SFX):
        audios.append(f'''      <audio id="sfx-{i}" class="clip" data-start="{fmt(STARTS[sn] + t)}" data-duration="{fmt(d)}" data-track-index="3" data-volume="{fmt(v)}" src="assets/audio/sfx/{f}"></audio>''')
    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=3840, height=2160" />
    <script src="assets/js/gsap.min.js"></script>
    <link rel="stylesheet" href="css/theme.css" />
    <style>
      html, body {{ width: 3840px; height: 2160px; background: var(--dark-bg); }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: var(--dark-bg); }}
    </style>
  </head>
  <body>
    <!-- Ahead of Rush AI — Gemini 4 Argon video. Scene durations = real VO + 1.2s
         tail. Starts: {[STARTS[n] for n in range(1, 7)]}, total {TOTAL}s. -->
    <div id="root" data-composition-id="ctrl-ahead-argon" data-start="0" data-duration="{fmt(TOTAL)}" data-width="3840" data-height="2160">
{chr(10).join(mounts)}
{chr(10).join(audios)}
    </div>
    <script src="js/shared.js"></script>
    <script>
      (function () {{
        const tl = makeSceneTimeline("ctrl-ahead-argon", {fmt(TOTAL)});
        window.__timelines["ctrl-ahead-argon"] = tl;
      }})();
    </script>
  </body>
</html>
"""
    with open(f'{ROOT}/index.html', 'w') as fh:
        fh.write(html)
    timing = {'vo_dur': VO_DUR, 'scene_dur': SCENE_DUR, 'starts': STARTS, 'total': TOTAL,
              'sids': SIDS, 'sfx': [list(s) for s in SFX]}
    json.dump(timing, open(f'{ROOT}/work/timing.json', 'w'), indent=1)
    print('wrote index.html, total', TOTAL)


def main():
    rows = (s5_row(1, 540, 'PICK ONE TANGLED MODULE',
                   [('Not the whole repo.', False), ('Run a separation pass — tests as the gate.', False)])
            + s5_row(2, 910, 'RUN YOUR ARGON EVAL EARLY',
                     [('Before November 30 — while it&rsquo;s half price.', False)])
            + s5_row(3, 1280, 'KEEP A HUMAN REVIEW STEP',
                     [('On every change.', False), ('That&rsquo;s how the Chromium result was produced.', True)]))
    s5_body = S5_BODY.replace('__ROWS__', rows)
    scene(1, SIDS[1], S1_CSS, S1_BODY, S1_JS)
    scene(2, SIDS[2], S2_CSS, S2_BODY, S2_JS)
    scene(3, SIDS[3], S3_CSS, S3_BODY, S3_JS)
    scene(4, SIDS[4], S4_CSS, S4_BODY, S4_JS)
    scene(5, SIDS[5], S5_CSS, s5_body, S5_JS)
    scene(6, SIDS[6], S6_CSS, S6_BODY, S6_JS)
    write_index()


if __name__ == '__main__':
    main()
