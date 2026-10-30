import json, pathlib, subprocess, os
base = pathlib.Path.home()/"workspace/goals/ctrl-ahead-os-ai-video/files/pipeline/data/portfolio/2026-W43/005-model-leaks"
v9 = base/"v9"; plan=json.load(open(v9/"plan.json"))
tmp = v9/"clips"; tmp.mkdir(exist_ok=True)
lst=[]
for p in plan:
    img = v9/"bannered"/f"{p['image']}.jpg"
    is_proof = p["image"].startswith("proof")
    for ci in range(len(p["cuts"])-1):
        a,b = p["cuts"][ci], p["cuts"][ci+1]
        dur = b-a
        if dur < 0.2: continue
        out = tmp/f"s{p['sentence']:02d}_c{ci}.mp4"
        if not out.exists():
            if is_proof:
                z="min(1.30+0.15*on/(%d),1.45)" % max(1,int(dur*30))
                x="(iw-iw/zoom)*on/(%d)" % max(1,int(dur*30))
                y="(ih-ih/zoom)*0.5"
            elif ci>0:  # after a comma: pulse up
                z="min(1.14+0.08*on/(%d),1.22)" % max(1,int(dur*30)); x="iw/2-(iw/zoom/2)"; y="ih/2-(ih/zoom/2)"
            else:
                z="min(1.00+0.12*on/(%d),1.12)" % max(1,int(dur*30)); x="iw/2-(iw/zoom/2)"; y="ih/2-(ih/zoom/2)"
            cmd=["ffmpeg","-y","-v","error","-loop","1","-i",str(img),"-vf",f"zoompan=z='{z}':x='{x}':y='{y}':d={max(1,int(dur*30))}:s=1920x1080:fps=30","-t",str(dur),"-c:v","libx264","-pix_fmt","yuv420p",str(out)]
            subprocess.run(cmd, check=True)
        lst.append(str(out))
        print(f"clip {p['sentence']} cut {ci} {dur:.2f}s", flush=True)
with open(v9/"concat.txt","w") as f:
    for x in lst: f.write(f"file '{x}'\n")
print("clips:", len(lst))
# concat + audio + subtitles
subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",str(v9/"concat.txt"),"-i",str(base/"vo2/vo.mp3"),"-vf",f"subtitles={v9/'tiktok9.ass'}:force_style='Fontname=DejaVu Sans,Fontsize=88'", "-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac","-shortest",str(v9/"v9-render.mp4")], check=True)
print("V9 DONE")
