#!/usr/bin/env python3
"""Per-scene render for the Ctrl-Ahead Argon video (pattern proven on the
Muse Comeback build): generate a temp root mounting ONE scene at local
time 0 with its VO, its slice of the music bed, and its SFX; render it;
repeat. Usage: render_scenes.py [scene numbers...] (default: all)."""
import json, os, subprocess, sys

ROOT = os.path.expanduser('~/workspace/ctrl-ahead-argon')
T = json.load(open(f'{ROOT}/work/timing.json'))
VO_DUR = {int(k): v for k, v in T['vo_dur'].items()}
SCENE_DUR = {int(k): v for k, v in T['scene_dur'].items()}
STARTS = {int(k): v for k, v in T['starts'].items()}
SIDS = {int(k): v for k, v in T['sids'].items()}
SFX = T['sfx']

TEMPLATE = """<!doctype html>
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
    <div id="root" data-composition-id="ctrl-ahead-argon" data-start="0" data-duration="{dur}" data-width="3840" data-height="2160">
      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="0" data-duration="{dur}" data-track-index="0" data-track-kind="graphics" data-width="3840" data-height="2160"></div>
      <audio id="vo-s{n}" class="clip" data-start="0" data-duration="{vodur}" data-track-index="1" data-volume="1" src="assets/audio/vo_s{n}.mp3"></audio>
      <audio id="music" class="clip" data-start="0" data-duration="{dur}" data-track-index="2" data-volume="1" src="renders/_work/music_s{n}.mp3"></audio>
{sfx}    </div>
    <script src="js/shared.js"></script>
    <script>
      (function () {{
        const tl = makeSceneTimeline("ctrl-ahead-argon", {dur});
        window.__timelines["ctrl-ahead-argon"] = tl;
      }})();
    </script>
  </body>
</html>
"""


def fmt(x):
    return '%g' % round(x, 3)


def render_scene(n):
    sid, dur, vodur = SIDS[n], SCENE_DUR[n], VO_DUR[n]
    slice_path = f'{ROOT}/renders/_work/music_s{n}.mp3'
    subprocess.run(['ffmpeg', '-v', 'error', '-ss', fmt(STARTS[n]), '-t', fmt(dur),
                    '-i', f'{ROOT}/assets/audio/music.mp3', '-c:a', 'libmp3lame',
                    '-q:a', '2', '-y', slice_path], check=True)
    sfx_html = ''
    for i, (sn, t, f, d, v) in enumerate([s for s in SFX if s[0] == n]):
        sfx_html += (f'      <audio id="sfx-{n}-{i}" class="clip" data-start="{fmt(t)}" '
                     f'data-duration="{fmt(d)}" data-track-index="3" data-volume="{fmt(v)}" '
                     f'src="assets/audio/sfx/{f}"></audio>\n')
    html = TEMPLATE.format(n=n, sid=sid, dur=fmt(dur), vodur=fmt(vodur), sfx=sfx_html)
    tmp = f'{ROOT}/tmp-root-s{n}.html'
    with open(tmp, 'w') as fh:
        fh.write(html)
    env = dict(os.environ, TMPDIR=os.path.expanduser('~/workspace/muse-comeback-v2/.hf-cache'))
    r = subprocess.run(['npx', '--yes', 'hyperframes@0.8.210', 'render', '.',
                        '--composition', f'tmp-root-s{n}.html', '--resolution', 'landscape',
                        '-f', '30', '-o', f'renders/s{n}.mp4'],
                       cwd=ROOT, env=env, capture_output=True, text=True)
    tail = (r.stdout + r.stderr)[-600:]
    os.remove(tmp)
    out = f'{ROOT}/renders/s{n}.mp4'
    ok = r.returncode == 0 and os.path.exists(out)
    print(f'--- scene {n}: rc={r.returncode} ok={ok}')
    print(tail)
    if ok:
        p = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration,size',
                            '-show_entries', 'stream=codec_type,width,height', '-of', 'csv', out],
                           capture_output=True, text=True)
        print(p.stdout)
    return ok


if __name__ == '__main__':
    scenes = [int(x) for x in sys.argv[1:]] or [1, 2, 3, 4, 5, 6]
    results = {n: render_scene(n) for n in scenes}
    print('RESULTS', results)
    sys.exit(0 if all(results.values()) else 1)
