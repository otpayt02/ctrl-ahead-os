# Face Hook — Veo + Your Voice, One Clip Total

The only Veo generation this video needs. Identity comes from Veo (your photo), voice comes from you, and a local lipsync pass re-renders the mouth to your recording. Veo's synthesized voice is muted and replaced.

## 1. Veo (one 8s generation, image-to-video)

In Google Flow (free 50 daily credits): image-to-video, upload your clearest front-facing photo as the start frame, paste:

> Photorealistic video of this exact man, preserving his face and identity unchanged. He sits at a desk in a dim home office — deep navy walls, warm amber desk lamp from the left. He looks directly into the camera, leans in slightly, and speaks with confident, curious documentary-host energy, natural blinks and micro-expressions, subtle raised brow on the second sentence. He says: "Every AI you've ever used has the exact same flaw as your high school history textbook — and I can prove it." Warm casual American male voice, unhurried delivery. Locked-off medium close-up, shallow depth of field, film grain, 8 seconds, no cuts.

Download the result and save it as `capture-inputs/veo-face.mp4` (drop it in `videos/capture/capture-inputs/`).

## 2. Your VO (read it exactly as written)

> Every AI you've ever used has the exact same flaw as your high school history textbook — and I can prove it, because the proof is sitting in my homework from 2021.

Either record on your phone and drop the file in as `capture-inputs/hook-vo.wav` (or .mp3/.m4a — update `vo_file` in capture.config.json), or use the scripted mic capture:

- `powershell -ExecutionPolicy Bypass -File scripts/record-vo.ps1` (first run lists your mic devices)
- `powershell -ExecutionPolicy Bypass -File scripts/record-vo.ps1 -Mic "<device name>" -Seconds 12`

Read the line at a natural documentary pace — the VO drives the final timing, so take a breath before you start and leave a beat at the end.

## 3. One-time lipsync tool setup

Wav2Lip (easy default):

```
git clone https://github.com/Rudrabha/Wav2Lip C:/tools/Wav2Lip
pip install -r C:/tools/Wav2Lip/requirements.txt
# download wav2lip_gan.pth into C:/tools/Wav2Lip/checkpoints/
```

Then set `face.lipsync.command` in `capture.config.json`:

```
python C:/tools/Wav2Lip/inference.py --checkpoint C:/tools/Wav2Lip/checkpoints/wav2lip_gan.pth --face {video} --audio {audio} --outfile {out}
```

LatentSync (sharper mouth, ComfyUI) works the same way — any command that takes a video + audio and writes a lipsynced MP4 to `{out}` is compatible.

## 4. Run it

```
npm run face
```

The script lipsyncs, trims to `face.trim_seconds`, scales to 1920x1080, muxes your VO as the audio track (Veo's voice muted), writes `../001-ai-lost-cause/assets/face-hook.mp4`, and adds the S1 ledger entry. The renderer picks it up with zero pipeline changes.
