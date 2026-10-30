import subprocess, pathlib
base = pathlib.Path.home()/"workspace/goals/ctrl-ahead-os-ai-video/files/pipeline/data/portfolio/2026-W43/005-model-leaks/v10"
texts = base/"texts"; texts.mkdir(exist_ok=True)
def txt(name, s):
    p=texts/name; p.write_text(s); return str(p)
font="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
# proof segment test: 4s, bg + header + 2 lines, alpha fade with escaped commas
filters = [
 "scale=1920:1280,crop=1920:1080",
 f"drawtext=fontfile={font}:textfile='{txt('t_hdr.txt','October 11 — models page')}':fontsize=44:fontcolor=white:x=(w-text_w)/2:y=280:box=1:boxcolor=black@0.5:boxborderw=16:enable='gte(t\\,0.1)'",
 f"drawtext=fontfile={font}:textfile='{txt('t_l1.txt','GPT-6 Astra')}':fontsize=76:fontcolor=0xFFD700:x=(w-text_w)/2:y=430:box=1:boxcolor=black@0.5:boxborderw=16:alpha='if(lt(t\\,0.5)\\,0\\,if(lt(t\\,0.9)\\,(t-0.5)/0.4\\,1))':enable='gte(t\\,0.5)'",
 f"drawtext=fontfile={font}:textfile='{txt('t_l2.txt','no Bel')}':fontsize=76:fontcolor=0xFFD700:x=(w-text_w)/2:y=560:box=1:boxcolor=black@0.5:boxborderw=16:alpha='if(lt(t\\,1.5)\\,0\\,if(lt(t\\,1.9)\\,(t-1.5)/0.4\\,1))':enable='gte(t\\,1.5)'",
]
vf=",".join(filters)
print(vf)
subprocess.run(["ffmpeg","-y","-v","error","-loop","1","-i",str(base/"proof-bg.jpg"),"-t","4","-vf",vf,"-r","30","-c:v","libx264","-pix_fmt","yuv420p","-an","/tmp/proof_test.mp4"], check=True)
print("ok")
