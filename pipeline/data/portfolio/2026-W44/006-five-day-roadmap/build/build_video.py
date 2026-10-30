#!/usr/bin/env python3
"""006 build: PIL illustrated plates + chip-stamp overlays + Helio VO + Whisper-aligned gold-word captions.
Fallback note: hook montage uses still plates with quick cuts (no generated video clips; Vast.ai/LTX not rented, no spending).
Provenance labels live here / in BUILD_NOTES.md only — never on frames."""
import json, re, difflib, pathlib, subprocess, sys, math, random
from PIL import Image, ImageDraw, ImageFont
BASE = pathlib.Path(__file__).parent
sys.path.insert(0, str(BASE))
from segments_data import SEGMENTS

W,H=1920,1080
NAVY=(11,14,20); PANEL=(19,26,42); CYAN=(0,240,255); PINK=(255,46,154); GOLD=(255,209,102); BRASS=(201,168,118); WHITE=(255,255,255); MUTED=(170,180,200); GREEN=(46,230,168); RED=(255,80,80)
FB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; FR="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def font(p,sz):
    try: return ImageFont.truetype(p,sz)
    except: return ImageFont.load_default()
def wrap(d,text,f,maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t,font=f)<=maxw: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines

def bg(later=False):
    im=Image.new("RGB",(W,H),NAVY); d=ImageDraw.Draw(im,"RGBA")
    for y in range(H):
        r=int(11+ (19-11)*y/H); g=int(14+(26-14)*y/H); b=int(20+(42-20)*y/H)
        d.line([(0,y),(W,y)],fill=(r,g,b))
    for x in range(0,W,96):
        for y in range(0,H,96): d.ellipse([x,y,x+4,y+4],fill=(255,255,255,18))
    d.rectangle([0,H-14,W,H],fill=BRASS)
    if later:
        # desaturate overlay + LATER badge handled in slide
        d.rectangle([0,0,W,H],fill=(90,90,100,70))
    return im,d

def draw_icon(d, icon, box):
    x0,y0,x1,y1=box; cx=(x0+x1)//2; cy=(y0+y1)//2
    C=CYAN; P=PINK; G=GOLD
    if icon=="route":
        pts=[(x0+40,y1-60),(x0+180,y0+120),(x0+330,y1-140),(x0+480,y0+80),(x1-60,y1-100)]
        d.line(pts,fill=BRASS,width=10)
        for i,(x,y) in enumerate(pts): d.ellipse([x-34,y-34,x+34,y+34],fill=GOLD if i<4 else GREEN,outline=WHITE,width=4); d.text((x-10,y-14),str(i+1),fill=(0,0,0),font=font(FB,36))
    elif icon=="cards":
        for i in range(5):
            x=x0+i*118; d.rounded_rectangle([x,y0+80,x+100,y0+300],12,outline=CYAN,width=6,fill=(20,30,50)); d.text((x+22,y0+160),f"D{i+1}",fill=WHITE,font=font(FB,36))
    elif icon=="timeline":
        d.line([(x0,cy),(x1,cy)],fill=BRASS,width=10)
        for i in range(6):
            x=x0+40+i*100; d.ellipse([x-26,cy-26,x+26,cy+26],fill=CYAN,outline=WHITE,width=3)
    elif icon=="meter":
        d.ellipse([cx-170,cy-170,cx+170,cy+170],outline=GOLD,width=12,fill=(20,25,35))
        for a in range(-120,121,30):
            rad=math.radians(a-90); d.line([(cx+120*math.cos(rad),cy+120*math.sin(rad)),(cx+150*math.cos(rad),cy+150*math.sin(rad))],fill=WHITE,width=5)
        rad=math.radians(-95); d.line([(cx,cy),(cx+130*math.cos(rad),cy+130*math.sin(rad))],fill=PINK,width=10)
    elif icon=="box":
        d.rectangle([cx-190,cy-140,cx+190,cy+160],outline=CYAN,width=10,fill=(18,28,48)); d.line([(cx-190,cy-140),(cx-120,cy-210),(cx+260,cy-210),(cx+190,cy-140)],fill=CYAN,width=8); d.rectangle([cx-90,cy-40,cx+90,cy+80],outline=GOLD,width=6)
    elif icon=="ghost":
        d.rectangle([x0+40,y0+40,x1-40,y1-40],outline=CYAN,width=8,fill=(15,22,38))
        for i in range(5): d.line([(x0+80,y0+90+i*55),(x1-120-i*40,y0+90+i*55)],fill=(0,240,255,160),width=10)
        d.ellipse([cx-45,y1-150,cx+45,y1-60],fill=(255,255,255,120))
    elif icon=="press":
        d.rectangle([cx-220,cy-40,cx+220,cy+40],fill=BRASS); d.rectangle([cx-160,cy+40,cx+160,cy+180],outline=WHITE,width=6)
        for i in range(3): d.rectangle([cx-120+i*20,cy+200+i*18,cx+120+i*20,cy+225+i*18],outline=GOLD,width=4)
        d.ellipse([cx-30,cy-170,cx+30,cy-110],outline=PINK,width=8)
    elif icon=="blueprint":
        d.rectangle([x0+30,y0+30,x1-30,y1-30],fill=(20,60,110),outline=WHITE,width=5)
        for i,(bx,by) in enumerate([(120,90),(300,90),(210,230),(90,230),(330,230)]): d.rectangle([x0+bx,y0+by,x0+bx+110,y0+by+70],outline=CYAN,width=5)
        d.line([(x0+175,y0+125),(x0+265,y0+265)],fill=GOLD,width=5); d.line([(x0+355,y0+125),(x0+265,y0+265)],fill=GOLD,width=5)
    elif icon=="bricks":
        for r in range(3):
            for c in range(3):
                x=x0+40+c*180; y=y0+60+r*130; d.rounded_rectangle([x,y,x+150,y+100],16,outline=[CYAN,PINK,GOLD][(r+c)%3],width=7,fill=(20,30,50))
    elif icon=="facade":
        d.rectangle([cx-200,cy-220,cx+200,cy+200],outline=GOLD,width=9,fill=(30,25,20))
        for r in range(3):
            for c in range(3): d.rectangle([cx-150+c*110,cy-160+r*110,cx-70+c*110,cy-80+r*110],fill=CYAN)
        for i in range(5): d.line([(cx+230,cy-220+i*20),(cx+320,cy-180+i*70)],fill=MUTED,width=4)
    elif icon=="door":
        d.rectangle([cx-110,cy-230,cx+110,cy+230],outline=GOLD,width=12,fill=(25,30,45)); d.ellipse([cx+55,cy-12,cx+85,cy+18],fill=PINK)
        for i in range(4): d.ellipse([x0+30+i*55,cy+150,x0+65+i*55,cy+185],fill=CYAN)
    elif icon=="lamp":
        d.polygon([(cx,cy-220),(cx-190,cy+140),(cx+190,cy+140)],fill=(255,209,102,70)); d.rectangle([cx-90,cy-250,cx+90,cy-200],fill=GOLD); d.line([(cx-260,cy+190),(cx+260,cy+190)],fill=BRASS,width=8)
        d.ellipse([cx+180,cy+90,cx+230,cy+140],outline=PINK,width=6)
    elif icon=="tickets":
        for i in range(3):
            y=y0+60+i*130; d.rounded_rectangle([x0+60,y,x1-60,y+95],14,outline=[GREEN,GOLD,CYAN][i],width=6,fill=(20,30,50)); d.text((x0+90,y+28),["CREATE","READ","CANCEL"][i],fill=WHITE,font=font(FB,40))
    elif icon=="queue":
        d.rectangle([cx-60,cy-220,cx+60,cy-60],outline=GOLD,width=8,fill=(25,30,45))
        for i in range(5): d.ellipse([x0+60+i*105,cy+120,x0+105+i*105,cy+165],fill=CYAN)
        d.rectangle([x1-130,y0+30,x1-90,y1-60],fill=(0,240,255,60))
    elif icon=="cabinet":
        d.rectangle([cx-190,cy-230,cx+190,cy+230],outline=CYAN,width=9,fill=(20,28,45))
        for r in range(4): d.rectangle([cx-160,cy-200+r*105,cx+160,cy-115+r*105],outline=GOLD,width=5); d.rectangle([cx-30,cy-175+r*105,cx+30,cy-155+r*105],fill=WHITE)
    elif icon=="seam":
        d.rectangle([x0+40,cy-160,cx-10,cy+160],outline=CYAN,width=8); d.rectangle([cx+10,cy-160,x1-40,cy+160],outline=PINK,width=8)
        for i in range(5): d.ellipse([cx-14,cy-140+i*70,cx+14,cy-112+i*70],fill=GOLD)
    elif icon=="garage":
        for i in range(5): d.line([(x0+40,y0+60+i*95),(x1-40,y0+60+i*95)],fill=BRASS,width=6)
        for i in range(8): d.rectangle([x0+60+i*70,y0+30,x0+115+i*70,y0+80],outline=CYAN,width=4)
        d.rectangle([x0+60,y1-150,x0+260,y1-50],outline=PINK,width=6)
    elif icon=="launchwall":
        for r in range(3):
            for c in range(6):
                x=x0+40+c*95; y=y0+50+r*110; d.ellipse([x,y,x+62,y+62],fill=GREEN if (r*6+c)%5 else GOLD,outline=WHITE,width=3)
        d.ellipse([cx-150,y1-110,cx-30,y1-30],fill=BRASS); d.ellipse([cx+30,y1-110,cx+150,y1-30],fill=BRASS)
    elif icon=="heart":
        pts=[]; 
        for i in range(60):
            x=x0+30+i*10; y=cy - (90 if i in (20,21) else 30 if i==22 else 0) + (60 if i==23 else 0); pts.append((x,y))
        d.line(pts,fill=PINK,width=9)
        for r in range(2):
            for c in range(3): d.rectangle([x0+60+c*180,y0+220+r*110,x0+200+c*180,y0+300+r*110],outline=CYAN,width=4)
    elif icon=="gauges":
        for i,ang in enumerate([-60,20,100]):
            gx=cx-180+i*180; d.ellipse([gx-70,cy-170,gx+70,cy-30],outline=GOLD,width=7); rad=math.radians(ang); d.line([(gx,cy-100),(gx+50*math.cos(rad),cy-100+50*math.sin(rad))],fill=PINK,width=6)
        d.line([(x0+60,y1-80),(cx,y1-140),(x1-60,y1-70)],fill=CYAN,width=7)
    else: # generic
        d.ellipse([cx-140,cy-140,cx+140,cy+140],outline=CYAN,width=10)

def make_slide(seg, idx):
    later=seg.get("later",False)
    im,d=bg(later)
    d.text((70,54),seg["scene"],fill=CYAN,font=font(FB,34))
    if later: 
        d.rounded_rectangle([W-300,44,W-70,104],12,fill=RED); d.text((W-262,58),"LATER",fill=WHITE,font=font(FB,36))
    # title wrapped
    tf=font(FB,92 if len(seg["title"])<=16 else 72)
    lines=wrap(d,seg["title"],tf,1050)
    y=130
    for ln in lines: d.text((70,y),ln,fill=WHITE,font=tf); y+= (100 if tf.size==92 else 82)
    if seg["year"]:
        d.rounded_rectangle([70,y+6,70+190,y+70],10,outline=GOLD,width=4); d.text((92,y+16),seg["year"],fill=GOLD,font=font(FB,40)); y+=86
    for ln in wrap(d,seg["subtitle"],font(FR,40),1000): d.text((70,y+8),ln,fill=MUTED,font=font(FR,40)); y+=52
    draw_icon(d, seg["icon"], (1180,170,1810,760))
    d.text((70,H-52),"CTRL-AHEAD  •  THE 5-DAY ROADMAP, EXPLAINED",fill=(140,150,170),font=font(FB,24))
    out=BASE/"slides"/f"{seg['id']}.jpg"; im.save(out,quality=92); return out

def make_daycard(day,title,hours,outname):
    im,d=bg()
    d.text((W//2-260,360),day,fill=GOLD,font=font(FB,150))
    d.text((W//2-260,540),title,fill=WHITE,font=font(FB,110))
    d.text((W//2-260,680),hours,fill=CYAN,font=font(FB,64))
    d.line([(360,820),(1560,820)],fill=BRASS,width=10)
    out=BASE/"slides"/outname; im.save(out,quality=92); return out

def make_outro():
    im,d=bg()
    # brass arrow
    d.polygon([(760,300),(1160,540),(760,780),(820,540)],fill=BRASS,outline=GOLD)
    d.text((520,830),"We don't chase the future. We check it.",fill=WHITE,font=font(FB,54))
    d.text((610,910),"Ctrl-Ahead — confirmed, not just claimed.",fill=MUTED,font=font(FR,40))
    d.rounded_rectangle([810,970,1110,1035],28,fill=PINK); d.text((862,982),"SUBSCRIBE",fill=WHITE,font=font(FB,36))
    out=BASE/"slides"/"outro.jpg"; im.save(out,quality=92); return out

def make_chip(seg, ci):
    label,text = seg["chips"][ci][0], seg["chips"][ci][1]
    col = RED if "SKIP" in label else GREEN if label=="HOW" or "HOW" in label else GOLD if label in ("LATER",) else CYAN
    if label=="LATER": col=MUTED
    im=Image.new("RGBA",(1060,118),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([2,2,1058,116],14,fill=(10,14,24,235),outline=col,width=4)
    d.text((22,14),label,fill=col,font=font(FB,30))
    lines=wrap(d,text,font(FR,30),1010)[:2]
    yy=52
    for ln in lines: d.text((22,yy),ln,fill=WHITE,font=font(FR,30)); yy+=34
    out=BASE/"overlays"/f"{seg['id']}_chip{ci}.png"; im.save(out); return out

def main():
    # durations
    durs={}
    for s in SEGMENTS:
        r=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(BASE/"vo"/f"{s['id']}.mp3")],capture_output=True,text=True)
        durs[s['id']]=float(r.stdout.strip())
    json.dump(durs, open(BASE/"vo_durations.json","w"), indent=1)
    # alignment: global script words to whisper words
    wdata=json.load(open(BASE/"words.json")); wlist=[]
    for seg in wdata: wlist.extend(seg["words"])
    def norm(w): return re.sub(r'[^a-z0-9]','',w.lower())
    script_words=[]; seg_bounds=[]
    for s in SEGMENTS:
        ws=s["vo"].split(); a=len(script_words); script_words.extend(ws); seg_bounds.append((a,len(script_words)))
    sw=[norm(w) for w in script_words]; ww=[norm(w["word"]) for w in wlist]
    sm=difflib.SequenceMatcher(a=sw,b=ww,autojunk=False); aligned=[None]*len(script_words)
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag=="equal":
            for k in range(i2-i1): aligned[i1+k]=j1+k
    times=[]
    for i,w in enumerate(script_words):
        wi=aligned[i]
        if wi is not None and wi < len(wlist): times.append((wlist[wi]["start"], wlist[wi]["end"]))
        else: times.append(times[-1] if times else (0,0.2))
    # Note: whisper times are on vo_full_raw (no pauses). Segment offsets in that file:
    raw_off={}; acc=0
    for s in SEGMENTS: raw_off[s['id']]=acc; acc+=durs[s['id']]
    # Build timeline with pauses/daycards
    DAYCARDS={ "s03_1":("DAY 1","SETUP","7 HOURS","day1.jpg"), "s04_1":("DAY 2","UI","8 HOURS","day2.jpg"), "s05_1":("DAY 3","BACKEND","8 HOURS","day3.jpg"), "s06_1":("DAY 4","DATA","8 HOURS","day4.jpg"), "s07_1":("DAY 5","LAUNCH","7 HOURS","day5.jpg") }
    for k,v in DAYCARDS.items(): make_daycard(v[0],v[1],v[2],v[3])
    make_outro()
    timeline=[]; t=0.0
    seg_start={}
    for s in SEGMENTS:
        if s['id'] in DAYCARDS:
            timeline.append(dict(kind="daycard",file=DAYCARDS[s['id']][3],start=t,dur=1.6)); t+=1.6
        seg_start[s['id']]=t
        dur=durs[s['id']]+0.55
        timeline.append(dict(kind="seg",id=s['id'],start=t,dur=dur)); t+=dur
    outro_start=t; timeline.append(dict(kind="outro",file="outro.jpg",start=t,dur=8.0)); t+=8.0
    total=t
    json.dump(dict(timeline=timeline,total=total,seg_start=seg_start), open(BASE/"timeline.json","w"), indent=1)
    print("total",total)
    # captions ASS: phrases <=7 words from script, timing via aligned whisper mapped to new timeline
    # map raw whisper time -> new time: find segment by raw_off
    def map_time(rt, seg_idx):
        s=SEGMENTS[seg_idx]; return seg_start[s['id']] + (rt - raw_off[s['id']])
    def fmt(tt):
        cs=int(round(tt*100)); h=cs//360000; m=(cs%360000)//6000; sec=(cs%6000)//100; c=cs%100; return f"{h}:{m:02d}:{sec:02d}.{c:02d}"
    ass=["[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Cap,DejaVu Sans,50,&H00FFFFFF,&H0000FFFF,&H90000000,&H90000000,-1,0,0,0,100,100,0,0,3,2,0,2,60,60,42,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"]
    chip_times={}  # seg id -> list of (label, newtime)
    for si,s in enumerate(SEGMENTS):
        a,b=seg_bounds[si]; words=script_words[a:b]; wt=[times[a+i] for i in range(len(words))]
        # phrases 6 words
        i=0
        while i < len(words):
            grp=words[i:i+6]; gwt=wt[i:i+6]
            for k in range(len(grp)):
                st=map_time(gwt[k][0], si); en=map_time(gwt[k+1][0], si) if k+1 < len(grp) else map_time(gwt[k][1], si)
                if en<=st: en=st+0.12
                parts=[]
                for j,w in enumerate(grp):
                    w2=w.replace("{","").replace("}","")
                    parts.append(f"{{\\1c&H00D7FF&}}{w2}" if j==k else f"{{\\1c&HFFFFFF&}}{w2}")
                ass.append(f"Dialogue: 0,{fmt(st)},{fmt(en)},Cap,,0,0,0,,{' '.join(parts)}\n")
            i+=6
        # chip trigger times: search chip text words in segment words (normalized, first match of first 2 significant words / or label markers)
        cts=[]
        low=[norm(w) for w in words]
        for ci,(label,ctext) in enumerate(s["chips"]):
            # trigger phrases are chip text in most cases (condensed) — instead use explicit marker search:
            marker=None
            # find first word of chip text that appears sequentially: try full normalized sequence of first 3 words
            cand=[norm(x) for x in ctext.split() if norm(x)][:3]
            pos=None
            for p in range(len(low)-len(cand)+1):
                if low[p:p+len(cand)]==cand: pos=p; break
            if pos is None and cand:
                # fallback: first occurrence of cand[0]
                if cand[0] in low: pos=low.index(cand[0])
            if pos is None: pos=int(len(words)*(ci+1)/(len(s["chips"])+1))
            cts.append((label, map_time(wt[pos][0], si)))
        chip_times[s['id']]=cts
    open(BASE/"captions.ass","w").write("".join(ass))
    json.dump(chip_times, open(BASE/"chip_times.json","w"), indent=1)
    # slides + chips
    for s in SEGMENTS:
        make_slide(s,0)
        for ci in range(len(s["chips"])): make_chip(s,ci)
    # hook plates extra (fallback montage): reuse launchwall/gauges icons as full slides for s01 subcuts — handled in render by switching base at 1/3,2/3 using alternate slides:
    for alt_icon, name in [("launchwall","s01_b"),("gauges","s01_c")]:
        fake=dict(SEGMENTS[0]); fake["icon"]=alt_icon; fake["id"]=name; make_slide(fake,0)
    print("slides/chips/captions done")
if __name__=="__main__": main()
