import os, subprocess, textwrap
from PIL import Image, ImageDraw, ImageFont
BASE="/home/hatch/workspace/goals/ctrl-ahead-os-ai-video/files/pipeline/data/portfolio/2026-W43/005-model-leaks"
V7=os.path.join(BASE,"v7"); CARDS=os.path.join(V7,"cards"); SEGS=os.path.join(V7,"segs")
os.makedirs(CARDS, exist_ok=True); os.makedirs(SEGS, exist_ok=True)
HEADLINES=[
"FOUR NAMES. Four verdicts.","FOUR POSTERS. One louder.","CHECKED. Not repeated.","FOUR DOORS. Only one real?","SCORECARD. Don't build on smoke.",
"RUMOR IS A MIRROR.","IT SHOWS WHAT YOU WANTED.","SELLING CERTAINTY. In fog.","TRUTH > HEADLINE.","DISCIPLINE. Not debunk.",
"FIRST: BEL. One envelope.","ONE POST. A flock.","NO DOCUMENT. No source.","LABEL CAME LATER.","NAMEPLATE: EMPTY.",
"THREE MOONS. No fourth.","NO BEL. NO GPT-7.","LIGHT UNDER A LOCKED DOOR.","TRUE ≠ SAME.","VERDICT: UNVERIFIED.",
"SEARCH: CLAUDE REA.","STAGE: EMPTY.","TWO BANS. Neither a model.","POLICY: OCT 8 → NOV 12.","CRUELTY? Chat closes.",
"ENDS CHAT. Not pulled.","ACCOUNTS. Copied. Banned.","SORT IT: Account / Behavior / Model.","PAUSE. On 'banned'.","BAN ACCOUNT = FENCE.",
"BAN BEHAVIOR = HOW WE TREAT A MIND.","BAN MODEL = ERASE IT.","THREE WORDS. Squashed into one.","WHAT? BY WHOM? FROM WHOM?","PRECISION. Fear → Understanding.",
"CARBON: CLOSEST. Not a product.","INSIDE THE LAB. Testing.","FEELS LIKE ≠ BENCHMARK.","NO CARD. NO PRICE. NO DATE.","APPEARED. Then pulled.",
"LOCKED APP. Key doesn't fit.","QWEN 4: IN TRAINING.","TIERS. No recipe.","SHELF: EMPTY.","PREVIEW. Not the film.",
"CODER: EMPTY CHAIR.","THE GAP. Imagination rushes in.","≠ ≠ ≠. Name each stage.","BUILD ON SHIPPED. Four bricks.","LEDGER. Confirmed + Shipped.",
]
FONTB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def card(i, headline):
    img=Image.new("RGB",(1920,1080),(11,18,32)); d=ImageDraw.Draw(img)
    for x in range(0,1920,160): d.line([(x,0),(x,1080)],fill=(20,30,50),width=1)
    for y in range(0,1080,160): d.line([(0,y),(1920,y)],fill=(20,30,50),width=1)
    d.rounded_rectangle([80,70,80+420,150],radius=40,fill=(232,163,61))
    f_pill=ImageFont.truetype(FONTB,36); d.text((110,92),f"SEGMENT {i+1:02d} / 50",font=f_pill,fill=(0,0,0))
    f_h=ImageFont.truetype(FONTB,96)
    lines=textwrap.wrap(headline,width=22)
    y=380
    for ln in lines:
        d.text((80,y),ln,font=f_h,fill=(255,255,255)); y+=120
    d.rectangle([80,y+20,80+520,y+32],fill=(232,163,61))
    f_s=ImageFont.truetype(FONT,44); d.text((80,y+60),"AI IMAGE / GRAPHIC — NOT A SCREENSHOT, NOT EVIDENCE",font=f_s,fill=(180,190,210))
    d.text((80,980),"Ctrl-Ahead OS  •  005 Model Leaks  •  Slow zoom, text reveal, highlight — never static over 5s",font=ImageFont.truetype(FONT,32),fill=(120,130,150))
    p=os.path.join(CARDS,f"card{i+1:02d}.png"); img.save(p); return p
# video/image segment mapping (0-indexed segment -> (kind, path))
GEN=os.path.join(V7,"gen")
import glob
def find(pat):
    m=glob.glob(os.path.join(GEN,pat)); return m[0] if m else None
SPECIAL={
 0:("video",find("media-generation-v7-hook-boxers*.mp4")),
 5:("video",find("media-generation-v7-i2v-mirror*.mp4")),
 7:("video",find("media-generation-v7-i2v-certainty*.mp4")),
 15:("video",find("media-generation-v7-bel-whisper-billboard*.mp4")),
 19:("video",find("media-generation-v7-i2v-stamp*.mp4")),
 21:("video",find("media-generation-v7-claude-empty-chair*.mp4")),
 35:("video",find("media-generation-v7-carbon-frosted-glass*.mp4")),
 41:("video",find("media-generation-v7-qwen-construction*.mp4")),
 46:("video",find("media-generation-v7-hype-balloon-pop*.mp4")),
 49:("video",find("media-generation-v7-i2v-ledger*.mp4")),
}
DUR=351.888/50
for i,hl in enumerate(HEADLINES):
    out=os.path.join(SEGS,f"seg{i+1:02d}.mp4")
    if os.path.exists(out): continue
    if i in SPECIAL and SPECIAL[i][1]:
        kind,src=SPECIAL[i]
        label="AI VIDEO — METAPHOR ONLY, NOT EVIDENCE" if kind=="video" else "AI IMAGE — METAPHOR ONLY, NOT EVIDENCE"
        # escape headline for drawtext
        txt=hl.replace("'","").replace(":","").replace("≠","!=")
        if kind=="video":
            vf=f"trim=0:{DUR:.3f},setpts=PTS-STARTPTS,scale=1920:1080,drawtext=fontfile={FONTB}:text='{txt}':fontsize=64:fontcolor=white:x=80:y=80:box=1:boxcolor=black@0.6:boxborderw=20,drawtext=fontfile={FONT}:text='{label}':fontsize=36:fontcolor=white:x=80:y=980:box=1:boxcolor=black@0.6:boxborderw=16"
            cmd=["ffmpeg","-y","-v","error","-i",src,"-vf",vf,"-t",f"{DUR:.3f}","-an","-c:v","libx264","-preset","veryfast","-crf","23",out]
        else:
            vf=f"scale=1920:1080,zoompan=z='min(zoom+0.0015,1.12)':d=211:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30,drawtext=fontfile={FONTB}:text='{txt}':fontsize=64:fontcolor=white:x=80:y=80:box=1:boxcolor=black@0.6:boxborderw=20,drawtext=fontfile={FONT}:text='{label}':fontsize=36:fontcolor=white:x=80:y=980:box=1:boxcolor=black@0.6:boxborderw=16"
            cmd=["ffmpeg","-y","-v","error","-loop","1","-i",src,"-vf",vf,"-t",f"{DUR:.3f}","-an","-c:v","libx264","-preset","veryfast","-crf","23",out]
        subprocess.run(cmd,check=True)
    else:
        p=card(i,hl)
        vf=f"zoompan=z='min(zoom+0.0015,1.12)':d=211:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30"
        subprocess.run(["ffmpeg","-y","-v","error","-loop","1","-i",p,"-vf",vf,"-t",f"{DUR:.3f}","-an","-c:v","libx264","-preset","veryfast","-crf","23",out],check=True)
    print("seg",i+1,"done",flush=True)
# concat
with open(os.path.join(V7,"concat.txt"),"w") as f:
    for i in range(50): f.write(f"file 'segs/seg{i+1:02d}.mp4'\n")
subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",os.path.join(V7,"concat.txt"),"-i",os.path.join(BASE,"vo2/vo.mp3"),"-vf","subtitles="+os.path.join(V7,"karaoke_small.ass")+",vignette=PI/5","-c:v","libx264","-preset","veryfast","-crf","23","-c:a","aac","-shortest",os.path.join(BASE,"v7-render.mp4")],check=True)
subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",os.path.join(V7,"concat.txt"),"-i",os.path.join(BASE,"vo2/vo.mp3"),"-c:v","libx264","-preset","veryfast","-crf","23","-c:a","aac","-shortest",os.path.join(V7,"v7_nocap.mp4")],check=True)
vf_short="split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=20,eq=brightness=-0.25[bg];[b]crop=608:1080,scale=1080:1920[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,subtitles="+os.path.join(V7,"karaoke_shorts.ass")
subprocess.run(["ffmpeg","-y","-v","error","-i",os.path.join(V7,"v7_nocap.mp4"),"-t","59","-filter_complex",vf_short,"-c:v","libx264","-preset","veryfast","-crf","23","-c:a","aac",os.path.join(BASE,"v7-shorts-9x16.mp4")],check=True)
print("V7 DONE")
