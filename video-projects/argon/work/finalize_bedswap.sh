#!/usr/bin/env bash
# Suno bed swap + rebalance (2026-10-30) — provenance record of the chain
# actually run. Oliver's direction: music more serious/calm/positive and
# WAY softer than the voice. Only the music bed changed; video stream,
# VO, SFX, captions, branding untouched (video stream copied bit-exact).
# Built from project stems (assets/audio/vo_s*.mp3, assets/audio/sfx/*.wav)
# per work/timing.json — NOT derived from the old master.
#
# New bed: Suno "Clear Horizons" (2:04) downloaded to
# ~/workspace/browser_downloads/sess-3080941376/...-1-Clear_Horizons.mp3
# Extended to 181.852s: full track + second copy acrossfade d=6 (tri),
# afade in 2.5s, afade out st=173.852 d=8 (outro tail).
#
# Measured (ffmpeg loudnorm, BS.1770):
#   VO stems assembled (stereo dual-mono):  -25.05 LUFS
#   New bed raw at unity (stereo):          -15.94 LUFS
#   Bed gain applied:                       -31.11 dB
#   Bed as mixed (stem):                    -47.05 LUFS  (22.0 dB under VO)
#   Old synth bed as composed:              -27.52 LUFS  (was ~level w/ VO
#                                          after normalize: the complaint)
#   Final v2 master:                        -16.89 LUFS, TP -1.49 dBTP
#   (current cut measures -16.82 / -0.44 for reference)
# Bed in the shipped file ~= -40.5 LUFS (stem + the chain's +6.53 dB
# overall gain), inside the -38..-42 target band.
#
# NOTE: loudnorm single-pass under/overshoots its I target depending on
# input; target was iterated empirically (takes F/G/H) to land -16.89.
# NOTE: VO/SFX sources are mono — force stereo (pan dual-mono + aformat)
# BEFORE amix or the whole mix collapses to mono (caught in v2 take A).
set -e
cd ~/workspace/ctrl-ahead-argon
W=renders/_work/bedswap
DRAFTS=~/workspace/goals/ctrl-ahead-os-ai-video/files/pipeline/backend/runs/2026-10-30-1346-proxy/drafts/automate-ai-coding-agents
MASTER="ahead-of-rush-ai-gemini-4-argon-1080p-v2.mp4"
SMALL="ahead-of-rush-ai-gemini-4-argon-720p-v2.mp4"
# stems: $W/vo_mix2.wav $W/sfx_mix2.wav $W/bed_raw.wav $W/bed_gained2.wav
#        $W/mix_raw2.wav  (built per the steps in this header's chain)
ffmpeg -v error -i renders/ahead-of-rush-ai-gemini-4-argon-1080p.mp4 -i $W/mix_raw2.wav \
  -map 0:v -map 1:a -c:v copy \
  -af "loudnorm=I=-15.01:TP=-2.5:LRA=11,alimiter=limit=0.75:level=false,atrim=0:181.900,asetpts=N/SR/TB" \
  -c:a aac -b:a 128k -ar 48000 -y $W/master_v2_h.mp4
cp $W/master_v2_h.mp4 ~/workspace/your_files/"$MASTER"
cp $W/master_v2_h.mp4 "$DRAFTS/$MASTER"
ffmpeg -v error -i ~/workspace/your_files/"$MASTER" -vf scale=1280:720 -c:v libx264 -crf 23 \
  -preset medium -c:a aac -b:a 128k -y ~/workspace/your_files/"$SMALL"
