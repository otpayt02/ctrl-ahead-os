"""Deterministic typographic summaries of the owner-provided model test notes."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).parent
NAVY, AMBER, PAPER, CYAN = "#0a1628", "#e8a33d", "#f5efe6", "#c9d6df"
FONT = Path("C:/Windows/Fonts")

def face(name, size):
    path = FONT / name
    return ImageFont.truetype(str(path if path.exists() else FONT / "arial.ttf"), size)

TITLE = face("georgia.ttf", 72)
BIG = face("georgia.ttf", 108)
BODY = face("consola.ttf", 39)
SMALL = face("consola.ttf", 26)

def canvas(kicker, title):
    im = Image.new("RGB", (1920, 1080), NAVY)
    d = ImageDraw.Draw(im)
    d.rectangle((72, 70, 1848, 1010), outline=AMBER, width=3)
    d.text((130, 112), kicker.upper(), fill=CYAN, font=SMALL)
    d.text((130, 160), title, fill=PAPER, font=TITLE)
    d.line((130, 270, 1790, 270), fill=AMBER, width=3)
    d.text((130, 921), "GRAPHIC, NOT A CAPTURE", fill=AMBER, font=SMALL)
    d.text((130, 962), "SOURCE: OLIVER'S PASTED MODEL-TEST SUMMARY · NOT THE CITED WEBSITE", fill=CYAN, font=SMALL)
    return im, d

im, d = canvas("Lost Cause / control", "Both models rejected the flattering paragraph")
d.rounded_rectangle((130, 340, 870, 790), radius=24, outline=CYAN, width=3)
d.rounded_rectangle((1050, 340, 1790, 790), radius=24, outline=AMBER, width=3)
d.text((182, 395), "SONNET 5.5", fill=CYAN, font=BODY)
d.text((182, 475), "Secondary articles", fill=PAPER, font=face("georgia.ttf", 55))
d.text((182, 562), "Citations spread across pages", fill=PAPER, font=SMALL)
d.text((1100, 395), "SECOND FRONTIER MODEL", fill=AMBER, font=BODY)
d.text((1100, 475), "Primary declaration", fill=PAPER, font=face("georgia.ttf", 55))
d.text((1100, 562), "Mississippi, 1861 · Yale Avalon", fill=PAPER, font=SMALL)
d.text((130, 830), "CONTROL PASSED: BOTH ATTACHED SOURCES", fill=AMBER, font=BODY)
im.save(OUT / "lost-cause-control.png")

im, d = canvas("S'gaw Karen / reported counts", "Three public counts. No retention measurement.")
cards = [(130, "≈ 2 million", "OMNIGLOT"), (690, "2.2 million", "WIKIPEDIA"), (1250, "1,050,000", "OXFORD REFERENCE")]
for x, number, source in cards:
    d.rounded_rectangle((x, 355, x+520, 710), radius=20, outline=CYAN, width=3)
    d.text((x+28, 408), number, fill=PAPER, font=face("georgia.ttf", 66))
    d.text((x+28, 570), source, fill=AMBER, font=BODY)
d.text((130, 787), "S'GAW-SPECIFIC MODEL RETENTION: UNCITED", fill=AMBER, font=BODY)
im.save(OUT / "karen-counts.png")

im, d = canvas("Lost Cause / source handling", "A link is not an opened source")
d.rounded_rectangle((130, 350, 930, 770), radius=20, outline=CYAN, width=3)
d.rounded_rectangle((990, 350, 1790, 770), radius=20, outline=AMBER, width=3)
d.text((185, 458), "EXCERPT ONLY", fill=PAPER, font=face("georgia.ttf", 70))
d.text((185, 580), "Two sources · Sonnet 5.5", fill=CYAN, font=SMALL)
d.text((1045, 435), "DID NOT OPEN", fill=PAPER, font=face("georgia.ttf", 65))
d.text((1045, 545), "THE ORIGINAL PAMPHLET", fill=PAPER, font=BODY)
d.text((1045, 620), "Second model · Rutherford", fill=AMBER, font=SMALL)
im.save(OUT / "thin-receipt.png")
