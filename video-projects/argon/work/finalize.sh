#!/usr/bin/env bash
# Finalize the Ctrl-Ahead Argon video: concat scene renders, deliver copies,
# verify (probe, dead-air scan, boundary frames).
set -e
cd ~/workspace/ctrl-ahead-argon
DRAFTS=~/workspace/goals/ctrl-ahead-os-ai-video/files/pipeline/backend/runs/2026-10-30-1346-proxy/drafts/automate-ai-coding-agents
MASTER="ctrl-ahead-gemini-4-argon-1080p.mp4"
SMALL="ctrl-ahead-gemini-4-argon-720p.mp4"

printf "file 's1.mp4'\nfile 's2.mp4'\nfile 's3.mp4'\nfile 's4.mp4'\nfile 's5.mp4'\nfile 's6.mp4'\n" > renders/concat.txt
ffmpeg -v error -f concat -safe 0 -i renders/concat.txt -c copy -y "renders/$MASTER"
echo "== master probe =="
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,avg_frame_rate,sample_rate,channels -show_entries format=duration,size -of default=noprint_wrappers=1 "renders/$MASTER"
md5sum "renders/$MASTER"

cp "renders/$MASTER" "$DRAFTS/$MASTER"
cp "renders/$MASTER" ~/workspace/your_files/"$MASTER"
ffmpeg -v error -i "renders/$MASTER" -vf scale=1280:720 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k -y ~/workspace/your_files/"$SMALL"
echo "== copies =="
ls -la "$DRAFTS/$MASTER" ~/workspace/your_files/"$MASTER" ~/workspace/your_files/"$SMALL"
md5sum "$DRAFTS/$MASTER" ~/workspace/your_files/"$MASTER"

echo "== dead-air scan (silences > 1.2s below -45dB) =="
ffmpeg -i "renders/$MASTER" -af silencedetect=noise=-45dB:d=1.2 -f null - 2>&1 | grep -E "silence_(start|end)" || echo "none found"

echo "== boundary frames =="
mkdir -p renders/_work/final_frames
for t in 1 6 12 22.5 24 30 45 59.5 61 75 90 102 104 115 125 132.5 134 142 155 160.5 162 168 176 180.5; do
  ffmpeg -v error -ss $t -i "renders/$MASTER" -frames:v 1 -y "renders/_work/final_frames/f_$t.png"
done
python3 - <<'EOF'
from PIL import Image
import glob, os
files = sorted(glob.glob('renders/_work/final_frames/f_*.png'), key=lambda p: float(os.path.basename(p)[2:-4]))
cols, tw, th = 4, 480, 270
rows = (len(files) + cols - 1) // cols
sheet = Image.new('RGB', (cols * tw, rows * th), 'black')
for i, f in enumerate(files):
    im = Image.open(f).resize((tw, th))
    sheet.paste(im, ((i % cols) * tw, (i // cols) * th))
sheet.save('renders/_work/final_frames/contact_sheet.png')
print('sheet', sheet.size, len(files), 'frames')
EOF
echo DONE
