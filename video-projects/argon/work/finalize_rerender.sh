#!/usr/bin/env bash
# Ahead of Rush AI branding rerender (2026-10-30) — provenance record of the
# chain actually run. Changes vs the original build: segment 1 VO re-recorded
# with "This is Ahead of Rush AI" (assets/audio/vo_s1.mp3, 22.368s), words_s1
# re-aligned (work/align_s1.py), VO_DUR[1]=22.368 in build_scenes.py, music
# regenerated at TOTAL=181.608 (synth_music.py), S1 kicker/brand chip and S6
# wordmark/tagline rebranded in build_scenes.py, scenes 1+6 re-rendered via
# work/render_scenes.py, Dec chip/tick anchor nudged 21.0 -> 21.2.
set -e
cd ~/workspace/ctrl-ahead-argon
DRAFTS=~/workspace/goals/ctrl-ahead-os-ai-video/files/pipeline/backend/runs/2026-10-30-1346-proxy/drafts/automate-ai-coding-agents
MASTER="ahead-of-rush-ai-gemini-4-argon-1080p.mp4"
SMALL="ahead-of-rush-ai-gemini-4-argon-720p.mp4"
printf "file 's1.mp4'\nfile 's2.mp4'\nfile 's3.mp4'\nfile 's4.mp4'\nfile 's5.mp4'\nfile 's6.mp4'\n" > renders/concat.txt
ffmpeg -v error -f concat -safe 0 -i renders/concat.txt -c copy -y renders/_work/concat_raw.mp4
# loudnorm (dynamic) + limiter; measured on the result: I -16.82 LUFS, TP -0.44 dBTP
ffmpeg -v error -i renders/_work/concat_raw.mp4 -c:v copy \
  -af "loudnorm=I=-16.35:TP=-2.5:LRA=11,alimiter=limit=0.75:level=false" \
  -c:a aac -b:a 128k -ar 48000 -y "renders/$MASTER"
cp "renders/$MASTER" "$DRAFTS/$MASTER"
cp "renders/$MASTER" ~/workspace/your_files/"$MASTER"
ffmpeg -v error -i "renders/$MASTER" -vf scale=1280:720 -c:v libx264 -crf 23 \
  -preset medium -c:a aac -b:a 128k -y ~/workspace/your_files/"$SMALL"
