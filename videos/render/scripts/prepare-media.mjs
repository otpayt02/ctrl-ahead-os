import {copyFile, mkdir, readdir, readFile, writeFile} from 'node:fs/promises';
import {existsSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {parseFile} from 'music-metadata';

const here = path.dirname(fileURLToPath(import.meta.url));
const project = path.resolve(here, '..');
const videos = path.resolve(project, '..');
const manifestPath = process.env.VIDEO_MANIFEST
  ? path.resolve(process.env.VIDEO_MANIFEST)
  : path.join(videos, '001-ai-lost-cause', 'manifest.json');
const manifest = JSON.parse(await readFile(manifestPath, 'utf8'));
const videoFolder = path.dirname(manifestPath);
const ledgerPath = path.join(videoFolder, 'evidence', 'evidence_manifest.json');
if (existsSync(ledgerPath)) {
  const ledger = JSON.parse(await readFile(ledgerPath, 'utf8'));
  const pointers = Array.isArray(ledger) ? ledger : (ledger.pointers ?? ledger.snippets ?? []);
  for (const pointer of pointers) {
    const slot = pointer.manifest_slot;
    const scene = manifest.scenes.find((item) => item.id === slot?.scene);
    if (!scene || !Array.isArray(slot.time_range)) continue;
    scene.manifest_slots ??= [];
    scene.manifest_slots.push({
      id: pointer.id,
      start: Math.max(0, slot.time_range[0] - scene.start),
      end: Math.min(scene.end - scene.start, slot.time_range[1] - scene.start),
      text: pointer.extracted_text || `${pointer.snippet_type} / ${pointer.id}`,
      asset: pointer.uri,
      type: pointer.snippet_type,
      recommended_animation: pointer.recommended_animation,
      annotation: pointer.annotation,
      provenance: pointer.provenance,
    });
  }
}
const captureLedgerPath = path.join(videoFolder, 'evidence-ledger.json');
if (existsSync(captureLedgerPath)) {
  const entries = JSON.parse(await readFile(captureLedgerPath, 'utf8'));
  if (!Array.isArray(entries)) throw new Error('Capture evidence ledger must be an array');
  for (const entry of entries) {
    const scene = manifest.scenes.find((item) => item.id === entry.scene_id);
    if (!scene || !Number.isFinite(entry.start) || !Number.isFinite(entry.end) || entry.end <= entry.start) continue;
    scene.manifest_slots ??= [];
    scene.manifest_slots.push({
      id: entry.id,
      start: Math.max(0, entry.start - scene.start),
      end: Math.min(scene.end - scene.start, entry.end - scene.start),
      text: entry.text,
      asset: entry.asset,
      type: entry.type,
      annotation: entry.annotation,
      provenance: entry.provenance,
    });
  }
}
const assetFolder = path.join(project, 'public', 'scene-assets');
const voOutput = path.join(project, 'public', 'vo');
await mkdir(assetFolder, {recursive: true});
await mkdir(voOutput, {recursive: true});

const availableAssets = [];
for (const scene of manifest.scenes) {
  for (const source of [...(scene.assets ?? []), ...(scene.manifest_slots ?? []).map((slot) => slot.asset)]) {
    if (typeof source !== 'string') continue;
    if (!source.startsWith('assets/')) continue;
    const filename = path.basename(source);
    const input = path.join(videoFolder, 'assets', filename);
    if (!existsSync(input)) continue;
    await copyFile(input, path.join(assetFolder, filename));
    availableAssets.push(filename);
  }
}

const voiceovers = {};
const voiceFolder = path.join(videoFolder, 'vo');
if (existsSync(voiceFolder)) {
  const files = await readdir(voiceFolder);
  for (const scene of manifest.scenes) {
    const filename = files.find((name) => new RegExp(`^${scene.id}\\.(wav|mp3|m4a)$`, 'i').test(name));
    if (!filename) continue;
    const input = path.join(voiceFolder, filename);
    const meta = await parseFile(input);
    const duration = meta.format.duration;
    if (!duration || !Number.isFinite(duration)) throw new Error(`Unable to read VO duration: ${input}`);
    await copyFile(input, path.join(voOutput, filename));
    voiceovers[scene.id] = {file: filename, durationSeconds: duration};
  }
}

const output = {videoId: manifest.video_id, availableAssets: [...new Set(availableAssets)], voiceovers};
await writeFile(path.join(project, 'src', 'generated-media.json'), JSON.stringify(output, null, 2));
await writeFile(path.join(project, 'src', 'generated-manifest.json'), JSON.stringify(manifest, null, 2));
console.log(`${manifest.video_id}: ${output.availableAssets.length} assets; ${Object.keys(voiceovers).length} VO tracks`);
