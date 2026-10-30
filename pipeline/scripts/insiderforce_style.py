"""InsiderForce-style Short boilerplate (Muse, open-source).
Generates: (1) karaoke ASS where unspoken=gray, spoken=black, (2) a number-card PNG,
(3) a sparkle-list PNG. All on pure white, bold black grotesque, centered.
Usage: python3 insiderforce_style.py phrases.json
phrases.json: [{"start":0.0,"end":3.0,"words":["five","free","plugins"]}, ...]
No brand, logo, or watermark of any other creator is included; pass --brand for the watermark.
"""
import json, sys, textwrap
from PIL import Image, ImageDraw, ImageFont
FONTB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def fmt(s):
    h=int(s//3600); m=int((s%3600)//60); sec=s%60
    return f"{h}:{m:02d}:{int(sec):02d}.{int(round((sec-int(sec))*100)):02d}"
def karaoke(phrases, out, brand=""):
    hdr="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Klo,DejaVu Sans,72,&H00000000,&H00999999,&H00FFFFFF,&H00000000,1,0,0,0,100,100,-2,0,1,0,0,8,80,80,700,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines=[hdr]
    for ph in phrases:
        words=ph["words"]; dur=(ph["end"]-ph["start"])/max(len(words),1)
        total=int(round((ph["end"]-ph["start"])*100)); per=total//len(words); rem=total-per*len(words)
        kara=[]
        for i,w in enumerate(words):
            cs=per+(rem if i==len(words)-1 else 0); kara.append(f"{{\\k{cs}}}{w}")
        lines.append(f"Dialogue: 0,{fmt(ph['start'])},{fmt(ph['end'])},Klo,,0,0,0,,{' '.join(kara)}")
    open(out,"w").write("\n".join(lines)); print(f"karaoke: {out}")
def number_card(num, name, out):
    img=Image.new("RGB",(1080,1920),(255,255,255)); d=ImageDraw.Draw(img)
    # terracotta asterisk motifs, corners
    for cx,cy in [(950,120),(130,1800)]:
        for a in range(8):
            import math
            x2=cx+int(60*math.cos(a*math.pi/4)); y2=cy+int(60*math.sin(a*math.pi/4))
            d.line([(cx,cy),(x2,y2)],fill=(208,122,82),width=14)
    # floating dark card placeholder (replace with real screenshot in production)
    d.rounded_rectangle([140,420,940,1020],radius=40,fill=(20,20,28))
    d.text((540,700),"[SCREENSHOT]",font=ImageFont.truetype(FONTB,48),fill=(255,255,255),anchor="mm")
    # giant gradient numeral (simulated: large black text, fading via stacked alpha is not in PIL text; use solid + note)
    d.text((540,1250),str(num),font=ImageFont.truetype(FONTB,420),fill=(0,0,0),anchor="mm")
    d.text((540,1520),name,font=ImageFont.truetype(FONTB,84),fill=(0,0,0),anchor="mm")
    img.save(out); print(f"number card: {out}")
def sparkle_list(items, out):
    img=Image.new("RGB",(1080,1920),(255,255,255)); d=ImageDraw.Draw(img)
    y=500
    for it in items:
        d.text((140,y),"✦",font=ImageFont.truetype(FONTB,72),fill=(208,122,82))
        for ln in textwrap.wrap(it,width=20):
            d.text((240,y),ln,font=ImageFont.truetype(FONTB,72),fill=(0,0,0)); y+=95
        y+=60
    img.save(out); print(f"sparkle list: {out}")
if __name__=="__main__":
    data=json.load(open(sys.argv[1])) if len(sys.argv)>1 else {"phrases":[],"number":1,"name":"Example","items":["hooks","skills"]}
    karaoke(data.get("phrases",[]),"karaoke.ass")
    number_card(data.get("number",1),data.get("name","Example"),"number_card.png")
    sparkle_list(data.get("items",[]),"sparkle_list.png")
