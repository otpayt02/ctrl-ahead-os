// Veo clip + owner VO -> full-length face-hook.mp4 (optional local lip sync).
// Veo's synthesized voice is dropped; your recording is the audio track.
import fs from 'node:fs';
import {execFileSync} from 'node:child_process';
import {addEntry} from './ledger.mjs';

const cfg = JSON.parse(fs.readFileSync('capture.config.json', 'utf8'));
const face = cfg.face;
const inDir = face.inputs_dir;
const veoClip = `${inDir}/${face.veo_clip}`;
const voFile = `${inDir}/${face.vo_file}`;
// Remotion's bundled ffmpeg omits audio mastering filters; use a full ffmpeg build.
const ffmpeg = process.env.FFMPEG_PATH || 'ffmpeg';

for (const f of [veoClip, voFile]) {
  if (!fs.existsSync(f)) {
    console.error(`Missing input: ${f}\nDrop the Veo export and your VO recording into ${inDir}/ — see FACE-HOOK.md.`);
    process.exit(1);
  }
}
fs.mkdirSync(cfg.outputs.tmp, {recursive: true});

let videoIn = veoClip;
const lipsyncCmd = (face.lipsync.command ?? '').trim();
if (lipsyncCmd) {
  const lipsynced = `${cfg.outputs.tmp}/face-lipsynced.mp4`;
  const cmd = lipsyncCmd
    .replaceAll('{video}', veoClip)
    .replaceAll('{audio}', voFile)
    .replaceAll('{out}', lipsynced);
  console.log(`Lipsync: ${cmd}`);
  execFileSync(cmd, {shell: true, stdio: 'inherit'});
  if (!fs.existsSync(lipsynced)) { console.error(`Lipsync command did not produce ${lipsynced}`); process.exit(1); }
  videoIn = lipsynced;
} else {
  console.log('No lipsync command set — using the raw Veo clip (set face.lipsync.command in capture.config.json for true sync).');
}

const out = `${cfg.outputs.assets}/${face.out}`;
const staged = `${cfg.outputs.tmp}/face-hook-staged.mp4`;
fs.mkdirSync(cfg.outputs.assets, {recursive: true});
const trim = face.trim_seconds ?? 8;
execFileSync(ffmpeg, [
  '-y', '-i', videoIn, '-i', voFile,
  '-t', String(trim),
  '-map', '0:v:0', '-map', '1:a:0',
  '-vf', 'scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080',
  '-af', `silenceremove=start_periods=1:start_duration=0:start_threshold=-35dB,highpass=f=80,equalizer=f=3000:t=q:w=1:g=2,apad=whole_dur=${trim},atrim=0:${trim},loudnorm=I=-16:TP=-1.5:LRA=7`,
  '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p',
  '-c:a', 'aac', '-b:a', '160k',
  staged,
], {stdio: 'inherit'});
fs.renameSync(staged, out);
console.log(`Saved ${out}`);

addEntry({
  scene_id: 'S1', start: 0, end: trim, type: 'face-footage', asset: `assets/${face.out}`,
  text: 'Face hook: Veo image-to-video with recorded VO replacing source audio.',
  annotation: {reason: 'S1 human face hook — real voice, AI-assisted likeness clip.'},
  provenance: {generator: 'Google Veo (image-to-video)', lipsync: face.lipsync.command ? 'local' : 'none', vo_source: 'recorded'},
});
