import {copyFile, mkdir, readdir, writeFile} from 'node:fs/promises';
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
const manifest = JSON.parse(await (await import('node:fs/promises')).readFile(manifestPath, 'utf8'));
const videoFolder = path.dirname(manifestPath);
const assetFolder = path.join(project, 'public', 'scene-assets');
const voOutput = path.join(project, 'public', 'vo');
await mkdir(assetFolder, {recursive: true});
await mkdir(voOutput, {recursive: true});

const availableAssets = [];
for (const scene of manifest.scenes) {
  for (const source of scene.assets ?? []) {
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
console.log(`${manifest.video_id}: ${output.availableAssets.length} images; ${Object.keys(voiceovers).length} VO tracks`);
