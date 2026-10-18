# Chapter narration slots

The renderer does not create VO. After script approval, place one recorded file per chapter in the video's ignored `vo/` folder, named `S1.wav` through `S8.wav` (MP3 and M4A are also accepted). `npm run prepare` reads the real audio duration with `music-metadata`, copies the audio into ignored render media, and extends a chapter when its VO plus a 0.5-second tail exceeds the manifest's chapter duration. Later chapters move forward. The manifest's original times remain unchanged.

Verified locally with a temporary 30.0-second silent WAV in S1: the 25-second chapter extended to 30.5 seconds, and the composition grew from **19,800 frames / 660.0 seconds** to **19,965 frames / 665.5 seconds** at 30 fps. The temporary WAV and its render copy were removed afterward; `prepare` again reports zero VO tracks.

Use `--enforce-audio-track` for a silent timing draft before approved recordings exist. The full-length draft is for pacing review and does not imply that the narration or cited screen evidence has been recorded.
