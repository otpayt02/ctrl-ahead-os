#!/bin/bash
# Render every composition to renders/<id>.mp4, concat, mux v1 final-mix audio.
set -u
export TMPDIR=~/workspace/.hf-tmp
cd "$(dirname "$0")"
mkdir -p renders
IDS="s01 s02 day1 s03_1 s03_2 s03_3 s03_4 s03_5 s03_6 day2 s04_1 s04_2 s04_3 day3 s05_1 s05_2 s05_3 day4 s06_1 s06_2 s06_3 day5 s07_1 s07_2 s07_3 s08 outro"
for id in $IDS; do
  if [ -s "renders/$id.mp4" ]; then echo "skip $id (exists)"; continue; fi
  echo "=== rendering $id $(date +%T) ==="
  npx --yes hyperframes@0.8.210 render -c "compositions/$id.html" -o "renders/$id.mp4" --quality standard 2>&1 | tail -2
done
: > renders/concat.txt
for id in $IDS; do echo "file '$id.mp4'" >> renders/concat.txt; done
ffmpeg -y -v error -f concat -safe 0 -i renders/concat.txt -c copy renders/video_silent.mp4
ffmpeg -y -v error -i renders/video_silent.mp4 -i assets/audio/final-mix.m4a -c:v copy -c:a aac -b:a 160k -shortest 006-five-day-roadmap-v2.mp4
ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,width,height,r_frame_rate -of default=noprint_wrappers=1 006-five-day-roadmap-v2.mp4
echo DONE
