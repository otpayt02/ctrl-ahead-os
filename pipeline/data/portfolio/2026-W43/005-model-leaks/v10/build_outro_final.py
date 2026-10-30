#!/usr/bin/env python3
import json, pathlib, subprocess, sys, re
BASE = pathlib.Path.home()/"workspace/goals/ctrl-ahead-os-ai-video/files/pipeline/data/portfolio/2026-W43/005-model-leaks"
V10 = BASE/"v10"; SEG = V10/"segments"; TXT = V10/"texts"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
ARROW = V10/"outro-arrow.jpg"
def run(cmd):
    r=subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if r.returncode!=0:
        print("FAILED:", " ".join(cmd)); print(r.stderr[-2000:]); sys.exit(1)
def txtfile(name, s):
    p=TXT/name; p.write_text(s); return str(p)
def render(name, image, dur, vf_extra, motion):
    out=SEG/f"{name}.mp4"
    if out.exists(): return str(out)
    vf=[motion]+vf_extra
    run(["ffmpeg","-y","-v","error","-loop","1","-i",str(image),"-t",f"{dur:.3f}","-vf",",".join(vf),"-r","30","-c:v","libx264","-pix_fmt","yuv420p","-an",str(out)])
    return str(out)
# Outro beats by time (outro VO 25.92s): welcome 0-12, subscribe popup 12-19, catchphrase 19-23.5, brand 23.5-25.92
beats=[]
# beat 1: arrow, pan-left
beats.append(render("outro_b1", ARROW, 12.0, [], "scale=2560:1440,crop=1920:1080:x='640*(1-t/12.000)':y=180"))
# beat 2: SUBSCRIBE popup: drawbox + drawtext, slide-right motion
tf_sub=txtfile("out_sub.txt","SUBSCRIBE")
beats.append(render("outro_b2", ARROW, 7.0, [
 f"drawbox=x=560:y=120:w=800:h=140:color=0xFFD700@0.9:t=fill",
 f"drawtext=fontfile={FONT}:textfile='{tf_sub}':fontsize=88:fontcolor=black:x=(w-text_w)/2:y=145",
], "scale=2560:1440,crop=1920:1080:x='640*(t/7.000)':y=180"))
# beat 3: catchphrase two lines
tf_c1=txtfile("out_c1.txt","We don't chase the future.")
tf_c2=txtfile("out_c2.txt","We check it.")
beats.append(render("outro_b3", ARROW, 4.5, [
 f"drawtext=fontfile={FONT}:textfile='{tf_c1}':fontsize=72:fontcolor=white:x=(w-text_w)/2:y=80:shadowcolor=black:shadowx=3:shadowy=3",
 f"drawtext=fontfile={FONT}:textfile='{tf_c2}':fontsize=96:fontcolor=0xFFD700:x=(w-text_w)/2:y=180:shadowcolor=black:shadowx=3:shadowy=3",
], "scale=2560:1440,crop=1920:1080:x=0:y=0"))
# beat 4: final brand
tf_b=txtfile("out_brand.txt","Ctrl-Ahead — confirmed, not just claimed.")
beats.append(render("outro_b4", ARROW, 2.42, [
 f"drawtext=fontfile={FONT}:textfile='{tf_b}':fontsize=64:fontcolor=0xFFD700:x=(w-text_w)/2:y=80:shadowcolor=black:shadowx=3:shadowy=3",
], "scale=1920:1440,crop=1920:1080:x=0:y='360*(t/2.420)'"))
# fade segment 0.5s black
fade=SEG/"fade.mp4"
if not fade.exists():
    run(["ffmpeg","-y","-v","error","-f","lavfi","-i","color=c=black:s=1920x1080:r=30:d=0.5","-c:v","libx264","-pix_fmt","yuv420p","-an",str(fade)])
# audio: main VO + 0.5s silence + outro
sil=V10/"silence.mp3"
if not sil.exists():
    run(["ffmpeg","-y","-v","error","-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-t","0.5","-c:a","libmp3lame",str(sil)])
audio=V10/"audio_full.mp3"
if not audio.exists():
    run(["ffmpeg","-y","-v","error","-i",str(BASE/"vo2/vo.mp3"),"-i",str(sil),"-i",str(V10/"outro.mp3"),"-filter_complex","[0:a][1:a][2:a]concat=n=3:v=0:a=1[a]","-map","[a]","-c:a","libmp3lame",str(audio)])
# subtitles: extend fixed ASS with outro groups
script_text = "And hey welcome to Ctrl-Ahead. This is the first video, so if you made it this far, you're early, and early is exactly where you want to be. Next time, we won't just check the hype, we'll test what actually shipped, on a real machine, and show you the receipts. So hit subscribe, and bring your skepticism. Because here, we don't chase the future. We check it. Ctrl-Ahead confirmed, not just claimed."
script_words = script_text.replace("—"," ").split()
wdata=json.load(open(V10/"outro_words.json"))
ww=[]
for seg in wdata: ww.extend(seg["words"])
# align script words to whisper times by index, monotonic
times=[]
prev=0
for i,w in enumerate(script_words):
    if i < len(ww):
        a,b = ww[i]["start"], ww[i]["end"]
    else:
        a,b = prev+0.2, prev+0.4
    if a < prev: a=prev
    if b<=a: b=a+0.2
    times.append((a,b)); prev=b
OFFSET = 351.888+0.5
def fmt(t):
    cs=int(round(t*100)); h=cs//360000; m=(cs%360000)//6000; s=(cs%6000)//100; c=cs%100
    return f"{h}:{m:02d}:{s:02d}.{c:02d}"
fixed = (BASE/"v9/tiktok9_fixed.ass").read_text()
# fixed ASS header+events: keep as-is, append outro events
out_events=[]
i=0
while i < len(script_words):
    n=4 if len(script_words)-i>=4 else len(script_words)-i
    gws=script_words[i:i+n]; gwt=times[i:i+n]
    gs=OFFSET+gwt[0][0]; ge=OFFSET+gwt[-1][1]
    raw=[]
    for k in range(n):
        d = (gwt[k+1][0]-gwt[k][0]) if k<n-1 else (gwt[k][1]-gwt[k][0])
        raw.append(max(0.02,d))
    tot=sum(raw); target=ge-gs
    durs=[max(2,int(round(r/tot*target*100))) for r in raw]
    text="".join(f"{{\\k{d}}}{w} " for w,d in zip(gws,durs)).strip()
    out_events.append((gs,ge,text)); i+=n
# enforce no overlaps
clean=[]
for idx,(gs,ge,text) in enumerate(out_events):
    if idx+1 < len(out_events) and out_events[idx+1][0]<=gs: continue
    if idx+1 < len(out_events): ge=min(ge, out_events[idx+1][0])
    if ge>gs: clean.append((gs,ge,text))
with open(V10/"tiktok10.ass","w") as f:
    f.write(fixed)
    if not fixed.endswith("\n"): f.write("\n")
    for gs,ge,text in clean:
        f.write(f"Dialogue: 0,{fmt(gs)},{fmt(ge)},TikTok,,0,0,0,,{text}\n")
print("outro beats:", beats, "outro groups:", len(clean))
# final concat list
main=json.load(open(V10/"main_plan.json"))
allv = main["concat"] + [str(fade)] + beats
with open(V10/"concat_final.txt","w") as f:
    for x in allv: f.write(f"file '{x}'\n")
print("final segments:", len(allv))
# final render
run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",str(V10/"concat_final.txt"),"-i",str(audio),
     "-vf",f"subtitles={V10/'tiktok10.ass'}:force_style='Fontname=DejaVu Sans,Fontsize=88'",
     "-c:v","libx264","-pix_fmt","yuv420p","-r","30","-c:a","aac",str(V10/"v10-render.mp4")])
print("V10 DONE")
