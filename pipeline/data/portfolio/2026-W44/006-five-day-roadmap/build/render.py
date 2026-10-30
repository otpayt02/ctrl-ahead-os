#!/usr/bin/env python3
import json, pathlib, subprocess, sys
BASE=pathlib.Path(__file__).parent
def run(cmd):
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode!=0:
        print("FAILED"," ".join(map(str,cmd))[:500]); print(r.stderr[-4000:]); sys.exit(1)
tl=json.load(open(BASE/"timeline.json")); timeline=tl["timeline"]; total=tl["total"]; seg_start=tl["seg_start"]
chips=json.load(open(BASE/"chip_times.json"))
SEGDIR=BASE/"segments"; SEGDIR.mkdir(exist_ok=True)
concat=[]
def render_clip(name, slide, dur, chip_list):
    """chip_list: [(png, local_start, scale_h_or_None)] cumulative pop-in"""
    out=SEGDIR/f"{name}.mp4"
    if out.exists(): concat.append(out); return
    inputs=["-loop","1","-t",str(dur),"-i",str(BASE/"slides"/slide)]
    for png,_,_ in chip_list: inputs+=["-i",str(png)]
    fc=[]
    last="[0:v]"
    n=len(chip_list)
    step = 128 if n<=4 else 110 if n==5 else 88
    for i,(png,st,_) in enumerate(chip_list):
        y=380+i*step
        src=f"[{i+1}:v]"
        if n>4:
            fc.append(f"{src}scale=1060:{step-6}[c{i}]"); src=f"[c{i}]"
        fc.append(f"{last}{src}overlay=70:{y}:enable='gte(t,{max(0,st):.3f})'[v{i}]"); last=f"[v{i}]"
    fc.append(f"{last}format=yuv420p[out]")
    cmd=["ffmpeg","-y","-v","error"]+inputs+["-filter_complex",";".join(fc),"-map","[out]","-r","30","-c:v","libx264","-preset","veryfast","-crf","19","-t",str(dur),str(out)]
    run(cmd); concat.append(out); print("clip",name,dur,flush=True)

for item in timeline:
    if item["kind"]=="daycard":
        render_clip(f"day_{item['file'][:-4]}", item["file"], item["dur"], [])
    elif item["kind"]=="outro":
        render_clip("outro", "outro.jpg", item["dur"], [])
    else:
        sid=item["id"]; start=item["start"]; dur=item["dur"]
        if sid=="s01":
            # HOOK FALLBACK MONTAGE: 3 still plates, quick cuts at thirds; chips flash in their third
            third=dur/3
            for pi,plate in enumerate(["s01.jpg","s01_b.jpg","s01_c.jpg"]):
                cl=[]
                for ci,(label,gt) in enumerate(chips[sid]):
                    lt=gt-start-pi*third
                    if 0 <= lt < third: cl.append((BASE/"overlays"/f"{sid}_chip{ci}.png", lt, None))
                render_clip(f"s01_p{pi}", plate, third, cl)
        else:
            cl=[]
            for ci,(label,gt) in enumerate(chips[sid]):
                cl.append((BASE/"overlays"/f"{sid}_chip{ci}.png", gt-start, None))
            render_clip(sid, f"{sid}.jpg", dur, cl)
# concat video
with open(BASE/"concat_video.txt","w") as f:
    for p in concat: f.write(f"file '{p.name}'\n")
run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",str(BASE/"concat_video.txt"),"-c","copy",str(BASE/"video_silent.mp4")])
print("video_silent done")
# audio: VO track via adelay mix
inputs=[]; fc=[]
import sys as _s; _s.path.insert(0,str(BASE))
from segments_data import SEGMENTS
for i,s in enumerate(SEGMENTS):
    inputs+=["-i",str(BASE/"vo"/f"{s['id']}.mp3")]
    ms=int(seg_start[s['id']]*1000); fc.append(f"[{i}:a]adelay={ms}|{ms},apad[vo{i}]")
fc.append("".join(f"[vo{i}]" for i in range(len(SEGMENTS)))+f"amix=inputs={len(SEGMENTS)}:normalize=0,atrim=0:{total:.3f}[vo]")
run(["ffmpeg","-y","-v","error"]+inputs+["-filter_complex",";".join(fc),"-map","[vo]","-c:a","pcm_s16le",str(BASE/"vo_track.wav")])
print("vo_track done")
