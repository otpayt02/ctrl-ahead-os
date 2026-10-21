// Record the four EXISTING Perplexity replies used by the S4 narration.
// This opens saved threads; it never submits a new model question.
import {chromium} from 'playwright';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const captureDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const videoDir = path.resolve(captureDir, '../001-ai-lost-cause');
const configPath = path.resolve(captureDir, process.argv[2] ?? 'capture-inputs/s4-replay.json');
const outDir = path.join(captureDir, 'out', 's4-replay');
const outputPath = path.join(videoDir, 'assets', 's4-two-model-replay.mp4');
const ledgerPath = path.join(videoDir, 'evidence-ledger.json');
const bundledFfmpeg = path.resolve(captureDir, '../render/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe');
const ffmpeg = process.env.FFMPEG_PATH || (fs.existsSync(bundledFfmpeg) ? bundledFfmpeg : 'ffmpeg');
const profile = path.join(captureDir, 'auth', 'profile-perplexity');

function sha256(value) {
  return createHash('sha256').update(value).digest('hex');
}

function validate(document) {
  if (!Array.isArray(document.cases) || document.cases.length !== 2 ||
      document.cases[0]?.id !== 'lost-cause' || document.cases[1]?.id !== 'sgaw-karen') {
    throw new Error('Replay config needs lost-cause and sgaw-karen cases, in that order.');
  }
  for (const test of document.cases) {
    if (!Array.isArray(test.sources) || test.sources.length !== 2) {
      throw new Error(`${test.id} needs exactly two saved reply URLs.`);
    }
    for (const source of test.sources) {
      let url;
      try { url = new URL(source.url); } catch { throw new Error(`${test.id}: supply a real thread URL for ${source.name}.`); }
      if (url.protocol !== 'https:' || !['perplexity.ai', 'www.perplexity.ai'].includes(url.hostname)) {
        throw new Error(`${test.id}: ${source.name} must be a Perplexity HTTPS thread URL.`);
      }
      if (typeof source.expected_text !== 'string' || source.expected_text.trim().length < 12 ||
          source.expected_text.includes('PASTE')) {
        throw new Error(`${test.id}: add a visible phrase from ${source.name}'s saved answer.`);
      }
    }
  }
  if (document.seconds_per_test !== 55) {
    throw new Error('Use 55 seconds per test to fill the 190–300 second S4 slot.');
  }
}

async function capture(source, caseId, sourceIndex, seconds) {
  const startedAt = Date.now();
  const context = await chromium.launchPersistentContext(profile, {
    headless: false,
    viewport: {width: 960, height: 1080},
    recordVideo: {dir: outDir, size: {width: 960, height: 1080}},
  });
  try {
    const page = context.pages()[0] ?? await context.newPage();
    await page.goto(source.url, {waitUntil: 'domcontentloaded', timeout: 90000});
    const proof = page.getByText(source.expected_text, {exact: false}).first();
    await proof.waitFor({state: 'visible', timeout: 90000});
    await proof.scrollIntoViewIfNeeded();
    await page.waitForTimeout(750);
    const bounds = await proof.boundingBox();
    if (!bounds || bounds.y >= 1080 || bounds.y + bounds.height <= 0) {
      throw new Error(`${caseId}: expected reply text is not visible for ${source.name}.`);
    }
    const openedAt = new Date().toISOString();
    const readyOffset = Math.max(0, (Date.now() - startedAt) / 1000 - 0.25);
    const screenshot = path.join(outDir, `${caseId}-${sourceIndex + 1}.png`);
    await page.screenshot({path: screenshot});
    console.log(`${caseId}: verified visible reply from ${source.name}; recording ${seconds}s`);
    await page.waitForTimeout((seconds + 2) * 1000);
    const video = page.video();
    await context.close();
    return {
      name: source.name,
      url: source.url,
      expected_text: source.expected_text,
      opened_at: openedAt,
      screenshot,
      screenshot_sha256: sha256(fs.readFileSync(screenshot)),
      raw_video: await video.path(),
      ready_offset_sec: readyOffset,
    };
  } catch (error) {
    await context.close();
    throw error;
  }
}

function renderPair(test, sources, seconds) {
  const pair = path.join(outDir, `${test.id}.mp4`);
  const side = (index) => `[${index}:v]trim=start=${sources[index].ready_offset_sec.toFixed(3)}:duration=${seconds},setpts=PTS-STARTPTS,fps=30,scale=960:1080:force_original_aspect_ratio=decrease,pad=960:1080:(ow-iw)/2:(oh-ih)/2:black,setsar=1[side${index}]`;
  execFileSync(ffmpeg, [
    '-y', '-i', sources[0].raw_video, '-i', sources[1].raw_video,
    '-filter_complex', `${side(0)};${side(1)};[side0][side1]hstack=inputs=2[v]`,
    '-map', '[v]', '-an', '-t', String(seconds), '-c:v', 'libx264', '-crf', '22',
    '-pix_fmt', 'yuv420p', pair,
  ], {stdio: 'inherit'});
  return pair;
}

function replacePendingLedger(sources) {
  const items = JSON.parse(fs.readFileSync(ledgerPath, 'utf8'));
  const pending = items.findIndex((item) => item.id === 'S4-PENDING-TWO-MODEL-CAPTURE');
  const recorded = items.findIndex((item) => item.id === 'S4-RECORDED-TWO-MODEL-CAPTURE');
  const target = pending >= 0 ? pending : recorded;
  if (target < 0) throw new Error('Expected the S4 pending or recorded ledger entry.');
  const isOldClockBug = (item) => item.scene_id === 'S4' && item.type === 'screen-recording' &&
    item.start === 0 && item.end === 110 && item.asset === 'assets/screen-compare.mp4';
  const competing = items.filter((item) => item.scene_id === 'S4' && item.type === 'screen-recording' &&
    item.id !== 'S4-RECORDED-TWO-MODEL-CAPTURE' && !isOldClockBug(item));
  if (competing.length) throw new Error('S4 has another screen recording entry; inspect the ledger before replacing it.');
  items[target] = {
    id: 'S4-RECORDED-TWO-MODEL-CAPTURE', scene_id: 'S4', start: 190, end: 300,
    type: 'screen-recording', asset: 'assets/s4-two-model-replay.mp4',
    text: 'Saved two-model replies for both the Lost Cause and S’gaw Karen tests.',
    annotation: {reason: 'Actual saved model threads; content match awaits Oliver’s review.'},
    provenance: {
      tool: 'Playwright', captured_at: new Date().toISOString(),
      source_url_sha256: sources.map((source) => sha256(source.url)),
      screenshot_sha256: sources.map((source) => source.screenshot_sha256),
      video_sha256: sha256(fs.readFileSync(outputPath)),
      review_status: 'pending owner content review',
      private_url_record: 'videos/capture/out/s4-replay/provenance.json',
    },
  };
  const stale = items.findIndex(isOldClockBug);
  if (stale >= 0) items.splice(stale, 1);
  fs.writeFileSync(ledgerPath, `${JSON.stringify(items, null, 2)}\n`);
}

if (!fs.existsSync(configPath)) {
  throw new Error(`Create ${configPath} from s4-replay.example.json and fill all four real thread URLs.`);
}
const document = JSON.parse(fs.readFileSync(configPath, 'utf8'));
validate(document);
fs.mkdirSync(outDir, {recursive: true});
const evidence = [];
const pairs = [];
for (const test of document.cases) {
  const sources = [];
  for (const [index, source] of test.sources.entries()) {
    sources.push(await capture(source, test.id, index, document.seconds_per_test));
  }
  evidence.push(...sources);
  pairs.push(renderPair(test, sources, document.seconds_per_test));
}
fs.mkdirSync(path.dirname(outputPath), {recursive: true});
execFileSync(ffmpeg, [
  '-y', '-i', pairs[0], '-i', pairs[1],
  '-filter_complex', '[0:v][1:v]concat=n=2:v=1:a=0[v]',
  '-map', '[v]', '-an', '-r', '30', '-c:v', 'libx264', '-crf', '22',
  '-pix_fmt', 'yuv420p', outputPath,
], {stdio: 'inherit'});
if (fs.statSync(outputPath).size < 100000) throw new Error('Output appears incomplete; ledger left pending.');
fs.writeFileSync(path.join(outDir, 'provenance.json'), `${JSON.stringify(evidence, null, 2)}\n`);
replacePendingLedger(evidence);
console.log(`Recorded ${outputPath}; replaced only the S4 pending ledger slot (190–300).`);
