#!/usr/bin/env python3
"""Fix v9 timeline: original v9-render.mp4 is 310.7s because sentence
pauses (gaps) were dropped from the concat and -shortest truncated the
351.888s voiceover. This rebuild keeps every sentence starting at its
original Whisper time: insert a hold-frame gap clip after each sentence
where the next sentence starts later, trim the last clip where the next
sentence overlaps, and add a 0.288s tail hold so the video matches the
full voiceover. Subtitle timings (original Whisper times) then align."""
import json, pathlib, subprocess, sys

base = pathlib.Path.home() / "workspace/goals/ctrl-ahead-os-ai-video/files/pipeline/data/portfolio/2026-W43/005-model-leaks"
v9 = base / "v9"
fix = v9 / "fix"
fix.mkdir(exist_ok=True)
plan = json.load(open(v9 / "plan.json"))
VO_LEN = 351.888

def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def make_gap(img_name, dur, out):
    if out.exists():
        return
    img = v9 / "bannered" / f"{img_name}.jpg"
    run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(img),
         "-t", str(dur), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", str(out)])

def trim_clip(src, dur, out):
    if out.exists():
        return
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-t", str(dur),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an", str(out)])

lst = []
for i, p in enumerate(plan):
    cuts = p["cuts"]
    nclips = len(cuts) - 1
    for ci in range(nclips):
        seg_dur = cuts[ci + 1] - cuts[ci]
        if seg_dur < 0.01:
            continue  # zero-length cut point in plan; contributes no time
        src = v9 / "clips" / f"s{p['sentence']:02d}_c{ci}.mp4"
        if not src.exists():
            # short segment the original render skipped (dur < 0.2s); generate it here
            gen = fix / f"s{p['sentence']:02d}_c{ci}_gen.mp4"
            if not gen.exists():
                img = v9 / "bannered" / f"{p['image']}.jpg"
                is_proof = p["image"].startswith("proof")
                if is_proof:
                    z = "min(1.30+0.15*on/(%d),1.45)" % max(1, int(seg_dur * 30))
                    x = "(iw-iw/zoom)*on/(%d)" % max(1, int(seg_dur * 30)); y = "(ih-ih/zoom)*0.5"
                elif ci > 0:
                    z = "min(1.14+0.08*on/(%d),1.22)" % max(1, int(seg_dur * 30)); x = "iw/2-(iw/zoom/2)"; y = "ih/2-(ih/zoom/2)"
                else:
                    z = "min(1.00+0.12*on/(%d),1.12)" % max(1, int(seg_dur * 30)); x = "iw/2-(iw/zoom/2)"; y = "ih/2-(ih/zoom/2)"
                run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(img),
                     "-vf", f"zoompan=z='{z}':x='{x}':y='{y}':d={max(1, int(seg_dur * 30))}:s=1920x1080:fps=30",
                     "-t", str(seg_dur), "-c:v", "libx264", "-pix_fmt", "yuv420p", str(gen)])
            src = gen
        # Overlap: next sentence starts before this one ends -> trim last clip
        if ci == nclips - 1 and i + 1 < len(plan) and plan[i + 1]["start"] < p["end"]:
            trimmed_dur = plan[i + 1]["start"] - cuts[ci]
            out = fix / f"s{p['sentence']:02d}_c{ci}_trim.mp4"
            trim_clip(src, trimmed_dur, out)
            lst.append(str(out))
        else:
            lst.append(str(src))
    if i + 1 < len(plan):
        gap = plan[i + 1]["start"] - p["end"]
        if gap > 0.01:
            out = fix / f"gap_after_s{p['sentence']:02d}.mp4"
            make_gap(p["image"], gap, out)
            lst.append(str(out))
    else:
        tail = VO_LEN - p["end"]
        if tail > 0.01:
            out = fix / "tail.mp4"
            make_gap(p["image"], tail, out)
            lst.append(str(out))

with open(fix / "concat.txt", "w") as f:
    for x in lst:
        f.write(f"file '{x}'\n")
print("concat entries:", len(lst), flush=True)
out = v9 / "v9-render-fixed.mp4"
run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(fix / "concat.txt"),
     "-i", str(base / "vo2" / "vo.mp3"),
     "-vf", f"subtitles={v9/'tiktok9.ass'}:force_style='Fontname=DejaVu Sans,Fontsize=88'",
     "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-t", str(VO_LEN), str(out)])
print("FIXED RENDER DONE:", out, flush=True)
